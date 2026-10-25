from fastapi import APIRouter
from pydantic import BaseModel, Field
router=APIRouter(prefix="/api/research",tags=["research"])
class Query(BaseModel): question:str=Field(min_length=3,max_length=4000)
@router.post("")
def research(q:Query):
    return {"question":q.question,"results":[],"status":"sources_not_configured","message":"No live legal research API is configured. No search results are fabricated. Use these official entry points to research directly.","sources":[{"name":"India Code","url":"https://www.indiacode.nic.in/"},{"name":"Supreme Court of India","url":"https://www.sci.gov.in/"},{"name":"eCourts Services","url":"https://ecourts.gov.in/"}]}
