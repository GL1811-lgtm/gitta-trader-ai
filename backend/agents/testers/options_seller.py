import random
from datetime import datetime

class OptionsSellerAgent:
    """
    Tester 1: Options Seller
    Simulates selling options (Straddles/Strangles) to profit from Theta decay.
    """
    
    def __init__(self):
        self.name = "Options Seller (Theta Eater)"
        self.capital = 100000
        self.pnl = 0

    def simulate_day(self, market_data):
        """
        Simulate one day of options selling.
        """
        # Mock Logic:
        # Sell at Open, Buy back at Close.
        # Profit if VIX drops or market stays range-bound.
        
        vix = market_data.get("INDIAVIX", {}).get("lastPrice", 15)
        nifty_change = abs(market_data.get("NIFTY", {}).get("pChange", 0))
        
        # Theta decay gives small consistent profit
        theta_gain = random.uniform(100, 500)
        
        # Gamma risk: If market moves too much, we lose
        gamma_loss = 0
        if nifty_change > 1.0: # Big move > 1%
            gamma_loss = random.uniform(1000, 3000)
            
        daily_pnl = theta_gain - gamma_loss
        self.pnl += daily_pnl
        
        return {
            "agent": self.name,
            "action": "SOLD STRADDLE",
            "pnl": round(daily_pnl, 2),
            "total_pnl": round(self.pnl, 2),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

if __name__ == "__main__":
    agent = OptionsSellerAgent()
    print(agent.simulate_day({"NIFTY": {"pChange": 0.5}, "INDIAVIX": {"lastPrice": 12}}))
