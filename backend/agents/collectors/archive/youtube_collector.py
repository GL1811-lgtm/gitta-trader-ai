import os
import re
from .base_collector import BaseCollectorAgent
from googleapiclient.discovery import build
import logging

logger = logging.getLogger(__name__)

class YouTubeCollector(BaseCollectorAgent):
    """
    Collects trading strategies from YouTube.
    Searches for Indian stock market trading videos.
    """
    
    def __init__(self, agent_id="YT_COLLECTOR_1"):
        super().__init__(agent_id, "YouTube")
        # YouTube API key from environment
        self.api_key = os.environ.get('YOUTUBE_API_KEY', None)
        
        # Search queries for Indian stock market
        self.queries = [
            "intraday trading strategy india",
            "nifty 50 trading strategy",
            "stock market technical analysis india",
            "price action trading nse",
            "swing trading strategy india"
        ]
    
    def collect(self):
        """Search YouTube and return strategy data."""
        if not self.api_key:
            logger.warning(f"[{self.agent_id}] No YouTube API key found. Returning mock data.")
            return self._get_mock_strategies()
        
        strategies = []
        
        try:
            youtube = build('youtube', 'v3', developerKey=self.api_key)
            
            for query in self.queries:
                # Search for videos
                request = youtube.search().list(
                    part="snippet",
                    q=query,
                    type="video",
                    maxResults=5,
                    relevanceLanguage="en",
                    regionCode="IN"
                )
                response = request.execute()
                
                for item in response.get('items', []):
                    snippet = item['snippet']
                    video_id = item['id']['videoId']
                    
                    strategy = {
                        'title': snippet['title'],
                        'content': snippet['description'],
                        'url': f"https://www.youtube.com/watch?v={video_id}",
                        'source': 'YouTube',
                        'thumbnail': snippet['thumbnails']['default']['url']
                    }
                    strategies.append(strategy)
            
            return strategies
            
        except Exception as e:
            logger.error(f"[{self.agent_id}] YouTube API error: {e}")
            return self._get_mock_strategies()
    
    def _get_mock_strategies(self):
        """Return mock strategies for testing when API is unavailable."""
        return [
            {
                'title': 'RSI Divergence Strategy for Nifty 50',
                'content': 'Using RSI divergence with price action to identify reversals in Nifty index...',
                'url': 'https://youtube.com/mock1',
                'source': 'YouTube'
            },
            {
                'title': 'MACD Crossover System for Intraday',
                'content': 'Simple MACD crossover with 200 EMA filter for high-probability trades...',
                'url': 'https://youtube.com/mock2',
                'source': 'YouTube'
            }
        ]

if __name__ == "__main__":
    # Test collector
    collector = YouTubeCollector()
    strategies = collector.run()
    print(f"Collected {len(strategies)} strategies")
    for s in strategies:
        print(f"- {s['title']}")
