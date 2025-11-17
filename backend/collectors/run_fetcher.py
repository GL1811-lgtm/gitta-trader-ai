import sys
import os

# Add project root to the path to allow importing 'backend'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.collectors.fetcher import fetch_latest

def run():
    """
    Fetches and displays sample data for NIFTY and BANKNIFTY.
    """
    symbols = {
        "NIFTY": "^NSEI",
        "BANKNIFTY": "^NSEBANK"
    }

    for name, symbol in symbols.items():
        print(f"--- Processing {name} ({symbol}) ---")
        df = fetch_latest(symbol)
        print(f"Successfully fetched {len(df)} rows.")
        print("Sample data:")
        print(df.head())
        print("-" * (len(name) + len(symbol) + 20))
        print("\n")

if __name__ == "__main__":
    run()

