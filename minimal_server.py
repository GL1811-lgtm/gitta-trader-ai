"""
Minimal Flask server to test market data endpoint in isolation.
This helps identify if the crash is due to app.py complexity or a fundamental issue.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

sys.path.insert(0, '.')

from flask import Flask, jsonify
from flask_cors import CORS
from backend.database.db import db
from backend.api.stock_routes import stock_bp
from backend.api.movers_routes import movers_bp
from backend.api.dashboard_routes import dashboard_bp

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "http://localhost:5173"]}})

# Register blueprints
app.register_blueprint(stock_bp, url_prefix='/api/stocks')
app.register_blueprint(movers_bp, url_prefix='/api/market/movers')
app.register_blueprint(dashboard_bp, url_prefix='/api/market')

@app.route('/api/market/indices', methods=['GET'])
def get_market_indices():
    """Get live market indices data."""
    try:
        indices = []
        
        # Fetch NIFTY 50
        nifty = db.get_latest_market_data("NIFTY")
        if nifty:
            change = nifty['close'] - nifty['open']
            change_percent = (change / nifty['open']) * 100 if nifty['open'] else 0
            indices.append({
                "name": "NIFTY 50",
                "value": nifty['close'],
                "change": change,
                "changePercent": change_percent
            })
            
        # Fetch BANKNIFTY
        bn = db.get_latest_market_data("BANKNIFTY")
        if bn:
            change = bn['close'] - bn['open']
            change_percent = (change / bn['open']) * 100 if bn['open'] else 0
            indices.append({
                "name": "BANKNIFTY",
                "value": bn['close'],
                "change": change,
                "changePercent": change_percent
            })
            
        # If no data in DB yet, return zero values
        if not indices:
             return jsonify([
                {"name": "NIFTY 50", "value": 0, "change": 0, "changePercent": 0},
                {"name": "BANKNIFTY", "value": 0, "change": 0, "changePercent": 0}
             ]), 200
             
        return jsonify(indices), 200
    except Exception as e:
        print(f"Error fetching market indices: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok", "message": "Minimal server running"}), 200

if __name__ == '__main__':
    print("Starting minimal Flask server on port 5000...")
    app.run(host='0.0.0.0', port=5000, debug=True)
