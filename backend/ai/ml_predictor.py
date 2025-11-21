import numpy as np
from typing import Dict, List, Optional
from datetime import datetime

try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

from backend.utils.logger import logger

class MLPredictor:
    """
    Machine learning predictor for short-term price direction.
    Uses Random Forest on technical indicators.
    """
    
    def __init__(self):
        if not SKLEARN_AVAILABLE:
            logger.warning("scikit-learn not available. Install with: pip install scikit-learn")
        
        self.model = None
        self.scaler = None
        self.trained = False
        
        if SKLEARN_AVAILABLE:
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            self.scaler = StandardScaler()
    
    def prepare_features(self, indicator_data: Dict) -> np.ndarray:
        """
        Prepare feature vector from technical indicators.
        Expected indicators: RSI, MACD, BB_upper, BB_lower, Volume, etc.
        """
        features = []
        
        # Extract features in consistent order
        features.append(indicator_data.get('rsi', 50))
        features.append(indicator_data.get('macd', 0))
        features.append(indicator_data.get('macd_signal', 0))
        features.append(indicator_data.get('bb_position', 0.5))  # (price - BB_lower) / (BB_upper - BB_lower)
        features.append(indicator_data.get('volume_ratio', 1.0))  # current_volume / avg_volume
        features.append(indicator_data.get('price_change_pct', 0))
        features.append(indicator_data.get('sma_20', 0))
        features.append(indicator_data.get('sma_50', 0))
        
        return np.array(features).reshape(1, -1)
    
    def train(self, historical_data: List[Dict], labels: List[int]) -> Dict:
        """
        Train the ML model on historical data.
        
        historical_data: List of indicator dictionaries
        labels: List of labels (1 = up, 0 = down/sideways)
        
        Returns training metrics
        """
        if not SKLEARN_AVAILABLE:
            return {'error': 'scikit-learn not available'}
        
        if len(historical_data) < 100:
            return {'error': 'Insufficient training data (need at least 100 samples)'}
        
        try:
            # Prepare features
            X = np.array([list(self.prepare_features(d).flatten()) for d in historical_data])
            y = np.array(labels)
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X)
            
            # Train model
            self.model.fit(X_scaled, y)
            self.trained = True
            
            # Calculate training accuracy
            train_score = self.model.score(X_scaled, y)
            
            # Feature importance
            feature_names = ['RSI', 'MACD', 'MACD_Signal', 'BB_Position', 
                           'Volume_Ratio', 'Price_Change', 'SMA_20', 'SMA_50']
            importances = self.model.feature_importances_
            
            feature_importance = {
                name: round(imp, 3) 
                for name, imp in zip(feature_names, importances)
            }
            
            return {
                'success': True,
                'training_samples': len(historical_data),
                'training_accuracy': round(train_score, 3),
                'feature_importance': feature_importance,
                'trained_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Model training failed: {e}")
            return {'error': str(e)}
    
    def predict(self, indicator_data: Dict) -> Dict:
        """
        Predict price direction for next period.
        
        Returns: {
            'prediction': 'up' or 'down',
            'confidence': float (0 to 1),
            'probabilities': {'up': float, 'down': float}
        }
        """
        if not SKLEARN_AVAILABLE:
            return {'prediction': 'neutral', 'confidence': 0.5}
        
        if not self.trained:
            return {'prediction': 'neutral', 'confidence': 0.5, 'error': 'Model not trained'}
        
        try:
            # Prepare and scale features
            X = self.prepare_features(indicator_data)
            X_scaled = self.scaler.transform(X)
            
            # Get prediction and probabilities
            prediction = self.model.predict(X_scaled)[0]
            probabilities = self.model.predict_proba(X_scaled)[0]
            
            # Map to up/down
            if prediction == 1:
                pred_label = 'up'
                confidence = probabilities[1]
            else:
                pred_label = 'down'
                confidence = probabilities[0]
            
            return {
                'prediction': pred_label,
                'confidence': round(confidence, 3),
                'probabilities': {
                    'down': round(probabilities[0], 3),
                    'up': round(probabilities[1], 3)
                },
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return {'prediction': 'neutral', 'confidence': 0.5, 'error': str(e)}
