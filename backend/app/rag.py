from app.services.context import build_context
from app.services.generation import generate_response
from app.services.retrieval import retrieve_chunks


async def answer_question(db, question: str) -> str:
    chunks = await retrieve_chunks(db, question)

    context = build_context(chunks)

    prompt = f"""Contexto:
{context}

Pergunta:
{question}
"""

    return await generate_response(prompt)
