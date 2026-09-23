import pytest
import httpx

from app.main import app


@pytest.mark.asyncio
async def test_ask_integration():
    transport = httpx.ASGITransport(app=app)

    async with httpx.AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/ask",
            json={
                "question": "Qual é o nome do curso concluído por Rodrigo Carvalho?"
            },
        )

    assert response.status_code == 200
    assert "Fundamentos do Python 1" in response.json()["answer"]
