import os
import sys
from backend.utils.logger import logger
from backend.core.errors import ConfigurationError
from backend.core.config import Config
from backend.database.db import db

def check_environment_variables():
    """Checks if essential environment variables are set."""
    required_vars = [
        'FLASK_ENV',
        'DATABASE_URL'
    ]
    # Add API keys if they are strictly required for startup 
    
    missing = [var for var in required_vars if not os.environ.get(var)]
    
    if missing:
        logger.error(f"Missing environment variables: {', '.join(missing)}")
        return False
    return True

def check_database_connection():
    """Checks if the database is accessible."""
    try:
        conn = db._get_connection()
        conn.execute("SELECT 1")
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

def check_api_keys():
    """Checks if API keys are valid (mock check for now)."""
    # In a real scenario, you might make a lightweight call to the API
    # Add API checks here as needed
    return True

def run_startup_checks():
    """Runs all security and configuration checks."""
    logger.info("Running startup security checks...")
    
    if not check_environment_variables():
        raise ConfigurationError("Environment variable check failed.")
        
    if not check_database_connection():
        raise ConfigurationError("Database connection check failed.")
        
    check_api_keys() # Non-blocking warning
    
    logger.info("All startup checks passed.")
    return True

if __name__ == "__main__":
    try:
        run_startup_checks()
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Startup failed: {e}")
        sys.exit(1)
