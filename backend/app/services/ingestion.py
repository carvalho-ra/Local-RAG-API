from app.models import Document, Chunk
from app.storage import upload_file
from app.services.embedding import generate_embedding
import uuid
from pathlib import Path
from io import BytesIO
from pypdf import PdfReader


ALLOWED_FILE_TYPES = {
    ".pdf": "application/pdf",
    ".md": "text/markdown",
    ".txt": "text/plain",
}

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def validate_file_type(filename, content_type) -> bool:
    extension = Path(filename).suffix.lower()
    if ALLOWED_FILE_TYPES.get(extension) == content_type:
        return True
    return False


def create_document(db, filename, content_type, storage_key) -> Document:
    doc = Document(
        filename = filename,
        content_type = content_type,
        storage_key = storage_key,
    )

    db.add(doc)
    db.commit()
    return doc


def extract_text(file_data: bytes, content_type: str) -> str:
    if content_type in ("text/plain", "text/markdown"):
        return file_data.decode("utf-8")

    if content_type == "application/pdf":
        reader = PdfReader(BytesIO(file_data))
        text = "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        )

        return text.replace("\x00", "")

    raise ValueError(f"Unsupported content type: {content_type}")

def chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be between 0 and chunk_size")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])

        if end >= len(text):
            break

        start += chunk_size - overlap

        if len(text) - start <= overlap:
            break

    return chunks


async def create_chunks(db, document, chunks):
    chunk_objs = []

    for content in chunks:
        embedding = await generate_embedding(content)
        chunk_objs.append(
            Chunk(
                document_id=document.id,
                content=content,
                embedding=embedding,
            )
        )

    db.add_all(chunk_objs)
    db.commit()

    return chunk_objs


async def ingest_document(db, file_data, filename, content_type) -> Document|None:
    if validate_file_type(filename, content_type):
        file_data = file_data.read()

        storage_key = f"{uuid.uuid4()}-{filename}"

        upload_file(BytesIO(file_data), storage_key, content_type)

        document = create_document(db, filename, content_type, storage_key)

        text = extract_text(file_data, content_type)

        chunks = chunk_text(
            text,
            CHUNK_SIZE,
            CHUNK_OVERLAP,
        )

        await create_chunks(db, document, chunks)

        return document
    
    return None
