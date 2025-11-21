"""
Full System Integration Test
Tests end-to-end flow: Evolution → Testers → Expert Agent → Reports
"""
import sys
import os
import logging

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.evolution.population import Population
from backend.agents.testers.tester_manager import TesterManager
from backend.agents.expert.expert_agent import ExpertAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def integration_test():
    logger.info("=" * 60)
    logger.info("FULL SYSTEM INTEGRATION TEST")
    logger.info("=" * 60)
    
    # ===== PHASE 3: EVOLUTION SYSTEM =====
    logger.info("\n🧬 PHASE 3: Evolution System")
    logger.info("-" * 60)
    
    pop = Population(population_size=20)  # Small population for testing
    pop.create_initial_population()
    logger.info(f"✅ Created population: {len(pop.organisms)} organisms")
    
    # Run 3 generations
    for gen in range(3):
        result = pop.evolve()
        logger.info(f"✅ Generation {result['generation']} complete | Best: {result['best_fitness']:.4f} | Avg: {result['avg_fitness']:.4f}")
    
    best_organism = pop.get_best_organism()
    logger.info(f"\n🏆 Best Organism: {best_organism.id}")
    logger.info(f"   Fitness: {best_organism.fitness:.4f}")
    logger.info(f"   Generation: {best_organism.generation}")
    
    # ===== PHASE 5: TESTER AGENTS =====
    logger.info("\n🧪 PHASE 5: Advanced Tester Agents")
    logger.info("-" * 60)
    
    manager = TesterManager()
    tester_results = manager.test_organism(best_organism)
    
    logger.info(f"✅ Tested with {tester_results['total_tests']} testers")
    logger.info(f"   Success rate: {tester_results['successful_tests']}/{tester_results['total_tests']}")
    logger.info(f"   Average fitness: {tester_results['avg_fitness']:.4f}")
    
    for tester_name, result in tester_results["tester_results"].items():
        if result.get("status") == "success":
            logger.info(f"   ✅ {tester_name}: {result.get('fitness', 0):.4f}")
        else:
            logger.info(f"   ⚠️  {tester_name}: {result.get('error', 'Failed')}")
    
    # ===== PHASE 4: EXPERT AGENT =====
    logger.info("\n📊 PHASE 4: Expert Agent Report")
    logger.info("-" * 60)
    
    expert = ExpertAgent()
    report_result = expert.run()
    
    if report_result["status"] == "success":
        logger.info(f"✅ Report generated: {report_result['report_length']} chars")
        logger.info(f"   Date: {report_result['date']}")
    else:
        logger.error(f"❌ Report failed: {report_result.get('message')}")
    
    # ===== VERIFICATION =====
    logger.info("\n" + "=" * 60)
    logger.info("INTEGRATION TEST RESULTS")
    logger.info("=" * 60)
    
    checks = []
    
    # Check 1: Evolution ran
    checks.append(("Evolution System", pop.generation > 1))
    
    # Check 2: Best organism found
    checks.append(("Best Organism", best_organism.fitness > 0))
    
    # Check 3: Testers ran
    checks.append(("Tester Execution", tester_results['successful_tests'] >= 3))
    
    # Check 4: Expert report
    checks.append(("Expert Report", report_result["status"] == "success"))
    
    # Check 5: DB persistence
    from backend.database.db import DatabaseManager
    db = DatabaseManager()
    with db._get_connection() as conn:
        cursor = conn.cursor()
        
        # Check evolution_history
        cursor.execute("SELECT COUNT(*) as count FROM evolution_history WHERE date(timestamp) = date('now')")
        evo_records = cursor.fetchone()['count']
        
        # Check test_results
        cursor.execute("SELECT COUNT(*) as count FROM test_results WHERE date(timestamp) = date('now')")
        test_records = cursor.fetchone()['count']
        
        # Check daily_reports
        cursor.execute("SELECT COUNT(*) as count FROM daily_reports WHERE date(report_date) = date('now')")
        report_records = cursor.fetchone()['count']
    
    checks.append(("Evolution DB Records", evo_records >= 3))
    checks.append(("Tester DB Records", test_records > 0))
    checks.append(("Report DB Records", report_records > 0))
    
    # Display results
    passed = 0
    for check_name, result in checks:
        if result:
            logger.info(f"✅ {check_name}")
            passed += 1
        else:
            logger.error(f"❌ {check_name}")
    
    logger.info("\n" + "=" * 60)
    if passed == len(checks):
        logger.info(f"🎉 INTEGRATION TEST PASSED: {passed}/{len(checks)}")
        logger.info("✅ All systems operational and integrated correctly!")
    else:
        logger.warning(f"⚠️  INTEGRATION TEST PARTIAL: {passed}/{len(checks)}")
    logger.info("=" * 60)
    
    return passed == len(checks)

if __name__ == "__main__":
    success = integration_test()
    sys.exit(0 if success else 1)
