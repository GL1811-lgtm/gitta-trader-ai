# backend/agents/expert/run_expert.py
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from backend.agents.expert.expert_agent import ExpertAgent

if __name__ == "__main__":
    print("Launching Expert Agent...")
    agent = ExpertAgent()
    agent.run()
