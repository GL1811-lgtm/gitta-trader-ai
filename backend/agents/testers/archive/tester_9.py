import asyncio
import random
from backend.agents.testers.base_tester import BaseTesterAgent

class TesterAgent9(BaseTesterAgent):
    def __init__(self):
        super().__init__("tester_9", "Trend Follower", risk_profile="medium")

    async def test_strategy(self, strategy):
        await asyncio.sleep(random.uniform(1, 3))
        win_rate = random.uniform(40, 55) # Trend following often has lower win rate
        profit_factor = random.uniform(1.4, 2.2) # But big wins
        total_trades = random.randint(20, 60)
        net_profit = total_trades * (win_rate/100 * 200 - (1 - win_rate/100) * 80)
        sharpe_ratio = random.uniform(0.9, 1.7)
        recommendation = "PASS" if profit_factor > 1.5 else "FAIL"
        return {
            "win_rate": round(win_rate, 2),
            "profit_factor": round(profit_factor, 2),
            "total_trades": total_trades,
            "net_profit": round(net_profit, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "recommendation": recommendation
        }
