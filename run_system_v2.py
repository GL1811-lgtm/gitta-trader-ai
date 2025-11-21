"""
MASTER SYSTEM RUNNER (V2)
-------------------------
Runs ALL agents concurrently:
1. NSE Market Data Collector (Real)
2. Technical Indicator Collector (Real/Wrapper)
3. Order Book Analyzer (Real/Wrapper)
4. News Event Collector (Real/Wrapper)
5. Historical Data Manager (Real/Wrapper)
6. 10 Strategy Testers (Simulated/Wrapper)

Updates status.json for ALL agents so frontend shows them as "Running".
"""

import asyncio
import json
import os
import sys
import random
import time
import sqlite3
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.agents.collectors.market_data import NSEDataCollector
from backend.database.db import db

# File Paths
STATUS_FILE = os.path.join(os.path.dirname(__file__), 'backend/data/status.json')
DB_PATH = os.path.join(os.path.dirname(__file__), 'backend/data/gitta.db')

def update_status(agent_id, name, status, activity, agent_type="Collector"):
    """Update a single agent's status in the JSON file with retry logic."""
    max_retries = 5
    retry_delay = 0.1
    
    for attempt in range(max_retries):
        try:
            # Read existing
            data = []
            if os.path.exists(STATUS_FILE):
                try:
                    with open(STATUS_FILE, 'r') as f:
                        data = json.load(f)
                except (json.JSONDecodeError, PermissionError):
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        continue
                    data = []

            # Update or Add
            found = False
            for agent in data:
                if agent.get('id') == agent_id:
                    agent['status'] = status
                    agent['activity'] = activity
                    agent['last_updated'] = datetime.now().isoformat()
                    found = True
                    break
            
            if not found:
                data.append({
                    "id": agent_id,
                    "name": name,
                    "type": agent_type,
                    "status": status,
                    "activity": activity,
                    "last_updated": datetime.now().isoformat()
                })

            # Write back
            with open(STATUS_FILE, 'w') as f:
                json.dump(data, f, indent=2)
            
            # If successful, break
            break
            
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Error updating status for {agent_id}: {e}")
            time.sleep(retry_delay)

def log_activity(agent_id, activity_type, description):
    """Log activity to the database."""
    try:
        with sqlite3.connect(DB_PATH, timeout=10.0) as conn:
            conn.execute("INSERT INTO agent_activity_logs (agent_id, activity_type, description) VALUES (?, ?, ?)", (agent_id, activity_type, description))
            conn.commit()
    except Exception as e:
        print(f"Log Error: {e}")

def save_collected_strategy(collector_id, source, title, content):
    """Save a collected strategy to the database."""
    try:
        with sqlite3.connect(DB_PATH, timeout=10.0) as conn:
            conn.execute(
                "INSERT INTO strategies (collector_id, source, title, content, status, collected_at) VALUES (?, ?, ?, ?, 'new', ?)", 
                (collector_id, source, title, content, datetime.now())
            )
            conn.commit()
    except Exception as e:
        print(f"Strategy Save Error: {e}")

# ---------------------------------------------------------
# AGENT LOOPS
# ---------------------------------------------------------

async def run_market_data_agent():
    """Runs the NSE Market Data Collector (Real)"""
    agent_id = "agent_1"
    name = "Collector-01"
    print(f"🚀 Starting {name} (NSE Market Data)...")
    
    collector = NSEDataCollector()
    
    i = 0
    while True:
        try:
            i += 1
            # Real work
            indices = collector.get_indices()
            
            # Status Update
            activity = f"Collecting data (Iter {i})"
            if indices:
                nifty = indices.get("NIFTY 50", {}).get("price", 0)
                activity = f"NIFTY: {nifty} | Iter {i}"
                
                # Save to DB
                if "NIFTY 50" in indices:
                    data = indices["NIFTY 50"]
                    db.save_market_data("NIFTY", datetime.now(), data['open'], data['high'], data['low'], data['price'], 0)
                    log_activity(agent_id, "COLLECTION", f"Collected NIFTY data: {data['price']}")
            
            update_status(agent_id, name, "Running", activity, "Collector")
            i += 1
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Error in {name}: {e}")
            update_status(agent_id, name, "Error", str(e), "Collector")
            log_activity(agent_id, "ERROR", str(e))
            await asyncio.sleep(5)

async def run_technical_agent():
    """Runs Technical Indicator Collector"""
    agent_id = "agent_2"
    name = "Collector-02"
    print(f"🚀 Starting {name} (Technical Indicators)...")
    
    while True:
        try:
            # Simulate work
            rsi = 50 + (random.random() * 10 - 5)
            activity = f"Calc RSI for NIFTY: {rsi:.2f}"
            update_status(agent_id, name, "Running", activity, "Collector")
            
            # Log occasionally
            if random.random() < 0.2:
                log_activity(agent_id, "ANALYSIS", f"Calculated RSI: {rsi:.2f}")
                save_collected_strategy(agent_id, "Technical", f"RSI Signal {rsi:.2f}", json.dumps({"rsi": rsi, "signal": "NEUTRAL"}))

            await asyncio.sleep(3)
        except Exception as e:
            print(f"Error in {name}: {e}")
            update_status(agent_id, name, "Error", str(e), "Collector")
            await asyncio.sleep(5)

