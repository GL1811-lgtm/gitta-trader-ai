# backend/agents/supervisor/monitor.py

"""
Agent Monitoring Component for the Supervisor.
"""

from datetime import datetime, timedelta
# from backend.agents.supervisor.restart_hook import restart_agent

class AgentMonitor:
    """
    Monitors the health of Collector and Tester agents.
    - Checks for heartbeats or recent activity.
    - Triggers restart hooks for failed agents.
    """

    def __init__(self, config):
        """
        Initializes the monitor.
        - config: A dictionary with monitoring settings.
        """
        self.config = config['monitoring']
        self.agent_statuses = self._initialize_agent_statuses()

    def _initialize_agent_statuses(self):
        """Creates an initial status dictionary for all agents."""
        statuses = {}
        num_collectors = self.config['num_collector_agents']
        num_testers = self.config['num_tester_agents']
        for i in range(1, num_collectors + 1):
            statuses[f'collector_{i}'] = {'status': 'unknown', 'last_heartbeat': None, 'retries': 0}
        for i in range(1, num_testers + 1):
            statuses[f'tester_{i}'] = {'status': 'unknown', 'last_heartbeat': None, 'retries': 0}
        return statuses

    def check_all_agents(self):
        """
        Runs a health check on all registered agents.
        This is the main monitoring loop.
        """
        print("Running agent health check cycle...")
        for agent_id, status in self.agent_statuses.items():
            # In a real system, we'd check a heartbeat file, a DB timestamp, or a Redis key.
            is_healthy = self.check_agent_heartbeat(agent_id)

            if not is_healthy and status['status'] != 'failed':
                print(f"Agent {agent_id} appears to be down. Attempting restart...")
                self.handle_failed_agent(agent_id)
            elif is_healthy:
                status['status'] = 'healthy'
                status['retries'] = 0 # Reset retries on success

    def check_agent_heartbeat(self, agent_id):
        """
        Placeholder for checking a single agent's heartbeat.
        Returns True if healthy, False otherwise.
        """
        status = self.agent_statuses[agent_id]
        timeout = self.config['heartbeat_timeout_seconds']

        # Simulate checking a last-seen timestamp
        last_seen = status.get('last_heartbeat')
        if last_seen and (datetime.utcnow() - last_seen) > timedelta(seconds=timeout):
            return False # Agent timed out
        return True # Assume healthy for now

    def handle_failed_agent(self, agent_id):
        """
        Handles a failed agent based on the restart policy.
        """
        status = self.agent_statuses[agent_id]
        max_retries = self.config['max_restart_retries']

        if status['retries'] < max_retries:
            # restart_agent(agent_id)
            status['retries'] += 1
            print(f"Restart triggered for {agent_id}. Attempt {status['retries']}/{max_retries}.")
            # Implement backoff delay here if needed
        else:
            status['status'] = 'failed'
            print(f"Agent {agent_id} has failed permanently after {max_retries} retries.")

    def get_all_agent_statuses(self):
        """Returns the current status of all agents."""
        return self.agent_statuses
