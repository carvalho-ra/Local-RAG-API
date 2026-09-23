import asyncio

from app.services.embedding import generate_embedding


def test_generate_embedding():
    embedding = asyncio.run(
        generate_embedding("Este é um teste de embedding.")
    )

    assert isinstance(embedding, list)
    assert len(embedding) == 768
    assert all(isinstance(value, float) for value in embedding)