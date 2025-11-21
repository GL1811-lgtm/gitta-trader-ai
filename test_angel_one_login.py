import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.trading.angel_one_client import AngelOneClient
from dotenv import load_dotenv

def test_angel_one_setup():
    print("Testing Angel One Setup...")
    
    # Load env
    load_dotenv()
    
    api_key = os.getenv("ANGEL_ONE_API_KEY")
    totp_secret = os.getenv("ANGEL_ONE_TOTP_SECRET")
    
    print(f"API Key present: {'Yes' if api_key else 'No'}")
    print(f"TOTP Secret present: {'Yes' if totp_secret else 'No'}")
    
    if not api_key or not totp_secret:
        print("❌ Missing credentials in .env")
        return

    try:
        client = AngelOneClient()
        print("✅ Angel One Client initialized")
        
        totp = client.generate_totp()
        print(f"✅ TOTP Generation Successful: {totp}")
        
        print("Attempting full login...")
        if client.login():
            print("✅ LOGIN SUCCESSFUL! 🚀")
            profile = client.get_profile()
            if profile:
                print(f"✅ Profile Fetched: {profile.get('data', {}).get('name', 'Unknown')}")
            else:
                print("⚠️ Login succeeded but profile fetch failed.")
        else:
            print("❌ Login Failed.")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_angel_one_setup()
