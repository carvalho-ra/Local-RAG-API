import pytest

from app.database import SessionLocal
from app.rag import answer_question


@pytest.mark.asyncio
async def test_rag_returns_response():
    db = SessionLocal()

    try:
        response = await answer_question(
            db,
            "Qual é o nome do curso concluído por Rodrigo Carvalho?",
        )

        # print(f"\nResposta do RAG: {response}")

        assert "Fundamentos do Python 1" in response

    finally:
        db.close()
