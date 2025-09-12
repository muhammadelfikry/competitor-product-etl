import pandas as pd
from utils.transform import transform_to_DataFrame, transform_data
import datetime

# ---------- Test transform_to_DataFrame ----------
def test_transform_to_DataFrame_success():
    data = [
        {"Title": "Product A", "Price": "$10", "Rating": "⭐ 4.5 / 5",
         "Colors": "3 Colors", "Size": "Size: M", "Gender": "Gender: Men",
         "Timestamp": datetime.datetime.now()}
    ]
    df = transform_to_DataFrame(data)
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 1
    assert df["Title"].iloc[0] == "Product A"

def test_transform_to_DataFrame_empty_list():
    df = transform_to_DataFrame([])
    assert isinstance(df, pd.DataFrame)
    assert df.empty

def test_transform_to_DataFrame_invalid_input():
    df = transform_to_DataFrame(None)
    assert df is None

# ---------- Test transform_data ----------
def test_transform_data_success():
    raw_data = [
        {"Title": "Product A", "Price": "$10", "Rating": "⭐ 4.5 / 5",
         "Colors": "3 Colors", "Size": "Size: M", "Gender": "Gender: Men",
         "Timestamp": datetime.datetime.now()},
        {"Title": "Product B", "Price": "$20", "Rating": "⭐ 3.9 / 5",
         "Colors": "2 Colors", "Size": "Size: L", "Gender": "Gender: Women",
         "Timestamp": datetime.datetime.now()},
        {"Title": "Unknown Product", "Price": "$15", "Rating": "⭐ 4.0 / 5",
         "Colors": "1 Colors", "Size": "Size: S", "Gender": "Gender: Unisex",
         "Timestamp": datetime.datetime.now()},
        {"Title": "Product C", "Price": "Price Unavailable", "Rating": "⭐ 5.0 / 5",
         "Colors": "5 Colors", "Size": "Size: XL", "Gender": "Gender: Men",
         "Timestamp": datetime.datetime.now()}
    ]
    df = transform_to_DataFrame(raw_data)
    transformed_df = transform_data(df, exchange_rate=16000)

    # Only Products A and B are valid
    assert transformed_df.shape[0] == 2

    # The Price column directly contains IDR 
    assert "Price" in transformed_df.columns
    assert all(transformed_df["Price"] > 0)

    # Ensure that the conversion value is correct
    assert transformed_df.loc[transformed_df["Title"] == "Product A", "Price"].iloc[0] == 160000
    assert transformed_df.loc[transformed_df["Title"] == "Product B", "Price"].iloc[0] == 320000

    # Check the data type of other columns
    assert transformed_df["Rating"].dtype == float
    assert transformed_df["Colors"].dtype == int
    assert transformed_df["Size"].dtype == object  
    assert transformed_df["Gender"].dtype == object  


def test_transform_data_invalid_input():
    result = transform_data(None, exchange_rate=16000)
    assert result is None


def test_transform_data_error_handling():
    # DataFrame with incorrect columns
    df = pd.DataFrame({"WrongCol": [1, 2, 3]})
    result = transform_data(df, exchange_rate=16000)
    assert result is None