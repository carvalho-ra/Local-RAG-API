from fastapi import FastAPI, UploadFile, File

from app.database import SessionLocal
from app.rag import answer_question
from app.schemas import AskRequest, AskResponse
from app.services.ingestion import ingest_document


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


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    db = SessionLocal()

    try:
        document = await ingest_document(
            db,
            file,
            file.filename,
            file.content_type,
        )

        if document is None:
            return {"error": "Unsupported file type"}

        return {
            "filename": document.filename,
            "message": "File uploaded successfully",
        }
    finally:
        db.close()
