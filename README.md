# Autonomous AI Research Agent

This is a complete, production-ready Autonomous AI Research Agent built with LangGraph, FastAPI, and React. It uses Ollama for local LLM inference and ChromaDB for local vector storage, running entirely locally using free and open-source software.

## Architecture
- **Frontend**: React + Vite + TailwindCSS
- **Backend**: FastAPI + LangGraph
- **LLM**: Ollama (Qwen2.5:7b or Llama3.1:8b)
- **Vector DB**: ChromaDB
- **Tools**: DuckDuckGo Search, ArXiv Search, PyMuPDF

## Prerequisites
- Docker & Docker Compose
- [Ollama](https://ollama.com/) installed on your host machine.

## Setup Instructions

1. **Initialize Ollama**
   Run the initialization script to pull the required models:
   ```bash
   ./scripts/init_ollama.bat  # For Windows
   # or
   # ollama pull qwen2.5:7b
   ```

2. **Run the Application**
   ```bash
   docker-compose up --build
   ```

3. **Access the Dashboard**
   Open your browser and navigate to `http://localhost:5173`.

## Usage
1. Enter a research topic in the dashboard search bar.
2. The LangGraph agent workflow will:
   - Break down the request into subtasks
   - Search the web and ArXiv
   - Download and extract PDFs
   - Store content in ChromaDB
   - Generate summaries, comparisons, and a final report
3. View the generated Markdown report directly in the UI.

## Environment Variables
See `.env.example` for available configuration. You can change `OLLAMA_MODEL` and `EMBEDDING_MODEL` if you prefer different local models.
