def load_to_csv(data, file_name):
    """
    Save a DataFrame to a CSV file.

    Args:
        data (pd.DataFrame): The DataFrame to be saved.
        file_name (str): The name of the CSV file to save.

    Returns:
        None
    """
    try:
        print("Saving DataFrame in .csv format")
        data.to_csv(file_name, index=False)
        print("Data successfully saved!")

    except Exception as e:
        print(f"An error occurred while saving the DataFrame: {e}")
