"""PreReq 2 coverage matrix, week presets, and config migration (Arjun-style 7 strategies)."""

from __future__ import annotations

import harshit_prereq_topics as hpt

PREREQ2_ID = 2
PREREQ2_STRATEGY_COUNT = 7

# Map legacy single topic-4 levels to split strategies 4–7
_LEGACY_TOPIC4_LEVEL_MAP: dict[str, tuple[int, str]] = {
    "A": (4, "A"),
    "B": (4, "B"),
    "C": (5, "C"),
    "D": (6, "D"),
    "E": (7, "E"),
}

PREREQ2_WEEK_PRESETS: dict[str, dict] = {
    "week1_foundation": {
        "label": "Week 1 — Foundation (Level A on all 7 strategies)",
        "week_label": "Algebra — Week 1 (Foundation)",
        "levels_by_topic": {tid: ["A"] for tid in range(1, PREREQ2_STRATEGY_COUNT + 1)},
    },
    "week2_build": {
        "label": "Week 2 — Build (Levels A + B)",
        "week_label": "Algebra — Week 2 (A + B)",
        "levels_by_topic": {tid: ["A", "B"] for tid in range(1, PREREQ2_STRATEGY_COUNT + 1)},
    },
    "week3_stretch": {
        "label": "Week 3 — Stretch (Levels A–C)",
        "week_label": "Algebra — Week 3 (A–C)",
        "levels_by_topic": {
            tid: ["A", "B", "C"] for tid in range(1, PREREQ2_STRATEGY_COUNT + 1)
        },
    },
    "week4_advanced": {
        "label": "Week 4 — Advanced (Levels A–D)",
        "week_label": "Algebra — Week 4 (A–D)",
        "levels_by_topic": {
            tid: ["A", "B", "C", "D"] for tid in range(1, PREREQ2_STRATEGY_COUNT + 1)
        },
    },
    "full_coverage": {
        "label": "Full coverage — all 7 strategies, Levels A–E",
        "week_label": "Algebra — Full coverage (A–E)",
        "levels_by_topic": {
            tid: list(hpt.LEVEL_ORDER) for tid in range(1, PREREQ2_STRATEGY_COUNT + 1)
        },
    },
    "polynomials_only": {
        "label": "Polynomials focus (Strategies 1–3, A–E)",
        "week_label": "Algebra — Polynomials (Ch 2)",
        "levels_by_topic": {tid: list(hpt.LEVEL_ORDER) for tid in (1, 2, 3)},
    },
    "linear_only": {
        "label": "Linear 2-var focus (Strategies 4–7, A–E)",
        "week_label": "Algebra — Linear Equations (Ch 4)",
        "levels_by_topic": {tid: list(hpt.LEVEL_ORDER) for tid in (4, 5, 6, 7)},
    },
}

PREREQ2_REQUIREMENTS: list[tuple[str, str]] = [
    ("Ch 2 · Polynomials", "Add/subtract like terms; multiply polynomials; factor using identities"),
    ("Ch 4 · Substitution", "Find one variable given the other in ax + by = c"),
    ("Ch 4 · Solution pairs", "Complete ordered pairs and tables of solutions"),
    ("Ch 4 · Graphing", "Verify points on a line; read solutions from graphs"),
    ("Ch 4 · Word problems", "Translate context into ax + by + c = 0 and solve"),
]

_PREREQ_LABELS = {
    1: "Number Systems",
    2: "Algebra",
    3: "Coordinate",
    4: "Geometry",
    5: "Mensuration",
    6: "Data",
}

GENERIC_WEEK_PRESETS: dict[str, dict] = {
    "week1_foundation": {
        "label": "Week 1 — Foundation (Level A on all topics)",
        "week_suffix": "Week 1 (Foundation)",
        "levels": ["A"],
    },
    "week2_build": {
        "label": "Week 2 — Build (Levels A + B)",
        "week_suffix": "Week 2 (A + B)",
        "levels": ["A", "B"],
    },
    "week3_stretch": {
        "label": "Week 3 — Stretch (Levels A–C)",
        "week_suffix": "Week 3 (A–C)",
        "levels": ["A", "B", "C"],
    },
    "week4_advanced": {
        "label": "Week 4 — Advanced (Levels A–D)",
        "week_suffix": "Week 4 (A–D)",
        "levels": ["A", "B", "C", "D"],
    },
    "full_coverage": {
        "label": "Full coverage — all topics, Levels A–E",
        "week_suffix": "Full coverage (A–E)",
        "levels": list(hpt.LEVEL_ORDER),
    },
}


