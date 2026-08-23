#!/usr/bin/env python3
"""Build HarshitChemistry/unit4/logic_schema.json (160 concept cards, Days 1–16)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.harshit.chemistry_unit4_content import DAY_BUILDERS, DAY_TITLES  # noqa: E402

OUT = ROOT / "HarshitChemistry" / "unit4" / "logic_schema.json"
UNIT_ID = 4


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
            "unit_title": "Carbon and its Compounds",
            "ncert": "Class 10 Science, Chapter 4 (Chemistry)",
            "stage1_days": 16,
            "stage2_days": 4,
            "concept_cards_total": 160,
            "mcq_total": 40,
            "release_active": 4,
            "session_kind_concepts": "harshit_chemistry_unit4_concepts",
            "session_kind_mcq": "harshit_chemistry_unit4_mcq",
        },
        "glossary": [
            {"term": "covalent bond", "definition": "Bond formed by sharing of electron pairs between atoms."},
            {"term": "catenation", "definition": "Property of carbon to form long chains and rings by bonding to other carbon atoms."},
            {"term": "tetravalency", "definition": "Carbon has valency four — forms four covalent bonds."},
            {"term": "hydrocarbon", "definition": "Compound containing only carbon and hydrogen."},
            {"term": "homologous series", "definition": "Family of compounds with same functional group, differing by CH₂."},
            {"term": "functional group", "definition": "Specific atom/group that determines chemical properties of an organic compound."},
            {"term": "saturated compound", "definition": "Contains only single C–C bonds (e.g. alkanes)."},
            {"term": "unsaturated compound", "definition": "Contains double or triple C–C bonds (e.g. alkenes, alkynes)."},
            {"term": "micelle", "definition": "Cluster of soap/detergent molecules that traps oily dirt in water."},
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
