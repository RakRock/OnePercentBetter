"""Persist AI-generated Spanish practice questions."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BANK_PATH = ROOT / "ArjunSpanish" / "ai_questions.json"


def _load_raw() -> list[dict]:
    if not BANK_PATH.is_file():
        return []
    try:
        data = json.loads(BANK_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    return data if isinstance(data, list) else []


def load_ai_bank() -> list[dict]:
    return [q for q in _load_raw() if isinstance(q, dict) and q.get("question")]


def add_questions(questions: list[dict]) -> int:
    if not questions:
        return 0
    BANK_PATH.parent.mkdir(parents=True, exist_ok=True)
    existing = load_ai_bank()
    seen = {str(q.get("question", "")).strip().lower() for q in existing}
    added = 0
    for q in questions:
        stem = str(q.get("question", "")).strip().lower()
        if not stem or stem in seen:
            continue
        seen.add(stem)
        existing.append(q)
        added += 1
    BANK_PATH.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    return added


def pick_ai_question(
    topic_id: str,
    *,
    used_ids: set[str],
    seen_fps: set[str],
) -> dict | None:
    from practice_quality.dedup import fingerprints_for_question, is_duplicate_of_any

    for q in load_ai_bank():
        if q.get("category") != topic_id:
            continue
        if str(q.get("id", "")) in used_ids:
            continue
        if is_duplicate_of_any(q, seen_fps):
            continue
        return dict(q)
    return None
