from app.models import Document


def create_document(db, filename, content) -> Document:
    doc = Document(
        filename = filename,
        content = content,
    )

    db.add(doc)
    db.commit()
    return doc
