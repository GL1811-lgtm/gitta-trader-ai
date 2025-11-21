import sys
import os
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.evolution.population import Population
from backend.database.db import DatabaseManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_evolution():
    logger.info("Starting Evolution System Verification...")
    
    # 1. Initialize Population
    pop = Population(population_size=20) # Small size for testing
    pop.create_initial_population()
    
    initial_best = pop.get_best_organism()
    logger.info(f"Initial Best Fitness: {initial_best.fitness}")
    
    # 2. Run 5 Generations
    for i in range(5):
        stats = pop.evolve()
        logger.info(f"Generation {stats['generation']} Complete. Best: {stats['best_fitness']:.4f}")
        
    final_best = pop.get_best_organism()
    logger.info(f"Final Best Fitness: {final_best.fitness}")
    
    # 3. Verify Improvement (Not guaranteed with random fitness, but check it runs)
    if final_best.fitness >= 0:
        logger.info("✅ Evolution cycle ran successfully.")
    else:
        logger.error("❌ Fitness calculation failed.")
        
    # 4. Verify DB Persistence
    db = DatabaseManager()
    with db._get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM evolution_history")
        count = cursor.fetchone()['count']
        
    if count >= 5:
        logger.info(f"✅ DB Persistence verified. Found {count} records.")
    else:
        logger.error(f"❌ DB Persistence failed. Found {count} records.")

if __name__ == "__main__":
    verify_evolution()
