from duckduckgo_search import DDGS
from typing import List, Dict

def web_search(query: str, max_results: int = 5) -> List[Dict]:
    """Search DuckDuckGo and return a list of results."""
    results = []
    try:
        with DDGS() as ddgs:
            # text() method returns a generator
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r.get("title"),
                    "url": r.get("href"),
                    "snippet": r.get("body")
                })
    except Exception as e:
        print(f"Web search error: {e}")
    
    # Remove duplicates based on URL
    unique_results = []
    seen_urls = set()
    for r in results:
        if r["url"] not in seen_urls:
            unique_results.append(r)
            seen_urls.add(r["url"])
            
    return unique_results
