# backend/agents/shared/queue.py

"""
Shared queue/messaging system for inter-agent communication.

This is a simplified, file-based implementation for passing messages.
In a production environment, this would be replaced with a robust
message broker like RabbitMQ, Redis Pub/Sub, or Kafka.
"""

import os
import json
from datetime import datetime

SUPERVISOR_INBOX = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'supervisor', 'inbox'))

def send_to_supervisor(agent_id: str, message_data: dict):
    """
    Sends a message from an agent to the supervisor's inbox.

    Args:
        agent_id (str): The ID of the sending agent (e.g., 'collector_1').
        message_data (dict): The data payload to send.
    """
    if not os.path.exists(SUPERVISOR_INBOX):
        os.makedirs(SUPERVISOR_INBOX)
        # Add a .gitkeep file to ensure the directory is tracked
        with open(os.path.join(SUPERVISOR_INBOX, '.gitkeep'), 'w') as f:
            pass

    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
    message_filename = f"{agent_id}_message_{timestamp}.json"
    message_path = os.path.join(SUPERVISOR_INBOX, message_filename)

    message = {
        'sender_id': agent_id,
        'timestamp': datetime.utcnow().isoformat(),
        'payload': message_data
    }

    try:
        with open(message_path, 'w') as f:
            json.dump(message, f, indent=4)
        print(f"Message from {agent_id} sent to supervisor: {message_path}")
        return True
    except IOError as e:
        print(f"Error sending message from {agent_id}: {e}")
        return False

def read_supervisor_inbox():
    """
    Reads all messages from the supervisor's inbox.
    (This function would be used by the Supervisor Agent).
    """
    messages = []
    if not os.path.exists(SUPERVISOR_INBOX):
        return messages

    for filename in os.listdir(SUPERVISOR_INBOX):
        if filename.endswith('.json'):
            message_path = os.path.join(SUPERVISOR_INBOX, filename)
            try:
                with open(message_path, 'r') as f:
                    messages.append(json.load(f))
                # Optionally, delete the message after reading
                # os.remove(message_path)
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error reading message {filename}: {e}")
    return messages
