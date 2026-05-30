"""AI Forge — learning content and Claude mentor (runs inside Streamlit)."""

from __future__ import annotations

import os

try:
    import truststore

    truststore.inject_into_ssl()
except ImportError:
    pass

import httpx

PERSONALITIES = ["teacher", "architect", "debugger", "interviewer", "reviewer"]

PERSONALITY_PROMPTS = {
    "teacher": (
        "You are a patient AI engineering teacher. Use questions and hints. "
        "Never dump full solutions immediately."
    ),
    "architect": (
        "You are a senior AI architect. Focus on trade-offs, boundaries, and production readiness."
    ),
    "debugger": (
        "You are a debugging mentor. Ask for logs, reproduce steps, and isolate root causes."
    ),
    "interviewer": (
        "You are a technical interviewer. Probe depth with follow-up questions."
    ),
    "reviewer": (
        "You are a code reviewer. Point out risks, missing tests, and clarity issues."
    ),
}

BASE_RULES = """
Rules:
- Guide with questions before giving answers.
- Prefer incremental hints over full code dumps.
- When code is needed, show the smallest snippet that unblocks the learner.
- Tie advice to production AI systems (latency, cost, evals, observability).
"""

CLAUDE_MODEL = os.environ.get("AI_FORGE_MODEL", "claude-sonnet-4-20250514")

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

PROJECTS = [
    {
        "slug": "rag-assistant",
        "title": "Build a RAG Assistant",
        "summary": (
            "Ship a citation-aware Q&A API over your own documents using Qdrant and Claude."
        ),
        "difficulty": "intermediate",
        "stack": ["Python", "FastAPI", "Qdrant", "Claude"],
        "deployment_checklist": [
            "Environment variables documented",
            "Health check endpoint",
            "Qdrant collection created",
            "Sample query returns cited answer",
        ],
        "concept": (
            "Retrieval-Augmented Generation (RAG) grounds LLM answers in your data. "
            "You chunk documents, embed them, retrieve relevant passages, then prompt the model."
        ),
        "architecture_mermaid": RAG_ARCHITECTURE,
        "checkpoints": [
            {
                "title": "Milestone 1 — Ingestion pipeline",
                "description": "Build document chunking and embedding upload to Qdrant.",
                "tasks": ["Create chunker", "Embed with chosen model", "Upsert to Qdrant"],
            },
            {
                "title": "Milestone 2 — Retrieval API",
                "description": "Implement semantic search with metadata filters.",
                "tasks": ["Query endpoint", "Top-k retrieval", "Return citations"],
            },
            {
                "title": "Milestone 3 — Grounded generation",
                "description": "Wire Claude with retrieved context and streaming.",
                "tasks": ["Prompt template", "SSE streaming", "Hallucination guardrails"],
            },
            {
                "title": "Milestone 4 — Evaluation & deploy",
                "description": "Add basic evals and deploy to cloud.",
                "tasks": ["Golden questions set", "Deploy checklist", "Smoke tests"],
            },
        ],
        "scaffold": {
            "README.md": (
                "# RAG Assistant Starter\n\n"
                "Production-style retrieval-augmented generation assistant.\n"
            ),
            "architecture.md": (
                "# Architecture\n\n"
                "- **API**: FastAPI\n"
                "- **Vector store**: Qdrant\n"
                "- **LLM**: Claude\n"
            ),
        },
    },
]


def get_project(slug: str) -> dict | None:
    for p in PROJECTS:
        if p["slug"] == slug:
            return p
    return None


def demo_mentor_reply(message: str, personality: str) -> str:
    snippet = message[:120] + ("…" if len(message) > 120 else "")
    return (
        f"**Demo mode** — add `ANTHROPIC_API_KEY` in Streamlit secrets for live Claude replies.\n\n"
        f"*{personality.title()} mentor* — you asked about: _{snippet}_\n\n"
        "Try this next:\n"
        "1. What is the smallest piece you can verify works today?\n"
        "2. What error or output do you see right now?\n"
        "3. What would a one-line test prove success?\n\n"
        "Reply with your answers and I'll give the next hint."
    )


def mentor_chat(
    api_key: str | None,
    message: str,
    *,
    personality: str = "teacher",
    history: list[dict] | None = None,
    project: dict | None = None,
    user_name: str = "Learner",
) -> str:
    """Socratic mentor reply via Claude Messages API."""
    if not api_key:
        return demo_mentor_reply(message, personality)

    system = (
        f"{PERSONALITY_PROMPTS.get(personality, PERSONALITY_PROMPTS['teacher'])}\n"
        f"{BASE_RULES}\n"
        f"The learner's name is {user_name}."
    )
    if project:
        system += (
            f"\n\nActive project: {project['title']}\n"
            f"{project['summary']}\n"
            f"Stack: {', '.join(project['stack'])}"
        )

    messages = []
    for turn in (history or [])[-12:]:
        role = turn.get("role", "user")
        if role in ("user", "assistant"):
            messages.append({"role": role, "content": turn["content"]})
    messages.append({"role": "user", "content": message})

    try:
        resp = httpx.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": CLAUDE_MODEL,
                "max_tokens": 1024,
                "system": system,
                "messages": messages,
            },
            timeout=90.0,
        )
        resp.raise_for_status()
        data = resp.json()
        blocks = data.get("content", [])
        parts = [b.get("text", "") for b in blocks if b.get("type") == "text"]
        return "".join(parts).strip() or "I couldn't generate a reply. Try rephrasing your question."
    except httpx.HTTPStatusError as exc:
        return f"Mentor API error ({exc.response.status_code}). Check your API key and try again."
    except Exception as exc:
        return f"Mentor unavailable: {exc}"
