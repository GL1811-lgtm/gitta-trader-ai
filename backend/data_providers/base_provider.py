from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import pandas as pd

class BaseDataProvider(ABC):
    """
    Abstract base class for all data providers.
    Ensures a consistent interface for fetching market data.
    """

    @abstractmethod
    def connect(self) -> bool:
        """
        Establish connection to the data provider.
        Returns True if successful, False otherwise.
        """
        pass

    @abstractmethod
    def get_live_price(self, symbol: str) -> Optional[float]:
        """
        Get the current live price for a symbol.
        Returns None if data is unavailable.
        """
        pass

    @abstractmethod
    def get_historical_data(self, symbol: str, period: str = "1mo", interval: str = "1d") -> Optional[pd.DataFrame]:
        """
        Get historical data for a symbol.
        Returns a DataFrame with columns: [Open, High, Low, Close, Volume]
        """
        pass

    @abstractmethod
    def get_top_gainers(self, limit: int = 50) -> List[Dict]:
        """
        Get the top gainers for the day.
        Returns a list of dictionaries with symbol and percent change.
        """
        pass
