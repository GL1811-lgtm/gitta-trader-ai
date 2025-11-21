from backend.core.safety_layer import SafetyLimits

def run_tests():
    try:
        print("Testing initialization...")
        safety = SafetyLimits(capital=100000)
        assert safety.capital == 100000
        print("PASS")

        print("Testing valid trade...")
        result = safety.validate_trade("INFY", 10, 100, 99, "paper")
        assert result.is_valid
        print("PASS")

        print("Testing invalid mode...")
        result = safety.validate_trade("INFY", 10, 100, 99, "invalid")
        assert not result.is_valid
        print("PASS")

        print("Testing max daily trades...")
        safety = SafetyLimits(capital=100000, daily_trades_count=20)
        result = safety.validate_trade("INFY", 10, 100, 99, "paper")
        assert not result.is_valid
        print("PASS")

        print("Testing max daily loss...")
        safety = SafetyLimits(capital=100000, current_pnl=-5001)
        result = safety.validate_trade("INFY", 10, 100, 99, "paper")
        assert not result.is_valid
        print("PASS")

        print("Testing position size...")
        safety = SafetyLimits(capital=100000)
        result = safety.validate_trade("INFY", 201, 100, 99, "paper")
        assert not result.is_valid
        print("PASS")

        print("Testing risk per trade...")
        safety = SafetyLimits(capital=100000)
        result = safety.validate_trade("INFY", 50, 100, 50, "paper")
        assert not result.is_valid
        print("PASS")
        
        print("ALL TESTS PASSED")
        
    except AssertionError as e:
        print(f"TEST FAILED: {e}")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    run_tests()
