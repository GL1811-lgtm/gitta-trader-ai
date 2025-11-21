import sqlite3
import os

DB_PATH = 'backend/data/gitta.db'

try:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    print("--- Strategies by Agent ---")
    rows = c.execute("SELECT collector_id, COUNT(*) FROM strategies WHERE collector_id LIKE 'agent_%' GROUP BY collector_id").fetchall()
    for r in rows:
        print(f"{r[0]}: {r[1]}")
        
    print("\n--- Total Logs ---")
    logs = c.execute("SELECT COUNT(*) FROM agent_activity_logs").fetchone()[0]
    print(logs)
    
    print("\n--- Market Data ---")
    md = c.execute("SELECT COUNT(*) FROM market_data").fetchone()[0]
    print(md)
    
except Exception as e:
    print(e)
finally:
    conn.close()
