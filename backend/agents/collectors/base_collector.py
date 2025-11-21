from abc import ABC, abstractmethod
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# Try to import multi-AI verification (optional)
try:
    from backend.ai.multi_ai_verifier import MultiAIVerifier
    from backend.ai.consensus_engine import ConsensusEngine
    MULTI_AI_AVAILABLE = True
except ImportError:
    logger.warning("Multi-AI verification not available")
    MULTI_AI_AVAILABLE = False
    MultiAIVerifier = None
    ConsensusEngine = None

class BaseCollectorAgent(ABC):
    """
    Base class for all Collector Agents.
    Each collector searches specific sources for trading strategies.
    Includes multi-AI verification before saving strategies.
    """
    
    def __init__(self, agent_id, source_name, confidence_threshold=70.0):
        self.agent_id = agent_id
        self.source_name = source_name
        self.status = "initialized"
        self.last_run = None
        self.confidence_threshold = confidence_threshold
        
        # Initialize multi-AI verifier if available
        if MULTI_AI_AVAILABLE:
            try:
                self.verifier = MultiAIVerifier()
                self.consensus_engine = ConsensusEngine()
                self.verification_enabled = True
                logger.info(f"[{self.agent_id}] Multi-AI verification enabled")
            except Exception as e:
                logger.warning(f"[{self.agent_id}] Could not initialize multi-AI: {e}")
                self.verification_enabled = False
        else:
            self.verification_enabled = False
            
        # FORCE DISABLE FOR DEBUGGING
        self.verification_enabled = False
        
    @abstractmethod
    def collect(self):
        """
        Main collection method. Returns list of strategies.
        Each strategy should be a dict with:
        - title: str
        - content: str
        - url: str (optional)
        - source: str
        """
        pass
    
    def verify_strategy(self, strategy: dict) -> dict:
        """
        Verify a strategy using multi-AI verification
        
        Args:
            strategy: Strategy dict with title and content
            
        Returns:
            Dict with verification results and decision
        """
        if not self.verification_enabled:
            return {
                "verified": True,
                "confidence": 100.0,
                "reason": "Multi-AI verification disabled",
                "verification_data": None
            }
        
        try:
            # Prepare strategy text for verification
            strategy_text = f"{strategy.get('title', 'Unknown Strategy')}\\n\\n{strategy.get('content', '')}"
            
            # Verify with multi-AI
            logger.info(f"[{self.agent_id}] Verifying strategy with {8} AI models...")
            verification_result = self.verifier.verify_strategy(strategy_text)
            
            # Calculate consensus
            consensus = self.consensus_engine.calculate_consensus(verification_result['responses'])
            
            # Determine if strategy passes threshold
            confidence = consensus.get('confidence', 0.0)
            passes_threshold = confidence >= self.confidence_threshold
            
            verification_decision = {
                "verified": passes_threshold,
                "confidence": confidence,
                "consensus_recommendation": consensus.get('consensus_recommendation', 'UNKNOWN'),
                "average_score": consensus.get('average_score', 0.0),
                "agreement_rate": consensus.get('agreement_rate', 0.0),
                "reason": consensus.get('interpretation', ''),
                "verification_data": {
                    "timestamp": datetime.now().isoformat(),
                    "total_models": verification_result['total_models'],
                    "successful_responses": verification_result['successful_responses'],
                    "failed_responses": verification_result['failed_responses'],
                    "total_duration": verification_result['total_duration'],
                    "responses": verification_result['responses'],
                    "consensus": consensus
                }
            }
            
            if passes_threshold:
                logger.info(
                    f"[{self.agent_id}] Strategy VERIFIED - "
                    f"Confidence: {confidence:.1f}%, "
                    f"Recommendation: {consensus.get('consensus_recommendation')}"
                )
            else:
                logger.warning(
                    f"[{self.agent_id}] Strategy REJECTED - "
                    f"Confidence: {confidence:.1f}% < Threshold: {self.confidence_threshold}%"
                )
            
            return verification_decision
            
        except Exception as e:
            logger.error(f"[{self.agent_id}] Verification error: {e}")
            return {
                "verified": False,
                "confidence": 0.0,
                "reason": f"Verification failed: {str(e)}",
                "verification_data": None
            }
    
    def run(self):
        """Execute collection and return results with verification."""
        try:
            logger.info(f"[{self.agent_id}] Starting collection from {self.source_name}...")
            self.status = "running"
            
            # Collect strategies
            strategies = self.collect()
            logger.info(f"[{self.agent_id}] Collected {len(strategies)} strategies")
            
            # Log collection event
            from backend.database.db import db
            db.log_agent_activity(
                self.agent_id, 
                "COLLECTION", 
                f"Collected {len(strategies)} strategies from {self.source_name}",
                {"count": len(strategies)}
            )
            
            # Verify each strategy
            verified_strategies = []
            rejected_strategies = []
            
            for i, strategy in enumerate(strategies, 1):
                logger.info(f"[{self.agent_id}] Verifying strategy {i}/{len(strategies)}: {strategy.get('title', 'Untitled')}")
                
                verification = self.verify_strategy(strategy)
                
                # Add verification data to strategy
                strategy['verification'] = verification
                strategy['collected_at'] = datetime.now().isoformat()
                strategy['collector_id'] = self.agent_id
                strategy['source'] = self.source_name
                
                if verification['verified']:
                    verified_strategies.append(strategy)
                else:
                    rejected_strategies.append(strategy)
            
            self.status = "completed"
            self.last_run = datetime.now()
            
            logger.info(
                f"[{self.agent_id}] Collection completed - "
                f"Verified: {len(verified_strategies)}, "
                f"Rejected: {len(rejected_strategies)}"
            )
            
            return {
                "total_collected": len(strategies),
                "verified": verified_strategies,
                "rejected": rejected_strategies,
                "verification_enabled": self.verification_enabled
            }
            
        except Exception as e:
            self.status = "failed"
            logger.error(f"[{self.agent_id}] Collection failed: {e}")
            return {
                "total_collected": 0,
                "verified": [],
                "rejected": [],
                "error": str(e)
            }
    
    def get_status(self):
        """Return agent status info."""
        return {
            "agent_id": self.agent_id,
            "source": self.source_name,
            "status": self.status,
            "last_run": str(self.last_run) if self.last_run else None,
            "verification_enabled": self.verification_enabled,
            "confidence_threshold": self.confidence_threshold
        }
    
    def update_status(self, status, activity=None):
        """Update agent status in the shared status file."""
        try:
            import json
            import os
            
            self.status = status
            
            # Path to status file
            status_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../data/status.json'))
            
            # Read existing status
            current_status = []
            if os.path.exists(status_file):
                try:
                    with open(status_file, 'r') as f:
                        current_status = json.load(f)
                except:
                    current_status = []
            
            # Update or add this agent's status
            updated = False
            for agent in current_status:
                if agent.get('id') == self.agent_id:
                    agent['status'] = status
                    agent['last_updated'] = datetime.now().isoformat()
                    if activity:
                        agent['activity'] = activity
                    updated = True
                    break
            
            if not updated:
                current_status.append({
                    "id": self.agent_id,
                    "name": f"Collector {self.agent_id.split('_')[-1].title()}",
                    "type": "Collector",
                    "status": status,
                    "activity": activity or "Initialized",
                    "last_updated": datetime.now().isoformat()
                })
            
            # Write back
            with open(status_file, 'w') as f:
                json.dump(current_status, f, indent=2)
                
            # Log to Database
            try:
                from backend.database.db import db
                db.log_agent_activity(
                    self.agent_id, 
                    "STATUS_UPDATE", 
                    f"Status changed to {status}", 
                    {"activity": activity}
                )
            except Exception as db_e:
                logger.error(f"[{self.agent_id}] Failed to log to DB: {db_e}")
                
        except Exception as e:
            logger.error(f"[{self.agent_id}] Failed to update status file: {e}")

    async def run_continuously(self, interval_minutes=15, max_iterations=None):
        """
        Run collector in continuous loop for 24/7 operation.
        
        Args:
            interval_minutes: Minutes between collection cycles (Ignored for now, using 10s)
            max_iterations: Maximum iterations (None for infinite)
        """
        import asyncio
        
        iteration = 0
        # Override interval to 10 seconds as requested
        interval_seconds = 10
        logger.info(f"[{self.agent_id}] Starting continuous mode - interval: {interval_seconds} seconds")
        
        while True:
            try:
                iteration += 1
                if max_iterations and iteration > max_iterations:
                    logger.info(f"[{self.agent_id}] Reached max iterations ({max_iterations})")
                    break
                
                logger.info(f"[{self.agent_id}] Continuous cycle #{iteration} starting...")
                self.update_status("Running", f"Collection Cycle #{iteration}")
                
                # Run collection
                result = self.run()
                
                # Log results
                logger.info(
                    f"[{self.agent_id}] Cycle #{iteration} complete - "
                    f"Collected: {result['total_collected']}, "
                    f"Verified: {len(result['verified'])}, "
                    f"Rejected: {len(result['rejected'])}"
                )
                
                # Save verified strategies to database
                if result['verified']:
                    from backend.database.db import db
                    for strategy in result['verified']:
                        try:
                            db.insert_strategy(
                                title=strategy.get('title', 'Unknown'),
                                content=strategy.get('content', ''),
                                url=strategy.get('url', ''),
                                source=self.source_name,
                                collector_id=self.agent_id,
                                verification_data=strategy.get('verification', {}),
                                verified=True,
                                confidence_score=strategy['verification'].get('confidence', 0.0)
                            )
                        except Exception as e:
                            logger.error(f"[{self.agent_id}] Failed to save strategy: {e}")
                
                # Update status to idle
                self.update_status("Idle", f"Waiting {interval_seconds}s")
                
                # Wait for next cycle
                logger.info(f"[{self.agent_id}] Waiting {interval_seconds} seconds until next cycle...")
                await asyncio.sleep(interval_seconds)
                
            except Exception as e:
                logger.error(f"[{self.agent_id}] Error in continuous cycle: {e}")
                self.update_status("Error", str(e))
                # Wait 10 seconds on error before retrying
                logger.info(f"[{self.agent_id}] Waiting 10 seconds before retry...")
                await asyncio.sleep(10)

