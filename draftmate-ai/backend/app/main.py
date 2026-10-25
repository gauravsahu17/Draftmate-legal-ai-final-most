from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from . import models
from .api import documents, drafting, skills, citations, research, exports, styles
Base.metadata.create_all(bind=engine)
app=FastAPI(title="DraftMate AI API",version="1.0.0")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173","http://127.0.0.1:5173"],allow_methods=["*"],allow_headers=["*"])
app.include_router(documents.router); app.include_router(drafting.router); app.include_router(skills.router); app.include_router(citations.router); app.include_router(research.router); app.include_router(exports.router); app.include_router(styles.router)
@app.get("/health")
def health(): return {"status":"ok","service":"DraftMate AI API"}
