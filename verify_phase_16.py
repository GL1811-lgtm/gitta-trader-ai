import requests
import sys
import time

BASE_URL = "http://localhost:5001"

def test_endpoints():
    print("--- Verifying Phase 16 Features ---")
    
    # 1. Test Health Check
    print("\n1. Testing /api/health...")
    try:
        res = requests.get(f"{BASE_URL}/api/health")
        if res.status_code == 200:
            print(f"✅ Health Check Passed: {res.json()}")
        else:
            print(f"❌ Health Check Failed: {res.status_code}")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        return

    # 2. Test System Status
    print("\n2. Testing /api/system/status...")
    try:
        res = requests.get(f"{BASE_URL}/api/system/status")
        if res.status_code == 200:
            print(f"✅ System Status Passed: {res.json()}")
        else:
            print(f"❌ System Status Failed: {res.status_code}")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

    # 3. Test Morning Report
    print("\n3. Testing /api/reports/morning...")
    try:
        res = requests.get(f"{BASE_URL}/api/reports/morning")
        if res.status_code == 200:
            print(f"✅ Morning Report Found: {res.json().get('date')}")
        elif res.status_code == 404:
            print(f"⚠️ Morning Report Not Found (Expected if not run yet)")
        else:
            print(f"❌ Morning Report Error: {res.status_code}")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

    # 4. Test Error Handling (404)
    print("\n4. Testing Error Handling (404)...")
    try:
        res = requests.get(f"{BASE_URL}/api/non_existent_endpoint")
        if res.status_code == 404:
            print(f"✅ 404 Handled Correctly: {res.json()}")
        else:
            print(f"❌ 404 Handling Failed: {res.status_code}")
    except Exception as e:
        print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    test_endpoints()
