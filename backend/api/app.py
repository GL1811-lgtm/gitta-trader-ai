from flask import Flask, jsonify
import sys
import os
import pandas as pd

# Adjust path to import from parent directories
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.collectors.fetcher import fetch_latest
from backend.predictor.predictor import predict_signal

app = Flask(__name__)

@app.route('/predict/<symbol>', methods=['GET'])
def get_prediction(symbol):
    """
    Fetches data for a symbol, runs the predictor, and returns the trading signal.
    """
    if not symbol:
        return jsonify({"error": "Symbol cannot be empty"}), 400

    try:
        # 1. Fetch data
        ohlcv_data = fetch_latest(symbol)
        if ohlcv_data.empty:
            return jsonify({"error": f"No data found for symbol: {symbol}"}), 404

        # 2. Get prediction
        prediction = predict_signal(ohlcv_data)
        if not prediction:
            return jsonify({"error": "Prediction failed"}), 500

        # 3. Format response
        response = {
            "symbol": symbol.upper(),
            "signal": prediction.get("signal"),
            "confidence": prediction.get("confidence"),
            "reason": prediction.get("reason")
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    # This allows running the app directly for testing
    port = int(os.environ.get('PORT', '5001'))
    app.run(host='0.0.0.0', port=port, debug=True)