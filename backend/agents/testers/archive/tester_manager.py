import asyncio
import logging
from backend.agents.testers.tester_1 import TesterAgent1
from backend.agents.testers.tester_2 import TesterAgent2
from backend.agents.testers.tester_3 import TesterAgent3
from backend.agents.testers.tester_4 import TesterAgent4
from backend.agents.testers.tester_5 import TesterAgent5
from backend.agents.testers.tester_6 import TesterAgent6
from backend.agents.testers.tester_7 import TesterAgent7
from backend.agents.testers.tester_8 import TesterAgent8
from backend.agents.testers.tester_9 import TesterAgent9
from backend.agents.testers.tester_10 import TesterAgent10

logger = logging.getLogger(__name__)

class TesterManager:
    def __init__(self):
        self.testers = [
            TesterAgent1(),
            TesterAgent2(),
            TesterAgent3(),
            TesterAgent4(),
            TesterAgent5(),
            TesterAgent6(),
            TesterAgent7(),
            TesterAgent8(),
            TesterAgent9(),
            TesterAgent10()
        ]
        logger.info(f"TesterManager initialized with {len(self.testers)} agents.")

    async def run_all_testers(self, strategies):
        """
        Runs all tester agents in parallel against the provided strategies.
        """
        logger.info("Starting Phase 2: Strategy Testing...")
        
        tasks = []
        for tester in self.testers:
            # For simplicity, each tester tests ALL strategies.
            # In a real system, we might distribute them.
            for strategy in strategies:
                tasks.append(tester.test_strategy(strategy))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        summary = {
            "total_tests": len(tasks),
            "successful": 0,
            "failed": 0,
            "details": []
        }
        
        for i, res in enumerate(results):
            if isinstance(res, Exception):
                summary["failed"] += 1
                summary["details"].append({"status": "failed", "error": str(res)})
            else:
                summary["successful"] += 1
                summary["details"].append({"status": "success", "result": res})
                
        logger.info(f"Testing complete. Success: {summary['successful']}, Failed: {summary['failed']}")
        return summary
