"""Build Harshit PreReq practice sessions from weekly topic/level configuration."""

from __future__ import annotations

import random

import harshit_prereq_topics as hpt

STRENGTH_THRESHOLD_PCT = 80
DEFAULT_QUESTION_COUNT = 12
MAX_WARMUP = 5


def _active_slots(prereq_id: int, config: dict) -> list[tuple[int, str]]:
    slots: list[tuple[int, str]] = []
    topics = hpt.topics_for_prereq(prereq_id)
    for item in config.get("topics", []):
        tid = int(item["id"])
        for lvl in item.get("levels", []):
            if tid in topics and lvl in topics[tid]["levels"]:
                slots.append((tid, lvl))
    return slots


def _build_warmups(prereq_id: int, config: dict) -> list[dict]:
    count = max(0, min(MAX_WARMUP, int(config.get("warmup_count", 0))))
    if count == 0:
        return []
    slots = _active_slots(prereq_id, config)
    if not slots:
        return []
    warm: list[dict] = []
    used: set[str] = set()
    easy = [(tid, "A") for tid, lvl in slots if lvl == "A"] or slots[:1]
    cycle = easy * (count + 1)
    random.shuffle(cycle)
    for tid, lvl in cycle:
        if len(warm) >= count:
            break
        q = hpt.generate_question(prereq_id, tid, lvl)
        if q and q["id"] not in used:
            q = dict(q)
            q["category_label"] = f"Warm-up · {q['category_label']}"
            q["is_warmup"] = True
            warm.append(q)
            used.add(q["id"])
    return warm


def build_session_set(
    prereq_id: int,
    config: dict,
    count: int = DEFAULT_QUESTION_COUNT,
) -> list[dict]:
    slots = _active_slots(prereq_id, config)
    if not slots:
        return _build_warmups(prereq_id, config)

    selected: list[dict] = []
    used_ids: set[str] = set()
    cycle = slots * ((count // len(slots)) + 1)
    random.shuffle(cycle)

    for tid, lvl in cycle:
        if len(selected) >= count:
            break
        for _ in range(10):
            q = hpt.generate_question(prereq_id, tid, lvl)
            if q and q["id"] not in used_ids:
                selected.append(q)
                used_ids.add(q["id"])
                break

    random.shuffle(selected)
    main = selected[:count]
    warmups = _build_warmups(prereq_id, config)
    return warmups + main if warmups else main


def build_session_report(questions: list[dict], answers: list[dict]) -> dict:
    by_key: dict[str, dict] = {}
    for q, ans in zip(questions, answers):
        key = q.get("category") or "unknown"
        bucket = by_key.setdefault(
            key,
            {"correct": 0, "total": 0, "label": q.get("category_label", key)},
        )
        bucket["total"] += 1
        if ans.get("correct"):
            bucket["correct"] += 1

    strengths: list[dict] = []
    needs_revision: list[dict] = []
    for key, stats in by_key.items():
        pct = int(100 * stats["correct"] / stats["total"]) if stats["total"] else 0
        emoji = "⚡" if "Warm-up" in stats["label"] else "📘"
        entry = {
            "category": key,
            "name": stats["label"],
            "emoji": emoji,
            "correct": stats["correct"],
            "total": stats["total"],
            "pct": pct,
            "tip": f"Review {stats['label']} in your NCERT notes.",
        }
        if pct >= STRENGTH_THRESHOLD_PCT:
            strengths.append(entry)
        else:
            needs_revision.append(entry)

    strengths.sort(key=lambda x: (-x["pct"], x["name"]))
    needs_revision.sort(key=lambda x: (x["pct"], x["name"]))
    correct_count = sum(1 for a in answers if a.get("correct"))
    total = len(answers)
    score_pct = int(100 * correct_count / total) if total else 0

    return {
        "correct_count": correct_count,
        "total": total,
        "score_pct": score_pct,
        "strengths": strengths,
        "needs_revision": needs_revision,
        "tip": needs_revision[0]["tip"] if needs_revision else "",
    }


def session_meta_from_config(prereq_id: int, config: dict) -> dict:
    return {
        "prereq_id": prereq_id,
        "week_label": config.get("week_label", ""),
        "topics": config.get("topics", []),
        "warmup_count": config.get("warmup_count", 0),
    }


def format_report_details(report: dict) -> str:
    lines = [f"Score: {report['correct_count']}/{report['total']} ({report['score_pct']}%)\n"]
    if report.get("strengths"):
        lines.append("Doing well:")
        for s in report["strengths"]:
            lines.append(f"  • {s['name']} — {s['correct']}/{s['total']}")
    if report.get("needs_revision"):
        lines.append("Needs revision:")
        for s in report["needs_revision"]:
            lines.append(f"  • {s['name']} — {s['correct']}/{s['total']}")
    return "\n".join(lines)
