import sys
import os
import asyncio
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.agents.collectors.collector_manager import CollectorManager
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

async def test_collectors():
    print("Starting Phase 1 Verification: 10 Collector Agents")
    
    # Load env
    load_dotenv()
    
    manager = CollectorManager()
    
    print(f"Initialized {len(manager.collectors)} Agents")
    
    # Run all collectors
    print("Running all agents in parallel...")
    summary = await manager.run_all_collectors()
    
    # Write results to file
    with open("collector_results.log", "w", encoding="utf-8") as f:
        f.write("Collection Summary:\n")
        f.write(f"Total Agents: {summary['total_agents']}\n")
        f.write(f"Successful: {summary['successful']}\n")
        f.write(f"Failed: {summary['failed']}\n")
        f.write(f"Total Strategies Collected: {summary['total_strategies']}\n")
        f.write(f"Verified Strategies: {summary['verified_strategies']}\n\n")
        
        f.write("Agent Details:\n")
        for detail in summary['details']:
            status_icon = "[OK]" if detail['status'] == 'success' else "[FAIL]"
            f.write(f"{status_icon} {detail['agent_id']}: {detail.get('collected', 0)} collected, {detail.get('verified', 0)} verified\n")
            if detail['status'] == 'failed':
                f.write(f"   Error: {detail.get('error')}\n")
    
    print("Results written to collector_results.log")

if __name__ == "__main__":
    asyncio.run(test_collectors())
