"""Seed learning paths, lessons, and first project lab."""

from sqlalchemy import select

from app.core.database import SessionLocal
from app.models import Checkpoint, LearningPath, Lesson, Project

RAG_ARCHITECTURE = """
flowchart LR
  User[User] --> API[FastAPI]
  API --> Embed[Embedding Service]
  Embed --> Qdrant[(Qdrant)]
  API --> LLM[Claude]
  Qdrant --> RAG[RAG Retriever]
  RAG --> LLM
  LLM --> API
"""

SCAFFOLD = {
    "README.md": """# RAG Assistant Starter

Production-style retrieval-augmented generation assistant.

## Run locally
```bash
docker compose up --build
```

## Features
- Document ingestion
- Semantic search (Qdrant)
- Claude-powered answers with citations
""",
    "architecture.md": """# Architecture

- **API**: FastAPI
- **Vector store**: Qdrant
- **LLM**: Claude via provider abstraction
- **Ingestion**: chunk → embed → upsert
""",
    "deployment.md": """# Deployment

1. Provision Qdrant Cloud or self-host
2. Set `ANTHROPIC_API_KEY`
3. Deploy API to Railway/Render
4. Run smoke tests on `/health` and `/query`
""",
    "Dockerfile": "FROM python:3.12-slim\nWORKDIR /app\nCOPY . .\nRUN pip install -r requirements.txt\nCMD uvicorn main:app --host 0.0.0.0 --port 8080\n",
}


async def seed_if_empty() -> None:
    async with SessionLocal() as db:
        existing = await db.execute(select(LearningPath).limit(1))
        if existing.scalar_one_or_none():
            return

        path = LearningPath(
            slug="ai-engineering-foundations",
            title="AI Engineering Foundations",
            description=(
                "Hands-on path for engineers shipping RAG systems, agents, and inference APIs."
            ),
            difficulty="beginner",
            order_index=0,
        )
        db.add(path)
        await db.flush()

        lesson = Lesson(
            path_id=path.id,
            slug="what-is-rag",
            title="What is RAG?",
            concept_markdown=(
                "Retrieval-Augmented Generation (RAG) grounds LLM answers in your data. "
                "You chunk documents, embed them, retrieve relevant passages, then prompt the model."
            ),
            architecture_mermaid=RAG_ARCHITECTURE,
            order_index=0,
        )
        db.add(lesson)

        project = Project(
            path_id=path.id,
            slug="rag-assistant",
            title="Build a RAG Assistant",
            summary=(
                "Ship a citation-aware Q&A API over your own documents using Qdrant and Claude."
            ),
            difficulty="intermediate",
            stack=["Python", "FastAPI", "Qdrant", "Claude"],
            rubric={
                "correctness": 25,
                "architecture": 25,
                "code_quality": 20,
                "performance": 15,
                "deployment_readiness": 15,
            },
            deployment_checklist=[
                "Environment variables documented",
                "Health check endpoint",
                "Qdrant collection created",
                "Sample query returns cited answer",
            ],
            scaffold_files=SCAFFOLD,
            order_index=0,
        )
        db.add(project)
        await db.flush()

        checkpoints = [
            (
                "Milestone 1 — Ingestion pipeline",
                "Build document chunking and embedding upload to Qdrant.",
                ["Create chunker", "Embed with chosen model", "Upsert to Qdrant"],
            ),
            (
                "Milestone 2 — Retrieval API",
                "Implement semantic search with metadata filters.",
                ["Query endpoint", "Top-k retrieval", "Return citations"],
            ),
            (
                "Milestone 3 — Grounded generation",
                "Wire Claude with retrieved context and streaming.",
                ["Prompt template", "SSE streaming", "Hallucination guardrails"],
            ),
            (
                "Milestone 4 — Evaluation & deploy",
                "Add basic evals and deploy to cloud.",
                ["Golden questions set", "Deploy checklist", "Smoke tests"],
            ),
        ]
        for i, (title, desc, tasks) in enumerate(checkpoints):
            db.add(
                Checkpoint(
                    project_id=project.id,
                    title=title,
                    description=desc,
                    tasks=tasks,
                    order_index=i,
                )
            )

        await db.commit()
