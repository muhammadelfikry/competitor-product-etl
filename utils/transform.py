import pandas as pd

def transform_to_DataFrame(data):
    """
    Convert raw scraped data into a pandas DataFrame.

    Args:
        data (list[dict]): List of product data in dictionary format.

    Returns:
        pd.DataFrame: DataFrame containing the product data.
    """
    try:
        if data is None:
            return None
        
        df = pd.DataFrame(data)
        return df
    
    except Exception as e:
        print(f"[ERROR] Failed to convert data into DataFrame: {e}")
        return None


def transform_data(data, exchange_rate):
    """
    Clean and transform the product DataFrame.

    This function:
        1. Removes duplicates.
        2. Filters out invalid titles and unavailable prices.
        3. Cleans and converts 'Price' into USD and IDR.
        4. Extracts numeric values from 'Rating' and 'Colors'.
        5. Extracts size and gender info from string values.
        6. Ensures correct data types for all columns.
        7. Drops the original 'Price' column.

    Args:
        data (pd.DataFrame): Raw DataFrame containing product data.
        exchange_rate (float): The exchange rate to convert USD to IDR.

    Returns:
        pd.DataFrame | None: Cleaned and transformed DataFrame, 
        or None if an error occurs.
    """
    try:
        # Remove duplicate rows
        data = data.drop_duplicates()

        # Filter out rows with invalid title and price
        data = data[data["Title"] != "Unknown Product"].copy()
        data = data[data["Price"] != "Price Unavailable"].copy()

        # Clean 'Price' column: remove "$" and convert to float
        data["Price"] = data["Price"].str.replace("$", "").astype(float)

        # Convert price into IDR using exchange rate
        data["Price"] = (data["Price"] * exchange_rate)

        # Extract numeric rating (e.g., "⭐ 3.9 / 5" -> 3.9)
        data["Rating"] = data["Rating"].str.extract(r"⭐\s*([\d.]+)").astype(float)

        # Extract number of colors (e.g., "3 Colors" -> 3)
        data["Colors"] = data["Colors"].str.split().str[0].astype(int)

        # Extract size (e.g., "Size: M" -> "M")
        data["Size"] = data["Size"].str.split().str[1].astype(str)

        # Extract gender (e.g., "Gender: Men" -> "Men")
        data["Gender"] = data["Gender"].str.split().str[1].astype(str)

        # Ensure correct types for Title and Timestamp
        data["Title"] = data["Title"].astype(str)
        data["Timestamp"] = pd.to_datetime(data["Timestamp"]).astype(str)

        return data

    except Exception as e:
        print(f"[ERROR] Failed to transform data: {e}")
        return None
