import re
def analyse_style(text: str) -> dict:
    lines=[line.strip() for line in text.splitlines() if line.strip()]
    sentences=[s for s in re.split(r"(?<=[.!?])\s+",text) if s.strip()]
    numbered=[line for line in lines if re.match(r"^(?:\d+(?:\.\d+)*[.)]?|\([a-z0-9]+\))\s+",line,re.I)]
    headings=[line.lstrip("# ").strip() for line in lines if line.startswith("#") or (line.isupper() and len(line)<100)]
    avg=round(sum(len(s.split()) for s in sentences)/max(len(sentences),1),1)
    formal_terms=sum(bool(re.search(r"\b(hereby|hereinafter|whereas|notwithstanding|pursuant)\b",text,re.I)) for _ in [0])
    return {"heading_examples":headings[:12],"numbered_clause_count":len(numbered),"average_sentence_words":avg,"tone":"formal" if formal_terms else "plain/formal-neutral","paragraph_count":len(lines),"guidance":"Use the heading depth, clause numbering and sentence length as form cues only. Do not reuse parties, facts or legal substance from the reference."}
