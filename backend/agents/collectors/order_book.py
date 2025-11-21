import logging
from typing import Dict, List, Any
import random
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OrderBookAnalyzer:
    """
    Collector Agent 3: Order Book Intelligence
    Responsibility: Analyze bid/ask depth, detect iceberg orders, calculate imbalance.
    """
    def __init__(self):
        self.name = "OrderBookAnalyzer"
        self.status = "initialized"

    def get_order_book(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch Level 2 order book data.
        """
        try:
            # Placeholder for actual L2 data fetch
            # In reality, this would connect to a broker API or data feed
            
            # Simulating 5 levels of depth
            bids = [{"price": 24500 - i*5, "qty": random.randint(100, 1000)} for i in range(5)]
            asks = [{"price": 24500 + i*5, "qty": random.randint(100, 1000)} for i in range(5)]
            
            return {
                "symbol": symbol,
                "bids": bids,
                "asks": asks,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error fetching order book for {symbol}: {e}")
            return {}

    def detect_iceberg_orders(self, order_book: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Detect potential iceberg orders (large orders hidden as small ones).
        Logic: Look for consistent reloading of quantity at a specific price level.
        """
        try:
            # This requires tracking order book changes over time.
            # For this stateless method, we'll return a mock detection.
            
            # Mock detection logic:
            icebergs = []
            if random.random() < 0.1: # 10% chance to detect one
                icebergs.append({
                    "type": "BUY" if random.random() > 0.5 else "SELL",
                    "price": 24500,
                    "estimated_qty": 5000,
                    "visible_qty": 500
                })
            return icebergs
        except Exception as e:
            logger.error(f"Error detecting iceberg orders: {e}")
            return []

    def calculate_imbalance(self, order_book: Dict[str, Any]) -> float:
        """
        Calculate buy/sell pressure imbalance (-1.0 to +1.0).
        Positive = Buy pressure, Negative = Sell pressure.
        """
        try:
            bids = order_book.get("bids", [])
            asks = order_book.get("asks", [])
            
            if not bids or not asks:
                return 0.0
            
            total_bid_qty = sum(b["qty"] for b in bids)
            total_ask_qty = sum(a["qty"] for a in asks)
            
            total_qty = total_bid_qty + total_ask_qty
            if total_qty == 0:
                return 0.0
                
            imbalance = (total_bid_qty - total_ask_qty) / total_qty
            return float(imbalance)
        except Exception as e:
            logger.error(f"Error calculating imbalance: {e}")
            return 0.0

    def predict_next_tick(self, imbalance: float) -> str:
        """
        Predict next tick direction based on imbalance.
        """
        if imbalance > 0.3:
            return "UP"
        elif imbalance < -0.3:
            return "DOWN"
        else:
            return "NEUTRAL"

if __name__ == "__main__":
    analyzer = OrderBookAnalyzer()
    ob = analyzer.get_order_book("NIFTY")
    print(f"Order Book: {ob}")
    imb = analyzer.calculate_imbalance(ob)
    print(f"Imbalance: {imb}")
    print(f"Prediction: {analyzer.predict_next_tick(imb)}")
