from agents.state import ResearchState
from agents.llm import get_llm
from langchain_core.messages import HumanMessage
import json

def summarizer_agent(state: ResearchState) -> ResearchState:
    """Summarize each paper and extract key points."""
    llm = get_llm(temperature=0.1)
    summaries = {}
    
    for paper_id, text in state.get('extracted_texts', {}).items():
        if not text:
            continue
            
        prompt = f"""You are an AI Research Summarizer. 
Read the following paper text (truncated for length) and extract:
- objective
- methodology
- datasets
- model (or architecture)
- strengths
- weaknesses
- limitations
- future work

Paper Text (first 4000 characters):
{text[:4000]}

Return ONLY a valid JSON object with the exact keys listed above. If a field is not found, use "Not specified".
"""
        try:
            response = llm.invoke([HumanMessage(content=prompt)])
            text_resp = response.content.strip()
            if text_resp.startswith("```json"):
                text_resp = text_resp[7:]
            if text_resp.startswith("```"):
                text_resp = text_resp[3:]
            if text_resp.endswith("```"):
                text_resp = text_resp[:-3]
                
            summary_json = json.loads(text_resp.strip())
            summaries[paper_id] = summary_json
        except Exception as e:
            print(f"Summarizer error for {paper_id}: {e}")
            summaries[paper_id] = {"error": str(e)}
            
    state['summaries'] = summaries
    return state
