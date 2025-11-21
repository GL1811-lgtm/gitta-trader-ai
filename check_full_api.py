import requests
import json

response = requests.get('http://localhost:5000/api/agents/agent_1/details')
data = response.json()

# Print full response
print("Full API Response:")
print(json.dumps(data, indent=2))
