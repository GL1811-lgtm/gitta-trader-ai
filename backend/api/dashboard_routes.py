"""
Dashboard features API - Trading Screens, News, Ticker
"""
from flask import Blueprint, jsonify
import random
from datetime import datetime, timedelta
from backend.database.db import db
from backend.utils.angel_one_helper import angel_helper
from backend.data.tickers import NIFTY_50_TICKERS

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/screens', methods=['GET'])
def get_trading_screens():
    """Get technical analysis screeners."""
    # TODO: Implement real technical analysis using TA-Lib or pandas-ta on DB data
    # Returning 0 counts to avoid showing dummy data
    screens = [
        {'id': '1', 'name': 'Resistance breakouts', 'type': 'Bullish', 'count': 0},
        {'id': '2', 'name': 'MACD above signal line', 'type': 'Bullish', 'count': 0},
        {'id': '3', 'name': 'RSI overbought', 'type': 'Bearish', 'count': 0},
        {'id': '4', 'name': 'RSI oversold', 'type': 'Bullish', 'count': 0},
        {'id': '5', 'name': 'Support breakdowns', 'type': 'Bearish', 'count': 0},
        {'id': '6', 'name': 'Golden cross', 'type': 'Bullish', 'count': 0},
    ]
    return jsonify({'screens': screens}), 200

@dashboard_bp.route('/news', methods=['GET'])
def get_stocks_news():
    """Get stocks in news today."""
    # TODO: Integrate with a real News API (e.g., NewsAPI.org, Google News)
    # Returning empty list to avoid showing dummy/fake news
    news = []
    return jsonify({'news': news}), 200

@dashboard_bp.route('/ticker', methods=['GET'])
def get_ticker_indices():
    """Get live ticker bar indices from Angel One API."""
    try:
        indices = []
        
        # Get NIFTY 50 from database (collected by NSEDataCollector)
        nifty = db.get_latest_market_data("NIFTY")
        if nifty:
            change = nifty['close'] - nifty['open']
            change_percent = (change / nifty['open']) * 100 if nifty['open'] else 0
            indices.append({
                'name': 'NIFTY',
                'value': round(nifty['close'], 2),
                'change': round(change, 2),
                'changePercent': round(change_percent, 2)
            })
        
        # Get SENSEX (Try Angel One Helper directly if not in DB)
        # Token for SENSEX is 99919000 on BSE
        try:
            sensex_data = angel_helper.get_market_data("BSE", "99919000", "SENSEX")
            if sensex_data:
                ltp = float(sensex_data.get('ltp', sensex_data.get('close', 0)))
                open_price = float(sensex_data.get('open', ltp))
                change = ltp - open_price
                change_percent = (change / open_price) * 100 if open_price else 0
                indices.append({
                    'name': 'SENSEX',
                    'value': round(ltp, 2),
                    'change': round(change, 2),
                    'changePercent': round(change_percent, 2)
                })
        except Exception as e:
            # Skip SENSEX if Angel One API fails
            pass
        
        # Get BANKNIFTY from database
        bn = db.get_latest_market_data("BANKNIFTY")
        if bn:
            change = bn['close'] - bn['open']
            change_percent = (change / bn['open']) * 100 if bn['open'] else 0
            indices.append({
                'name': 'BANKNIFTY',
                'value': round(bn['close'], 2),
                'change': round(change, 2),
                'changePercent': round(change_percent, 2)
            })
        
        # Add MIDCPNIFTY and FINNIFTY from DB if available
        for symbol, name in [('MIDCPNIFTY', 'MIDCPNIFTY'), ('FINNIFTY', 'FINNIFTY')]:
            data = db.get_latest_market_data(symbol)
            if data:
                change = data['close'] - data['open']
                change_percent = (change / data['open']) * 100 if data['open'] else 0
                indices.append({
                    'name': name,
                    'value': round(data['close'], 2),
                    'change': round(change, 2),
                    'changePercent': round(change_percent, 2)
                })
        
        # If no data, return empty (frontend will handle)
        if not indices:
            return jsonify({'indices': [], 'error': 'No data available yet. Run continuous agents.'}), 200
        
        return jsonify({'indices': indices}), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error in ticker: {e}")
        return jsonify({'indices': [], 'error': str(e)}), 500

