.PHONY: install setup test lint run up down

install:
	uv sync

setup:
	uv python install
	uv sync

test:
	uv run pytest

lint:
	uv run ruff check .
	uv run ruff format .

run:
	uv run main.py

up:
	docker compose up --build

down:
	docker compose down