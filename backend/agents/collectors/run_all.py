# backend/agents/collectors/run_all.py
import sys
import os

# Add the project root to the python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

from backend.agents.collectors.collector_1 import CollectorAgent1
from backend.agents.collectors.collector_2 import CollectorAgent2
from backend.agents.collectors.collector_3 import CollectorAgent3
from backend.agents.collectors.collector_4 import CollectorAgent4
from backend.agents.collectors.collector_5 import CollectorAgent5
from backend.agents.collectors.collector_6 import CollectorAgent6
from backend.agents.collectors.collector_7 import CollectorAgent7
from backend.agents.collectors.collector_8 import CollectorAgent8
from backend.agents.collectors.collector_9 import CollectorAgent9
from backend.agents.collectors.collector_10 import CollectorAgent10

def run_all_collectors():
    collectors = [
        CollectorAgent1("collector_1", "backend/data/inbox"),
        CollectorAgent2("collector_2", "backend/data/inbox"),
        CollectorAgent3("collector_3", "backend/data/inbox"),
        CollectorAgent4("collector_4", "backend/data/inbox"),
        CollectorAgent5("collector_5", "backend/data/inbox"),
        CollectorAgent6("collector_6", "backend/data/inbox"),
        CollectorAgent7("collector_7", "backend/data/inbox"),
        CollectorAgent8("collector_8", "backend/data/inbox"),
        CollectorAgent9("collector_9", "backend/data/inbox"),
        CollectorAgent10("collector_10", "backend/data/inbox"),
    ]

    print("Starting Collector Agents Verification...")
    print("-" * 50)

    for collector in collectors:
        try:
            print(f"Running {collector.agent_id}...")
            sources = collector.fetch_sources()
            print(f"  Found {len(sources)} items.")
            for item in sources:
                print(f"    - {item.get('title', 'No Title')} ({item.get('source', 'Unknown Source')})")
                collector.save_strategy(item)
            
        except Exception as e:
            print(f"  ERROR running {collector.agent_id}: {e}")
        print("-" * 50)

if __name__ == "__main__":
    run_all_collectors()
