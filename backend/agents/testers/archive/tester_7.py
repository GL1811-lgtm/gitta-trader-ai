import asyncio
import random
from backend.agents.testers.base_tester import BaseTesterAgent

class TesterAgent7(BaseTesterAgent):
    def __init__(self):
        super().__init__("tester_7", "Position Trader", risk_profile="long_term")

    async def test_strategy(self, strategy):
        await asyncio.sleep(random.uniform(1, 3))
        win_rate = random.uniform(55, 70)
        profit_factor = random.uniform(1.5, 2.5)
        total_trades = random.randint(5, 15) # Very low volume
        net_profit = total_trades * (win_rate/100 * 500 - (1 - win_rate/100) * 200)
        sharpe_ratio = random.uniform(1.2, 2.0)
        recommendation = "PASS" if profit_factor > 1.6 else "FAIL"
        return {
            "win_rate": round(win_rate, 2),
            "profit_factor": round(profit_factor, 2),
            "total_trades": total_trades,
            "net_profit": round(net_profit, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "recommendation": recommendation
        }
