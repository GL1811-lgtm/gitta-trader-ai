import time
from typing import Any, Optional, Dict
from datetime import datetime
from backend.utils.logger import logger

class CacheManager:
    """
    Enhanced caching layer with TTL and statistics.
    """
    
    def __init__(self):
        self.cache = {}
        self.cache_metadata = {}
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0
        }
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if key not in self.cache:
            self.stats['misses'] += 1
            return None
        
        # Check if expired
        metadata = self.cache_metadata.get(key)
        if metadata and metadata['expires_at'] < time.time():
            self.delete(key)
            self.stats['misses'] += 1
            self.stats['evictions'] += 1
            return None
        
        self.stats['hits'] += 1
        
        # Update access time
        if metadata:
            metadata['last_accessed'] = time.time()
            metadata['access_count'] += 1
        
        return self.cache[key]
    
    def set(self, key: str, value: Any, ttl_seconds: int = 300):
        """Set value in cache with TTL."""
        self.cache[key] = value
        self.cache_metadata[key] = {
            'created_at': time.time(),
            'expires_at': time.time() + ttl_seconds,
            'last_accessed': time.time(),
            'access_count': 0,
            'ttl': ttl_seconds
        }
    
    def delete(self, key: str):
        """Delete value from cache."""
        if key in self.cache:
            del self.cache[key]
            del self.cache_metadata[key]
    
    def clear(self):
        """Clear all cache."""
        count = len(self.cache)
        self.cache.clear()
        self.cache_metadata.clear()
        logger.info(f"Cache cleared: {count} items removed")
    
    def cleanup_expired(self):
        """Remove expired entries."""
        current_time = time.time()
        expired_keys = [
            key for key, meta in self.cache_metadata.items()
            if meta['expires_at'] < current_time
        ]
        
        for key in expired_keys:
            self.delete(key)
            self.stats['evictions'] += 1
        
        if expired_keys:
            logger.info(f"Cache cleanup: {len(expired_keys)} expired items removed")
    
    def get_stats(self) -> Dict:
        """Get cache statistics."""
        total_requests = self.stats['hits'] + self.stats['misses']
        hit_rate = (self.stats['hits'] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            'size': len(self.cache),
            'hits': self.stats['hits'],
            'misses': self.stats['misses'],
            'evictions': self.stats['evictions'],
            'hit_rate_percent': round(hit_rate, 2),
            'total_requests': total_requests
        }
    
    def get_cache_info(self) -> Dict:
        """Get detailed cache information."""
        # Find most accessed items
        items = [
            {
                'key': key,
                'access_count': meta['access_count'],
                'age_seconds': round(time.time() - meta['created_at'], 2),
                'ttl_remaining': round(meta['expires_at'] - time.time(), 2)
            }
            for key, meta in self.cache_metadata.items()
        ]
        
        most_accessed = sorted(items, key=lambda x: x['access_count'], reverse=True)[:10]
        
        return {
            'total_items': len(self.cache),
            'most_accessed': most_accessed,
            'stats': self.get_stats()
        }

# Global cache instance
cache_manager = CacheManager()
