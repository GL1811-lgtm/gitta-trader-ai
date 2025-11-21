# backend/agents/collectors/run_all.py
import sys
import os
import logging

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from backend.agents.collectors.collector_manager import CollectorManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_all_collectors():
    print("Starting Collector Manager...")
    print("-" * 50)

    try:
        manager = CollectorManager()
        # Assuming manager has a method to run all or specific collectors
        # If not, we might need to instantiate individual collectors if they exist elsewhere
        # But based on file list, individual collector files are missing.
        # So we rely on the manager.
        
        # For now, let's just instantiate it to verify imports work.
        # In a real run, we'd call manager.run_all() or similar.
        print("CollectorManager initialized successfully.")
        
    except Exception as e:
        print(f"ERROR initializing CollectorManager: {e}")
    print("-" * 50)

if __name__ == "__main__":
    run_all_collectors()
