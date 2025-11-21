import os
import pyotp
from SmartApi import SmartConnect
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AngelOneClient:
    """
    Client for interacting with Angel One SmartAPI.
    Handles authentication (including TOTP) and basic trading operations.
    """
    def __init__(self):
        self.api_key = os.getenv("ANGEL_ONE_API_KEY")
        self.client_id = os.getenv("ANGEL_ONE_CLIENT_ID") # Note: This might be needed if not using API Key as Client ID
        self.password = os.getenv("ANGEL_ONE_PASSWORD") # Needed for full login flow if not using just API Key
        self.totp_secret = os.getenv("ANGEL_ONE_TOTP_SECRET")
        
        # Angel One uses API Key for SmartConnect init
        if not self.api_key:
            logger.error("ANGEL_ONE_API_KEY not found in environment variables")
            raise ValueError("ANGEL_ONE_API_KEY is required")
            
        self.smart_api = SmartConnect(api_key=self.api_key)
        self.session_data = None
        self.auth_token = None
        self.refresh_token = None
        self.feed_token = None

    def generate_totp(self):
        """Generates Time-based OTP using the secret key."""
        if not self.totp_secret:
            raise ValueError("ANGEL_ONE_TOTP_SECRET is required for login")
        try:
            totp = pyotp.TOTP(self.totp_secret).now()
            return totp
        except Exception as e:
            logger.error(f"Error generating TOTP: {str(e)}")
            raise

    def login(self):
        """
        Logs in to Angel One using Client ID, Password, and TOTP.
        Note: For the new SmartAPI flow, we typically need:
        1. Client Code (User ID)
        2. Password (PIN/Password)
        3. TOTP
        
        However, the `generateSession` method signature is:
        generateSession(clientCode, password, totp)
        """
        # We need Client ID (User ID) and Password (PIN) for login
        # If they are not in env, we can't proceed with full login
        # But for now, let's assume we might have them or user will provide them.
        
        # Check if we have all credentials
        if not self.client_id or not self.password or not self.totp_secret:
             logger.warning("Missing Client ID, Password, or TOTP Secret. Cannot perform full login.")
             # We can still initialize the object, but login will fail.
             return False

        try:
            totp = self.generate_totp()
            data = self.smart_api.generateSession(self.client_id, self.password, totp)
            
            if data['status'] == True:
                self.session_data = data['data']
                self.auth_token = data['data']['jwtToken']
                self.refresh_token = data['data']['refreshToken']
                self.feed_token = data['data']['feedToken']
                logger.info(f"Successfully logged in to Angel One. Client: {self.client_id}")
                return True
            else:
                logger.error(f"Login failed: {data['message']}")
                return False
                
        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return False

    def get_profile(self):
        """Fetches user profile."""
        if not self.auth_token:
            logger.warning("Not logged in. Cannot fetch profile.")
            return None
        try:
            return self.smart_api.getProfile(self.refresh_token)
        except Exception as e:
            logger.error(f"Error fetching profile: {str(e)}")
            return None

    def get_historical_data(self, exchange, symbol_token, interval, from_date, to_date):
        """
        Fetches historical candle data.
        
        Params:
        exchange: "NSE" or "NFO"
        symbol_token: Stock/Contract Token (e.g., "3045")
        interval: "ONE_MINUTE", "FIVE_MINUTE", "ONE_HOUR", "ONE_DAY"
        from_date: "yyyy-mm-dd HH:MM"
        to_date: "yyyy-mm-dd HH:MM"
        """
        if not self.auth_token:
            logger.warning("Not logged in. Cannot fetch historical data.")
            return None
            
        try:
            historicParam = {
                "exchange": exchange,
                "symboltoken": symbol_token,
                "interval": interval,
                "fromdate": from_date, 
                "todate": to_date
            }
            data = self.smart_api.getCandleData(historicParam)
            return data
        except Exception as e:
            logger.error(f"Error fetching historical data: {str(e)}")
            return None

if __name__ == "__main__":
    # Simple test
    try:
        client = AngelOneClient()
        print("Angel One Client initialized successfully.")
        # We can't test login without Client ID and Password in env
        # But we can verify TOTP generation
        if client.totp_secret:
            print(f"Generated TOTP: {client.generate_totp()}")
    except Exception as e:
        print(f"Initialization failed: {e}")
