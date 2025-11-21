import sys
import os
sys.path.append(os.getcwd())

try:
    from backend.evolution.population import Population
    print(f"Imported Population from: {Population}")
    p = Population(population_size=100)
    print("Success: Population instantiated.")
except Exception as e:
    print(f"Error: {e}")
