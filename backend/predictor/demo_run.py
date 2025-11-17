import sys
import os

# Add the project root to the Python path to allow importing from backend
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.collectors.fetcher import fetch_latest
from backend.predictor.predictor import predict_signal, _calculate_rsi

def run_prediction_demo():
    """
    Fetches the latest data, runs the prediction, and prints a clear summary.
    """
    print("─" * 50)
    print("Running Gitta Trader AI - Prediction Demo")
    print("─" * 50)

    # 1. Fetch Data
    symbol = "NIFTY" 
    print(f"Fetching latest data for {symbol}...")
    try:
        df = fetch_latest(symbol)
        if df is None or df.empty:
            print("\nCould not fetch or generate data. Exiting.")
            return
        # Ensure we have enough data for calculations
        if len(df) < 22:
            print(f"\nWarning: Not enough data ({len(df)} rows) for full MA21 calculation. Results may be inaccurate.")
        
        print(f"Successfully fetched {len(df)} data points.")
        print(f"Latest Close Price: {df['Close'].iloc[-1]:.2f}")

    except Exception as e:
        print(f"\nAn error occurred during data fetching: {e}")
        return

    # 2. Run Prediction
    print("\nRunning prediction logic...")
    prediction = predict_signal(df)

    # 3. Display Results
    print("\n" + "─" * 20 + " PREDICTION RESULT " + "─" * 19)
    
    # Recalculate values for display if pandas is available
    try:
        ma9 = df['Close'].rolling(window=9).mean().iloc[-1]
        ma21 = df['Close'].rolling(window=21).mean().iloc[-1]
        rsi = _calculate_rsi(df, window=14)
        print(f"  - Moving Average (9):   {ma9:.2f}")
        print(f"  - Moving Average (21):  {ma21:.2f}")
        print(f"  - Relative Strength Index (RSI): {rsi:.2f}")
    except (TypeError, AttributeError): # Handles case where pandas is not installed
        print("  - Could not calculate indicator values (pandas might be missing).")


    print("\n" + "─" * 23 + " DECISION " + "─" * 23)
    print(f"  Signal:     {prediction['signal']}")
    print(f"  Confidence: {prediction['confidence']:.0%}")
    print(f"  Reason:     {prediction['reason']}")
    print("─" * 50)


if __name__ == "__main__":
    run_prediction_demo()
