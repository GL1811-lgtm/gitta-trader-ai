from datetime import datetime, timedelta
import logging
from .base_collector import BaseCollectorAgent
from backend.trading.angel_one_client import AngelOneClient

logger = logging.getLogger(__name__)

class CollectorAgent9(BaseCollectorAgent):
    """
    Angel One Market Data Collector.
    Fetches real historical data and generates Price Action strategies based on recent market moves.
    """
    def __init__(self, agent_id, source_name):
        super().__init__(agent_id, source_name)
        self.client = None
        try:
            self.client = AngelOneClient()
            # Attempt login
            if not self.client.login():
                logger.warning(f"[{self.agent_id}] Angel One login failed during init")
        except Exception as e:
            logger.error(f"[{self.agent_id}] Angel One client init failed: {e}")

    def collect(self) -> list[dict]:
        """
        Fetches data for key indices/stocks and generates strategies.
        """
        if not self.client or not self.client.auth_token:
            logger.error(f"[{self.agent_id}] Client not ready. Skipping collection.")
            return []
            
        strategies = []
        
        # Define symbols to check (Example: NIFTY 50, BANKNIFTY, SBIN)
        # Note: Symbol tokens need to be accurate. 
        # NIFTY 50 is usually '99926000' (NSE) or similar depending on exchange
        # SBIN is '3045' (NSE)
        symbols = [
            {"name": "SBIN", "token": "3045", "exchange": "NSE"},
            # Add more symbols here if tokens are known
        ]
        
        for symbol in symbols:
            try:
                # Fetch last 5 days of hourly data
                to_date = datetime.now()
                from_date = to_date - timedelta(days=5)
                
                data = self.client.get_historical_data(
                    exchange=symbol["exchange"],
                    symbol_token=symbol["token"],
                    interval="ONE_HOUR",
                    from_date=from_date.strftime("%Y-%m-%d %H:%M"),
                    to_date=to_date.strftime("%Y-%m-%d %H:%M")
                )
                
                if data and data.get('status') and data.get('data'):
                    candles = data['data']
                    last_candle = candles[-1]
                    prev_candle = candles[-2] if len(candles) > 1 else last_candle
                    
                    # Simple Strategy Logic: Bullish Engulfing or Trend
                    close = last_candle[4]
                    open_price = last_candle[1]
                    prev_close = prev_candle[4]
                    prev_open = prev_candle[1]
                    
                    strategy_type = "Neutral"
                    signal = "Hold"
                    
                    if close > open_price and close > prev_open and open_price < prev_close:
                         strategy_type = "Bullish Engulfing"
                         signal = "Buy"
                    elif close < open_price and close < prev_open and open_price > prev_close:
                        strategy_type = "Bearish Engulfing"
                        signal = "Sell"
                    
                    # Create strategy object
                    strategy = {
                        "title": f"{symbol['name']} {strategy_type} Strategy",
                        "source": "Angel One Real Data",
                        "content": f"Detected {strategy_type} pattern on {symbol['name']} (Hourly).\\n"
                                   f"Current Price: {close}\\n"
                                   f"Signal: {signal}\\n"
                                   f"Analysis based on real market data from Angel One.",
                        "url": "https://trade.angelone.in/",
                        "metadata": {
                            "symbol": symbol['name'],
                            "price": close,
                            "timestamp": last_candle[0]
                        }
                    }
                    strategies.append(strategy)
                    
            except Exception as e:
                logger.error(f"[{self.agent_id}] Error processing {symbol['name']}: {e}")
                
        return strategies