from app.models import Document
from app.storage import upload_file
import uuid
from pathlib import Path


ALLOWED_FILE_TYPES = {
    ".pdf": "application/pdf",
    ".md": "text/markdown",
    ".txt": "text/plain",
}


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


def ingest_document(db, file_data, filename, content_type) -> Document|None:
    if validate_file_type(filename, content_type):
        storage_key = f"{uuid.uuid4()}-{filename}"
        upload_file(file_data, storage_key, content_type)
        doc = create_document(db, filename, content_type, storage_key)
        return doc
    else:
        return None

