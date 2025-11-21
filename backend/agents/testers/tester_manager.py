"""
Tester Manager - Coordinates all 5 advanced tester agents
Runs parallel tests on organisms and aggregates results
"""
import logging
from typing import List, Dict, Any
import asyncio
from concurrent.futures import ThreadPoolExecutor

from backend.evolution.organism import TradingOrganism
from backend.agents.testers.scalper import ScalperStrategy
from backend.agents.testers.swing_trader import SwingTraderStrategy
from backend.agents.testers.mean_reversion import MeanReversionStrategy
from backend.agents.testers.adaptive_meta import AdaptiveMetaStrategy

logger = logging.getLogger(__name__)

class TesterManager:
    """
    Manages all 5 tester agents and coordinates parallel testing
    """
    
    def __init__(self):
        self.testers = {
            "scalper": ScalperStrategy,
            "swing_trader": SwingTraderStrategy,
            "mean_reversion": MeanReversionStrategy,
            "adaptive_meta": AdaptiveMetaStrategy
        }
        
    def test_organism(self, organism: TradingOrganism) -> Dict[str, Any]:
        """
        Test a single organism with all tester agents
        
        Args:
            organism: TradingOrganism to test
            
        Returns:
            Aggregated test results from all testers
        """
        logger.info(f"Testing organism {organism.id} with all testers...")
        
        results = {}
        fitness_scores = []
        
        for tester_name, TesterClass in self.testers.items():
            try:
                tester = TesterClass(organism=organism)
                result = tester.test_strategy()
                
                results[tester_name] = result
                
                if result.get("status") == "success":
                    fitness_scores.append(result.get("fitness", 0))
                    
            except Exception as e:
                logger.error(f"Error testing with {tester_name}: {e}")
                results[tester_name] = {
                    "status": "error",
                    "error": str(e)
                }
                
        # Calculate aggregate fitness (average of all successful testers)
        avg_fitness = sum(fitness_scores) / len(fitness_scores) if fitness_scores else 0
        
        return {
            "organism_id": organism.id,
            "tester_results": results,
            "avg_fitness": avg_fitness,
            "successful_tests": len(fitness_scores),
            "total_tests": len(self.testers)
        }
        
    def test_population(self, organisms: List[TradingOrganism], max_workers: int = 3) -> List[Dict[str, Any]]:
        """
        Test multiple organisms in parallel
        
        Args:
            organisms: List of organisms to test
            max_workers: Max parallel tests
            
        Returns:
            List of aggregated results
        """
        logger.info(f"Testing {len(organisms)} organisms in parallel...")
        
        results = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.test_organism, org) for org in organisms]
            
            for future in futures:
                try:
                    result = future.result(timeout=300)  # 5 min timeout per organism
                    results.append(result)
                except Exception as e:
                    logger.error(f"Error in parallel testing: {e}")
                    
        logger.info(f"Completed testing {len(results)}/{len(organisms)} organisms")
        return results
        
    def get_best_tester_for_organism(self, organism: TradingOrganism) -> str:
        """
        Determine which tester performs best for a given organism
        
        Args:
            organism: TradingOrganism to evaluate
            
        Returns:
            Name of best-performing tester
        """
        test_results = self.test_organism(organism)
        
        best_tester = None
        best_fitness = 0
        
        for tester_name, result in test_results["tester_results"].items():
            if result.get("status") == "success":
                fitness = result.get("fitness", 0)
                if fitness > best_fitness:
                    best_fitness = fitness
                    best_tester = tester_name
                    
        return best_tester or "unknown"


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Test with a sample organism
    from backend.evolution.organism import TradingOrganism
    
    organism = TradingOrganism.create_random(generation=1, organism_id="test_manager")
    
    manager = TesterManager()
    results = manager.test_organism(organism)
    
    print(f"\nTester Manager Results:")
    print(f"Organism ID: {results['organism_id']}")
    print(f"Average Fitness: {results['avg_fitness']:.4f}")
    print(f"Successful Tests: {results['successful_tests']}/{results['total_tests']}")
    
    for tester_name, result in results["tester_results"].items():
        status = result.get("status")
        fitness = result.get("fitness", 0)
        print(f"  {tester_name}: {status} (fitness: {fitness:.4f})")
