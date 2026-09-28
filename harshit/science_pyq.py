"""Mix Class 10 science previous-year questions into daily practice."""

from __future__ import annotations

import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_DIRS = {
    "chemistry": ROOT / "HarshitChemistry" / "pyq_seeds",
    "physics": ROOT / "HarshitPhysics" / "pyq_seeds",
    "biology": ROOT / "HarshitBiology" / "pyq_seeds",
}
_CACHE: dict[tuple[str, int], dict] = {}

PYQ_PER_SESSION = 4


def _path(subject: str, unit_id: int) -> Path:
    return _DIRS[subject] / f"unit_{unit_id:02d}.json"


def load_seeds(subject: str, unit_id: int) -> dict:
    key = (subject, unit_id)
    if key in _CACHE:
        return _CACHE[key]
    path = _path(subject, unit_id)
    if not path.is_file():
        data = {"meta": {}, "mcq": [], "short_answer": []}
    else:
        data = json.loads(path.read_text(encoding="utf-8"))
        data.setdefault("mcq", [])
        data.setdefault("short_answer", [])
    _CACHE[key] = data
    return data


def seeds_available(subject: str, unit_id: int) -> bool:
    data = load_seeds(subject, unit_id)
    return bool(data.get("mcq") or data.get("short_answer"))


def _wrap_mcq(raw: dict) -> dict:
    return {
        "id": raw["id"],
        "type": "mcq",
        "question": raw["question"],
        "options": list(raw["options"]),
        "answer": int(raw.get("answer", 0)),
        "explanation": raw.get("explanation", ""),
        "category": "board_pyq",
        "category_label": "Board PYQ (MCQ)",
        "level": "C",
        "day_id": 1,
        "topic": 1,
        "source": "board_pyq",
        "source_paper": raw.get("source_paper", ""),
        "marks": 1,
    }


def _wrap_short(raw: dict) -> dict:
    marks = int(raw.get("marks") or 1)
    model = str(raw.get("model_answer") or "").strip()
    return {
        "id": raw["id"],
        "type": "short_answer",
        "question": raw["question"],
        "model_answer": model,
        "explanation": model,
        "options": [],
        "answer": 0,
        "category": "board_pyq",
        "category_label": f"Board PYQ ({marks} mark{'s' if marks != 1 else ''})",
        "level": "C" if marks <= 2 else "D",
        "day_id": 1,
        "topic": 1,
        "source": "board_pyq",
        "source_paper": raw.get("source_paper", ""),
        "marks": marks,
    }


def pick_pyq_questions(subject: str, unit_id: int, count: int, *, used_ids: set[str]) -> list[dict]:
    if count <= 0 or not seeds_available(subject, unit_id):
        return []
    data = load_seeds(subject, unit_id)
    mcq_pool = [q for q in data.get("mcq", []) if q.get("id") not in used_ids]
    short_pool = [q for q in data.get("short_answer", []) if q.get("id") not in used_ids]
    random.shuffle(mcq_pool)
    random.shuffle(short_pool)
    picked: list[dict] = []
    # Prefer a mix: half previous-year MCQs when they exist, the rest short answers.
    mcq_slots = min(len(mcq_pool), max(1, count // 2)) if mcq_pool else 0
    if not short_pool:
        mcq_slots = min(len(mcq_pool), count)
    for raw in mcq_pool[:mcq_slots]:
        used_ids.add(str(raw["id"]))
        picked.append(_wrap_mcq(raw))
    for raw in short_pool:
        if len(picked) >= count:
            break
        used_ids.add(str(raw["id"]))
        picked.append(_wrap_short(raw))
    random.shuffle(picked)
    return picked[:count]


def inject_pyq_into_session(
    subject: str,
    unit_id: int,
    questions: list[dict],
    *,
    used_ids: set[str],
    session_count: int,
    config: dict | None = None,
) -> list[dict]:
    config = config or {}
    if not config.get("include_board_pyq", True):
        return questions
    if not questions or not seeds_available(subject, unit_id):
        return questions
    pyq_count = int(config.get("pyq_count", PYQ_PER_SESSION))
    pyq_count = max(0, min(session_count, pyq_count))
    pyq_items = pick_pyq_questions(subject, unit_id, pyq_count, used_ids=used_ids)
    if not pyq_items:
        return questions
    keep = max(0, len(questions) - len(pyq_items))
    merged = questions[:keep] + pyq_items
    random.shuffle(merged)
    return merged[:session_count]
