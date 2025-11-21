import requests
import json

BASE_URL = "http://localhost:5001"

def test_backtest_api():
    print("--- Testing Backtest API ---")
    
    payload = {
        "symbol": "RELIANCE.NS",
        "strategy": "SMA_CROSSOVER",
        "period": "1y",
        "initial_capital": 100000
    }
    
    try:
        print(f"Sending Backtest Request for {payload['symbol']}...")
        res = requests.post(f"{BASE_URL}/api/backtest/run", json=payload)
        
        if res.status_code == 200:
            data = res.json()
            if "error" in data:
                print(f"❌ Backtest Error: {data['error']}")
            else:
                print("✅ Backtest Successful!")
                print(f"   Final Equity: ₹{data['final_equity']}")
                print(f"   Total Return: {data['total_return_pct']}%")
                print(f"   Max Drawdown: {data['max_drawdown_pct']}%")
                print(f"   Total Trades: {data['total_trades']}")
        else:
            print(f"❌ Request Failed: {res.status_code} - {res.text}")

    except Exception as e:
        print(f"❌ Test Failed: {e}")

if __name__ == "__main__":
    test_backtest_api()
