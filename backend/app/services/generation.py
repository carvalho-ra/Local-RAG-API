import os

import httpx


OLLAMA_URL = os.environ["OLLAMA_URL"]
OLLAMA_MODEL = os.environ["OLLAMA_MODEL"]


async def generate_response(prompt: str) -> str:
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 128,
                },
            },
        )

        response.raise_for_status()

        data = response.json()

        return data["response"]