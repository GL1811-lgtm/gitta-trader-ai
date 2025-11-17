# backend/agents/expert/expert_agent.py

"""
Expert Agent: Analyzes all data and generates the final daily report.
"""

import os
import json
from datetime import datetime

# Import placeholder modules and the new message schema
from backend.agents.expert.analysis import StrategyAnalyzer
from backend.agents.expert.report_writer import write_daily_report
from backend.agents.shared.message_schema import AgentMessage

class ExpertAgent:
    """
    The Expert Agent runs once daily to process all data collected and
    tested by other agents, producing a human-readable report.
    """

    def __init__(self, config_path='backend/agents/expert/config.yaml'):
        """Initializes the Expert Agent."""
        # self.config = self._load_config(config_path)
        self.inbox_dir = 'backend/agents/expert/inbox'
        self.reports_dir = 'backend/agents/expert/reports'
        self.analyzer = StrategyAnalyzer()
        os.makedirs(self.inbox_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
        print("Expert Agent initialized.")

    def generate_daily_report(self):
        """
        The main entry point for the agent's daily run.
        This is triggered by an API call.
        """
        print("\n--- Expert Agent starting daily analysis and report generation ---")

        # 1. Ingest and sort data from inbox
        messages = self._read_inbox()
        if not messages:
            print("No new data from Supervisor. Generating an empty report.")
            # Still generate a report to show the system is alive
            analysis_results = {'error': 'No data received from Supervisor.'}
        else:
            strategies = [m for m in messages if m.message_type == 'strategy']
            test_results = [m for m in messages if m.message_type == 'test_result']
            print(f"Read {len(strategies)} new strategies and {len(test_results)} new test results.")

            # 2. Pass the sorted data to the analysis module (placeholder)
            analysis_results = self.analyzer.analyze_data(strategies, test_results)

        # 3. Generate and write the report (placeholder)
        report_path = write_daily_report(analysis_results, self.reports_dir)
        print(f"Daily report generated at: {report_path}")

        # 4. Clean up the inbox for the next day's run
        self._clear_inbox(messages)

        print("--- Expert Agent daily run complete ---\n")
        return report_path

    def _read_inbox(self) -> list[AgentMessage]:
        """
        Reads all JSON message files from the inbox and deserializes them
        into AgentMessage objects.
        """
        messages = []
        print(f"Reading data from inbox: {self.inbox_dir}")
        for filename in os.listdir(self.inbox_dir):
            if not filename.endswith('.json'):
                continue
            
            file_path = os.path.join(self.inbox_dir, filename)
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                messages.append(AgentMessage.from_dict(data))
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Could not parse message file {filename}: {e}")
        return messages

    def _clear_inbox(self, processed_messages: list[AgentMessage]):
        """
        Deletes the files that were successfully processed.
        """
        print(f"Clearing {len(processed_messages)} messages from inbox...")
        # This is a simplification. In a real system, you'd use the message
        # file's original path, stored during the read phase.
        for filename in os.listdir(self.inbox_dir):
             if filename.endswith('.json'):
                os.remove(os.path.join(self.inbox_dir, filename))

if __name__ == '__main__':
    # This allows running a single cycle directly for testing
    expert = ExpertAgent()
    expert.generate_daily_report()
