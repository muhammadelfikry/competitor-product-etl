import pandas as pd
from unittest.mock import MagicMock, patch
from utils.csv_loader import load_to_csv  

# ---------- Test load_to_csv ----------

def test_load_to_csv_success():
    """
    Test case for load_to_csv when data is successfully saved.

    This test verifies that:
    - The `to_csv` method of DataFrame is called exactly once.
    - The parameters passed to `to_csv` are correct (`file_name`, `index=False`).

    Steps:
        1. Create a dummy DataFrame.
        2. Patch `to_csv` to avoid writing an actual file.
        3. Call `load_to_csv`.
        4. Assert that `to_csv` was called once with the expected arguments.
    """
    # Create a dummy DataFrame
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    
    # Mock method to_csv
    with patch.object(df, "to_csv", return_value=None) as mock_to_csv:
        load_to_csv(df, "dummy.csv")
        # Ensure that to_csv is called once with the correct parameters
        mock_to_csv.assert_called_once_with("dummy.csv", index=False)


def test_load_to_csv_exception():
    """
    Test case for load_to_csv when an exception occurs.

    This test simulates a failure during the `to_csv` operation
    (e.g., "Disk full"). The function should handle the exception
    gracefully without propagating it.

    Expected behavior:
        - `to_csv` is still called once with the expected parameters.
        - The exception is caught inside `load_to_csv`, so the test
          does not raise an error.
    """
    df = pd.DataFrame({"A": [1, 2]})
    
    # Create a mock to_csv that throws an exception
    with patch.object(df, "to_csv", side_effect=Exception("Disk full")) as mock_to_csv:
        load_to_csv(df, "dummy.csv")
        mock_to_csv.assert_called_once_with("dummy.csv", index=False)
        # The test only ensures that the exception is handled; no need to raise it.