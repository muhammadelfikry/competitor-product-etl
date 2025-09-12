from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def colnum_to_excel_col(n):
    """
    Convert a column number to an Excel-style column letter.

    This function converts a positive integer (1-based index) into 
    the corresponding Excel column label. For example:
        1 -> "A"
        26 -> "Z"
        27 -> "AA"
        52 -> "AZ"
        53 -> "BA"

    Args:
        n (int): The column number (1-based index).

    Returns:
        str: The corresponding Excel-style column label.

    Raises:
        ValueError: If n is not a positive integer.
    """
    try:
        if not isinstance(n, int) or n <= 0:
            raise ValueError("Input must be a positive integer")

        result = ""
        while n > 0:
            n, remainder = divmod(n - 1, 26)
            result = chr(65 + remainder) + result
        
        return result

    except Exception as e:
        print(f"[ERROR] Failed to convert column number to Excel column: {e}")
        return None


def load_to_google_sheets(data):
    """
    Upload a pandas DataFrame to a Google Spreadsheet.

    This function:
        1. Authenticates using a Google service account.
        2. Converts the DataFrame into a list format suitable for Google Sheets.
        3. Calculates the range of cells required to fit the DataFrame.
        4. Updates the Google Sheet with the DataFrame content.

    Args:
        data (pd.DataFrame): The DataFrame to upload.

    Returns:
        None

    Raises:
        Exception: If authentication fails or the upload process encounters an error.
    """
    SERVICE_ACCOUNT_FILE = "./client_secret.json"
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

    try:
        # Authenticate with Google Sheets API
        credential = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        # Target Google Spreadsheet ID (should be stored in env/secure config ideally)
        SPREADSHEET_ID = "spreadsheet_id"

        # Determine DataFrame shape
        num_rows, num_cols = data.shape

        # Define the cell range for writing
        start_cell = "A1"
        end_col = colnum_to_excel_col(num_cols)
        end_row = num_rows + 1  # +1 for header
        end_cell = f"{end_col}{end_row}"
        RANGE_NAME = f"Sheet1!{start_cell}:{end_cell}"

        # Prepare Google Sheets API client
        service = build('sheets', 'v4', credentials=credential)
        sheet = service.spreadsheets()

        # Prepare body (header + data rows)
        values = [data.columns.tolist()] + data.values.tolist()
        body = {"values": values}

        # Update sheet values
        sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_NAME,
            valueInputOption='RAW',
            body=body
        ).execute()

        print("Successfully added data to Google Spreadsheets!")

    except Exception as e:
        print(f"Failed to add data: {e}")
