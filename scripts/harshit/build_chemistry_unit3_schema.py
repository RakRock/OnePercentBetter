#!/usr/bin/env python3
"""Build HarshitChemistry/unit3/logic_schema.json (160 concept cards, Days 1–16)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.harshit.chemistry_unit3_content import DAY_BUILDERS, DAY_TITLES  # noqa: E402

OUT = ROOT / "HarshitChemistry" / "unit3" / "logic_schema.json"
UNIT_ID = 3


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
            "unit_id": UNIT_ID,
            "unit_title": "Metals and Non-metals",
            "ncert": "Class 10 Science, Chapter 3 (Chemistry)",
            "stage1_days": 16,
            "stage2_days": 4,
            "concept_cards_total": 160,
            "mcq_total": 40,
            "release_active": 4,
            "session_kind_concepts": "harshit_chemistry_unit3_concepts",
            "session_kind_mcq": "harshit_chemistry_unit3_mcq",
        },
        "glossary": [
            {"term": "metal", "definition": "Element that is lustrous, malleable, ductile, and generally good conductor of heat and electricity."},
            {"term": "non-metal", "definition": "Element that is generally dull, brittle, and poor conductor (with exceptions like graphite)."},
            {"term": "malleability", "definition": "Property of metals to be beaten into thin sheets."},
            {"term": "ductility", "definition": "Property of metals to be drawn into thin wires."},
            {"term": "reactivity series", "definition": "Arrangement of metals in order of decreasing reactivity."},
            {"term": "ionic compound", "definition": "Compound formed by transfer of electrons between metal and non-metal ions."},
            {"term": "ore", "definition": "Mineral from which a metal can be extracted profitably."},
            {"term": "corrosion", "definition": "Gradual destruction of metals by reaction with environment (e.g. rusting of iron)."},
            {"term": "galvanisation", "definition": "Coating iron/steel with zinc to prevent rusting."},
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
