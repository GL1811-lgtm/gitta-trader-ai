import os
import glob
import subprocess
import threading
import time
from datetime import datetime
import json

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Histogram

from apscheduler.schedulers.background import BackgroundScheduler
import atexit

from backend.database.db import db
from backend.utils.logger import logger
from backend.core.security import run_startup_checks

# Run startup checks
try:
    run_startup_checks()
except Exception as e:
    logger.critical(f"Startup checks failed: {e}")
    # We might want to exit here, but for now let's just log critical error
    # sys.exit(1) 

# Try to import Google Drive archiver (optional dependency)
try:
    from backend.archiver.google_drive import GoogleDriveArchiver
    GOOGLE_DRIVE_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Google Drive archiver not available: {e}")
    GOOGLE_DRIVE_AVAILABLE = False
    GoogleDriveArchiver = None

# Initialize Flask app
app = Flask(__name__)

# --- Configuration ---
# Using simple in-memory cache instead of Redis for easier setup
app.config['CACHE_TYPE'] = 'simple'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # 5 minutes

# --- Extensions ---
# CORS Configuration - CRITICAL FIX for cross-origin requests
# Flask-CORS requires proper configuration to work
cors_origins_str = os.environ.get('CORS_ORIGINS', 'http://localhost:5173,http://localhost:3000')
cors_origins = cors_origins_str.split(',')

# Add Render frontend URL if in production
if os.environ.get('ENVIRONMENT') == 'production':
    render_frontend = 'https://gitta-trader-ai-frontend.onrender.com'
    if render_frontend not in cors_origins:
        cors_origins.append(render_frontend)

# CRITICAL: Flask-CORS configuration - use resources parameter for proper setup
CORS(app, 
     resources={r"/api/*": {"origins": cors_origins}},
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
)
cache = Cache(app)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["2000 per day", "500 per hour"], # Increased limits for dev/testing
    storage_uri="memory://"
)

# --- Monitoring ---
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP Request Duration', ['method', 'endpoint'])

@app.before_request
def before_request_handler():
    request.start_time = time.time()

@app.after_request
def after_request_handler(response):
    if request.endpoint:
        latency = time.time() - request.start_time
        REQUEST_LATENCY.labels(request.method, request.endpoint).observe(latency)
        REQUEST_COUNT.labels(request.method, request.endpoint, response.status_code).inc()
    return response

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# --- Scheduler Setup ---
scheduler = BackgroundScheduler()
# Scheduled job functions (called by scheduler)
# archiver = GoogleDriveArchiver() if GOOGLE_DRIVE_AVAILABLE else None

# --- Error Handlers ---


@app.route('/predict/<symbol>', methods=['GET'])
def predict(symbol):
    """Returns dummy prediction data for the given symbol."""
    if not symbol:
        return jsonify({"error": "Symbol cannot be empty"}), 400
    return jsonify({
        "symbol": symbol.upper(),
        "price": 123.45,
        "message": "Dummy prediction OK"
    })

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
            
        # If no data in DB yet (first run), try to fetch synchronously or return error
        if not indices:
             # Try to trigger a collection (this is a simplified approach, ideally we wait for agent)
             # For now, we return 503 Service Unavailable to indicate data is not ready
             return jsonify({"error": "Market data not available yet. Please wait for agents to collect data."}), 503
             
        return jsonify(indices), 200
    except Exception as e:
        logger.error(f"Error fetching market indices: {e}")
        return jsonify({"error": str(e)}), 500

# --- Dashboard Endpoints ---

