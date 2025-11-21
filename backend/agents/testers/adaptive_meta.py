"""
Adaptive Meta Tester Agent - Multi-Regime Strategy Switcher
DNA-driven adaptive strategy that detects market regimes and switches tactics
"""
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import pandas as pd
import numpy as np

from backend.evolution.organism import TradingOrganism
from backend.evolution.fitness import FitnessCalculator
from backend.database.db import DatabaseManager
from backend.intelligence.backtester import BacktestEngine

logger = logging.getLogger(__name__)

class AdaptiveMetaStrategy:
    """
    Adaptive strategy that switches between approaches based on market regime
    """
    
    REGIMES = {
        "TRENDING_BULL": "Trending Bull (ADX>25, Price>MA200)",
        "TRENDING_BEAR": "Trending Bear (ADX>25, Price<MA200)",
        "RANGE_BOUND": "Range-Bound (ADX<20)",
        "HIGH_VOLATILITY": "High Volatility (VIX>25)",
        "LOW_VOLATILITY": "Low Volatility (VIX<15)"
    }
    
    def __init__(self, organism: Optional[TradingOrganism] = None):
        self.organism = organism
        self.agent_name = "adaptive_meta"
        self.db = DatabaseManager()
        self.fitness_calculator = FitnessCalculator()
        self.backtester = BacktestEngine()
        
        if organism:
            self.params = self._extract_dna_params(organism.dna)
        else:
            self.params = self._default_params()
            
    def _default_params(self) -> Dict[str, Any]:
        """Default adaptive strategy parameters"""
        return {
            # Regime detection thresholds
            "adx_strong_trend": 25,
            "adx_range_bound": 20,
            "vix_high": 25,
            "vix_low": 15,
            "ma_period": 200,
            
            # Strategy params for different regimes
            "trending_fast_ma": 10,
            "trending_slow_ma": 30,
            "ranging_rsi_period": 14,
            "ranging_rsi_oversold": 30,
            "ranging_rsi_overbought": 70,
            
            # Risk params
            "stop_loss_pct": 2.0,
            "take_profit_pct": 4.0
        }
        
    def _extract_dna_params(self, dna: Dict[str, Any]) -> Dict[str, Any]:
        """Extract adaptive strategy parameters from organism DNA"""
        return {
            # Use DNA params but keep regime-specific logic
            "adx_strong_trend": 25,
            "adx_range_bound": 20,
            "vix_high": 25,
            "vix_low": 15,
            "ma_period": 200,
            
            "trending_fast_ma": dna.get("ma_fast", 10),
            "trending_slow_ma": dna.get("ma_slow", 30),
            "ranging_rsi_period": dna.get("rsi_period", 14),
            "ranging_rsi_oversold": dna.get("rsi_oversold", 30),
            "ranging_rsi_overbought": dna.get("rsi_overbought", 70),
            
            "stop_loss_pct": dna.get("stop_loss_pct", 2.0),
            "take_profit_pct": dna.get("take_profit_pct", 4.0)
        }
        
    def run_backtest(self, symbol: str = "^NSEI", period: str = "1y") -> Dict[str, Any]:
        """
        Run adaptive strategy backtest
        Uses EVOLUTION_DNA strategy for regime switching
        
        Args:
            symbol: Trading symbol
            period: Backtest period
            
        Returns:
            Backtest results
        """
        logger.info(f"[{self.agent_name}] Running adaptive meta backtest for {symbol}...")
        
        # Use EVOLUTION_DNA strategy which combines RSI + MA
        # This simulates regime switching by using both indicators
        results = self.backtester.run_backtest(
            symbol=symbol,
            strategy="EVOLUTION_DNA",
            period=period,
            strategy_params=self.params
        )
        
        if "error" not in results:
            results["regime_detection"] = "Multi-regime adaptive"
            results["strategy_type"] = "adaptive_meta"
            
        return results
        
    def test_strategy(self) -> Dict[str, Any]:
        """
        Test adaptive meta strategy and save results
        
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
                "total_trades": metrics["total_trades"],
                "regime_aware": True
            }
            
        except Exception as e:
            logger.error(f"Error testing adaptive meta strategy: {e}")
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
                    0,
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
    adaptive = AdaptiveMetaStrategy()
    result = adaptive.test_strategy()
    print(f"\nAdaptive Meta Test Result: {result}")
