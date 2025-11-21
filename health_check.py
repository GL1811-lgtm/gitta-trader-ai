import requests
import sys
import time

def check_health(url="http://localhost:5001/api/health", retries=5, delay=2):
    print(f"Checking system health at {url}...")
    
    for i in range(retries):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ System is HEALTHY!")
                print(f"   Database: {data.get('database')}")
                print(f"   Timestamp: {data.get('timestamp')}")
                return True
            else:
                print(f"❌ System returned status code {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"⚠️ Connection failed. Retrying ({i+1}/{retries})...")
        
        time.sleep(delay)
    
    print("❌ Health check FAILED. System might be down.")
    return False

if __name__ == "__main__":
    success = check_health()
    sys.exit(0 if success else 1)
