from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from fastapi import FastAPI

from app.rag import answer_question
from app.main import app


client = TestClient(app)


def test_ask():
    with patch(
        "app.main.answer_question",
        new_callable=AsyncMock,
    ) as answer:
        answer.return_value = "resposta final"

        response = client.post(
            "/ask",
            json={"question": "Qual é a pergunta?"},
        )

        assert response.status_code == 200
        assert response.json() == {"answer": "resposta final"}
