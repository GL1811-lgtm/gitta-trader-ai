import asyncio
import random
from backend.agents.testers.base_tester import BaseTesterAgent

class TesterAgent1(BaseTesterAgent):
    def __init__(self):
        super().__init__("tester_1", "Conservative Tester", risk_profile="low")

    async def test_strategy(self, strategy):
        """
        Simulate conservative trading:
        - Low win rate but high profit factor? Or high win rate, low risk?
        - Conservative usually means tight stops, lower risk per trade.
        """
        await asyncio.sleep(random.uniform(1, 3)) # Simulate processing time
        
        # Mock logic based on strategy content
        # In a real system, we'd parse strategy['content'] and run a backtest.
        
        # Conservative simulation:
        win_rate = random.uniform(55, 75)
        profit_factor = random.uniform(1.2, 1.8)
        total_trades = random.randint(10, 50)
        net_profit = total_trades * (win_rate/100 * 100 - (1 - win_rate/100) * 50) # Mock profit calc
        sharpe_ratio = random.uniform(1.0, 2.0)
        
        recommendation = "PASS" if win_rate > 60 and profit_factor > 1.5 else "FAIL"
        
        return {
            "win_rate": round(win_rate, 2),
            "profit_factor": round(profit_factor, 2),
            "total_trades": total_trades,
            "net_profit": round(net_profit, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "recommendation": recommendation
        }
