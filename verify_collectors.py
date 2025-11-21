from backend.agents.collectors.market_data import NSEDataCollector
from backend.agents.collectors.technical import TechnicalIndicatorCollector
from backend.agents.collectors.order_book import OrderBookAnalyzer
from backend.agents.collectors.news_events import NewsEventCollector
from backend.agents.collectors.historical import HistoricalDataManager

def verify_collectors():
    print("--- Verifying Collectors ---")
    
    # 1. Market Data
    print("\n1. Testing NSEDataCollector...")
    try:
        c1 = NSEDataCollector()
        data = c1.collect()
        if "NIFTY" in data:
            print("PASS: Fetched NIFTY data")
        else:
            print("FAIL: No NIFTY data")
    except Exception as e:
        print(f"FAIL: {e}")

    # 2. Technical
    print("\n2. Testing TechnicalIndicatorCollector...")
    try:
        c2 = TechnicalIndicatorCollector()
        c2.process_symbol("NIFTY")
        print("PASS: Calculated indicators")
    except Exception as e:
        print(f"FAIL: {e}")

    # 3. Order Book
    print("\n3. Testing OrderBookAnalyzer...")
    try:
        c3 = OrderBookAnalyzer()
        c3.analyze("NIFTY")
        print("PASS: Analyzed order book")
    except Exception as e:
        print(f"FAIL: {e}")

    # 4. News
    print("\n4. Testing NewsEventCollector...")
    try:
        c4 = NewsEventCollector()
        c4.collect()
        print("PASS: Collected news")
    except Exception as e:
        print(f"FAIL: {e}")

    # 5. Historical
    print("\n5. Testing HistoricalDataManager...")
    try:
        c5 = HistoricalDataManager()
        c5.download_data("NIFTY", "2024-01-01", "2024-01-02")
        print("PASS: Downloaded historical data")
    except Exception as e:
        print(f"FAIL: {e}")

if __name__ == "__main__":
    verify_collectors()
