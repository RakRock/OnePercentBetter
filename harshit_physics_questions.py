"""Question bank loader for Harshit Physics practice."""

from __future__ import annotations

import json
import random
import re
from pathlib import Path

import harshit_physics_content as hpc
import harshit_physics_topics as hpt
from llm_question_format import is_quality_practice_question


def bank_path(unit_id: int) -> Path:
    return hpc.unit_dir(unit_id) / "question_bank.json"


def question_dedup_key(text: str, options: list[str] | None = None) -> str:
    t = str(text or "").strip().lower()
    t = re.sub(r"\s+", " ", t)
    t = t.rstrip(".?!").strip()
    if options:
        opts = "|".join(sorted(str(o).strip().lower() for o in options))
        t = f"{t}||{opts}"
    return t


def load_bank(unit_id: int | None = None) -> dict:
    uid = unit_id if unit_id is not None else hpc.active_unit_id()
    path = bank_path(uid)
    if not path.is_file():
        return {"questions": [], "questions_by_day": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return {"questions": [], "questions_by_day": {}}
    data.setdefault("questions", [])
    data.setdefault("questions_by_day", {})
    return data


def normalize_question(raw: dict, unit_id: int | None = None) -> dict:
    uid = unit_id if unit_id is not None else int(raw.get("unit_id", hpc.active_unit_id()))
    umeta = hpc.unit_meta(uid)
    options = [str(o) for o in raw.get("options", [])]
    answer = int(raw.get("answer", 0))
    if len(options) != 4 or answer not in range(4):
        raise ValueError("Question must have 4 options and answer index 0-3")
    if len({o.strip().lower() for o in options}) < 4:
        raise ValueError("Question must have 4 distinct options")

    day_id = int(raw.get("day_id", raw.get("topic", 1)))
    level = str(raw.get("level", "A"))
    prefix = f"u{uid}"
    qid = str(raw.get("id") or f"{prefix}_d{day_id}_{level}_{random.randint(1000, 9999)}")

    return {
        "id": qid,
        "question": str(raw.get("question", "")).strip(),
        "options": options,
        "answer": answer,
        "explanation": str(raw.get("explanation", "")).strip(),
        "day_id": day_id,
        "topic": day_id,
        "level": level,
        "unit_id": uid,
        "concept_id": raw.get("concept_id", ""),
        "category": raw.get("category") or f"{prefix}_d{day_id}_{level}",
        "category_label": raw.get("category_label")
        or hpt.format_topic_level_label(uid, day_id, level),
        "source": raw.get("source", "bank"),
        "chapter_ref": raw.get("chapter_ref", umeta.get("chapter_ref", "")),
    }


def pool_for(day_id: int, level: str, unit_id: int | None = None) -> list[dict]:
    uid = unit_id if unit_id is not None else hpc.active_unit_id()
    bank = load_bank(uid)
    by_day = bank.get("questions_by_day") or {}
    day_pool = list(by_day.get(str(day_id), []))
    if not day_pool:
        day_pool = [q for q in bank.get("questions", []) if int(q.get("day_id", 0)) == day_id]
    return [q for q in day_pool if str(q.get("level", "")) == level]


def pick_question(
    unit_id: int,
    day_id: int,
    level: str,
    *,
    exclude_ids: set[str] | None = None,
    exclude_text: set[str] | None = None,
) -> dict | None:
    exclude_ids = exclude_ids or set()
    exclude_text = exclude_text or set()
    candidates: list[dict] = []
    for raw in pool_for(day_id, level, unit_id):
        qid = str(raw.get("id") or "")
        if qid and qid in exclude_ids:
            continue
        key = question_dedup_key(str(raw.get("question", "")), raw.get("options"))
        if key in exclude_text:
            continue
        opts = raw.get("options") or []
        if not is_quality_practice_question(str(raw.get("question", "")), [str(o) for o in opts]):
            continue
        try:
            candidates.append(normalize_question(raw, unit_id))
        except ValueError:
            continue
    if not candidates:
        return None
    return random.choice(candidates)


def bank_stats(unit_id: int | None = None) -> dict:
    uid = unit_id if unit_id is not None else hpc.active_unit_id()
    bank = load_bank(uid)
    questions = bank.get("questions") or []
    by_level: dict[str, int] = {}
    by_day: dict[int, int] = {}
    for q in questions:
        lvl = str(q.get("level", "?"))
        by_level[lvl] = by_level.get(lvl, 0) + 1
        did = int(q.get("day_id", 0))
        by_day[did] = by_day.get(did, 0) + 1
    return {
        "total": len(questions),
        "by_level": by_level,
        "by_day": by_day,
        "days": len(by_day),
    }


def bank_status_message(unit_id: int | None = None) -> str:
    uid = unit_id if unit_id is not None else hpc.active_unit_id()
    stats = bank_stats(uid)
    if stats["total"]:
        return f"{stats['total']} questions in bank across {stats['days']} topic days."
    return f"Question bank empty — run scripts/build_physics_unit{uid}_question_bank.py"


def seed_examples(day_id: int, level: str, n: int = 3, unit_id: int | None = None) -> list[dict]:
    """Return up to n bank questions as Grok style seeds."""
    uid = unit_id if unit_id is not None else hpc.active_unit_id()
    pool = list(pool_for(day_id, level, uid))
    if not pool:
        for lvl in ("A", "B", "C"):
            pool.extend(pool_for(day_id, lvl, uid))
    if not pool:
        return []
    return random.sample(pool, min(n, len(pool)))


def add_questions(questions: list[dict], unit_id: int | None = None) -> int:
    """Append validated questions to the bank file (deduped)."""
    uid = unit_id if unit_id is not None else hpc.active_unit_id()
    path = bank_path(uid)
    bank = load_bank(uid)
    all_q = list(bank.get("questions") or [])
    by_day: dict[str, list] = {str(k): list(v) for k, v in (bank.get("questions_by_day") or {}).items()}
    existing_ids = {str(q.get("id")) for q in all_q if q.get("id")}
    existing_keys = {
        question_dedup_key(str(q.get("question", "")), q.get("options"))
        for q in all_q
        if isinstance(q, dict)
    }
    added = 0
    for raw in questions:
        if isinstance(raw, dict) and raw.get("id") and raw.get("question"):
            q = raw
        else:
            try:
                q = normalize_question(raw if isinstance(raw, dict) else {}, uid)
            except ValueError:
                continue
        key = question_dedup_key(q["question"], q["options"])
        if q["id"] in existing_ids or key in existing_keys:
            continue
        all_q.append(q)
        did = str(q["day_id"])
        by_day.setdefault(did, []).append(q)
        existing_ids.add(q["id"])
        existing_keys.add(key)
        added += 1
    bank["questions"] = all_q
    bank["questions_by_day"] = by_day
    bank.setdefault("meta", {})["total"] = len(all_q)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(bank, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return added
