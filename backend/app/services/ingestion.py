from app.models import Document
from app.storage import upload_file
import uuid


def create_document(db, filename, content_type, storage_key) -> Document:
    doc = Document(
        filename = filename,
        content_type = content_type,
        storage_key = storage_key,
    )

    db.add(doc)
    db.commit()
    return doc


def ingest_document(db, file_data, filename, content_type) -> Document:
    storage_key = f"{uuid.uuid4()}-{filename}"
    upload_file(file_data, storage_key, content_type)
    doc = create_document(db, filename, content_type, storage_key)
    return doc
