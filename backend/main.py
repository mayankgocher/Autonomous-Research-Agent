from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router

from database.db import init_db

app = FastAPI(title="Autonomous AI Research Agent API")

@app.on_event("startup")
def on_startup():
    init_db()

# Setup CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Autonomous Research Agent API is running"}
