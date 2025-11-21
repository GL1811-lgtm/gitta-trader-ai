"""
Script to fetch initial data for NIFTY 50 stocks from Angel One
and populate the database so the UI is not empty.
"""
import time
import logging
from dotenv import load_dotenv
import os

# Load environment variables first
load_dotenv()

from datetime import datetime
from backend.utils.angel_one_helper import angel_helper
from backend.database.db import db
from backend.data.tickers import NIFTY_50_TICKERS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_initial_data():
    print("🚀 Starting initial data fetch for NIFTY 50 stocks...")
    
    if not angel_helper.connect():
        print("❌ Failed to connect to Angel One. Check credentials.")
        return

    count = 0
    for ticker in NIFTY_50_TICKERS:
        symbol = ticker.replace('.NS', '').replace('.BO', '')
        print(f"Processing {symbol}...")
        
        try:
            # 1. Get Token
            # Try with -EQ suffix for NSE equity
            search_symbol = symbol + "-EQ"
            token = angel_helper.get_token(search_symbol, "NSE")
            
            if not token:
                # Try without suffix
                token = angel_helper.get_token(symbol, "NSE")
            
            if not token:
                print(f"⚠️ Could not find token for {symbol}")
                continue
                
            # 2. Get Market Data
            data = angel_helper.get_market_data("NSE", token, symbol)
            
            if data:
                # 3. Save to DB
                db.save_market_data(
                    symbol=symbol,
                    timestamp=datetime.now(),
                    open_price=float(data.get('open', 0)),
                    high=float(data.get('high', 0)),
                    low=float(data.get('low', 0)),
                    close=float(data.get('ltp', 0)),
                    volume=int(data.get('volume', 0))
                )
                print(f"✅ Saved data for {symbol}: LTP {data.get('ltp')}")
                count += 1
            else:
                print(f"⚠️ No data received for {symbol}")
                
            # Rate limit to avoid hitting API limits
            time.sleep(0.2)
            
        except Exception as e:
            print(f"❌ Error processing {symbol}: {e}")

    print(f"✨ Completed! Saved data for {count} stocks.")
    print("Refresh the dashboard to see the data.")

if __name__ == "__main__":
    fetch_initial_data()
