# backend/agents/testers/run_testers.py
import os
import sys

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from backend.agents.testers.tester_1 import TesterAgent1
from backend.agents.testers.tester_2 import TesterAgent2
from backend.agents.testers.tester_3 import TesterAgent3
from backend.agents.testers.tester_4 import TesterAgent4
from backend.agents.testers.tester_5 import TesterAgent5
from backend.agents.testers.tester_6 import TesterAgent6
from backend.agents.testers.tester_7 import TesterAgent7
from backend.agents.testers.tester_8 import TesterAgent8
from backend.agents.testers.tester_9 import TesterAgent9
from backend.agents.testers.tester_10 import TesterAgent10

def run_all_testers():
    print("Starting all Tester Agents...")
    
    input_dir = "backend/data/inbox"
    output_dir = "backend/data/results"
    
    # Ensure directories exist
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    agents = [
        TesterAgent1("tester_1", input_dir, output_dir),
        TesterAgent2("tester_2", input_dir, output_dir),
        TesterAgent3("tester_3", input_dir, output_dir),
        TesterAgent4("tester_4", input_dir, output_dir),
        TesterAgent5("tester_5", input_dir, output_dir),
        TesterAgent6("tester_6", input_dir, output_dir),
        TesterAgent7("tester_7", input_dir, output_dir),
        TesterAgent8("tester_8", input_dir, output_dir),
        TesterAgent9("tester_9", input_dir, output_dir),
        TesterAgent10("tester_10", input_dir, output_dir),
    ]

    for agent in agents:
        print(f"\n--- Running {agent.agent_id} ---")
        try:
            agent.run()
        except Exception as e:
            print(f"Error running {agent.agent_id}: {e}")

    print("\nAll Tester Agents finished.")

if __name__ == "__main__":
    run_all_testers()
