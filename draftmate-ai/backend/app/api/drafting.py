from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Document, Draft, StyleProfile
from ..schemas import DraftRequest, DraftSave
from ..services.ai_provider import AIUnavailable, generate
from ..services.skills import SKILLS
router=APIRouter(prefix="/api",tags=["drafting"])
@router.post("/drafting/generate")
async def draft(req:DraftRequest, db:Session=Depends(get_db)):
    doc=db.get(Document,req.document_id) if req.document_id else None
    if req.document_id and not doc: raise HTTPException(404,"Selected document not found.")
    style=db.query(StyleProfile).order_by(StyleProfile.created_at.desc()).first()
    skill=next((s for s in SKILLS if s["id"]==req.skill_id),None)
    system=("You are an AI drafting assistant. Never invent facts, parties, laws, citations, or authorities. Use [MISSING: detail] placeholders for material unknowns. Preserve substance unless instructed otherwise. State assumptions and questions. Drafts require review by qualified counsel. " + (f"Apply this style profile only to form, not substance: {style.profile}" if style else ""))
    prompt=f"Document type: {req.doc_type}\nTask: {req.instruction}\nFacts supplied: {req.facts}\n" + (f"Reference document content:\n{doc.content[:16000]}\n" if doc else "") + (f"Selected text:\n{req.selected_text}\n" if req.selected_text else "") + (f"Skill: {skill['name']} - {skill['description']}\n" if skill else "")
    try: return {"content":await generate(system,prompt),"provider":"configured","disclosure":"Supplied prompt and relevant document text are sent to the configured external AI provider."}
    except AIUnavailable as exc: raise HTTPException(503,str(exc))
@router.post("/drafts")
def save_draft(req:DraftSave, db:Session=Depends(get_db)):
    obj=db.get(Draft,req.id) if req.id else None
    if obj is None: obj=Draft(title=req.title,content=req.content); db.add(obj)
    else: obj.title=req.title; obj.content=req.content
    db.commit(); db.refresh(obj)
    return {"id":obj.id,"title":obj.title,"content":obj.content,"updated_at":obj.updated_at}
@router.get("/drafts")
def list_drafts(db:Session=Depends(get_db)):
    return [{"id":x.id,"title":x.title,"updated_at":x.updated_at} for x in db.query(Draft).order_by(Draft.updated_at.desc()).all()]
@router.get("/drafts/{draft_id}")
def get_draft(draft_id:int,db:Session=Depends(get_db)):
    obj=db.get(Draft,draft_id)
    if not obj: raise HTTPException(404,"Draft not found.")
    return {"id":obj.id,"title":obj.title,"content":obj.content}
