"""
Test OpenRouter API Integration
"""

import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.ai.openrouter_client import OpenRouterClient

def test_openrouter():
    """Test OpenRouter API functionality"""
    
    print("=" * 50)
    print("OpenRouter API Test")
    print("=" * 50)
    print()
    
    try:
        # Initialize client
        print("1. Initializing OpenRouter client...")
        client = OpenRouterClient()
        print("   ✓ Client initialized successfully")
        print()
        
        # Test 1: Simple chat
        print("2. Testing basic chat completion...")
        response = client.chat_completion([
            {"role": "user", "content": "What are the top 3 technical indicators for day trading? Answer in 2 sentences."}
        ])
        
        if response["success"]:
            print("   ✓ Chat completion successful")
            print(f"   Model: {response['model']}")
            print(f"   Response: {response['content'][:150]}...")
        else:
            print(f"   ✗ Chat completion failed: {response.get('error')}")
        print()
        
        # Test 2: Strategy analysis
        print("3. Testing strategy analysis...")
        strategy = "Buy when RSI crosses above 30, sell when it crosses below 70. Use 15-minute timeframe."
        analysis = client.analyze_strategy(strategy)
        
        if "Error" not in analysis:
            print("   ✓ Strategy analysis successful")
            print(f"   Analysis: {analysis[:150]}...")
        else:
            print(f"   ✗ Strategy analysis failed: {analysis}")
        print()
        
        # Test 3: Market research
        print("4. Testing market research...")
        research = client.research_market_topic("Current trends in NIFTY 50 index")
        
        if "Error" not in research:
            print("   ✓ Market research successful")
            print(f"   Research: {research[:150]}...")
        else:
            print(f"   ✗ Market research failed: {research}")
        print()
        
        print("=" * 50)
        print("✓ All tests completed successfully!")
        print("=" * 50)
        
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_openrouter()
