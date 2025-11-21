import asyncio
import logging
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from backend.agents.supervisor.supervisor_agent import SupervisorAgent

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def main():
    logger.info("==================================================")
    logger.info("PHASE 3 VERIFICATION: SUPERVISOR AGENT")
    logger.info("==================================================")

    try:
        # 1. Initialize Supervisor
        logger.info("Initializing SupervisorAgent...")
        supervisor = SupervisorAgent()
        
        # 2. Run Manual Cycle (Triggers Collection -> Testing)
        logger.info("Running Manual Cycle...")
        await supervisor.run_manual_cycle()
        
        logger.info("\n✅ SUCCESS: Supervisor Agent completed the full workflow!")
            
    except Exception as e:
        logger.error(f"Verification failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Use Windows-compatible event loop policy if needed
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(main())
