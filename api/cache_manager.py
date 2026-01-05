from cachetools import TTLCache
import hashlib
import json
from datetime import datetime

# Cache configuration
# TTL = Time To Live (5 minutes = 300 seconds)
# maxsize = Maximum number of cached items
research_cache = TTLCache(maxsize=100, ttl=300)
cache_stats = {"hits": 0, "misses": 0, "total_requests": 0}

def get_cache_key(query: str) -> str:
    """Generate unique cache key from query"""
    return hashlib.md5(query.lower().strip().encode()).hexdigest()

def get_from_cache(query: str):
    """Get cached response if available"""
    cache_stats["total_requests"] += 1
    key = get_cache_key(query)
    
    if key in research_cache:
        cache_stats["hits"] += 1
        cached_item = research_cache[key]
        cached_item["cached"] = True
        cached_item["cached_at"] = cached_item.get("timestamp", "unknown")
        return cached_item
    
    cache_stats["misses"] += 1
    return None

def save_to_cache(query: str, result: dict):
    """Save response to cache"""
    key = get_cache_key(query)
    result["timestamp"] = datetime.now().isoformat()
    result["cached"] = False
    research_cache[key] = result
    return result

def get_cache_stats():
    """Get cache statistics"""
    hit_rate = (cache_stats["hits"] / cache_stats["total_requests"] * 100) if cache_stats["total_requests"] > 0 else 0
    return {
        "cache_size": len(research_cache),
        "max_size": research_cache.maxsize,
        "ttl_seconds": research_cache.ttl,
        "total_requests": cache_stats["total_requests"],
        "cache_hits": cache_stats["hits"],
        "cache_misses": cache_stats["misses"],
        "hit_rate": f"{hit_rate:.2f}%"
    }

def clear_cache():
    """Clear all cached data"""
    research_cache.clear()
    cache_stats["hits"] = 0
    cache_stats["misses"] = 0
    cache_stats["total_requests"] = 0
    return {"message": "Cache cleared successfully"}
