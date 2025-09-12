from sqlalchemy import create_engine

def load_to_database(data, table_name):
    """
    Save a DataFrame into a PostgreSQL database table.

    This function connects to a PostgreSQL database using SQLAlchemy,
    then writes the given DataFrame into the specified table.
    If the table already exists, it will be replaced.

    Args:
        data (pd.DataFrame): The DataFrame to be stored in the database.
        table_name (str): The name of the database table.

    Returns:
        None

    Raises:
        Exception: If the connection or data saving fails.
    """
    try:
        # Define database connection URL
        DATABASE_URL = "database_url"
        engine = create_engine(DATABASE_URL)

        # Establish connection to the database
        with engine.connect() as connection:
            print("Connected to the database!")

            # Save DataFrame into the database table
            print("Saving DataFrames to a database")
            data.to_sql(table_name, con=connection, if_exists="append", index=False)
            print("DataFrame successfully added!")

    except Exception as e:
        print(f"An error occurred while saving to the database: {e}")
