import os
import joblib
import pandas as pd
from backend.data_providers.manager import DataProviderManager
from backend.ml.feature_engineering import FeatureEngineer
import logging

logger = logging.getLogger(__name__)

class MLPredictor:
    def __init__(self):
        self.data_provider = DataProviderManager()
        self.feature_engineer = FeatureEngineer()
        self.models_dir = "backend/ml/models"

    def predict(self, symbol):
        """
        Loads model and predicts probability of price going UP.
        """
        model_path = os.path.join(self.models_dir, f"{symbol}_rf.joblib")
        
        if not os.path.exists(model_path):
            return {"status": "error", "message": "Model not found. Please train first."}

        # 1. Load Model
        try:
            model = joblib.load(model_path)
        except Exception as e:
            return {"status": "error", "message": f"Failed to load model: {e}"}

        # 2. Fetch Recent Data
        # We need enough data to calculate indicators (e.g. 200 days for SMA_200)
        df = self.data_provider.get_historical_data(symbol, period="1y", interval="1d")
        if df is None or df.empty:
            return {"status": "error", "message": "No data found"}

        # 3. Engineer Features
        # We only need the last row for prediction, but we need history for indicators
        df = self.feature_engineer.add_technical_indicators(df)
        df = df.dropna() # Drop rows with NaNs (initial rows)
        
        if df.empty:
             return {"status": "error", "message": "Insufficient data for indicators"}

        # Get latest features
        last_row = df.iloc[[-1]]
        feature_cols = ['RSI', 'MACD', 'MACD_Signal', 'SMA_50', 'SMA_200', 'BB_Upper', 'BB_Lower']
        X_new = last_row[feature_cols]

        # 4. Predict
        prediction = model.predict(X_new)[0] # 0 or 1
        probability = model.predict_proba(X_new)[0][1] # Probability of class 1 (UP)

        return {
            "status": "success",
            "symbol": symbol,
            "prediction": "UP" if prediction == 1 else "DOWN",
            "confidence": round(probability * 100, 2),
            "features": X_new.to_dict(orient='records')[0]
        }
