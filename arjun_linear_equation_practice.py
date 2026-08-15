"""Build practice sessions from weekly strategy/level configuration."""

from __future__ import annotations

import random

from arjun_linear_equation_strategies import (
    STRATEGIES,
    format_strategy_level_label,
    format_week_plan_summary,
    generate_question,
)
from arjun_mental_math_drills import build_mental_warmups, get_mental_math_count

STRENGTH_THRESHOLD_PCT = 80
DEFAULT_QUESTION_COUNT = 15


def _active_slots(config: dict) -> list[tuple[int, str]]:
    slots: list[tuple[int, str]] = []
    for item in config.get("strategies", []):
        sid = int(item["id"])
        for lvl in item.get("levels", []):
            if sid in STRATEGIES and lvl in STRATEGIES[sid]["levels"]:
                slots.append((sid, lvl))
    return slots


def _build_procedural_session(config: dict, count: int = DEFAULT_QUESTION_COUNT) -> list[dict]:
    """Generate questions from built-in Python templates."""
    slots = _active_slots(config)
    if not slots:
        return []

    selected: list[dict] = []
    used_ids: set[str] = set()
    slot_cycle = slots * ((count // len(slots)) + 1)
    random.shuffle(slot_cycle)

    for sid, lvl in slot_cycle:
        if len(selected) >= count:
            break
        for _ in range(12):
            q = generate_question(sid, lvl)
            if q and q["id"] not in used_ids:
                q = dict(q)
                q["category"] = f"s{sid}_{lvl}"
                q["category_label"] = format_strategy_level_label(sid, lvl)
                q["source"] = "template"
                selected.append(q)
                used_ids.add(q["id"])
                break

    random.shuffle(selected)
    return selected[:count]


def build_session_set(
    config: dict,
    count: int = DEFAULT_QUESTION_COUNT,
    *,
    xai_api_key: str | None = None,
) -> list[dict]:
    """Generate questions across enabled strategy/level slots."""
    linear_count = count
    if config.get("use_llm") and xai_api_key:
        from arjun_linear_equation_llm import generate_session_questions

        try:
            linear_questions = generate_session_questions(
                xai_api_key,
                config,
                linear_count,
                fallback=_build_procedural_session,
            )
        except (ValueError, OSError):
            linear_questions = _build_procedural_session(config, linear_count)
    else:
        linear_questions = _build_procedural_session(config, linear_count)

    warmups = build_mental_warmups(config)
    if warmups and linear_questions:
        return warmups + linear_questions
    if warmups:
        return warmups
    return linear_questions


def build_session_report(questions: list[dict], answers: list[dict]) -> dict:
    by_key: dict[str, dict] = {}
    for q, ans in zip(questions, answers):
        key = q.get("category") or f"s{q.get('strategy')}_{q.get('level')}"
        bucket = by_key.setdefault(key, {"correct": 0, "total": 0, "label": q.get("category_label", key)})
        bucket["total"] += 1
        if ans.get("correct"):
            bucket["correct"] += 1

    strengths: list[dict] = []
    needs_revision: list[dict] = []
    for key, stats in by_key.items():
        pct = int(100 * stats["correct"] / stats["total"]) if stats["total"] else 0
        sid = int(key.split("_")[0][1:]) if key.startswith("s") else 0
        emoji = (
            "⚡" if key.startswith("mm_")
            else "🔍" if sid == 1
            else "⚖️" if sid == 2
            else "✂️" if sid == 3
            else "📦" if sid == 4
            else "➗" if sid == 5
            else "📐" if sid == 6
            else "🔗"
        )
        entry = {
            "category": key,
            "name": stats["label"],
            "emoji": emoji,
            "color": "#6366f1",
            "correct": stats["correct"],
            "total": stats["total"],
            "pct": pct,
            "activity_slug": None,
            "tip": f"Review {stats['label']} and try similar problems.",
        }
        if pct >= STRENGTH_THRESHOLD_PCT:
            strengths.append(entry)
        elif pct < STRENGTH_THRESHOLD_PCT:
            needs_revision.append(entry)

    strengths.sort(key=lambda x: (-x["pct"], x["name"]))
    needs_revision.sort(key=lambda x: (x["pct"], x["name"]))
    correct_count = sum(1 for a in answers if a.get("correct"))
    total = len(answers)
    score_pct = int(100 * correct_count / total) if total else 0

    tip = needs_revision[0]["tip"] if needs_revision else ""

    return {
        "correct_count": correct_count,
        "total": total,
        "score_pct": score_pct,
        "strengths": strengths,
        "needs_revision": needs_revision,
        "tip": tip,
    }


def format_report_details(report: dict) -> str:
    lines = [f"Score: {report['correct_count']}/{report['total']} ({report['score_pct']}%)\n"]
    if report.get("strengths"):
        lines.append("✅ Doing well:")
        for s in report["strengths"]:
            lines.append(f"  • {s['name']} — {s['correct']}/{s['total']}")
    if report.get("needs_revision"):
        lines.append("\n📚 Needs revision:")
        for r in report["needs_revision"]:
            lines.append(f"  • {r['name']} — {r['correct']}/{r['total']}")
    return "\n".join(lines)


def session_meta_from_config(config: dict) -> dict:
    return {
        "week_label": config.get("week_label", ""),
        "plan_summary": format_week_plan_summary(config),
        "strategies": config.get("strategies", []),
    }
