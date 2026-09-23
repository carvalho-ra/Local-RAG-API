from app.database import SessionLocal
from app.services.ingestion import (
    create_document,
    ingest_document,
    validate_file_type,
    )


def test_create_document():
    db = SessionLocal()

    document = create_document(
        db,
        "file.pdf",
        "application/pdf",
        "test/file.pdf",
    )

    assert document.id is not None
    assert document.filename == "file.pdf"
    assert document.content_type == "application/pdf"
    assert document.storage_key == "test/file.pdf"

    db.close()


def test_ingest_document_pdf():
    db = SessionLocal()
    file = open("tests/fixtures/test.pdf", "rb")

    document = ingest_document(
        db,
        file,
        "injection.pdf",
        "application/pdf",
    )

    assert document.id is not None
    assert document.filename == "injection.pdf"
    assert document.content_type == "application/pdf"
    assert document.storage_key.endswith("-injection.pdf")

    db.close()

def test_ingest_document_md():
    db = SessionLocal()
    file = open("tests/fixtures/README.md", "rb")

    document = ingest_document(
        db,
        file,
        "README.md",
        "text/markdown",
    )

    assert document.id is not None
    assert document.filename == "README.md"
    assert document.content_type == "text/markdown"
    assert document.storage_key.endswith("-README.md")

    db.close()


def test_validate_file_type():
    assert validate_file_type("file.pdf", "application/pdf")
    assert validate_file_type("file.md", "text/markdown")
    assert validate_file_type("file.txt", "text/plain")


def test_validate_file_type_rejects_invalid_type():
    assert not validate_file_type("file.pdf", "text/plain")
    assert not validate_file_type("file.md", "application/pdf")
    assert not validate_file_type("file.exe", "application/pdf")