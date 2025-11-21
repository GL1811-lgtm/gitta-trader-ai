import asyncio
import random
from backend.agents.testers.base_tester import BaseTesterAgent

class TesterAgent4(BaseTesterAgent):
    def __init__(self):
        super().__init__("tester_4", "Scalping Tester", risk_profile="high_frequency")

    async def test_strategy(self, strategy):
        await asyncio.sleep(random.uniform(1, 3))
        win_rate = random.uniform(40, 70)
        profit_factor = random.uniform(1.0, 1.5)
        total_trades = random.randint(100, 500) # High volume
        net_profit = total_trades * (win_rate/100 * 20 - (1 - win_rate/100) * 15) # Small gains/losses
        sharpe_ratio = random.uniform(0.5, 2.0)
        recommendation = "PASS" if net_profit > 500 and profit_factor > 1.1 else "FAIL"
        return {
            "win_rate": round(win_rate, 2),
            "profit_factor": round(profit_factor, 2),
            "total_trades": total_trades,
            "net_profit": round(net_profit, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "recommendation": recommendation
        }
