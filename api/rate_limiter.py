from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, Response
from fastapi.responses import JSONResponse

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Custom rate limit handler
def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> Response:
    """Custom response for rate limit exceeded"""
    return JSONResponse(
        status_code=429,
        content={
            "error": "Rate limit exceeded",
            "message": f"Too many requests. Try again in {exc.detail} seconds.",
            "retry_after": exc.detail
        }
    )
