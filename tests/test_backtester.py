import pytest
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.intelligence.backtester import BacktestEngine
import pandas as pd

def test_backtest_engine():
    engine = BacktestEngine()
    
    # We can mock the data provider, but for an integration test we can try a real fetch
    # or just test the logic with a dummy dataframe if we want to be pure unit test.
    # Let's try a real fetch for "RELIANCE.NS" as it's robust.
    
    result = engine.run_backtest("RELIANCE.NS", strategy="SMA_CROSSOVER", period="1mo")
    
    if "error" in result:
        # If data fetch fails (e.g. no internet), we skip
        pytest.skip(f"Data fetch failed: {result['error']}")
        
    assert "final_equity" in result
    assert "total_return_pct" in result
    assert "max_drawdown_pct" in result
    assert isinstance(result['trades'], list)
    
    print(f"Backtest Result: {result}")

if __name__ == "__main__":
    test_backtest_engine()
