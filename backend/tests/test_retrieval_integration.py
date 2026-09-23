import pytest

from app.database import SessionLocal
from app.services.retrieval import retrieve_chunks


@pytest.mark.asyncio
async def test_retrieve_chunks_for_certificate():
    db = SessionLocal()

    try:
        chunks = await retrieve_chunks(
            db,
            "Certificado",
        )

        # for chunk in chunks:
        #     print(f"\nCHUNK:\n{chunk.content}")

        assert chunks

    finally:
        db.close()
    