import os
from typing import Dict, List, Optional
import pandas as pd
from .base_provider import BaseDataProvider
# from api_helper import NorenApiPy # Uncomment when installed

class FinvasiaDataProvider(BaseDataProvider):
    """
    Data provider using Finvasia (Shoonya).
    Acts as the SECONDARY provider.
    """

    def __init__(self):
        self.user_id = os.getenv("FINVASIA_USER_ID")
        self.password = os.getenv("FINVASIA_PASSWORD")
        self.factor2 = os.getenv("FINVASIA_FACTOR2")
        self.vc = os.getenv("FINVASIA_VC")
        self.app_key = os.getenv("FINVASIA_APP_KEY")
        self.imei = os.getenv("FINVASIA_IMEI")
        self.api = None

    def connect(self) -> bool:
        if not self.user_id:
            print("Finvasia credentials not found.")
            return False
        
        try:
            # self.api = NorenApiPy()
            # ret = self.api.login(userid=self.user_id, password=self.password, twoFA=self.factor2, vendor_code=self.vc, api_secret=self.app_key, imei=self.imei)
            print("Finvasia connected successfully (Mock).")
            return True
        except Exception as e:
            print(f"Finvasia connection failed: {e}")
            return False

    def get_live_price(self, symbol: str) -> Optional[float]:
        if not self.api:
            return None
        return None

    def get_historical_data(self, symbol: str, period: str = "1mo", interval: str = "1d") -> Optional[pd.DataFrame]:
        if not self.api:
            return None
        return None

    def get_top_gainers(self, limit: int = 50) -> List[Dict]:
        if not self.api:
            return []
        return []
