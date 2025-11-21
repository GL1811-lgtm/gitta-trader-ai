# backend/agents/testers/run_testers.py
import os
import sys
import logging

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from backend.agents.testers.tester_manager import TesterManager

logging.basicConfig(level=logging.INFO)

def run_all_testers():
    print("Starting Tester Manager...")
    
    try:
        manager = TesterManager()
        print("TesterManager initialized successfully.")
        # In a real scenario, we would call manager.test_population() here
        
    except Exception as e:
        print(f"Error initializing TesterManager: {e}")

    print("\nTester Manager check finished.")

if __name__ == "__main__":
    run_all_testers()
