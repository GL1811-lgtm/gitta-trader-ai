from typing import Dict, List
from datetime import datetime, timedelta
try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    
from backend.utils.logger import logger

class SentimentAnalyzer:
    """
    Analyzes sentiment from news headlines and market commentary.
    Uses TextBlob for lightweight, local sentiment analysis.
    """
    
    def __init__(self):
        if not TEXTBLOB_AVAILABLE:
            logger.warning("TextBlob not available. Install with: pip install textblob")
        self.sentiment_cache = {}
        
    def analyze_text(self, text: str) -> Dict:
        """
        Analyze sentiment of a single text.
        Returns: {
            'polarity': float (-1 to 1, negative to positive),
            'subjectivity': float (0 to 1, objective to subjective),
            'sentiment': str ('positive', 'negative', 'neutral')
        }
        """
        if not TEXTBLOB_AVAILABLE:
            return {'polarity': 0.0, 'subjectivity': 0.5, 'sentiment': 'neutral'}
        
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Classify sentiment
            if polarity > 0.1:
                sentiment = 'positive'
            elif polarity < -0.1:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            return {
                'polarity': round(polarity, 3),
                'subjectivity': round(subjectivity, 3),
                'sentiment': sentiment,
                'confidence': abs(polarity)
            }
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return {'polarity': 0.0, 'subjectivity': 0.5, 'sentiment': 'neutral'}
    
    def analyze_headlines(self, headlines: List[str]) -> Dict:
        """
        Analyze multiple headlines and aggregate sentiment.
        """
        if not headlines:
            return {'avg_polarity': 0.0, 'sentiment': 'neutral', 'count': 0}
        
        sentiments = [self.analyze_text(h) for h in headlines]
        
        avg_polarity = sum(s['polarity'] for s in sentiments) / len(sentiments)
        avg_subjectivity = sum(s['subjectivity'] for s in sentiments) / len(sentiments)
        
        # Count sentiment distribution
        positive_count = sum(1 for s in sentiments if s['sentiment'] == 'positive')
        negative_count = sum(1 for s in sentiments if s['sentiment'] == 'negative')
        neutral_count = sum(1 for s in sentiments if s['sentiment'] == 'neutral')
        
        # Overall sentiment based on majority
        if positive_count > negative_count and positive_count > neutral_count:
            overall = 'positive'
        elif negative_count > positive_count and negative_count > neutral_count:
            overall = 'negative'
        else:
            overall = 'neutral'
        
        return {
            'avg_polarity': round(avg_polarity, 3),
            'avg_subjectivity': round(avg_subjectivity, 3),
            'sentiment': overall,
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'total_count': len(headlines),
            'sentiment_strength': round(abs(avg_polarity), 3)
        }
    
    def get_symbol_sentiment(self, symbol: str, headlines: List[str]) -> Dict:
        """
        Get sentiment for a specific symbol from news headlines.
        Caches results for performance.
        """
        cache_key = f"{symbol}_{datetime.now().strftime('%Y%m%d_%H')}"
        
        if cache_key in self.sentiment_cache:
            return self.sentiment_cache[cache_key]
        
        # Filter headlines mentioning the symbol
        relevant_headlines = [h for h in headlines if symbol.upper() in h.upper()]
        
        if not relevant_headlines:
            # Use general market sentiment if no symbol-specific news
            result = self.analyze_headlines(headlines)
        else:
            result = self.analyze_headlines(relevant_headlines)
        
        result['symbol'] = symbol
        result['timestamp'] = datetime.now().isoformat()
        
        # Cache result
        self.sentiment_cache[cache_key] = result
        
        return result
    
    def get_trading_signal(self, sentiment_data: Dict) -> str:
        """
        Convert sentiment to trading signal.
        Returns: 'bullish', 'bearish', or 'neutral'
        """
        polarity = sentiment_data.get('avg_polarity', 0)
        strength = sentiment_data.get('sentiment_strength', 0)
        
        # Require strong sentiment for signal
        if polarity > 0.2 and strength > 0.2:
            return 'bullish'
        elif polarity < -0.2 and strength > 0.2:
            return 'bearish'
        else:
            return 'neutral'
