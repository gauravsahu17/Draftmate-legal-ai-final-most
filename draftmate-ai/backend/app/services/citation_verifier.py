import re
from datetime import datetime, timezone
PATTERNS = [re.compile(r"\b(?:\d{4}\s+)?(?:SCC|AIR|SCR|INSC)\s+\d{4,5}\b", re.I), re.compile(r"\b(?:Section|Article|§)\s+\d+[A-Za-z]?(?:\([\w]+\))*\b", re.I)]
def extract_citations(text: str):
    found = []
    for pat in PATTERNS:
        for match in pat.finditer(text):
            found.append({"original":match.group(0),"status":"UNVERIFIED","source_url":None,"metadata":{},"reason":"No authoritative source lookup is configured. Verification is never inferred from citation format.","limitations":"No court or statute record was retrieved; existence and legal proposition remain unconfirmed.","verified_at":datetime.now(timezone.utc).isoformat()})
    return found
