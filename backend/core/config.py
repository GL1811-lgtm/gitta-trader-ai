"""
Configuration Loader for Gitta Trader AI V2.0
"""
import os
from dotenv import load_dotenv
from backend.core.constants import MODE_PAPER

# Load environment variables
load_dotenv()

class Config:
    """Centralized configuration for the application."""
    
    # General
    TRADING_MODE = os.getenv("TRADING_MODE", MODE_PAPER)
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    
    # Broker (Angel One)
    ANGEL_API_KEY = os.getenv("ANGEL_API_KEY")
    ANGEL_CLIENT_ID = os.getenv("ANGEL_CLIENT_ID")
    ANGEL_PASSWORD = os.getenv("ANGEL_PASSWORD")
    ANGEL_TOTP_KEY = os.getenv("ANGEL_TOTP_KEY")
    
    # Database
    DB_PATH = os.getenv("DB_PATH", "gitta.db")
    
    # Paper Trading
    PAPER_CAPITAL = float(os.getenv("PAPER_CAPITAL", "100000"))
    
    @classmethod
    def validate(cls):
        """Validate critical configuration."""
        if not cls.GEMINI_API_KEY:
            print("WARNING: GEMINI_API_KEY not found. AI features will be disabled.")
        
        if cls.TRADING_MODE == "live":
            if not all([cls.ANGEL_API_KEY, cls.ANGEL_CLIENT_ID, cls.ANGEL_PASSWORD, cls.ANGEL_TOTP_KEY]):
                raise ValueError("CRITICAL: Missing Angel One credentials for LIVE trading.")
