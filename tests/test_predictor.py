import unittest
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.predictor.predictor import predict_signal
from backend.collectors.fetcher import fetch_latest

class TestPredictor(unittest.TestCase):
    """
    Tests for the rule-based predictor.
    """

    def test_predictor_runs_without_errors(self):
        """
        Verify that predict_signal runs without raising exceptions.
        """
        try:
            # Fetch real or simulated data
            df = fetch_latest("NIFTY") 
            self.assertIsNotNone(df, "Data fetching failed.")
            
            # Run prediction
            predict_signal(df)
        except Exception as e:
            self.fail(f"predict_signal raised an exception: {e}")

    def test_predictor_output_format(self):
        """
        Verify that the predictor returns a dictionary with the correct keys.
        """
        df = fetch_latest("BANKNIFTY")
        self.assertIsNotNone(df, "Data fetching failed.")

        result = predict_signal(df)

        # Check if the result is a dictionary
        self.assertIsInstance(result, dict, "Output should be a dictionary.")

        # Check for mandatory keys
        self.assertIn("signal", result)
        self.assertIn("confidence", result)
        self.assertIn("reason", result)

        # Check data types and constraints
        self.assertIsInstance(result["signal"], str, "Signal should be a string.")
        self.assertIn(result["signal"], ["BUY", "SELL", "HOLD"], "Signal has an invalid value.")
        self.assertIsInstance(result["confidence"], float, "Confidence should be a float.")
        self.assertTrue(0.0 <= result["confidence"] <= 1.0, "Confidence must be between 0.0 and 1.0.")
        self.assertIsInstance(result["reason"], str, "Reason should be a string.")

if __name__ == '__main__':
    unittest.main()
