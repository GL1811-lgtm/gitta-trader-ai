from abc import ABC, abstractmethod
import logging
import json
import asyncio
import random
from datetime import datetime
from backend.database.db import db

logger = logging.getLogger(__name__)

class BaseTesterAgent(ABC):
    """
    Base class for all Tester Agents.
    Each tester simulates trading based on collected strategies using different risk profiles.
    """
    
    def __init__(self, agent_id, name, risk_profile="neutral"):
        self.agent_id = agent_id
        self.name = name
        self.risk_profile = risk_profile
        self.status = "initialized"
        self.last_run = None
        
    def update_status(self, status, activity):
        """Update agent status in the shared status file."""
        self.status = status
        try:
            status_file = 'backend/data/status.json'
            try:
                with open(status_file, 'r') as f:
                    statuses = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                statuses = []
            
            # Update or append this agent's status
            updated = False
            for s in statuses:
                if s['id'] == self.agent_id:
                    s['status'] = status
                    s['activity'] = activity
                    s['last_updated'] = datetime.now().isoformat()
                    updated = True
                    break
            
            if not updated:
                statuses.append({
                    "id": self.agent_id,
                    "name": self.name,
                    "type": "Tester",
                    "status": status,
                    "activity": activity,
                    "last_updated": datetime.now().isoformat()
                })
                
            with open(status_file, 'w') as f:
                json.dump(statuses, f, indent=2)
                
        except Exception as e:
            logger.error(f"[{self.agent_id}] Failed to update status: {e}")

    async def run_continuously(self, interval_seconds=10):
        """Run the tester in a continuous loop."""
        logger.info(f"[{self.name}] Starting continuous testing loop...")
        
        while True:
            try:
                self.update_status("Running", "Fetching untested strategies")
                
                # 1. Fetch untested strategies
                strategies = db.get_untested_strategies(limit=1)
                
                if strategies:
                    for strategy in strategies:
                        self.update_status("Testing", f"Testing Strategy #{strategy['id']}")
                        logger.info(f"[{self.name}] Testing strategy: {strategy['title']}")
                        
                        # 2. Run simulation
                        result = await self.test_strategy(strategy)
                        
                        # 3. Save result
                        self.save_result(strategy['id'], result)
                        
                        # 4. Mark strategy as tested (optional, or just log it)
                        # db.mark_strategy_tested(strategy['id']) 
                        # Note: We might want multiple testers to test the same strategy, 
                        # so maybe we don't mark it as 'tested' globally, or we have a 'tested_by' table.
                        # For now, let's assume we just save the result.
                        
                else:
                    self.update_status("Idle", "No new strategies to test")
                
                # Sleep
                self.update_status("Idle", f"Waiting {interval_seconds}s")
                await asyncio.sleep(interval_seconds)
                
            except Exception as e:
                logger.error(f"[{self.name}] Error in continuous loop: {e}")
                self.update_status("Error", str(e))
                await asyncio.sleep(interval_seconds)

    @abstractmethod
    async def test_strategy(self, strategy):
        """
        Simulate trading for the given strategy.
        Must return a dictionary with:
        - win_rate
        - profit_factor
        - total_trades
        - net_profit
        - sharpe_ratio
        - recommendation ('PASS' or 'FAIL')
        """
        pass

    def save_result(self, strategy_id, result):
        """Save the test result to the database."""
        try:
            db.save_test_result(
                strategy_id=strategy_id,
                agent_name=self.name,
                win_rate=result.get('win_rate', 0),
                profit_factor=result.get('profit_factor', 0),
                total_trades=result.get('total_trades', 0),
                net_profit=result.get('net_profit', 0),
                sharpe_ratio=result.get('sharpe_ratio', 0),
                recommendation=result.get('recommendation', 'FAIL')
            )
            logger.info(f"[{self.name}] Saved result for strategy #{strategy_id}")
        except Exception as e:
            logger.error(f"[{self.name}] Failed to save result: {e}")
