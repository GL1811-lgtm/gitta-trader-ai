import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

from backend.core.safety_layer import SafetyLimits

def run_tests():
    print("Running Safety Layer Tests...")
    failures = 0
    
    try:
        # Test Initialization
        safety = SafetyLimits(current_capital=100000)
        if safety.current_capital != 100000: raise ValueError("Init failed")
        print("✓ Initialization passed")
        
        # Test Risk Per Trade
        safety = SafetyLimits(current_capital=100000)
        res = safety.validate_trade(100, 96, 100) # Risk 400 (0.4%)
        if not res['allowed']: raise ValueError(f"Safe trade rejected: {res}")
        
        res = safety.validate_trade(100, 94, 100) # Risk 600 (0.6%)
        if res['allowed']: raise ValueError("Unsafe trade allowed")
        print("✓ Risk limits passed")
        
        # Test Position Size
        safety = SafetyLimits(current_capital=100000)
        res = safety.validate_trade(150, 149, 100) # 15000 (15%)
        if not res['allowed']: raise ValueError(f"Safe position rejected: {res}")
        
        res = safety.validate_trade(250, 249, 100) # 25000 (25%)
        if res['allowed']: raise ValueError("Unsafe position allowed")
        print("✓ Position limits passed")
        
        # Test Daily Loss
        safety = SafetyLimits(current_capital=100000)
        safety.update_capital(97900) # -2100 (-2.1%)
        if not safety.circuit_breaker_check(): raise ValueError("Circuit breaker failed on daily loss")
        res = safety.validate_trade(100, 99, 10)
        if res['allowed']: raise ValueError("Trade allowed after circuit breaker")
        print("✓ Daily loss limits passed")
        
        # Test Consecutive Losses
        safety = SafetyLimits(current_capital=100000)
        for _ in range(5): safety.record_trade_result(-100)
        if not safety.circuit_breaker_check(): raise ValueError("Circuit breaker failed on consecutive losses")
        print("✓ Consecutive loss limits passed")
        
        print("\nALL TESTS PASSED SUCCESSFULLY!")
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
