.DEFAULT_GOAL := up

include .env

UID := $(shell id -u)
GID := $(shell id -g)

export UID
export GID

TABLE ?= documents

help:
	@echo "Available commands:"
	@echo "  make up                 Start containers"
	@echo "  make down               Stop containers"
	@echo "  make test               Run tests"
	@echo "  make migrate            Apply database migrations"
	@echo "  make migration          Create a new migration"
	@echo "  make db                 Open PostgreSQL shell"
	@echo "  make db_query            Query a PostgreSQL table"
	@echo "  make db_table_clear      Clear a PostgreSQL table"
	@echo "  make db_clear            Clear all PostgreSQL tables"
	@echo "  make storage_list         List storage files"
	@echo "  make storage_clear        Clear all storage files"

up:
	@docker compose up -d --build
	@$(MAKE) --no-print-directory migrate

down:
	@docker compose down

test:
	@docker compose exec backend pytest -v

migrate:
	@docker compose exec backend alembic upgrade head

migration:
	@docker compose exec backend alembic revision --autogenerate -m "$(MSG)"

db:
	@docker compose exec postgres psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

db_query:
	@docker compose exec postgres psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) \
		-c "SELECT * FROM $(TABLE)"

db_table_clear:
	@docker compose exec postgres psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) \
		-c "TRUNCATE TABLE $(TABLE) RESTART IDENTITY CASCADE"

db_clear:
	@$(MAKE) --no-print-directory db_table_clear TABLE=documents
	@$(MAKE) --no-print-directory db_table_clear TABLE=chunks

storage_list:
	@docker compose exec backend python scripts/storage_list.py

storage_clear:
	@docker compose exec backend python scripts/storage_clear.py

clean:
	@docker compose down -v

fclean:
	@docker compose down -v --remove-orphans --rmi all

.PHONY: help up down test migrate migration db db_query db_table_clear db_clear \
	storage_list storage_clear clean fclean
