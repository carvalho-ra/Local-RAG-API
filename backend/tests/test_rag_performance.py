import time

import pytest

from app.database import SessionLocal
from app.services.context import build_context
from app.services.embedding import generate_embedding
from app.services.generation import generate_response
from app.services.ingestion import create_document
from app.services.retrieval import (
    expand_with_neighbors,
    search_similar_chunks,
)


@pytest.mark.asyncio
async def test_rag_performance():
    db = SessionLocal()

    question = "Qual curso aparece no certificado?"

    total_start = time.perf_counter()

    start = time.perf_counter()
    query_embedding = await generate_embedding(question)
    embedding_time = time.perf_counter() - start

    start = time.perf_counter()
    chunks = search_similar_chunks(
        db,
        query_embedding,
        limit=10,
    )
    retrieval_time = time.perf_counter() - start

    start = time.perf_counter()
    chunks = expand_with_neighbors(db, chunks)
    expansion_time = time.perf_counter() - start

    start = time.perf_counter()
    context = build_context(chunks)
    context_time = time.perf_counter() - start

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

    start = time.perf_counter()
    response = await generate_response(prompt)
    generation_time = time.perf_counter() - start

    total_time = time.perf_counter() - total_start

    print("\n=== RAG PERFORMANCE ===")
    print(f"Embedding:          {embedding_time:.3f}s")
    print(f"Retrieval:          {retrieval_time:.3f}s")
    print(f"Expansão vizinhos:  {expansion_time:.3f}s")
    print(f"Construção contexto:{context_time:.3f}s")
    print(f"Geração Ollama:     {generation_time:.3f}s")
    print("---------------------------")
    print(f"TOTAL:              {total_time:.3f}s")
    print(f"Chunks no contexto: {len(chunks)}")
    print(f"Resposta:           {response}")

    db.close()
