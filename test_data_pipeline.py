import sys
import os
import time

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.data_providers.manager import DataProviderManager
from backend.data.tickers import ALL_TICKERS

def test_pipeline():
    print("--- Testing Real Data Pipeline ---")
    
    manager = DataProviderManager()
    
    # 1. Test Single Symbol Fetch (Yahoo)
    symbol = "RELIANCE.NS"
    print(f"\n1. Fetching Live Price for {symbol}...")
    price = manager.get_live_price(symbol)
    if price:
        print(f"✅ Success: {symbol} Price = {price}")
    else:
        print(f"❌ Failed to fetch price for {symbol}")

    # 2. Test Historical Data
    print(f"\n2. Fetching Historical Data for {symbol}...")
    df = manager.get_historical_data(symbol, period="5d")
    if df is not None and not df.empty:
        print(f"✅ Success: Fetched {len(df)} rows")
        print(df.head())
    else:
        print(f"❌ Failed to fetch historical data")

    # 3. Test Ticker List Expansion
    print(f"\n3. Verifying Ticker List...")
    print(f"Total Tickers: {len(ALL_TICKERS)}")
    if len(ALL_TICKERS) > 50:
        print("✅ Ticker list expanded correctly (NIFTY 500 subset)")
    else:
        print("❌ Ticker list seems small")

    # 4. Test Scanner Logic (Small Subset)
    print("\n4. Testing Scanner Logic (First 5 symbols)...")
    from backend.intelligence.scanner import MorningScanner
    scanner = MorningScanner()
    
    # Monkey patch ALL_TICKERS to just test 5 to save time
    original_tickers = scanner.scan_market.__globals__['ALL_TICKERS']
    scanner.scan_market.__globals__['ALL_TICKERS'] = ALL_TICKERS[:5]
    
    try:
        report = scanner.scan_market()
        print("\nGenerated Report Snippet:")
        print(report[:200] + "...")
        print("✅ Scanner ran successfully")
    except Exception as e:
        print(f"❌ Scanner failed: {e}")

if __name__ == "__main__":
    test_pipeline()
