#!/usr/bin/env python3
"""Build Harshit Biology Stage 2 mcq_bank (40 MCQs, days 17–20) for units 1+."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import harshit.biology.questions as hbq  # noqa: E402

QUESTIONS_PER_DAY = 10

UNIT_CONFIG: dict[int, dict] = {
    1: {
        "chapter_ref": "NCERT Class 10 Ch 5 — Life Processes",
        "pdf": "jesc105.pdf",
        "note": "Stage 2: NCERT Exercises Q1–4 + Intext + concept bank. Activities 5.1–5.8 linked per day.",
        "sessions": [
            (17, "Nutrition and Photosynthesis", [1, 2], [1, 2, 3, 4]),
            (18, "Digestion and Respiration", [3, 4], [5, 6, 7, 8, 9, 10]),
            (19, "Transport in Plants and Animals", [], [11, 12, 13, 14]),
            (20, "Excretion and Life Processes Review", [], [15, 16]),
        ],
    },
    2: {
        "chapter_ref": "NCERT Class 10 Ch 6 — Control and Coordination",
        "pdf": "jesc106.pdf",
        "note": "Stage 2: NCERT Exercises Q1–3 + Intext + concept bank. Activities 6.1–6.4 linked per day.",
        "sessions": [
            (17, "Nervous System and Receptors", [1], [1, 2, 3, 4]),
            (18, "Reflex Arc and Brain", [2], [5, 6, 7, 8]),
            (19, "Plant Coordination and Hormones", [3], [9, 10, 11, 12]),
            (20, "Endocrine System and Review", [], [13, 14, 15, 16]),
        ],
    },
    3: {
        "chapter_ref": "NCERT Class 10 Ch 7 — How do Organisms Reproduce?",
        "pdf": "jesc107.pdf",
        "note": "Stage 2: NCERT Exercises Q1–3 + Intext + concept bank. Activities 7.1–7.7 linked per day.",
        "sessions": [
            (17, "Asexual Reproduction", [1], [1, 2, 3, 4]),
            (18, "More Asexual Modes and Sexual Intro", [2], [5, 6, 7, 8]),
            (19, "Human Reproduction", [3], [9, 10, 11, 12]),
            (20, "Reproductive Health and Review", [], [13, 14, 15, 16]),
        ],
    },
    4: {
        "chapter_ref": "NCERT Class 10 Ch 8 — Heredity",
        "pdf": "jesc108.pdf",
        "note": "Stage 2: NCERT Exercise Q1 + 7 Intext + concept bank. Activities 8.1–8.2 linked per day.",
        "sessions": [
            (17, "Heredity and Variation", [1], [1, 2, 3, 4]),
            (18, "Mendel and Monohybrid Cross", [], [5, 6, 7, 8]),
            (19, "Dihybrid Cross and Sex Determination", [], [9, 10, 11, 12]),
            (20, "Inheritance Review and Exam Prep", [], [13, 14, 15, 16]),
        ],
    },
}


def _guess_misconception_unit1(q: dict) -> str:
    text = (q.get("question", "") + " " + q.get("explanation", "")).lower()
    if "xylem" in text or "phloem" in text or "translocation" in text:
        return "xylem_phloem_swap"
    if "aerobic" in text or "anaerobic" in text or "mitochondri" in text or "ferment" in text:
        return "aerobic_anaerobic_confusion"
    if "photosynth" in text or "chlorophyll" in text:
        return "photosynthesis_respiration_swap"
    if "autotroph" in text or "heterotroph" in text:
        return "autotroph_heterotroph_confusion"
    if "alveol" in text or "nephr" in text or "kidney" in text:
        return "alveoli_nephron_confusion"
    if "breathing" in text and "respiration" in text:
        return "photosynthesis_respiration_swap"
    return "aerobic_anaerobic_confusion"


def _guess_misconception_unit2(q: dict) -> str:
    text = (q.get("question", "") + " " + q.get("explanation", "")).lower()
    if "reflex" in text or "spinal cord" in text:
        return "reflex_brain_confusion"
    if "synapse" in text or "axon" in text or "dendrite" in text:
        return "synapse_axon_confusion"
    if "cytokinin" in text or "auxin" in text or "plant hormone" in text:
        return "plant_animal_hormone_swap"
    if "cerebellum" in text or "cerebrum" in text or "balance" in text:
        return "cerebellum_cerebrum_swap"
    if "adrenaline" in text or "hormone" in text or "endocrine" in text:
        return "nervous_hormonal_speed_swap"
    return "reflex_brain_confusion"


def _guess_misconception_unit3(q: dict) -> str:
    text = (q.get("question", "") + " " + q.get("explanation", "")).lower()
    if "budding" in text or "binary fission" in text or "fission" in text:
        return "binary_budding_swap"
    if "pollination" in text or "fertilisation" in text or "anther" in text:
        return "pollination_fertilisation_swap"
    if "vas deferens" in text or "ovary" in text or "testis" in text or "uterus" in text:
        return "male_female_organ_swap"
    if "dna" in text or "variation" in text:
        return "dna_copying_confusion"
    if "asexual" in text or "sexual" in text:
        return "asexual_sexual_swap"
    return "asexual_sexual_swap"


def _guess_misconception_unit4(q: dict) -> str:
    text = (q.get("question", "") + " " + q.get("explanation", "")).lower()
    if "dominant" in text or "recessive" in text or "mendel" in text:
        return "dominant_recessive_swap"
    if "genotype" in text or "phenotype" in text or "ttww" in text:
        return "genotype_phenotype_swap"
    if "dihybrid" in text or "monohybrid" in text or "independent" in text:
        return "monohybrid_dihybrid_swap"
    if "sex" in text and ("chromosom" in text or "child" in text or "xy" in text):
        return "sex_determination_confusion"
    if "variation" in text or "trait" in text:
        return "variation_inheritance_swap"
    return "dominant_recessive_swap"


_GUESS_BY_UNIT = {
    1: _guess_misconception_unit1,
    2: _guess_misconception_unit2,
    3: _guess_misconception_unit3,
    4: _guess_misconception_unit4,
}


def _load_ncert(unit_id: int) -> dict:
    path = ROOT / "HarshitBiology" / f"unit{unit_id}" / "ncert_source.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _exercise_by_num(ncert: dict, num: int) -> dict | None:
    for ex in ncert.get("exercise_mcqs", []):
        if int(ex["num"]) == num:
            return ex
    return None


def _intext_questions(ncert: dict) -> list[dict]:
    return list(ncert.get("intext_samples") or [])


def _normalize_ncert(
    raw: dict,
    *,
    unit_id: int,
    day_id: int,
    seq: int,
    chapter_ref: str,
    prefix: str = "ncert",
) -> dict:
    return {
        "id": f"u{unit_id}_d{day_id}_{prefix}_{seq:02d}",
        "question": raw["question"],
        "options": [str(o) for o in raw["options"]],
        "answer": int(raw["answer"]),
        "explanation": str(raw.get("explanation", "")),
        "misconception": raw.get("misconception", ""),
        "concept_id": (raw.get("concept_ids") or [""])[0] if raw.get("concept_ids") else "",
        "source": raw.get("source", f"NCERT Ch {unit_id}"),
        "chapter_ref": chapter_ref,
        "ncert_ref": raw.get("source") or raw.get("ref", ""),
    }


def _from_bank(
    unit_id: int,
    day_id: int,
    level: str,
    seq: int,
    used_text: set[str],
    guess_fn,
) -> dict | None:
    for raw in hbq.pool_for(day_id, level, unit_id):
        key = hbq.question_dedup_key(str(raw.get("question", "")), raw.get("options"))
        if key in used_text:
            continue
        try:
            q = hbq.normalize_question(raw, unit_id)
        except ValueError:
            continue
        used_text.add(key)
        out = dict(q)
        out["id"] = f"u{unit_id}_s2_d{day_id}_bank_{seq:02d}"
        out["misconception"] = out.get("misconception") or guess_fn(out)
        out["source"] = "concept_bank"
        return out
    return None


def _fill_bank_questions(
    unit_id: int,
    session_day: int,
    bank_days: list[int],
    need: int,
    used_text: set[str],
    start_seq: int,
    guess_fn,
) -> list[dict]:
    out: list[dict] = []
    seq = start_seq
    for src_day in bank_days:
        for lvl in ("B", "C", "A"):
            if len(out) >= need:
                return out
            q = _from_bank(unit_id, src_day, lvl, seq, used_text, guess_fn)
            if q:
                out.append(q)
                seq += 1
    for src_day in range(1, 17):
        if len(out) >= need:
            break
        for lvl in ("B", "C", "A"):
            if len(out) >= need:
                break
            q = _from_bank(unit_id, src_day, lvl, seq, used_text, guess_fn)
            if q:
                out.append(q)
                seq += 1
    return out


def _build_session(
    unit_id: int,
    day_id: int,
    title: str,
    exercise_nums: list[int],
    bank_days: list[int],
    ncert: dict,
    intext_pool: list[dict],
    used_bank: set[str],
    chapter_ref: str,
    guess_fn,
) -> dict:
    questions: list[dict] = []
    seq = 1

    for num in exercise_nums:
        ex = _exercise_by_num(ncert, num)
        if ex:
            questions.append(
                _normalize_ncert(
                    ex, unit_id=unit_id, day_id=day_id, seq=seq, chapter_ref=chapter_ref
                )
            )
            seq += 1

    while intext_pool and len(questions) < QUESTIONS_PER_DAY:
        raw = intext_pool.pop(0)
        questions.append(
            _normalize_ncert(
                raw,
                unit_id=unit_id,
                day_id=day_id,
                seq=seq,
                chapter_ref=chapter_ref,
                prefix="intext",
            )
        )
        seq += 1

    if len(questions) < QUESTIONS_PER_DAY:
        extra = _fill_bank_questions(
            unit_id,
            day_id,
            bank_days,
            QUESTIONS_PER_DAY - len(questions),
            used_bank,
            seq,
            guess_fn,
        )
        questions.extend(extra)

    activity_ids = [
        a["id"]
        for a in ncert.get("activities", [])
        if int(a.get("stage2_day", 0)) == day_id
    ]
    return {
        "day": day_id,
        "title": title,
        "active": True,
        "activity_refs": activity_ids,
        "questions": questions[:QUESTIONS_PER_DAY],
    }


def build_unit(unit_id: int) -> None:
    if unit_id not in UNIT_CONFIG:
        raise SystemExit(f"Unknown unit {unit_id}; choose from {sorted(UNIT_CONFIG)}")

    cfg = UNIT_CONFIG[unit_id]
    ncert = _load_ncert(unit_id)
    intext_pool = _intext_questions(ncert)
    used_bank: set[str] = set()
    guess_fn = _GUESS_BY_UNIT[unit_id]
    sessions = []
    for day_id, title, ex_nums, bank_days in cfg["sessions"]:
        sessions.append(
            _build_session(
                unit_id,
                day_id,
                title,
                ex_nums,
                bank_days,
                ncert,
                intext_pool,
                used_bank,
                cfg["chapter_ref"],
                guess_fn,
            )
        )

    total = sum(len(s["questions"]) for s in sessions)
    out = ROOT / "HarshitBiology" / f"unit{unit_id}" / "mcq_bank.json"
    payload = {
        "meta": {
            "unit_id": unit_id,
            "stage": 2,
            "active": True,
            "release": 5,
            "total_mcqs": total,
            "pdf": cfg["pdf"],
            "note": cfg["note"],
        },
        "sessions": sessions,
    }
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {out} — {total} MCQs across {len(sessions)} sessions")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Harshit Biology Stage 2 MCQ bank")
    parser.add_argument("--unit", type=int, required=True, choices=sorted(UNIT_CONFIG))
    args = parser.parse_args()
    build_unit(args.unit)


if __name__ == "__main__":
    main()
