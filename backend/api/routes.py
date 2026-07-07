from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
import sqlite3
from typing import List, Dict, Any
from database.db import get_db_connection, ResearchRequest, ResearchResponse

router = APIRouter()

@router.post("/research", response_model=ResearchResponse)
def start_research(request: ResearchRequest, background_tasks: BackgroundTasks):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO research_history (query, status) VALUES (?, ?)",
        (request.query, "pending")
    )
    conn.commit()
    research_id = cursor.lastrowid
    conn.close()

    # In a real scenario, we start LangGraph agent workflow here via background_tasks
    # background_tasks.add_task(run_research_workflow, research_id, request.query)

    return ResearchResponse(id=research_id, query=request.query, status="pending")

@router.get("/history")
def get_history():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM research_history ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@router.get("/report/{research_id}")
def get_report(research_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT report_markdown, report_pdf_path FROM research_history WHERE id=?", (research_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Research not found")
        
    return {"markdown": row["report_markdown"], "pdf_path": row["report_pdf_path"]}

@router.get("/status/{research_id}")
def get_status(research_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM research_history WHERE id=?", (research_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Research not found")
        
    return {"status": row["status"]}
