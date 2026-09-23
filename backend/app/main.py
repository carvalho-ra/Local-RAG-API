from fastapi import FastAPI

from app.database import SessionLocal
from app.rag import answer_question
from app.schemas import AskRequest, AskResponse


app = FastAPI(title="Local RAG API")


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask")
async def ask(question: AskRequest):
    db = SessionLocal()

    try:
        answer = await answer_question(db, question.question)
        return {"answer": answer}
    finally:
        db.close()
