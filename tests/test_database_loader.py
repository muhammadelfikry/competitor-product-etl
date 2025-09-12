import pandas as pd
from unittest.mock import patch, MagicMock
from utils.database_loader import load_to_database

# ---------- Test load_to_database ----------

def test_load_to_database_success():
    """
    Test case for load_to_database when data is successfully saved.

    This test verifies that:
    - `create_engine` is called exactly once.
    - `engine.connect` is called to establish the connection.
    - `to_sql` is called with the correct parameters (`if_exists="append"`).

    Steps:
        1. Patch `create_engine` so it does not connect to a real database.
        2. Mock the engine and connection objects.
        3. Patch `to_sql` method of DataFrame to avoid actual DB operations.
        4. Call `load_to_database` and assert the expected calls.
    """
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    table_name = "test_table"

    # Patch create_engine so it doesn't connect to the real DB
    with patch("utils.database_loader.create_engine") as mock_create_engine:
        # Mock object engine and connect
        mock_engine = MagicMock()
        mock_connection = MagicMock()
        mock_create_engine.return_value = mock_engine
        mock_engine.connect.return_value.__enter__.return_value = mock_connection

        # Patch to_sql so that it does not actually write
        with patch.object(df, "to_sql", return_value=None) as mock_to_sql:
            load_to_database(df, table_name)

            # Ensure that create_engine is called
            mock_create_engine.assert_called_once()
            # Ensure that connect is called
            mock_engine.connect.assert_called_once()
            # Ensure that to_sql is called with the correct parameters
            mock_to_sql.assert_called_once_with(table_name, con=mock_connection, if_exists="append", index=False)


def test_load_to_database_exception():
    """
    Test case for load_to_database when an exception occurs.

    This test simulates a database connection failure by forcing
    `create_engine` to raise an Exception.

    Expected behavior:
        - `load_to_database` should handle the exception gracefully.
        - The test passes if the exception is caught and does not propagate.
    """
    df = pd.DataFrame({"A": [1, 2]})
    table_name = "test_table"

    # Simulation create_engine throws an exception
    with patch("utils.database_loader.create_engine", side_effect=Exception("Koneksi gagal")):
        load_to_database(df, table_name)
        # The test is successful if the exception is handled (not raised).