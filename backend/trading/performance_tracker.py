import math
from typing import List, Dict
from backend.database.db import db
from backend.utils.logger import logger

class PerformanceTracker:
    """
    Tracks and calculates performance metrics for paper trading validation.
    """
    
    @staticmethod
    def calculate_win_rate(trades: List[Dict]) -> float:
        """Calculate percentage of winning trades."""
        if not trades:
            return 0.0
        winning_trades = sum(1 for t in trades if t.get('pnl', 0) > 0)
        return (winning_trades / len(trades)) * 100
    
    @staticmethod
    def calculate_profit_factor(trades: List[Dict]) -> float:
        """Calculate profit factor (gross profit / gross loss)."""
        gross_profit = sum(t.get('pnl', 0) for t in trades if t.get('pnl', 0) > 0)
        gross_loss = abs(sum(t.get('pnl', 0) for t in trades if t.get('pnl', 0) < 0))
        
        if gross_loss == 0:
            return float('inf') if gross_profit > 0 else 0.0
        return gross_profit / gross_loss
    
    @staticmethod
    def calculate_max_drawdown(equity_curve: List[float]) -> float:
        """Calculate maximum drawdown percentage."""
        if not equity_curve or len(equity_curve) < 2:
            return 0.0
        
        peak = equity_curve[0]
        max_dd = 0.0
        
        for value in equity_curve:
            if value > peak:
                peak = value
            drawdown = ((peak - value) / peak) * 100
            if drawdown > max_dd:
                max_dd = drawdown
        
        return max_dd
    
    @staticmethod
    def calculate_sharpe_ratio(returns: List[float], risk_free_rate=0.05) -> float:
        """
        Calculate Sharpe ratio (annualized).
        returns: List of daily returns as decimals
        """
        if not returns or len(returns) < 2:
            return 0.0
        
        avg_return = sum(returns) / len(returns)
        
        # Calculate standard deviation
        variance = sum((r - avg_return) ** 2 for r in returns) / len(returns)
        std_dev = math.sqrt(variance)
        
        if std_dev == 0:
            return 0.0
        
        # Annualize (assuming 252 trading days)
        annualized_return = avg_return * 252
        annualized_std = std_dev * math.sqrt(252)
        
        sharpe = (annualized_return - risk_free_rate) / annualized_std
        return sharpe
    
    @staticmethod
    def generate_performance_report(session_id: str) -> Dict:
        """Generate comprehensive performance report for a validation session."""
        # Get all trades for this session
        trades = db.get_validation_trades(session_id)
        
        if not trades:
            return {
                "session_id": session_id,
                "total_trades": 0,
                "message": "No trades executed yet"
            }
        
        # Calculate metrics
        win_rate = PerformanceTracker.calculate_win_rate(trades)
        profit_factor = PerformanceTracker.calculate_profit_factor(trades)
        
        total_pnl = sum(t.get('pnl', 0) for t in trades)
        
        # Get equity curve for drawdown
        equity_curve = db.get_equity_curve(session_id)
        max_drawdown = PerformanceTracker.calculate_max_drawdown(equity_curve)
        
        # Calculate returns for Sharpe
        returns = []
        for i in range(1, len(equity_curve)):
            daily_return = (equity_curve[i] - equity_curve[i-1]) / equity_curve[i-1]
            returns.append(daily_return)
        
        sharpe_ratio = PerformanceTracker.calculate_sharpe_ratio(returns)
        
        return {
            "session_id": session_id,
            "total_trades": len(trades),
            "win_rate": round(win_rate, 2),
            "profit_factor": round(profit_factor, 2),
            "total_pnl": round(total_pnl, 2),
            "max_drawdown": round(max_drawdown, 2),
            "sharpe_ratio": round(sharpe_ratio, 2),
            "avg_trade_pnl": round(total_pnl / len(trades), 2) if trades else 0
        }
