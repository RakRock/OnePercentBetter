"""Strategy/skill-level mastery from session results."""

from __future__ import annotations

MASTERED_PCT = 80
DEVELOPING_PCT = 50


def _strategy_id(q: dict) -> int | None:
    if q.get("strategy") is not None:
        return int(q["strategy"])
    cat = str(q.get("category", ""))
    if cat.startswith("s") and "_" in cat:
        try:
            return int(cat.split("_")[0][1:])
        except ValueError:
            return None
    if cat.startswith("p") and "_t" in cat:
        try:
            return int(cat.split("_t")[1].split("_")[0])
        except ValueError:
            return None
    return None


def _strategy_name(q: dict, sid: int | None) -> str:
    if q.get("strategy_name"):
        return str(q["strategy_name"])
    label = str(q.get("category_label", ""))
    if label and "·" in label:
        return label.split("·")[0].strip()
    if label and "Level" in label:
        return label.split("Level")[0].strip()
    try:
        import arjun_linear_equation_strategies as leqs

        if sid and sid in leqs.STRATEGIES:
            return leqs.STRATEGIES[sid]["short"]
    except Exception:
        pass
    return label or f"Strategy {sid or '?'}"


def _skill_label(q: dict) -> str:
    if q.get("skill"):
        return str(q["skill"])
    sid = _strategy_id(q)
    lvl = str(q.get("level", ""))
    try:
        import arjun_linear_equation_strategies as leqs

        if sid and sid in leqs.STRATEGIES and lvl in leqs.STRATEGIES[sid]["levels"]:
            return leqs.STRATEGIES[sid]["levels"][lvl]
    except Exception:
        pass
    label = str(q.get("category_label", ""))
    if "· Level" in label:
        return label.split("· Level", 1)[1].strip()
    if "Level" in label:
        parts = label.split("Level", 1)
        if len(parts) > 1:
            return parts[1].strip()
    return label or "General"


def compute_mastery(
    questions: list[dict],
    answers: list[dict],
    *,
    exclude_warmups: bool = True,
) -> dict:
    """Mastery by strategy and by skill (strategy × level)."""
    by_strategy: dict[int, dict] = {}
    by_skill: dict[str, dict] = {}

    for q, ans in zip(questions, answers):
        if exclude_warmups and q.get("is_warmup"):
            continue
        sid = _strategy_id(q)
        skill = _skill_label(q)
        sname = _strategy_name(q, sid)

        if sid is not None:
            bucket = by_strategy.setdefault(
                sid,
                {"strategy_id": sid, "name": sname, "correct": 0, "total": 0},
            )
            bucket["total"] += 1
            if ans.get("correct"):
                bucket["correct"] += 1

        skill_key = f"{sname} — {skill}" if skill != sname else skill
        sb = by_skill.setdefault(
            skill_key,
            {"skill": skill, "strategy": sname, "correct": 0, "total": 0},
        )
        sb["total"] += 1
        if ans.get("correct"):
            sb["correct"] += 1

    def _status(pct: int) -> str:
        if pct >= MASTERED_PCT:
            return "Mastered"
        if pct >= DEVELOPING_PCT:
            return "Developing"
        return "Needs Practice"

    strategy_rows = []
    for sid, stats in sorted(by_strategy.items(), key=lambda x: x[0]):
        pct = int(100 * stats["correct"] / stats["total"]) if stats["total"] else 0
        strategy_rows.append(
            {
                **stats,
                "pct": pct,
                "status": _status(pct),
            }
        )

    skill_rows = []
    for key, stats in by_skill.items():
        pct = int(100 * stats["correct"] / stats["total"]) if stats["total"] else 0
        skill_rows.append(
            {
                "key": key,
                **stats,
                "pct": pct,
                "status": _status(pct),
            }
        )
    skill_rows.sort(key=lambda r: (r["pct"], r["key"]))

    mastered = [r for r in strategy_rows if r["status"] == "Mastered"]
    developing = [r for r in strategy_rows if r["status"] == "Developing"]
    needs = [r for r in strategy_rows if r["status"] == "Needs Practice"]

    if len(mastered) == len(strategy_rows) and strategy_rows:
        overall = "Mastered"
    elif needs and not developing and not mastered:
        overall = "Needs Practice"
    elif needs:
        overall = "Developing"
    else:
        overall = "Developing"

    return {
        "by_strategy": strategy_rows,
        "by_skill": skill_rows,
        "mastered_strategies": mastered,
        "developing_strategies": developing,
        "needs_practice_strategies": needs,
        "overall_status": overall,
    }
