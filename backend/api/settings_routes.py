"""
Settings API endpoints
"""
from flask import Blueprint, jsonify, request
import json
import os

settings_bp = Blueprint('settings', __name__)

SETTINGS_FILE = 'user_settings.json'

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {
        'theme': 'dark',
        'notifications': True,
        'autoTrade': False,
        'maxRiskPerTrade': 1.0,
        'dailyLossLimit': 2.0
    }

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

@settings_bp.route('', methods=['GET'])
def get_settings():
    """Get user settings."""
    return jsonify(load_settings()), 200

@settings_bp.route('', methods=['POST'])
def update_settings():
    """Update user settings."""
    try:
        new_settings = request.json
        current_settings = load_settings()
        current_settings.update(new_settings)
        save_settings(current_settings)
        return jsonify(current_settings), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
