"""Question banks for Harshit Class 10 unit practice."""

from __future__ import annotations

import json
import random
import uuid
from pathlib import Path

import harshit_class10_topics as h10t
import harshit_math_render as hmr
from llm_question_format import is_quality_practice_question

ROOT = Path(__file__).resolve().parent
BANK_DIR = ROOT / "HarshitMath" / "class10" / "question_banks"


def bank_path(unit_id: int, topic_id: int) -> Path:
    return BANK_DIR / f"unit_{unit_id:02d}" / f"topic_{topic_id:02d}.json"


def load_bank(unit_id: int, topic_id: int) -> dict:
    path = bank_path(unit_id, topic_id)
    if not path.is_file():
        return {"questions": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"questions": {}}
    if not isinstance(data, dict):
        return {"questions": {}}
    data.setdefault("questions", {})
    return data


def save_bank(unit_id: int, topic_id: int, bank: dict) -> Path:
    path = bank_path(unit_id, topic_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(bank, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def question_dedup_key(text: str, options: list[str] | None = None) -> str:
    import re

    t = str(text or "").strip().lower()
    t = re.sub(r"\s+", " ", t)
    t = t.rstrip(".?!").strip()
    if options:
        opts = "|".join(sorted(str(o).strip().lower() for o in options))
        t = f"{t}||{opts}"
    return t


def normalize_question(raw: dict, unit_id: int, topic_id: int, level: str) -> dict:
    options = [hmr.sanitize_grok_math_text(str(o)) for o in raw.get("options", [])]
    answer = int(raw.get("answer", 0))
    if len(options) != 4 or answer not in range(4):
        raise ValueError("Question must have 4 options and answer index 0-3")
    if len({o.strip().lower() for o in options}) < 4:
        raise ValueError("Question must have 4 distinct options")

    qid = str(raw.get("id") or f"u{unit_id}_t{topic_id}_{level}_{uuid.uuid4().hex[:8]}")
    out = {
        "id": qid,
        "question": hmr.normalize_unit_coefficients(
            hmr.sanitize_grok_math_text(str(raw.get("question", "")))
        ).strip(),
        "options": [hmr.normalize_unit_coefficients(o) for o in options],
        "answer": answer,
        "explanation": hmr.sanitize_grok_math_text(str(raw.get("explanation", ""))).strip(),
        "topic": topic_id,
        "level": level,
        "unit_id": unit_id,
        "category": f"u{unit_id}_t{topic_id}_{level}",
        "category_label": h10t.format_topic_level_label(unit_id, topic_id, level),
        "source": raw.get("source", "template"),
        "chapter_ref": raw.get("chapter_ref", ""),
    }
    if raw.get("valid_answers"):
        out["valid_answers"] = [str(v) for v in raw["valid_answers"]]
    return out


def add_questions(unit_id: int, topic_id: int, level: str, questions: list[dict]) -> int:
    bank = load_bank(unit_id, topic_id)
    bank.setdefault("meta", {"unit_id": unit_id, "topic_id": topic_id})
    bucket = bank.setdefault("questions", {}).setdefault(level, [])
    existing_ids = {q.get("id") for q in bucket if isinstance(q, dict)}
    existing_keys = {
        question_dedup_key(str(q.get("question", "")), q.get("options"))
        for q in bucket
        if isinstance(q, dict)
    }
    added = 0
    for raw in questions:
        q = normalize_question(raw, unit_id, topic_id, level)
        key = question_dedup_key(str(q.get("question", "")), q.get("options"))
        if q["id"] in existing_ids or key in existing_keys:
            continue
        bucket.append(q)
        existing_ids.add(q["id"])
        existing_keys.add(key)
        added += 1
    save_bank(unit_id, topic_id, bank)
    return added


def pick_question(
    unit_id: int,
    topic_id: int,
    level: str,
    *,
    exclude_ids: set[str] | None = None,
    exclude_text: set[str] | None = None,
) -> dict | None:
    bank = load_bank(unit_id, topic_id)
    pool = list(bank.get("questions", {}).get(level, []))
    if not pool:
        return None
    exclude_ids = exclude_ids or set()
    exclude_text = exclude_text or set()
    candidates = []
    for q in pool:
        qid = str(q.get("id") or "")
        if qid and qid in exclude_ids:
            continue
        key = question_dedup_key(str(q.get("question", "")), q.get("options"))
        if key in exclude_text:
            continue
        opts = q.get("options") or []
        if is_quality_practice_question(str(q.get("question", "")), [str(o) for o in opts]):
            candidates.append(q)
    if not candidates:
        candidates = [q for q in pool if str(q.get("id") or "") not in exclude_ids]
    if not candidates:
        return None
    raw = random.choice(candidates)
    try:
        return normalize_question(raw, unit_id, topic_id, level)
    except (ValueError, TypeError, KeyError):
        return None


def clear_unit_bank(unit_id: int) -> int:
    """Remove all bank JSON files for a unit. Returns number of files deleted."""
    folder = BANK_DIR / f"unit_{unit_id:02d}"
    if not folder.is_dir():
        return 0
    removed = 0
    for path in folder.glob("topic_*.json"):
        path.unlink(missing_ok=True)
        removed += 1
    return removed


def bank_stats(unit_id: int) -> dict:
    topics = h10t.topics_for_unit(unit_id)
    total = 0
    by_topic: dict[int, int] = {}
    for tid in topics:
        bank = load_bank(unit_id, tid)
        count = sum(len(v) for v in bank.get("questions", {}).values() if isinstance(v, list))
        by_topic[tid] = count
        total += count
    return {"total": total, "by_topic": by_topic}


def bank_status_message(unit_id: int) -> str:
    stats = bank_stats(unit_id)
    if stats["total"]:
        return f"Question bank: {stats['total']} practice question(s) for this unit."
    return "Question bank: empty — using live templates for this session."
