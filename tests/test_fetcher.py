import unittest
import sys
import os

# Add project root to path to allow for imports from backend
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.collectors.fetcher import fetch_latest, YFINANCE_INSTALLED

# We need a DataFrame to check against, even if it's the dummy one
if YFINANCE_INSTALLED:
    import pandas as pd
    DataFrame = pd.DataFrame
else:
    # If yfinance is not installed, fetcher.py creates a dummy DataFrame
    from backend.collectors.fetcher import DataFrame


class TestFetcher(unittest.TestCase):

    def test_fetch_latest_returns_dataframe(self):
        """
        Tests that fetch_latest returns a DataFrame (real or simulated).
        """
        symbol = "^NSEI"  # NIFTY
        data = fetch_latest(symbol)
        self.assertIsInstance(data, DataFrame, "Function should return a DataFrame instance.")

    def test_fetch_latest_dataframe_not_empty(self):
        """
        Tests that the returned DataFrame is not empty.
        """
        symbol = "^NSEBANK"  # BANKNIFTY
        data = fetch_latest(symbol)
        self.assertFalse(data.empty, "Returned DataFrame should not be empty.")

    def test_fetch_latest_has_required_columns(self):
        """
        Tests that the returned DataFrame has the required OHLCV columns.
        """
        symbol = "^NSEI"
        data = fetch_latest(symbol)
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        self.assertTrue(all(col in data.columns for col in required_columns), f"DataFrame must contain {required_columns}")


if __name__ == '__main__':
    # This allows running the tests directly from the command line
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestFetcher)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    # Exit with a non-zero status if tests failed, useful for CI
    sys.exit(not result.wasSuccessful())
