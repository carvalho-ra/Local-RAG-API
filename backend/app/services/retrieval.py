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


async def retrieve_chunks(db, question, limit=5):
    query_embedding = await generate_embedding(question)

    return search_similar_chunks(
        db,
        query_embedding,
        limit,
    )
