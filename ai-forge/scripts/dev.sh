#!/usr/bin/env bash
# Start AI Forge backend locally (venv + SQLite — no Docker).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKEND="$ROOT/backend"
VENV="$BACKEND/.venv"

cd "$BACKEND"

if [[ ! -d "$VENV" ]]; then
  echo "Creating venv at $VENV ..."
  python3 -m venv "$VENV"
fi

# shellcheck disable=SC1091
source "$VENV/bin/activate"

pip install -q -r requirements.txt

mkdir -p "$ROOT/data"
# Local venv dev always uses SQLite (ignores Postgres URLs in .env / shell)
export DATABASE_URL="sqlite+aiosqlite:///$ROOT/data/aiforge.db"
export AIFORGE_ENV_FILE="$ROOT/.env"

echo ""
echo "  AI Forge API → http://localhost:8000"
echo "  API docs     → http://localhost:8000/docs"
echo "  Database     → $DATABASE_URL"
echo ""
echo "  Frontend (optional, separate terminal):"
echo "    cd $ROOT/frontend && npm install && npm run dev"
echo ""

exec uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
