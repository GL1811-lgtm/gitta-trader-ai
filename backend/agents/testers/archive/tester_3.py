import asyncio
import random
from backend.agents.testers.base_tester import BaseTesterAgent

class TesterAgent3(BaseTesterAgent):
    def __init__(self):
        super().__init__("tester_3", "Balanced Tester", risk_profile="medium")

    async def test_strategy(self, strategy):
        await asyncio.sleep(random.uniform(1, 3))
        win_rate = random.uniform(45, 65)
        profit_factor = random.uniform(1.1, 1.6)
        total_trades = random.randint(20, 80)
        net_profit = total_trades * (win_rate/100 * 120 - (1 - win_rate/100) * 80)
        sharpe_ratio = random.uniform(0.8, 1.8)
        recommendation = "PASS" if win_rate > 50 and profit_factor > 1.2 else "FAIL"
        return {
            "win_rate": round(win_rate, 2),
            "profit_factor": round(profit_factor, 2),
            "total_trades": total_trades,
            "net_profit": round(net_profit, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "recommendation": recommendation
        }
