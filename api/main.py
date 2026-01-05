from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
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

# Initialize FastAPI
app = FastAPI(
    title="AI Research Assistant API",
    description="Multi-agent AI system with security",
    version="2.0.0"
)

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
        "message": "AI Research Assistant API v2.0",
        "security": "API Key required for protected endpoints",
        "get_key": "Use 'dev_key_123' for testing",
        "endpoints": {
            "research": "/research (Protected)",
            "summarize": "/summarize (Protected)",
            "verify": "/verify (Protected)",
            "complete": "/complete (Protected)"
        }
    }

@app.post("/research")
def research_endpoint(
    request: ResearchRequest,
    api_key_info: dict = Depends(verify_api_key)
):
    """Research with API key protection"""
    log_request("/research", api_key_info, request.query)
    
    try:
        result = research(request.query)
        return {
            "status": "success",
            "query": request.query,
            "research": result,
            "usage": f"{api_key_info['usage']}/{api_key_info['limit']}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize")
def summarize_endpoint(
    request: SummaryRequest,
    api_key_info: dict = Depends(verify_api_key)
):
    """Summarize with API key protection"""
    log_request("/summarize", api_key_info)
    
    try:
        result = summarizer.summarize(request.text, request.summary_type)
        return {
            "status": "success",
            "result": result,
            "usage": f"{api_key_info['usage']}/{api_key_info['limit']}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/verify")
def verify_endpoint(
    request: VerifyRequest,
    api_key_info: dict = Depends(verify_api_key)
):
    """Fact-check with API key protection"""
    log_request("/verify", api_key_info)
    
    try:
        result = fact_checker.verify_claims(request.text)
        return {
            "status": "success",
            "verification": result,
            "usage": f"{api_key_info['usage']}/{api_key_info['limit']}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/complete")
def complete_endpoint(
    request: ResearchRequest,
    api_key_info: dict = Depends(verify_api_key)
):
    """Complete workflow with API key protection"""
    log_request("/complete", api_key_info, request.query)
    
    try:
        result = orchestrator.research_complete(request.query)
        result["usage"] = f"{api_key_info['usage']}/{api_key_info['limit']}"
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """Public health check (no API key needed)"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
