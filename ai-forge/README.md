# AI Forge

**AI Forge** is a production-oriented AI engineering learning platform for Rakesh (and motivated engineers). Phase 1 delivers authentication stubs, dashboard, Claude-powered mentor chat, and the first project lab.

## Architecture

```
┌─────────────┐     REST/SSE      ┌──────────────┐
│  Next.js 15 │ ◄──────────────► │   FastAPI    │
│  (frontend) │                   │   (backend)  │
└─────────────┘                   └──────┬───────┘
                                         │
                    ┌────────────────────┼────────────────────┐
                    ▼                    ▼                    ▼
              PostgreSQL              Redis              Qdrant
              (Phase 1)            (Phase 2+)         (Phase 2+)
```

See [ARCHITECTURE.md](./ARCHITECTURE.md) for module breakdown and phased roadmap.

## Quick start

### Prerequisites

- Docker & Docker Compose
- [Anthropic API key](https://console.anthropic.com/) for mentor chat

### 1. Configure environment

```bash
cd ai-forge
cp .env.example .env
# Edit .env — set ANTHROPIC_API_KEY at minimum
```

### 2. Run the stack

```bash
make up
```

| Service   | URL                    |
|-----------|------------------------|
| Frontend  | http://localhost:3000  |
| API       | http://localhost:8000 |
| API docs  | http://localhost:8000/docs |
| Postgres  | localhost:5433         |
| Qdrant    | http://localhost:6333  |

### 3. Open the app

Visit http://localhost:3000 → **Enter the forge** → Dashboard, Mentor, or **Build a RAG Assistant** project.

## OnePercent (Streamlit) bridge

Rakesh's dashboard in the family app links to AI Forge:

1. Set `AIFORGE_PUBLIC_URL` (e.g. `http://localhost:3000` or your deployed URL).
2. In OnePercent, choose **Rakesh** → **Open AI Forge**.

## Phase 1 features

| Module | Status |
|--------|--------|
| Dev auth (`X-Forge-User-Id` headers) | ✅ |
| User dashboard | ✅ |
| AI mentor (Claude + LangGraph) | ✅ |
| Project lab (RAG assistant) | ✅ |
| Evaluation stub | ✅ |
| Sandbox execution | Phase 2 |
| Full RAG ingestion | Phase 2 |
| Multi-agent orchestration | Phase 3 |
| GitHub / portfolio | Phase 3 |

## Local development (without Docker)

**Backend:**

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL=postgresql+asyncpg://aiforge:aiforge@localhost:5433/aiforge
export ANTHROPIC_API_KEY=sk-ant-...
uvicorn app.main:app --reload --port 8000
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

## API overview

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/api/v1/auth/me` | Current user (auto-provisioned) |
| GET | `/api/v1/projects` | List project labs |
| GET | `/api/v1/projects/{slug}` | Project detail + checkpoints |
| POST | `/api/v1/mentor/chat/sync` | Mentor reply (non-streaming) |
| POST | `/api/v1/mentor/chat` | Mentor reply (SSE stream) |
| POST | `/api/v1/evaluation/submit` | Submit for evaluation |

## Tests

```bash
cd backend
TESTING=1 pytest -q
```

## Deployment (outline)

- **Backend:** Railway / Render / Fly.io — set `DATABASE_URL`, `ANTHROPIC_API_KEY`, `CORS_ORIGINS`
- **Frontend:** Vercel — set `NEXT_PUBLIC_API_URL` to your API URL
- **Database:** Managed PostgreSQL
- **Phase 2+:** Redis, Celery workers, Qdrant Cloud

## License

Private — family learning project.
