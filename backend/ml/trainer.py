import os
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from backend.data_providers.manager import DataProviderManager
from backend.ml.feature_engineering import FeatureEngineer
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelTrainer:
    def __init__(self):
        self.data_provider = DataProviderManager()
        self.feature_engineer = FeatureEngineer()
        self.models_dir = "backend/ml/models"
        os.makedirs(self.models_dir, exist_ok=True)

    def train_model(self, symbol):
        """
        Fetches data, engineers features, trains model, and saves it.
        """
        logger.info(f"Starting training for {symbol}...")
        
        # 1. Fetch Historical Data (Max available)
        df = self.data_provider.get_historical_data(symbol, period="5y", interval="1d")
        if df is None or df.empty:
            logger.error(f"No data found for {symbol}")
            return {"status": "error", "message": "No data found"}

        # 2. Prepare Dataset
        X, y = self.feature_engineer.prepare_data(df)
        if X is None or len(X) < 100:
             logger.error(f"Insufficient data for {symbol}")
             return {"status": "error", "message": "Insufficient data"}

        # 3. Split Data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

        # 4. Train Random Forest
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # 5. Evaluate
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        
        logger.info(f"Model trained. Accuracy: {accuracy:.2f}")

        # 6. Save Model
        model_path = os.path.join(self.models_dir, f"{symbol}_rf.joblib")
        joblib.dump(model, model_path)
        
        return {
            "status": "success",
            "accuracy": accuracy,
            "report": report,
            "model_path": model_path
        }
