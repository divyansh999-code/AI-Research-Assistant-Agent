from ddgs import DDGS

def search_web(query: str, max_results: int = 5):
    """
    Search web using DuckDuckGo
    
    Args:
        query: Search query string
        max_results: Number of results to return
        
    Returns:
        List of dicts with {title, url, snippet}
    """
    try:
        results = []
        ddgs = DDGS()
        
        for result in ddgs.text(query, max_results=max_results):
            results.append({
                'title': result.get('title', ''),
                'url': result.get('href', ''),
                'snippet': result.get('body', '')
            })
            
        return results
    except Exception as e:
        print(f"Search error: {e}")
        return []

# Test it
if __name__ == "__main__":
    query = "what is langchain?"
    results = search_web(query, max_results=3)
    
    print(f"\nSearch results for: {query}\n")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['title']}")
        print(f"   {result['url']}")
        print(f"   {result['snippet'][:100]}...\n")
