#!/usr/bin/env python3
"""Build Harshit Biology question bank (200 MCQs from concept cards) for units 1–4."""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import harshit.biology.content as hpc  # noqa: E402
import harshit.biology.topics as hpt  # noqa: E402

TARGET_TOTAL = 200


def _distractors(concepts: list[dict], skip_id: str, field: str, n: int = 3) -> list[str]:
    pool = []
    for c in concepts:
        if c["id"] == skip_id:
            continue
        val = str(c.get(field) or "").strip()
        if val and len(val) > 8:
            pool.append(val.split(".")[0].strip() + ".")
    random.shuffle(pool)
    out: list[str] = []
    for p in pool:
        if p not in out:
            out.append(p)
        if len(out) >= n:
            break
    while len(out) < n:
        out.append("This statement is not correct for this topic.")
    return out[:n]


def _shuffle_options(correct: str, wrong: list[str]) -> tuple[list[str], int]:
    opts = [correct] + wrong[:3]
    while len(opts) < 4:
        opts.append(f"None of the above ({len(opts)})")
    random.shuffle(opts)
    return opts, opts.index(correct)


def _chapter_ref(unit_id: int) -> str:
    return hpc.unit_meta(unit_id)["chapter_ref"]


def _q_recall(concept: dict, day_id: int, concepts: list[dict], level: str, seq: int, unit_id: int) -> dict:
    name = concept["name"]
    correct = str(concept.get("simple_answer", "")).split(".")[0].strip() + "."
    wrong = _distractors(concepts, concept["id"], "simple_answer")
    options, answer = _shuffle_options(correct, wrong)
    prefix = f"u{unit_id}"
    return {
        "id": f"{prefix}_d{day_id}_{level.lower()}_{seq:03d}",
        "question": f"Which statement best describes **{name}**?",
        "options": options,
        "answer": answer,
        "explanation": concept.get("remember") or concept.get("simple_answer", ""),
        "day_id": day_id,
        "concept_id": concept["id"],
        "level": level,
        "category": f"{prefix}_d{day_id}_{level}",
        "category_label": hpt.format_topic_level_label(unit_id, day_id, level),
        "source": "bank",
        "chapter_ref": _chapter_ref(unit_id),
    }


def _q_remember(concept: dict, day_id: int, concepts: list[dict], level: str, seq: int, unit_id: int) -> dict:
    remember = str(concept.get("remember") or concept.get("simple_answer", "")).strip()
    if not remember:
        return _q_recall(concept, day_id, concepts, level, seq, unit_id)
    correct = remember.split(".")[0].strip() + ("." if "." not in remember[:80] else "")
    wrong = _distractors(concepts, concept["id"], "remember") or _distractors(concepts, concept["id"], "simple_answer")
    options, answer = _shuffle_options(correct, wrong)
    prefix = f"u{unit_id}"
    return {
        "id": f"{prefix}_d{day_id}_{level.lower()}_{seq:03d}",
        "question": f"What is the key takeaway about **{concept['name']}**?",
        "options": options,
        "answer": answer,
        "explanation": remember,
        "day_id": day_id,
        "concept_id": concept["id"],
        "level": level,
        "category": f"{prefix}_d{day_id}_{level}",
        "category_label": hpt.format_topic_level_label(unit_id, day_id, level),
        "source": "bank",
        "chapter_ref": _chapter_ref(unit_id),
    }


def _q_confusion(concept: dict, day_id: int, concepts: list[dict], level: str, seq: int, unit_id: int) -> dict:
    confusion = str(concept.get("common_confusion") or "").strip()
    if not confusion:
        return _q_apply(concept, day_id, concepts, level, seq, unit_id)
    correct = f"Avoid thinking: {confusion.split('.')[0].strip()}."
    wrong = [
        confusion,
        "There are no common mistakes for this topic.",
        "Any answer is acceptable in exams.",
    ]
    options, answer = _shuffle_options(correct, wrong)
    prefix = f"u{unit_id}"
    return {
        "id": f"{prefix}_d{day_id}_{level.lower()}_{seq:03d}",
        "question": f"Which advice helps you avoid mistakes about **{concept['name']}**?",
        "options": options,
        "answer": answer,
        "explanation": confusion,
        "day_id": day_id,
        "concept_id": concept["id"],
        "level": level,
        "category": f"{prefix}_d{day_id}_{level}",
        "category_label": hpt.format_topic_level_label(unit_id, day_id, level),
        "source": "bank",
        "chapter_ref": _chapter_ref(unit_id),
    }


