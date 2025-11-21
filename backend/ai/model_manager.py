"""
AI Model Manager
Manages AI model usage, statistics, and fallback mechanisms
"""

import os
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict
import json

from backend.ai.config.models_config import (
    get_all_models,
    get_active_models,
    get_model_by_id,
    get_trading_models
)

class ModelManager:
    """Manages AI models, tracks usage, and implements fallback logic"""
    
    def __init__(self):
        self.usage_stats = defaultdict(lambda: {
            "total_calls": 0,
            "successful_calls": 0,
            "failed_calls": 0,
            "total_duration": 0.0,
            "average_duration": 0.0,
            "last_used": None,
            "error_count": 0,
            "rate_limit_hits": 0
        })
        self.rate_limits = defaultdict(lambda: {
            "calls_per_minute": 0,
            "last_reset": datetime.now(),
            "current_count": 0
        })
    
    def record_usage(self, model_id: str, duration: float, success: bool, error: Optional[str] = None):
        """
        Record usage statistics for a model
        
        Args:
            model_id: ID of the model
            duration: Request duration in seconds
            success: Whether the request was successful
            error: Error message if failed
        """
        stats = self.usage_stats[model_id]
        
        stats["total_calls"] += 1
        stats["total_duration"] += duration
        stats["last_used"] = datetime.now().isoformat()
        
        if success:
            stats["successful_calls"] += 1
        else:
            stats["failed_calls"] += 1
            stats["error_count"] += 1
        
        # Update average duration
        if stats["total_calls"] > 0:
            stats["average_duration"] = stats["total_duration"] / stats["total_calls"]
        
        # Check if it's a rate limit error
        if error and ("rate" in error.lower() or "limit" in error.lower()):
            stats["rate_limit_hits"] += 1
    
    def get_model_stats(self, model_id: Optional[str] = None) -> Dict:
        """
        Get usage statistics for a model or all models
        
        Args:
            model_id: Optional model ID, if None returns all stats
            
        Returns:
            Dictionary of statistics
        """
        if model_id:
            return dict(self.usage_stats.get(model_id, {}))
        return dict(self.usage_stats)
    
    def get_best_performing_models(self, top_n: int = 5) -> List[Dict]:
        """
        Get top performing models based on success rate and speed
        
        Args:
            top_n: Number of top models to return
            
        Returns:
            List of model stats sorted by performance
        """
        model_scores = []
        
        for model_id, stats in self.usage_stats.items():
            if stats["total_calls"] == 0:
                continue
            
            success_rate = stats["successful_calls"] / stats["total_calls"]
            avg_duration = stats["average_duration"]
            
            # Score: 70% success rate + 30% speed (inverse of duration)
            # Normalize duration to 0-1 scale (assume max 30 seconds)
            normalized_speed = max(0, 1 - (avg_duration / 30))
            score = (success_rate * 0.7) + (normalized_speed * 0.3)
            
            model_scores.append({
                "model_id": model_id,
                "score": score,
                "success_rate": success_rate,
                "avg_duration": avg_duration,
                "total_calls": stats["total_calls"]
            })
        
        # Sort by score descending
        model_scores.sort(key=lambda x: x["score"], reverse=True)
        return model_scores[:top_n]
    
    def check_rate_limit(self, model_id: str, limit: int = 60) -> bool:
        """
        Check if model has hit rate limit
        
        Args:
            model_id: Model ID to check
            limit: Calls per minute limit
            
        Returns:
            True if under limit, False if exceeded
        """
        rate_info = self.rate_limits[model_id]
        now = datetime.now()
        
        # Reset counter if a minute has passed
        time_diff = (now - rate_info["last_reset"]).total_seconds()
        if time_diff >= 60:
            rate_info["current_count"] = 0
            rate_info["last_reset"] = now
        
        # Check limit
        if rate_info["current_count"] >= limit:
            return False
        
        # Increment counter
        rate_info["current_count"] += 1
        rate_info["calls_per_minute"] = rate_info["current_count"]
        
        return True
    
    def get_fallback_model(self, failed_model_id: str) -> Optional[Dict]:
        """
        Get a fallback model when primary model fails
        
        Args:
            failed_model_id: ID of the model that failed
            
        Returns:
            Fallback model config or None
        """
        # Get failed model info
        failed_model = get_model_by_id(failed_model_id)
        if not failed_model:
            return None
        
        # Get models from same tier
        active_models = get_active_models()
        same_tier_models = [
            m for m in active_models 
            if m["tier"] == failed_model["tier"] and m["id"] != failed_model_id
        ]
        
        if same_tier_models:
            # Return model with best performance from same tier
            best_model = None
            best_score = -1
            
            for model in same_tier_models:
                stats = self.usage_stats.get(model["id"])
                if stats and stats["total_calls"] > 0:
                    success_rate = stats["successful_calls"] / stats["total_calls"]
                    if success_rate > best_score:
                        best_score = success_rate
                        best_model = model
            
            if best_model:
                return best_model
            
            # If no stats, return first available
            return same_tier_models[0]
        
        # If no same-tier models, return any active model
        other_models = [m for m in active_models if m["id"] != failed_model_id]
        if other_models:
            return other_models[0]
        
        return None
    
    def reset_stats(self, model_id: Optional[str] = None):
        """Reset statistics for a model or all models"""
        if model_id:
            if model_id in self.usage_stats:
                del self.usage_stats[model_id]
        else:
            self.usage_stats.clear()
    
    def export_stats(self, filepath: str):
        """Export statistics to JSON file"""
        stats_data = {
            "exported_at": datetime.now().isoformat(),
            "usage_stats": dict(self.usage_stats),
            "rate_limits": {
                k: {
                    "calls_per_minute": v["calls_per_minute"],
                    "last_reset": v["last_reset"].isoformat()
                }
                for k, v in self.rate_limits.items()
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(stats_data, f, indent=2)
    
    def get_summary(self) -> Dict:
        """Get overall usage summary"""
        total_calls = sum(s["total_calls"] for s in self.usage_stats.values())
        total_successful = sum(s["successful_calls"] for s in self.usage_stats.values())
        total_failed = sum(s["failed_calls"] for s in self.usage_stats.values())
        
        return {
            "total_models_used": len(self.usage_stats),
            "total_calls": total_calls,
            "total_successful": total_successful,
            "total_failed": total_failed,
            "overall_success_rate": total_successful / total_calls if total_calls > 0 else 0,
            "models_with_stats": list(self.usage_stats.keys())
        }


# Global model manager instance
model_manager = ModelManager()


if __name__ == "__main__":
    # Test model manager
    print("=" * 60)
    print("Model Manager Test")
    print("=" * 60)
    
    manager = ModelManager()
    
    # Simulate some usage
    manager.record_usage("model1", 2.5, True)
    manager.record_usage("model1", 3.0, True)
    manager.record_usage("model1", 2.8, False, "Timeout error")
    manager.record_usage("model2", 1.5, True)
    manager.record_usage("model2", 5.0, False, "Rate limit exceeded")
    
    # Get stats
    print("\nModel 1 Stats:")
    print(json.dumps(manager.get_model_stats("model1"), indent=2))
    
    print("\nBest Performing Models:")
    for model in manager.get_best_performing_models(top_n=3):
        print(f"  {model['model_id']}: Score {model['score']:.2f}, Success {model['success_rate']*100:.1f}%")
    
    print("\nOverall Summary:")
    print(json.dumps(manager.get_summary(), indent=2))
    
    print("\n✅ Model Manager working correctly!")
