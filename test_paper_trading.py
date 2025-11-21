import requests
import sys
import time

BASE_URL = "http://localhost:5001"

def test_paper_trading():
    print("--- Testing Paper Trading Engine ---")
    
    symbol = "RELIANCE.NS"
    quantity = 10
    
    try:
        # 1. Get Initial Account State
        print("\n1. Fetching Initial Account State...")
        res = requests.get(f"{BASE_URL}/api/trading/account")
        if res.status_code != 200:
            print(f"❌ Failed to fetch account: {res.text}")
            return
        
        account = res.json()
        initial_balance = account['balance']
        print(f"✅ Initial Balance: ₹{initial_balance}")
        
        # 2. Place BUY Order
        print(f"\n2. Placing BUY Order for {quantity} {symbol}...")
        order_data = {"symbol": symbol, "side": "BUY", "quantity": quantity}
        res = requests.post(f"{BASE_URL}/api/trading/order", json=order_data)
        
        if res.status_code == 200:
            data = res.json()
            print(f"✅ Buy Successful: {data['message']}")
            print(f"   Price: ₹{data['price']}, Total: ₹{data['total']}")
        else:
            print(f"❌ Buy Failed: {res.text}")
            return

        # 3. Check Portfolio
        print("\n3. Verifying Portfolio...")
        res = requests.get(f"{BASE_URL}/api/trading/account")
        account = res.json()
        holdings = account['holdings']
        
        found = False
        for item in holdings:
            if item['symbol'] == symbol:
                print(f"✅ Found {symbol} in portfolio: {item['quantity']} qty @ ₹{item['avg_price']}")
                found = True
                break
        
        if not found:
            print(f"❌ {symbol} not found in portfolio!")
            return

        # 4. Place SELL Order
        print(f"\n4. Placing SELL Order for {quantity} {symbol}...")
        order_data = {"symbol": symbol, "side": "SELL", "quantity": quantity}
        res = requests.post(f"{BASE_URL}/api/trading/order", json=order_data)
        
        if res.status_code == 200:
            data = res.json()
            print(f"✅ Sell Successful: {data['message']}")
        else:
            print(f"❌ Sell Failed: {res.text}")
            return

        # 5. Final Account Check
        print("\n5. Verifying Final Balance...")
        res = requests.get(f"{BASE_URL}/api/trading/account")
        account = res.json()
        final_balance = account['balance']
        print(f"✅ Final Balance: ₹{final_balance}")
        
        if final_balance != initial_balance: # It won't be exactly same due to price fluctuation spread usually, but in mock it might be if price didn't change
             print(f"ℹ️ Balance changed by ₹{final_balance - initial_balance:.2f} (P&L)")

    except Exception as e:
        print(f"❌ Test Failed: {e}")

if __name__ == "__main__":
    test_paper_trading()
