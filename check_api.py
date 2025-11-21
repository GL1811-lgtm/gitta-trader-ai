import requests
import json

response = requests.get('http://localhost:5000/api/agents/agent_1/details')
data = response.json()

print("live_status field present:", 'live_status' in data)
if 'live_status' in data:
    print("\nlive_status content:")
    print(json.dumps(data['live_status'], indent=2))
else:
    print("\nlive_status missing!")
    
print("\nstatus field:", data.get('status', 'N/A'))
