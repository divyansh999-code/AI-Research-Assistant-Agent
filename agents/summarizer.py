import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv(override=True)

class SummarizerAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0.3  # Lower temp for factual summaries
        )
    
    def summarize(self, research_text: str, summary_type: str = "brief") -> dict:
        """
        Generate different types of summaries
        
        Args:
            research_text: The research output to summarize
            summary_type: 'brief', 'detailed', 'key_points', or 'executive'
        """
        
        prompts = {
            "brief": """Summarize this research in 2-3 sentences. Focus on the most important findings only.

Research:
{research_text}

Brief Summary:""",
            
            "detailed": """Provide a comprehensive paragraph summarizing this research. Include main findings, key statistics, and important context.

Research:
{research_text}

Detailed Summary:""",
            
            "key_points": """Extract 5-7 key points from this research as a bullet list. Each point should be one clear sentence.

Research:
{research_text}

Key Points:""",
            
            "executive": """Create an executive summary suitable for business stakeholders. Focus on: What it means, Why it matters, What actions to consider.

Research:
{research_text}

Executive Summary:"""
        }
        
        prompt_template = PromptTemplate(
            input_variables=["research_text"],
            template=prompts.get(summary_type, prompts["brief"])
        )
        
        chain = prompt_template | self.llm
        
        try:
            result = chain.invoke({"research_text": research_text})
            return {
                "summary_type": summary_type,
                "summary": result.content,
                "original_length": len(research_text),
                "summary_length": len(result.content),
                "compression_ratio": f"{(1 - len(result.content)/len(research_text))*100:.1f}%"
            }
        except Exception as e:
            return {"error": str(e)}

# Test the agent
if __name__ == "__main__":
    # Sample research text
    sample_research = """
    The year 2025 has been identified as a pivotal period for the advancement of AI agents, 
    marking a decisive shift in their development and deployment. These agents represent a 
    "whole new ballgame" compared to generative AI, characterized by their ability to utilize 
    other software tools and operate autonomously. Key developments include major industry 
    adoption with IBM launching BeeAI and Agent Stack, Google introducing Vertex AI Agent 
    Builder, and companies like AWS, Databricks, GitHub, and Salesforce releasing agentic 
    AI tools during 2025. The focus is heavily on enterprise solutions, empowering businesses 
    to integrate and leverage intelligent agents for various tasks and operations.
    """
    
    agent = SummarizerAgent()
    
    print("=" * 60)
    print("TESTING SUMMARIZER AGENT")
    print("=" * 60)
    
    # Test all summary types
    for summary_type in ["brief", "detailed", "key_points", "executive"]:
        print(f"\n{'='*60}")
        print(f"SUMMARY TYPE: {summary_type.upper()}")
        print('='*60)
        result = agent.summarize(sample_research, summary_type)
        
        if "error" not in result:
            print(f"\n{result['summary']}")
            print(f"\n📊 Stats: Original={result['original_length']} chars | "
                  f"Summary={result['summary_length']} chars | "
                  f"Compressed by {result['compression_ratio']}")
        else:
            print(f"❌ Error: {result['error']}")
