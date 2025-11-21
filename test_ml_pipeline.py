import requests
import time

BASE_URL = "http://localhost:5001"
SYMBOL = "RELIANCE.NS"

def test_ml_pipeline():
    print("--- Testing ML Pipeline ---")
    
    # 1. Train Model
    print(f"\n1. Training Model for {SYMBOL}...")
    try:
        res = requests.post(f"{BASE_URL}/api/ml/train", json={"symbol": SYMBOL})
        if res.status_code == 200:
            data = res.json()
            if "error" in data:
                print(f"❌ Training Failed: {data['error']}")
                return
            print(f"✅ Training Successful!")
            print(f"   Accuracy: {data['accuracy']:.2f}")
            print(f"   Model saved at: {data['model_path']}")
        else:
            print(f"❌ Training Request Failed: {res.status_code} - {res.text}")
            return
    except Exception as e:
        print(f"❌ Training Exception: {e}")
        return

    # 2. Predict
    print(f"\n2. Predicting for {SYMBOL}...")
    try:
        res = requests.get(f"{BASE_URL}/api/ml/predict/{SYMBOL}")
        if res.status_code == 200:
            data = res.json()
            if "error" in data:
                print(f"❌ Prediction Failed: {data['error']}")
                return
            print(f"✅ Prediction Successful!")
            print(f"   Prediction: {data['prediction']}")
            print(f"   Confidence: {data['confidence']}%")
            print(f"   Features: {data['features']}")
        else:
            print(f"❌ Prediction Request Failed: {res.status_code} - {res.text}")
            return
    except Exception as e:
        print(f"❌ Prediction Exception: {e}")
        return

if __name__ == "__main__":
    test_ml_pipeline()
