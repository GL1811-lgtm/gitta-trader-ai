import asyncio
import logging
import sys
import os
import sqlite3
from datetime import datetime
from unittest.mock import MagicMock

# Add project root to path
sys.path.append(os.getcwd())

from backend.agents.expert.expert_agent import ExpertAgent
from backend.database.db import db

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_test_db():
    """Re-creates the daily_reports table with the new schema for testing."""
    logger.info("Setting up test database schema...")
    conn = db._get_connection()
    cursor = conn.cursor()
    
    # Drop old table if exists
    cursor.execute("DROP TABLE IF EXISTS daily_reports")
    
    # Create new table
    cursor.execute("""
    CREATE TABLE daily_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        report_date DATE NOT NULL,
        type TEXT NOT NULL,
        content TEXT NOT NULL,
        summary_stats TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        UNIQUE(report_date, type)
    );
    """)
    conn.commit()
    conn.close()

async def main():
    logger.info("==================================================")
    logger.info("PHASE 4 VERIFICATION: EXPERT AGENT")
    logger.info("==================================================")

    try:
        # 1. Setup DB
        setup_test_db()
        
        # 2. Initialize Expert Agent
        logger.info("Initializing ExpertAgent...")
        expert = ExpertAgent()
        
        # Mock the AI client to avoid API usage/costs during test
        expert.ai_client.generate_report_summary = MagicMock(return_value="# Mock Report\n\nThis is a generated report.")
        
        # 3. Generate Morning Report
        logger.info("Generating Morning Report...")
        morning_report = await expert.generate_morning_report()
        
        if morning_report and morning_report['type'] == 'MORNING':
            logger.info("✅ Morning Report Generated.")
        else:
            logger.error("❌ Failed to generate Morning Report.")
            
        # 4. Generate Evening Report
        logger.info("Generating Evening Report...")
        evening_report = await expert.generate_evening_report()
        
        if evening_report and evening_report['type'] == 'EVENING':
            logger.info("✅ Evening Report Generated.")
        else:
            logger.error("❌ Failed to generate Evening Report.")
            
        # 5. Verify DB Storage
        logger.info("Verifying Database Storage...")
        saved_morning = db.get_latest_report("MORNING")
        saved_evening = db.get_latest_report("EVENING")
        
        if saved_morning and "Mock Report" in saved_morning:
            logger.info("✅ Morning Report found in DB.")
        else:
            logger.error("❌ Morning Report NOT found in DB.")
            
        if saved_evening and "Mock Report" in saved_evening:
            logger.info("✅ Evening Report found in DB.")
        else:
            logger.error("❌ Evening Report NOT found in DB.")
            
        if saved_morning and saved_evening:
            logger.info("\n✅ SUCCESS: Expert Agent is working correctly!")
        else:
            logger.error("\n❌ FAILURE: Database verification failed.")
            
    except Exception as e:
        logger.error(f"Verification failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
