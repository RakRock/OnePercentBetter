#!/usr/bin/env python3
"""Build HarshitChemistry/unit2/logic_schema.json (160 concept cards, Days 1–16)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.harshit.chemistry_unit2_content import DAY_BUILDERS, DAY_TITLES  # noqa: E402

OUT = ROOT / "HarshitChemistry" / "unit2" / "logic_schema.json"


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
            "unit_id": 2,
            "unit_title": "Acids, Bases and Salts",
            "ncert": "Class 10 Science, Chapter 2 (Chemistry)",
            "stage1_days": 16,
            "stage2_days": 4,
            "concept_cards_total": 160,
            "mcq_total": 40,
            "release_active": 4,
            "session_kind_concepts": "harshit_chemistry_unit2_concepts",
            "session_kind_mcq": "harshit_chemistry_unit2_mcq",
        },
        "glossary": [
            {"term": "acid", "definition": "Substance that turns blue litmus red; produces H⁺ ions in aqueous solution."},
            {"term": "base", "definition": "Substance that turns red litmus blue; produces OH⁻ ions in aqueous solution."},
            {"term": "indicator", "definition": "Substance that changes colour in acidic or basic medium (e.g. litmus)."},
            {"term": "neutralisation", "definition": "Reaction of acid and base to form salt and water."},
            {"term": "pH", "definition": "Measure of hydrogen ion concentration; 7 is neutral, below 7 acidic, above 7 basic."},
            {"term": "salt", "definition": "Ionic compound formed from acid-base reaction (or other neutralisation)."},
            {"term": "water of crystallisation", "definition": "Fixed number of water molecules in one formula unit of a crystal."},
            {"term": "dilution", "definition": "Adding water to lower concentration; always add acid to water, slowly with stirring."},
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
