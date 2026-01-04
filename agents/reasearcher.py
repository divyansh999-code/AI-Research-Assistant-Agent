# Add at the top
from summarizer import SummarizerAgent

# Inside ResearcherAgent class, after the research method
def research_with_summary(self, query: str, summary_type: str = "brief"):
    """Research and return with summary"""
    research_result = self.research(query)
    
    summarizer = SummarizerAgent()
    summary = summarizer.summarize(research_result, summary_type)
    
    return {
        "query": query,
        "full_research": research_result,
        "summary": summary
    }

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.web_search import search_web

# Load environment variables
load_dotenv()

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3
)



def research(question: str):
    """
    Research a question using web search and LLM
    
    Args:
        question: The question to research
        
    Returns:
        Research results as a string
    """
    try:
        # Step 1: Search the web
        print(f"🔍 Searching web for: {question}")
        search_results = search_web(question, max_results=5)
        
        if not search_results:
            return "No search results found."
        
        # Step 2: Format results
        formatted_results = "\n\n".join([
            f"Source {i+1}: {r['title']}\nURL: {r['url']}\nContent: {r['snippet']}"
            for i, r in enumerate(search_results)
        ])
        
        print(f"\n✅ Found {len(search_results)} sources")
        print(f"\n📝 Analyzing results with LLM...\n")
        
        # Step 3: Use LLM to analyze
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a research assistant. Analyze the web search results and provide a comprehensive answer to the user's question. Cite sources by number."),
            ("user", f"Question: {question}\n\nSearch Results:\n{formatted_results}\n\nProvide a detailed answer based on these sources.")
        ])
        
        chain = prompt | llm
        response = chain.invoke({})
        
        return response.content
        
    except Exception as e:
        return f"Research error: {str(e)}"

# Test it
if __name__ == "__main__":
    question = "who is hero in movie saaho?"
    print(f"\n{'='*60}")
    print(f"RESEARCHING: {question}")
    print(f"{'='*60}\n")
    
    result = research(question)
    
    print(f"\n{'='*60}")
    print("FINAL RESEARCH RESULT:")
    print(f"{'='*60}\n")
    print(result)
