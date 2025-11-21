import pandas as pd
import numpy as np

class FeatureEngineer:
    """
    Generates technical indicators for ML models.
    """
    
    def prepare_data(self, df):
        """
        Takes a DataFrame with 'Close' prices and returns X (features) and y (target).
        """
        if df is None or df.empty:
            return None, None

        df = df.copy()
        
        # 1. Add Technical Indicators
        df = self.add_technical_indicators(df)
        
        # 2. Create Target Variable
        # Target: 1 if Close price 5 days later is higher than today, else 0
        df['Target'] = (df['Close'].shift(-5) > df['Close']).astype(int)
        
        # 3. Drop NaNs created by indicators and shifting
        df = df.dropna()
        
        # 4. Select Features
        feature_cols = ['RSI', 'MACD', 'MACD_Signal', 'SMA_50', 'SMA_200', 'BB_Upper', 'BB_Lower']
        X = df[feature_cols]
        y = df['Target']
        
        return X, y

    def add_technical_indicators(self, df):
        """
        Calculates RSI, MACD, SMA, Bollinger Bands.
        """
        close = df['Close']
        
        # RSI (14)
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # MACD (12, 26, 9)
        exp1 = close.ewm(span=12, adjust=False).mean()
        exp2 = close.ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        
        # SMA (50, 200)
        df['SMA_50'] = close.rolling(window=50).mean()
        df['SMA_200'] = close.rolling(window=200).mean()
        
        # Bollinger Bands (20)
        sma20 = close.rolling(window=20).mean()
        std20 = close.rolling(window=20).std()
        df['BB_Upper'] = sma20 + (std20 * 2)
        df['BB_Lower'] = sma20 - (std20 * 2)
        
        return df
