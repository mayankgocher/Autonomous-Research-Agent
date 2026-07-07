import os
import sqlite3
from pathlib import Path
from pydantic import BaseModel
from typing import List, Optional

# Load env or default
DB_PATH = os.getenv("DB_PATH", "./data/research.db")

def get_db_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Research History Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS research_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            report_markdown TEXT,
            report_pdf_path TEXT
        )
    ''')

    # Create Papers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS papers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            research_id INTEGER,
            title TEXT,
            authors TEXT,
            url TEXT,
            pdf_path TEXT,
            summary TEXT,
            FOREIGN KEY (research_id) REFERENCES research_history (id)
        )
    ''')

    conn.commit()
    conn.close()

# Pydantic schemas for API
class ResearchRequest(BaseModel):
    query: str

class ResearchResponse(BaseModel):
    id: int
    query: str
    status: str
