import pytest

from app.services.generation import generate_response


@pytest.mark.asyncio
async def test_generate_response():
    result = await generate_response("Responda apenas: OK")

    assert isinstance(result, str)
    assert result.strip()
