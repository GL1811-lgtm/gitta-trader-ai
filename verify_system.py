import requests
import time
import sys

BASE_URL = "http://localhost:5001"

def print_test(name, passed):
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} - {name}")

def test_health_check():
    """Test basic health endpoint"""
    try:
        res = requests.get(f"{BASE_URL}/api/health", timeout=5)
        print_test("Health Check", res.status_code == 200)
        return res.status_code == 200
    except Exception as e:
        print_test("Health Check", False)
        print(f"   Error: {e}")
        return False

def test_scheduler_jobs():
    """Test scheduler status"""
    try:
        res = requests.get(f"{BASE_URL}/api/scheduler/jobs", timeout=5)
        data = res.json()
        passed = res.status_code == 200 and data.get('status') == 'running'
        print_test("Scheduler Jobs", passed)
        if passed:
            print(f"   Jobs registered: {len(data.get('jobs', []))}")
        return passed
    except Exception as e:
        print_test("Scheduler Jobs", False)
        return False

def test_trading_account():
    """Test paper trading account"""
    try:
        res = requests.get(f"{BASE_URL}/api/trading/account", timeout=5)
        data = res.json()
        passed = res.status_code == 200 and 'balance' in data
        print_test("Trading Account", passed)
        if passed:
            print(f"   Balance: ₹{data['balance']:,.2f}")
        return passed
    except Exception as e:
        print_test("Trading Account", False)
        return False

def test_trading_order():
    """Test placing a paper trade order"""
    try:
        payload = {"symbol": "RELIANCE.NS", "side": "BUY", "quantity": 1}
        res = requests.post(f"{BASE_URL}/api/trading/order", json=payload, timeout=10)
        data = res.json()
        passed = res.status_code == 200 and data.get('status') == 'success'
        print_test("Place Order (BUY)", passed)
        if passed:
            print(f"   {data.get('message', '')}")
        return passed
    except Exception as e:
        print_test("Place Order (BUY)", False)
        return False

def test_backtest():
    """Test backtesting engine"""
    try:
        payload = {
            "symbol": "RELIANCE.NS",
            "strategy": "SMA_CROSSOVER",
            "period": "3mo",
            "initial_capital": 100000
        }
        res = requests.post(f"{BASE_URL}/api/backtest/run", json=payload, timeout=15)
        data = res.json()
        passed = res.status_code == 200 and 'final_equity' in data
        print_test("Backtest Engine", passed)
        if passed:
            print(f"   Return: {data.get('total_return_pct', 0):.2f}%")
        return passed
    except Exception as e:
        print_test("Backtest Engine", False)
        return False

def test_ml_prediction():
    """Test ML prediction (if model exists)"""
    try:
        res = requests.get(f"{BASE_URL}/api/ml/predict/RELIANCE.NS", timeout=10)
        data = res.json()
        
        if data.get('status') == 'error' and 'Model not found' in data.get('message', ''):
            print_test("ML Prediction", True)
            print("   ℹ️ Model not trained yet (expected)")
            return True
        
        passed = res.status_code == 200 and data.get('status') == 'success'
        print_test("ML Prediction", passed)
        if passed:
            print(f"   Prediction: {data.get('prediction')} ({data.get('confidence')}%)")
        return passed
    except Exception as e:
        print_test("ML Prediction", False)
        return False

def test_metrics():
    """Test Prometheus metrics endpoint"""
    try:
        res = requests.get(f"{BASE_URL}/metrics", timeout=5)
        passed = res.status_code == 200 and b'http_requests_total' in res.content
        print_test("Prometheus Metrics", passed)
        return passed
    except Exception as e:
        print_test("Prometheus Metrics", False)
        return False

def main():
    print("\n" + "="*60)
    print("🚀 GITTA TRADER AI - SYSTEM VERIFICATION")
    print("="*60 + "\n")
    
    print("📡 Testing Backend Server...\n")
    
    # Basic connectivity
    if not test_health_check():
        print("\n❌ Backend server is not responding!")
        print("   Please start the server with: python backend/api/app.py")
        sys.exit(1)
    
    print("\n📊 Testing Core Features...\n")
    
    results = []
    results.append(test_scheduler_jobs())
    results.append(test_metrics())
    
    print("\n💰 Testing Paper Trading...\n")
    results.append(test_trading_account())
    results.append(test_trading_order())
    
    print("\n🔬 Testing Intelligence Features...\n")
    results.append(test_backtest())
    results.append(test_ml_prediction())
    
    print("\n" + "="*60)
    passed = sum(results)
    total = len(results)
    print(f"📊 RESULTS: {passed}/{total} tests passed ({(passed/total*100):.0f}%)")
    print("="*60 + "\n")
    
    if passed == total:
        print("✅ ALL SYSTEMS OPERATIONAL! 🎉")
        print("   The system is ready for deployment.")
    elif passed >= total * 0.8:
        print("⚠️ MOSTLY OPERATIONAL")
        print("   Some features may need attention.")
    else:
        print("❌ SYSTEM ISSUES DETECTED")
        print("   Please review the failed tests above.")
    
    print()

if __name__ == "__main__":
    main()
