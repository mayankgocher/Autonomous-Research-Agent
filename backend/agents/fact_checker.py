from agents.state import ResearchState
from agents.llm import get_llm
from langchain_core.messages import HumanMessage
import json

def fact_checker_agent(state: ResearchState) -> ResearchState:
    """Compare information and detect contradictions."""
    if not state.get('summaries'):
        state['fact_check_results'] = "No summaries available to fact check."
        return state
        
    llm = get_llm(temperature=0.1)
    
    summaries_text = json.dumps(state['summaries'], indent=2)
    
    prompt = f"""You are an AI Fact Checker. 
Review the following summaries from multiple papers.
1. Detect any contradictions or conflicting information between the papers.
2. Calculate a rough confidence score (0-100%) for the general consensus.

Summaries:
{summaries_text}

Return your findings in Markdown format.
"""
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        state['fact_check_results'] = response.content.strip()
    except Exception as e:
        print(f"Fact check error: {e}")
        state['errors'].append(f"Fact check error: {e}")
        state['fact_check_results'] = ""
        
    return state
