import os
from dotenv import load_dotenv
from groq import Groq

print("=" * 60)
print("🚀 GROQ API VERIFICATION TEST")
print("=" * 60)

# Load environment
load_dotenv()

api_key = os.getenv('GROQ_API_KEY')

if not api_key:
    print("\n❌ GROQ_API_KEY not found in .env file")
    exit(1)

print(f"\n✅ API Key found: {api_key[:20]}...")

try:
    # Initialize Groq client
    client = Groq(api_key=api_key)
    
    print("\n🧪 Testing Groq API...")
    print("   Using Llama 3 model...")
    
    # Test with a simple prompt
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Reply with exactly: 'Groq API is working perfectly! Super fast!'"
            }
        ],
        model="llama-3.3-70b-versatile",  # Current Groq model
    )
    
    print("\n" + "=" * 60)
    print("✅ SUCCESS! GROQ IS WORKING!")
    print("=" * 60)
    print(f"\n📝 Response: {chat_completion.choices[0].message.content}")
    print(f"💰 Model used: {chat_completion.model}")
    print(f"⚡ Speed: SUPER FAST!")
    print(f"💵 Cost: 100% FREE!\n")
    
except Exception as e:
    print("\n" + "=" * 60)
    print("❌ GROQ API ERROR")
    print("=" * 60)
    print(f"\nError: {str(e)}\n")
    
    if "invalid" in str(e).lower():
        print("💡 Issue: Invalid API key")
        print("Get a new key from: https://console.groq.com")
