# Local RAG API

A local Retrieval-Augmented Generation (RAG) application for querying documents through a conversational interface.

The project uses Ollama for local embeddings and text generation, PostgreSQL with pgvector for semantic search, MinIO for document storage, and a React frontend.

The goal was to build a complete RAG application, from document ingestion and vector storage to semantic retrieval, local generation and persistent conversations.

## Features

* Upload and process PDF, Markdown and plain-text documents.
* Automatic text extraction and chunking.
* Embeddings generated locally with Ollama.
* Semantic search with PostgreSQL and pgvector.
* Local text generation with Ollama.
* Persistent conversations and messages.
* Original documents stored in MinIO.
* React + TypeScript frontend.
* FastAPI backend.
* Docker-based environment.
* Automated backend tests.

## Stack

* Python 3.12
* FastAPI
* PostgreSQL
* pgvector
* SQLAlchemy
* Alembic
* MinIO
* Ollama
* React
* TypeScript
* Vite
* Docker
* Docker Compose
* pytest

## How it works

The application follows a RAG pipeline:

```text
Document
   |
   v
Text extraction
   |
   v
Chunking
   |
   v
Embedding generation
   |
   v
PostgreSQL + pgvector
```

When the user asks a question, the question follows a similar embedding process:

```text
User question
   |
   v
Question embedding
   |
   v
Semantic search
   |
   v
Relevant document chunks
   |
   v
Context + question
   |
   v
Ollama
   |
   v
Answer
```

Both document chunks and user questions are represented as vectors. The application uses cosine similarity to retrieve the document chunks that are most relevant to the question.

The current chunk configuration is:

```text
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
```

## Running locally

### Requirements

* Docker
* Docker Compose

Configure the environment:

```bash
cp .env.example .env
```

Then start the application:

```bash
make
```

That's it.

The project starts the required services and applies the database migrations.

The application is available at:

```text
http://localhost:5173
```

The API is available at:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

## API

The main question-answering endpoint is:

```http
POST /ask
```

The complete API documentation is available through Swagger at `/docs`.

## Testing

Run the backend tests with:

```bash
make test
```

The frontend can also be checked with:

```bash
cd frontend
npm run build
npm run lint
```

## Project structure

```text
Local-RAG-API/
├── backend/
│   ├── alembic/
│   ├── app/
│   └── tests/
├── frontend/
│   ├── public/
│   └── src/
├── docker-compose.yml
├── Makefile
├── .env.example
└── README.md
```

## Why I built it

I wanted to build a project that went beyond simply calling an external AI API.

The idea was to understand and implement the infrastructure around a real AI application: document processing, embeddings, vector search, retrieval, local generation, persistence and a user interface.

The project gave me practical experience with:

* Python and FastAPI
* PostgreSQL and pgvector
* RAG architecture
* Embeddings and semantic search
* Local LLMs with Ollama
* Document processing
* Object storage with MinIO
* Docker
* React and TypeScript
* Automated testing

The result is a small but complete application that can ingest documents and use them as a knowledge base for a local AI assistant.
