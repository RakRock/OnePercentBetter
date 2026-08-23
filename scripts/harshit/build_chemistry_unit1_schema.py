#!/usr/bin/env python3
"""Build HarshitChemistry/unit1/logic_schema.json (160 concept cards, Days 1–16)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.harshit.chemistry_unit1_content import DAY_BUILDERS, DAY_TITLES  # noqa: E402

OUT = ROOT / "HarshitChemistry" / "unit1" / "logic_schema.json"


def build_schema() -> dict:
    days = []
    for day_num in sorted(DAY_BUILDERS):
        days.append(
            {
                "day": day_num,
                "stage": 1,
                "title": DAY_TITLES[day_num],
                "active": True,
                "release": (day_num - 1) // 4 + 1,
                "concepts": DAY_BUILDERS[day_num](),
            }
        )

    return {
        "meta": {
            "student": "Harshit Sai",
            "unit_id": 1,
            "unit_title": "Chemical Reactions and Equations",
            "ncert": "Class 10 Science, Chapter 1 (Chemistry)",
            "stage1_days": 16,
            "stage2_days": 4,
            "concept_cards_total": 160,
            "mcq_total": 40,
            "release_active": 4,
            "session_kind_concepts": "harshit_chemistry_unit1_concepts",
            "session_kind_mcq": "harshit_chemistry_unit1_mcq",
        },
        "glossary": [
            {"term": "chemical reaction", "definition": "Process where reactants change into new products with different properties."},
            {"term": "chemical equation", "definition": "Symbolic representation of a reaction using formulae and state symbols."},
            {"term": "balanced equation", "definition": "Equation with equal numbers of each atom on both sides (conservation of mass)."},
            {"term": "combination reaction", "definition": "Two or more substances combine to form a single product."},
            {"term": "decomposition reaction", "definition": "Single compound breaks into two or more simpler substances."},
            {"term": "displacement reaction", "definition": "More reactive element displaces less reactive element from its compound."},
            {"term": "double displacement", "definition": "Exchange of ions between two compounds, often forming a precipitate."},
            {"term": "oxidation", "definition": "Gain of oxygen or loss of hydrogen (or loss of electrons)."},
            {"term": "reduction", "definition": "Loss of oxygen or gain of hydrogen (or gain of electrons)."},
            {"term": "corrosion", "definition": "Gradual destruction of metals by chemical reaction with environment (e.g. rusting)."},
            {"term": "rancidity", "definition": "Oxidation of fats and oils causing unpleasant smell and taste in food."},
        ],
        "days": days,
    }


def main() -> None:
    schema = build_schema()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(schema, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    active_cards = sum(len(d["concepts"]) for d in schema["days"] if d.get("active"))
    print(f"Wrote {OUT} — {active_cards} active concept cards (Days 1–16)")


if __name__ == "__main__":
    main()
