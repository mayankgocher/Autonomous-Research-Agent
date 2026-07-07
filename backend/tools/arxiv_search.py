import arxiv
import os
import requests
from typing import List, Dict

def arxiv_search(query: str, max_results: int = 5, download_dir: str = "./data/papers") -> List[Dict]:
    """Search arxiv and optionally download PDFs."""
    os.makedirs(download_dir, exist_ok=True)
    
    # Configure arxiv client
    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    results = []
    for paper in client.results(search):
        paper_id = paper.get_short_id()
        pdf_path = os.path.join(download_dir, f"{paper_id}.pdf")
        
        # Download PDF if not exists
        if not os.path.exists(pdf_path):
            try:
                # Use arxiv client download method directly
                paper.download_pdf(dirpath=download_dir, filename=f"{paper_id}.pdf")
            except Exception as e:
                print(f"Failed to download {paper_id}: {e}")
                
        results.append({
            "id": paper_id,
            "title": paper.title,
            "authors": [author.name for author in paper.authors],
            "summary": paper.summary,
            "url": paper.entry_id,
            "pdf_url": paper.pdf_url,
            "pdf_path": pdf_path if os.path.exists(pdf_path) else None
        })
        
    return results
