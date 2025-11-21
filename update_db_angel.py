from dotenv import load_dotenv
load_dotenv()

import sys
sys.path.insert(0, '.')

from backend.agents.collectors.market_data import NSEDataCollector
from backend.database.db import db

print("=" * 60)
print("UPDATING DATABASE WITH ANGEL ONE DATA")
print("=" * 60)

# Initialize collector
collector = NSEDataCollector()
print(f"\n✓ Collector Status: {collector.status}")

#Fetch and save data
print("\n▶ Fetching live data from Angel One...")
indices = collector.get_indices()

print("\n▶ Saving to database...")
for name, data in indices.items():
    symbol = "NIFTY" if name == "NIFTY 50" else "BANKNIFTY"
    
    success = db.save_market_data(
        symbol=symbol,
        timestamp=__import__('datetime').datetime.now(),
        open_price=data['open'],
        high=data['high'],
        low=data['low'],
        close=data['price'],
        volume=0
    )
    
    if success:
        print(f"  ✓ Saved {name}: {data['price']}")
    else:
        print(f"  ✗ Failed to save {name}")

# Verify database
print("\n▶ Verifying database...")
nifty_db = db.get_latest_market_data("NIFTY")
bn_db = db.get_latest_market_data("BANKNIFTY")

print(f"\n=== DATABASE VALUES ===")
print(f"NIFTY 50: {nifty_db['close'] if nifty_db else 'Not found'}")
print(f"BANKNIFTY: {bn_db['close'] if bn_db else 'Not found'}")

print("\n" + "=" * 60)
print("Database updated! Restart minimal_server.py to see changes.")
print("=" * 60)
