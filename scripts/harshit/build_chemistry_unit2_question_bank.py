#!/usr/bin/env python3
"""Build Harshit Chemistry Unit 2 question bank (200 MCQs from concept cards)."""

from __future__ import annotations

import json
import random
import re
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import harshit.chemistry.content as hpc  # noqa: E402
import harshit.chemistry.topics as hpt  # noqa: E402

TARGET_TOTAL = 200
BANK_PATH = ROOT / "HarshitChemistry" / "unit2" / "question_bank.json"


def _slug(text: str) -> str:
    t = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")
    return t[:40] or "q"


def _shuffle_options(correct: str, wrong: list[str]) -> tuple[list[str], int]:
    opts = [correct] + wrong[:3]
    while len(opts) < 4:
        opts.append(f"None of the above ({len(opts)})")
    random.shuffle(opts)
    return opts, opts.index(correct)


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


def _q_recall(concept: dict, day_id: int, concepts: list[dict], level: str, seq: int) -> dict:
    name = concept["name"]
    correct = str(concept.get("simple_answer", "")).split(".")[0].strip() + "."
    wrong = _distractors(concepts, concept["id"], "simple_answer")
    options, answer = _shuffle_options(correct, wrong)
    return {
        "id": f"u2_d{day_id}_{level.lower()}_{seq:03d}",
        "question": f"Which statement best describes **{name}**?",
        "options": options,
        "answer": answer,
        "explanation": concept.get("remember") or concept.get("simple_answer", ""),
        "day_id": day_id,
        "concept_id": concept["id"],
        "level": level,
        "category": f"u2_d{day_id}_{level}",
        "category_label": hpt.format_topic_level_label(2, day_id, level),
        "source": "bank",
        "chapter_ref": "NCERT Class 10 Ch 2 — Acids, Bases and Salts",
    }


def _q_remember(concept: dict, day_id: int, concepts: list[dict], level: str, seq: int) -> dict:
    remember = str(concept.get("remember") or concept.get("simple_answer", "")).strip()
    if not remember:
        return _q_recall(concept, day_id, concepts, level, seq)
    correct = remember.split(".")[0].strip() + ("." if "." not in remember[:80] else "")
    wrong = _distractors(concepts, concept["id"], "remember") or _distractors(concepts, concept["id"], "simple_answer")
    options, answer = _shuffle_options(correct, wrong)
    return {
        "id": f"u2_d{day_id}_{level.lower()}_{seq:03d}",
        "question": f"What is the key takeaway about **{concept['name']}**?",
        "options": options,
        "answer": answer,
        "explanation": remember,
        "day_id": day_id,
        "concept_id": concept["id"],
        "level": level,
        "category": f"u2_d{day_id}_{level}",
        "category_label": hpt.format_topic_level_label(2, day_id, level),
        "source": "bank",
        "chapter_ref": "NCERT Class 10 Ch 2 — Acids, Bases and Salts",
    }


def _q_confusion(concept: dict, day_id: int, concepts: list[dict], level: str, seq: int) -> dict:
    confusion = str(concept.get("common_confusion") or "").strip()
    if not confusion:
        return _q_apply(concept, day_id, concepts, level, seq)
    correct = f"Avoid thinking: {confusion.split('.')[0].strip()}."
    wrong = [
        confusion,
        "There are no common mistakes for this topic.",
        "Any answer is acceptable in exams.",
    ]
    options, answer = _shuffle_options(correct, wrong)
    return {
        "id": f"u2_d{day_id}_{level.lower()}_{seq:03d}",
        "question": f"Which advice helps you avoid mistakes about **{concept['name']}**?",
        "options": options,
        "answer": answer,
        "explanation": confusion,
        "day_id": day_id,
        "concept_id": concept["id"],
        "level": level,
        "category": f"u2_d{day_id}_{level}",
        "category_label": hpt.format_topic_level_label(2, day_id, level),
        "source": "bank",
        "chapter_ref": "NCERT Class 10 Ch 2 — Acids, Bases and Salts",
    }


