# backend/agents/supervisor/supervisor.py

"""
Supervisor Agent: Orchestrates and monitors all other agents.
"""

import os
import json
import time
from datetime import datetime
# import yaml # In a real implementation, you'd use this

# Import the message schema
from backend.agents.shared.message_schema import AgentMessage

class SupervisorAgent:
    """
    The main Supervisor Agent. Its responsibilities include:
    - Polling inboxes for new messages from Collector and Tester agents.
    - Wrapping the data into a standardized AgentMessage format.
    - Forwarding these messages to the Expert Agent's inbox.
    - (Future) Monitoring agent health and triggering restarts.
    """

    def __init__(self, config_path='backend/agents/supervisor/config.yaml'):
        """Initializes the Supervisor Agent."""
        # self.config = self._load_config(config_path)
        self.collector_inbox = 'backend/agents/supervisor/inbox'
        self.tester_inbox = 'backend/agents/supervisor/inbox_tests'
        self.expert_inbox = 'backend/agents/expert/inbox'
        self.running = False
        os.makedirs(self.expert_inbox, exist_ok=True)
        print("Supervisor Agent initialized.")

    def run_once(self):
        """
        Runs a single cycle of the supervisor's tasks.
        This function will be triggered by an API call.
        """
        print("\n--- Supervisor running one cycle ---")
        self.process_inbox(self.collector_inbox, "strategy")
        self.process_inbox(self.tester_inbox, "test_result")
        print("--- Supervisor cycle complete ---\n")

    def process_inbox(self, inbox_path: str, message_type: str):
        """
        Scans an inbox, processes each message, and forwards it.
        """
        print(f"Scanning {inbox_path} for new messages...")
        if not os.path.exists(inbox_path):
            print(f"Inbox {inbox_path} does not exist. Skipping.")
            return

        for filename in os.listdir(inbox_path):
            if not filename.endswith('.json'):
                continue

            file_path = os.path.join(inbox_path, filename)
            try:
                with open(file_path, 'r') as f:
                    raw_payload = json.load(f)

                # Determine the source agent from the filename or payload
                source_agent = raw_payload.get('agent_id', 'unknown_agent')

                # Wrap the data in the standard message schema
                message = AgentMessage(
                    message_type=message_type,
                    source_agent=source_agent,
                    payload=raw_payload
                )

                # Forward the standardized message
                self.forward_to_expert(message)

                # Clean up the original message
                os.remove(file_path)
                print(f"Processed and removed {filename}")

            except (json.JSONDecodeError, Exception) as e:
                print(f"Error processing file {filename}: {e}")
                # In a real system, move this to a 'quarantine' or 'dead-letter' queue
                pass

    def forward_to_expert(self, message: AgentMessage):
        """
        Forwards the standardized message to the Expert Agent's inbox
        as a new JSON file.
        """
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
        output_filename = f"{message.source_agent}_{timestamp}.json"
        output_path = os.path.join(self.expert_inbox, output_filename)

        print(f"Forwarding message from {message.source_agent} to Expert Agent at {output_path}")
        try:
            with open(output_path, 'w') as f:
                json.dump(message.to_dict(), f, indent=4)
        except IOError as e:
            print(f"Failed to forward message to expert: {e}")

if __name__ == '__main__':
    # This allows running a single cycle directly for testing
    supervisor = SupervisorAgent()
    supervisor.run_once()
