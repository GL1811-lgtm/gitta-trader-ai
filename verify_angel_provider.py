import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.data_providers.angel_one import AngelOneDataProvider
from dotenv import load_dotenv

def test_provider():
    print("Testing AngelOneDataProvider...")
    load_dotenv()
    
    provider = AngelOneDataProvider()
    print("Initializing provider...")
    
    if provider.connect():
        print("✅ Provider connected successfully!")
    else:
        print("❌ Provider connection failed.")

if __name__ == "__main__":
    test_provider()
