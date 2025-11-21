from flask import Blueprint, jsonify
from backend.evolution.population import Population

evolution_bp = Blueprint('evolution', __name__)

# Global population instance (in memory for now)
# In production, this would be managed by a background worker/scheduler
population = Population(20)

@evolution_bp.route('/status', methods=['GET'])
def get_status():
    """Get current evolution status."""
    best_org = population.get_best_organism()
    return jsonify({
        "generation": population.generation,
        "population_size": len(population.organisms),
        "best_fitness": best_org.fitness,
        "best_dna": best_org.dna
    })

@evolution_bp.route('/organisms', methods=['GET'])
def get_organisms():
    """Get all organisms in current population."""
    return jsonify([org.__dict__ for org in population.organisms])

@evolution_bp.route('/evolve', methods=['POST'])
def trigger_evolution():
    """Manually trigger an evolution cycle (for testing/demo)."""
    population.evolve()
    best_org = population.get_best_organism()
    return jsonify({
        "message": "Evolution cycle completed",
        "new_generation": population.generation,
        "best_fitness": best_org.fitness
    })
