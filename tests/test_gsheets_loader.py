import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from utils.gsheets_loader import colnum_to_excel_col, load_to_google_sheets 

# ---------- Test colnum_to_excel_col ----------
@pytest.mark.parametrize("input_val,expected", [
    (1, "A"),
    (26, "Z"),
    (27, "AA"),
    (52, "AZ"),
    (53, "BA"),
    (702, "ZZ"),
    (703, "AAA")
])
def test_colnum_to_excel_col(input_val, expected):
    assert colnum_to_excel_col(input_val) == expected

# ---------- Test load_to_google_sheets ----------
def test_load_to_google_sheets_success():
    # DataFrame dummy
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})

    with patch("utils.gsheets_loader.Credentials.from_service_account_file") as mock_cred, \
         patch("utils.gsheets_loader.build") as mock_build:

        # Mock credentials object
        mock_cred.return_value = MagicMock()

        # Mock service and sheet.values().update().execute()
        mock_service = MagicMock()
        mock_sheet = MagicMock()
        mock_service.spreadsheets.return_value = mock_sheet
        mock_build.return_value = mock_service

        # Call the function
        load_to_google_sheets(df)

        # Ensure the build is called
        mock_build.assert_called_once()
        # Ensure that values().update().execute() is called
        mock_sheet.values.return_value.update.assert_called_once()
        mock_sheet.values.return_value.update.return_value.execute.assert_called_once()

def test_load_to_google_sheets_exception():
    df = pd.DataFrame({"A": [1]})

    # Credential simulation triggers an exception
    with patch("utils.gsheets_loader.Credentials.from_service_account_file", side_effect=Exception("Auth gagal")):
        load_to_google_sheets(df)
        # The test is successful if the exception is handled (not raised).