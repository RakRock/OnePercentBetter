"""Persist AI-generated Arjun Course 3 concept-check questions."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONCEPT_CHECK_DIR = ROOT / "ArjunCourse3" / "concept_checks"


def _unit_path(unit_id: int) -> Path:
    CONCEPT_CHECK_DIR.mkdir(parents=True, exist_ok=True)
    return CONCEPT_CHECK_DIR / f"unit_{unit_id}.json"


def question_dedup_key(question: str, options: list | None) -> str:
    text = re.sub(r"\s+", " ", str(question or "").strip().lower())
    opts = "|".join(str(o).strip().lower() for o in (options or []))
    return f"{text}::{opts}"


def load_ai_bank(unit_id: int) -> list[dict]:
    path = _unit_path(unit_id)
    if not path.is_file():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    if not isinstance(data, list):
        return []
    out: list[dict] = []
    for item in data:
        if not isinstance(item, dict):
            continue
        q = dict(item)
        q.setdefault("source", "concept_check")
        q.setdefault("origin", "llm")
        out.append(q)
    return out


def add_questions(unit_id: int, questions: list[dict]) -> int:
    """Append unique concept-check questions to the unit JSON bank."""
    existing = load_ai_bank(unit_id)
    seen = {question_dedup_key(q.get("question", ""), q.get("options")) for q in existing}
    seen_ids = {str(q.get("id", "")) for q in existing}
    added: list[dict] = []
    for q in questions:
        if not isinstance(q, dict):
            continue
        key = question_dedup_key(q.get("question", ""), q.get("options"))
        qid = str(q.get("id", ""))
        if key in seen or (qid and qid in seen_ids):
            continue
        item = dict(q)
        item["source"] = "concept_check"
        item.setdefault("origin", "llm")
        added.append(item)
        seen.add(key)
        if qid:
            seen_ids.add(qid)
    if not added:
        return 0
    merged = existing + added
    _unit_path(unit_id).write_text(json.dumps(merged, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return len(added)


def count_by_category(unit_id: int) -> dict[str, int]:
    counts: dict[str, int] = {}
    for q in load_ai_bank(unit_id):
        cat = str(q.get("category", ""))
        counts[cat] = counts.get(cat, 0) + 1
    return counts
