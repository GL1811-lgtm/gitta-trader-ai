import asyncio
import random
from backend.agents.testers.base_tester import BaseTesterAgent

class TesterAgent2(BaseTesterAgent):
    def __init__(self):
        super().__init__("tester_2", "Aggressive Tester", risk_profile="high")

    async def test_strategy(self, strategy):
        """
        Simulate aggressive trading:
        - High risk, potential for high reward (or big loss).
        """
        await asyncio.sleep(random.uniform(1, 3))
        
        # Aggressive simulation:
        win_rate = random.uniform(30, 60) # Lower win rate often
        profit_factor = random.uniform(0.8, 2.5) # Volatile
        total_trades = random.randint(50, 200) # More trades
        net_profit = total_trades * (win_rate/100 * 200 - (1 - win_rate/100) * 100)
        sharpe_ratio = random.uniform(0.5, 1.5)
        
        recommendation = "PASS" if net_profit > 1000 and profit_factor > 1.3 else "FAIL"
        
        return {
            "win_rate": round(win_rate, 2),
            "profit_factor": round(profit_factor, 2),
            "total_trades": total_trades,
            "net_profit": round(net_profit, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "recommendation": recommendation
        }
