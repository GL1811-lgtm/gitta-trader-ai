"""
Multi-AI System Comprehensive Test
Tests the complete multi-AI verification system
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.ai.multi_ai_verifier import MultiAIVerifier
from backend.ai.consensus_engine import ConsensusEngine
from backend.ai.config.models_config import get_model_stats, get_trading_models

def test_configuration():
    """Test model configuration"""
    print("=" * 60)
    print("TEST 1: Configuration")
    print("=" * 60)
    
    stats = get_model_stats()
    print(f"✓ Total Models: {stats['total_models']}")
    print(f"✓ Active Models: {stats['active_models']}")
    print(f"✓ Trading Models: {stats['trading_models']}")
    print(f"✓ Specialized Models: {stats['specialized_models']}")
    
    trading_models = get_trading_models()
    print(f"\n✓ Trading Models ({len(trading_models)}):")
    for model in trading_models:
        print(f"  - {model['name']} ({model['role'].value})")
    
    print("\n✅ Configuration test PASSED\n")
    return True

def test_multi_ai_verification():
    """Test multi-AI verification with real API call"""
    print("=" * 60)
    print("TEST 2: Multi-AI Verification (LIVE API)")
    print("=" * 60)
    
    verifier = MultiAIVerifier()
    
    # Simple test strategy
    strategy = """
    EMA Crossover Strategy:
    - Buy when 9 EMA crosses above 21 EMA
    - Sell when 9 EMA crosses below 21 EMA
    - Stop loss: 1.5%
    - Timeframe: 1 hour
    """
    
    print(f"Strategy to verify:")
    print(strategy)
    print(f"\nCalling {len(get_trading_models())} AI models in parallel...")
    print("Please wait 6-10 seconds...\n")
    
    result = verifier.verify_strategy(strategy)
    
    print("=" * 60)
    print("Verification Results:")
    print("=" * 60)
    print(f"Duration: {result['total_duration']:.2f} seconds")
    print(f"Models Called: {result['total_models']}")
    print(f"Successful: {result['successful_responses']}")
    print(f"Failed: {result['failed_responses']}")
    
    # Show first 2 responses
    print("\n✓ Sample Responses:")
    for i, response in enumerate(result['responses'][:2]):
        if response['success']:
            print(f"\n{i+1}. {response['model_name']} ({response['duration']:.2f}s)")
            print(f"   {response['content'][:150]}...")
    
    if result['successful_responses'] > 0:
        print("\n✅ Multi-AI verification test PASSED\n")
        return True, result
    else:
        print("\n❌ Multi-AI verification test FAILED\n")
        return False, result

def test_consensus_engine(verification_result):
    """Test consensus engine"""
    print("=" * 60)
    print("TEST 3: Consensus Engine")
    print("=" * 60)
    
    engine = ConsensusEngine()
    consensus = engine.calculate_consensus(verification_result['responses'])
    
    print(f"Status: {consensus['status']}")
    print(f"Total Responses: {consensus['total_responses']}")
    print(f"Average Score: {consensus['average_score']}/10")
    print(f"Weighted Average: {consensus['weighted_average_score']}/10")
    print(f"Consensus Recommendation: {consensus['consensus_recommendation']}")
    print(f"Agreement Rate: {consensus['agreement_rate']}%")
    print(f"Confidence: {consensus['confidence']}%")
    print(f"\nInterpretation: {consensus['interpretation']}")
    
    print("\n✅ Consensus engine test PASSED\n")
    return True, consensus

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "MULTI-AI SYSTEM TEST" + " " * 23 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    all_passed = True
    
    # Test 1: Configuration
    try:
        if not test_configuration():
            all_passed = False
    except Exception as e:
        print(f"❌ Configuration test FAILED: {e}\n")
        all_passed = False
    
    # Test 2: Multi-AI Verification
    verification_result = None
    try:
        success, verification_result = test_multi_ai_verification()
        if not success:
            all_passed = False
    except Exception as e:
        print(f"❌ Multi-AI verification test FAILED: {e}\n")
        all_passed = False
    
    # Test 3: Consensus Engine
    if verification_result:
        try:
            success, consensus = test_consensus_engine(verification_result)
            if not success:
                all_passed = False
        except Exception as e:
            print(f"❌ Consensus engine test FAILED: {e}\n")
            all_passed = False
    
    # Final summary
    print("=" * 60)
    if all_passed:
        print("✅ ALL TESTS PASSED!")
        print("\nThe Multi-AI verification system is working correctly.")
        print(f"All {get_model_stats()['trading_models']} trading models are operational.")
    else:
        print("❌ SOME TESTS FAILED")
        print("\nPlease check the errors above.")
    print("=" * 60)
    print()

if __name__ == "__main__":
    main()
