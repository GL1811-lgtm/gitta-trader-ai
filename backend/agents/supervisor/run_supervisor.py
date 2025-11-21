# backend/agents/supervisor/run_supervisor.py
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from backend.agents.supervisor.supervisor_agent import SupervisorAgent

if __name__ == "__main__":
    print("Launching Supervisor Agent in Continuous Mode...")
    supervisor = SupervisorAgent()
    import asyncio
    asyncio.run(supervisor.run_continuous_mode())
