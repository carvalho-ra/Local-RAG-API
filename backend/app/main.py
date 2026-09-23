from fastapi import FastAPI

from app.database import get_connection


app = FastAPI(title="Local RAG API")


@app.get("/health")
def health():
    return {"status": "ok"}
