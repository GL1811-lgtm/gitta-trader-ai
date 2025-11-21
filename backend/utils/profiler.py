import time
import functools
import tracemalloc
from datetime import datetime
from typing import Dict, List, Callable
from backend.utils.logger import logger

class PerformanceProfiler:
    """
    Performance profiling utility for tracking execution time and memory usage.
    """
    
    def __init__(self):
        self.metrics = []
        self.function_stats = {}
        
    def profile(self, func: Callable):
        """Decorator to profile function execution time and memory."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Track memory before
            tracemalloc.start()
            
            # Track time
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
            finally:
                # Calculate metrics
                end_time = time.time()
                execution_time = end_time - start_time
                
                current, peak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                
                # Log metrics
                metric = {
                    'function': func.__name__,
                    'execution_time_ms': round(execution_time * 1000, 2),
                    'memory_current_mb': round(current / 1024 / 1024, 2),
                    'memory_peak_mb': round(peak / 1024 / 1024, 2),
                    'timestamp': datetime.now().isoformat()
                }
                
                self.metrics.append(metric)
                
                # Update function stats
                if func.__name__ not in self.function_stats:
                    self.function_stats[func.__name__] = {
                        'calls': 0,
                        'total_time_ms': 0,
                        'avg_time_ms': 0,
                        'max_time_ms': 0
                    }
                
                stats = self.function_stats[func.__name__]
                stats['calls'] += 1
                stats['total_time_ms'] += metric['execution_time_ms']
                stats['avg_time_ms'] = stats['total_time_ms'] / stats['calls']
                stats['max_time_ms'] = max(stats['max_time_ms'], metric['execution_time_ms'])
                
                # Log slow functions (>1s)
                if execution_time > 1.0:
                    logger.warning(f"SLOW FUNCTION: {func.__name__} took {execution_time:.2f}s")
            
            return result
        
        return wrapper
    
    def get_stats(self, limit=10) -> Dict:
        """Get performance statistics."""
        # Sort by average time
        sorted_functions = sorted(
            self.function_stats.items(),
            key=lambda x: x[1]['avg_time_ms'],
            reverse=True
        )[:limit]
        
        return {
            'total_metrics': len(self.metrics),
            'slowest_functions': [
                {
                    'name': name,
                    **stats
                }
                for name, stats in sorted_functions
            ],
            'recent_metrics': self.metrics[-20:] if self.metrics else []
        }
    
    def identify_bottlenecks(self, threshold_ms=500) -> List[Dict]:
        """Identify performance bottlenecks."""
        bottlenecks = []
        
        for name, stats in self.function_stats.items():
            if stats['avg_time_ms'] > threshold_ms:
                bottlenecks.append({
                    'function': name,
                    'avg_time_ms': round(stats['avg_time_ms'], 2),
                    'max_time_ms': round(stats['max_time_ms'], 2),
                    'calls': stats['calls'],
                    'severity': 'critical' if stats['avg_time_ms'] > 1000 else 'warning'
                })
        
        return sorted(bottlenecks, key=lambda x: x['avg_time_ms'], reverse=True)
    
    def reset(self):
        """Reset all metrics."""
        self.metrics = []
        self.function_stats = {}

# Global profiler instance
profiler = PerformanceProfiler()
