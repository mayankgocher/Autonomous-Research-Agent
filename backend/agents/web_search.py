from agents.state import ResearchState
from tools.search import web_search as run_web_search

def web_search_agent(state: ResearchState) -> ResearchState:
    """Perform web searches based on query and subtasks."""
    queries = [state['query']] + state.get('subtasks', [])
    all_results = []
    
    for q in queries:
        res = run_web_search(q, max_results=3)
        all_results.extend(res)
        
    # Deduplicate
    unique = []
    seen = set()
    for r in all_results:
        if r['url'] not in seen:
            unique.append(r)
            seen.add(r['url'])
            
    state['web_results'] = unique
    return state