@dashboard_bp.route('/most-traded', methods=['GET'])
def get_most_traded():
    """Get most traded stocks from database (sorted by volume)."""
    try:
        # Get latest data for NIFTY 50 stocks from database
        stocks = []
        for ticker in NIFTY_50_TICKERS[:20]:  # Check first 20 for performance
            symbol = ticker.replace('.NS', '').replace('.BO', '')
            data = db.get_latest_market_data(symbol)
            
            if data and data.get('volume', 0) > 0:
                change = data['close'] - data['open']
                change_percent = (change / data['open']) * 100 if data['open'] else 0
                stocks.append({
                    'symbol': symbol,
                    'name': symbol.replace('_', ' ').title(),
                    'price': round(data['close'], 2),
                    'change': round(change, 2),
                    'changePercent': round(change_percent, 2),
                    'volume': data.get('volume', 0)
                })
        
        # Sort by volume descending and take top 8
        stocks.sort(key=lambda x: x['volume'], reverse=True)
        top_stocks = stocks[:8]
        
        # Remove volume from response (not needed in frontend)
        for stock in top_stocks:
            stock.pop('volume', None)
        
        # If no real data, return placeholder message
        if not top_stocks:
            return jsonify({
                'stocks': [],
                'message': 'No data available. Please run continuous agents to collect data.'
            }), 200
        
        return jsonify({'stocks': top_stocks}), 200
        
    except Exception as e:
        print(f"Error fetching most traded: {e}")
        return jsonify({'stocks': []}), 500

@dashboard_bp.route('/all-indices', methods=['GET'])
def get_all_indices():
    """Get all market indices (Indian and Global) from real database."""
    try:
        # Indian Indices
        indian_indices = []
        # Map of display name to DB symbol
        indian_symbols = [
            ("NIFTY 50", "NIFTY"),
            ("BANKNIFTY", "BANKNIFTY"),
            ("FINNIFTY", "FINNIFTY"),
            ("MIDCPNIFTY", "MIDCPNIFTY"),
            ("NIFTY NEXT 50", "NIFTYNXT50"),
            ("INDIA VIX", "INDIAVIX"),
            ("SENSEX", "SENSEX"),
            ("BANKEX", "BANKNEX")
        ]
        
        for name, symbol in indian_symbols:
            # Try Angel One Helper for SENSEX/BANKNEX if not in DB
            if symbol in ["SENSEX", "BANKNEX"]:
                data = angel_helper.get_market_data("BSE", "1" if symbol == "SENSEX" else "12", symbol) # Tokens need verification
                # Fallback to DB if helper fails or for others
            else:
                data = None
            
            if not data:
                data = db.get_latest_market_data(symbol)
            
            if data:
                change = data['close'] - data['open']
                change_percent = (change / data['open']) * 100 if data['open'] else 0
                indian_indices.append({
                    'name': name,
                    'symbol': symbol,
                    'ltp': round(data['close'], 2),
                    'ltpChng': round(change, 2),
                    'ltpChngPercent': round(change_percent, 2),
                    'open': round(data['open'], 2),
                    'high': round(data['high'], 2),
                    'low': round(data['low'], 2),
                    'close': round(data['close'], 2)
                })

        # Global Indices
        # Currently we don't have a real source for Global Indices in Angel One API (NSE/BSE only)
        # Returning empty list to avoid dummy data as requested
        global_indices = []
        
        return jsonify({
            'indianIndices': indian_indices,
            'globalIndices': global_indices
        }), 200
        
    except Exception as e:
        print(f"Error fetching all indices: {e}")
        return jsonify({'indianIndices': [], 'globalIndices': [], 'error': str(e)}), 500

