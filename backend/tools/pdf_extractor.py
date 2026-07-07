import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract clean text from PDF using PyMuPDF."""
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text("text")
        doc.close()
        return clean_pdf_text(text)
    except Exception as e:
        print(f"Error extracting PDF {pdf_path}: {e}")
        return ""

def clean_pdf_text(text: str) -> str:
    """Clean the extracted text, optionally ignoring references."""
    # Basic cleaning
    text = re.sub(r'\n+', '\n', text)
    
    # Try to strip references if found (very basic heuristic)
    ref_match = re.search(r'\n(?:References|REFERENCES|Bibliography|BIBLIOGRAPHY)\n', text)
    if ref_match:
        text = text[:ref_match.start()]
        
    return text.strip()