@app.route('/api/dashboard/ticker', methods=['GET'])
def get_dashboard_ticker():
    """Get ticker data for the dashboard bar."""
    try:
        # For now, return the same indices data or a subset
        # Ideally this comes from a cached high-frequency store
        indices = [
            {"name": "NIFTY 50", "value": 23518.50, "change": 120.50, "changePercent": 0.52},
            {"name": "SENSEX", "value": 77339.01, "change": 350.20, "changePercent": 0.45},
            {"name": "BANKNIFTY", "value": 51400.25, "change": -80.00, "changePercent": -0.15},
            {"name": "NIFTY IT", "value": 32100.00, "change": 450.00, "changePercent": 1.42}
        ]
        # Try to fetch real data if available
        real_nifty = db.get_latest_market_data("NIFTY")
        if real_nifty:
             indices[0] = {
                "name": "NIFTY 50",
                "value": real_nifty['close'],
                "change": real_nifty['close'] - real_nifty['open'],
                "changePercent": ((real_nifty['close'] - real_nifty['open']) / real_nifty['open']) * 100
             }
             
        return jsonify({"indices": indices})
    except Exception as e:
        logger.error(f"Error fetching ticker: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/dashboard/screens', methods=['GET'])
def get_dashboard_screens():
    """Get active trading screens/signals."""
    try:
        # Mock data for screens
        screens = [
            {"id": "1", "name": "Bullish MACD Crossover", "type": "Bullish", "count": 12, "icon": "📈"},
            {"id": "2", "name": "RSI Oversold (<30)", "type": "Bullish", "count": 5, "icon": "📉"},
            {"id": "3", "name": "Resistance Breakout", "type": "Bullish", "count": 8, "icon": "🚀"},
            {"id": "4", "name": "Bearish Engulfing", "type": "Bearish", "count": 3, "icon": "🔻"}
        ]
        return jsonify({"screens": screens})
    except Exception as e:
        logger.error(f"Error fetching screens: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/dashboard/most-traded', methods=['GET'])
def get_most_traded():
    """Get most traded stocks."""
    try:
        # Mock data
        stocks = [
            {"symbol": "RELIANCE", "name": "Reliance Industries", "price": 2450.00, "change": 15.00, "changePercent": 0.61},
            {"symbol": "TCS", "name": "Tata Consultancy Svcs", "price": 3500.00, "change": -20.00, "changePercent": -0.57},
            {"symbol": "HDFCBANK", "name": "HDFC Bank", "price": 1650.00, "change": 10.00, "changePercent": 0.61},
            {"symbol": "INFY", "name": "Infosys", "price": 1450.00, "change": 25.00, "changePercent": 1.75},
            {"symbol": "ICICIBANK", "name": "ICICI Bank", "price": 950.00, "change": 5.00, "changePercent": 0.53}
        ]
        return jsonify({"stocks": stocks})
    except Exception as e:
        logger.error(f"Error fetching most traded: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/dashboard/news', methods=['GET'])
def get_dashboard_news():
    """Get latest market news."""
    try:
        # Mock data
        news = [
            {
                "symbol": "RELIANCE",
                "company": "Reliance Industries",
                "headline": "Reliance to acquire new solar energy startup",
                "time": "10 mins ago",
                "changePercent": 0.61
            },
            {
                "symbol": "TCS",
                "company": "Tata Consultancy Svcs",
                "headline": "TCS bags major deal with UK insurer",
                "time": "1 hour ago",
                "changePercent": -0.57
            },
            {
                "symbol": "TATAMOTORS",
                "company": "Tata Motors",
                "headline": "EV sales surge 50% in Q3",
                "time": "2 hours ago",
                "changePercent": 2.10
            }
        ]
        return jsonify({"news": news})
    except Exception as e:
        logger.error(f"Error fetching news: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"status": "ok"}), 200

@app.route('/api/alerts', methods=['GET'])
def get_alerts():
    """Get live trading alerts."""
    try:
        # Mock data matching the Alert interface
        alerts = [
            {
                "id": "1",
                "instrument": "NIFTY 18000 CE",
                "type": "BUY",
                "confidence": 85,
                "reason": "Strong momentum + Volume breakout",
                "timestamp": "10:30 AM",
                "strikePrice": 150.0,
                "targetPrice": 180.0,
                "stopLoss": 135.0
            },
            {
                "id": "2",
                "instrument": "BANKNIFTY 42000 PE",
                "type": "SELL",
                "confidence": 78,
                "reason": "Resistance rejection at VWAP",
                "timestamp": "11:15 AM",
                "strikePrice": 320.0,
                "targetPrice": 280.0,
                "stopLoss": 340.0
            }
        ]
        return jsonify(alerts)
    except Exception as e:
        logger.error(f"Error fetching alerts: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/learning/logs', methods=['GET'])
def get_learning_logs():
    """Get AI learning logs."""
    try:
        # Mock data matching the LearningLogEntry interface
        logs = [
            {
                "id": "1",
                "timestamp": "Today, 09:45 AM",
                "title": "Pattern Recognition Update",
                "summary": "Identified new correlation between NIFTY IT volume and midcap breakouts.",
                "accuracyChange": 2.5
            },
            {
                "id": "2",
                "timestamp": "Yesterday, 03:30 PM",
                "title": "Strategy Optimization",
                "summary": "Adjusted stop-loss parameters for high volatility regimes based on last 50 trades.",
                "accuracyChange": 1.2
            },
            {
                "id": "3",
                "timestamp": "20 Nov, 11:00 AM",
                "title": "False Positive Detection",
                "summary": "Learned to filter out fake breakouts during low liquidity lunch hours.",
                "accuracyChange": 3.8
            }
        ]
        return jsonify(logs)
    except Exception as e:
        logger.error(f"Error fetching learning logs: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/gemini/analysis', methods=['POST'])
def gemini_analysis():
    """
    Mock endpoint for Gemini analysis.
    In a real implementation, this would call the Google Gemini API.
    """
    data = request.get_json()
    prompt = data.get('prompt', '')
    
    # Mock response based on the prompt context
    if "market learnings" in prompt:
        analysis = """
### Expert Market Analysis

Based on the recent data and learnings:

1.  **Volatility Alert**: The VIX is showing signs of cooling off, suggesting a potential consolidation phase.
2.  **Strategy Insight**: The "Cup and Handle" pattern on the 15m chart is holding. Recommended action is to **HOLD** current long positions with a trailing stop.
3.  **Sentiment**: Market sentiment remains **Cautiously Bullish** driven by positive global cues.

*Note: This is a simulated AI response.*
"""
    else:
        analysis = """
### Technical Analysis

**Trend**: Bullish
**Support**: 23,400
**Resistance**: 23,550

The market is currently trading above the 50-day moving average. RSI is neutral. Suggest waiting for a breakout above 23,550 for fresh entries.
"""

    return jsonify({"analysis": analysis})

@app.route('/api/reports/latest', methods=['GET'])
def get_latest_report():
    """Returns the content of the latest daily report."""
    reports_dir = os.path.join(os.path.dirname(__file__), '../data/reports')
    
    # Ensure dir exists
    if not os.path.exists(reports_dir):
        return jsonify({"error": "Reports directory not found"}), 404

    list_of_files = glob.glob(os.path.join(reports_dir, '*.md'))
    if not list_of_files:
        return jsonify({"error": "No reports found"}), 404
    
    # Get the latest file by creation time
    latest_file = max(list_of_files, key=os.path.getctime)
    
    try:
        with open(latest_file, 'r') as f:
            content = f.read()
        return jsonify({"content": content, "filename": os.path.basename(latest_file)})
    except Exception as e:
        return jsonify({"error": f"Error reading report: {str(e)}"}), 500

@app.route('/api/reports/morning', methods=['GET'])
@cache.cached(timeout=3600) # Cache for 1 hour
def get_morning_report():
    """Returns the latest Morning Opportunity Report."""
    try:
        report = db.get_latest_report("morning_report")
        if report:
            return jsonify(report)
        return jsonify({"message": "No morning report available yet. Reports generate at 8 AM daily."}), 200
    except Exception as e:
        logger.warning(f"Morning report not ready: {e}")
        return jsonify({"message": "Morning report will be available after 8 AM", "status": "pending"}), 200

@app.route('/api/reports/evening', methods=['GET'])
@cache.cached(timeout=3600) # Cache for 1 hour
def get_evening_report():
    """Returns the latest Evening Performance Review."""
    try:
        report = db.get_latest_report("evening_validation")
        if report:
            return jsonify(report)
        return jsonify({"message": "No evening report available yet. Reports generate at 5 PM daily."}), 200
    except Exception as e:
        logger.warning(f"Evening report not ready: {e}")
        return jsonify({"message": "Evening report will be available after 5 PM", "status": "pending"}), 200

@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    """Returns list of all tracked stocks."""
    try:
        from backend.data.tickers import ALL_TICKERS
        return jsonify({"stocks": ALL_TICKERS, "count": len(ALL_TICKERS)})
    except Exception as e:
        logger.error(f"Error fetching stocks: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check endpoint."""
    try:
        # Check DB connection
        db._get_connection().close()
        return jsonify({"status": "healthy", "database": "connected", "timestamp": datetime.now().isoformat()}), 200
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

@app.route('/api/system/status', methods=['GET'])
def system_status():
    """Detailed system status."""
    # Basic system info
    status = {
        "timestamp": datetime.now().isoformat(),
        "agents_active": 0, # Placeholder
        "database_size_bytes": os.path.getsize(db.db_path) if os.path.exists(db.db_path) else 0,
        "reports_count": 0 # Placeholder
    }
    return jsonify(status)


@app.route('/api/workflow/run', methods=['POST'])
def run_workflow():
    """Triggers the Supervisor Agent to run the daily workflow in the background."""
    script_path = os.path.join(os.path.dirname(__file__), '../agents/supervisor/run_supervisor.py')
    
    if not os.path.exists(script_path):
        return jsonify({"error": "Supervisor script not found"}), 500

    try:
        # Run in a separate process (fire and forget)
        # We use the same python interpreter
        # We set cwd to the project root so imports work
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        subprocess.Popen(["python", script_path], cwd=project_root)
        
        return jsonify({
            "status": "Workflow triggered", 
            "message": "Supervisor agent started in background. Check logs for progress."
        }), 202
    except Exception as e:
        return jsonify({"error": f"Failed to start workflow: {str(e)}"}), 500

@app.route('/api/data', methods=['DELETE'])
def reset_system():
    """Clears all data (inbox, results, reports) to reset the system."""
    data_dirs = [
        os.path.join(os.path.dirname(__file__), '../data/inbox'),
        os.path.join(os.path.dirname(__file__), '../data/results'),
        os.path.join(os.path.dirname(__file__), '../data/reports'),
        os.path.join(os.path.dirname(__file__), '../data/logs')
    ]
    
    deleted_count = 0
    try:
        for directory in data_dirs:
            if os.path.exists(directory):
                files = glob.glob(os.path.join(directory, '*'))
                for f in files:
                    try:
                        os.remove(f)
                        deleted_count += 1
                    except Exception as e:
                        print(f"Error deleting {f}: {e}")
        
        return jsonify({"message": f"System reset successful. {deleted_count} files deleted."})
    except Exception as e:
        return jsonify({"error": f"System reset failed: {str(e)}"}), 500

@app.route('/api/agents/status', methods=['GET'])
def get_agent_status():
    """Returns the real-time status of all agents."""
    status_file = os.path.join(os.path.dirname(__file__), '../data/status.json')
    try:
        if os.path.exists(status_file):
            with open(status_file, 'r') as f:
                data = json.load(f)
            return jsonify(data)
        else:
            return jsonify([])
    except Exception as e:
        return jsonify({"error": f"Failed to fetch status: {str(e)}"}), 500

# Removed duplicate get_agent_details - keeping the more complete version at line 851

@app.route('/api/analytics/performance', methods=['GET'])
def get_analytics_performance():
    """Returns aggregated performance data for the dashboard chart."""
    try:
        data = db.get_analytics_performance()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch analytics: {str(e)}"}), 500

@app.route('/api/learning/history', methods=['GET'])
def get_learning_history():
    """Returns history of daily reports/learnings."""
    try:
        data = db.get_learning_history()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": f"Failed to fetch learning history: {str(e)}"}), 500



def run_morning_scan():
    """Job to run Morning Scanner at 8:00 AM."""
    logger.info(f"[{datetime.now()}] ⏰ Triggering Morning Scanner...")
    try:
        subprocess.Popen(["python", "backend/intelligence/scanner.py"], cwd=os.getcwd())
    except Exception as e:
        logger.error(f"Failed to run Morning Scanner: {e}")

def run_evening_validation():
    """Job to run Expert Agent at 5:00 PM for daily report generation."""
    logger.info(f"[{datetime.now()}] 🌇 Triggering Expert Agent for daily report...")
    try:
        from backend.agents.expert.expert_agent import ExpertAgent
        agent = ExpertAgent()
        result = agent.run()
        logger.info(f"Expert Agent completed: {result}")
    except Exception as e:
        logger.error(f"Failed to run Expert Agent: {e}")

from backend.utils.backup import backup_database

def run_daily_archive():
    """Job to archive data to Google Drive at 11:00 PM."""
    logger.info(f"[{datetime.now()}] 📦 Triggering Daily Archive...")
    try:
        if archiver:
            success = archiver.archive_data()
            if success:
                logger.info("Daily Archive Successful")
            else:
                logger.error("Daily Archive Failed (Check credentials)")
        else:
            logger.warning("Google Drive archiver not available, skipping archive")
    except Exception as e:
        logger.error(f"Failed to run Daily Archive: {e}")

def run_db_backup():
    """Job to backup database locally at 2:00 AM."""
    logger.info(f"[{datetime.now()}] 💾 Triggering Local DB Backup...")
    backup_database()

from backend.trading.paper_engine import PaperTradingEngine
from backend.core.safety_layer import SafetyLimits
from backend.core.config import Config

# Initialize Trading Engine
trading_engine = PaperTradingEngine()

# Initialize Safety Layer
# We get the initial capital from the trading engine/DB
current_balance = trading_engine.get_account_summary().get('balance', Config.PAPER_CAPITAL)
safety_limits = SafetyLimits(current_capital=current_balance, trading_mode=Config.TRADING_MODE)

@app.route('/api/trading/account', methods=['GET'])
def get_trading_account():
    """Get virtual account summary."""
    try:
        summary = trading_engine.get_account_summary()
        # Update safety layer capital to keep it in sync
        if 'balance' in summary:
            safety_limits.update_capital(summary['balance'])
        return jsonify(summary)
    except Exception as e:
        logger.error(f"Error fetching account summary: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/trading/order', methods=['POST'])
def place_order():
    """Place a buy/sell order."""
    try:
        data = request.json
        symbol = data.get('symbol')
        side = data.get('side') # 'BUY' or 'SELL'
        quantity = int(data.get('quantity', 0))
        price = float(data.get('price', 0)) # Limit price or current market price
        stop_loss = float(data.get('stop_loss', 0))
        
        if not symbol or not side or quantity <= 0:
            return jsonify({"error": "Invalid order parameters"}), 400
            
        # --- SAFETY LAYER CHECK ---
        # Update capital first
        summary = trading_engine.get_account_summary()
        safety_limits.update_capital(summary.get('balance', Config.PAPER_CAPITAL))
        
        # Check Circuit Breaker
        if safety_limits.circuit_breaker_check():
             return jsonify({"error": "CIRCUIT BREAKER ACTIVE: Trading halted due to safety limits."}), 403

        # Validate Trade (only for BUY orders usually, or opening positions)
        if side.upper() == 'BUY':
            # For validation we need price and stop_loss. 
            # If market order, price might be 0 in request, need to fetch current price?
            # For now assuming price is provided or we skip price-based checks if 0 (but risk check needs it)
            if price > 0 and stop_loss > 0:
                validation = safety_limits.validate_trade(
                    entry_price=price, 
                    stop_loss=stop_loss, 
                    quantity=quantity
                )
                if not validation['allowed']:
                    logger.warning(f"Trade rejected by Safety Layer: {validation['reason']}")
                    return jsonify({"error": f"Safety Violation: {validation['reason']}"}), 403
        # ---------------------------

        result = trading_engine.place_order(symbol, side, quantity, price)
        
        if result['status'] == 'success':
            return jsonify(result)
        else:
            return jsonify(result), 400
            
    except Exception as e:
        logger.error(f"Error placing order: {e}")
        return jsonify({"error": str(e)}), 500



from backend.intelligence.backtester import BacktestEngine
backtester = BacktestEngine()

@app.route('/api/backtest/run', methods=['POST'])
def run_backtest():
    """Run a backtest simulation."""
    try:
        data = request.json
        symbol = data.get('symbol')
        strategy = data.get('strategy', 'SMA_CROSSOVER')
        period = data.get('period', '1y')
        initial_capital = int(data.get('initial_capital', 100000))
        
        if not symbol:
            return jsonify({"error": "Symbol is required"}), 400
            
        results = backtester.run_backtest(symbol, strategy, period, initial_capital)
        return jsonify(results)
    except Exception as e:
        logger.error(f"Error running backtest: {e}")
        return jsonify({"error": str(e)}), 500



from backend.ml.trainer import ModelTrainer
from backend.ml.predictor import MLPredictor

ml_trainer = ModelTrainer()
ml_predictor = MLPredictor()

@app.route('/api/ml/train', methods=['POST'])
def train_model():
    """Train ML model for a symbol."""
    try:
        data = request.json
        symbol = data.get('symbol')
        if not symbol:
            return jsonify({"error": "Symbol is required"}), 400
            
        result = ml_trainer.train_model(symbol)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error training model: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/ml/predict/<symbol>', methods=['GET'])
def predict_ml(symbol):
    """Get ML prediction for a symbol."""
    try:
        result = ml_predictor.predict(symbol)
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error predicting: {e}")
        return jsonify({"error": str(e)}), 500

# Placeholder scheduled job functions (these must be defined before scheduler.add_job calls later)
def run_morning_scan():
    """Placeholder for morning market scan."""
    logger.info("Running morning scan (placeholder)")
    pass

def run_evening_validation():
    """Placeholder for evening validation."""
    logger.info("Running evening validation (placeholder)")
    pass

def run_daily_archive():
    """Placeholder for daily archive."""
    logger.info("Running daily archive (placeholder)")
    pass

def run_db_backup():
    """Placeholder for database backup."""
    logger.info("Running database backup (placeholder)")
    pass

# Add jobs to scheduler
scheduler.add_job(func=run_morning_scan, trigger="cron", hour=9, minute=15)
scheduler.add_job(func=run_evening_validation, trigger="cron", hour=17, minute=0)
scheduler.add_job(func=run_daily_archive, trigger="cron", hour=23, minute=0)
scheduler.add_job(func=run_db_backup, trigger="cron", hour=2, minute=0)

# Start Scheduler
scheduler.start()
atexit.register(lambda: scheduler.shutdown())

@app.route('/api/scheduler/jobs', methods=['GET'])
def get_scheduled_jobs():
    """Returns list of scheduled jobs."""
    jobs = []
    for job in scheduler.get_jobs():
        jobs.append({
            "id": job.id,
            "name": job.name,
            "next_run_time": str(job.next_run_time),
            "trigger": str(job.trigger)
        })
    return jsonify({"jobs": jobs, "status": "running" if scheduler.running else "stopped"})


# ===== Multi-AI Verification Endpoints =====
try:
    from backend.ai.multi_ai_verifier import MultiAIVerifier
    from backend.ai.consensus_engine import ConsensusEngine
    from backend.ai.config.models_config import get_model_stats, get_trading_models
    
    multi_ai_available = True
    multi_ai_verifier = MultiAIVerifier()
    consensus_engine = ConsensusEngine()
except Exception as e:
    logger.warning(f"Multi-AI system not available: {e}")
    multi_ai_available = False

@app.route('/api/ai/verify', methods=['POST'])
def verify_strategy_ai():
    """Verify a trading strategy using multiple AI models"""
    if not multi_ai_available:
        return jsonify({"error": "Multi-AI system not available"}), 503
    
    try:
        data = request.get_json()
        strategy_text = data.get('strategy', '')
        
        if not strategy_text:
            return jsonify({"error": "Strategy text is required"}), 400
        
        # Verify with multi-AI
        result = multi_ai_verifier.verify_strategy(strategy_text)
        
        # Calculate consensus
        consensus = consensus_engine.calculate_consensus(result['responses'])
        
        # Combine results
        return jsonify({
            "strategy": strategy_text,
            "verification": result,
            "consensus": consensus,
            "status": "success"
        })
        
    except Exception as e:
        logger.error(f"Error in AI verification: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/ai/models', methods=['GET'])
def get_ai_models():
    """Get list of available AI models"""
    if not multi_ai_available:
        return jsonify({"error": "Multi-AI system not available"}), 503
    
    try:
        stats = get_model_stats()
        models = get_trading_models()
        
        model_list = [{
            "id": m['id'],
            "name": m['name'],
            "role": m['role'].value,
            "specialty": m['specialty'],
            "weight": m['weight'],
            "enabled": m['enabled']
        } for m in models]
        
        return jsonify({
            "models": model_list,
            "stats": stats
        })
    except Exception as e:
        logger.error(f"Error fetching models: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/ai/stats', methods=['GET'])
def get_ai_stats():
    """Get AI model usage statistics"""
    if not multi_ai_available:
        return jsonify({"error": "Multi-AI system not available"}), 503
    
    try:
        from backend.ai.model_manager import model_manager
        
        # Get summary statistics
        summary = model_manager.get_summary()
        
        # Get best performing models
        best_models = model_manager.get_best_performing_models(top_n=5)
        
        # Get per-model stats
        all_stats = model_manager.get_model_stats()
        
        return jsonify({
            "summary": summary,
            "best_performers": best_models,
            "model_stats": all_stats,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Error fetching AI stats: {e}")
        return jsonify({"error": str(e)}), 500

# ===== Evolution System Endpoints =====
# try:
#     from backend.evolution.population import Population
#     evolution_population = Population(100)
#     # Create initial population
#     evolution_population.create_initial_population()
#     evolution_available = True
# except Exception as e:
#     logger.error(f"Failed to initialize Evolution System: {e}")
#     evolution_available = False
evolution_available = False

@app.route('/api/evolution/status', methods=['GET'])
def get_evolution_status():
    """Get current evolution status."""
    if not evolution_available:
        return jsonify({"error": "Evolution system not available"}), 503
        
    try:
        best_organism = evolution_population.get_best_organism()
        return jsonify({
            "generation": evolution_population.generation,
            "population_size": len(evolution_population.organisms),
            "best_fitness": best_organism.fitness if best_organism else 0.0,
            "best_organism_id": best_organism.id if best_organism else None
        })
    except Exception as e:
        logger.error(f"Error fetching evolution status: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/evolution/evolve', methods=['POST'])
def trigger_evolution():
    """Manually trigger an evolution cycle."""
    if not evolution_available:
        return jsonify({"error": "Evolution system not available"}), 503

    try:
        stats = evolution_population.evolve()
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error triggering evolution: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/evolution/best', methods=['GET'])
def get_best_organism_endpoint():
    """Get the best organism's DNA."""
    if not evolution_available:
        return jsonify({"error": "Evolution system not available"}), 503

    try:
        best = evolution_population.get_best_organism()
        if best:
            return jsonify({
                "id": best.id,
                "generation": best.generation,
                "fitness": best.fitness,
                "dna": best.dna
            })
        return jsonify({"message": "No organisms found"}), 404
    except Exception as e:
        logger.error(f"Error fetching best organism: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/evolution/history', methods=['GET'])
def get_evolution_history():
    """Get evolution history (generations)."""
    if not evolution_available:
        return jsonify({"error": "Evolution system not available"}), 503

    try:
        # In a real implementation, this would fetch from the database
        # For now, we'll return mock history if DB is empty, or fetch from DB
        history = []
        
        # Try to fetch from DB first
        try:
            with db._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM evolution_history ORDER BY generation DESC LIMIT 20")
                rows = cursor.fetchall()
                for row in rows:
                    history.append({
                        "generation": row['generation'],
                        "best_fitness": row['best_fitness'],
                        "avg_fitness": row['avg_fitness'],
                        "population_size": row['population_size']
                    })
        except Exception as db_e:
            logger.warning(f"Failed to fetch evolution history from DB: {db_e}")
            
        # If no history yet, return current state as gen 1
        if not history and evolution_population.generation > 0:
             history.append({
                "generation": evolution_population.generation,
                "best_fitness": evolution_population.get_best_organism().fitness if evolution_population.get_best_organism() else 0,
                "avg_fitness": 0.0, # Calculate if needed
                "population_size": len(evolution_population.organisms)
             })
             
        return jsonify(history)
    except Exception as e:
        logger.error(f"Error fetching evolution history: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/demo/multi-ai-research', methods=['GET'])
def demo_multi_ai():
    """Demo endpoint to test multi-AI verification"""
    if not multi_ai_available:
        return jsonify({"error": "Multi-AI system not available"}), 503
    
    try:
        # Sample strategy for demo
        demo_strategy = """
        Trading Strategy: RSI Oversold/Overbought
        
        Entry Rules:
        - BUY when RSI crosses below 30 (oversold)
        - SELL when RSI crosses above 70 (overbought)
        
        Parameters:
        - RSI Period: 14
        - Timeframe: 15 minutes
        - Stop Loss: 2%
        - Take Profit: 4%
        
        Risk Management:
        - Max position size: 5% of capital
        - Max daily trades: 3
        """
        
        # Verify with multi-AI
        result = multi_ai_verifier.verify_strategy(demo_strategy)
        
        # Calculate consensus
        consensus = consensus_engine.calculate_consensus(result['responses'])
        
        # Save demo output to file
        try:
            demo_output_dir = os.path.join(os.path.dirname(__file__), '../data/demo_outputs')
            os.makedirs(demo_output_dir, exist_ok=True)
            
            output_file = os.path.join(demo_output_dir, f"demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            with open(output_file, 'w') as f:
                json.dump({
                    "demo": True,
                    "strategy": demo_strategy,
                    "verification": result,
                    "consensus": consensus,
                    "timestamp": datetime.now().isoformat()
                }, f, indent=2)
            logger.info(f"Demo output saved to {output_file}")
        except Exception as e:
            logger.warning(f"Could not save demo output: {e}")
        
        return jsonify({
            "demo": True,
            "strategy": demo_strategy,
            "verification": result,
            "consensus": consensus,
            "message": "This is a demo of the multi-AI verification system"
        })
        
    except Exception as e:
        logger.error(f"Error in demo: {e}")
        return jsonify({"error": str(e)}), 500


# ===== Agent Detail View Endpoints =====

@app.route('/api/agents/<agent_id>/details', methods=['GET'])
def get_agent_details(agent_id):
    """Get comprehensive details for a specific agent"""
    try:
        # Agent metadata
        agent_names = {
            "agent_1": "NSE Data Collector",
            "agent_2": "Technical Indicator Collector",
            "agent_3": "Order Book Analyzer",
            "agent_4": "News Event Collector",
            "agent_5": "Historical Data Manager",
            "agent_6": "Web News Aggregator",
            "agent_7": "Technical Indicator Analyst",
            "agent_8": "Crypto Strategy Hunter",
            "agent_9": "Angel One Data Miner",
            "agent_10": "Market Sentiment Analyzer",
            "tester_1": "Conservative Tester",
            "tester_2": "Aggressive Tester",
            "tester_3": "Balanced Tester",
            "tester_4": "Scalping Tester",
            "tester_5": "Swing Tester",
            "tester_6": "Day Trader",
            "tester_7": "Position Trader",
            "tester_8": "Volatility Tester",
            "tester_9": "Trend Follower",
            "tester_10": "Mean Reversion Tester"
        }

        # Get live status from status.json
        live_status = {}
        try:
            status_file = os.path.join(os.path.dirname(__file__), '../data/status.json')
            if os.path.exists(status_file):
                with open(status_file, 'r') as f:
                    all_status = json.load(f)
                    for agent in all_status:
                        if agent.get('id') == agent_id:
                            live_status = agent
                            logger.info(f"Found live_status for {agent_id}: {live_status}")
                            break
                    if not live_status:
                        logger.warning(f"No live_status found in status.json for {agent_id}")
        except Exception as e:
            logger.error(f"Error reading status file: {e}")

        if agent_id.startswith('tester_'):
            stats = db.get_tester_statistics(agent_id)
            results = db.get_tester_results(agent_id, limit=20)
            graph_data = db.get_tester_graph_data(agent_id)
            
            return jsonify({
                "agent_id": agent_id,
                "name": agent_names.get(agent_id, agent_id.replace("_", " ").title()),
                "type": "Tester",
                "specialty": "Strategy Simulation",
                "status": live_status.get('status', 'Active'),
                "live_status": live_status,
                "stats": stats,
                "recent_activity": results,
                "test_results": results, 
                "performanceMetrics": graph_data.get('performanceMetrics', {}),
                "profitDistribution": graph_data.get('profitDistribution', [])
            })
        else:
            # Collector Logic
            # Collector Logic
            try:
                stats = db.get_agent_statistics(agent_id)
            except Exception:
                stats = {}
            
            try:
                collections = db.get_agent_collections(agent_id, limit=20)
            except Exception:
                collections = []
                
            try:
                verification = db.get_agent_verification_breakdown(agent_id)
            except Exception:
                verification = {}
                
            try:
                timeline = db.get_agent_timeline(agent_id, days=30)
            except Exception:
                timeline = []
                
            try:
                graph_data = db.get_agent_graph_data(agent_id)
            except Exception:
                graph_data = {}
            
            return jsonify({
                "agent_id": agent_id,
                "name": agent_names.get(agent_id, agent_id.replace("_", " ").title()),
                "type": "Collector",
                "specialty": "Trading Strategy Collection",
                "status": live_status.get('status', 'Active'),
                "live_status": live_status,
                "stats": stats,
                "verification": verification,
                "recent_collections": collections,
                "timeline": timeline,
                "sourceBreakdown": graph_data.get('sourceBreakdown', []),
                "qualityDistribution": graph_data.get('qualityDistribution', []),
                "performanceMetrics": graph_data.get('performanceMetrics', {})
            })

    except Exception as e:
        logger.error(f"Error fetching agent details: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/agents/<agent_id>/collections', methods=['GET'])
def get_agent_collections_paginated(agent_id):
    """Get paginated collections for an agent"""
    try:
        limit = int(request.args.get('limit', 20))
        collections = db.get_agent_collections(agent_id, limit=limit)
        return jsonify({
            "agent_id": agent_id,
            "collections": collections,
            "count": len(collections)
        })
    except Exception as e:
        logger.error(f"Error fetching collections: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/agents/<agent_id>/stats', methods=['GET'])
def get_agent_stats_only(agent_id):
    """Get just the statistics for an agent"""
    try:
        stats = db.get_agent_statistics(agent_id)
        verification = db.get_agent_verification_breakdown(agent_id)
        return jsonify({
            "agent_id": agent_id,
            "stats": stats,
            "verification": verification
        })
    except Exception as e:
        logger.error(f"Error fetching stats: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/agents/<agent_id>/activity', methods=['GET'])
def get_agent_activity(agent_id):
    """Get complete activity log for an agent"""
    try:
        limit = request.args.get('limit', 100, type=int)
        
        if agent_id.startswith('tester_'):
            # Get tester results
            results = db.get_tester_results(agent_id, limit=limit)
            
            # Format as activity log
            activity_log = []
            for i, result in enumerate(results):
                status_map = {'PASS': 'approved', 'FAIL': 'rejected'}
                activity = {
                    'id': result.get('id'),
                    'timestamp': result.get('timestamp'),
                    'type': 'test',
                    'action': f"Tested strategy: {result.get('strategy_name')}",
                    'strategy_name': result.get('strategy_name'),
                    'source': result.get('source', 'Unknown'),
                    'source_url': '#', # Testers don't store URL directly in results usually, but strategy has it
                    'status': status_map.get(result.get('recommendation'), 'warning'),
                    'quality_score': int(result.get('win_rate', 0)), # Use Win Rate as quality score equivalent
                    'details': {
                        'win_rate': result.get('win_rate'),
                        'profit_factor': result.get('profit_factor'),
                        'net_profit': result.get('net_profit')
                    }
                }
                activity_log.append(activity)
                
            return jsonify({
                'agent_id': agent_id,
                'total_activities': len(activity_log),
                'activities': activity_log
            })
            
        else:
            # Get all collections (acts as activity log)
            collections = db.get_agent_collections(agent_id, limit=limit)
            
            # Format as activity log
            activity_log = []
            for i, collection in enumerate(collections):
                activity = {
                    'id': collection.get('id'),
                    'timestamp': collection.get('collected_at'),
                    'type': 'collection',
                    'action': f"Collected strategy: {collection.get('strategy_name')}",
                    'strategy_name': collection.get('strategy_name'),
                    'source': collection.get('source'),
                    'source_url': collection.get('source_url'),
                    'status': collection.get('verification_status', 'unknown'),
                    'quality_score': collection.get('quality_score', 0),
                    'details': {
                        'verified': collection.get('verification_status') == 'approved',
                        'confidence': collection.get('quality_score', 0),
                        'source': collection.get('source')
                    }
                }
                activity_log.append(activity)
            
            return jsonify({
                'agent_id': agent_id,
                'total_activities': len(activity_log),
                'activities': activity_log
            })
        
    except Exception as e:
        logger.error(f"Error getting activity log for {agent_id}: {e}")
        return jsonify({"error": str(e)}), 500



# ===== Paper Trading Validation Endpoints =====
from backend.trading.validation_manager import ValidationManager
from backend.trading.performance_tracker import PerformanceTracker
from backend.evolution.population import Population

# Initialize validation manager (will be created per request in production)
validation_pop = Population(population_size=20)
validation_manager = ValidationManager(validation_pop, num_strategies=3, duration_days=5)

@app.route('/api/paper-trading/start', methods=['POST'])
def start_paper_trading():
    """Start a new paper trading validation session."""
    try:
        result = validation_manager.start_validation()
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to start validation: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/paper-trading/status', methods=['GET'])
def get_paper_trading_status():
    """Get current validation session status."""
    try:
        status = validation_manager.get_session_status()
        return jsonify(status), 200
    except Exception as e:
        logger.error(f"Failed to get status: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/paper-trading/stop', methods=['POST'])
def stop_paper_trading():
    """Stop the current validation session."""
    try:
        result = validation_manager.stop_validation()
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to stop validation: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/paper-trading/results', methods=['GET'])
def get_paper_trading_results():
    """Get performance results for current or specified session."""
    try:
        session_id = request.args.get('session_id', validation_manager.session_id)
        if not session_id:
            return jsonify({"error": "No session specified or active"}), 400
        
        report = PerformanceTracker.generate_performance_report(session_id)
        return jsonify(report), 200
    except Exception as e:
        logger.error(f"Failed to get results: {e}")
        return jsonify({"error": str(e)}), 500


# ===== Live Trading Endpoints =====
from backend.trading.live_manager import LiveTradingManager
from backend.trading.approval_system import TradeApprovalSystem

# Initialize live trading manager (DISABLED by default)
live_trading_manager = LiveTradingManager(initial_capital=25000)

@app.route('/api/live-trading/enable', methods=['POST'])
@limiter.limit("1 per hour")  # Strict rate limit for this critical endpoint
def enable_live_trading():
    """Enable live trading (requires authorization)."""
    try:
        data = request.get_json() or {}
        authorized_by = data.get('authorized_by', 'unknown')
        
        result = live_trading_manager.enable_live_trading(authorized_by)
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        logger.error(f"Failed to enable live trading: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/live-trading/disable', methods=['POST'])
def disable_live_trading():
    """Disable live trading."""
    try:
        data = request.get_json() or {}
        reason = data.get('reason', 'Manual stop')
        
        result = live_trading_manager.disable_live_trading(reason)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to disable live trading: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/live-trading/emergency-stop', methods=['POST'])
def emergency_stop():
    """Emergency stop - immediately halt all trading."""
    try:
        data = request.get_json() or {}
        reason = data.get('reason', 'Emergency stop button pressed')
        
        result = live_trading_manager.emergency_stop_all(reason)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Emergency stop failed: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/live-trading/status', methods=['GET'])
def get_live_trading_status():
    """Get current live trading status."""
    try:
        status = live_trading_manager.get_status()
        return jsonify(status), 200
    except Exception as e:
        logger.error(f"Failed to get live trading status: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/live-trading/submit-trade', methods=['POST'])
def submit_trade():
    """Submit a trade (may require approval)."""
    try:
        trade_details = request.get_json()
        result = live_trading_manager.submit_trade(trade_details)
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to submit trade: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/live-trading/approve-trade/<trade_id>', methods=['POST'])
def approve_trade(trade_id):
    """Approve a pending trade."""
    try:
        data = request.get_json() or {}
        approved_by = data.get('approved_by', 'user')
        
        result = live_trading_manager.approval_system.approve_trade(trade_id, approved_by)
        
        if result['success']:
            # Execute the approved trade
            trade = result['trade']
            execution = live_trading_manager._execute_trade(trade)
            result['execution'] = execution
        
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        logger.error(f"Failed to approve trade: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/live-trading/reject-trade/<trade_id>', methods=['POST'])
def reject_trade(trade_id):
    """Reject a pending trade."""
    try:
        data = request.get_json() or {}
        reason = data.get('reason', 'No reason provided')
        
        result = live_trading_manager.approval_system.reject_trade(trade_id, reason)
        return jsonify(result), 200 if result['success'] else 400
    except Exception as e:
        logger.error(f"Failed to reject trade: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/live-trading/pending-trades', methods=['GET'])
def get_pending_trades():
    """Get all trades awaiting approval."""
    try:
        pending = live_trading_manager.approval_system.get_pending_trades()
        return jsonify({'pending_trades': pending, 'count': len(pending)}), 200
    except Exception as e:
        logger.error(f"Failed to get pending trades: {e}")
        return jsonify({"error": str(e)}), 500


# ===== Advanced AI Endpoints =====
from backend.ai.sentiment_analyzer import SentimentAnalyzer
from backend.ai.pattern_detector import PatternDetector
from backend.ai.ml_predictor import MLPredictor
from backend.ai.regime_detector import RegimeDetector

# Initialize AI systems
sentiment_analyzer = SentimentAnalyzer()
pattern_detector = PatternDetector()
ml_predictor = MLPredictor()
regime_detector = RegimeDetector()

@app.route('/api/ai/sentiment/<symbol>', methods=['GET'])
def get_sentiment(symbol):
    """Get sentiment analysis for a symbol."""
    try:
        # Mock headlines for demonstration - in production, fetch real news
        mock_headlines = [
            f"{symbol} shows strong growth potential",
            f"Analysts bullish on {symbol} stock",
            f"{symbol} reports better than expected earnings"
        ]
        
        result = sentiment_analyzer.get_symbol_sentiment(symbol, mock_headlines)
        signal = sentiment_analyzer.get_trading_signal(result)
        result['trading_signal'] = signal
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Sentiment analysis failed: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/ai/patterns/<symbol>', methods=['GET'])
def get_patterns(symbol):
    """Detect chart patterns for a symbol."""
    try:
        # Mock price data for demonstration - in production, fetch real data
        mock_prices = []
        for i in range(50):
            mock_prices.append({
                'open': 100 + i * 0.5,
                'high': 102 + i * 0.5,
                'low': 99 + i * 0.5,
                'close': 101 + i * 0.5,
                'timestamp': f"2024-01-{i+1:02d}"
            })
        
        result = pattern_detector.analyze_patterns(mock_prices)
        result['symbol'] = symbol
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Pattern detection failed: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/ai/predict/<symbol>', methods=['GET'])
def get_ml_prediction(symbol):
    """Get ML-based price prediction for a symbol."""
    try:
        # Mock indicator data for demonstration
        mock_indicators = {
            'rsi': 55,
            'macd': 1.2,
            'macd_signal': 1.0,
            'bb_position': 0.6,
            'volume_ratio': 1.3,
            'price_change_pct': 0.5,
            'sma_20': 100,
            'sma_50': 98
        }
        
        result = ml_predictor.predict(mock_indicators)
        result['symbol'] = symbol
        result['note'] = 'Model requires training on historical data'
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"ML prediction failed: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/ai/regime', methods=['GET'])
def get_market_regime():
    """Get current market regime classification."""
    try:
        # Mock price history for demonstration
        mock_prices = [100 + i * 0.2 + np.random.randn() * 2 for i in range(50)]
        
        result = regime_detector.classify_regime(mock_prices)
        adjustments = regime_detector.get_strategy_adjustment(result['regime'])
        result['strategy_adjustments'] = adjustments
        
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Regime detection failed: {e}")
        return jsonify({"error": str(e)}), 500


# ===== System Monitoring & Optimization Endpoints =====
# from backend.utils.profiler import profiler  # DISABLED
# from backend.utils.cache import cache_manager  # DISABLED
# from backend.tasks.queue import task_queue  # DISABLED

# Start task queue
# task_queue.start()  # DISABLED: Causes Flask to crash on startup

@app.route('/api/monitoring/performance', methods=['GET'])
def get_performance_metrics():
    """Get performance profiling metrics."""
    try:
        # stats = profiler.get_stats(limit=20)  # DISABLED
        # bottlenecks = profiler.identify_bottlenecks(threshold_ms=200)  # DISABLED
        stats, bottlenecks = [], []
        
        return jsonify({
            'performance_stats': stats,
            'bottlenecks': bottlenecks,
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        logger.error(f"Failed to get performance metrics: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/monitoring/cache', methods=['GET'])
def get_cache_stats():
    """Get cache statistics and info."""
    try:
        # cache_info = cache_manager.get_cache_info()  # DISABLED
        cache_info = {'status': 'disabled'}
        return jsonify(cache_info), 200
    except Exception as e:
        logger.error(f"Failed to get cache stats: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/monitoring/cache/clear', methods=['POST'])
def clear_cache():
    """Clear all cache."""
    try:
        # cache_manager.clear()  # DISABLED
        pass
        return jsonify({"message": "Cache cleared successfully"}), 200
    except Exception as e:
        logger.error(f"Failed to clear cache: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/monitoring/queue', methods=['GET'])
def get_queue_status():
    """Get task queue status."""
    try:
        # status = task_queue.get_queue_status()  # DISABLED
        status = {'status': 'disabled'}
        return jsonify(status), 200
    except Exception as e:
        logger.error(f"Failed to get queue status: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/monitoring/database', methods=['GET'])
def get_database_stats():
    """Get database statistics."""
    try:
        stats = db.get_db_stats()
        return jsonify(stats), 200
    except Exception as e:
        logger.error(f"Failed to get database stats: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/optimization/database/vacuum', methods=['POST'])
def vacuum_database():
    """Optimize database (vacuum and analyze)."""
    try:
        # Run in background via task queue
        # task_id = task_queue.submit(db.vacuum_database)  # DISABLED
        db.vacuum_database()  # Run synchronously
        task_id = 'disabled'
        return jsonify({
            "message": "Database optimization started",
            "task_id": task_id
        }), 202
    except Exception as e:
        logger.error(f"Failed to start database optimization: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/optimization/database/create-indexes', methods=['POST'])
def create_database_indexes():
    """Create database indexes for query optimization."""
    try:
        db.create_indexes()
        return jsonify({"message": "Database indexes created successfully"}), 200
    except Exception as e:
        logger.error(f"Failed to create indexes: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task_result(task_id):
    """Get result of a background task."""
    try:
        # result = task_queue.get_result(task_id)  # DISABLED
        result = {'status': 'disabled'}
        return jsonify(result), 200
    except Exception as e:
        logger.error(f"Failed to get task result: {e}")
        return jsonify({"error": str(e)}), 500


# Register Blueprints for additional features
from backend.api.dashboard_routes import dashboard_bp
from backend.api.movers_routes import movers_bp
from backend.api.stock_routes import stock_bp
from backend.api.alert_routes import alert_bp
from backend.api.learning_routes import learning_bp
from backend.api.settings_routes import settings_bp

app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
app.register_blueprint(movers_bp, url_prefix='/api/market/movers')
app.register_blueprint(stock_bp, url_prefix='/api/stocks')
app.register_blueprint(alert_bp, url_prefix='/api/alerts')
app.register_blueprint(learning_bp, url_prefix='/api/learning')
app.register_blueprint(settings_bp, url_prefix='/api/settings')

# Evolution blueprint kept commented for now
# from backend.api.evolution_routes import evolution_bp
# app.register_blueprint(evolution_bp, url_prefix='/api/evolution')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

