"""Mix board previous-year questions into daily Class 10 practice sessions."""

from __future__ import annotations

import random
from typing import Any

import harshit_class10_board_seeds as h10bs
import harshit_class10_unit_test as h10ut

WRITTEN_BUCKETS = ("vsa", "sa", "la")


def pyq_defaults() -> dict[str, Any]:
    return {
        "include_board_pyq": True,
        "pyq_count": 4,
        "pyq_written_slots": 2,
    }


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
        "topic": 0,
        "source": "board_pyq",
        "source_paper": raw.get("source_paper", ""),
        "marks": 1,
        "needs_answer_key": bool((raw.get("pyq_meta") or {}).get("needs_answer_key")),
    }


def _wrap_ar(raw: dict) -> dict:
    wrapped = h10ut._wrap_ar(raw, q_num=0)
    wrapped["category"] = "board_pyq"
    wrapped["category_label"] = "Board PYQ (Assertion–Reason)"
    wrapped["level"] = "C"
    wrapped["topic"] = 0
    wrapped["source"] = "board_pyq"
    return wrapped


def _wrap_written(raw: dict, bucket: str) -> dict:
    default_marks = {"vsa": 2, "sa": 3, "la": 5}.get(bucket, 3)
    section = {"vsa": "B", "sa": "C", "la": "D"}[bucket]
    wrapped = h10ut._wrap_written(raw, q_num=0, section=section, default_marks=default_marks)
    wrapped["category"] = "board_pyq"
    wrapped["category_label"] = f"Board PYQ ({int(wrapped.get('marks', 2))} marks)"
    wrapped["level"] = "D" if bucket == "la" else "C"
    wrapped["topic"] = 0
    wrapped["source"] = "board_pyq"
    wrapped["self_check"] = True
    return wrapped


def pick_pyq_questions(
    unit_id: int,
    count: int,
    *,
    written_slots: int,
    used_ids: set[str],
) -> list[dict]:
    if count <= 0 or not h10bs.seeds_available(unit_id):
        return []

    written_slots = max(0, min(count, written_slots))
    mcq_slots = count - written_slots
    # Reserve at least one AR when we have 2+ MCQ slots and seeds exist.
    ar_slot = 0
    seeds = h10bs.load_unit_seeds(unit_id)
    if mcq_slots >= 2 and seeds.get("assertion_reason"):
        ar_slot = 1
        mcq_slots -= 1

    picked: list[dict] = []

    for _ in range(ar_slot):
        raw = h10bs.pick_ar_seed(unit_id, exclude_ids=used_ids)
        if not raw:
            mcq_slots += 1
            continue
        used_ids.add(str(raw["id"]))
        picked.append(_wrap_ar(raw))

    for _ in range(mcq_slots):
        raw = h10bs.pick_mcq_seed(unit_id, exclude_ids=used_ids)
        if not raw:
            continue
        used_ids.add(str(raw["id"]))
        picked.append(_wrap_mcq(raw))

    buckets = list(WRITTEN_BUCKETS)
    random.shuffle(buckets)
    for _ in range(written_slots):
        bucket = buckets[_ % len(buckets)]
        raw = h10bs.pick_written_seed(unit_id, bucket, exclude_ids=used_ids)
        if not raw:
            for alt in WRITTEN_BUCKETS:
                raw = h10bs.pick_written_seed(unit_id, alt, exclude_ids=used_ids)
                if raw:
                    bucket = alt
                    break
        if not raw:
            continue
        used_ids.add(str(raw["id"]))
        picked.append(_wrap_written(raw, bucket))

    random.shuffle(picked)
    return picked


def inject_pyq_into_session(
    unit_id: int,
    questions: list[dict],
    config: dict,
    *,
    used_ids: set[str],
    session_count: int,
) -> list[dict]:
    if not config.get("include_board_pyq", True):
        return questions
    if not h10bs.seeds_available(unit_id):
        return questions

    defaults = pyq_defaults()
    pyq_count = int(config.get("pyq_count", defaults["pyq_count"]))
    pyq_count = max(0, min(session_count, pyq_count))
    written_slots = int(config.get("pyq_written_slots", defaults["pyq_written_slots"]))
    pyq_items = pick_pyq_questions(
        unit_id,
        pyq_count,
        written_slots=written_slots,
        used_ids=used_ids,
    )
    if not pyq_items:
        return questions

    # Replace tail of bank questions so session size stays fixed.
    keep = max(0, len(questions) - len(pyq_items))
    merged = questions[:keep] + pyq_items
    random.shuffle(merged)
    return merged[:session_count]