def migrate_prereq2_config(config: dict) -> dict:
    """Expand legacy 4-topic PreReq 2 plans into 7-strategy plans."""
    if not config.get("topics"):
        return config

    needs_split = any(
        int(item["id"]) == 4 and lvl in ("C", "D", "E")
        for item in config.get("topics", [])
        for lvl in item.get("levels", [])
    )
    if not needs_split:
        return config

    merged: dict[int, set[str]] = {}
    for item in config.get("topics", []):
        tid = int(item["id"])
        for lvl in item.get("levels", []):
            if tid == 4 and lvl in _LEGACY_TOPIC4_LEVEL_MAP:
                new_tid, new_lvl = _LEGACY_TOPIC4_LEVEL_MAP[lvl]
                merged.setdefault(new_tid, set()).add(new_lvl)
            else:
                merged.setdefault(tid, set()).add(lvl)

    new_topics = [
        {"id": tid, "levels": sorted(levels, key=hpt.LEVEL_ORDER.index)}
        for tid, levels in sorted(merged.items())
        if levels
    ]
    out = dict(config)
    out["topics"] = new_topics
    return out


def apply_preset(preset_key: str) -> dict:
    preset = PREREQ2_WEEK_PRESETS[preset_key]
    topics = [
        {"id": tid, "levels": list(levels)}
        for tid, levels in sorted(preset["levels_by_topic"].items())
    ]
    return {
        "week_label": preset["week_label"],
        "topics": topics,
        "warmup_count": 0,
        "use_llm": True,
        "use_chapter_llm": True,
        "grok_fresh_only": False,
        "prereq_id": PREREQ2_ID,
    }


def apply_generic_preset(prereq_id: int, preset_key: str) -> dict:
    """Week presets for PreReqs 1 and 3–6 (all topics in the unit)."""
    preset = GENERIC_WEEK_PRESETS[preset_key]
    catalog = hpt.topics_for_prereq(prereq_id)
    label_base = _PREREQ_LABELS.get(prereq_id, f"PreReq {prereq_id}")
    topics: list[dict] = []
    for tid in sorted(catalog):
        levels = [lvl for lvl in preset["levels"] if lvl in catalog[tid]["levels"]]
        if levels:
            topics.append({"id": tid, "levels": levels})
    return {
        "week_label": f"{label_base} — {preset['week_suffix']}",
        "topics": topics,
        "warmup_count": 0,
        "use_llm": True,
        "use_chapter_llm": True,
        "grok_fresh_only": False,
        "prereq_id": prereq_id,
    }


def merge_missing_topics(prereq_id: int, config: dict) -> dict:
    """Add catalog topics missing from a saved plan (default Levels A + B)."""
    if not config.get("topics"):
        return config
    catalog = hpt.topics_for_prereq(prereq_id)
    present = {int(item["id"]) for item in config.get("topics", [])}
    missing = [tid for tid in sorted(catalog) if tid not in present]
    if not missing:
        return config
    topics = list(config.get("topics", []))
    for tid in missing:
        topics.append({"id": tid, "levels": ["A", "B"]})
    out = dict(config)
    out["topics"] = sorted(topics, key=lambda item: int(item["id"]))
    return out


def migrate_week_config(prereq_id: int, config: dict) -> dict:
    """Normalize saved weekly plans (PreReq 2 split + newly added topics)."""
    if prereq_id == PREREQ2_ID:
        config = migrate_prereq2_config(config)
    return merge_missing_topics(prereq_id, config)


def coverage_stats(prereq_id: int, config: dict) -> dict:
    """How many strategy×level cells are configured vs total."""
    topics = hpt.topics_for_prereq(prereq_id)
    if not topics:
        return {"configured": 0, "total": 0, "pct": 0, "by_topic": {}}

    configured = 0
    by_topic: dict[int, list[str]] = {}
    for item in config.get("topics", []):
        tid = int(item["id"])
        if tid not in topics:
            continue
        lvls = [lvl for lvl in item.get("levels", []) if lvl in topics[tid]["levels"]]
        by_topic[tid] = lvls
        configured += len(lvls)

    total = sum(len(info["levels"]) for info in topics.values())
    pct = round(100 * configured / total) if total else 0
    return {"configured": configured, "total": total, "pct": pct, "by_topic": by_topic}


def format_coverage_line(prereq_id: int, config: dict) -> str:
    stats = coverage_stats(prereq_id, config)
    if not stats["total"]:
        return "No topics defined."
    unit = "strategy×level" if prereq_id == PREREQ2_ID else "topic×level"
    return (
        f"Coverage: {stats['configured']}/{stats['total']} {unit} cells "
        f"({stats['pct']}%)"
    )


def strategy_label(prereq_id: int, topic_id: int) -> str:
    """Arjun-style 'Strategy N' prefix for PreReq 2."""
    if prereq_id == PREREQ2_ID:
        return f"Strategy {topic_id}"
    return "Topic"
