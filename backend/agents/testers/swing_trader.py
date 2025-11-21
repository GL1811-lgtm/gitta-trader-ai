"""
Swing Trader Tester Agent - Multi-Day Trend Strategy
DNA-driven swing trading with ADX trend detection and moving averages
"""
import logging
from typing import Dict, Any, Optional
from datetime import datetime

from backend.evolution.organism import TradingOrganism
from backend.evolution.fitness import FitnessCalculator
from backend.database.db import DatabaseManager
from backend.intelligence.backtester import BacktestEngine

logger = logging.getLogger(__name__)

class SwingTraderStrategy:
    """
    DNA-driven swing trading strategy for 1-5 day holds
    Uses ADX for trend strength and moving average crossovers
    """
    
    def __init__(self, organism: Optional[TradingOrganism] = None):
        self.organism = organism
        self.agent_name = "swing_trader"
        self.db = DatabaseManager()
        self.fitness_calculator = FitnessCalculator()
        self.backtester = BacktestEngine()
        
        if organism:
            self.params = self._extract_dna_params(organism.dna)
        else:
            self.params = self._default_params()
            
    def _default_params(self) -> Dict[str, Any]:
        """Default swing trading parameters"""
        return {
            "ma_fast": 20,
            "ma_slow": 50,
            "adx_threshold": 25,  # Strong trend
            "profit_target_pct": 4.0,  # 4% target
            "stop_loss_pct": 2.0,  # 2% stop
            "rsi_period": 14,
            "rsi_overbought": 70,
            "rsi_oversold": 30
        }
        
    def _extract_dna_params(self, dna: Dict[str, Any]) -> Dict[str, Any]:
        """Extract swing trading parameters from organism DNA"""
        return {
            "ma_fast": dna.get("ma_fast", 20),
            "ma_slow": dna.get("ma_slow", 50),
            "adx_threshold": 25,
            "profit_target_pct": dna.get("take_profit_pct", 4.0),
            "stop_loss_pct": dna.get("stop_loss_pct", 2.0),
            "rsi_period": dna.get("rsi_period", 14),
            "rsi_overbought": dna.get("rsi_overbought", 70),
            "rsi_oversold": dna.get("rsi_oversold", 30)
        }
        
    def run_backtest(self, symbol: str = "^NSEI", period: str = "1y") -> Dict[str, Any]:
        """
        Run swing trading backtest
        
        Args:
            symbol: Trading symbol
            period: Backtest period (default 1 year)
            
        Returns:
            Backtest results
        """
        logger.info(f"[{self.agent_name}] Running swing trading backtest for {symbol}...")
        
        # Use SMA_CROSSOVER strategy with DNA params
        results = self.backtester.run_backtest(
            symbol=symbol,
            strategy="SMA_CROSSOVER",
            period=period,
            strategy_params=self.params
        )
        
        return results
        
    def test_strategy(self) -> Dict[str, Any]:
        """
        Test swing trading strategy and save results
        
        Returns:
            Test results with fitness score
        """
        try:
            backtest_results = self.run_backtest()
            
            if "error" in backtest_results:
                logger.error(f"Backtest error: {backtest_results['error']}")
                return {
                    "status": "error",
                    "error": backtest_results["error"]
                }
            
            # Calculate fitness
            metrics = {
                "sharpe_ratio": backtest_results.get("sharpe_ratio", 0),
                "sortino_ratio": backtest_results.get("sortino_ratio", 0),
                "win_rate": backtest_results.get("win_rate", 0),
                "max_drawdown": backtest_results.get("max_drawdown_pct", 100),
                "total_trades": backtest_results.get("total_trades", 0)
            }
            
            fitness = self.fitness_calculator.calculate_fitness(metrics)
            
            # Save to database
            self._save_results_to_db(backtest_results, fitness)
            
            return {
                "status": "success",
                "fitness": fitness,
                "metrics": metrics,
                "total_trades": metrics["total_trades"]
            }
            
        except Exception as e:
            logger.error(f"Error testing swing trading strategy: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
            
    def _save_results_to_db(self, backtest_results: Dict[str, Any], fitness: float):
        """Save test results to database"""
        try:
            with self.db._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO test_results 
                    (agent_name, win_rate, profit_factor, total_trades, net_profit, sharpe_ratio, recommendation, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    self.agent_name,
                    backtest_results.get("win_rate", 0),
                    0,  # Profit factor not in current backtest results
                    backtest_results.get("total_trades", 0),
                    backtest_results.get("total_return_pct", 0),
                    backtest_results.get("sharpe_ratio", 0),
                    "PASS" if fitness > 0.5 else "FAIL",
                    datetime.now()
                ))
                conn.commit()
                logger.info(f"[{self.agent_name}] Results saved to database")
        except Exception as e:
            logger.error(f"Error saving to database: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test with default params
    swing_trader = SwingTraderStrategy()
    result = swing_trader.test_strategy()
    print(f"\nSwing Trader Test Result: {result}")
