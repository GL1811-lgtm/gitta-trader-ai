"""
Market movers API endpoint - Top Gainers, Losers, Volume Shockers
"""
from flask import Blueprint, request, jsonify
from backend.data.tickers import NIFTY_50_TICKERS, NIFTY_500_TICKERS
from backend.database.db import db
from datetime import datetime

movers_bp = Blueprint('movers', __name__)

@movers_bp.route('', methods=['GET'])
def get_market_movers():
    """
    Get top market movers (gainers, losers, volume shockers) from real database.
    Query param: index (NIFTY 50, NIFTY 100, NIFTY 500)
    """
    try:
        index_param = request.args.get('index', 'NIFTY 100')
        
        # Select stock universe
        if 'NIFTY 50' in index_param:
            stock_list = NIFTY_50_TICKERS
        else:
            stock_list = NIFTY_500_TICKERS[:100]  # Limit to 100 for performance
        
        # Fetch real data from database
        all_stocks = []
        for ticker in stock_list:
            symbol = ticker.replace('.NS', '').replace('.BO', '')
            data = db.get_latest_market_data(symbol)
            
            if data:
                change = data['close'] - data['open']
                change_percent = (change / data['open']) * 100 if data['open'] else 0
                all_stocks.append({
                    'symbol': symbol,
                    'name': symbol.replace('_', ' ').title(),
                    'price': round(data['close'], 2),
                    'change': round(change, 2),
                    'changePercent': round(change_percent, 2),
                    'volume': data.get('volume', 0)
                })
        
        # Sort for gainers (highest % change - positive only)
        gainers = sorted([s for s in all_stocks if s['changePercent'] > 0], 
                        key=lambda x: x['changePercent'], reverse=True)[:5]
        
        # Sort for losers (lowest % change - negative only)
        losers = sorted([s for s in all_stocks if s['changePercent'] < 0], 
                       key=lambda x: x['changePercent'])[:5]
        
        # Sort by volume
        volume_shockers = sorted(all_stocks, key=lambda x: x['volume'], reverse=True)[:5]
        
        # Remove volume from response for gainers/losers
        for stock_list in [gainers, losers]:
            for stock in stock_list:
                stock.pop('volume', None)
        
        return jsonify({
            'gainers': gainers,
            'losers': losers,
            'volumeShockers': volume_shockers,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }), 200
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error in market movers: {e}")
        return jsonify({
            'gainers': [],
            'losers': [],
            'volumeShockers': [],
            'error': str(e)
        }), 500
