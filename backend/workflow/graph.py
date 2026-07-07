from langgraph.graph import StateGraph, END
from agents.state import ResearchState
from agents.planner import planner_agent
from agents.web_search import web_search_agent
from agents.arxiv import arxiv_agent
from agents.pdf_reader import pdf_reader_agent
from agents.retriever import retriever_agent
from agents.summarizer import summarizer_agent
from agents.comparison import comparison_agent
from agents.fact_checker import fact_checker_agent
from agents.report import report_agent
import sqlite3
from database.db import get_db_connection

def build_graph():
    workflow = StateGraph(ResearchState)
    
    # Add nodes
    workflow.add_node("planner", planner_agent)
    workflow.add_node("web_search", web_search_agent)
    workflow.add_node("arxiv_search", arxiv_agent)
    workflow.add_node("pdf_reader", pdf_reader_agent)
    workflow.add_node("retriever", retriever_agent)
    workflow.add_node("summarizer", summarizer_agent)
    workflow.add_node("comparison", comparison_agent)
    workflow.add_node("fact_checker", fact_checker_agent)
    workflow.add_node("report", report_agent)
    
    # Edges
    workflow.set_entry_point("planner")
    
    # Planner goes to parallel search
    workflow.add_edge("planner", "web_search")
    workflow.add_edge("planner", "arxiv_search")
    
    # After arxiv, download and read PDFs
    workflow.add_edge("arxiv_search", "pdf_reader")
    
    # Both search streams converge on retriever
    # To handle parallel branches joining in LangGraph, we typically use an intermediate node or conditional edges.
    # For simplicity, we can do sequential: planner -> web -> arxiv -> pdf -> retriever -> etc.
    # To run parallel in LangChain/Graph standardly without complex fan-out/fan-in, we just link them.
    # Let's adjust to sequential for stability if parallel is not strictly enforced in the orchestrator.
    # BUT prompt requested "Use parallel execution". Langgraph can run nodes in parallel and wait for all to finish if they join a node.
    
    workflow.add_edge("web_search", "retriever")
    workflow.add_edge("pdf_reader", "retriever")
    
    workflow.add_edge("retriever", "summarizer")
    
    workflow.add_edge("summarizer", "comparison")
    workflow.add_edge("summarizer", "fact_checker")
    
    workflow.add_edge("comparison", "report")
    workflow.add_edge("fact_checker", "report")
    
    workflow.add_edge("report", END)
    
    return workflow.compile()

def run_research_workflow(research_id: int, query: str):
    """Entry point for the background task."""
    try:
        app = build_graph()
        initial_state = ResearchState(
            research_id=research_id,
            query=query,
            subtasks=[],
            web_results=[],
            arxiv_results=[],
            downloaded_pdfs=[],
            extracted_texts={},
            summaries={},
            comparison_table="",
            fact_check_results="",
            final_report_markdown="",
            final_report_pdf="",
            errors=[]
        )
        
        # Execute the graph
        final_state = app.invoke(initial_state)
        
        # Update DB
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE research_history SET status='completed', report_markdown=?, report_pdf_path=? WHERE id=?",
            (final_state.get('final_report_markdown', ''), final_state.get('final_report_pdf', ''), research_id)
        )
        conn.commit()
        conn.close()
        
    except Exception as e:
        print(f"Workflow error: {e}")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE research_history SET status='error' WHERE id=?", (research_id,))
        conn.commit()
        conn.close()