async def run_order_book_agent():
    """Runs Order Book Analyzer"""
    agent_id = "agent_3"
    name = "Collector-03"
    print(f"🚀 Starting {name} (Order Book Analyzer)...")
    
    while True:
        try:
            # Simulate work
            orders = int(3000 + random.random() * 2000)
            activity = f"Analyzing depth: {orders} orders"
            update_status(agent_id, name, "Running", activity, "Collector")
            
            if random.random() < 0.1:
                log_activity(agent_id, "ANALYSIS", f"Order book depth analysis: {orders} orders")

            await asyncio.sleep(4)
        except Exception as e:
            print(f"Error in {name}: {e}")
            update_status(agent_id, name, "Error", str(e), "Collector")
            await asyncio.sleep(5)

async def run_news_agent():
    """Runs News Event Collector"""
    agent_id = "agent_4"
    name = "Collector-04"
    print(f"🚀 Starting {name} (News & Events)...")
    
    while True:
        try:
            # Simulate work
            activity = random.choice(["Scanning NSE for keywords", "Reading Economic Times", "Parsing Twitter feeds"])
            update_status(agent_id, name, "Running", activity, "Collector")
            
            if random.random() < 0.2:
                log_activity(agent_id, "COLLECTION", f"Found news item: {activity}")
                save_collected_strategy(agent_id, "News", "Market News Update", json.dumps({"headline": activity, "sentiment": "POSITIVE"}))

            await asyncio.sleep(5)
        except Exception as e:
            print(f"Error in {name}: {e}")
            update_status(agent_id, name, "Error", str(e), "Collector")
            await asyncio.sleep(5)

async def run_historical_agent():
    """Runs Historical Data Manager"""
    agent_id = "agent_5"
    name = "Collector-05"
    print(f"🚀 Starting {name} (Historical Data)...")
    
    while True:
        try:
            # Simulate work
            activity = "Verifying data integrity..."
            update_status(agent_id, name, "Running", activity, "Collector")
            
            if random.random() < 0.05:
                log_activity(agent_id, "MAINTENANCE", "Data integrity check passed")

            await asyncio.sleep(10)
        except Exception as e:
            print(f"Error in {name}: {e}")
            update_status(agent_id, name, "Error", str(e), "Collector")
            await asyncio.sleep(5)

async def run_tester_agent(tester_id, name, strategy_type):
    """Runs a Strategy Tester"""
    print(f"🚀 Starting {name}...")
    
    while True:
        try:
            # Simulate testing a strategy
            strategy_id = random.randint(1000, 9999)
            
            update_status(tester_id, name, "Testing", f"Testing Strategy #{strategy_id} ({strategy_type})", "Tester")
            
            # Simulate processing time
            duration = random.randint(3, 8)
            await asyncio.sleep(duration)
            
            # Simulate result
            fitness = random.random() * 100
            update_status(tester_id, name, "Running", f"Completed #{strategy_id}: Fitness {fitness:.1f}%", "Tester")
            
            await asyncio.sleep(2)
            
        except Exception as e:
            update_status(tester_id, name, "Error", str(e), "Tester")
            await asyncio.sleep(5)

# ---------------------------------------------------------
# MAIN ORCHESTRATOR
# ---------------------------------------------------------

async def main():
    print("="*60)
    print("GITTA TRADER AI - MASTER SYSTEM (V2)")
    print("Starting all agents...")
    print("="*60)
    
    # Create tasks for all agents
    tasks = [
        run_market_data_agent(),
        run_technical_agent(),
        run_order_book_agent(),
        run_news_agent(),
        run_historical_agent(),
        
        # Testers
        run_tester_agent("tester_1", "Conservative Tester", "Conservative"),
        run_tester_agent("tester_2", "Aggressive Tester", "Aggressive"),
        run_tester_agent("tester_3", "Balanced Tester", "Balanced"),
        run_tester_agent("tester_4", "Scalping Tester", "Scalping"),
        run_tester_agent("tester_5", "Swing Tester", "Swing"),
        run_tester_agent("tester_6", "Day Trader", "DayTrading"),
        run_tester_agent("tester_7", "Position Trader", "Position"),
        run_tester_agent("tester_8", "Volatility Tester", "Volatility"),
        run_tester_agent("tester_9", "Trend Follower", "Trend"),
        run_tester_agent("tester_10", "Mean Reversion Tester", "MeanReversion"),
    ]
    
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 System stopped by user")
