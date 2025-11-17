# backend/agents/collectors/shared/queue.py
import os
import json
from datetime import datetime

# The supervisor will read from this directory.
COLLECTOR_QUEUE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'supervisor', 'inbox'))

def push_to_collector_queue(agent_id: str, strategy_name: str):
    """
    Pushes a notification to the collector queue (which is the supervisor's collector inbox).
    This notifies the supervisor that a new strategy has been added.
    """
    if not os.path.exists(COLLECTOR_QUEUE_DIR):
        os.makedirs(COLLECTOR_QUEUE_DIR)

    message = {
        'agent_id': agent_id,
        'type': 'new_strategy_collected',
        'strategy_name': strategy_name,
        'timestamp': datetime.utcnow().isoformat()
    }
    filename = f"notification_{agent_id}_{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}.json"
    filepath = os.path.join(COLLECTOR_QUEUE_DIR, filename)

    try:
        with open(filepath, 'w') as f:
            json.dump(message, f, indent=4)
        return True
    except Exception as e:
        # In a real app, you'd have more robust error logging here.
        print(f"Error pushing to collector queue: {e}")
        return False
