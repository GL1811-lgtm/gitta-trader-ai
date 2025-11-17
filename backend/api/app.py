from flask import Flask, jsonify
import sys
import os

# Adjust path to import from parent directories
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import existing and new components
from backend.collectors.fetcher import fetch_latest
from backend.predictor.predictor import predict_signal
from backend.agents.supervisor.supervisor import SupervisorAgent
from backend.agents.expert.expert_agent import ExpertAgent

app = Flask(__name__)

# --- New Agent Instances ---
# In a real application, these would be managed as singletons.
supervisor = SupervisorAgent()
expert = ExpertAgent()

# --- Existing Prediction Endpoint ---

@app.route('/predict/<symbol>')
def get_prediction(symbol):
    """
    Fetches data for a symbol, runs the predictor, and returns the trading signal.
    """
    if not symbol:
        return jsonify({"error": "Symbol cannot be empty"}), 400

    try:
        ohlcv_data = fetch_latest(symbol)
        if ohlcv_data.empty:
            return jsonify({"error": f"No data found for symbol: {symbol}"}), 404

        prediction = predict_signal(ohlcv_data)
        if not prediction:
            return jsonify({"error": "Prediction failed"}), 500

        response = {
            "symbol": symbol.upper(),
            "signal": prediction.get("signal"),
            "confidence": prediction.get("confidence"),
            "reason": prediction.get("reason")
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

# --- Phase 5: New Placeholder API Endpoints ---

@app.route('/ping', methods=['GET'])
def ping():
    """A simple health-check endpoint."""
    return jsonify({"status": "ok", "timestamp": supervisor.expert_inbox.title()}), 200

@app.route('/agent/supervisor/run', methods=['POST'])
def run_supervisor():
    """
    Triggers a single, placeholder run of the Supervisor agent's inbox processing.
    """
    try:
        supervisor.run_once()
        return jsonify({"status": "supervisor run triggered"}), 200
    except Exception as e:
        return jsonify({"error": f"Supervisor run failed: {str(e)}"}), 500

@app.route('/agent/expert/generate', methods=['POST'])
def generate_expert_report():
    """
    Triggers the Expert agent's daily summary generation.
    """
    try:
        report_path = expert.generate_daily_report()
        return jsonify({
            "status": "expert report generation triggered",
            "report_path": report_path
        }), 200
    except Exception as e:
        return jsonify({"error": f"Expert report generation failed: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', '5001'))
    app.run(host='0.0.0.0', port=port, debug=True)