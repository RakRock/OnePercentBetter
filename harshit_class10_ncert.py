"""NCERT exercise practice for Class 10. Questions are stored per unit."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NCERT_DIR = ROOT / "HarshitMath" / "class10" / "ncert"

_CACHE: dict[int, list[dict]] = {}
_LEVEL = {1: "A", 2: "B", 3: "C", 5: "D"}


def _path(unit_id: int) -> Path:
    return NCERT_DIR / f"unit_{unit_id:02d}.json"


def load_questions(unit_id: int) -> list[dict]:
    if unit_id in _CACHE:
        return _CACHE[unit_id]
    path = _path(unit_id)
    if not path.is_file():
        _CACHE[unit_id] = []
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    questions = [q for q in data.get("questions", []) if q.get("question")]
    _CACHE[unit_id] = questions
    return questions


def ncert_available(unit_id: int) -> bool:
    return bool(load_questions(unit_id))


def mark_counts(unit_id: int) -> dict[int, int]:
    counts: dict[int, int] = {}
    for question in load_questions(unit_id):
        marks = int(question.get("marks") or 1)
        counts[marks] = counts.get(marks, 0) + 1
    return counts


def pattern_summary(unit_id: int) -> str:
    counts = mark_counts(unit_id)
    if not counts:
        return ""
    return ", ".join(f"{counts[marks]} × {marks} mark" for marks in sorted(counts))


def _wrap(raw: dict, q_num: int) -> dict:
    marks = int(raw.get("marks") or 1)
    wrapped = {
        "id": raw["id"],
        "q_num": q_num,
        "type": raw.get("type") or "mcq",
        "question": raw["question"],
        "marks": marks,
        "category": "ncert",
        "category_label": f"NCERT ({marks} mark{'s' if marks != 1 else ''})",
        "level": _LEVEL.get(marks, "C"),
        "topic": 0,
        "source": "ncert",
        "explanation": raw.get("explanation", ""),
    }
    if wrapped["type"] == "mcq":
        wrapped["options"] = list(raw.get("options") or [])
        wrapped["answer"] = int(raw.get("answer", 0))
    else:
        wrapped["type"] = "written"
        wrapped["model_answer"] = raw.get("model_answer", "")
        wrapped["self_check"] = True
    if raw.get("figure"):
        wrapped["figure"] = raw["figure"]
    return wrapped


def build_session(unit_id: int) -> list[dict]:
    """The chapter set, in mark order, so the same paper can be practiced again."""
    raw_questions = load_questions(unit_id)
    ordered = sorted(enumerate(raw_questions), key=lambda item: (int(item[1].get("marks") or 1), item[0]))
    return [_wrap(raw, index + 1) for index, (_, raw) in enumerate(ordered)]
