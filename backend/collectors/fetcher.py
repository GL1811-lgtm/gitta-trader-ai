import datetime
import logging
from typing import Optional
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    from backend.data_providers.angel_one import AngelOneDataProvider
    ANGEL_PROVIDER = AngelOneDataProvider()
except ImportError:
    ANGEL_PROVIDER = None
    logger.error("Could not import AngelOneDataProvider")

def fetch_latest(symbol: str) -> Optional[pd.DataFrame]:
    """
    Fetches the latest 1-minute OHLCV data for a given symbol using Angel One.
    Returns None if data cannot be fetched.
    """
    logger.info(f"Fetching latest data for {symbol}...")
    
    if not ANGEL_PROVIDER:
        logger.error("Angel One provider not initialized.")
        return None

    if not ANGEL_PROVIDER.connect():
        logger.error("Failed to connect to Angel One.")
        return None

    try:
        # Use Angel One provider to get historical data (1 minute interval for last day)
        # Note: AngelOneDataProvider.get_historical_data needs to be implemented fully
        # For now, we will try to use it, but if it returns None, we return None.
        # We do NOT simulate data anymore.
        
        # Map common symbols to Angel One format if needed
        if symbol == '^NSEI':
            angel_symbol = "NIFTY" 
        elif symbol == '^NSEBANK':
            angel_symbol = "BANKNIFTY"
        else:
            angel_symbol = symbol

        data = ANGEL_PROVIDER.get_historical_data(angel_symbol, period="1d", interval="1m")
        
        if data is None or data.empty:
            logger.warning(f"No data returned for {symbol} from Angel One.")
            return None
            
        return data
        
    except Exception as e:
        logger.error(f"An error occurred fetching data for {symbol}: {e}")
        return None

if __name__ == '__main__':
    # For direct testing
    nifty_data = fetch_latest('^NSEI')
    if nifty_data is not None:
        print("\nNIFTY Data:")
        print(nifty_data.head())
    else:
        print("\nFailed to fetch NIFTY Data (Expected if Angel One not configured)")

    banknifty_data = fetch_latest('^NSEBANK')
    if banknifty_data is not None:
        print("\nBANKNIFTY Data:")
        print(banknifty_data.head())
    else:
        print("\nFailed to fetch BANKNIFTY Data (Expected if Angel One not configured)")
