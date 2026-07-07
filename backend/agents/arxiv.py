from agents.state import ResearchState
from tools.arxiv_search import arxiv_search as run_arxiv_search

def arxiv_agent(state: ResearchState) -> ResearchState:
    """Search arxiv for papers and download them."""
    try:
        results = run_arxiv_search(state['query'], max_results=3)
        state['arxiv_results'] = results
        
        downloaded = []
        for r in results:
            if r.get('pdf_path'):
                downloaded.append(r['pdf_path'])
        state['downloaded_pdfs'] = downloaded
    except Exception as e:
        print(f"Arxiv agent error: {e}")
        state['arxiv_results'] = []
        state['downloaded_pdfs'] = []
        state['errors'].append(f"Arxiv error: {e}")
        
    return state
