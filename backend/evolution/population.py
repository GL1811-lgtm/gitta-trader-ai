import logging
from typing import List, Dict, Any
import random
import uuid
from backend.evolution.organism import TradingOrganism
from backend.evolution.fitness import FitnessCalculator
from backend.database.db import DatabaseManager

logger = logging.getLogger(__name__)

from backend.intelligence.backtester import BacktestEngine

class Population:
    """
    Manages a population of TradingOrganisms and handles the evolution process.
    """
    
    def __init__(self, population_size: int = 100):
        self.population_size = population_size
        self.organisms: List[TradingOrganism] = []
        self.generation = 0
        self.fitness_calculator = FitnessCalculator()
        self.db = DatabaseManager()
        self.backtester = BacktestEngine()
        
    def create_initial_population(self):
        """Generate the first generation of random organisms."""
        logger.info(f"Creating initial population of {self.population_size} organisms...")
        self.organisms = []
        for _ in range(self.population_size):
            org_id = str(uuid.uuid4())
            organism = TradingOrganism.create_random(generation=0, organism_id=org_id)
            self.organisms.append(organism)
        self.generation = 1
        logger.info("Initial population created.")

    def evolve(self) -> Dict[str, Any]:
        """
        Run one full evolution cycle:
        1. Evaluate Fitness
        2. Select Survivors
        3. Reproduce
        4. Mutate
        5. Save Stats
        """
        logger.info(f"Starting evolution for Generation {self.generation}...")
        
        # 1. Evaluate Fitness
        self.evaluate_fitness()
        
        # Sort by fitness (descending)
        self.organisms.sort(key=lambda x: x.fitness, reverse=True)
        
        best_fitness = self.organisms[0].fitness
        avg_fitness = sum(o.fitness for o in self.organisms) / len(self.organisms)
        worst_fitness = self.organisms[-1].fitness
        
        logger.info(f"Gen {self.generation} Stats - Best: {best_fitness:.4f}, Avg: {avg_fitness:.4f}")
        
        # Save to DB
        self.db.log_evolution(
            generation=self.generation,
            best_fitness=best_fitness,
            avg_fitness=avg_fitness,
            worst_fitness=worst_fitness,
            population_size=len(self.organisms)
        )
        
        # 2. Selection (Top 50%)
        survivors_count = self.population_size // 2
        survivors = self.organisms[:survivors_count]
        
        # 3. Reproduction
        new_population = []
        
        # Elitism: Keep top 10% unchanged
        elite_count = int(self.population_size * 0.10)
        new_population.extend(survivors[:elite_count])
        
        # Fill the rest with children
        while len(new_population) < self.population_size:
            parent1 = random.choice(survivors)
            parent2 = random.choice(survivors)
            
            if parent1 != parent2:
                child_id = str(uuid.uuid4())
                child = parent1.crossover(parent2, child_id)
                child.mutate(mutation_rate=0.1)
                child.generation = self.generation + 1
                new_population.append(child)
                
        self.organisms = new_population
        self.generation += 1
        
        return {
            "generation": self.generation - 1,
            "best_fitness": best_fitness,
            "avg_fitness": avg_fitness,
            "population_size": len(self.organisms)
        }

    def evaluate_fitness(self):
        """
        Run backtest for each organism and calculate fitness.
        """
        symbol = "^NSEI" # Default symbol for evolution
        period = "1y"
        
        for i, org in enumerate(self.organisms):
            try:
                # Run backtest with organism's DNA
                results = self.backtester.run_backtest(
                    symbol=symbol,
                    strategy="EVOLUTION_DNA",
                    period=period,
                    strategy_params=org.dna
                )
                
                if "error" in results:
                    # If backtest fails (e.g. no data), assign 0 fitness
                    # logger.warning(f"Backtest failed for organism {org.id}: {results['error']}")
                    org.fitness = 0.0
                else:
                    # Calculate fitness from results
                    # Map backtest results to what FitnessCalculator expects
                    metrics = {
                        "sharpe_ratio": results.get("sharpe_ratio", 0),
                        "sortino_ratio": results.get("sortino_ratio", 0),
                        "win_rate": results.get("win_rate", 0),
                        "max_drawdown": results.get("max_drawdown_pct", 100),
                        "total_trades": results.get("total_trades", 0)
                    }
                    org.fitness = self.fitness_calculator.calculate_fitness(metrics)
                    
            except Exception as e:
                logger.error(f"Error evaluating organism {org.id}: {e}")
                org.fitness = 0.0

    def get_best_organism(self) -> TradingOrganism:
        """Return the organism with the highest fitness."""
        if not self.organisms:
            return None
        return max(self.organisms, key=lambda x: x.fitness)
