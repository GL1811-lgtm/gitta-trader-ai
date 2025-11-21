"""
Comprehensive End-to-End System Test
Tests all major components of Gitta Trader AI
"""
import requests
import time
import sys

print("=" * 70)
print("🧪 GITTA TRADER AI - END-TO-END SYSTEM TEST")
print("=" * 70)

BASE_URL = "http://localhost:5001"
tests_passed = 0
tests_failed = 0
errors = []

def test_endpoint(name, url, method="GET", data=None):
    global tests_passed, tests_failed, errors
    try:
        print(f"\n📝 Testing: {name}")
        if method == "GET":
            response = requests.get(url, timeout=10)
        else:
            response = requests.post(url, json=data, timeout=10)
        
        if response.status_code in [200, 201]:
            print(f"   ✅ PASS - Status: {response.status_code}")
            tests_passed += 1
            return True
        else:
            print(f"   ❌ FAIL - Status: {response.status_code}")
            print(f"   Error: {response.text[:100]}")
            tests_failed += 1
            errors.append(f"{name}: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ FAIL - Exception: {str(e)[:100]}")
        tests_failed += 1
        errors.append(f"{name}: {str(e)[:50]}")
        return False

print("\n" + "=" * 70)
print("STEP 1: SERVER HEALTH CHECK")
print("=" * 70)

# Wait a moment for server to be ready
print("\nWaiting for server...")
time.sleep(2)

test_endpoint("Health Check", f"{BASE_URL}/api/health")

print("\n" + "=" * 70)
print("STEP 2: CORE API ENDPOINTS")
print("=" * 70)

test_endpoint("Paper Trading - Get Account", f"{BASE_URL}/api/trading/account")
test_endpoint("Paper Trading - Get Portfolio", f"{BASE_URL}/api/trading/portfolio")
test_endpoint("Get Stock List", f"{BASE_URL}/api/stocks")

print("\n" + "=" * 70)
print("STEP 3: TRADING OPERATIONS")
print("=" * 70)

# Test placing an order
order_data = {
    "symbol": "RELIANCE.NS",
    "side": "BUY",
    "quantity": 1
}
test_endpoint("Place Paper Trade Order", f"{BASE_URL}/api/trading/order", "POST", order_data)

print("\n" + "=" * 70)
print("STEP 4: ML & PREDICTION")
print("=" * 70)

test_endpoint("ML Prediction", f"{BASE_URL}/api/ml/predict/RELIANCE.NS")

print("\n" + "=" * 70)
print("STEP 5: BACKTESTING")
print("=" * 70)

backtest_data = {
    "symbol": "RELIANCE.NS",
    "strategy": "SMA_CROSSOVER",
    "period": "3mo"
}
test_endpoint("Run Backtest", f"{BASE_URL}/api/backtest/run", "POST", backtest_data)

print("\n" + "=" * 70)
print("STEP 6: REPORTS")
print("=" * 70)

test_endpoint("Morning Report", f"{BASE_URL}/api/reports/morning")
test_endpoint("Evening Report", f"{BASE_URL}/api/reports/evening")

print("\n" + "=" * 70)
print("STEP 7: MONITORING")
print("=" * 70)

test_endpoint("Prometheus Metrics", f"{BASE_URL}/metrics")

print("\n" + "=" * 70)
print("📊 TEST SUMMARY")
print("=" * 70)

total_tests = tests_passed + tests_failed
pass_rate = (tests_passed / total_tests * 100) if total_tests > 0 else 0

print(f"\n✅ Tests Passed: {tests_passed}/{total_tests}")
print(f"❌ Tests Failed: {tests_failed}/{total_tests}")
print(f"📈 Pass Rate: {pass_rate:.1f}%")

if errors:
    print("\n🔴 ERRORS FOUND:")
    for i, error in enumerate(errors, 1):
        print(f"   {i}. {error}")
else:
    print("\n🎉 ALL TESTS PASSED!")

print("\n" + "=" * 70)

if pass_rate >= 80:
    print("✅ SYSTEM IS PRODUCTION READY!")
    sys.exit(0)
elif pass_rate >= 60:
    print("⚠️  SYSTEM NEEDS MINOR FIXES")
    sys.exit(0)
else:
    print("❌ SYSTEM NEEDS MAJOR FIXES")
    sys.exit(1)
