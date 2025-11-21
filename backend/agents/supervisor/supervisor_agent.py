import asyncio
import logging
import time
import schedule
from datetime import datetime
from backend.agents.collectors.collector_manager import CollectorManager
from backend.agents.testers.tester_manager import TesterManager
from backend.database.db import db

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SupervisorAgent:
    """
    The Supervisor Agent is responsible for:
    1. Orchestrating the workflow (Collectors -> Testers).
    2. Scheduling daily operations (Morning & Evening).
    3. Monitoring system health.
    """
    def __init__(self):
        self.agent_id = "supervisor_1"
        self.collector_manager = CollectorManager()
        self.tester_manager = TesterManager()
        self.is_running = False

    async def run_morning_workflow(self):
        """
        Morning Workflow (8:00 AM):
        - Trigger Expert Agent for morning report.
        - Trigger all Collector Agents to gather fresh strategies.
        """
        logger.info("🌅 Starting Morning Workflow: Data Collection")
        
        try:
            # 1. Generate Morning Report
            try:
                from backend.agents.expert.expert_agent import ExpertAgent
                expert = ExpertAgent()
                await expert.generate_morning_report()
                logger.info("✅ Morning Report Generated.")
            except Exception as e:
                logger.error(f"Failed to generate Morning Report: {e}")
            
            # 2. Run Collectors
            logger.info("Triggering Collector Agents...")
            results = await self.collector_manager.run_all_collectors()
            
            logger.info(f"Morning Collection Complete. Collected: {results['total_collected']}")
            
        except Exception as e:
            logger.error(f"Morning Workflow Failed: {e}")

    async def run_evening_workflow(self):
        """
        Evening Workflow (5:00 PM):
        - Fetch today's collected strategies.
        - Trigger Tester Agents to validate them.
        - Trigger Expert Agent for evening report.
        """
        logger.info("🌆 Starting Evening Workflow: Strategy Testing & Review")
        
        try:
            # 1. Fetch Strategies to Test
            strategies = db.get_all_strategies()
            
            if not strategies:
                logger.warning("No strategies found to test.")
                return

            # 2. Run Testers
            logger.info(f"Triggering Tester Agents for {len(strategies)} strategies...")
            results = await self.tester_manager.run_all_testers(strategies)
            
            logger.info(f"Evening Testing Complete. Success: {results['successful']}, Failed: {results['failed']}")
            
            # 3. Trigger Expert Agent for Evening Report
            try:
                from backend.agents.expert.expert_agent import ExpertAgent
                expert = ExpertAgent()
                await expert.generate_evening_report()
                logger.info("✅ Evening Report Generated.")
            except Exception as e:
                logger.error(f"Failed to generate Evening Report: {e}")
            
        except Exception as e:
            logger.error(f"Evening Workflow Failed: {e}")

    def start_scheduler(self):
        """
        Starts the scheduling loop.
        """
        self.is_running = True
        logger.info("Supervisor Agent Scheduler Started 🕒")
        
        # Schedule Morning Workflow at 08:00
        schedule.every().day.at("08:00").do(lambda: asyncio.create_task(self.run_morning_workflow()))
        
        # Schedule Evening Workflow at 17:00
        schedule.every().day.at("17:00").do(lambda: asyncio.create_task(self.run_evening_workflow()))
        
        # Keep running
        while self.is_running:
            schedule.run_pending()
            time.sleep(1)

    async def run_manual_cycle(self):
        """
        Manually runs a full cycle (Collection -> Testing) for immediate execution/testing.
        """
        logger.info("🔧 Starting Manual Full Cycle")
        await self.run_morning_workflow()
        await self.run_evening_workflow()
        logger.info("✅ Manual Cycle Complete")
    
    async def run_continuous_mode(self):
        """
        Run all agents in continuous 24/7 mode.
        
        Collectors run every 15 minutes, testers process new strategies continuously.
        Daily reports are still generated at scheduled times.
        """
        from backend.config.continuous_config import (
            COLLECTOR_INTERVAL_MINUTES,
            TESTER_INTERVAL_MINUTES
        )
        
        logger.info("🚀 Starting Continuous 24/7 Operation Mode")
        logger.info(f"Collector interval: {COLLECTOR_INTERVAL_MINUTES} minutes")
        logger.info(f"Tester interval: {TESTER_INTERVAL_MINUTES} minutes")
        
        try:
            # Get all collectors
            all_collectors = self.collector_manager.collectors
            
            # Create tasks for all collectors to run continuously
            collector_tasks = []
            for collector in all_collectors.values():
                if hasattr(collector, 'run_continuously'):
                    collector_tasks.append(collector.run_continuously(interval_minutes=COLLECTOR_INTERVAL_MINUTES))

            
            # Create tasks for all testers to run continuously
            tester_tasks = [
                tester.run_continuously(interval_seconds=10)
                for tester in self.tester_manager.testers
            ]
            
            # Create task for scheduled reports
            report_task = self._run_scheduled_reports()
            
            logger.info(f"Started {len(collector_tasks)} collectors and {len(tester_tasks)} testers in continuous mode")
            
            # Run all tasks concurrently
            await asyncio.gather(
                *collector_tasks,
                *tester_tasks,
                report_task
            )
            
        except Exception as e:
            logger.error(f"Continuous mode error: {e}")
    
    async def _run_continuous_testing(self, interval_minutes):
        """Continuously test new strategies"""
        logger.info(f"Starting continuous testing loop (interval: {interval_minutes} min)")
        
        while True:
            try:
                # Get untested strategies
                strategies = db.get_strategies()  # Fixed: use get_strategies() instead
                untested = [s for s in strategies if not s.get('tested', False)]
                
                if untested:
                    logger.info(f"Testing {len(untested)} strategies...")
                    results = await self.tester_manager.run_all_testers(untested)
                    logger.info(f"Testing complete - Success: {results['successful']}, Failed: {results['failed']}")
                
                await asyncio.sleep(interval_minutes * 60)
                
            except Exception as e:
                logger.error(f"Testing loop error: {e}")
                await asyncio.sleep(60)
    
    async def _run_scheduled_reports(self):
        """Generate reports at scheduled times"""
        from datetime import datetime
        import asyncio
        
        logger.info("Starting scheduled report generation")
        
        while True:
            try:
                now = datetime.now()
                current_time = now.strftime("%H:%M")
                
                # Morning report at 08:00
                if current_time == "08:00":
                    try:
                        from backend.agents.expert.expert_agent import ExpertAgent
                        expert = ExpertAgent()
                        await expert.generate_morning_report()
                        logger.info("✅ Morning Report Generated")
                    except Exception as e:
                        logger.error(f"Morning report failed: {e}")
                    
                    # Sleep for 2 minutes to avoid duplicate generation
                    await asyncio.sleep(120)
                
                # Evening report at 17:00
                elif current_time == "17:00":
                    try:
                        from backend.agents.expert.expert_agent import ExpertAgent
                        expert = ExpertAgent()
                        await expert.generate_evening_report()
                        logger.info("✅ Evening Report Generated")
                    except Exception as e:
                        logger.error(f"Evening report failed: {e}")
                    
                    # Sleep for 2 minutes to avoid duplicate generation
                    await asyncio.sleep(120)
                
                # Check every minute
                await asyncio.sleep(60)
                
            except Exception as e:
                logger.error(f"Report generation error: {e}")
                await asyncio.sleep(60)


if __name__ == "__main__":
    # For testing purposes, we can run a manual cycle
    supervisor = SupervisorAgent()
    asyncio.run(supervisor.run_manual_cycle())
