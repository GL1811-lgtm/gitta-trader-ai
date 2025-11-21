import time
from datetime import datetime, timedelta
from backend.database.db import db
from backend.evolution.population import Population
from backend.trading.paper_engine import PaperTradingEngine
from backend.utils.logger import logger

class ValidationManager:
    """
    Manages paper trading validation sessions for evolved strategies.
    """
    def __init__(self, population: Population, num_strategies=3, duration_days=5):
        self.population = population
        self.num_strategies = num_strategies
        self.duration_days = duration_days
        self.session_id = None
        self.active = False
        
    def start_validation(self):
        """Start a new validation session with top evolved strategies."""
        # Get best organisms
        organisms = sorted(self.population.organisms, key=lambda o: o.fitness, reverse=True)
        top_organisms = organisms[:self.num_strategies]
        
        # Create session
        self.session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        start_time = datetime.now()
        end_time = start_time + timedelta(days=self.duration_days)
        
        logger.info(f"Starting validation session: {self.session_id}")
        logger.info(f"Testing {len(top_organisms)} strategies for {self.duration_days} days")
        
        # Log session to database
        db.create_validation_session(
            session_id=self.session_id,
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            num_strategies=len(top_organisms)
        )
        
        # Log each strategy being tested
        for i, organism in enumerate(top_organisms):
            db.log_validation_strategy(
                session_id=self.session_id,
                strategy_id=f"org_{i}",
                dna=organism.dna,
                initial_fitness=organism.fitness
            )
        
        self.active = True
        return {
            "session_id": self.session_id,
            "strategies": len(top_organisms),
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat()
        }
    
    def get_session_status(self):
        """Get current validation session status."""
        if not self.session_id:
            return {"active": False, "message": "No active session"}
        
        session = db.get_validation_session(self.session_id)
        if not session:
            return {"active": False, "message": "Session not found"}
        
        # Calculate progress
        start = datetime.fromisoformat(session['start_time'])
        end = datetime.fromisoformat(session['end_time'])
        now = datetime.now()
        
        if now >= end:
            self.active = False
            progress = 100
        else:
            total_duration = (end - start).total_seconds()
            elapsed = (now - start).total_seconds()
            progress = min(100, (elapsed / total_duration) * 100)
        
        return {
            "active": self.active,
            "session_id": self.session_id,
            "progress": round(progress, 2),
            "start_time": session['start_time'],
            "end_time": session['end_time'],
            "days_remaining": max(0, (end - now).days)
        }
    
    def stop_validation(self):
        """Stop the current validation session."""
        if self.session_id:
            db.update_validation_session(self.session_id, status='stopped')
            logger.info(f"Stopped validation session: {self.session_id}")
            self.active = False
            return {"message": "Session stopped", "session_id": self.session_id}
        return {"message": "No active session to stop"}
