.DEFAULT_GOAL := up

.PHONY: help up down test migrate migration db db_query

TABLE ?= documents

help:
	@echo "Available commands:"
	@echo "  make up          Start containers"
	@echo "  make down        Stop containers"
	@echo "  make test        Run tests"
	@echo "  make migrate     Apply database migrations"
	@echo "  make migration   Create a new migration"
	@echo "  make db          Open PostgreSQL shell"
	@echo "  make db_query    Query a PostgreSQL table"

up:
	docker compose up -d --build

down:
	docker compose down

test:
	docker compose exec backend pytest -v

migrate:
	docker compose exec backend alembic upgrade head

migration:
	docker compose exec backend alembic revision --autogenerate -m "$(MSG)"

db:
	docker compose exec postgres psql -U rag -d rag

db_query:
	docker compose exec postgres psql -U rag -d rag -c "SELECT * FROM $(TABLE)"