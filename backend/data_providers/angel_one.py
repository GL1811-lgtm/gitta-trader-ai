import os
from typing import Dict, List, Optional
import pandas as pd
from .base_provider import BaseDataProvider
# from SmartApi import SmartConnect # Uncomment when installed

class AngelOneDataProvider(BaseDataProvider):
    """
    Data provider using Angel One SmartAPI.
    Acts as the PRIMARY provider.
    """

    def __init__(self):
        self.api_key = os.getenv("ANGEL_ONE_API_KEY")
        self.client_code = os.getenv("ANGEL_ONE_CLIENT_ID")
        self.password = os.getenv("ANGEL_ONE_PASSWORD")
        self.totp_secret = os.getenv("ANGEL_ONE_TOTP_SECRET")
        self.obj = None

    def connect(self) -> bool:
        if not self.api_key or not self.client_code or not self.password or not self.totp_secret:
            print("Angel One credentials not found in environment.")
            return False
        
        try:
            try:
                from SmartApi import SmartConnect
                import pyotp
            except ImportError:
                print("SmartApi or pyotp not installed. Run `pip install smartapi-python pyotp`")
                return False

            self.obj = SmartConnect(api_key=self.api_key)
            
            # Generate TOTP
            try:
                totp = pyotp.TOTP(self.totp_secret).now()
            except Exception as e:
                print(f"Error generating TOTP: {e}")
                return False

            data = self.obj.generateSession(self.client_code, self.password, totp)
            
            if data['status'] == False:
                print(f"Angel One Login Failed: {data['message']}")
                return False

            self.refreshToken = data['data']['refreshToken']
            self.feedToken = self.obj.getfeedToken()
            # self.userProfile = self.obj.getProfile(self.refreshToken)
            print("Angel One connected successfully.")
            return True
        except Exception as e:
            print(f"Angel One connection failed: {e}")
            return False

    def get_live_price(self, symbol: str) -> Optional[float]:
        if not self.obj:
            return None
        # Implementation for fetching live price
        return None

    def get_historical_data(self, symbol: str, period: str = "1mo", interval: str = "1d") -> Optional[pd.DataFrame]:
        if not self.obj:
            return None
        # Implementation for fetching historical data
        return None

    def get_top_gainers(self, limit: int = 50) -> List[Dict]:
        if not self.obj:
            return []
        # Implementation for fetching top gainers
        return []
