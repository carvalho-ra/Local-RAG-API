from app.database import SessionLocal
from app.services.ingestion import (
    create_document,
    ingest_document,
    validate_file_type,
    extract_text,
    chunk_text,
    create_chunks,
    )
import pytest, pytest_asyncio


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


def test_validate_file_type():
    assert validate_file_type("file.pdf", "application/pdf")
    assert validate_file_type("file.md", "text/markdown")
    assert validate_file_type("file.txt", "text/plain")


def test_validate_file_type_rejects_invalid_type():
    assert not validate_file_type("file.pdf", "text/plain")
    assert not validate_file_type("file.md", "application/pdf")
    assert not validate_file_type("file.exe", "application/pdf")


@pytest.mark.asyncio
async def test_ingest_document_pdf():
    db = SessionLocal()
    file = open("tests/fixtures/test.pdf", "rb")

    document = await ingest_document(
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


@pytest.mark.asyncio
async def test_ingest_document_md():
    db = SessionLocal()
    file = open("tests/fixtures/README.md", "rb")

    document = await ingest_document(
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


@pytest.mark.asyncio
async def test_ingest_document_exe():
    db = SessionLocal()
    file = open("tests/fixtures/test.exe", "rb")

    document = await ingest_document(
        db,
        file,
        "test.exe",
        "text/markdown",
    )

    assert document == None

    file.close()
    db.close()


def test_extract_text_txt():
    content = "Hello RAG!"
    result = extract_text(content.encode("utf-8"), "text/plain")

    assert result == content


def test_extract_text_markdown():
    content = "# Hello RAG\n\nThis is a document."
    result = extract_text(content.encode("utf-8"), "text/markdown")

    assert result == content


def test_extract_text_pdf():
    with open("tests/fixtures/test.pdf", "rb") as file:
        file_data = file.read()

    result = extract_text(file_data, "application/pdf")

    assert isinstance(result, str)
    assert result.strip()


def test_extract_text_unsupported_type():
    with pytest.raises(ValueError):
        extract_text(b"content", "application/octet-stream")


def test_chunk_text():
    result = chunk_text("ABCDEFGHIJ", 6, 2)

    assert result == [
        "ABCDEF",
        "EFGHIJ",
    ]


@pytest.mark.asyncio
async def test_create_chunks():
    db = SessionLocal()
    document = create_document(
        db,
        "test.pdf",
        "application/pdf",
        "test.pdf",
    )

    chunks = await create_chunks(
        db,
        document,
        ["primeiro chunk", "segundo chunk"],
    )

    assert len(chunks) == 2
    assert chunks[0].content == "primeiro chunk"
    assert chunks[1].content == "segundo chunk"
    assert chunks[0].document_id == document.id

    db.close()
