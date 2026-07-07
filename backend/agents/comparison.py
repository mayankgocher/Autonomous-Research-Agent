from agents.state import ResearchState
from agents.llm import get_llm
from langchain_core.messages import HumanMessage
import json

def comparison_agent(state: ResearchState) -> ResearchState:
    """Compare summaries and generate a comparison table (Markdown)."""
    if not state.get('summaries'):
        state['comparison_table'] = "No summaries available to compare."
        return state
        
    llm = get_llm(temperature=0.2)
    
    summaries_text = json.dumps(state['summaries'], indent=2)
    
    prompt = f"""You are an AI Research Analyst. 
Based on the following JSON summaries of different papers, generate a Markdown comparison table.
Include the following columns if applicable: Model, Architecture, Dataset, Accuracy, Parameters, Advantages, Limitations.

Summaries:
{summaries_text}

Return ONLY the Markdown table and nothing else.
"""
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        state['comparison_table'] = response.content.strip()
    except Exception as e:
        print(f"Comparison error: {e}")
        state['errors'].append(f"Comparison error: {e}")
        state['comparison_table'] = ""
        
    return state