def _q_apply(concept: dict, day_id: int, concepts: list[dict], level: str, seq: int, unit_id: int) -> dict:
    example = str(concept.get("example") or concept.get("why") or concept.get("simple_answer", "")).strip()
    correct = example.split(".")[0].strip() + "."
    wrong = _distractors(concepts, concept["id"], "example") or _distractors(concepts, concept["id"], "why")
    options, answer = _shuffle_options(correct, wrong)
    prefix = f"u{unit_id}"
    return {
        "id": f"{prefix}_d{day_id}_{level.lower()}_{seq:03d}",
        "question": f"Which example or application fits **{concept['name']}**?",
        "options": options,
        "answer": answer,
        "explanation": example,
        "day_id": day_id,
        "concept_id": concept["id"],
        "level": level,
        "category": f"{prefix}_d{day_id}_{level}",
        "category_label": hpt.format_topic_level_label(unit_id, day_id, level),
        "source": "bank",
        "chapter_ref": _chapter_ref(unit_id),
    }


def _q_name_pick(concept: dict, day_id: int, concepts: list[dict], level: str, seq: int, unit_id: int) -> dict:
    definition = str(concept.get("simple_answer", "")).split(".")[0].strip()
    correct = concept["name"]
    others = [c["name"] for c in concepts if c["id"] != concept["id"]]
    random.shuffle(others)
    wrong = others[:3]
    while len(wrong) < 3:
        wrong.append(f"Topic {len(wrong) + 1}")
    options, answer = _shuffle_options(correct, wrong)
    prefix = f"u{unit_id}"
    return {
        "id": f"{prefix}_d{day_id}_{level.lower()}_{seq:03d}",
        "question": f"Which term matches this description? \"{definition}.\"",
        "options": options,
        "answer": answer,
        "explanation": f"This describes {concept['name']}: {concept.get('simple_answer', '')}",
        "day_id": day_id,
        "concept_id": concept["id"],
        "level": level,
        "category": f"{prefix}_d{day_id}_{level}",
        "category_label": hpt.format_topic_level_label(unit_id, day_id, level),
        "source": "bank",
        "chapter_ref": _chapter_ref(unit_id),
    }


GENERATORS = {
    "A": [_q_recall, _q_name_pick, _q_remember],
    "B": [_q_apply, _q_remember, _q_recall],
    "C": [_q_confusion, _q_apply, _q_remember],
}


def _questions_for_day(unit_id: int, day_id: int, count: int) -> list[dict]:
    concepts = hpc.concepts_for_day(day_id, unit_id=unit_id)
    if not concepts:
        return []
    out: list[dict] = []
    seq = 1
    levels_cycle = ["A", "B", "C"]
    ci = 0
    gi = 0
    while len(out) < count:
        concept = concepts[ci % len(concepts)]
        level = levels_cycle[len(out) % 3]
        gens = GENERATORS[level]
        gen = gens[gi % len(gens)]
        q = gen(concept, day_id, concepts, level, seq, unit_id)
        out.append(q)
        seq += 1
        ci += 1
        gi += 1
    return out


def build_bank(unit_id: int, *, seed: int = 42) -> dict:
    random.seed(seed)
    days = [d for d in hpc.list_days(stage=1, unit_id=unit_id) if d.get("active")]
    n_days = len(days) or 1
    base = TARGET_TOTAL // n_days
    extra = TARGET_TOTAL % n_days

    all_q: list[dict] = []
    by_day: dict[str, list[dict]] = {}
    for i, day in enumerate(sorted(days, key=lambda d: d["day"])):
        did = int(day["day"])
        count = base + (1 if i < extra else 0)
        day_qs = _questions_for_day(unit_id, did, count)
        by_day[str(did)] = day_qs
        all_q.extend(day_qs)

    prefix = f"u{unit_id}"
    seen: set[str] = set()
    unique: list[dict] = []
    for q in all_q:
        key = q["question"].strip().lower()
        if key in seen:
            q["id"] = f"{prefix}_{uuid.uuid4().hex[:8]}"
            key = q["question"].strip().lower() + q["id"]
        seen.add(key)
        unique.append(q)

    umeta = hpc.unit_meta(unit_id)
    return {
        "meta": {
            "unit_id": unit_id,
            "total": len(unique),
            "target": TARGET_TOTAL,
            "ncert": umeta["ncert"],
            "levels": list(hpt.LEVELS.keys()),
        },
        "questions_by_day": by_day,
        "questions": unique,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Harshit Biology question bank")
    parser.add_argument("--unit", type=int, required=True, choices=[1, 2, 3, 4])
    args = parser.parse_args()

    bank = build_bank(args.unit)
    out = ROOT / "HarshitBiology" / f"unit{args.unit}" / "question_bank.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(bank, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {out} — {bank['meta']['total']} questions")


if __name__ == "__main__":
    main()
