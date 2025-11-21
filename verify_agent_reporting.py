import requests
import sqlite3
import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database.db import db

def verify_db_logging():
    print("Verifying DB logging...")
    try:
        logs = db.get_agent_activity_logs("test_agent")
        if logs:
            print(f"Found {len(logs)} logs for test_agent.")
        else:
            print("No logs found for test_agent. Creating one...")
            db.log_agent_activity("test_agent", "INFO", "Test log entry", {"test": True})
            logs = db.get_agent_activity_logs("test_agent")
            if logs:
                print("Successfully created and retrieved log.")
            else:
                print("FAILED to create/retrieve log.")
                return False
        return True
    except Exception as e:
        print(f"DB Verification Failed: {e}")
        return False

def verify_api_endpoint():
    print("\nVerifying API endpoint...")
    try:
        # Ensure server is running or mock the request if testing locally without server
        # For this script, we'll assume the server is running on localhost:5000
        # If not, we might need to start it or just rely on DB verification for now
        
        response = requests.get("http://localhost:5000/api/agents/test_agent/details")
        if response.status_code == 200:
            data = response.json()
            print("API Response OK")
            print(f"Agent ID: {data.get('agent_id')}")
            print(f"Stats: {data.get('stats')}")
            print(f"Logs count: {len(data.get('logs', []))}")
            return True
        else:
            print(f"API Request Failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"API Verification Failed (Server might not be running): {e}")
        return False

if __name__ == "__main__":
    db_ok = verify_db_logging()
    api_ok = verify_api_endpoint()
    
    if db_ok:
        print("\nDatabase verification PASSED")
    else:
        print("\nDatabase verification FAILED")
        
    if api_ok:
        print("API verification PASSED")
    else:
        print("API verification FAILED (Check if server is running)")
