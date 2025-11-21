"""
Improved data collection script with proper status reporting.
Updates status.json so frontend shows agents as active.
"""

import sys
import os
import asyncio
import json
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.agents.collectors.market_data import NSEDataCollector
from backend.database.db import db

def update_agent_status(agent_id, name, status, activity):
    """Update the status.json file so frontend knows agent is running."""
    status_file = os.path.join(os.path.dirname(__file__), 'backend/data/status.json')
    
    try:
        # Read existing status
        if os.path.exists(status_file):
            with open(status_file, 'r') as f:
                all_status = json.load(f)
        else:
            all_status = []
        
        # Update or add this agent's status
        agent_found = False
        for agent in all_status:
            if agent.get('id') == agent_id:
                agent['status'] = status
                agent['activity'] = activity
                agent['last_updated'] = datetime.now().isoformat()
                agent_found = True
                break
        
        if not agent_found:
            all_status.append({
                'id': agent_id,
                'name': name,
                'type': 'Collector',
                'status': status,
                'activity': activity,
                'last_updated': datetime.now().isoformat()
            })
        
        # Write back
        with open(status_file, 'w') as f:
            json.dump(all_status, f, indent=2)
            
    except Exception as e:
        print(f"⚠️  Warning: Could not update status file: {e}")

print("=" * 70)
print("🚀 GITTA TRADER AI - CONTINUOUS DATA COLLECTION (v2)")
print("=" * 70)
print(f"\n⏰ Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Initialize collector
collector = NSEDataCollector()

print(f"✓ NSEDataCollector initialized")
print(f"  Status: {collector.status}")
print(f"  Angel One: {'✅ Connected' if collector.angel_client else '❌ Not Connected'}")
print()

# Update status file to show as "Active"
update_agent_status(
    agent_id='market_data',
    name='NSE Market Data',
    status='Running',
    activity='Collecting market data every 3 seconds'
)
print("✓ Updated status.json - frontend will show agent as ACTIVE")
print()

if collector.status not in ['connected_angel_one']:
    print("=" * 70)
    print("⚠️  WARNING: Angel One API may not be configured properly")
    print("   The system will attempt to collect data anyway...")
    print("=" * 70)
    print()

print("📊 Starting continuous market data collection...")
print("   - Interval: Every 3 seconds")
print("   - Symbols: NIFTY 50, BANKNIFTY")
print("   - Database: backend/data/gitta.db")
print("   - Status Updates: backend/data/status.json")
print()
print("🛑 Press Ctrl+C to stop")
print("=" * 70)
print()

# Track iteration count
iteration = 0

async def run_with_status_updates():
    """Run collection with periodic status updates."""
    global iteration
    
    try:
        while True:
            iteration += 1
            
            # Update status every 10 iterations (every ~30 seconds)
            if iteration % 10 == 0:
                update_agent_status(
                    agent_id='market_data',
                    name='NSE Market Data',
                    status='Running',
                    activity=f'Collecting data (iteration {iteration})'
                )
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✓ Status updated (iteration {iteration})")
            
            # Attempt to collect data
            try:
                indices = collector.get_indices()
                
                if indices:
                    # Save to database
                    if "NIFTY 50" in indices:
                        nifty_data = indices["NIFTY 50"]
                        db.save_market_data(
                            symbol="NIFTY",
                            timestamp=datetime.now(),
                            open_price=nifty_data["open"],
                            high=nifty_data["high"],
                            low=nifty_data["low"],
                            close=nifty_data["price"],
                            volume=0
                        )
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ NIFTY: ₹{nifty_data['price']}")
                    
                    if "BANKNIFTY" in indices:
                        bn_data = indices["BANKNIFTY"]
                        db.save_market_data(
                            symbol="BANKNIFTY",
                            timestamp=datetime.now(),
                            open_price=bn_data["open"],
                            high=bn_data["high"],
                            low=bn_data["low"],
                            close=bn_data["price"],
                            volume=0
                        )
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ BANKNIFTY: ₹{bn_data['price']}")
                else:
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️  No data received, retrying...")
                    
            except Exception as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Error: {e}")
            
            # Wait 3 seconds
            await asyncio.sleep(3)
            
    except KeyboardInterrupt:
        raise
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()

try:
    # Run continuous collection
    asyncio.run(run_with_status_updates())
except KeyboardInterrupt:
    print("\n\n" + "=" * 70)
    print("🛑 Stopping data collection...")
    
    # Update status to show as stopped
    update_agent_status(
        agent_id='market_data',
        name='NSE Market Data',
        status='Stopped',
        activity='Manually stopped by user'
    )
    
    print(f"⏰ Stopped at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Show summary
    latest_nifty = db.get_latest_market_data('NIFTY')
    latest_bn = db.get_latest_market_data('BANKNIFTY')
    
    if latest_nifty:
        print(f"\n📈 Latest NIFTY: ₹{latest_nifty.get('close', 'N/A')}")
    if latest_bn:
        print(f"📈 Latest BANKNIFTY: ₹{latest_bn.get('close', 'N/A')}")
    
    print(f"\n✅ Collection stopped successfully (Total iterations: {iteration})")
    print("=" * 70)
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    
    # Update status to show error
    update_agent_status(
        agent_id='market_data',
        name='NSE Market Data',
        status='Error',
        activity=f'Error: {str(e)[:50]}'
    )
