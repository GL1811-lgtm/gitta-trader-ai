import numpy as np
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

class FitnessCalculator:
    """
    Calculates fitness score for a trading strategy based on performance metrics.
    """
    
    def __init__(self):
        # Weights for different metrics
        self.weights = {
            "sharpe": 0.40,
            "sortino": 0.30,
            "win_rate": 0.20,
            "drawdown": 0.10
        }
        
    def calculate_fitness(self, results: Dict[str, Any]) -> float:
        """
        Calculate weighted fitness score (0.0 to 1.0+).
        
        Args:
            results: Dictionary containing backtest results:
                     - sharpe_ratio
                     - sortino_ratio
                     - win_rate (0-100)
                     - max_drawdown (0-100, positive value representing % drop)
                     - total_trades
        """
        try:
            if not results or results.get("total_trades", 0) < 10:
                return 0.0 # Penalize strategies with too few trades
                
            # 1. Sharpe Score (Target > 1.0, Cap at 3.0)
            sharpe = results.get("sharpe_ratio", 0.0)
            sharpe_score = min(max(sharpe, 0), 3.0) / 3.0
            
            # 2. Sortino Score (Target > 1.5, Cap at 5.0)
            sortino = results.get("sortino_ratio", 0.0)
            sortino_score = min(max(sortino, 0), 5.0) / 5.0
            
            # 3. Win Rate Score (Target 60%+, Linear scale)
            win_rate = results.get("win_rate", 0.0)
            win_rate_score = min(win_rate, 100.0) / 100.0
            
            # 4. Drawdown Penalty (Target < 10%, Inverse scale)
            max_dd = abs(results.get("max_drawdown", 100.0))
            # Score is 1.0 if DD is 0%, 0.0 if DD is 30%+
            dd_score = max(0, (30.0 - max_dd) / 30.0)
            
            # Weighted Sum
            fitness = (
                (sharpe_score * self.weights["sharpe"]) +
                (sortino_score * self.weights["sortino"]) +
                (win_rate_score * self.weights["win_rate"]) +
                (dd_score * self.weights["drawdown"])
            )
            
            return round(fitness, 4)
            
        except Exception as e:
            logger.error(f"Error calculating fitness: {e}")
            return 0.0
