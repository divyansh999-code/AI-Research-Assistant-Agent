import os
import sys
from datetime import datetime
import time
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all agents
from agents.researcher import research
from agents.summarizer import SummarizerAgent
from agents.fact_checker import FactCheckerAgent

load_dotenv()


class OrchestratorAgent:
    """
    Orchestrates multiple AI agents to produce comprehensive research reports
    """
    
    def __init__(self):
        self.summarizer = SummarizerAgent()
        self.fact_checker = FactCheckerAgent()
    
    def research_complete(self, query: str) -> dict:
        """
        Execute complete research workflow with all agents
        
        Args:
            query: The research question
            
        Returns:
            Complete research report with all agent outputs
        """
        start_time = time.time()
        
        print(f"\n{'='*60}")
        print(f"🎯 ORCHESTRATING RESEARCH FOR: {query}")
        print(f"{'='*60}\n")
        
        report = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "status": "success",
            "agents_executed": []
        }
        
        try:
            # STEP 1: Research Agent
            print("📊 STEP 1/3: Running Researcher Agent...")
            research_start = time.time()
            
            research_result = research(query)
            research_time = time.time() - research_start
            
            report["research"] = {
                "content": research_result,
                "processing_time": f"{research_time:.2f}s",
                "status": "success"
            }
            report["agents_executed"].append("Researcher")
            print(f"✅ Research complete ({research_time:.2f}s)\n")
            
        except Exception as e:
            report["research"] = {"status": "failed", "error": str(e)}
            print(f"❌ Research failed: {e}\n")
        
        try:
            # STEP 2: Summarizer Agent (all 4 formats)
            print("📝 STEP 2/3: Running Summarizer Agent...")
            summary_start = time.time()
            
            summaries = {}
            for summary_type in ["brief", "detailed", "key_points", "executive"]:
                result = self.summarizer.summarize(
                    report["research"]["content"], 
                    summary_type
                )
                summaries[summary_type] = result
            
            summary_time = time.time() - summary_start
            
            report["summaries"] = {
    "brief": summaries["brief"].get("summary", str(summaries["brief"])),
    "detailed": summaries["detailed"].get("summary", str(summaries["detailed"])),
    "key_points": summaries["key_points"].get("summary", str(summaries["key_points"])),
    "executive": summaries["executive"].get("summary", str(summaries["executive"])),
    "compression_stats": {
        "brief": summaries["brief"].get("compression_ratio", "N/A"),
        "detailed": summaries["detailed"].get("compression_ratio", "N/A"),
        "key_points": summaries["key_points"].get("compression_ratio", "N/A"),
        "executive": summaries["executive"].get("compression_ratio", "N/A")
    },
    "processing_time": f"{summary_time:.2f}s",
    "status": "success"
}

            report["agents_executed"].append("Summarizer")
            print(f"✅ Summaries complete ({summary_time:.2f}s)\n")
            
        except Exception as e:
            report["summaries"] = {"status": "failed", "error": str(e)}
            print(f"❌ Summarization failed: {e}\n")
        
        try:
            # STEP 3: Fact-Checker Agent
            print("🔍 STEP 3/3: Running Fact-Checker Agent...")
            fact_check_start = time.time()
            
            verification = self.fact_checker.verify_claims(
                report["research"]["content"]
            )
            fact_check_time = time.time() - fact_check_start
            
            report["verification"] = {
                "total_claims": verification["total_claims_checked"],
                "supported_claims": verification["supported_claims"],
                "average_confidence": verification["average_confidence"],
                "reliability": verification["overall_reliability"],
                "detailed_claims": verification["claims"],
                "processing_time": f"{fact_check_time:.2f}s",
                "status": "success"
            }
            report["agents_executed"].append("Fact-Checker")
            print(f"✅ Fact-checking complete ({fact_check_time:.2f}s)\n")
            
        except Exception as e:
            report["verification"] = {"status": "failed", "error": str(e)}
            print(f"❌ Fact-checking failed: {e}\n")
        
        # Calculate total time
        total_time = time.time() - start_time
        report["total_processing_time"] = f"{total_time:.2f}s"
        
        return report
    
    def print_report(self, report: dict):
        """Pretty print the complete research report"""
        
        print(f"\n{'='*60}")
        print("📋 COMPLETE RESEARCH REPORT")
        print(f"{'='*60}\n")
        
        print(f"Query: {report['query']}")
        print(f"Timestamp: {report['timestamp']}")
        print(f"Total Processing Time: {report['total_processing_time']}")
        print(f"Agents Executed: {', '.join(report['agents_executed'])}\n")
        
        # Research Section
        if report.get("research", {}).get("status") == "success":
            print(f"{'='*60}")
            print("🔬 RESEARCH RESULTS")
            print(f"{'='*60}\n")
            print(report["research"]["content"][:500] + "...\n")
            print(f"Processing time: {report['research']['processing_time']}\n")
        
        # Summary Section
        if report.get("summaries", {}).get("status") == "success":
            print(f"{'='*60}")
            print("📝 SUMMARIES")
            print(f"{'='*60}\n")
            
            print("Brief Summary:")
            print(report["summaries"]["brief"])
            print(f"\nCompression: {report['summaries']['compression_stats']['brief']}\n")
            
            print("-" * 60)
            print("\nKey Points:")
            print(report["summaries"]["key_points"])
            print(f"\nCompression: {report['summaries']['compression_stats']['key_points']}\n")
        
        # Verification Section
        if report.get("verification", {}).get("status") == "success":
            print(f"{'='*60}")
            print("✅ FACT VERIFICATION")
            print(f"{'='*60}\n")
            print(f"Total Claims Checked: {report['verification']['total_claims']}")
            print(f"Supported Claims: {report['verification']['supported_claims']}")
            print(f"Average Confidence: {report['verification']['average_confidence']}")
            print(f"Overall Reliability: {report['verification']['reliability']}")
            print(f"Processing time: {report['verification']['processing_time']}\n")


# Test the orchestrator
if __name__ == "__main__":
    orchestrator = OrchestratorAgent()
    
    # Test queries
    test_queries = [
        "What are AI agents and how do they work?",
        "Latest developments in quantum computing 2025",
        "How does machine learning differ from deep learning?"
    ]
    
    print(f"\n{'='*60}")
    print("🚀 TESTING ORCHESTRATOR AGENT")
    print(f"{'='*60}\n")
    print(f"Testing with {len(test_queries)} queries...\n")
    
    # Run first query only (to save API quota)
    query = test_queries[0]
    report = orchestrator.research_complete(query)
    orchestrator.print_report(report)
    
    print(f"\n{'='*60}")
    print("✅ ORCHESTRATOR TEST COMPLETE")
    print(f"{'='*60}\n")
    print(f"Total agents coordinated: {len(report['agents_executed'])}")
    print(f"Overall success: {report['status']}")
    print(f"Total time: {report['total_processing_time']}")
