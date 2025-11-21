from dotenv import load_dotenv
load_dotenv()

import sys
sys.path.insert(0, '.')

from backend.agents.collectors.market_data import NSEDataCollector

print("=" * 60)
print("TESTING ANGEL ONE API CONNECTION")
print("=" * 60)

# Initialize collector
collector = NSEDataCollector()
print(f"\n✓ Collector initialized")
print(f"  Status: {collector.status}")
print(f"  Angel Client: {'Connected' if collector.angel_client else 'Not Connected'}")

# Fetch live data
print("\n▶ Fetching live market data...")
indices = collector.get_indices()

print("\n=== LIVE MARKET DATA ===")
for name, data in indices.items():
    print(f"\n{name}:")
    print(f"  Price: {data['price']}")
    print(f"  Open: {data['open']}")
    print(f"  High: {data['high']}")  
    print(f"  Low: {data['low']}")
    print(f"  Prev Close: {data['prev_close']}")

print("\n" + "=" * 60)
print("If you see 0.0 values, Angel One credentials are missing/invalid")
print("If you see real values (23,000+), Angel One API is working! ✓")
print("=" * 60)
