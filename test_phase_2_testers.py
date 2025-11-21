import asyncio
import logging
import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from backend.agents.testers.tester_manager import TesterManager

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def main():
    logger.info("==================================================")
    logger.info("PHASE 2 VERIFICATION: 10 TESTER AGENTS")
    logger.info("==================================================")

    try:
        # 1. Initialize Manager
        logger.info("Initializing TesterManager...")
        manager = TesterManager()
        
        # 2. Create Mock Strategies
        mock_strategies = [
            {
                "id": "strat_001",
                "name": "NIFTY 50 SMA Crossover",
                "symbol": "^NSEI",
                "content": "Buy when SMA 50 crosses above SMA 200",
                "type": "Technical"
            },
            {
                "id": "strat_002",
                "name": "SBIN RSI Scalp",
                "symbol": "SBIN.NS",
                "content": "RSI < 30 Buy, RSI > 70 Sell",
                "type": "Scalping"
            },
            {
                "id": "strat_003",
                "name": "Bitcoin Volatility Breakout",
                "symbol": "BTC-USD",
                "content": "Buy on high volatility breakout",
                "type": "Crypto"
            }
        ]
        
        logger.info(f"Created {len(mock_strategies)} mock strategies for testing.")
        
        # 3. Run All Testers
        logger.info("Running all 10 Tester Agents...")
        results = await manager.run_all_testers(mock_strategies)
        
        # 4. Analyze Results
        logger.info("==================================================")
        logger.info("TEST RESULTS SUMMARY")
        logger.info("==================================================")
        logger.info(f"Total Tests: {results['total_tests']}")
        logger.info(f"Successful: {results['successful']}")
        logger.info(f"Failed: {results['failed']}")
        
        logger.info("\n--- Detailed Results (Sample) ---")
        for i, res in enumerate(results['details'][:5]): # Show first 5
            logger.info(f"Result {i+1}: {res}")
            
        if results['failed'] == 0:
            logger.info("\n✅ SUCCESS: All Tester Agents ran successfully!")
        else:
            logger.error("\n❌ FAILURE: Some agents failed.")
            
    except Exception as e:
        logger.error(f"Verification failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Use Windows-compatible event loop policy if needed
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    asyncio.run(main())
