import os
from dotenv import load_dotenv
from openai import OpenAI

print("=" * 60)
print("🤖 OPENAI API VERIFICATION TEST")
print("=" * 60)

# Load environment
load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    print("\n❌ OPENAI_API_KEY not found in .env file")
    exit(1)

print(f"\n✅ API Key found: {api_key[:20]}...")

try:
    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)
    
    print("\n🧪 Testing OpenAI API...")
    print("   Sending test request to GPT-4o-mini...")
    
    # Test with a simple prompt
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Reply with exactly: 'OpenAI API is working perfectly!'"}
        ],
        max_tokens=50
    )
    
    print("\n" + "=" * 60)
    print("✅ SUCCESS! OPENAI IS WORKING!")
    print("=" * 60)
    print(f"\n📝 Response: {response.choices[0].message.content}")
    print(f"💰 Model used: {response.model}")
    print(f"🔢 Tokens used: {response.usage.total_tokens}\n")
    
except Exception as e:
    print("\n" + "=" * 60)
    print("❌ OPENAI API ERROR")
    print("=" * 60)
    print(f"\nError: {str(e)}\n")
    
    if "invalid" in str(e).lower():
        print("💡 Issue: Invalid API key")
        print("Check your OpenAI dashboard for the correct key")
    elif "quota" in str(e).lower():
        print("💡 Issue: API quota exceeded or billing not set up")
        print("Visit: https://platform.openai.com/account/billing")
