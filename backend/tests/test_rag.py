from unittest.mock import AsyncMock, patch

import pytest

from app.rag import answer_question


@pytest.mark.asyncio
async def test_answer_question():
    db = object()

    with (
        patch("app.rag.retrieve_chunks", new_callable=AsyncMock) as retrieve,
        patch("app.rag.build_context") as context,
        patch("app.rag.generate_response", new_callable=AsyncMock) as generate,
    ):
        retrieve.return_value = ["chunk 1", "chunk 2"]
        context.return_value = "contexto"
        generate.return_value = "resposta final"

        result = await answer_question(db, "Qual é a pergunta?")

        assert result == "resposta final"

        retrieve.assert_awaited_once_with(db, "Qual é a pergunta?")
        context.assert_called_once_with(["chunk 1", "chunk 2"])
        generate.assert_awaited_once()
