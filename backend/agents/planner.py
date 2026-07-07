from agents.state import ResearchState
from agents.llm import get_llm
from langchain_core.messages import SystemMessage, HumanMessage
import json

def planner_agent(state: ResearchState) -> ResearchState:
    """Analyze the query and break it down into subtasks."""
    llm = get_llm(temperature=0.2)
    
    prompt = f"""You are an AI Research Planner. Break down the following research request into 2-4 concrete subtasks.
Return ONLY a valid JSON list of strings representing the subtasks.

Request: {state['query']}
"""
    try:
        response = llm.invoke([HumanMessage(content=prompt)])
        
        # Simple extraction of JSON list if wrapped in markdown blocks
        text = response.content.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
            
        subtasks = json.loads(text.strip())
        state['subtasks'] = subtasks
    except Exception as e:
        print(f"Planner error: {e}")
        state['subtasks'] = [state['query']]
        state['errors'].append(f"Planner error: {e}")
        
    return state
