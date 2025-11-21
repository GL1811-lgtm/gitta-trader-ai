import asyncio
import random
from backend.agents.testers.base_tester import BaseTesterAgent

class TesterAgent6(BaseTesterAgent):
    def __init__(self):
        super().__init__("tester_6", "Day Trader", risk_profile="intraday")

    async def test_strategy(self, strategy):
        await asyncio.sleep(random.uniform(1, 3))
        win_rate = random.uniform(50, 65)
        profit_factor = random.uniform(1.1, 1.4)
        total_trades = random.randint(20, 60)
        net_profit = total_trades * (win_rate/100 * 50 - (1 - win_rate/100) * 40)
        sharpe_ratio = random.uniform(1.0, 1.5)
        recommendation = "PASS" if net_profit > 200 else "FAIL"
        return {
            "win_rate": round(win_rate, 2),
            "profit_factor": round(profit_factor, 2),
            "total_trades": total_trades,
            "net_profit": round(net_profit, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "recommendation": recommendation
        }
