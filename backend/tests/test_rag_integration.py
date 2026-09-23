import pytest

from app.database import SessionLocal
from app.rag import answer_question


@pytest.mark.asyncio
async def test_rag_returns_response():
    db = SessionLocal()

    try:
        response = await answer_question(
            db,
            "Qual é o assunto principal do documento?",
        )
        
        assert isinstance(response, str)
        assert response.strip()

    finally:
        db.close()
