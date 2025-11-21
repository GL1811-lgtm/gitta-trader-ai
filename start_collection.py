"""
Simple script to start continuous data collection.
This runs all collector agents in continuous mode.
"""

import sys
import os
import asyncio
import time
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.agents.collectors.market_data import NSEDataCollector
from backend.database.db import db

print("=" * 70)
print("🚀 GITTA TRADER AI - CONTINUOUS DATA COLLECTION")
print("=" * 70)
print(f"\n⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Initialize collector
collector = NSEDataCollector()

print(f"✓ NSEDataCollector initialized")
print(f"  Status: {collector.status}")
print(f"  Angel One: {'✅ Connected' if collector.angel_client else '❌ Not Connected'}")
print()

if collector.status not in ['connected_angel_one', 'error_no_credentials', 'error_missing_credentials']:
    print("=" * 70)
    print("⚠️  WARNING: Angel One API may not be configured properly")
    print("   The system will attempt to collect data anyway...")
    print("=" * 70)
    print()

print("📊 Starting continuous market data collection...")
print("   - Interval: Every 3 seconds")
print("   - Symbols: NIFTY 50, BANKNIFTY")
print("   - Database: backend/data/gitta.db")
print()
print("🛑 Press Ctrl+C to stop")
print("=" * 70)
print()

try:
    # Run continuous collection
    asyncio.run(collector.run_continuously(interval_minutes=1))
except KeyboardInterrupt:
    print("\n\n" + "=" * 70)
    print("🛑 Stopping data collection...")
    print(f"⏰ Stopped at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Show summary
    latest_nifty = db.get_latest_market_data('NIFTY')
    latest_bn = db.get_latest_market_data('BANKNIFTY')
    
    if latest_nifty:
        print(f"\n📈 Latest NIFTY: {latest_nifty.get('close', 'N/A')}")
    if latest_bn:
        print(f"📈 Latest BANKNIFTY: {latest_bn.get('close', 'N/A')}")
    
    print("\n✅ Collection stopped successfully")
    print("=" * 70)
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
