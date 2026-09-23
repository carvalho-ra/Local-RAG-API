from app.database import SessionLocal
from app.services.ingestion import create_document


def test_create_document():
    db = SessionLocal()

    document = create_document(db, "file.pdf", "conteúdo")

    assert document.id is not None
    assert document.filename == "file.pdf"
    assert document.content == "conteúdo"
    
    db.close()
