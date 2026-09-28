"""Mix board previous-year questions into daily Class 10 practice sessions."""

from __future__ import annotations

import random
from typing import Any

import harshit_class10_board_seeds as h10bs
import harshit_class10_unit_test as h10ut

WRITTEN_BUCKETS = ("vsa", "sa", "la")

# Daily practice: 5 × 1 mark, 4 × (2 or 3 mark), 1 × 5 mark.
SESSION_SIZE = 10
ONE_MARK_SLOTS = 5
MID_MARK_SLOTS = 4
FIVE_MARK_SLOTS = 1


def pyq_defaults() -> dict[str, Any]:
    return {
        "include_board_pyq": True,
        "pyq_count": SESSION_SIZE,
        "pyq_written_slots": MID_MARK_SLOTS + FIVE_MARK_SLOTS,
    }


def two_three_split(unit_id: int) -> tuple[int, int]:
    """Split the four middle slots using this unit's 2-mark vs 3-mark PYQ counts."""
    seeds = h10bs.load_unit_seeds(unit_id)
    two = len(seeds.get("vsa") or [])
    three = len(seeds.get("sa") or [])
    if two + three == 0:
        return 2, 2
    n_two = int(round(MID_MARK_SLOTS * two / (two + three)))
    n_two = max(0, min(MID_MARK_SLOTS, n_two))
    return n_two, MID_MARK_SLOTS - n_two


def pattern_summary(unit_id: int) -> str:
    n_two, n_three = two_three_split(unit_id)
    return (
        f"{ONE_MARK_SLOTS} × 1 mark, {n_two} × 2 mark, "
        f"{n_three} × 3 mark, {FIVE_MARK_SLOTS} × 5 mark"
    )


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


def _take(unit_id: int, bucket: str, used_ids: set[str], *, marks: int | None = None) -> dict | None:
    pool = [
        q
        for q in h10bs.load_unit_seeds(unit_id).get(bucket, [])
        if q.get("id") not in used_ids and (marks is None or int(q.get("marks", marks)) == marks)
    ]
    if not pool and marks is not None:
        pool = [q for q in h10bs.load_unit_seeds(unit_id).get(bucket, []) if q.get("id") not in used_ids]
    if not pool:
        return None
    raw = random.choice(pool)
    used_ids.add(str(raw["id"]))
    return raw


def _label_marks(question: dict, marks: int) -> dict:
    question["marks"] = marks
    question["category_label"] = f"Board PYQ ({marks} mark{'s' if marks != 1 else ''})"
    return question


def build_mark_pattern_session(unit_id: int, *, used_ids: set[str]) -> list[dict]:
    """10 previous-year questions: five 1-mark, four 2/3-mark, one 5-mark."""
    if not h10bs.seeds_available(unit_id):
        return []

    n_two, n_three = two_three_split(unit_id)
    one_mark: list[dict] = []
    seeds = h10bs.load_unit_seeds(unit_id)
    if seeds.get("assertion_reason"):
        raw = _take(unit_id, "assertion_reason", used_ids)
        if raw:
            one_mark.append(_label_marks(_wrap_ar(raw), 1))

    while len(one_mark) < ONE_MARK_SLOTS:
        raw = _take(unit_id, "mcq", used_ids)
        if not raw:
            break
        one_mark.append(_label_marks(_wrap_mcq(raw), 1))

    two_mark: list[dict] = []
    for _ in range(n_two):
        raw = _take(unit_id, "vsa", used_ids, marks=2)
        if not raw:
            break
        two_mark.append(_label_marks(_wrap_written(raw, "vsa"), 2))

    three_mark: list[dict] = []
    for _ in range(n_three):
        raw = _take(unit_id, "sa", used_ids, marks=3)
        if not raw:
            break
        three_mark.append(_label_marks(_wrap_written(raw, "sa"), 3))

    five_mark: list[dict] = []
    raw = _take(unit_id, "la", used_ids, marks=5)
    if raw:
        five_mark.append(_label_marks(_wrap_written(raw, "la"), 5))

    for group in (one_mark, two_mark, three_mark):
        random.shuffle(group)
    return one_mark + two_mark + three_mark + five_mark


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
