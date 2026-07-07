from typing import List, Dict, TypedDict, Any

class ResearchState(TypedDict):
    research_id: int
    query: str
    subtasks: List[str]
    web_results: List[Dict[str, Any]]
    arxiv_results: List[Dict[str, Any]]
    downloaded_pdfs: List[str]
    extracted_texts: Dict[str, str]
    summaries: Dict[str, Dict[str, Any]]
    comparison_table: str
    fact_check_results: str
    final_report_markdown: str
    final_report_pdf: str
    errors: List[str]
