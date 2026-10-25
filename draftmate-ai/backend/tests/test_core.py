from fastapi.testclient import TestClient
from app.main import app
from app.services.document_parser import extract_document
from app.services.citation_verifier import extract_citations
client=TestClient(app)
def test_health(): assert client.get("/health").json()["status"]=="ok"
def test_skills_registry_has_twelve(): assert len(client.get("/api/skills").json())==12
def test_unsupported_upload_parser():
    try: extract_document("thing.exe",b"stuff")
    except ValueError as e: assert "Unsupported" in str(e)
    else: assert False
def test_empty_upload_parser():
    try: extract_document("thing.txt",b"")
    except ValueError as e: assert "empty" in str(e)
    else: assert False
def test_citation_extraction_is_unverified():
    items=extract_citations("See Section 10 and AIR 2020 1234.")
    assert len(items)>=1 and all(x["status"]=="UNVERIFIED" for x in items)
def test_research_has_no_fabricated_results():
    r=client.post("/api/research",json={"question":"What is contract law?"})
    assert r.status_code==200 and r.json()["results"]==[] and len(r.json()["sources"])>=1
def test_draft_generation_requires_api_key():
    r=client.post("/api/drafting/generate",json={"instruction":"Draft an agreement","doc_type":"Service agreement"})
    assert r.status_code in (200,503)
    if r.status_code==503: assert "AI_API_KEY" in r.json()["detail"]
def test_style_profile_analysis_and_reset():
    d=client.post("/api/documents",files={"file":("reference.txt",b"1. Payment will be made. Hereinafter called Client.","text/plain")}).json()
    r=client.post(f"/api/styles/analyze/{d['id']}")
    assert r.status_code==200
    assert r.json()["profile"]["numbered_clause_count"]==1
    assert client.delete(f"/api/styles/{r.json()['id']}").json()["deleted"] is True
    client.delete(f"/api/documents/{d['id']}")
