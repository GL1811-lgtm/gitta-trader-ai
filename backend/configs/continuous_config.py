"""
Continuous Operation Configuration

Controls 24/7 operation mode for all agents
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ========== CONTINUOUS OPERATION MODE ==========
CONTINUOUS_MODE = os.getenv('CONTINUOUS_MODE', 'true').lower() == 'true'

# ========== COLLECTOR CONFIGURATION ==========
COLLECTOR_INTERVAL_MINUTES = int(os.getenv('COLLECTOR_INTERVAL_MINUTES', '15'))
MAX_DAILY_CALLS_PER_COLLECTOR = int(os.getenv('MAX_DAILY_CALLS_PER_COLLECTOR', '96'))

# ========== TESTER CONFIGURATION ==========
TESTER_INTERVAL_MINUTES = int(os.getenv('TESTER_INTERVAL_MINUTES', '30'))
BATCH_SIZE_STRATEGIES = int(os.getenv('BATCH_SIZE_STRATEGIES', '10'))

# ========== EXPERT CONFIGURATION ==========
REPORT_INTERVAL_HOURS = int(os.getenv('REPORT_INTERVAL_HOURS', '24'))
MORNING_REPORT_TIME = os.getenv('MORNING_REPORT_TIME', '08:00')
EVENING_REPORT_TIME = os.getenv('EVENING_REPORT_TIME', '17:00')

# ========== RATE LIMITING ==========
RATE_LIMIT_DELAY_SECONDS = int(os.getenv('RATE_LIMIT_DELAY_SECONDS', '2'))
MAX_CONCURRENT_COLLECTORS = int(os.getenv('MAX_CONCURRENT_COLLECTORS', '10'))
MAX_CONCURRENT_TESTERS = int(os.getenv('MAX_CONCURRENT_TESTERS', '5'))

# ========== ERROR HANDLING ==========
MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
RETRY_DELAY_SECONDS = int(os.getenv('RETRY_DELAY_SECONDS', '60'))
HEALTH_CHECK_INTERVAL_SECONDS = int(os.getenv('HEALTH_CHECK_INTERVAL_SECONDS', '300'))

# ========== RESOURCE LIMITS ==========
MAX_CPU_PERCENT = int(os.getenv('MAX_CPU_PERCENT', '80'))
MAX_MEMORY_PERCENT = int(os.getenv('MAX_MEMORY_PERCENT', '80'))

# ========== LOGGING ==========
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_TO_FILE = os.getenv('LOG_TO_FILE', 'true').lower() == 'true'
LOG_FILE_PATH = os.getenv('LOG_FILE_PATH', 'logs/continuous_agents.log')


def get_config_summary():
    """Return configuration summary for logging"""
    return {
        'continuous_mode': CONTINUOUS_MODE,
        'collector_interval_minutes': COLLECTOR_INTERVAL_MINUTES,
        'tester_interval_minutes': TESTER_INTERVAL_MINUTES,
        'max_daily_calls_per_collector': MAX_DAILY_CALLS_PER_COLLECTOR,
        'rate_limit_delay_seconds': RATE_LIMIT_DELAY_SECONDS,
        'max_concurrent_collectors': MAX_CONCURRENT_COLLECTORS,
        'max_concurrent_testers': MAX_CONCURRENT_TESTERS,
    }
