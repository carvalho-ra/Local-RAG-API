from app.database import SessionLocal
from app.models import Chunk
from app.services.ingestion import create_document
from app.services.retrieval import (
    search_similar_chunks,
    retrieve_chunks,
    expand_with_neighbors,
    )
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

    assert len(results) == 2
    assert results[0].content == "Python é uma linguagem de programação."
    assert results[1].content == "O Rio de Janeiro é uma cidade brasileira."

    db.close()


def test_expand_with_neighbors():
    db = SessionLocal()

    document = create_document(
        db,
        "test.pdf",
        "application/pdf",
        "test.pdf",
    )

    chunks = [
        Chunk(
            document_id=document.id,
            chunk_index=i,
            content=f"chunk {i}",
            embedding=[1.0] + [0.0] * 767,
        )
        for i in range(4)
    ]

    db.add_all(chunks)
    db.commit()

    results = expand_with_neighbors(
        db,
        [chunks[1], chunks[2]],
    )

    indexes = [chunk.chunk_index for chunk in results]

    assert indexes == [0, 1, 2, 3]
    assert len(results) == 4

    db.close()