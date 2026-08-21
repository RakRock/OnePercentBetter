"""Build practice sessions from weekly strategy/level configuration."""

from __future__ import annotations

import random

from arjun_linear_equation_strategies import (
    STRATEGIES,
    attach_question_parts,
    format_strategy_level_label,
    format_week_plan_summary,
    generate_question,
)
from arjun_mental_math_drills import build_mental_warmups, get_mental_math_count
from practice_quality.assembler import qa_and_assemble
from practice_quality.report import build_learning_report

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


def _slot_plan(config: dict, count: int) -> list[tuple[int, str]]:
    slots = _active_slots(config)
    if not slots:
        return []
    cycle = slots * ((count // len(slots)) + 1)
    random.shuffle(cycle)
    return cycle[:count]


def _slot_dict(sid: int, lvl: str) -> dict:
    info = STRATEGIES[sid]
    return {
        "strategy": sid,
        "level": lvl,
        "strategy_name": info["short"],
        "skill": info["levels"][lvl],
        "question_type": "equation_solving",
        "category": f"s{sid}_{lvl}",
        "category_label": format_strategy_level_label(sid, lvl),
    }


def _procedural_for_slot(slot: dict, used_ids: set[str], seen_fps: set[str]) -> dict | None:
    from practice_quality.dedup import is_duplicate_of_any

    sid, lvl = int(slot["strategy"]), str(slot["level"])
    for _ in range(20):
        q = generate_question(sid, lvl)
        if not q:
            continue
        q = attach_question_parts(dict(q))
        q.update(
            {
                "category": slot["category"],
                "category_label": slot["category_label"],
                "strategy_name": slot["strategy_name"],
                "skill": slot["skill"],
                "question_type": slot["question_type"],
                "source": "template",
            }
        )
        qid = str(q.get("id", ""))
        if qid and qid in used_ids:
            continue
        if is_duplicate_of_any(q, seen_fps):
            continue
        return q
    return None


def _build_procedural_session(config: dict, count: int = DEFAULT_QUESTION_COUNT) -> list[dict]:
    plan = _slot_plan(config, count)
    if not plan:
        return []
    slots = [_slot_dict(sid, lvl) for sid, lvl in plan]
    return qa_and_assemble(
        slots,
        _procedural_for_slot,
        program="linear",
        max_attempts_per_slot=24,
    )


def build_session_set(
    config: dict,
    count: int = DEFAULT_QUESTION_COUNT,
    *,
    xai_api_key: str | None = None,
    exclude_ids: set[str] | None = None,
    exclude_keys: set[str] | None = None,
) -> list[dict]:
    """Generate validated, deduplicated questions across enabled strategy/level slots."""
    linear_count = count
    plan = _slot_plan(config, linear_count)
    if not plan:
        warmups = build_mental_warmups(config)
        return warmups if warmups else []

    slots = [_slot_dict(sid, lvl) for sid, lvl in plan]
    initial: list[dict | None] = [None] * len(slots)

    if config.get("use_llm") and xai_api_key:
        from arjun_linear_equation_llm import generate_session_questions_raw

        try:
            batch = generate_session_questions_raw(xai_api_key, config, linear_count)
            for i, q in enumerate(batch[: len(slots)]):
                initial[i] = attach_question_parts(dict(q))
        except (ValueError, OSError):
            initial = [None] * len(slots)

    linear_questions = qa_and_assemble(
        slots,
        _procedural_for_slot,
        initial=initial,
        exclude_ids=exclude_ids,
        exclude_keys=exclude_keys,
        program="linear",
        max_attempts_per_slot=24,
    )

    warmups = build_mental_warmups(config)
    if warmups and linear_questions:
        return warmups + linear_questions
    if warmups:
        return warmups
    return linear_questions


def build_session_report(
    questions: list[dict],
    answers: list[dict],
    *,
    student_name: str = "Student",
) -> dict:
    return build_learning_report(questions, answers, student_name=student_name, program="linear")


def format_report_details(report: dict) -> str:
    lines = [f"Score: {report['correct_count']}/{report['total']} ({report['score_pct']}%)\n"]
    if report.get("summary_narrative"):
        lines.append(report["summary_narrative"])
        lines.append("")
    if report.get("strengths"):
        lines.append("✅ Doing well:")
        for s in report["strengths"]:
            lines.append(f"  • {s['name']} — {s['correct']}/{s['total']}")
    if report.get("needs_revision"):
        lines.append("\n📚 Needs revision:")
        for r in report["needs_revision"]:
            lines.append(f"  • {r['name']} — {r['correct']}/{r['total']}")
    if report.get("recommendations", {}).get("summary"):
        lines.append(f"\n🎯 Next: {report['recommendations']['summary']}")
    return "\n".join(lines)


def session_meta_from_config(config: dict) -> dict:
    return {
        "week_label": config.get("week_label", ""),
        "plan_summary": format_week_plan_summary(config),
        "strategies": config.get("strategies", []),
    }
