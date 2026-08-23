#!/usr/bin/env python3
"""Build Harshit Chemistry Stage 2 mcq_bank (40 MCQs, days 17–20) for units 1–4."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import harshit.chemistry.questions as hcq  # noqa: E402

QUESTIONS_PER_DAY = 10

UNIT_CONFIG: dict[int, dict] = {
    1: {
        "chapter_ref": "NCERT Class 10 Ch 1 — Chemical Reactions and Equations",
        "pdf": "jesc101.pdf",
        "note": "Stage 2: NCERT Exercises Q1–3 + Intext + concept bank. Activities 1.1–1.11 linked per day.",
        "sessions": [
            (17, "Signs of Reaction and Equations", [1, 2], [1, 2, 3, 4]),
            (18, "Balancing and Reaction Types", [3], [5, 6, 7, 8, 9]),
            (19, "Displacement and Double Displacement", [], [9, 10, 11, 12]),
            (20, "Redox, Corrosion and Rancidity", [], [11, 12, 13, 14, 15, 16]),
        ],
    },
    2: {
        "chapter_ref": "NCERT Class 10 Ch 2 — Acids, Bases and Salts",
        "pdf": "jesc102.pdf",
        "note": "Stage 2: NCERT Exercises Q1–4 + Intext + concept bank. Activities 2.1–2.15 linked per day.",
        "sessions": [
            (17, "Acids, Bases and Indicators", [1, 2], [1, 2, 3]),
            (18, "Acid-Base Reactions and Neutralisation", [3, 4], [4, 5, 6, 7]),
            (19, "pH Scale and Everyday Acids/Bases", [], [8, 9, 10, 11]),
            (20, "Salts and Chemicals from Common Salt", [], [12, 13, 14, 15, 16]),
        ],
    },
    3: {
        "chapter_ref": "NCERT Class 10 Ch 3 — Metals and Non-metals",
        "pdf": "jesc103.pdf",
        "note": "Stage 2: NCERT Exercises Q1–4 + Intext + concept bank. Activities 3.1–3.13 linked per day.",
        "sessions": [
            (17, "Physical Properties of Metals", [1, 2], [1, 2, 3, 4]),
            (18, "Chemical Properties and Reactivity", [3, 4], [5, 6, 7, 8, 9]),
            (19, "Ionic Compounds and Extraction", [], [10, 11, 12, 13]),
            (20, "Corrosion Prevention and Alloys", [], [14, 15, 16]),
        ],
    },
    4: {
        "chapter_ref": "NCERT Class 10 Ch 4 — Carbon and its Compounds",
        "pdf": "jesc104.pdf",
        "note": "Stage 2: NCERT Exercises Q1–3 + Intext + concept bank. Activities 4.1–4.12 linked per day.",
        "sessions": [
            (17, "Covalent Bonding and Homologous Series", [1, 2], [1, 2, 3, 4]),
            (18, "Saturated/Unsaturated and Nomenclature", [3], [4, 5, 6, 7, 8]),
            (19, "Chemical Properties and Functional Groups", [], [9, 10, 11, 12]),
            (20, "Soaps, Detergents and Fuels", [], [13, 14, 15, 16]),
        ],
    },
}


def _guess_misconception_unit1(q: dict) -> str:
    text = (q.get("question", "") + " " + q.get("explanation", "")).lower()
    if "coefficient" in text or "subscript" in text or "balance" in text:
        return "coefficient_subscript_confusion"
    if "unbalanced" in text or "conservation" in text:
        return "unbalanced_equation_accepted"
    if "oxid" in text or "reduc" in text or "redox" in text:
        return "oxidation_reduction_swap"
    if "displac" in text or "reactiv" in text:
        return "displacement_reactivity_error"
    if "physical" in text and "chemical" in text:
        return "physical_vs_chemical_change"
    return "coefficient_subscript_confusion"


def _guess_misconception_unit2(q: dict) -> str:
    text = (q.get("question", "") + " " + q.get("explanation", "")).lower()
    if "litmus" in text:
        return "litmus_colour_confusion"
    if "neutral" in text or "salt" in text and "water" in text:
        return "neutralisation_products_error"
    if "dilut" in text or "water to acid" in text:
        return "dilution_order_wrong"
    if "ph" in text:
        return "ph_scale_reversed"
    if "phenolphthalein" in text or "methyl orange" in text or "indicator" in text:
        return "indicator_in_acid_base_confusion"
    return "ph_scale_reversed"


def _guess_misconception_unit3(q: dict) -> str:
    text = (q.get("question", "") + " " + q.get("explanation", "")).lower()
    if "malleab" in text or "ductil" in text or "lustre" in text or "sonor" in text:
        return "metal_nonmetal_property_swap"
    if "reactiv" in text or "series" in text or "displac" in text:
        return "reactivity_series_order_error"
    if "ionic" in text or "electron transfer" in text or "nacl" in text:
        return "ionic_bond_covalent_confusion"
    if "corros" in text or "rust" in text or "galvan" in text or "paint" in text:
        return "corrosion_prevention_wrong"
    return "displacement_reactivity_error"


def _guess_misconception_unit4(q: dict) -> str:
    text = (q.get("question", "") + " " + q.get("explanation", "")).lower()
    if "ionic" in text or "covalent" in text or "share" in text:
        return "ionic_covalent_confusion"
    if "saturat" in text or "unsaturat" in text or "double bond" in text:
        return "saturated_unsaturated_swap"
    if "addition" in text or "substitution" in text:
        return "addition_substitution_confusion"
    if "functional" in text or "suffix" in text or "ketone" in text or "aldehyde" in text:
        return "functional_group_naming_error"
    if "soap" in text or "detergent" in text or "hard water" in text or "micelle" in text:
        return "soap_detergent_hard_water_error"
    return "ionic_covalent_confusion"


_GUESS_BY_UNIT = {
    1: _guess_misconception_unit1,
    2: _guess_misconception_unit2,
    3: _guess_misconception_unit3,
    4: _guess_misconception_unit4,
}


def _load_ncert(unit_id: int) -> dict:
    path = ROOT / "HarshitChemistry" / f"unit{unit_id}" / "ncert_source.json"
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
    for raw in hcq.pool_for(day_id, level, unit_id):
        key = hcq.question_dedup_key(str(raw.get("question", "")), raw.get("options"))
        if key in used_text:
            continue
        try:
            q = hcq.normalize_question(raw, unit_id)
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
        raise SystemExit(f"Unknown unit {unit_id}; choose 1, 2, 3, or 4")

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
    out = ROOT / "HarshitChemistry" / f"unit{unit_id}" / "mcq_bank.json"
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
    parser = argparse.ArgumentParser(description="Build Harshit Chemistry Stage 2 MCQ bank")
    parser.add_argument("--unit", type=int, required=True, choices=[1, 2, 3, 4])
    args = parser.parse_args()
    build_unit(args.unit)


if __name__ == "__main__":
    main()
