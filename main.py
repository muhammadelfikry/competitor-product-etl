from utils.extract import scrape_fashion
from utils.transform import transform_to_DataFrame, transform_data
from utils.csv_loader import load_to_csv
from utils.database_loader import load_to_database
from utils.gsheets_loader import load_to_google_sheets

def main():
    """
    Run the ETL (Extract, Transform, Load) pipeline for fashion product data.

    This function performs the following steps:
        1. Scrape product data from the source URL.
        2. Convert the scraped data into a pandas DataFrame.
        3. Transform the DataFrame (clean values, convert prices, parse ratings, etc.).
        4. Print the transformed DataFrame.
        5. Save the DataFrame into a CSV file.
        6. Save the DataFrame into Database.
        7. Save the DataFrame into Google Spreadsheets

    If an error occurs at any stage, the function will catch it and print
    an error message without stopping the program.

    Args:
        None

    Returns:
        None
    """
    BASE_URL = "https://fashion-studio.dicoding.dev/"

    try:
        # Step 1: Scrape data from the website
        all_fashion_data = scrape_fashion(BASE_URL)

        if all_fashion_data:
            # Step 2: Convert data into DataFrame
            df = transform_to_DataFrame(all_fashion_data)

            # Step 3: Transform data with exchange rate
            df = transform_data(df, exchange_rate=16000)

            # Step 4: Print transformed DataFrame
            print(df)

            # Step 5: Save transformed DataFrame into CSV
            load_to_csv(df, file_name="products.csv")

            # Step 6: Save transformed DataFrame into Database
            load_to_database(df, "product_records")

            # Step 7: Save transformed DataFrame into Google Spreadsheets
            load_to_google_sheets(df)
        else:
            print("No data found.")

    except Exception as e:
        print(f"[ERROR] ETL pipeline failed: {e}")

if __name__ == "__main__":
    main()