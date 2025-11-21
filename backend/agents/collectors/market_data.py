import time
import logging
import json
import asyncio
from datetime import datetime, timedelta
import random
from typing import Dict, Any, Optional
from backend.database.db import db

# Angel One API
try:
    from SmartApi import SmartConnect
    import pyotp
    import os
    ANGEL_API_AVAILABLE = True
except ImportError:
    ANGEL_API_AVAILABLE = False
    print("SmartApi not installed. Install with: pip install smartapi-python")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NSEDataCollector:
    """
    Collector Agent 1: Live Market Data (NSE) using Angel One API
    Responsibility: Fetch live option chain, indices, VIX, and FII/DII data.
    """
    def __init__(self):
        self.name = "NSEDataCollector"
        self.status = "initialized"
        self.last_collection_time = 0
        self.collection_interval = 3  # 3 seconds
        self.snapshot_interval = 3600 # 1 hour
        self.last_snapshot_time = 0
        self.data_buffer = {}
        
        # Angel One initialization
        self.angel_client = None
        self.api_key = os.getenv("ANGEL_ONE_API_KEY")
        self.client_id = os.getenv("ANGEL_ONE_CLIENT_ID")
        self.password = os.getenv("ANGEL_ONE_PASSWORD")
        self.totp_secret = os.getenv("ANGEL_ONE_TOTP_SECRET")
        
        # Token mappings for Angel One API
        self.token_map = {
            "NIFTY 50": {"exchange": "NSE", "token": "99926000", "symbol": "Nifty 50"},
            "BANKNIFTY": {"exchange": "NSE", "token": "99926009", "symbol": "Nifty Bank"}
        }
        
        # Initialize Angel One connection
        if ANGEL_API_AVAILABLE and self.api_key:
            self._init_angel_one()
        else:
            logger.warning("Angel One API not available or credentials missing.")
            self.status = "error_no_credentials"

    def _init_angel_one(self):
        """Initialize Angel One SmartAPI connection."""
        try:
            self.angel_client = SmartConnect(api_key=self.api_key)
            
            if self.client_id and self.password and self.totp_secret:
                # Generate TOTP
                totp = pyotp.TOTP(self.totp_secret).now()
                
                # Login
                data = self.angel_client.generateSession(self.client_id, self.password, totp)
                
                if data and data.get('status'):
                    self.auth_token = data['data']['jwtToken']
                    self.refresh_token = data['data']['refreshToken']
                    self.feed_token = data['data']['feedToken']
                    logger.info(f"✅ Angel One API connected successfully for {self.client_id}")
                    self.status = "connected_angel_one"
                else:
                    logger.error(f"Angel One login failed: {data.get('message', 'Unknown error')}")
                    self.angel_client = None
                    self.status = "error_login_failed"
            else:
                logger.warning("Missing Angel One credentials (CLIENT_ID/PASSWORD/TOTP). API initialized but not logged in.")
                self.status = "error_missing_credentials"
                
        except Exception as e:
            logger.error(f"Angel One initialization failed: {e}")
            self.angel_client = None
            self.status = "error_initialization_failed"

    def get_indices(self) -> Dict[str, Dict[str, float]]:
        """
        Fetch major indices data (NIFTY 50, BANKNIFTY) using Angel One API.
        Returns empty dict if Angel One is not available.
        """
        if self.angel_client and self.auth_token:
            try:
                # Angel One LTP (Last Traded Price) API
                data = {}
                
                for index_name, token_info in self.token_map.items():
                    try:
                        # Fetch LTP using Angel One
                        ltp_data = self.angel_client.ltpData(
                            token_info["exchange"],
                            token_info["symbol"],
                            token_info["token"]
                        )
                        
                        if ltp_data and ltp_data.get('status') and ltp_data.get('data'):
                            ltp = float(ltp_data['data']['ltp'])
                            
                            data[index_name] = {
                                "price": ltp,
                                "open": ltp,  # Will be replaced with actual OHLC if available
                                "high": ltp,
                                "low": ltp,
                                "prev_close": ltp
                            }
                            logger.info(f"✅ Fetched {index_name} from Angel One: {ltp}")
                    except Exception as e:
                        logger.error(f"Error fetching {index_name} from Angel One: {e}")
                
                return data
                    
            except Exception as e:
                logger.error(f"Angel One API error: {e}")
        
        # No fallback data. Return empty to indicate failure.
        logger.error("❌ Failed to fetch indices: Angel One API not connected or failed.")
        return {}

    def get_vix(self) -> float:
        """
        Fetch India VIX.
        """
        # TODO: Implement VIX fetching via Angel One or another reliable source.
        # yfinance removed.
        return 0.0

    def get_option_chain(self, symbol: str = "NIFTY") -> Dict[str, Any]:
        """
        Fetch option chain data.
        """
        # TODO: Implement real option chain fetching via Angel One.
        # Mock data removed.
        return {}

    def get_fii_dii_data(self) -> Dict[str, Any]:
        """
        Fetch FII/DII activity.
        """
        # TODO: Implement real FII/DII fetching.
        # Mock data removed.
        return {}

    def save_snapshot_for_frontend(self, market_snapshot: Dict[str, Any]):
        """
        Save a 'strategy' entry that serves as a market report for the frontend.
        """
        try:
            title = f"Market Snapshot - {datetime.now().strftime('%H:%M')}"
            
            # Format content as a readable string/markdown for the frontend
            nifty_price = market_snapshot['indices'].get('NIFTY 50', {}).get('price', 'N/A')
            bn_price = market_snapshot['indices'].get('BANKNIFTY', {}).get('price', 'N/A')
            
            content_str = f"""
### Market Update ({datetime.now().strftime('%H:%M')})

**Indices**:
- NIFTY 50: {nifty_price}
- BANKNIFTY: {bn_price}

**Volatility**:
- India VIX: {market_snapshot.get('vix', 'N/A')}

**Institutional Activity**:
- FII: {market_snapshot['fii_dii'].get('FII_cash', 0):.2f} Cr
- DII: {market_snapshot['fii_dii'].get('DII_cash', 0):.2f} Cr
            """
            
            db.insert_strategy(
                source="NSE Market Data",
                content=content_str, # Frontend expects string or JSON
                title=title,
                url="https://www.nseindia.com",
                verified=True,
                confidence_score=100.0,
                collector_id="agent_1" # Mapping to Agent 1
            )
            logger.info("Saved market snapshot for frontend.")
            
        except Exception as e:
            logger.error(f"Error saving frontend snapshot: {e}")

    async def run_continuously(self, interval_minutes: int = 1):
        """
        Main loop for continuous data collection.
        """
        self.status = "running"
        logger.info(f"{self.name} started continuous collection.")
        
        while True:
            try:
                current_time = time.time()
                
                # Collect all data
                indices = self.get_indices()
                
                if not indices:
                    logger.warning("No data collected. Retrying in 5 seconds...")
                    await asyncio.sleep(5)
                    continue

                vix = self.get_vix()
                option_chain = self.get_option_chain()
                fii_dii = self.get_fii_dii_data()
                
                # Aggregate data
                market_snapshot = {
                    "indices": indices,
                    "vix": vix,
                    "option_chain": option_chain,
                    "fii_dii": fii_dii,
                    "timestamp": datetime.now().isoformat()
                }
                
                self.data_buffer = market_snapshot
                self.last_collection_time = current_time
                
                # Save to Market Data Table (High Frequency)
                # We save NIFTY 50 as the primary symbol for now
                if "NIFTY 50" in indices:
                    nifty_data = indices["NIFTY 50"]
                    db.save_market_data(
                        symbol="NIFTY",
                        timestamp=datetime.now(),
                        open_price=nifty_data["open"],
                        high=nifty_data["high"],
                        low=nifty_data["low"],
                        close=nifty_data["price"],
                        volume=0
                    )
                    
                if "BANKNIFTY" in indices:
                    bn_data = indices["BANKNIFTY"]
                    db.save_market_data(
                        symbol="BANKNIFTY",
                        timestamp=datetime.now(),
                        open_price=bn_data["open"],
                        high=bn_data["high"],
                        low=bn_data["low"],
                        close=bn_data["price"],
                        volume=0
                    )
                
                logger.info(f"Collected market data at {market_snapshot['timestamp']}")
                
                # Periodic Snapshot for Frontend (Low Frequency)
                if current_time - self.last_snapshot_time > self.snapshot_interval:
                    self.save_snapshot_for_frontend(market_snapshot)
                    self.last_snapshot_time = current_time
                
                # Wait for next interval
                await asyncio.sleep(self.collection_interval) 
                
            except Exception as e:
                logger.error(f"Error in continuous collection: {e}")
                self.status = "error"
                await asyncio.sleep(5) # Wait before retrying

if __name__ == "__main__":
    collector = NSEDataCollector()
    # asyncio.run(collector.run_continuously())
