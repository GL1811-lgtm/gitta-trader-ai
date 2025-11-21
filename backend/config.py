"""
Centralized Configuration Manager for Gitta Trader AI
Handles environment variables, cloud vs local differences, and configuration validation
"""

import os
from typing import Optional
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()


class Config:
    """Main configuration class"""
    
    # ========== ENVIRONMENT ==========
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    IS_PRODUCTION = ENVIRONMENT == 'production'
    IS_DEVELOPMENT = ENVIRONMENT == 'development'
    
    # ========== DATABASE ==========
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    # Determine database type
    if DATABASE_URL and DATABASE_URL.startswith('postgresql'):
        DATABASE_TYPE = 'postgresql'
        DATABASE_PATH = None  # PostgreSQL uses URL
    else:
        DATABASE_TYPE = 'sqlite'
        # Default SQLite path
        # Fixed: Only go up 2 levels from backend/config.py -> backend/ -> project_root/
        PROJECT_ROOT = Path(__file__).parent.parent
        DATABASE_PATH = os.getenv(
            'SQLITE_PATH',
            str(PROJECT_ROOT / 'backend' / 'data' / 'gitta.db')
        )
        # Ensure data directory exists
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    # ========== API KEYS ==========
    # Angel One
    ANGEL_ONE_API_KEY = os.getenv('ANGEL_ONE_API_KEY')
    ANGEL_ONE_CLIENT_ID = os.getenv('ANGEL_ONE_CLIENT_ID')
    ANGEL_ONE_PASSWORD = os.getenv('ANGEL_ONE_PASSWORD')
    ANGEL_ONE_TOTP_SECRET = os.getenv('ANGEL_ONE_TOTP_SECRET')
    ANGEL_ONE_SECRET_KEY = os.getenv('ANGEL_ONE_SECRET_KEY')
    
    # AI APIs
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
    
    # YouTube API
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')
    
    # ========== GOOGLE DRIVE ==========
    GOOGLE_DRIVE_ENABLED = os.getenv('GOOGLE_DRIVE_ENABLED', 'true').lower() == 'true'
    GOOGLE_DRIVE_CREDENTIALS_PATH = os.getenv(
        'GOOGLE_DRIVE_CREDENTIALS_PATH',
        'credentials.json'
    )
    GOOGLE_DRIVE_FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
    BACKUP_ENABLED = os.getenv('BACKUP_ENABLED', 'true').lower() == 'true'
    
    # ========== TRADING SETTINGS ==========
    TRADING_MODE = os.getenv('TRADING_MODE', 'paper')  # 'paper' or 'live'
    PAPER_CAPITAL = float(os.getenv('PAPER_CAPITAL', '100000'))
    MAX_POSITION_SIZE = float(os.getenv('MAX_POSITION_SIZE', '10000'))
    DAILY_LOSS_LIMIT = float(os.getenv('DAILY_LOSS_LIMIT', '1.5'))  # percentage
    
    # ========== AGENT SETTINGS ==========
    CONTINUOUS_MODE = os.getenv('CONTINUOUS_MODE', 'true').lower() == 'true'
    COLLECTOR_INTERVAL_MINUTES = int(os.getenv('COLLECTOR_INTERVAL_MINUTES', '15'))
    TESTER_INTERVAL_MINUTES = int(os.getenv('TESTER_INTERVAL_MINUTES', '30'))
    BATCH_SIZE_STRATEGIES = int(os.getenv('BATCH_SIZE_STRATEGIES', '10'))
    MAX_DAILY_CALLS_PER_COLLECTOR = int(os.getenv('MAX_DAILY_CALLS_PER_COLLECTOR', '96'))
    
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
    LOG_FILE_PATH = os.getenv('LOG_FILE_PATH', 'logs/gitta_trader.log')
    
    # ========== WEB SERVER ==========
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', '5001'))
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5173,http://localhost:3000').split(',')
    
    # ========== CLOUD SPECIFIC ==========
    CLOUD_PLATFORM = os.getenv('CLOUD_PLATFORM')  # 'railway', 'render', 'fly', 'gcp'
    
    @classmethod
    def validate(cls) -> tuple[bool, list[str]]:
        """
        Validate configuration
        
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check database configuration
        if cls.DATABASE_TYPE == 'postgresql' and not cls.DATABASE_URL:
            errors.append("DATABASE_URL is required for PostgreSQL")
        
        # Check critical API keys (at least one AI API should be present)
        ai_keys = [cls.GEMINI_API_KEY, cls.OPENROUTER_API_KEY]
        if not any(ai_keys):
            errors.append("At least one AI API key is required (GEMINI or OPENROUTER)")
        
        # Check Google Drive configuration if enabled
        if cls.GOOGLE_DRIVE_ENABLED and cls.BACKUP_ENABLED:
            if not os.path.exists(cls.GOOGLE_DRIVE_CREDENTIALS_PATH):
                errors.append(f"Google Drive credentials not found at {cls.GOOGLE_DRIVE_CREDENTIALS_PATH}")
            if not cls.GOOGLE_DRIVE_FOLDER_ID:
                errors.append("GOOGLE_DRIVE_FOLDER_ID is required when backups are enabled")
        
        return (len(errors) == 0, errors)
    
    @classmethod
    def print_config(cls):
        """Print current configuration (excluding sensitive data)"""
        print("=" * 60)
        print("GITTA TRADER AI - CONFIGURATION")
        print("=" * 60)
        print(f"Environment:        {cls.ENVIRONMENT}")
        print(f"Database Type:      {cls.DATABASE_TYPE}")
        
        if cls.DATABASE_TYPE == 'postgresql':
            # Mask password in DATABASE_URL
            masked_url = cls.DATABASE_URL
            if '@' in masked_url:
                parts = masked_url.split('@')
                before_at = parts[0].split(':')
                before_at[-1] = '****'
                masked_url = ':'.join(before_at) + '@' + parts[1]
            print(f"Database URL:       {masked_url}")
        else:
            print(f"Database Path:      {cls.DATABASE_PATH}")
        
        print(f"Trading Mode:       {cls.TRADING_MODE}")
        print(f"Paper Capital:      ₹{cls.PAPER_CAPITAL:,.0f}")
        print(f"Continuous Mode:    {cls.CONTINUOUS_MODE}")
        print(f"Google Drive:       {'✅ Enabled' if cls.GOOGLE_DRIVE_ENABLED else '❌ Disabled'}")
        print(f"Backups:            {'✅ Enabled' if cls.BACKUP_ENABLED else '❌ Disabled'}")
        
        # API Keys status
        print("\nAPI Keys:")
        print(f"  Gemini:           {'✅' if cls.GEMINI_API_KEY else '❌'}")
        print(f"  OpenAI:           {'✅' if cls.OPENAI_API_KEY else '❌'}")
        print(f"  OpenRouter:       {'✅' if cls.OPENROUTER_API_KEY else '❌'}")
        print(f"  YouTube:          {'✅' if cls.YOUTUBE_API_KEY else '❌'}")
        print(f"  Angel One:        {'✅' if cls.ANGEL_ONE_API_KEY else '❌'}")
        
        print("=" * 60)
        
        # Validate
        is_valid, errors = cls.validate()
        if is_valid:
            print("✅ Configuration is valid")
        else:
            print("❌ Configuration has errors:")
            for error in errors:
                print(f"   - {error}")
        print("=" * 60)


# Export singleton instance
config = Config()


if __name__ == "__main__":
    # Print configuration when run directly
    config.print_config()
