import os

import httpx


OLLAMA_URL = os.environ["OLLAMA_URL"]
OLLAMA_EMBEDDING_MODEL = os.environ["OLLAMA_EMBEDDING_MODEL"]


async def generate_embedding(text: str) -> list[float]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{OLLAMA_URL}/api/embed",
            json={
                "model": OLLAMA_EMBEDDING_MODEL,
                "input": text,
            },
        )

        response.raise_for_status()

        data = response.json()

        return data["embeddings"][0]
