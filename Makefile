COMPOSE_DB_FILE := docker-compose.db.yml
TEST_DB_URL := postgresql+asyncpg://postgres@localhost:5432/devsprint

.PHONY: db-up db-down test

db-up:
	@docker compose -f $(COMPOSE_DB_FILE) up -d

db-down:
	@docker compose -f $(COMPOSE_DB_FILE) down

test: db-up
	@TEST_DATABASE_URL=$(TEST_DB_URL) pytest
