import sqlite3
import os

db_path = 'backend/data/gitta.db'

if not os.path.exists(db_path):
    print(f"Database file not found at {db_path}")
    # Try initializing it
    from backend.database.db import DatabaseManager
    db = DatabaseManager()
    print("Database initialized.")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    print("Existing tables:")
    for table in tables:
        print(f"- {table}")
        
    required_tables = [
        'evolution_history', 
        'code_modifications', 
        'system_health', 
        'order_book_snapshots', 
        'performance_analytics',
        'market_data'
    ]
    
    missing = [t for t in required_tables if t not in tables]
    if missing:
        print(f"\n❌ Missing tables: {missing}")
        # Force schema update
        print("Attempting to update schema...")
        with open('backend/database/schema.sql', 'r') as f:
            schema = f.read()
        conn.executescript(schema)
        print("Schema executed.")
        
        # Check again
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        missing_after = [t for t in required_tables if t not in tables]
        if not missing_after:
            print("✅ All tables created successfully.")
        else:
            print(f"❌ Still missing: {missing_after}")
    else:
        print("\n✅ All required tables are present.")
        
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals():
        conn.close()
