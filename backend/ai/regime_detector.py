import numpy as np
from typing import Dict, List
from datetime import datetime
from backend.utils.logger import logger

class RegimeDetector:
    """
    Detects current market regime (trending, ranging, volatile, quiet).
    Helps strategies adapt to changing market conditions.
    """
    
    def __init__(self):
        self.current_regime = 'unknown'
        self.regime_history = []
    
    def calculate_volatility(self, prices: List[float], window=20) -> float:
        """Calculate price volatility (standard deviation of returns)."""
        if len(prices) < window + 1:
            return 0.0
        
        recent_prices = prices[-window-1:]
        returns = [(recent_prices[i] - recent_prices[i-1]) / recent_prices[i-1] 
                   for i in range(1, len(recent_prices))]
        
        return np.std(returns) if returns else 0.0
    
    def calculate_trend_strength(self, prices: List[float], window=20) -> float:
        """
        Calculate trend strength using linear regression slope.
        Returns normalized value (0 to 1).
        """
        if len(prices) < window:
            return 0.0
        
        recent_prices = prices[-window:]
        x = np.arange(len(recent_prices))
        y = np.array(recent_prices)
        
        # Linear regression
        slope = np.polyfit(x, y, 1)[0]
        
        # Normalize slope relative to price level
        avg_price = np.mean(recent_prices)
        normalized_slope = abs(slope) / avg_price if avg_price > 0 else 0
        
        # Cap at 1.0
        return min(normalized_slope * 100, 1.0)
    
    def detect_range(self, prices: List[float], window=20, threshold=0.03) -> bool:
        """
        Detect if market is ranging (price stays within a tight range).
        threshold: percentage range (e.g., 0.03 = 3%)
        """
        if len(prices) < window:
            return False
        
        recent_prices = prices[-window:]
        price_range = (max(recent_prices) - min(recent_prices)) / np.mean(recent_prices)
        
        return price_range < threshold
    
    def classify_regime(self, prices: List[float]) -> Dict:
        """
        Classify current market regime.
        
        Returns: {
            'regime': str ('trending_up', 'trending_down', 'ranging', 'volatile', 'quiet'),
            'confidence': float (0 to 1),
            'metrics': dict with volatility, trend_strength, etc.
        }
        """
        if len(prices) < 21:
            return {
                'regime': 'unknown',
                'confidence': 0.0,
                'metrics': {}
            }
        
        # Calculate metrics
        volatility = self.calculate_volatility(prices)
        trend_strength = self.calculate_trend_strength(prices)
        is_ranging = self.detect_range(prices)
        
        # Price direction
        price_change = (prices[-1] - prices[-20]) / prices[-20]
        
        # Classify regime
        regime = 'unknown'
        confidence = 0.5
        
        # High volatility
        if volatility > 0.02:  # 2% daily volatility
            regime = 'volatile'
            confidence = min(volatility / 0.03, 1.0)
        
        # Low volatility
        elif volatility < 0.005:  # 0.5% daily volatility
            regime = 'quiet'
            confidence = 1.0 - (volatility / 0.005)
        
        # Ranging market
        elif is_ranging and trend_strength < 0.3:
            regime = 'ranging'
            confidence = 0.7
        
        # Trending market
        elif trend_strength > 0.4:
            if price_change > 0.02:
                regime = 'trending_up'
            elif price_change < -0.02:
                regime = 'trending_down'
            else:
                regime = 'trending_up' if price_change > 0 else 'trending_down'
            
            confidence = min(trend_strength, 1.0)
        
        # Default to ranging
        else:
            regime = 'ranging'
            confidence = 0.6
        
        self.current_regime = regime
        
        result = {
            'regime': regime,
            'confidence': round(confidence, 3),
            'metrics': {
                'volatility': round(volatility, 4),
                'trend_strength': round(trend_strength, 3),
                'price_change_20d': round(price_change * 100, 2),  # percentage
                'is_ranging': is_ranging
            },
            'timestamp': datetime.now().isoformat()
        }
        
        self.regime_history.append(result)
        
        return result
    
    def get_strategy_adjustment(self, regime: str) -> Dict:
        """
        Suggest strategy parameter adjustments based on regime.
        """
        adjustments = {
            'trending_up': {
                'position_sizing': 'increase',
                'stop_loss': 'wider',
                'take_profit': 'trailing',
                'strategy_type': 'momentum'
            },
            'trending_down': {
                'position_sizing': 'reduce',
                'stop_loss': 'tight',
                'take_profit': 'quick',
                'strategy_type': 'short_selling'
            },
            'ranging': {
                'position_sizing': 'moderate',
                'stop_loss': 'tight',
                'take_profit': 'fixed',
                'strategy_type': 'mean_reversion'
            },
            'volatile': {
                'position_sizing': 'reduce',
                'stop_loss': 'very_tight',
                'take_profit': 'quick',
                'strategy_type': 'scalping'
            },
            'quiet': {
                'position_sizing': 'moderate',
                'stop_loss': 'moderate',
                'take_profit': 'patient',
                'strategy_type': 'swing'
            }
        }
        
        return adjustments.get(regime, {
            'position_sizing': 'moderate',
            'stop_loss': 'moderate',
            'take_profit': 'moderate',
            'strategy_type': 'balanced'
        })
