import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import re

load_dotenv(override=True)

class FactCheckerAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.1  # Very low for factual verification
        )
    
    def verify_claims(self, research_text: str, sources: list = None) -> dict:
        """
        Verify claims in research text against sources
        
        Args:
            research_text: The research output to verify
            sources: List of source texts/URLs used in research
        """
        
        # Step 1: Extract claims
        extract_prompt = PromptTemplate(
            input_variables=["research_text"],
            template="""Extract all factual claims from this research text. List each claim as a numbered statement.

Research:
{research_text}

Factual Claims (one per line):"""
        )
        
        chain = extract_prompt | self.llm
        claims_result = chain.invoke({"research_text": research_text})
        
        # Parse claims
        claims = [line.strip() for line in claims_result.content.split('\n') 
                  if line.strip() and re.match(r'^\d+\.', line.strip())]
        
        # Step 2: Verify each claim
        verify_prompt = PromptTemplate(
            input_variables=["claim", "research_text"],
            template="""Verify this claim against the research context. Provide:
1. Verification status: SUPPORTED / PARTIALLY SUPPORTED / UNSUPPORTED
2. Confidence score: 0-100%
3. Evidence: Quote supporting text or explain why unsupported
4. Concerns: Any issues with the claim

Claim: {claim}

Research Context:
{research_text}

Verification:"""
        )
        
        verified_claims = []
        
        for claim in claims[:5]:  # Limit to 5 claims for speed
            verify_chain = verify_prompt | self.llm
            verification = verify_chain.invoke({
                "claim": claim,
                "research_text": research_text
            })
            
            # Parse confidence score
            confidence = self._extract_confidence(verification.content)
            status = self._extract_status(verification.content)
            
            verified_claims.append({
                "claim": claim,
                "status": status,
                "confidence": confidence,
                "verification_details": verification.content
            })
        
        # Step 3: Generate summary report
        total_claims = len(verified_claims)
        supported = sum(1 for c in verified_claims if c['status'] == 'SUPPORTED')
        avg_confidence = sum(c['confidence'] for c in verified_claims) / total_claims if total_claims > 0 else 0
        
        return {
            "total_claims_checked": total_claims,
            "supported_claims": supported,
            "average_confidence": f"{avg_confidence:.1f}%",
            "overall_reliability": self._calculate_reliability(supported, total_claims, avg_confidence),
            "claims": verified_claims
        }
    
    def _extract_confidence(self, text: str) -> float:
        """Extract confidence percentage from verification text"""
        match = re.search(r'(\d+)%', text)
        return float(match.group(1)) if match else 50.0
    
    def _extract_status(self, text: str) -> str:
        """Extract verification status"""
        text_upper = text.upper()
        if 'UNSUPPORTED' in text_upper:
            return 'UNSUPPORTED'
        elif 'PARTIALLY SUPPORTED' in text_upper or 'PARTIAL' in text_upper:
            return 'PARTIALLY SUPPORTED'
        elif 'SUPPORTED' in text_upper:
            return 'SUPPORTED'
        return 'UNKNOWN'
    
    def _calculate_reliability(self, supported: int, total: int, avg_confidence: float) -> str:
        """Calculate overall reliability rating"""
        if total == 0:
            return "INSUFFICIENT DATA"
        
        support_ratio = supported / total
        
        if support_ratio >= 0.8 and avg_confidence >= 80:
            return "HIGH RELIABILITY"
        elif support_ratio >= 0.6 and avg_confidence >= 60:
            return "MODERATE RELIABILITY"
        else:
            return "LOW RELIABILITY - VERIFY INDEPENDENTLY"


# Test the agent
if __name__ == "__main__":
    sample_research = """
    The year 2025 has been identified as a pivotal period for AI agents. IBM launched BeeAI 
    and Agent Stack in early 2025, enabling enterprises to build intelligent agents. Google 
    introduced Vertex AI Agent Builder during the same period. Companies like AWS, Databricks, 
    and GitHub also released agentic AI tools. The Chinese model DeepSeek-R1 was released in 
    January 2025, accelerating momentum in the field. AI agents can now operate autonomously 
    and utilize other software tools, marking a shift from traditional generative AI.
    """
    
    agent = FactCheckerAgent()
    
    print("=" * 60)
    print("TESTING FACT-CHECKER AGENT")
    print("=" * 60)
    print("\n📝 Extracting and verifying claims...\n")
    
    result = agent.verify_claims(sample_research)
    
    print(f"{'='*60}")
    print("VERIFICATION REPORT")
    print(f"{'='*60}\n")
    
    print(f"📊 Total Claims Checked: {result['total_claims_checked']}")
    print(f"✅ Supported Claims: {result['supported_claims']}")
    print(f"📈 Average Confidence: {result['average_confidence']}")
    print(f"🎯 Overall Reliability: {result['overall_reliability']}\n")
    
    print(f"{'='*60}")
    print("DETAILED CLAIM VERIFICATION")
    print(f"{'='*60}\n")
    
    for i, claim_data in enumerate(result['claims'], 1):
        print(f"Claim {i}: {claim_data['claim']}")
        print(f"Status: {claim_data['status']}")
        print(f"Confidence: {claim_data['confidence']}%")
        print(f"\nDetails:\n{claim_data['verification_details']}")
        print("\n" + "-"*60 + "\n")
