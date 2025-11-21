import numpy as np
from typing import Dict, List, Optional
from backend.utils.logger import logger

class PatternDetector:
    """
    Detects chart patterns and candlestick formations in price data.
    """
    
    def __init__(self):
        self.patterns_detected = []
    
    def detect_support_resistance(self, prices: List[float], window=20) -> Dict:
        """
        Detect support and resistance levels.
        """
        if len(prices) < window:
            return {'support': None, 'resistance': None}
        
        recent_prices = prices[-window:]
        
        # Simple approach: recent min/max
        support = min(recent_prices)
        resistance = max(recent_prices)
        current = prices[-1]
        
        return {
            'support': round(support, 2),
            'resistance': round(resistance, 2),
            'current': round(current, 2),
            'distance_to_support': round(((current - support) / support) * 100, 2),
            'distance_to_resistance': round(((resistance - current) / current) * 100, 2)
        }
    
    def detect_doji(self, open_price: float, high: float, low: float, close: float) -> bool:
        """
        Detect Doji candlestick pattern.
        Doji: Open and close are very close (small body).
        """
        body = abs(close - open_price)
        range_size = high - low
        
        if range_size == 0:
            return False
        
        # Doji if body is less than 10% of range
        return (body / range_size) < 0.1
    
    def detect_hammer(self, open_price: float, high: float, low: float, close: float) -> bool:
        """
        Detect Hammer candlestick pattern (bullish reversal).
        Hammer: Small body at top, long lower shadow.
        """
        body = abs(close - open_price)
        lower_shadow = min(open_price, close) - low
        upper_shadow = high - max(open_price, close)
        
        if body == 0:
            return False
        
        # Hammer: lower shadow at least 2x body, small upper shadow
        return lower_shadow > (2 * body) and upper_shadow < body
    
    def detect_engulfing(self, prev_candle: Dict, curr_candle: Dict) -> Optional[str]:
        """
        Detect Engulfing pattern (bullish or bearish).
        Returns: 'bullish_engulfing', 'bearish_engulfing', or None
        """
        prev_body = abs(prev_candle['close'] - prev_candle['open'])
        curr_body = abs(curr_candle['close'] - curr_candle['open'])
        
        # Bullish engulfing: prev red, curr green, curr engulfs prev
        if (prev_candle['close'] < prev_candle['open'] and
            curr_candle['close'] > curr_candle['open'] and
            curr_body > prev_body and
            curr_candle['close'] > prev_candle['open'] and
            curr_candle['open'] < prev_candle['close']):
            return 'bullish_engulfing'
        
        # Bearish engulfing: prev green, curr red, curr engulfs prev
        if (prev_candle['close'] > prev_candle['open'] and
            curr_candle['close'] < curr_candle['open'] and
            curr_body > prev_body and
            curr_candle['close'] < prev_candle['open'] and
            curr_candle['open'] > prev_candle['close']):
            return 'bearish_engulfing'
        
        return None
    
    def detect_double_top(self, prices: List[float], tolerance=0.02) -> bool:
        """
        Detect Double Top pattern (bearish).
        Two peaks at similar levels with a trough between.
        """
        if len(prices) < 20:
            return False
        
        # Find peaks (local maxima)
        peaks = []
        for i in range(1, len(prices) - 1):
            if prices[i] > prices[i-1] and prices[i] > prices[i+1]:
                peaks.append((i, prices[i]))
        
        if len(peaks) < 2:
            return False
        
        # Check last two peaks
        peak1, peak2 = peaks[-2], peaks[-1]
        
        # Peaks should be at similar levels (within tolerance)
        if abs(peak1[1] - peak2[1]) / peak1[1] <= tolerance:
            # Should have a trough between
            trough_prices = prices[peak1[0]:peak2[0]]
            if trough_prices and min(trough_prices) < peak1[1] * 0.95:
                return True
        
        return False
    
    def detect_double_bottom(self, prices: List[float], tolerance=0.02) -> bool:
        """
        Detect Double Bottom pattern (bullish).
        Two troughs at similar levels with a peak between.
        """
        if len(prices) < 20:
            return False
        
        # Find troughs (local minima)
        troughs = []
        for i in range(1, len(prices) - 1):
            if prices[i] < prices[i-1] and prices[i] < prices[i+1]:
                troughs.append((i, prices[i]))
        
        if len(troughs) < 2:
            return False
        
        # Check last two troughs
        trough1, trough2 = troughs[-2], troughs[-1]
        
        # Troughs should be at similar levels
        if abs(trough1[1] - trough2[1]) / trough1[1] <= tolerance:
            # Should have a peak between
            peak_prices = prices[trough1[0]:trough2[0]]
            if peak_prices and max(peak_prices) > trough1[1] * 1.05:
                return True
        
        return False
    
    def analyze_patterns(self, price_data: List[Dict]) -> Dict:
        """
        Comprehensive pattern analysis on OHLC data.
        price_data: List of {'open', 'high', 'low', 'close', 'timestamp'}
        """
        if len(price_data) < 2:
            return {'patterns': [], 'signals': []}
        
        patterns = []
        signals = []
        
        # Get prices for pattern detection
        closes = [d['close'] for d in price_data]
        
        # Support/Resistance
        sr_levels = self.detect_support_resistance(closes)
        patterns.append({
            'type': 'support_resistance',
            'data': sr_levels
        })
        
        # Candlestick patterns on most recent candle
        latest = price_data[-1]
        
        if self.detect_doji(latest['open'], latest['high'], latest['low'], latest['close']):
            patterns.append({'type': 'doji', 'signal': 'indecision', 'confidence': 0.6})
            signals.append('indecision')
        
        if self.detect_hammer(latest['open'], latest['high'], latest['low'], latest['close']):
            patterns.append({'type': 'hammer', 'signal': 'bullish_reversal', 'confidence': 0.7})
            signals.append('bullish')
        
        # Engulfing (need 2 candles)
        if len(price_data) >= 2:
            engulfing = self.detect_engulfing(price_data[-2], price_data[-1])
            if engulfing:
                signal = 'bullish' if 'bullish' in engulfing else 'bearish'
                patterns.append({'type': engulfing, 'signal': signal, 'confidence': 0.75})
                signals.append(signal)
        
        # Chart patterns
        if self.detect_double_top(closes):
            patterns.append({'type': 'double_top', 'signal': 'bearish', 'confidence': 0.8})
            signals.append('bearish')
        
        if self.detect_double_bottom(closes):
            patterns.append({'type': 'double_bottom', 'signal': 'bullish', 'confidence': 0.8})
            signals.append('bullish')
        
        # Aggregate signal
        if signals:
            bullish_count = signals.count('bullish')
            bearish_count = signals.count('bearish')
            
            if bullish_count > bearish_count:
                overall_signal = 'bullish'
            elif bearish_count > bullish_count:
                overall_signal = 'bearish'
            else:
                overall_signal = 'neutral'
        else:
            overall_signal = 'neutral'
        
        return {
            'patterns': patterns,
            'overall_signal': overall_signal,
            'pattern_count': len(patterns),
            'timestamp': price_data[-1].get('timestamp')
        }
