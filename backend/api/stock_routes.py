"""
Stock search and price endpoints for minimal server
"""
import os
from flask import Blueprint, request, jsonify
from backend.data.tickers import NIFTY_50_TICKERS, NIFTY_500_TICKERS
from datetime import datetime
from backend.database.db import db

stock_bp = Blueprint('stocks', __name__)

# Combine all stocks for search
ALL_STOCKS = NIFTY_500_TICKERS

@stock_bp.route('/search', methods=['GET'])
def search_stocks():
    """
    Search stocks by symbol or name
    Query param: q (search query)
    """
    query = request.args.get('q', '').strip().upper()
    
    if len(query) < 2:
        return jsonify({'results': []}), 200
    
    # Search in stock list
    results = []
    for stock in ALL_STOCKS:
        symbol = stock.replace('.NS', '').replace('.BO', '')
        # Match symbol or partial match
        if query in symbol:
            results.append({
                'symbol': symbol,
                'name': symbol,  # In real implementation, fetch company name
                'exchange': 'NSE',
                'fullSymbol': stock
            })
    
    # Limit results
    results = results[:20]
    
    return jsonify({'results': results}), 200

@stock_bp.route('/price/<symbol>', methods=['GET'])
def get_stock_price(symbol):
    """Get real-time stock price from Angel One (via DB)."""
    try:
        # Clean symbol
        clean_symbol = symbol.replace('.NS', '').replace('.BO', '')
        
        # Try fetching from DB first (fastest)
        data = db.get_latest_market_data(clean_symbol)
        
        # If not in DB, return 404
        if not data:
            return jsonify({'error': 'Stock data not found. Add to watchlist to start tracking.'}), 404
            
        change = data['close'] - data['open']
        change_percent = (change / data['open']) * 100 if data['open'] else 0
        
        return jsonify({
            'symbol': clean_symbol,
            'price': round(data['close'], 2),
            'change': round(change, 2),
            'changePercent': round(change_percent, 2),
            'open': round(data['open'], 2),
            'high': round(data['high'], 2),
            'low': round(data['low'], 2),
            'prevClose': round(data['open'], 2), # Approx
            'volume': data.get('volume', 0),
            'timestamp': datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        print(f"Error fetching stock price: {e}")
        return jsonify({'error': str(e)}), 500

@stock_bp.route('/history/<symbol>', methods=['GET'])
def get_stock_history(symbol):
    """Get historical data for a stock (mocked for now until DB has history)."""
    try:
        clean_symbol = symbol.replace('.NS', '').replace('.BO', '')
        
        # In a real implementation, query the 'market_data' table with timeframe
        # For now, generate realistic looking intraday data based on current price
        
        current_data = db.get_latest_market_data(clean_symbol)
        base_price = current_data['close'] if current_data else 1000.0
        
        history = []
        import random
        import math
        
        # Generate 50 points (e.g. 15 min intervals)
        price = base_price * 0.98 # Start slightly lower
        
        for i in range(50):
            # Random walk
            change = (random.random() - 0.45) * (base_price * 0.005)
            price += change
            
            history.append({
                'time': f"{9 + (i * 15 // 60)}:{(i * 15) % 60:02d}",
                'open': price,
                'high': price * (1 + random.random() * 0.001),
                'low': price * (1 - random.random() * 0.001),
                'close': price * (1 + (random.random() - 0.5) * 0.001)
            })
            
        return jsonify(history), 200
        
    except Exception as e:
        print(f"Error fetching history: {e}")
        return jsonify([]), 500
