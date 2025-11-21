from backend.evolution.population import Population

def verify_evolution():
    print("--- Verifying Evolution System ---")
    
    try:
        # Initialize small population
        print("\nInitializing Population (Size=10)...")
        pop = Population(size=10)
        
        # Run 3 generations
        print("\nRunning 3 Generations...")
        for i in range(3):
            pop.evolve()
            
        # Check results
        best = pop.get_best_organism()
        print(f"\nEvolution Complete.")
        print(f"Best Fitness: {best.fitness}")
        print(f"Best DNA: {best.dna}")
        
        if best.fitness > 0:
            print("\nPASS: Evolution cycle completed successfully.")
        else:
            print("\nFAIL: Fitness calculation failed.")
            
    except Exception as e:
        print(f"\nFAIL: Error during evolution: {e}")

if __name__ == "__main__":
    verify_evolution()
