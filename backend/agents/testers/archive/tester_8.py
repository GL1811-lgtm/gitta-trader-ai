import asyncio
import random
from backend.agents.testers.base_tester import BaseTesterAgent

class TesterAgent8(BaseTesterAgent):
    def __init__(self):
        super().__init__("tester_8", "Volatility Tester", risk_profile="high")

    async def test_strategy(self, strategy):
        await asyncio.sleep(random.uniform(1, 3))
        win_rate = random.uniform(35, 55)
        profit_factor = random.uniform(0.9, 2.2)
        total_trades = random.randint(30, 90)
        net_profit = total_trades * (win_rate/100 * 150 - (1 - win_rate/100) * 80)
        sharpe_ratio = random.uniform(0.6, 1.4)
        recommendation = "PASS" if net_profit > 300 else "FAIL"
        return {
            "win_rate": round(win_rate, 2),
            "profit_factor": round(profit_factor, 2),
            "total_trades": total_trades,
            "net_profit": round(net_profit, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "recommendation": recommendation
        }
