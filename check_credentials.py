"""
Check if Angel One API credentials are configured.
This script helps you verify your setup step-by-step.
"""

import os
from dotenv import load_dotenv

print("🔍 Checking Angel One API Configuration...")
print("=" * 60)

# Load environment variables
load_dotenv()

# Check each required credential
credentials = {
    "ANGEL_ONE_API_KEY": os.getenv("ANGEL_ONE_API_KEY"),
    "ANGEL_ONE_CLIENT_ID": os.getenv("ANGEL_ONE_CLIENT_ID"),
    "ANGEL_ONE_PASSWORD": os.getenv("ANGEL_ONE_PASSWORD"),
    "ANGEL_ONE_TOTP_SECRET": os.getenv("ANGEL_ONE_TOTP_SECRET"),
}

all_present = True
for key, value in credentials.items():
    if value and value != f"your_{key.lower()}_here":
        print(f"✅ {key}: Configured")
    else:
        print(f"❌ {key}: Missing")
        all_present = False

print("=" * 60)

if all_present:
    print("\n🎉 SUCCESS! All Angel One credentials are configured.")
    print("\nNext step: Run test_angel_one.py to verify connection:")
    print("  python test_angel_one.py")
else:
    print("\n⚠️  INCOMPLETE SETUP")
    print("\nYou have 3 options:")
    print("\n1. Configure Angel One API (Recommended)")
    print("   • Create .env file from .env.example")
    print("   • Add your Angel One credentials")
    print("   • See QUICK_START_GUIDE.md for details")
    print("\n2. Apply for Angel One API")
    print("   • Visit: https://smartapi.angelbroking.com/")
    print("   • Create app and get credentials")
    print("   • Takes 5-10 minutes")
    print("\n3. Use Mock Data (Temporary)")
    print("   • I can set up simulated data for testing")
    print("   • No real market data")
    print("\nWhich option would you like?")

print("\n" + "=" * 60)
