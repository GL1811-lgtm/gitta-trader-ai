"""
Data Provider Manager
Manages different data providers (Angel One as primary).
"""

from typing import Dict, List, Optional
import pandas as pd
from .angel_one import AngelOneDataProvider

class DataProviderManager:
    """
    Manages the Data Provider.
    Uses Angel One exclusively.
    """

    def __init__(self):
        self.angel_one = AngelOneDataProvider()
        self.active_provider = None
        self._initialize_providers()

    def _initialize_providers(self):
        """Try to connect to Angel One."""
        if self.angel_one.connect():
            self.active_provider = self.angel_one
            print("Using Primary Provider: Angel One")
        else:
            print("WARNING: Angel One connection failed. No data provider available.")
            self.active_provider = None

    def get_live_price(self, symbol: str) -> Optional[float]:
        """Get live price using the active provider."""
        if self.active_provider is None:
            print(f"No active provider for {symbol}")
            return None
        return self.active_provider.get_live_price(symbol)

    def get_historical_data(self, symbol: str, period: str = "1mo", interval: str = "1d") -> Optional[pd.DataFrame]:
        """Get historical data using the active provider."""
        if self.active_provider is None:
            print(f"No active provider for historical data {symbol}")
            return None
        return self.active_provider.get_historical_data(symbol, period, interval)

    def get_top_gainers(self, limit: int = 50) -> List[Dict]:
        """Get top gainers using the active provider."""
        if self.active_provider is None:
            print("No active provider for top gainers")
            return []
        return self.active_provider.get_top_gainers(limit)
