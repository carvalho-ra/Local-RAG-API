from app.services.context import build_context
from app.services.generation import generate_response
from app.services.retrieval import retrieve_chunks


async def answer_question(db, question: str) -> str:
    chunks = await retrieve_chunks(db, question, limit=10)

    context = build_context(chunks)

    prompt = f"""Responda diretamente à pergunta usando apenas o contexto abaixo.
    Extraia somente a informação solicitada pela pergunta.
    Não inclua outras informações do contexto.
    Se a informação solicitada não estiver no contexto, diga que não encontrou a resposta.
    
    Contexto:
    {context}

    Pergunta:
    {question}

    Responda em português:
    """

    return await generate_response(prompt)
