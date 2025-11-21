from backend.database.db import db
import time

def verify_db():
    print("Verifying DB methods...")
    
    # 1. Evolution
    print("Logging evolution...")
    eid = db.log_evolution(1, 1.5, 1.2, 0.8, 100)
    if eid:
        print(f"Evolution logged with ID: {eid}")
    else:
        print("Failed to log evolution")

    # 2. Code Modification
    print("Logging code mod...")
    cid = db.log_code_modification("test.py", "FIX", "Test fix", "oldhash", "newhash")
    if cid:
        print(f"Code mod logged with ID: {cid}")
    else:
        print("Failed to log code mod")
        
    # 3. System Health
    print("Logging health...")
    hid = db.log_system_health("CPU", 50.5, "OK")
    if hid:
        print(f"Health logged with ID: {hid}")
    else:
        print("Failed to log health")
        
    # 4. Market Data
    print("Saving market data...")
    success = db.save_market_data("TEST", "2023-01-01 10:00:00", 100, 105, 95, 102, 1000)
    if success:
        print("Market data saved")
    else:
        print("Failed to save market data")

if __name__ == "__main__":
    verify_db()
