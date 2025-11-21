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
        self.client_code = os.getenv("ANGEL_ONE_CLIENT_CODE")
        self.password = os.getenv("ANGEL_ONE_PASSWORD")
        self.obj = None

    def connect(self) -> bool:
        if not self.api_key or not self.client_code or not self.password:
            print("Angel One credentials not found in environment.")
            return False
        
        try:
            try:
                from SmartApi import SmartConnect
            except ImportError:
                print("SmartApi not installed. Run `pip install smartapi-python`")
                return False

            self.obj = SmartConnect(api_key=self.api_key)
            data = self.obj.generateSession(self.client_code, self.password)
            
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
