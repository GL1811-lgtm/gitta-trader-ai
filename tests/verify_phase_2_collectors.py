import asyncio
import sys
import os
import pytest

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.agents.collectors.market_data import NSEDataCollector
from backend.agents.collectors.technical import TechnicalIndicatorCollector

@pytest.mark.asyncio
async def test_nse_collector():
    print("\nTesting NSEDataCollector...")
    collector = NSEDataCollector()
    
    # Test Indices
    indices = collector.get_indices()
    print(f"Indices: {indices}")
    assert "timestamp" in indices
    # We expect NIFTY 50 or BANKNIFTY if yfinance works, or at least empty dict if fails gracefully
    
    # Test VIX
    vix = collector.get_vix()
    print(f"VIX: {vix}")
    assert isinstance(vix, float)
    
    # Test Option Chain
    oc = collector.get_option_chain()
    print(f"Option Chain Keys: {oc.keys()}")
    assert "strikes" in oc

    # Test Snapshot Logic (Mock DB)
    # We won't actually write to DB in this quick test to avoid polluting, 
    # but we verified the code structure.

def test_technical_collector():
    print("\nTesting TechnicalIndicatorCollector...")
    collector = TechnicalIndicatorCollector()
    prices = [100, 101, 102, 101, 100, 99, 98, 99, 100, 101, 102, 103, 104, 105, 106]
    
    # Test RSI
    rsi = collector.calculate_rsi(prices, period=5)
    print(f"RSI: {rsi}")
    assert 0 <= rsi <= 100
    
    # Test BB
    bb = collector.calculate_bollinger_bands(prices, period=5)
    print(f"BB: {bb}")
    assert bb['upper'] >= bb['middle'] >= bb['lower']

if __name__ == "__main__":
    # Manual run
    asyncio.run(test_nse_collector())
    test_technical_collector()
