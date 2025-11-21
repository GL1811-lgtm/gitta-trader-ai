import requests
import sys
import time

BASE_URL = "http://localhost:5001"

def test_scheduler():
    print("--- Testing Automated Scheduler ---")
    
    try:
        # 1. Check Scheduled Jobs
        print("\n1. Fetching Scheduled Jobs...")
        res = requests.get(f"{BASE_URL}/api/scheduler/jobs")
        
        if res.status_code == 200:
            data = res.json()
            print(f"✅ Scheduler Status: {data.get('status')}")
            
            jobs = data.get('jobs', [])
            print(f"✅ Found {len(jobs)} jobs:")
            for job in jobs:
                print(f"   - {job['name']} (Next Run: {job['next_run_time']})")
            
            if len(jobs) >= 2:
                print("✅ Morning Scanner and Evening Validator are scheduled.")
            else:
                print("❌ Missing scheduled jobs.")
        else:
            print(f"❌ Failed to fetch jobs: {res.status_code}")
            
    except Exception as e:
        print(f"❌ Connection Failed: {e}")
        print("Make sure the backend is running!")

if __name__ == "__main__":
    test_scheduler()
