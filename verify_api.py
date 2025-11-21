import requests
import time
import threading
from backend.api.app import app

def run_server():
    app.run(port=5002)

def verify_api():
    print("--- Verifying Evolution API ---")
    
    # Start server in background thread
    server_thread = threading.Thread(target=run_server, daemon=True)
    server_thread.start()
    time.sleep(2) # Wait for server to start
    
    base_url = "http://localhost:5002/api/evolution"
    
    try:
        # 1. Get Status
        print("\n1. Testing GET /status...")
        resp = requests.get(f"{base_url}/status")
        if resp.status_code == 200:
            print(f"PASS: Status Code 200. Data: {resp.json().keys()}")
        else:
            print(f"FAIL: Status Code {resp.status_code}")

        # 2. Trigger Evolution
        print("\n2. Testing POST /evolve...")
        resp = requests.post(f"{base_url}/evolve")
        if resp.status_code == 200:
            print(f"PASS: Evolution Triggered. New Gen: {resp.json()['new_generation']}")
        else:
            print(f"FAIL: Status Code {resp.status_code}")

        # 3. Get Organisms
        print("\n3. Testing GET /organisms...")
        resp = requests.get(f"{base_url}/organisms")
        if resp.status_code == 200:
            print(f"PASS: Fetched {len(resp.json())} organisms.")
        else:
            print(f"FAIL: Status Code {resp.status_code}")

    except Exception as e:
        print(f"FAIL: API Error: {e}")

if __name__ == "__main__":
    verify_api()
