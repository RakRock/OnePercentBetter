"""Difficulty levels for Arjun Course 3 practice (textbook + Edgenuity)."""

from __future__ import annotations

LEVEL_ORDER = ["A", "B", "C", "D", "E"]

DEFAULT_LEVELS = ["B", "C"]

LEVEL_DESCRIPTIONS: dict[str, str] = {
    "A": "Foundation — quick recall, one step",
    "B": "Build — standard grade-level practice",
    "C": "Standard — multi-step, typical test items",
    "D": "Stretch — harder numbers or reasoning",
    "E": "Challenge — exam-style twist problems",
}


def levels_for_category(category_id: str, category_name: str = "") -> dict[str, str]:
    """Per-category level menu (shared descriptions; category name for context)."""
    _ = category_name or category_id.replace("_", " ").title()
    return dict(LEVEL_DESCRIPTIONS)


def infer_level(position: int, total: int) -> str:
    """Assign A–E when a bank question has no explicit level tag."""
    if total <= 1:
        return "B"
    ratio = position / max(total - 1, 1)
    if ratio < 0.2:
        return "A"
    if ratio < 0.55:
        return "B"
    if ratio < 0.8:
        return "C"
    if ratio < 0.93:
        return "D"
    return "E"


def bank_level_map(bank: list[dict]) -> dict[str, str]:
    by_cat: dict[str, list[dict]] = {}
    for q in bank:
        by_cat.setdefault(str(q.get("category", "")), []).append(q)
    result: dict[str, str] = {}
    for qs in by_cat.values():
        total = len(qs)
        for i, q in enumerate(qs):
            qid = str(q.get("id", ""))
            tagged = q.get("level")
            if tagged in LEVEL_ORDER:
                result[qid] = str(tagged)
            else:
                result[qid] = infer_level(i, total)
    return result


def normalize_topics(
    config: dict,
    valid_categories: set[str],
    *,
    default_levels: list[str] | None = None,
) -> list[dict]:
    """Normalize week config to topics: [{id, levels}]. Migrates legacy categories list."""
    defaults = default_levels or DEFAULT_LEVELS
    topics = config.get("topics")
    if isinstance(topics, list) and topics:
        normalized: list[dict] = []
        for item in topics:
            if not isinstance(item, dict):
                continue
            cat_id = str(item.get("id", "")).strip()
            if cat_id not in valid_categories:
                continue
            levels = item.get("levels")
            if not isinstance(levels, list):
                levels = []
            clean_levels = [str(lvl) for lvl in levels if str(lvl) in LEVEL_ORDER]
            if clean_levels:
                normalized.append({"id": cat_id, "levels": clean_levels})
        if normalized:
            return normalized

    legacy = config.get("categories")
    if isinstance(legacy, list) and legacy:
        return [
            {"id": str(cat_id), "levels": list(defaults)}
            for cat_id in legacy
            if str(cat_id) in valid_categories
        ]
    return []


def categories_from_topics(topics: list[dict]) -> list[str]:
    return [str(t["id"]) for t in topics if isinstance(t, dict) and t.get("id")]


def active_slots(topics: list[dict], valid_categories: set[str]) -> list[tuple[str, str]]:
    slots: list[tuple[str, str]] = []
    for item in topics:
        cat_id = str(item.get("id", ""))
        if cat_id not in valid_categories:
            continue
        for lvl in item.get("levels") or []:
            if str(lvl) in LEVEL_ORDER:
                slots.append((cat_id, str(lvl)))
    return slots


def slot_plan(topics: list[dict], valid_categories: set[str], count: int) -> list[tuple[str, str]]:
    slots = active_slots(topics, valid_categories)
    if not slots or count <= 0:
        return []
    cycle = slots * ((count // len(slots)) + 1)
    import random

    random.shuffle(cycle)
    return cycle[:count]


def level_label(level: str) -> str:
    return LEVEL_DESCRIPTIONS.get(level, f"Level {level}")


def format_level_picker_label(level: str) -> str:
    return f"Level {level} — {LEVEL_DESCRIPTIONS.get(level, level)}"


def normalize_week_config(
    config: dict,
    valid_categories: set[str],
    *,
    unit_id: int | None = None,
) -> dict:
    """Return config with normalized topics and derived categories."""
    topics = normalize_topics(config, valid_categories)
    out = {**config, "topics": topics, "categories": categories_from_topics(topics)}
    if unit_id is not None:
        out["unit_id"] = unit_id
    return out
