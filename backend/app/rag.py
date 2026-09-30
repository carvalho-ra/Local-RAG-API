from app.services.context import build_context
from app.services.generation import generate_response
from app.services.retrieval import retrieve_chunks


async def answer_question(db, question: str) -> str:
    chunks = await retrieve_chunks(db, question, limit=5)

    context = build_context(chunks)

    prompt = f"""Você é um assistente que responde perguntas usando exclusivamente o contexto fornecido.

    Regras:
    - Use somente informações explicitamente presentes no contexto.
    - Não invente, suponha ou complete informações ausentes.
    - Responda somente ao que foi perguntado.
    - Não inclua informações irrelevantes.
    - Consolide informações repetidas e não repita a mesma informação.
    - Se a pergunta solicitar várias informações, liste todas as informações relevantes disponíveis no contexto.
    - Se a informação solicitada não estiver no contexto, diga que não encontrou a resposta.
    - Não use conhecimento externo.
    - Responda em português.

    Contexto:
    {context}

    Pergunta:
    {question}

    Resposta:
    """
    return await generate_response(prompt)
