from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from slowapi.errors import RateLimitExceeded
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.researcher import research
from agents.summarizer import SummarizerAgent
from agents.fact_checker import FactCheckerAgent
from agents.orchestrator import OrchestratorAgent
from auth import verify_api_key
from logging_config import log_request
from rate_limiter import limiter, rate_limit_handler
from cache_manager import get_from_cache, save_to_cache, get_cache_stats, clear_cache

# Initialize FastAPI with rate limiter
app = FastAPI(
    title="AI Research Assistant API",
    description="Production-ready multi-agent AI system",
    version="3.0.0"
)

# Add rate limiter state
app.state.limiter = limiter

# Add rate limit exception handler
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
summarizer = SummarizerAgent()
fact_checker = FactCheckerAgent()
orchestrator = OrchestratorAgent()

# Request models
class ResearchRequest(BaseModel):
    query: str

class SummaryRequest(BaseModel):
    text: str
    summary_type: str = "brief"

class VerifyRequest(BaseModel):
    text: str

# API Endpoints
@app.get("/")
def root():
    return {
        "message": "AI Research Assistant API v3.0",
        "features": ["Authentication", "Rate Limiting", "Caching", "Monitoring"],
        "test_key": "dev_key_123",
        "endpoints": {
            "research": "/research (Protected, Cached, Rate Limited)",
            "summarize": "/summarize (Protected, Rate Limited)",
            "verify": "/verify (Protected, Rate Limited)",
            "complete": "/complete (Protected, Rate Limited)",
            "stats": "/stats (Public)",
            "health": "/health (Public)"
        }
    }

@app.post("/research")
@limiter.limit("10/minute")  # 10 requests per minute per IP
def research_endpoint(
    request: Request,
    research_req: ResearchRequest,
    api_key_info: dict = Depends(verify_api_key)
):
    """Research with caching, rate limiting, and authentication"""
    log_request("/research", api_key_info, research_req.query)
    
    # Check cache first
    cached_result = get_from_cache(research_req.query)
    if cached_result:
        cached_result["usage"] = f"{api_key_info['usage']}/{api_key_info['limit']}"
        return cached_result
    
    # If not cached, perform research
    try:
        result = research(research_req.query)
        response = {
            "status": "success",
            "query": research_req.query,
            "research": result,
            "usage": f"{api_key_info['usage']}/{api_key_info['limit']}"
        }
        
        # Save to cache
        return save_to_cache(research_req.query, response)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize")
@limiter.limit("20/minute")
def summarize_endpoint(
    request: Request,
    summary_req: SummaryRequest,
    api_key_info: dict = Depends(verify_api_key)
):
    """Summarize with rate limiting"""
    log_request("/summarize", api_key_info)
    
    try:
        result = summarizer.summarize(summary_req.text, summary_req.summary_type)
        return {
            "status": "success",
            "result": result,
            "usage": f"{api_key_info['usage']}/{api_key_info['limit']}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/verify")
@limiter.limit("15/minute")
def verify_endpoint(
    request: Request,
    verify_req: VerifyRequest,
    api_key_info: dict = Depends(verify_api_key)
):
    """Fact-check with rate limiting"""
    log_request("/verify", api_key_info)
    
    try:
        result = fact_checker.verify_claims(verify_req.text)
        return {
            "status": "success",
            "verification": result,
            "usage": f"{api_key_info['usage']}/{api_key_info['limit']}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/complete")
@limiter.limit("5/minute")
def complete_endpoint(
    request: Request,
    research_req: ResearchRequest,
    api_key_info: dict = Depends(verify_api_key)
):
    """Complete workflow with strict rate limiting"""
    log_request("/complete", api_key_info, research_req.query)
    
    try:
        result = orchestrator.research_complete(research_req.query)
        result["usage"] = f"{api_key_info['usage']}/{api_key_info['limit']}"
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
def stats_endpoint():
    """Get API statistics (public endpoint)"""
    return {
        "cache_stats": get_cache_stats(),
        "rate_limits": {
            "research": "10 requests/minute",
            "summarize": "20 requests/minute",
            "verify": "15 requests/minute",
            "complete": "5 requests/minute"
        }
    }

@app.delete("/cache")
def clear_cache_endpoint(api_key_info: dict = Depends(verify_api_key)):
    """Clear cache (protected endpoint)"""
    return clear_cache()

@app.get("/health")
@limiter.limit("100/minute")
def health_check(request: Request):
    """Health check with generous rate limit"""
    return {
        "status": "healthy",
        "version": "3.0.0",
        "features": ["auth", "rate_limiting", "caching"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

