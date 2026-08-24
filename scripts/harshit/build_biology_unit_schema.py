#!/usr/bin/env python3
"""Build HarshitBiology/unitN/logic_schema.json (160 concept cards, Days 1–16)."""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import harshit.biology.content as hpc  # noqa: E402

UNIT_GLOSSARY: dict[int, list[dict]] = {
    1: [
        {"term": "life processes", "definition": "Basic functions like nutrition, respiration, transport, and excretion that maintain life."},
        {"term": "nutrition", "definition": "Process of obtaining and using food for growth, repair, and energy."},
        {"term": "photosynthesis", "definition": "Synthesis of food in green plants using CO₂, water, and sunlight."},
        {"term": "respiration", "definition": "Release of energy from food inside cells, often using oxygen."},
        {"term": "xylem", "definition": "Vascular tissue transporting water and minerals upward in plants."},
        {"term": "phloem", "definition": "Vascular tissue transporting food (sucrose) in plants."},
        {"term": "excretion", "definition": "Removal of harmful metabolic wastes from the body."},
        {"term": "nephron", "definition": "Structural and functional unit of the kidney that filters blood and forms urine."},
    ],
    2: [
        {"term": "neuron", "definition": "Nerve cell that transmits electrical impulses for control and coordination."},
        {"term": "synapse", "definition": "Gap between two neurons where chemical neurotransmitters pass the signal."},
        {"term": "reflex arc", "definition": "Neural pathway for quick automatic responses without conscious thought."},
        {"term": "hormone", "definition": "Chemical messenger secreted by endocrine glands that regulates body functions."},
        {"term": "tropism", "definition": "Directional growth movement of a plant in response to a stimulus."},
        {"term": "auxin", "definition": "Plant hormone that promotes cell elongation and phototropism."},
        {"term": "adrenaline", "definition": "Fight-or-flight hormone from adrenal glands that prepares body for emergency."},
        {"term": "cerebellum", "definition": "Hind-brain region controlling posture, balance, and precision of voluntary actions."},
    ],
    3: [
        {"term": "asexual reproduction", "definition": "Reproduction involving a single parent without gamete fusion."},
        {"term": "sexual reproduction", "definition": "Reproduction involving fusion of male and female gametes with variation."},
        {"term": "binary fission", "definition": "Asexual division of a unicellular organism into two equal parts."},
        {"term": "pollination", "definition": "Transfer of pollen from anther to stigma in flowering plants."},
        {"term": "fertilisation", "definition": "Fusion of male and female gametes to form a zygote."},
        {"term": "menstruation", "definition": "Monthly shedding of uterine lining when fertilisation does not occur."},
        {"term": "contraception", "definition": "Methods to prevent pregnancy by blocking fertilisation or implantation."},
        {"term": "DNA copying", "definition": "Replication of genetic material essential for faithful inheritance in reproduction."},
    ],
    4: [
        {"term": "heredity", "definition": "Transmission of traits from parents to offspring through genes."},
        {"term": "variation", "definition": "Differences among individuals of a species in inherited characteristics."},
        {"term": "dominant trait", "definition": "Trait expressed even when only one copy of the allele is present."},
        {"term": "recessive trait", "definition": "Trait expressed only when two copies of the allele are present."},
        {"term": "monohybrid cross", "definition": "Mendelian cross involving one pair of contrasting traits."},
        {"term": "dihybrid cross", "definition": "Cross involving two pairs of contrasting traits studied by Mendel."},
        {"term": "genotype", "definition": "Genetic makeup of an organism (e.g. Tt, TT, tt)."},
        {"term": "phenotype", "definition": "Observable physical expression of traits (e.g. tall, violet flowers)."},
    ],
}


def _load_content(unit_id: int):
    mod = importlib.import_module(f"scripts.harshit.biology_unit{unit_id}_content")
    return mod.DAY_BUILDERS, mod.DAY_TITLES


def build_schema(unit_id: int) -> dict:
    meta = hpc.unit_meta(unit_id)
    day_builders, day_titles = _load_content(unit_id)
    days = []
    for day_num in sorted(day_builders):
        days.append(
            {
                "day": day_num,
                "stage": 1,
                "title": day_titles[day_num],
                "active": True,
                "release": (day_num - 1) // 4 + 1,
                "concepts": day_builders[day_num](),
            }
        )

    return {
        "meta": {
            "student": "Harshit Sai",
            "unit_id": unit_id,
            "unit_title": meta["title"],
            "ncert": meta["ncert"],
            "stage1_days": 16,
            "stage2_days": 4,
            "concept_cards_total": 160,
            "mcq_total": 40,
            "release_active": 4,
            "session_kind_concepts": meta["session_kind_concepts"],
            "session_kind_mcq": meta["session_kind_mcq"],
        },
        "glossary": UNIT_GLOSSARY.get(unit_id, []),
        "days": days,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Harshit Biology logic_schema.json")
    parser.add_argument("--unit", type=int, required=True, choices=[1, 2, 3, 4])
    args = parser.parse_args()

    schema = build_schema(args.unit)
    out = ROOT / "HarshitBiology" / f"unit{args.unit}" / "logic_schema.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(schema, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    active_cards = sum(len(d["concepts"]) for d in schema["days"] if d.get("active"))
    print(f"Wrote {out} — {active_cards} active concept cards (Days 1–16)")


if __name__ == "__main__":
    main()
