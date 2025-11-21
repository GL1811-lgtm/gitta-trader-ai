import logging
from backend.database.db import db
from backend.data_providers.manager import DataProviderManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PaperTradingEngine:
    """
    Simulates stock trading with a virtual account.
    """
    def __init__(self):
        self.data_provider = DataProviderManager()

    def get_account_summary(self):
        """Returns balance and total portfolio value."""
        balance = db.get_account_balance()
        portfolio = db.get_portfolio()
        
        portfolio_value = 0.0
        holdings = []

        for item in portfolio:
            symbol = item['symbol']
            qty = item['quantity']
            avg_price = item['avg_price']
            
            # Get real-time price
            current_price = self.data_provider.get_live_price(symbol)
            if not current_price:
                current_price = avg_price # Fallback if API fails
            
            current_val = qty * current_price
            portfolio_value += current_val
            
            pnl = (current_price - avg_price) * qty
            pnl_percent = (pnl / (avg_price * qty)) * 100 if avg_price > 0 else 0

            holdings.append({
                "symbol": symbol,
                "quantity": qty,
                "avg_price": round(avg_price, 2),
                "current_price": round(current_price, 2),
                "current_value": round(current_val, 2),
                "pnl": round(pnl, 2),
                "pnl_percent": round(pnl_percent, 2)
            })

        total_equity = balance + portfolio_value
        
        return {
            "balance": round(balance, 2),
            "portfolio_value": round(portfolio_value, 2),
            "total_equity": round(total_equity, 2),
            "holdings": holdings
        }

    def place_order(self, symbol, side, quantity, price=None):
        """
        Executes a MARKET or LIMIT order.
        side: 'BUY' or 'SELL'
        price: Optional limit price. If None, fetches current market price.
        """
        try:
            # 1. Get execution price
            if price is None or price <= 0:
                price = self.data_provider.get_live_price(symbol)
            
            if not price:
                return {"status": "failed", "message": f"Could not fetch price for {symbol}"}

            total_cost = price * quantity
            balance = db.get_account_balance()

            # 2. Validate Order
            if side == 'BUY':
                if balance < total_cost:
                    return {"status": "failed", "message": "Insufficient funds"}
                
                # Execute Buy
                db.update_balance(-total_cost)
                db.update_portfolio(symbol, quantity, price)
                db.add_transaction(symbol, 'BUY', quantity, price)
                
                return {
                    "status": "success", 
                    "message": f"Bought {quantity} {symbol} @ ₹{price}",
                    "price": price,
                    "total": total_cost
                }

            elif side == 'SELL':
                # Check holdings
                portfolio = db.get_portfolio()
                holding = next((item for item in portfolio if item['symbol'] == symbol), None)
                
                if not holding or holding['quantity'] < quantity:
                    return {"status": "failed", "message": "Insufficient holdings"}
                
                # Execute Sell
                db.update_balance(total_cost)
                db.update_portfolio(symbol, -quantity, price)
                db.add_transaction(symbol, 'SELL', quantity, price)

                return {
                    "status": "success", 
                    "message": f"Sold {quantity} {symbol} @ ₹{price}",
                    "price": price,
                    "total": total_cost
                }
            
            else:
                return {"status": "failed", "message": "Invalid order side"}

        except Exception as e:
            logger.error(f"Order execution failed: {e}")
            return {"status": "error", "message": str(e)}

    def reset_account(self):
        """Resets account to initial state."""
        # This would require a DB method to clear tables, for now we can just update balance
        # Ideally we truncate tables but let's just set balance for safety
        # Implementation pending full reset logic in DB
        pass
