"""
Continuous 24/7 Agent Runner

This script starts all agents in continuous operation mode.
Collectors run every 15 minutes, testers process new strategies continuously.
"""
import asyncio
import sys
import logging
from backend.agents.supervisor.supervisor_agent import SupervisorAgent
from backend.config.continuous_config import get_config_summary, CONTINUOUS_MODE

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/continuous_agents.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)


async def main():
    """Main entry point for continuous operation"""
    
    if not CONTINUOUS_MODE:
        logger.warning("Continuous mode is DISABLED in configuration!")
        logger.warning("Set CONTINUOUS_MODE=true in .env to enable")
        return
    
    # Log configuration
    config = get_config_summary()
    logger.info("=" * 60)
    logger.info("🚀 GITTA TRADER AI - CONTINUOUS 24/7 OPERATION")
    logger.info("=" * 60)
    logger.info(f"Configuration:")
    for key, value in config.items():
        logger.info(f"  {key}: {value}")
    logger.info("=" * 60)
    
    try:
        # Create supervisor
        supervisor = SupervisorAgent()
        
        # Start continuous mode
        logger.info("Starting continuous operation...")
        logger.info("Press Ctrl+C to stop")
        
        await supervisor.run_continuous_mode()
        
    except KeyboardInterrupt:
        logger.info("\n" + "=" * 60)
        logger.info("🛑 Shutdown signal received")
        logger.info("Stopping all agents gracefully...")
        logger.info("=" * 60)
        sys.exit(0)
        
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    import os
    os.makedirs('logs', exist_ok=True)
    
    # Run continuous mode
    asyncio.run(main())
