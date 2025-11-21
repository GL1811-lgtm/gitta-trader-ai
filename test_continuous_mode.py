"""
Test Continuous Operation - Quick Verification

This script tests the continuous operation mode by running collectors for 2 cycles.
"""
import asyncio
import logging
from backend.agents.collectors.youtube_collector import YouTubeCollector

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def test_continuous_collector():
    """Test a single collector in continuous mode"""
    logger.info("=" * 60)
    logger.info("Testing Continuous Operation - YouTubeCollector")
    logger.info("Running 2 cycles with 1-minute intervals")
    logger.info("=" * 60)
    
    # Create collector
    collector = YouTubeCollector("test_collector_continuous")
    
    # Run for 2 cycles with 1-minute interval (for testing)
    await collector.run_continuously(interval_minutes=1, max_iterations=2)
    
    logger.info("=" * 60)
    logger.info("✅ Test Complete!")
    logger.info("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_continuous_collector())
