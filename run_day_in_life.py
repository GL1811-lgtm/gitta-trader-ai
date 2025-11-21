import time
import logging
from datetime import datetime
from backend.intelligence.scanner import MorningScanner
from backend.intelligence.validator import EveningValidator
from backend.database.db import DatabaseManager
from backend.notifications.telegram_bot import TelegramBot

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_simulation():
    logger.info("=== STARTING DAY IN THE LIFE SIMULATION ===")
    
    db = DatabaseManager()
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    # Initialize Telegram Bot
    bot = TelegramBot()
    bot.send_alert("🚀 *Gitta Trader AI* - Day in the Life Simulation Started")

    # 1. Morning Simulation
    logger.info("\n[08:00 AM] Simulating Morning Scan...")
    try:
        scanner = MorningScanner()
        morning_report = scanner.scan_market()
        logger.info("Morning Scan Completed.")
        logger.info(f"Report Preview: {morning_report[:100]}...")
        bot.send_alert(f"🌅 *Morning Prediction Report*\n\n{morning_report[:200]}...\n\n[View Full Report](http://localhost:5173/#reports)")
    except Exception as e:
        logger.error(f"Morning Scan Failed: {e}")
        bot.send_alert(f"⚠️ Morning Scan Failed: {e}")
        return

    # Verify Morning Persistence
    saved_morning = db.get_report(date_str)
    if saved_morning:
        logger.info("SUCCESS: Morning Report saved to DB.")
    else:
        logger.error("FAILURE: Morning Report NOT found in DB.")
        return

    # 2. Market Activity Simulation (Placeholder)
    logger.info("\n[10:00 AM - 03:30 PM] Simulating Market Activity...")
    time.sleep(2) # Simulate time passing
    logger.info("Market Closed.")

    # 3. Evening Simulation
    logger.info("\n[05:00 PM] Simulating Evening Validation...")
    try:
        validator = EveningValidator()
        evening_report = validator.validate_predictions()
        logger.info("Evening Validation Completed.")
        logger.info(f"Report Preview: {evening_report[:100]}...")
        bot.send_alert(f"🌇 *Evening Review Report*\n\n{evening_report[:200]}...\n\n[View Full Report](http://localhost:5173/#reports)")
    except Exception as e:
        logger.error(f"Evening Validation Failed: {e}")
        bot.send_alert(f"⚠️ Evening Validation Failed: {e}")
        return

    # Verify Evening Persistence
    # Note: Evening reports are saved with suffix _EVENING in the current implementation
    saved_evening = db.get_report(f"{date_str}_EVENING")
    if saved_evening:
        logger.info("SUCCESS: Evening Report saved to DB.")
    else:
        logger.error("FAILURE: Evening Report NOT found in DB.")
        return

    logger.info("\n=== SIMULATION COMPLETED SUCCESSFULLY ===")
    logger.info("The Gitta Trader AI system is fully operational.")
    bot.send_alert("✅ *Simulation Completed Successfully*\nSystem is fully operational.")

if __name__ == "__main__":
    run_simulation()
