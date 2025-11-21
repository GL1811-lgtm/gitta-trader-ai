"""
Angel One API Helper - Provides real-time market data
"""
import os
from SmartApi import SmartConnect
import pyotp
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class AngelOneHelper:
    """Helper class for Angel One API integration."""
    
    def __init__(self):
        self.api_key = os.getenv('ANGEL_ONE_API_KEY')
        self.client_id = os.getenv('ANGEL_ONE_CLIENT_ID')
        self.password = os.getenv('ANGEL_ONE_PASSWORD')
        self.totp_secret = os.getenv('ANGEL_ONE_TOTP_SECRET')
        self.smart_api = None
        self._is_connected = False
        
    def connect(self) -> bool:
        """Establish connection to Angel One API."""
        if self._is_connected:
            return True
            
        try:
            self.smart_api = SmartConnect(api_key=self.api_key)
            totp = pyotp.TOTP(self.totp_secret).now()
            
            session = self.smart_api.generateSession(
                self.client_id,
                self.password,
                totp
            )
            
            if session and session.get('status'):
                self._is_connected = True
                logger.info("✅ Connected to Angel One API")
                return True
            else:
                logger.error("❌ Failed to connect to Angel One API")
                return False
                
        except Exception as e:
            logger.error(f"❌ Angel One connection error: {e}")
            return False
    
    def get_ltp(self, exchange: str, symbol_token: str, trading_symbol: str) -> Optional[Dict]:
        """Get Last Traded Price for a symbol."""
        if not self._is_connected:
            if not self.connect():
                return None
        
        try:
            data = self.smart_api.ltpData(exchange, trading_symbol, symbol_token)
            if data and data.get('status'):
                return data.get('data')
            return None
        except Exception as e:
            logger.error(f"Error fetching LTP for {trading_symbol}: {e}")
            return None
    
    def get_market_data(self, exchange: str, symbol_token: str, trading_symbol: str) -> Optional[Dict]:
        """Get comprehensive market data for a symbol."""
        if not self._is_connected:
            if not self.connect():
                return None
        
        try:
            data = self.smart_api.getMarketData(
                mode="FULL",
                exchangeTokens={exchange: [symbol_token]}
            )
            
            if data and data.get('status') and data.get('data'):
                fetched = data['data'].get('fetched', [])
                if fetched:
                    return fetched[0]
            return None
        except Exception as e:
            logger.error(f"Error fetching market data for {trading_symbol}: {e}")
            return None
    
    def get_nifty_50_data(self) -> Optional[Dict]:
        """Get NIFTY 50 data."""
        # NIFTY 50 token
        return self.get_market_data("NSE", "99926000", "NIFTY 50")
    
    def get_banknifty_data(self) -> Optional[Dict]:
        """Get BANKNIFTY data."""
        # BANKNIFTY token
        return self.get_market_data("NSE", "99926009", "NIFTY BANK")
    
    def get_token(self, symbol: str, exchange: str = "NSE") -> Optional[str]:
        """Get symbol token for a given symbol."""
        if not self._is_connected:
            if not self.connect():
                return None
                
        try:
            # Search for the scrip
            # Note: SmartApi searchScrip payload might vary, assuming standard
            payload = {
                "exchange": exchange,
                "searchscrip": symbol
            }
            data = self.smart_api.searchScrip(exchange, symbol)
            
            if data and data.get('status') and data.get('data'):
                # Return the first match's token
                # Filter for exact match if possible, or take first
                for scrip in data['data']:
                    scrip_symbol = scrip.get('symbol', '')
                    trading_symbol = scrip.get('tradingsymbol', '')
                    token = scrip.get('symboltoken')
                    
                    if token and (scrip_symbol == symbol or trading_symbol == symbol + "-EQ"):
                        return token
                
                # If no exact match, return first
                if len(data['data']) > 0:
                    return data['data'][0].get('symboltoken')
            
            return None
        except Exception as e:
            logger.error(f"Error searching token for {symbol}: {e}")
            return None

# Global instance
angel_helper = AngelOneHelper()
