from sqlalchemy import select

from app.models import Chunk
from app.services.embedding import generate_embedding


def search_similar_chunks(db, query_embedding, limit=5):
    statement = (
        select(Chunk)
        .where(Chunk.embedding.is_not(None))
        .order_by(Chunk.embedding.cosine_distance(query_embedding))
        .limit(limit)
    )

    return db.scalars(statement).all()


def expand_with_neighbors(db, chunks):
    expanded = {}

    for chunk in chunks:
        expanded[chunk.id] = chunk

        statement = select(Chunk).where(
            Chunk.document_id == chunk.document_id,
            Chunk.chunk_index.in_(
                [chunk.chunk_index - 1, chunk.chunk_index + 1]
            ),
        )

        neighbors = db.scalars(statement).all()

        for neighbor in neighbors:
            expanded[neighbor.id] = neighbor

    return sorted(
        expanded.values(),
        key=lambda chunk: (chunk.document_id, chunk.chunk_index),
    )


async def retrieve_chunks(db, question, limit=5):
    query_embedding = await generate_embedding(question)

    chunks = search_similar_chunks(
        db,
        query_embedding,
        limit,
    )

    return expand_with_neighbors(db, chunks)