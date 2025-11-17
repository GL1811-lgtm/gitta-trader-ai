try:
    import pandas as pd
    import numpy as np
except ImportError:
    # Fallback if pandas/numpy is not installed
    pd = None
    np = None

def _calculate_rsi(data, window=14):
    """
    Calculate the Relative Strength Index (RSI) manually.
    """
    if pd is None or data is None:
        return 50  # Return a neutral value if library/data is missing

    close_prices = data['Close']
    delta = close_prices.diff()

    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()

    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    # Return the last value of the series, which is the current RSI
    return rsi.iloc[-1]

def predict_signal(df):
    """
    Predicts a trading signal based on MA and RSI indicators.

    Args:
        df (pd.DataFrame): DataFrame with OHLCV data, must include a 'Close' column.

    Returns:
        dict: A dictionary containing the signal, confidence, and reason.
    """
    if pd is None or df is None or df.empty:
        return {
            "signal": "HOLD",
            "confidence": 0.5,
            "reason": "Data not available or pandas not installed."
        }

    # 1. Calculate Indicators
    ma9 = df['Close'].rolling(window=9).mean().iloc[-1]
    ma21 = df['Close'].rolling(window=21).mean().iloc[-1]
    rsi = _calculate_rsi(df, window=14)

    # 2. Decision Logic
    signal = "HOLD"
    confidence = 0.5
    reason = "Neither BUY nor SELL conditions were met."

    if ma9 > ma21 and rsi > 55:
        signal = "BUY"
        confidence = min(0.7 + (rsi - 55) / 100, 0.95) # Confidence increases with RSI
        reason = f"MA9 ({ma9:.2f}) > MA21 ({ma21:.2f}) and RSI ({rsi:.2f}) > 55."
    elif ma9 < ma21 and rsi < 45:
        signal = "SELL"
        confidence = min(0.7 + (45 - rsi) / 100, 0.95) # Confidence increases as RSI drops
        reason = f"MA9 ({ma9:.2f}) < MA21 ({ma21:.2f}) and RSI ({rsi:.2f}) < 45."

    return {
        "signal": signal,
        "confidence": round(confidence, 2),
        "reason": reason
    }
