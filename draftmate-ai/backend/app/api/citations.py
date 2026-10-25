from fastapi import APIRouter
from pydantic import BaseModel, Field
from ..services.citation_verifier import extract_citations
router=APIRouter(prefix="/api/citations",tags=["citations"])
class CitationRequest(BaseModel): text:str=Field(max_length=200000)
@router.post("/verify")
def verify(req:CitationRequest):
    return {"results":extract_citations(req.text),"source_access":"unavailable","note":"Citation pattern extraction only. No live legal-source search or verification is configured."}
