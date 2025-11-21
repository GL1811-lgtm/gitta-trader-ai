import os
import praw
from .base_collector import BaseCollectorAgent
import logging

logger = logging.getLogger(__name__)

class RedditCollector(BaseCollectorAgent):
    """
    Collects trading strategies from Reddit.
    Monitors r/IndiaInvestments, r/stocks, r/algotrading.
    """
    
    def __init__(self, agent_id="REDDIT_COLLECTOR_1"):
        super().__init__(agent_id, "Reddit")
        
        # Reddit API credentials
        self.client_id = os.environ.get('REDDIT_CLIENT_ID', None)
        self.client_secret = os.environ.get('REDDIT_CLIENT_SECRET', None)
        self.user_agent = "Gitta-Trader-AI v1.0"
        
        # Subreddits to monitor
        self.subreddits = ['IndiaInvestments', 'stocks', 'algotrading']
        
        # Search keywords
        self.keywords = ['strategy', 'indicator', 'trading system', 'setup']
    
    def collect(self):
        """Search Reddit and return strategy posts."""
        if not self.client_id or not self.client_secret:
            logger.warning(f"[{self.agent_id}] No Reddit credentials. Returning mock data.")
            return self._get_mock_strategies()
        
        strategies = []
        
        try:
            reddit = praw.Reddit(
                client_id=self.client_id,
                client_secret=self.client_secret,
                user_agent=self.user_agent
            )
            
            for subreddit_name in self.subreddits:
                subreddit = reddit.subreddit(subreddit_name)
                
                # Search for strategy-related posts
                for keyword in self.keywords:
                    for submission in subreddit.search(keyword, limit=5, time_filter='week'):
                        strategy = {
                            'title': submission.title,
                            'content': submission.selftext[:500],  # First 500 chars
                            'url': f"https://reddit.com{submission.permalink}",
                            'source': f'Reddit (r/{subreddit_name})',
                            'score': submission.score
                        }
                        strategies.append(strategy)
            
            return strategies
            
        except Exception as e:
            logger.error(f"[{self.agent_id}] Reddit API error: {e}")
            return self._get_mock_strategies()
    
    def _get_mock_strategies(self):
        """Return mock strategies for testing."""
        return [
            {
                'title': 'My 3-year successful swing trading strategy in Indian markets',
                'content': 'Using weekly timeframe with RSI and volume confirmation...',
                'url': 'https://reddit.com/mock1',
                'source': 'Reddit (r/IndiaInvestments)',
                'score': 125
            },
            {
                'title': 'Backtested: Simple moving average crossover on Nifty',
                'content': 'Results of 5-year backtest on SMA 50/200 crossover strategy...',
                'url': 'https://reddit.com/mock2',
                'source': 'Reddit (r/algotrading)',
                'score': 89
            }
        ]

if __name__ == "__main__":
    # Test collector
    collector = RedditCollector()
    strategies = collector.run()
    print(f"Collected {len(strategies)} strategies")
    for s in strategies:
        print(f"- {s['title']} (Score: {s.get('score', 'N/A')})")
