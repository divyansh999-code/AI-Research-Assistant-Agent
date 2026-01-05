from fastapi import FastAPI, HTTPException
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

# Initialize FastAPI
app = FastAPI(
    title="AI Research Assistant API",
    description="Multi-agent AI system for autonomous research, summarization, and fact-checking",
    version="1.0.0"
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
    summary_type: str = "brief"  # brief, detailed, key_points, executive

class VerifyRequest(BaseModel):
    text: str

# API Endpoints
@app.get("/")
def root():
    return {
        "message": "AI Research Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "research": "/research",
            "summarize": "/summarize",
            "verify": "/verify",
            "complete": "/complete"
        }
    }

@app.post("/research")
def research_endpoint(request: ResearchRequest):
    """Research a topic using web search + LLM"""
    try:
        result = research(request.query)
        return {
            "status": "success",
            "query": request.query,
            "research": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/summarize")
def summarize_endpoint(request: SummaryRequest):
    """Summarize text in different formats"""
    try:
        result = summarizer.summarize(request.text, request.summary_type)
        return {
            "status": "success",
            "summary_type": request.summary_type,
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/verify")
def verify_endpoint(request: VerifyRequest):
    """Fact-check claims in text"""
    try:
        result = fact_checker.verify_claims(request.text)
        return {
            "status": "success",
            "verification": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/complete")
def complete_endpoint(request: ResearchRequest):
    """Complete research workflow (all agents)"""
    try:
        result = orchestrator.research_complete(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
