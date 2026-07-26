"""Export learning plans and progress reports."""

from __future__ import annotations

import json
from typing import Any

from .content_catalog import MODULES
from .progress_store import ProgressStore


def export_plan_markdown(markdown: str) -> str:
    return markdown


def export_progress_markdown(store: ProgressStore, user_id: int, profile: str) -> str:
    prog = store.get_module_progress(user_id)
    stats = store.dashboard_summary(user_id, len(MODULES))
    q = store.quiz_stats(user_id)
    drills = store.drill_progress(user_id)

    lines = [
        f"# Progress Report — {profile}",
        "",
        f"- Modules completed: **{stats['modules_completed']} / {stats['modules_total']}** ({stats['progress_pct']}%)",
        f"- Quiz average: **{stats['quiz_average_pct']}%** ({stats['quiz_attempts']} attempts)",
        f"- Design drills completed: **{stats['drills_completed']}**",
        "",
        "## Module status",
        "",
    ]
    for m in MODULES:
        p = prog.get(m.id, {})
        status = "✅" if p.get("completed") else "⬜"
        lines.append(f"- {status} **{m.title}** ({m.difficulty})")
        if p.get("notes"):
            lines.append(f"  - Notes: {p['notes'][:200]}")
    lines.extend(["", "## Recent quiz attempts", ""])
    for r in q.get("recent", []):
        lines.append(f"- {r['quiz_id']}: {r['score']}/{r['total']} ({r['created_at'][:10]})")
    lines.extend(["", "## Drills", ""])
    for d_id, done in drills.items():
        lines.append(f"- {'✅' if done else '⬜'} {d_id}")
    return "\n".join(lines)


def export_progress_json(store: ProgressStore, user_id: int, profile: str) -> str:
    data: dict[str, Any] = {
        "profile": profile,
        "summary": store.dashboard_summary(user_id, len(MODULES)),
        "modules": store.get_module_progress(user_id),
        "quizzes": store.quiz_stats(user_id),
        "drills": store.drill_progress(user_id),
        "bookmarks": store.list_bookmarks(user_id),
        "latest_plan": store.latest_plan(user_id),
    }
    return json.dumps(data, indent=2)
