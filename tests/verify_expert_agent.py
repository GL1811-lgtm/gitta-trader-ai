"""
Test script to verify Expert Agent functionality
"""
import sys
import os
import logging

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.agents.expert.expert_agent import ExpertAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_expert_agent():
    logger.info("Starting Expert Agent verification...")
    
    # 1. Initialize Expert Agent
    agent = ExpertAgent()
    logger.info(f"✅ Expert Agent initialized: {agent.name}")
    
    # 2. Test data collection
    logger.info("\nCollecting daily data...")
    data = agent.collect_daily_data()
    logger.info(f"Evolution data: {data.get('evolution', {})}")
    logger.info(f"Tester data: {data.get('testers', {})}")
    logger.info(f"Market data: {data.get('market', {})}")
    
    # 3. Test report generation
    logger.info("\nGenerating report...")
    report = agent.generate_report(data)
    logger.info(f"Report length: {len(report)} characters")
    logger.info(f"First 200 chars:\n{report[:200]}...")
    
    # 4. Test report saving
    logger.info("\nSaving report...")
    success = agent.save_report(report, "EVENING")
    if success:
        logger.info("✅ Report saved successfully")
    else:
        logger.error("❌ Report save failed")
        
    # 5. Run full workflow
    logger.info("\nRunning full Expert Agent workflow...")
    result = agent.run()
    logger.info(f"Final result: {result}")
    
    if result.get('status') == 'success':
        logger.info("✅ Expert Agent verification PASSED")
    else:
        logger.error("❌ Expert Agent verification FAILED")

if __name__ == "__main__":
    test_expert_agent()
