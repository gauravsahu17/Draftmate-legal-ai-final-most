import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Document, StyleProfile
from ..services.style_analyser import analyse_style
router=APIRouter(prefix="/api/styles",tags=["style profiles"])
@router.post("/analyze/{document_id}")
def analyze(document_id:int,db:Session=Depends(get_db)):
    doc=db.get(Document,document_id)
    if not doc: raise HTTPException(404,"Reference document not found.")
    profile=analyse_style(doc.content)
    obj=StyleProfile(name=doc.name,profile=json.dumps(profile,ensure_ascii=False))
    db.add(obj);db.commit();db.refresh(obj)
    return {"id":obj.id,"name":obj.name,"profile":profile,"notice":"Heuristic style analysis only. Style is separate from legal substance; review before reuse."}
@router.get("")
def list_profiles(db:Session=Depends(get_db)):
    return [{"id":p.id,"name":p.name,"profile":json.loads(p.profile)} for p in db.query(StyleProfile).order_by(StyleProfile.created_at.desc()).all()]
@router.delete("/{profile_id}")
def reset(profile_id:int,db:Session=Depends(get_db)):
    obj=db.get(StyleProfile,profile_id)
    if not obj: raise HTTPException(404,"Style profile not found.")
    db.delete(obj);db.commit();return {"deleted":True}