def _q_apply(concept: dict, day_id: int, concepts: list[dict], level: str, seq: int) -> dict:
    example = str(concept.get("example") or concept.get("why") or concept.get("simple_answer", "")).strip()
    correct = example.split(".")[0].strip() + "."
    wrong = _distractors(concepts, concept["id"], "example") or _distractors(concepts, concept["id"], "why")
    options, answer = _shuffle_options(correct, wrong)
    return {
        "id": f"u2_d{day_id}_{level.lower()}_{seq:03d}",
        "question": f"Which example or application fits **{concept['name']}**?",
        "options": options,
        "answer": answer,
        "explanation": example,
        "day_id": day_id,
        "concept_id": concept["id"],
        "level": level,
        "category": f"u2_d{day_id}_{level}",
        "category_label": hpt.format_topic_level_label(2, day_id, level),
        "source": "bank",
        "chapter_ref": "NCERT Class 10 Ch 2 — Acids, Bases and Salts",
    }


def _q_name_pick(concept: dict, day_id: int, concepts: list[dict], level: str, seq: int) -> dict:
    """Pick the concept name from a definition."""
    definition = str(concept.get("simple_answer", "")).split(".")[0].strip()
    correct = concept["name"]
    others = [c["name"] for c in concepts if c["id"] != concept["id"]]
    random.shuffle(others)
    wrong = others[:3]
    while len(wrong) < 3:
        wrong.append(f"Topic {len(wrong) + 1}")
    options, answer = _shuffle_options(correct, wrong)
    return {
        "id": f"u2_d{day_id}_{level.lower()}_{seq:03d}",
        "question": f"Which term matches this description? \"{definition}.\"",
        "options": options,
        "answer": answer,
        "explanation": f"This describes {concept['name']}: {concept.get('simple_answer', '')}",
        "day_id": day_id,
        "concept_id": concept["id"],
        "level": level,
        "category": f"u2_d{day_id}_{level}",
        "category_label": hpt.format_topic_level_label(2, day_id, level),
        "source": "bank",
        "chapter_ref": "NCERT Class 10 Ch 2 — Acids, Bases and Salts",
    }


GENERATORS = {
    "A": [_q_recall, _q_name_pick, _q_remember],
    "B": [_q_apply, _q_remember, _q_recall],
    "C": [_q_confusion, _q_apply, _q_remember],
}


def _questions_for_day(day_id: int, count: int) -> list[dict]:
    concepts = hpc.concepts_for_day(day_id, unit_id=2)
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
        q = gen(concept, day_id, concepts, level, seq)
        out.append(q)
        seq += 1
        ci += 1
        gi += 1
    return out


def build_bank(*, seed: int = 42) -> dict:
    random.seed(seed)
    days = [d for d in hpc.list_days(stage=1, unit_id=2) if d.get("active")]
    n_days = len(days) or 1
    base = TARGET_TOTAL // n_days
    extra = TARGET_TOTAL % n_days

    all_q: list[dict] = []
    by_day: dict[str, list[dict]] = {}
    for i, day in enumerate(sorted(days, key=lambda d: d["day"])):
        did = int(day["day"])
        count = base + (1 if i < extra else 0)
        day_qs = _questions_for_day(did, count)
        by_day[str(did)] = day_qs
        all_q.extend(day_qs)

    # Dedupe by question text
    seen: set[str] = set()
    unique: list[dict] = []
    for q in all_q:
        key = q["question"].strip().lower()
        if key in seen:
            q["id"] = f"u2_{uuid.uuid4().hex[:8]}"
            key = q["question"].strip().lower() + q["id"]
        seen.add(key)
        unique.append(q)

    return {
        "meta": {
            "unit_id": 2,
            "total": len(unique),
            "target": TARGET_TOTAL,
            "ncert": "Class 10 Science, Chapter 2 — Acids, Bases and Salts",
            "levels": list(hpt.LEVELS.keys()),
        },
        "questions_by_day": by_day,
        "questions": unique,
    }


def main() -> None:
    bank = build_bank()
    BANK_PATH.parent.mkdir(parents=True, exist_ok=True)
    BANK_PATH.write_text(json.dumps(bank, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {BANK_PATH} — {bank['meta']['total']} questions")


if __name__ == "__main__":
    main()
