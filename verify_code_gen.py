from backend.evolution.safety import CodeSafetySanitizer
from backend.evolution.improvement_loop import ImprovementLoop

def verify_code_gen():
    print("--- Verifying AI Code Generator ---")
    
    # 1. Test Safety Sanitizer
    print("\n1. Testing CodeSafetySanitizer...")
    safe_code = "import math\nx = math.sqrt(25)"
    unsafe_code = "import os\nos.system('rm -rf /')"
    
    is_safe, msg = CodeSafetySanitizer.validate(safe_code)
    if is_safe:
        print("PASS: Safe code accepted.")
    else:
        print(f"FAIL: Safe code rejected: {msg}")
        
    is_safe, msg = CodeSafetySanitizer.validate(unsafe_code)
    if not is_safe:
        print(f"PASS: Unsafe code rejected: {msg}")
    else:
        print("FAIL: Unsafe code accepted!")

    # 2. Test Improvement Loop
    print("\n2. Testing ImprovementLoop...")
    loop = ImprovementLoop()
    dummy_code = """
def strategy(data):
    return 1
"""
    metrics = {"sharpe_ratio": 0.5, "max_drawdown": -0.3, "win_rate": 0.3}
    
    try:
        new_code = loop.improve_strategy("verify_test", dummy_code, metrics)
        if new_code and "SMA" in new_code: # The mock generator adds SMA logic
            print("PASS: Improvement loop generated new code.")
        else:
            print("FAIL: Improvement loop failed to generate code.")
    except Exception as e:
        print(f"FAIL: Error in loop: {e}")

if __name__ == "__main__":
    verify_code_gen()
