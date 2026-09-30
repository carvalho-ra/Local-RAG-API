.DEFAULT_GOAL := up

include .env

UID := $(shell id -u)
GID := $(shell id -g)

export UID
export GID

GREEN := \033[0;32m
YELLOW := \033[0;33m
CYAN := \033[0;36m
RED := \033[0;31m
BOLD := \033[1m
RESET := \033[0m

TABLE ?= documents

help:
	@echo "Available commands:"
	@echo "  make info               API infos"
	@echo "  make up                 Start containers"
	@echo "  make prod               Start production frontend"
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

info:
	@IP=$$(hostname -I | awk '{print $$1}'); \
	echo ""; \
	echo "$(GREEN)$(BOLD)Local RAG API$(RESET)"; \
	echo "────────────────────────────────────────"; \
	echo "$(YELLOW)$(BOLD)Frontend:$(RESET)             $(CYAN)http://localhost:5173$(RESET)"; \
	echo "$(YELLOW)$(BOLD)Production Frontend:$(RESET)  $(CYAN)http://localhost:8080$(RESET)"; \
	echo "$(YELLOW)$(BOLD)API:$(RESET)                  $(CYAN)http://localhost:8000$(RESET)"; \
	echo "$(YELLOW)$(BOLD)Swagger:$(RESET)              $(CYAN)http://localhost:8000/docs$(RESET)"; \
	echo ""; \
	echo "$(GREEN)$(BOLD)Rede local$(RESET)"; \
	echo "────────────────────────────────────────"; \
	echo "$(YELLOW)$(BOLD)Frontend:$(RESET)             $(RED)http://$$IP:5173$(RESET)"; \
	echo "$(YELLOW)$(BOLD)Production Frontend:$(RESET)  $(RED)http://$$IP:8080$(RESET)"; \
	echo "$(YELLOW)$(BOLD)API:$(RESET)                  $(RED)http://$$IP:8000$(RESET)"; \
	echo "$(YELLOW)$(BOLD)Swagger:$(RESET)              $(RED)http://$$IP:8000/docs$(RESET)"; \
	echo "────────────────────────────────────────"; \
	echo ""
	
up:
	@docker compose up -d --build
	@$(MAKE) --no-print-directory migrate
	@$(MAKE) --no-print-directory info

prod: up
	@docker compose -f docker-compose.yml down frontend
	@docker compose -f docker-compose.prod.yml up -d --build
	@$(MAKE) --no-print-directory info

down: clean-pycache
	@docker compose down

test:
	@docker compose exec postgres sh -c 'psql -U $(POSTGRES_USER) -d postgres -c "DROP DATABASE IF EXISTS rag_test WITH (FORCE)"'
	@docker compose exec postgres sh -c 'psql -U $(POSTGRES_USER) -d postgres -c "CREATE DATABASE rag_test"'
	@docker compose exec -e DATABASE_URL=postgresql+psycopg://$(POSTGRES_USER):$(POSTGRES_PASSWORD)@postgres:5432/rag_test backend alembic upgrade head
	@docker compose exec -e DATABASE_URL=postgresql+psycopg://$(POSTGRES_USER):$(POSTGRES_PASSWORD)@postgres:5432/rag_test backend pytest -v
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

clean-pycache:
	@find . -type d \( -name "__pycache__" -o -name ".pytest_cache" \) -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete

clean:
	@docker compose down -v

fclean:
	@docker compose down -v --remove-orphans --rmi all

.PHONY: help info up prod down test migrate migration db db_query db_table_clear db_clear \
	storage_list storage_clear clean-pycache clean fclean
