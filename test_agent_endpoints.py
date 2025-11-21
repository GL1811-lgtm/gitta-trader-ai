import requests
import json

BASE_URL = "http://localhost:5001"

def test_agent_endpoints():
    """Test the new agent detail endpoints"""
    
    # Test with collector_1 (should have data if you ran collectors before)
    agent_id = "collector_1"
    
    print("="*60)
    print(f"Testing Agent Detail Endpoints for: {agent_id}")
    print("="*60)
    
    # Test 1: Get Full Details
    print("\n1. Testing GET /api/agents/<id>/details")
    try:
        response = requests.get(f"{BASE_URL}/api/agents/{agent_id}/details")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS - Agent Name: {data.get('name')}")
            print(f"   Total Collected: {data.get('stats', {}).get('total_collected', 0)}")
            print(f"   Success Rate: {data.get('stats', {}).get('success_rate', 0)}%")
            print(f"   Collections Count: {len(data.get('recent_collections', []))}")
        else:
            print(f"❌ FAILED - Status: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # Test 2: Get Collections Only
    print("\n2. Testing GET /api/agents/<id>/collections")
    try:
        response = requests.get(f"{BASE_URL}/api/agents/{agent_id}/collections?limit=5")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS - Retrieved {data.get('count', 0)} collections")
            if data.get('collections'):
                first = data['collections'][0]
                print(f"   First: {first.get('strategy_name')} ({first.get('quality_score')}%)")
        else:
            print(f"❌ FAILED - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    # Test 3: Get Stats Only
    print("\n3. Testing GET /api/agents/<id>/stats")
    try:
        response = requests.get(f"{BASE_URL}/api/agents/{agent_id}/stats")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS - Agent ID: {data.get('agent_id')}")
            print(f"   Stats: {json.dumps(data.get('stats'), indent=2)}")
            print(f"   Verification: {json.dumps(data.get('verification'), indent=2)}")
        else:
            print(f"❌ FAILED - Status: {response.status_code}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
    
    print("\n" + "="*60)
    print("Testing Complete!")
    print("="*60)

if __name__ == "__main__":
    test_agent_endpoints()
