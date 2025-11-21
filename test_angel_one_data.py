import sys
import os
from datetime import datetime, timedelta

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.trading.angel_one_client import AngelOneClient
from dotenv import load_dotenv

def test_historical_data():
    print("Testing Angel One Data Fetching...")
    
    # Load env
    load_dotenv()
    
    try:
        client = AngelOneClient()
        print("✅ Client Initialized")
        
        print("Logging in...")
        if client.login():
            print("✅ Login Successful")
            
            # Define parameters for SBIN (State Bank of India)
            # Exchange: NSE
            # Symbol Token: 3045 (SBIN)
            # Interval: ONE_DAY
            
            to_date = datetime.now()
            from_date = to_date - timedelta(days=5)
            
            # Format dates as required by Angel One API: "yyyy-mm-dd HH:MM"
            from_date_str = from_date.strftime("%Y-%m-%d %H:%M")
            to_date_str = to_date.strftime("%Y-%m-%d %H:%M")
            
            print(f"Fetching data for SBIN (3045) from {from_date_str} to {to_date_str}...")
            
            data = client.get_historical_data(
                exchange="NSE",
                symbol_token="3045",
                interval="ONE_DAY",
                from_date=from_date_str,
                to_date=to_date_str
            )
            
            if data and data.get('status'):
                candles = data.get('data', [])
                print(f"✅ Data Fetched Successfully! Received {len(candles)} candles.")
                if candles:
                    print("Sample Candle (Timestamp, Open, High, Low, Close, Volume):")
                    print(candles[0])
            else:
                print(f"❌ Failed to fetch data. Response: {data}")
                
        else:
            print("❌ Login Failed")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_historical_data()
