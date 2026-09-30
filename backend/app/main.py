from fastapi import FastAPI, UploadFile, File

from app.database import SessionLocal
from app.rag import answer_question
from app.schemas import AskRequest, AskResponse
from app.services.ingestion import ingest_document, DocumentAlreadyExistsError
from app.models import Conversation, Document, Message

app = FastAPI(title="Local RAG API")


@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ask", response_model=AskResponse)
async def ask(question: AskRequest):
    db = SessionLocal()

    try:
        if question.conversation_id is None:
            conversation = Conversation()
            db.add(conversation)
            db.flush()
        else:
            conversation = db.get(Conversation, question.conversation_id)

            if conversation is None:
                return {"error": "Conversation not found"}

        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=question.question,
        )
        db.add(user_message)

        answer = await answer_question(db, question.question)

        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=answer,
        )
        db.add(assistant_message)

        db.commit()

        return {
            "conversation_id": conversation.id,
            "answer": answer,
        }
    finally:
        db.close()


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    db = SessionLocal()

    try:
        try:
            document = await ingest_document(
                db,
                file,
                file.filename,
                file.content_type,
            )
        except DocumentAlreadyExistsError:
            return {
                "error": "Document already exists",
            }

        if document is None:
            return {"error": "Unsupported file type"}

        return {
            "filename": document.filename,
            "message": "File uploaded successfully",
        }
    finally:
        db.close()


@app.get("/documents")
async def list_documents():
    db = SessionLocal()

    try:
        documents = db.query(Document).order_by(Document.created_at.desc()).all()

        return [
            {
                "id": document.id,
                "filename": document.filename,
                "created_at": document.created_at,
            }
            for document in documents
        ]
    finally:
        db.close()
