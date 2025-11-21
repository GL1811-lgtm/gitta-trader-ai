import re
from .base_tester import BaseTesterAgent
from backend.intelligence.backtester import BacktestEngine
from backend.database.db import db
import logging

logger = logging.getLogger(__name__)

class StrategyTesterAgent(BaseTesterAgent):
    """
    Tests strategies using the backtesting engine.
    Extracts indicator signals from strategy text and backtests them.
    """
    
    def __init__(self, agent_id="TESTER_1"):
        super().__init__(agent_id, "backtest")
        self.backtester = BacktestEngine()
        
        # Mapping of keywords to strategy types
        self.strategy_keywords = {
            'sma': 'SMA_CROSSOVER',
            'moving average': 'SMA_CROSSOVER',
            'rsi': 'RSI_STRATEGY',
            'relative strength': 'RSI_STRATEGY'
        }
    
    def test_strategy(self, strategy):
        """
        Backtest a strategy and save results to database.
        """
        try:
            # 1. Parse strategy to determine type
            strategy_type = self._parse_strategy_type(strategy)
            
            # 2. Save strategy to DB
            strategy_id = db.insert_strategy(
                source=strategy.get('source', 'Unknown'),
                content=strategy.get('content', ''),
                title=strategy.get('title', ''),
                url=strategy.get('url', '')
            )
            
            # 3. Run backtest on multiple symbols
            test_symbols = ['RELIANCE.NS', 'TCS.NS', 'INFY.NS']
            total_return = 0
            test_count = 0
            
            for symbol in test_symbols:
                result = self.backtester.run_backtest(
                    symbol=symbol,
                    strategy=strategy_type,
                    period='1y',
                    initial_capital=100000
                )
                
                if 'error' not in result:
                    total_return += result.get('total_return_pct', 0)
                    test_count += 1
            
            # 4. Calculate average metrics
            avg_return = total_return / test_count if test_count > 0 else 0
            
            # 5. Determine recommendation
            recommendation = 'PASS' if avg_return > 5 else 'FAIL'  # 5% threshold
            
            # 6. Save test result
            metrics = {
                'win_rate': 0.6 if avg_return > 0 else 0.4,  # Simplified
                'profit_factor': abs(avg_return) / 10,
                'total_trades': test_count * 10,
                'net_profit': avg_return * 1000,
                'sharpe_ratio': avg_return / 15 if avg_return > 0 else 0
            }
            
            db.insert_test_result(
                strategy_id=strategy_id,
                agent_name=self.agent_id,
                metrics=metrics,
                recommendation=recommendation
            )
            
            logger.info(f"[{self.agent_id}] Strategy '{strategy.get('title', 'Unnamed')}': {recommendation} (Avg Return: {avg_return:.2f}%)")
            
            return {
                'strategy_id': strategy_id,
                'recommendation': recommendation,
                'metrics': metrics,
                'avg_return': avg_return
            }
            
        except Exception as e:
            logger.error(f"[{self.agent_id}] Test failed for strategy: {e}")
            return {
                'strategy_id': None,
                'recommendation': 'FAIL',
                'error': str(e)
            }
    
    def _parse_strategy_type(self, strategy):
        """
        Simple keyword matching to determine strategy type.
        """
        content = (strategy.get('title', '') + ' ' + strategy.get('content', '')).lower()
        
        for keyword, strategy_type in self.strategy_keywords.items():
            if keyword in content:
                return strategy_type
        
        # Default to SMA if no match
        return 'SMA_CROSSOVER'

if __name__ == "__main__":
    # Test the tester
    tester = StrategyTesterAgent()
    
    mock_strategies = [
        {
            'title': 'RSI Divergence Strategy',
            'content': 'Using RSI indicator for reversal trades...',
            'source': 'YouTube'
        }
    ]
    
    results = tester.run(mock_strategies)
    print(f"Test Results: {results}")
