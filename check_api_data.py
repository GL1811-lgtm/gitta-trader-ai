import urllib.request, json

# Test Ticker API
url = 'http://localhost:5000/api/dashboard/ticker'
with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode('utf-8'))
    print("=== TICKER API RESPONSE ===")
    print(json.dumps(data, indent=2))
    
print("\n\n")

# Test Movers API  
url2 = 'http://localhost:5000/api/market/movers?index=NIFTY%20100'
with urllib.request.urlopen(url2) as response:
    data2 = json.loads(response.read().decode('utf-8'))
    print("=== MOVERS API RESPONSE ===")
    print(f"Gainers: {len(data2.get('gainers', []))} items")
    print(f"Losers: {len(data2.get('losers', []))} items")
    print(f"Volume Shockers: {len(data2.get('volumeShockers', []))} items")
    if data2.get('gainers'):
        print("\nFirst Gainer:")
        print(json.dumps(data2['gainers'][0], indent=2))
