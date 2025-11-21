import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=" * 60)
print("🔍 GEMINI API VERIFICATION TEST")
print("=" * 60)

# Method 1: Direct file read
print("\n📁 Method 1: Reading .env file directly...")
try:
    with open('.env', 'r') as f:
        for line in f:
            if 'GEMINI_API_KEY' in line and not line.startswith('#'):
                key_part = line.split('=')[1].strip().strip('"')
                print(f"✅ Found key in file: {key_part[:25]}...")
                actual_key = key_part
                break
except Exception as e:
    print(f"❌ Error reading .env: {e}")
    sys.exit(1)

# Method 2: Test with python-dotenv
print("\n📦 Method 2: Using python-dotenv...")
try:
    from dotenv import load_dotenv
    load_dotenv()
    dotenv_key = os.getenv('GEMINI_API_KEY')
    if dotenv_key:
        print(f"✅ Key loaded: {dotenv_key[:25]}...")
    else:
        print("❌ Key not loaded by dotenv")
except Exception as e:
    print(f"❌ dotenv error: {e}")

# Method 3: Test Gemini API
print("\n🧪 Method 3: Testing Gemini API...")
try:
    import google.generativeai as genai
    
    # Use the key we found from file
    genai.configure(api_key=actual_key)
    
    model = genai.GenerativeModel('gemini-pro')
    
    print("   Sending test request...")
    response = model.generate_content("Reply with exactly: 'Gemini API is working!'")
    
    print("\n" + "=" * 60)
    print("✅ SUCCESS! GEMINI IS WORKING!")
    print("=" * 60)
    print(f"\n📝 Response: {response.text}\n")
    
except Exception as e:
    print("\n" + "=" * 60)
    print("❌ GEMINI API ERROR")
    print("=" * 60)
    print(f"\nError: {str(e)}\n")
    
    # Provide helpful troubleshooting
    if "API key not valid" in str(e):
        print("💡 Issue: Invalid API key")
        print("\n🔧 Steps to fix:")
        print("1. Go to: https://aistudio.google.com/app/apikey")
        print("2. Create a NEW API key")
        print("3. Update .env file with: GEMINI_API_KEY=\"YOUR_NEW_KEY\"")
    elif "quota" in str(e).lower():
        print("💡 Issue: API quota exceeded")
        print("Either wait or create a new API key")
    else:
        print("💡 Issue: Unknown error")
        print("Check your internet connection and API key permissions")
