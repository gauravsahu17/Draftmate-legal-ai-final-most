import re
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session
from ..config import settings
from ..database import get_db
from ..models import Document
from ..services.document_parser import extract_document
router = APIRouter(prefix="/api/documents", tags=["documents"])
def safe_name(name: str) -> str:
    name = re.sub(r"[^A-Za-z0-9._() -]", "_", name or "upload")
    return name[:255] or "upload"
@router.post("")
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    raw = await file.read(settings.max_upload_mb * 1024 * 1024 + 1)
    if len(raw) > settings.max_upload_mb * 1024 * 1024:
        raise HTTPException(413, f"File exceeds {settings.max_upload_mb} MB limit.")
    try:
        content, kind = extract_document(safe_name(file.filename or ""), raw)
    except ValueError as exc:
        raise HTTPException(400, str(exc))
    except Exception:
        raise HTTPException(400, "The file could not be parsed. Check that it is a valid, unencrypted DOCX or PDF.")
    doc = Document(name=safe_name(file.filename or "upload"), kind=kind, content=content)
    db.add(doc); db.commit(); db.refresh(doc)
    return {"id":doc.id,"name":doc.name,"kind":doc.kind,"characters":len(content),"status":"processed"}
@router.get("")
def list_documents(db: Session = Depends(get_db)):
    return [{"id":d.id,"name":d.name,"kind":d.kind,"characters":len(d.content),"created_at":d.created_at} for d in db.query(Document).order_by(Document.created_at.desc()).all()]
@router.get("/{doc_id}")
def get_document(doc_id:int, db:Session=Depends(get_db)):
    doc=db.get(Document,doc_id)
    if not doc: raise HTTPException(404,"Document not found.")
    return {"id":doc.id,"name":doc.name,"kind":doc.kind,"content":doc.content}
@router.delete("/{doc_id}")
def delete_document(doc_id:int, db:Session=Depends(get_db)):
    doc=db.get(Document,doc_id)
    if not doc: raise HTTPException(404,"Document not found.")
    db.delete(doc); db.commit()
    return {"deleted":True}
