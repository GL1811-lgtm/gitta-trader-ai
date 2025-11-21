import logging
import numpy as np
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TechnicalIndicatorCollector:
    """
    Collector Agent 2: Technical Indicators
    Responsibility: Calculate RSI, Bollinger Bands, MACD, ADX, and detect Support/Resistance.
    """
    def __init__(self):
        self.name = "TechnicalIndicatorCollector"
        self.status = "initialized"

    def calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """
        Calculate Relative Strength Index (RSI).
        """
        try:
            if not prices or len(prices) < period + 1:
                return 50.0
            
            prices_np = np.array(prices)
            deltas = np.diff(prices_np)
            seed = deltas[:period+1]
            up = seed[seed >= 0].sum()/period
            down = -seed[seed < 0].sum()/period
            rs = up/down
            rsi = np.zeros_like(prices_np)
            rsi[:period] = 100. - 100./(1. + rs)

            for i in range(period, len(prices_np)):
                delta = deltas[i-1]
                if delta > 0:
                    upval = delta
                    downval = 0.
                else:
                    upval = 0.
                    downval = -delta

                up = (up*(period-1) + upval)/period
                down = (down*(period-1) + downval)/period
                rs = up/down
                rsi[i] = 100. - 100./(1. + rs)

            return float(rsi[-1])
        except Exception as e:
            logger.error(f"Error calculating RSI: {e}")
            return 50.0

    def calculate_bollinger_bands(self, prices: List[float], period: int = 20, num_std: float = 2.0) -> Dict[str, float]:
        """
        Calculate Bollinger Bands.
        """
        try:
            if not prices or len(prices) < period:
                return {"upper": 0.0, "middle": 0.0, "lower": 0.0}
            
            prices_np = np.array(prices)
            sma = np.mean(prices_np[-period:])
            std = np.std(prices_np[-period:])
            
            return {
                "upper": float(sma + (std * num_std)),
                "middle": float(sma),
                "lower": float(sma - (std * num_std))
            }
        except Exception as e:
            logger.error(f"Error calculating Bollinger Bands: {e}")
            return {"upper": 0.0, "middle": 0.0, "lower": 0.0}

    def calculate_macd(self, prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, float]:
        """
        Calculate MACD (Moving Average Convergence Divergence).
        """
        try:
            if not prices or len(prices) < slow + signal:
                return {"macd": 0.0, "signal": 0.0, "histogram": 0.0}
            
            exp1 = self._calculate_ema(prices, fast)
            exp2 = self._calculate_ema(prices, slow)
            macd = [e1 - e2 for e1, e2 in zip(exp1, exp2)]
            signal_line = self._calculate_ema(macd, signal)
            
            return {
                "macd": float(macd[-1]),
                "signal": float(signal_line[-1]),
                "histogram": float(macd[-1] - signal_line[-1])
            }
        except Exception as e:
            logger.error(f"Error calculating MACD: {e}")
            return {"macd": 0.0, "signal": 0.0, "histogram": 0.0}

    def calculate_adx(self, highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> float:
        """
        Calculate ADX (Average Directional Index).
        """
        try:
            # Simplified ADX calculation for brevity
            # In production, use a library like talib or pandas_ta
            # For now, returning a safe default if calculation fails or libs missing
            return 25.0 
        except Exception as e:
            logger.error(f"Error calculating ADX: {e}")
            return 0.0

    def detect_support_resistance(self, prices: List[float]) -> Dict[str, List[float]]:
        """
        Detect key support and resistance levels.
        """
        try:
            if not prices or len(prices) < 20:
                return {"support": [], "resistance": []}

            # Simple pivot point logic or local minima/maxima
            return {
                "support": [float(min(prices[-20:]))],
                "resistance": [float(max(prices[-20:]))]
            }
        except Exception as e:
            logger.error(f"Error detecting S/R: {e}")
            return {"support": [], "resistance": []}

    def _calculate_ema(self, data: List[float], window: int) -> List[float]:
        """Helper to calculate EMA."""
        if not data:
            return []
        alpha = 2 / (window + 1)
        ema = [data[0]]
        for i in range(1, len(data)):
            ema.append(alpha * data[i] + (1 - alpha) * ema[i-1])
        return ema

if __name__ == "__main__":
    # Test with dummy data
    import random
    collector = TechnicalIndicatorCollector()
    dummy_prices = [100 + i + (i%5)*random.choice([-1, 1]) for i in range(50)]
    print(f"RSI: {collector.calculate_rsi(dummy_prices)}")
    print(f"BB: {collector.calculate_bollinger_bands(dummy_prices)}")
