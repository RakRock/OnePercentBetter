.PHONY: install dev backend frontend test lint

# Local development (venv + SQLite — no Docker)
install:
	cd backend && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

dev:
	@bash scripts/dev.sh

backend:
	@bash scripts/dev.sh

frontend:
	cd frontend && npm install && npm run dev

test:
	cd backend && .venv/bin/env TESTING=1 pytest -q 2>/dev/null || (cd backend && TESTING=1 python3 -m pytest -q)

lint:
	cd backend && .venv/bin/ruff check app 2>/dev/null || ruff check app
