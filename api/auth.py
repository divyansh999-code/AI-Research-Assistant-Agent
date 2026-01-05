from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from datetime import datetime
import os

# API Key configuration
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# In production, store this in database. For now, environment variable.
VALID_API_KEYS = {
    os.getenv("API_KEY_1", "dev_key_123"): {"name": "Development", "usage_limit": 100},
    os.getenv("API_KEY_2", "demo_key_456"): {"name": "Demo", "usage_limit": 50}
}

# Usage tracking (in-memory for demo, use Redis/DB in production)
usage_tracker = {}

async def verify_api_key(api_key: str = Security(api_key_header)):
    """Verify API key and track usage"""
    
    # Check if API key provided
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key required. Add 'X-API-Key' header with your key."
        )
    
    # Check if API key is valid
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    
    # Track usage
    if api_key not in usage_tracker:
        usage_tracker[api_key] = {"count": 0, "first_used": datetime.now()}
    
    usage_tracker[api_key]["count"] += 1
    
    # Check usage limit
    limit = VALID_API_KEYS[api_key]["usage_limit"]
    current_usage = usage_tracker[api_key]["count"]
    
    if current_usage > limit:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Usage limit exceeded. Limit: {limit} requests."
        )
    
    return {
        "api_key": api_key,
        "name": VALID_API_KEYS[api_key]["name"],
        "usage": current_usage,
        "limit": limit
    }
