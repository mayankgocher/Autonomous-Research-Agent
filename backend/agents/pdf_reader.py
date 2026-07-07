from agents.state import ResearchState
from tools.pdf_extractor import extract_text_from_pdf
import os

def pdf_reader_agent(state: ResearchState) -> ResearchState:
    """Read downloaded PDFs and extract text."""
    extracted = {}
    for pdf_path in state.get('downloaded_pdfs', []):
        if os.path.exists(pdf_path):
            text = extract_text_from_pdf(pdf_path)
            # Use filename without extension as key
            key = os.path.basename(pdf_path).replace('.pdf', '')
            extracted[key] = text
            
    state['extracted_texts'] = extracted
    return state
