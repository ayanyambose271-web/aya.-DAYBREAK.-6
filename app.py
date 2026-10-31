"""FastAPI entrypoint; auto-detected by Vercel's Python runtime."""
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from daybreak import TOPICS, get_questions, grade_answer, SOURCES

ROOT = Path(__file__).resolve().parent
app = FastAPI(title="DAYBREAK Study Lab", version="0.3.0", docs_url="/api/docs", openapi_url="/api/openapi.json")
app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")


class GradeSubmission(BaseModel):
    question_id: str = Field(min_length=1, max_length=50)
    answer_index: int = Field(ge=0, le=3)


@app.get("/")
def index():
    return FileResponse(ROOT / "static" / "index.html")


@app.get("/api/health")
def health():
    return {"status": "ok", "application": "daybreak-study-lab"}


@app.get("/api/topics")
def topics():
    return {"topics": TOPICS}


@app.get("/api/sources")
def sources():
    return {"sources": SOURCES, "notice": "Direct textbook verification covers Swartz Ch. 18 & 24. Other topics use PSY144 lecture slides; full external prescribed chapters/articles not verified."}


@app.get("/api/questions")
def questions(topic_id: str, count: int = Query(default=4, ge=1, le=20), mode: str = Query(default="medium", pattern="^(medium|hard)$")):
    try:
        return {"questions": get_questions(topic_id, count, mode=mode)}
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.post("/api/grade")
def grade(payload: GradeSubmission):
    try:
        return grade_answer(payload.question_id, payload.answer_index)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
