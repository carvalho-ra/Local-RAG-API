from fastapi import FastAPI


app = FastAPI(title="Local RAG API")


@app.get("/health")
def health():
    return {"status": "ok"}
