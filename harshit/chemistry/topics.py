"""Practice topic catalog for Harshit Chemistry."""

from __future__ import annotations

from . import content as hpc

LEVELS = {
    "A": "Recall — definitions and key facts",
    "B": "Apply — examples and reasoning",
    "C": "Avoid mistakes — common confusions",
}


def topics_for_unit(unit_id: int = 1) -> dict[int, dict]:
    """Day number → topic metadata (mirrors Class 10 topic map)."""
    if unit_id not in hpc.UNITS:
        return {}
    out: dict[int, dict] = {}
    for day in hpc.list_days(stage=1, unit_id=unit_id):
        if not day.get("active"):
            continue
        did = int(day["day"])
        out[did] = {
            "id": did,
            "name": day["title"],
            "emoji": "🧪",
            "levels": dict(LEVELS),
            "concept_count": len(day.get("concepts") or []),
        }
    return out


def format_topic_level_label(unit_id: int, day_id: int, level: str) -> str:
    topics = topics_for_unit(unit_id)
    info = topics.get(day_id, {})
    lvl = LEVELS.get(level, level)
    return f"Day {day_id} — {info.get('name', 'Topic')} · {lvl}"


def default_week_config(unit_id: int = 1) -> dict:
    topics = topics_for_unit(unit_id)
    umeta = hpc.unit_meta(unit_id)
    return {
        "unit_id": unit_id,
        "week_label": f"Unit {unit_id} — {umeta['title']} (all topics)",
        "topics": [{"id": did, "levels": ["A", "B", "C"]} for did in sorted(topics)],
        "practice_difficulty": 3,
        "use_chapter_llm": False,
        "grok_fresh_only": False,
    }


def format_week_plan_summary(unit_id: int, config: dict) -> str:
    lines = []
    if config.get("week_label"):
        lines.append(f"Week: {config['week_label']}")
    topics = topics_for_unit(unit_id)
    for item in config.get("topics", []):
        did = int(item["id"])
        info = topics.get(did, {})
        levels = ", ".join(item.get("levels", []))
        lines.append(f"• Day {did}: {info.get('name', '?')} — levels {levels}")
    return "\n".join(lines) if lines else "No topics selected."
