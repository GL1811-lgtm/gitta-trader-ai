import urllib.request, urllib.error, json

url = 'http://localhost:5000/api/dashboard/ticker'
try:
    with urllib.request.urlopen(url, timeout=3) as response:
        data = json.loads(response.read().decode('utf-8'))
        print(f"Success: {data}")
except urllib.error.HTTPError as e:
    error_body = e.read().decode('utf-8')
    try:
        error_json = json.loads(error_body)
        print(f"Error response: {error_json}")
    except:
        print(f"HTML Error (first 500 chars): {error_body[:500]}")
except Exception as e:
    print(f"Exception: {e}")
