from fastapi import FastAPI

from app.database import get_connection


app = FastAPI(title="Local RAG API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/db")
def health_db():
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()

    return {"status": "ok", "database": result[0]}