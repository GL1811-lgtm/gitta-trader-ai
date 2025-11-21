"""
Verification script for Phase 5: Advanced Tester Agents
Tests all upgraded testers with organism DNA
"""
import sys
import os
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.evolution.organism import TradingOrganism
from backend.agents.testers.tester_manager import TesterManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_testers():
    logger.info("==" * 30)
    logger.info("Phase 5: Advanced Tester Agents Verification")
    logger.info("==" * 30)
    
    # 1. Create test organism
    logger.info("\n✅ Creating test organism with random DNA...")
    organism = TradingOrganism.create_random(generation=1, organism_id="test_phase5")
    logger.info(f"Organism ID: {organism.id}")
    logger.info(f"DNA Sample: RSI={organism.dna['rsi_period']}, MA Fast={organism.dna['ma_fast']}, MA Slow={organism.dna['ma_slow']}")
    
    # 2. Initialize Tester Manager
    logger.info("\n✅ Initializing Tester Manager...")
    manager = TesterManager()
    logger.info(f"Loaded {len(manager.testers)} testers")
    
    # 3. Test organism with all testers
    logger.info(f"\n✅ Testing organism with all tester agents...")
    results = manager.test_organism(organism)
    
    # 4. Display results
    logger.info("\n" + "==" * 30)
    logger.info("VERIFICATION RESULTS")
    logger.info("==" * 30)
    logger.info(f"Organism ID: {results['organism_id']}")
    logger.info(f"Average Fitness: {results['avg_fitness']:.4f}")
    logger.info(f"Successful Tests: {results['successful_tests']}/{results['total_tests']}")
    
    logger.info("\nIndividual Tester Results:")
    for tester_name, result in results["tester_results"].items():
        status = result.get("status")
        if status == "success":
            fitness = result.get("fitness", 0)
            trades = result.get("metrics", {}).get("total_trades", 0)
            win_rate = result.get("metrics", {}).get("win_rate", 0)
            logger.info(f"  ✅ {tester_name.upper()}: Fitness={fitness:.4f}, Trades={trades}, WinRate={win_rate:.1f}%")
        else:
            error = result.get("error", "Unknown error")
            logger.info(f"  ❌ {tester_name.upper()}: {error}")
    
    # 5. Verification checks
    logger.info("\n" + "==" * 30)
    logger.info("VERIFICATION CHECKS")
    logger.info("==" * 30)
    
    checks_passed = 0
    total_checks = 4
    
    # Check 1: All testers executed
    if results['total_tests'] == len(manager.testers):
        logger.info("✅ All testers executed")
        checks_passed += 1
    else:
        logger.error(f"❌ Expected {len(manager.testers)} tests, got {results['total_tests']}")
    
    # Check 2: At least 3 successful
    if results['successful_tests'] >= 3:
        logger.info(f"✅ {results['successful_tests']} testers succeeded")
        checks_passed += 1
    else:
        logger.error(f"❌ Only {results['successful_tests']} testers succeeded (need >=3)")
    
    # Check 3: Average fitness calculated
    if results['avg_fitness'] > 0:
        logger.info(f"✅ Average fitness calculated: {results['avg_fitness']:.4f}")
        checks_passed += 1
    else:
        logger.error("❌ Average fitness is 0")
    
    # Check 4: DB persistence (check test_results table)
    from backend.database.db import DatabaseManager
    db = DatabaseManager()
    with db._get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM test_results WHERE date(timestamp) = date('now')")
        row = cursor.fetchone()
        db_records = row['count']
        
    if db_records > 0:
        logger.info(f"✅ DB persistence verified: {db_records} records saved")
        checks_passed += 1
    else:
        logger.error("❌ No records saved to test_results table")
    
    # Final verdict
    logger.info("\n" + "==" * 30)
    if checks_passed == total_checks:
        logger.info(f"🎉 VERIFICATION PASSED: {checks_passed}/{total_checks} checks")
        logger.info("Phase 5: Advanced Tester Agents - COMPLETE")
    else:
        logger.error(f"⚠️  VERIFICATION INCOMPLETE: {checks_passed}/{total_checks} checks passed")
    logger.info("==" * 30)

if __name__ == "__main__":
    verify_testers()
