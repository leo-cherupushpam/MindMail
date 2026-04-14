import os
import sys
from pathlib import Path

# Ensure project root is on path so services/* can be imported
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional

from services.mock_data import get_sample_threads
from services.context_analyzer import ContextAnalyzer
from services.qa_service import ask_question, generate_draft_reply, summarize_emails

app = FastAPI()

# ── Startup: load and enrich all threads once ─────────────────────────────
_threads = get_sample_threads()
_analyzer = ContextAnalyzer()
_enriched = [_analyzer.analyze_thread(t) for t in _threads]

# ── Static files ──────────────────────────────────────────────────────────
_static = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(_static)), name="static")


# ── Page ──────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return FileResponse(str(_static / "index.html"))


# ── Thread list (inbox) ───────────────────────────────────────────────────
@app.get("/api/threads")
def api_threads():
    result = []
    for idx, thread in enumerate(_threads):
        msg = thread.messages[0] if thread.messages else None
        body = msg.body if msg else ""
        snippet = (body[:80].replace("\n", " ") + "...") if len(body) > 80 else body.replace("\n", " ")
        result.append({
            "idx": idx,
            "sender": msg.sender if msg else "",
            "subject": thread.main_topic,
            "snippet": snippet,
            "timestamp": msg.timestamp if msg else "",
            "is_unread": idx < 5,
        })
    return result


# ── Single thread (reading pane) ──────────────────────────────────────────
@app.get("/api/thread/{idx}")
def api_thread(idx: int):
    if idx < 0 or idx >= len(_threads):
        return JSONResponse({"error": "not found"}, status_code=404)
    thread = _threads[idx]
    enriched = _enriched[idx]
    return {
        "idx": idx,
        "subject": thread.main_topic,
        "messages": [
            {"sender": m.sender, "timestamp": m.timestamp, "body": m.body}
            for m in thread.messages
        ],
        "urgency": enriched.urgency_assessment,
        "sentiment_arc": enriched.sentiment_arc,
    }


# ── AI: Ask ───────────────────────────────────────────────────────────────
class AskRequest(BaseModel):
    thread_idx: int
    question: str

@app.post("/api/ask")
def api_ask(req: AskRequest):
    if req.thread_idx < 0 or req.thread_idx >= len(_enriched):
        return JSONResponse({"error": "invalid thread"}, status_code=400)
    answer = ask_question(req.question, _enriched[req.thread_idx])
    return {"answer": answer}


# ── AI: Draft ─────────────────────────────────────────────────────────────
class DraftRequest(BaseModel):
    thread_idx: int
    intent: Optional[str] = None
    tone: str = "professional"

@app.post("/api/draft")
def api_draft(req: DraftRequest):
    if req.thread_idx < 0 or req.thread_idx >= len(_enriched):
        return JSONResponse({"error": "invalid thread"}, status_code=400)
    draft = generate_draft_reply(_enriched[req.thread_idx], user_intent=req.intent, tone=req.tone)
    return {"draft": draft}


# ── AI: Summarize ─────────────────────────────────────────────────────────
class SummarizeRequest(BaseModel):
    thread_idx: int

@app.post("/api/summarize")
def api_summarize(req: SummarizeRequest):
    if req.thread_idx < 0 or req.thread_idx >= len(_enriched):
        return JSONResponse({"error": "invalid thread"}, status_code=400)
    summary = summarize_emails(_enriched[req.thread_idx])
    return {"summary": summary}
