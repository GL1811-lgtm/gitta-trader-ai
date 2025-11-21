from backend.agents.testers.options_seller import OptionsSellerAgent
from backend.agents.testers.scalper import ScalperAgent
from backend.agents.testers.swing_trader import SwingTraderAgent
from backend.agents.testers.mean_reversion import MeanReversionAgent
from backend.agents.testers.adaptive_meta import AdaptiveMetaAgent

def verify_testers():
    print("--- Verifying Advanced Tester Agents ---")
    
    agents = [
        OptionsSellerAgent(),
        ScalperAgent(),
        SwingTraderAgent(),
        MeanReversionAgent(),
        AdaptiveMetaAgent()
    ]
    
    mock_market_data = {
        "NIFTY": {"pChange": 0.75, "lastPrice": 24000},
        "INDIAVIX": {"lastPrice": 14.5}
    }
    
    for agent in agents:
        print(f"\nTesting {agent.name}...")
        try:
            result = agent.simulate_day(mock_market_data)
            print(f"PASS: {result['action']} | PnL: {result['pnl']}")
        except Exception as e:
            print(f"FAIL: {e}")

if __name__ == "__main__":
    verify_testers()
