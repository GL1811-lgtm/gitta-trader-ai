import asyncio
import random
from backend.agents.testers.base_tester import BaseTesterAgent

class TesterAgent10(BaseTesterAgent):
    def __init__(self):
        super().__init__("tester_10", "Mean Reversion Tester", risk_profile="medium")

    async def test_strategy(self, strategy):
        await asyncio.sleep(random.uniform(1, 3))
        win_rate = random.uniform(60, 75) # High win rate
        profit_factor = random.uniform(1.1, 1.5) # Smaller wins
        total_trades = random.randint(40, 100)
        net_profit = total_trades * (win_rate/100 * 60 - (1 - win_rate/100) * 60)
        sharpe_ratio = random.uniform(1.1, 1.9)
        recommendation = "PASS" if win_rate > 65 else "FAIL"
        return {
            "win_rate": round(win_rate, 2),
            "profit_factor": round(profit_factor, 2),
            "total_trades": total_trades,
            "net_profit": round(net_profit, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "recommendation": recommendation
        }
