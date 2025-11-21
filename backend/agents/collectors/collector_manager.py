import logging
import asyncio
from typing import Dict, Any
from .market_data import NSEDataCollector
from .technical import TechnicalIndicatorCollector
from .order_book import OrderBookAnalyzer
from .news_events import NewsEventCollector
from .historical import HistoricalDataManager

logger = logging.getLogger(__name__)

class CollectorManager:
    """
    Manages the lifecycle and execution of V2 Collector Agents.
    """
    def __init__(self):
        self.collectors = {}
        self.initialize_agents()
        
    def initialize_agents(self):
        """Initialize all 5 specialized collector agents."""
        try:
            self.collectors = {
                "market_data": NSEDataCollector(),
                "technical": TechnicalIndicatorCollector(),
                "order_book": OrderBookAnalyzer(),
                "news": NewsEventCollector(),
                "historical": HistoricalDataManager()
            }
            logger.info(f"Initialized {len(self.collectors)} V2 collector agents")
        except Exception as e:
            logger.error(f"Failed to initialize agents: {e}")
            
    async def run_all_collectors(self) -> Dict[str, Any]:
        """
        Run collection cycle.
        For V2, this means:
        1. Ensuring continuous collectors are running.
        2. Fetching point-in-time data (News, Events).
        3. Aggregating current market state.
        """
        logger.info("Starting V2 collection cycle...")
        
        summary = {
            "total_collected": 0,
            "status": "success",
            "details": {}
        }
        
        try:
            # 1. Market Data (Should be running continuously, but we check/start here)
            # For now, we'll just fetch a snapshot
            market_collector = self.collectors["market_data"]
            market_snapshot = market_collector.get_indices()
            summary["details"]["market_data"] = "active"
            
            # 2. News & Events
            news_collector = self.collectors["news"]
            events = news_collector.get_economic_calendar()
            sentiment = news_collector.get_market_sentiment()
            summary["details"]["news"] = len(events)
            
            # 3. Order Book (Snapshot)
            ob_collector = self.collectors["order_book"]
            # Mock symbol for now
            ob = ob_collector.get_order_book("NIFTY")
            summary["details"]["order_book"] = "captured"
            
            # 4. Technicals (On current price)
            tech_collector = self.collectors["technical"]
            # Mock price data
            rsi = tech_collector.calculate_rsi([100, 101, 102, 101, 100])
            summary["details"]["technical"] = "calculated"
            
            logger.info("V2 Collection cycle completed.")
            return summary
            
        except Exception as e:
            logger.error(f"Collection cycle failed: {e}")
            summary["status"] = "failed"
            summary["error"] = str(e)
            return summary

    def get_agent_statuses(self):
        """Get status of all agents."""
        statuses = []
        for key, agent in self.collectors.items():
            statuses.append({
                "id": key,
                "name": agent.name,
                "status": agent.status,
                "type": "Collector"
            })
        return statuses

    def save_agent_statuses(self):
        """Save current status of all agents to status.json"""
        try:
            import json
            import os
            from datetime import datetime
            
            # Path to status file
            # Assuming relative path from backend/agents/collectors/collector_manager.py
            # to backend/data/status.json
            status_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/status.json'))
            
            statuses = []
            for key, agent in self.collectors.items():
                statuses.append({
                    "id": key,
                    "name": agent.name,
                    "type": "Collector",
                    "status": agent.status,
                    "activity": "Active",
                    "last_updated": datetime.now().isoformat()
                })
                
            with open(status_file, 'w') as f:
                json.dump(statuses, f, indent=2)
                
        except Exception as e:
            logger.error(f"Failed to save agent statuses: {e}")

