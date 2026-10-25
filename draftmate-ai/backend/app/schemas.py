from pydantic import BaseModel, Field
class DraftRequest(BaseModel):
    instruction: str = Field(min_length=3, max_length=12000)
    doc_type: str = "General legal document"
    facts: str = ""
    selected_text: str = ""
    document_id: int | None = None
    skill_id: str | None = None
class DraftSave(BaseModel):
    id: int | None = None
    title: str = Field(default="Untitled draft", max_length=255)
    content: str = Field(max_length=200000)
class CompareRequest(BaseModel):
    left_id: int
    right_id: int
