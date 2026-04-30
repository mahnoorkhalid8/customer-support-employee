# Makefile for Customer Success FTE

.PHONY: help install setup start stop restart logs test clean

help:
	@echo "Customer Success FTE - Available Commands"
	@echo "=========================================="
	@echo "make install    - Install Python dependencies"
	@echo "make setup      - Run setup script"
	@echo "make verify     - Verify project setup"
	@echo "make start      - Start all services with Docker Compose"
	@echo "make stop       - Stop all services"
	@echo "make restart    - Restart all services"
	@echo "make logs       - View logs from all services"
	@echo "make logs-api   - View API logs"
	@echo "make logs-worker - View worker logs"
	@echo "make test       - Run tests"
	@echo "make clean      - Clean up containers and volumes"
	@echo "make db-init    - Initialize database"
	@echo "make db-shell   - Open PostgreSQL shell"

install:
	pip install -r requirements.txt

setup:
	python setup.py

verify:
	python verify_setup.py

start:
	docker-compose up -d
	@echo "Services started. API available at http://localhost:8000"

stop:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

logs-api:
	docker-compose logs -f api

logs-worker:
	docker-compose logs -f worker

test:
	pytest tests/ -v

clean:
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

db-init:
	docker-compose exec postgres psql -U fte_user -d fte_db -f /docker-entrypoint-initdb.d/01-schema.sql

db-shell:
	docker-compose exec postgres psql -U fte_user -d fte_db

dev-api:
	uvicorn production.api.main:app --reload --port 8000

dev-worker:
	python production/workers/message_processor.py
