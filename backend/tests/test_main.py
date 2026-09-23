import httpx
import pytest
from unittest.mock import AsyncMock, patch

from app.main import app


@pytest.mark.asyncio
async def test_ask():
    with patch(
        "app.main.answer_question",
        new_callable=AsyncMock,
    ) as answer:
        answer.return_value = "resposta final"

        transport = httpx.ASGITransport(app=app)

        async with httpx.AsyncClient(
            transport=transport,
            base_url="http://test",
        ) as client:
            response = await client.post(
                "/ask",
                json={"question": "Qual é a pergunta?"},
            )

        assert response.status_code == 200
        assert response.json() == {"answer": "resposta final"}


@pytest.mark.asyncio
async def test_ask_requires_question():
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/ask",
            json={},
        )

    assert response.status_code == 422