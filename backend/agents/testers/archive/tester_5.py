import asyncio
import random
from backend.agents.testers.base_tester import BaseTesterAgent

class TesterAgent5(BaseTesterAgent):
    def __init__(self):
        super().__init__("tester_5", "Swing Tester", risk_profile="medium")

    async def test_strategy(self, strategy):
        await asyncio.sleep(random.uniform(1, 3))
        win_rate = random.uniform(40, 60)
        profit_factor = random.uniform(1.3, 2.0)
        total_trades = random.randint(10, 30) # Low volume
        net_profit = total_trades * (win_rate/100 * 300 - (1 - win_rate/100) * 150) # Larger moves
        sharpe_ratio = random.uniform(0.8, 1.6)
        recommendation = "PASS" if profit_factor > 1.4 else "FAIL"
        return {
            "win_rate": round(win_rate, 2),
            "profit_factor": round(profit_factor, 2),
            "total_trades": total_trades,
            "net_profit": round(net_profit, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "recommendation": recommendation
        }
