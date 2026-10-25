# DraftMate AI — Legal Drafting Studio
A locally runnable legal drafting prototype inspired by the Kodekurrent Season 2 brief. React + TypeScript + Vite frontend; FastAPI + SQLite backend.

## Start on Windows 11
Prerequisites: Python 3.11 or newer and Node.js 20 or newer.
1. Copy `backend/.env.example` to `backend/.env`.
2. Add your OpenAI-compatible provider key as `AI_API_KEY` to enable real AI drafting. Keep it out of frontend code.
3. From this project folder, run `powershell -ExecutionPolicy Bypass -File .\start.ps1`.
4. Open http://127.0.0.1:5173. Backend health is at http://127.0.0.1:8000/health.
5. Run `powershell -ExecutionPolicy Bypass -File .\stop.ps1` to stop the services.

The startup script creates a project-local Python environment, installs Python and npm dependencies, then starts both services. It does not install system-wide software.

## Included
- Dashboard, drafting studio, document library, 12-skill library, research, citation review, comparison and settings.
- DOCX, text PDF and TXT uploads with extraction, size/type validation, status, local SQLite storage, open and confirmed deletion.
- Configurable OpenAI-compatible chat-completions integration. Missing key, timeout and rate-limit errors are shown honestly. Prompts and selected document text are sent to the configured provider when drafting.
- Editable text drafts with save, reopen, and DOCX export.
- Reference-document heuristic style analysis (heading examples, clause numbering, sentence length and paragraph counts). Preview and reset are supported; only form cues are passed into drafting.
- Browser speech recognition and text-to-speech when supported, with text input available.
- Citation pattern extraction. All results remain UNVERIFIED because no authoritative source search integration is configured.
- Legal research provides official India Code, Supreme Court and eCourts portals. It returns no fabricated search results.
- Text comparison highlights added and deleted sentence strings; it never applies changes to source documents.

## Configuration
Pydantic Settings reads process variables or `backend/.env`:
- `AI_API_KEY`
- `AI_BASE_URL` (default https://api.openai.com/v1)
- `AI_MODEL` (default gpt-4o-mini)
- `AI_PROVIDER` (reserved for provider selection)
- `MAX_UPLOAD_MB` (default 15)
- `DATABASE_URL` (default sqlite:///./draftmate.db)

Uploads are parsed in memory. SQLite stores the sanitized name, file type, extracted text and timestamps. Avoid uploading content you are not permitted to send to an external AI provider. This is a single-user local prototype, not an authentication, legal privilege or confidentiality guarantee.

## Development and checks
Backend: from `backend/`, run `python -m venv .venv`, install `requirements.txt`, then `.venv\Scripts\python.exe -m uvicorn app.main:app --reload`.
Frontend: from `frontend/`, run `npm install`, `npm run dev`; `npm run build` creates the production bundle.
Tests: run `cd backend; .venv\\Scripts\\python.exe -m pytest tests -q`; run `npm test` from `frontend/`.

## Fictional demonstration
Fictional facts: Northstar Studio hires Asha Rao Design for a six-week branding project for INR 80,000. Upload a TXT with those details, choose Service agreement, and ask for a short agreement with missing dates and addresses marked `[MISSING]`. Generate after configuring an AI key, edit and save, reopen the draft, export DOCX, and compare it with a second TXT that changes the project duration. The names and terms are invented only for demonstration.

## Limits
- AI generation requires a user-supplied provider API key; it was not exercised without credentials.
- No live legal search or authoritative citation verification is connected. Citation extraction is not verification.
- OCR, PDF export, Tailwind CSS, TipTap/rich-text formatting, selection-based rewrites, model picker, automatic draft revisions, redline acceptance, full modified-clause diffing, and draft revision history are not implemented.
- Style analysis is heuristic. DOCX export preserves headings and paragraphs; complex source formatting is not retained.
- Browser voice support and microphone permission depend on the browser and user settings.

DraftMate is an assistive prototype, not legal advice. AI text can be incomplete or wrong. Have qualified legal counsel review documents before use.
