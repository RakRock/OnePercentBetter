"""Learning plan generator — Claude when available, deterministic template otherwise."""

from __future__ import annotations

from typing import Any

from .content_catalog import MODULES
from .llm_client import claude_chat, claude_json, get_anthropic_api_key
from .models import GeneratedPlan, LearningPlanInput
from .rag_sources import OFFICIAL_DOCS


def _module_slugs_for_focus(focus_areas: list[str]) -> list[int]:
    if not focus_areas:
        return [m.id for m in MODULES]
    ids: list[int] = []
    focus_lower = [f.lower() for f in focus_areas]
    for m in MODULES:
        blob = f"{m.title} {m.domain} {' '.join(m.key_terms)}".lower()
        if any(f in blob for f in focus_lower):
            ids.append(m.id)
    return ids or [m.id for m in MODULES]


def _template_plan(profile: str, inp: LearningPlanInput) -> GeneratedPlan:
    mod_ids = _module_slugs_for_focus(inp.focus_areas)
    modules_ordered = [m for m in MODULES if m.id in mod_ids]
    per_week = max(1, len(modules_ordered) // inp.weeks)
    weeks: list[dict[str, Any]] = []

    idx = 0
    for w in range(1, inp.weeks + 1):
        chunk = modules_ordered[idx : idx + per_week]
        idx += per_week
        tasks = []
        for m in chunk:
            tasks.append(
                {
                    "type": "lesson",
                    "module_id": m.id,
                    "title": m.title,
                    "hours": round(m.minutes / 60, 1),
                    "docs": [OFFICIAL_DOCS.get(k, OFFICIAL_DOCS["ra_index"]) for k in m.doc_keys[:2]],
                }
            )
            tasks.append({"type": "quiz", "module_id": m.id, "title": f"Quiz: {m.title}"})
        if w % 2 == 0:
            tasks.append({"type": "design_drill", "title": "Complete one architecture drill"})
        if w == inp.weeks:
            tasks.append({"type": "assessment", "title": "50-question final assessment"})
        weeks.append(
            {
                "week": w,
                "theme": f"Week {w}: {inp.goal}",
                "hours_budget": inp.hours_per_week,
                "tasks": tasks,
                "checkpoint": f"Review weak areas; verify against NVIDIA lifecycle docs",
                "deliverable": f"Week {w} summary notes + architecture sketch",
            }
        )

    md_lines = [
        f"# Learning Plan — {profile}",
        "",
        f"**Role:** {inp.role} | **Level:** {inp.level} | **Goal:** {inp.goal}",
        f"**Duration:** {inp.weeks} weeks × {inp.hours_per_week} hrs/week",
        "",
        "## Focus areas",
        ", ".join(inp.focus_areas) if inp.focus_areas else "Full curriculum",
        "",
        "## Constraints",
        inp.constraints or "None specified",
        "",
        "## Official references",
        f"- [NVIDIA AI Enterprise RA]({OFFICIAL_DOCS['ra_index']})",
        f"- [Lifecycle policy]({OFFICIAL_DOCS['lifecycle']})",
        "",
    ]
    for wk in weeks:
        md_lines.append(f"## Week {wk['week']}")
        md_lines.append(f"*{wk['theme']}* — budget **{wk['hours_budget']}h**")
        md_lines.append("")
        for t in wk["tasks"]:
            if t["type"] == "lesson":
                md_lines.append(f"- **Lesson:** {t['title']} (~{t['hours']}h)")
                for d in t.get("docs", []):
                    md_lines.append(f"  - Read: {d}")
            else:
                md_lines.append(f"- **{t['type'].title()}:** {t['title']}")
        md_lines.append(f"- **Checkpoint:** {wk['checkpoint']}")
        md_lines.append(f"- **Deliverable:** {wk['deliverable']}")
        md_lines.append("")

    markdown = "\n".join(md_lines)
    return GeneratedPlan(profile=profile, input=inp, weeks=weeks, markdown=markdown)


def generate_plan(profile: str, inp: LearningPlanInput, api_key: str | None = None) -> GeneratedPlan:
    key = get_anthropic_api_key(api_key)
    if not key:
        return _template_plan(profile, inp)

    module_summary = [
        {"id": m.id, "title": m.title, "domain": m.domain, "minutes": m.minutes}
        for m in MODULES
    ]
    system = (
        "You are an NVIDIA AI Enterprise Reference Architecture learning coach. "
        "Generate a week-by-week learning plan as JSON with keys: "
        "weeks (list of {week, theme, hours_budget, tasks, checkpoint, deliverable}) "
        "and markdown (full plan as markdown string). "
        "Ground tasks in the module catalog. Include official NVIDIA doc URLs. "
        "Do not invent compatibility claims."
    )
    import json

    user = json.dumps(
        {
            "profile": profile,
            "input": inp.__dict__,
            "modules": module_summary,
            "official_docs": OFFICIAL_DOCS,
        }
    )
    try:
        data = claude_json(system, user, api_key=key)
        if not data:
            return _template_plan(profile, inp)
        weeks = data.get("weeks") or _template_plan(profile, inp).weeks
        markdown = data.get("markdown") or _template_plan(profile, inp).markdown
        return GeneratedPlan(profile=profile, input=inp, weeks=weeks, markdown=markdown)
    except Exception:
        return _template_plan(profile, inp)


COACH_SYSTEM_PROMPT = """You are an NVIDIA AI Enterprise Reference Architecture learning coach.
Teach enterprise platform engineers using accurate, structured explanations.
Ground answers in the provided content catalog and official NVIDIA docs.
Prefer diagrams, mental models, checklists, quizzes, and practical implementation guidance.
Do not invent compatibility claims.
For version-specific guidance, tell the user to check the NVIDIA AI Enterprise support matrix
and lifecycle/compatibility explorer.
Do not pretend to have deployed anything in the user's environment."""


def coach_reply(
    user_message: str,
    context: str,
    api_key: str | None = None,
    history: list[dict] | None = None,
) -> str:
    """Agent coach — Claude if ANTHROPIC_API_KEY available, else rule-based."""
    key = get_anthropic_api_key(api_key)
    if key:
        try:
            transcript = ""
            for turn in (history or [])[-8:]:
                role = turn.get("role", "user")
                transcript += f"\n{role.upper()}: {turn.get('content', '')}\n"
            user_block = f"Context:\n{context[:12000]}\n\nConversation:{transcript}\n\nUser: {user_message}"
            reply = claude_chat(COACH_SYSTEM_PROMPT, user_block, api_key=key, max_tokens=2048)
            if reply:
                return reply
        except Exception as exc:
            return f"Coach unavailable ({exc}). Using offline guidance below.\n\n" + _offline_coach(
                user_message, context
            )
    return _offline_coach(user_message, context)


def _offline_coach(message: str, context: str) -> str:
    msg = message.lower()
    if "gpu operator" in msg:
        return (
            "**GPU Operator** deploys driver, container toolkit, device plugin, and DCGM on GPU nodes. "
            "Check ClusterPolicy and node labels first when pods can't get `nvidia.com/gpu`.\n\n"
            f"Docs: {OFFICIAL_DOCS['gpu_operator']}\n\n"
            "Recommended next lesson: Module 5 — GPU Operator Deep Dive."
        )
    if "nim" in msg or "nimcache" in msg:
        return (
            "**NIM** provides optimized inference microservices. **NIM Operator** manages CRDs like "
            "NIMCache (model artifacts) and NIMService (running inference). Ensure NIMCache is Ready before NIMService.\n\n"
            f"Docs: {OFFICIAL_DOCS['nim_operator']}\n\n"
            "Recommended: Modules 9–12."
        )
    if "plan" in msg or "path" in msg:
        return "Use **Learning Path** in the sidebar to generate a week-by-week plan (works offline with templates)."
    if "quiz" in msg:
        return "Open **Quizzes** for module quizzes or the 50-question final assessment."
    return (
        "I'm in offline coach mode — set `ANTHROPIC_API_KEY` (e.g. in ~/.zshrc) for full Claude coaching.\n\n"
        "Try asking about GPU Operator, NIM, RAG, lifecycle branches, or troubleshooting.\n\n"
        f"Start here: {OFFICIAL_DOCS['ra_index']}"
    )
