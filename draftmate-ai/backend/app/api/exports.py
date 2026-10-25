from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from io import BytesIO
from ..services.export_service import make_docx
router=APIRouter(prefix="/api/exports",tags=["exports"])
class Export(BaseModel):
    title:str=Field(default="DraftMate Document",max_length=255)
    content:str=Field(max_length=200000)
@router.post("/docx")
def export_docx(req:Export):
    stream=BytesIO(make_docx(req.title,req.content)); return StreamingResponse(stream,media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",headers={"Content-Disposition":"attachment; filename=DraftMate-document.docx"})
