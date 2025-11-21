import logging
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HistoricalDataManager:
    """
    Collector Agent 5: Historical Data Manager
    Responsibility: Download, store, and manage historical data for backtesting.
    """
    def __init__(self):
        self.name = "HistoricalDataManager"
        self.status = "initialized"
        self.data_dir = "backend/data/historical"
        os.makedirs(self.data_dir, exist_ok=True)

    def download_data(self, symbol: str, start_date: str, end_date: str = None) -> bool:
        """
        Download historical data from Yahoo Finance.
        """
        try:
            import yfinance as yf
            
            if end_date is None:
                end_date = datetime.now().strftime("%Y-%m-%d")
                
            logger.info(f"Downloading data for {symbol} from {start_date} to {end_date}")
            
            # Add .NS suffix for NSE stocks if not present
            ticker = symbol if symbol.endswith(".NS") or symbol in ["^NSEI", "^NSEBANK"] else f"{symbol}.NS"
            
            data = yf.download(ticker, start=start_date, end=end_date)
            
            if data.empty:
                logger.warning(f"No data found for {symbol}")
                return False
                
            # Save to CSV
            filename = f"{self.data_dir}/{symbol}_{start_date}_{end_date}.csv"
            data.to_csv(filename)
            logger.info(f"Data saved to {filename}")
            
            # Also save to DB (mock call)
            # self.save_to_db(symbol, data)
            
            return True
        except ImportError:
            logger.error("yfinance not installed. Please install it: pip install yfinance")
            return False
        except Exception as e:
            logger.error(f"Error downloading data for {symbol}: {e}")
            return False

    def load_data(self, symbol: str) -> pd.DataFrame:
        """
        Load historical data from local CSV.
        """
        try:
            # Find latest file for symbol
            files = [f for f in os.listdir(self.data_dir) if f.startswith(symbol)]
            if not files:
                logger.warning(f"No local data found for {symbol}")
                return pd.DataFrame()
                
            # Sort by modification time
            latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(self.data_dir, f)))
            return pd.read_csv(os.path.join(self.data_dir, latest_file))
        except Exception as e:
            logger.error(f"Error loading data for {symbol}: {e}")
            return pd.DataFrame()

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and validate data (handle missing values, outliers).
        """
        try:
            # Drop missing values
            df = df.dropna()
            
            # Remove duplicates
            df = df.drop_duplicates()
            
            # Ensure numeric columns
            cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            for col in cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            return df
        except Exception as e:
            logger.error(f"Error cleaning data: {e}")
            return df

if __name__ == "__main__":
    manager = HistoricalDataManager()
    # manager.download_data("^NSEI", "2023-01-01") # Commented out to avoid actual network call in test
    print("Historical Data Manager initialized")
