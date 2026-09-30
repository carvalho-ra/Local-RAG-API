from app.database import SessionLocal
from app.models import Chunk
from app.services.ingestion import create_document
from app.services.retrieval import search_similar_chunks, retrieve_chunks
from app.services.embedding import generate_embedding
import pytest


def test_search_similar_chunks():
    db = SessionLocal()

    document = create_document(
        db,
        "test.pdf",
        "application/pdf",
        "test.pdf",
    )

    chunk_1 = Chunk(
        document_id=document.id,
        chunk_index=0,
        content="primeiro chunk",
        embedding=[1.0] + [0.0] * 767,
    )

    chunk_2 = Chunk(
        document_id=document.id,
        chunk_index=1,
        content="segundo chunk",
        embedding=[0.0, 1.0] + [0.0] * 766,
    )

    db.add_all([chunk_1, chunk_2])
    db.commit()

    query_embedding = [1.0] + [0.0] * 767

    results = search_similar_chunks(
        db,
        query_embedding,
        limit=1,
    )

    assert len(results) == 1
    assert results[0].content == "primeiro chunk"

    db.close()


@pytest.mark.asyncio
async def test_retrieve_chunks():
    db = SessionLocal()

    document = create_document(
        db,
        "test.pdf",
        "application/pdf",
        "test.pdf",
    )

    chunk_1 = Chunk(
        document_id=document.id,
        chunk_index=0,
        content="Python é uma linguagem de programação.",
        embedding=await generate_embedding(
            "Python é uma linguagem de programação."
        ),
    )

    chunk_2 = Chunk(
        document_id=document.id,
        chunk_index=1,
        content="O Rio de Janeiro é uma cidade brasileira.",
        embedding=await generate_embedding(
            "O Rio de Janeiro é uma cidade brasileira."
        ),
    )

    db.add_all([chunk_1, chunk_2])
    db.commit()

    results = await retrieve_chunks(
        db,
        "O que é Python?",
        limit=1,
    )

    assert len(results) == 1
    assert results[0].content == "Python é uma linguagem de programação."

    db.close()