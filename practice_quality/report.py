"""Learning progress reports with validated stats, mastery, and recommendations."""

from __future__ import annotations

from practice_quality.error_analysis import analyze_errors
from practice_quality.mastery import compute_mastery, MASTERED_PCT
from practice_quality.coaching import build_coaching_concepts


def _question_text_for_report(q: dict) -> str:
    if q.get("equation"):
        try:
            import arjun_linear_equation_strategies as leqs

            return leqs.compose_question(
                q.get("instruction", ""),
                q.get("equation", ""),
                q.get("followup", ""),
            )
        except Exception:
            pass
    return str(q.get("question", "")).strip()


def _picked_and_correct_for_report(q: dict, ans: dict) -> tuple[str, str]:
    if "picked" in ans:
        return str(ans.get("picked", "?")), str(ans.get("correct_val", "?"))
    opts = q.get("options") or []
    choice = ans.get("choice")
    picked = opts[choice] if isinstance(choice, int) and 0 <= choice < len(opts) else "?"
    correct_idx = q.get("answer")
    correct = opts[correct_idx] if isinstance(correct_idx, int) and 0 <= correct_idx < len(opts) else "?"
    return str(picked), str(correct)


def _base_category_report(questions: list[dict], answers: list[dict]) -> dict:
    """Legacy per-category strengths/needs_revision (excludes warm-ups from scoring)."""
    by_key: dict[str, dict] = {}
    scored_qs = []
    scored_ans = []
    for q, ans in zip(questions, answers):
        if q.get("is_warmup"):
            continue
        scored_qs.append(q)
        scored_ans.append(ans)
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
        entry = {
            "category": key,
            "name": stats["label"],
            "emoji": "⚡" if "Warm-up" in stats["label"] else "📘",
            "correct": stats["correct"],
            "total": stats["total"],
            "pct": pct,
            "tip": f"Review {stats['label']} and try similar problems.",
        }
        if pct >= MASTERED_PCT:
            strengths.append(entry)
        else:
            needs_revision.append(entry)

    strengths.sort(key=lambda x: (-x["pct"], x["name"]))
    needs_revision.sort(key=lambda x: (x["pct"], x["name"]))

    correct_count = sum(1 for a in scored_ans if a.get("correct"))
    total = len(scored_ans)
    score_pct = int(100 * correct_count / total) if total else 0

    return {
        "correct_count": correct_count,
        "total": total,
        "score_pct": score_pct,
        "strengths": strengths,
        "needs_revision": needs_revision,
        "tip": needs_revision[0]["tip"] if needs_revision else "",
    }


def _build_recommendations(mastery: dict, errors: dict) -> dict:
    weak = [s for s in mastery.get("by_skill", []) if s["status"] != "Mastered"]
    weak.sort(key=lambda x: (x["pct"], x["key"]))

    buckets: list[dict] = []
    total_q = 10
    if not weak:
        return {
            "summary": "Continue mixed practice across all strategies at 80%+ before advancing.",
            "items": [{"skill": "Mixed review", "count": total_q}],
            "mastery_target_pct": MASTERED_PCT,
        }

    remaining = total_q
    for row in weak[:4]:
        share = max(1, round(total_q * (100 - row["pct"]) / max(100 * len(weak[:4]), 1)))
        share = min(share, remaining)
        buckets.append({"skill": row["key"], "count": share, "strategy": row.get("strategy", "")})
        remaining -= share
    if remaining > 0 and buckets:
        buckets[0]["count"] += remaining

    parts = [f"{b['count']} {b['skill']}" for b in buckets]
    summary = f"Complete {total_q} targeted questions: " + ", ".join(parts) + f". Aim for {MASTERED_PCT}%+ before advancing."

    return {
        "summary": summary,
        "items": buckets,
        "mastery_target_pct": MASTERED_PCT,
    }


def _summary_narrative(
    student_name: str,
    report: dict,
    mastery: dict,
    errors: dict,
) -> str:
    name = student_name.split()[0] if student_name else "The student"
    score = f"{report['correct_count']}/{report['total']} ({report['score_pct']}%)"
    mastered = [r["name"] for r in mastery.get("mastered_strategies", [])]
    weak = [r["name"] for r in mastery.get("needs_practice_strategies", [])]
    developing = [r["name"] for r in mastery.get("developing_strategies", [])]

    parts = [f"{name} completed {report['total']} questions and scored {score}."]
    if mastered:
        parts.append(f"Strong with {', '.join(mastered[:3])}{'…' if len(mastered) > 3 else ''}.")
    focus = weak or developing
    if focus:
        parts.append(f"Main areas to improve: {', '.join(focus[:3])}{'…' if len(focus) > 3 else ''}.")
    elif errors.get("patterns"):
        labels = [p["label"] for p in errors["patterns"][:2]]
        parts.append(f"Watch for: {'; '.join(labels)}.")
    else:
        parts.append("Solid session across strategies.")
    return " ".join(parts)


def _validate_report_consistency(questions: list[dict], answers: list[dict], report: dict) -> None:
    scored = [(q, a) for q, a in zip(questions, answers) if not q.get("is_warmup")]
    actual_correct = sum(1 for _, a in scored if a.get("correct"))
    actual_total = len(scored)
    if report["correct_count"] != actual_correct or report["total"] != actual_total:
        raise ValueError(
            f"Report score {report['correct_count']}/{report['total']} "
            f"does not match answers {actual_correct}/{actual_total}"
        )


def build_learning_report(
    questions: list[dict],
    answers: list[dict],
    *,
    student_name: str = "Student",
    program: str = "auto",
) -> dict:
    """
    Full learning report: base scores, mastery by strategy, error patterns,
    recommendations, and failed-question detail for email footer.
    """
    base = _base_category_report(questions, answers)
    mastery = compute_mastery(questions, answers)
    errors = analyze_errors(questions, answers)
    recommendations = _build_recommendations(mastery, errors)
    failed = []
    for idx, (q, ans) in enumerate(zip(questions, answers)):
        if q.get("is_warmup") or ans.get("correct"):
            continue
        topic = q.get("category_label") or q.get("category", "")
        picked, correct = _picked_and_correct_for_report(q, ans)
        failed.append(
            {
                "number": idx + 1,
                "topic": topic,
                "question": _question_text_for_report(q),
                "picked": picked,
                "correct": correct,
                "explanation": str(q.get("explanation", "")).strip(),
            }
        )

    _validate_report_consistency(questions, answers, base)

    narrative = _summary_narrative(student_name, base, mastery, errors)
    coaching_concepts = build_coaching_concepts(errors, student_name=student_name)

    # Group mastered skills by strategy name (not every level line).
    skills_mastered = [
        {"name": r["name"], "pct": r["pct"], "status": r["status"]}
        for r in mastery.get("mastered_strategies", [])
    ]
    skills_needing = [
        {"name": r["key"], "pct": r["pct"], "status": r["status"], "wrong": r["total"] - r["correct"]}
        for r in mastery.get("by_skill", [])
        if r["status"] != "Mastered"
    ]

    return {
        **base,
        "overall_status": mastery.get("overall_status", "Developing"),
        "summary_narrative": narrative,
        "mastery": mastery,
        "skills_mastered": skills_mastered,
        "skills_needing_practice": skills_needing,
        "error_analysis": errors,
        "mistake_patterns": errors.get("patterns", []),
        "recommendations": recommendations,
        "coaching_concepts": coaching_concepts,
        "failed_questions": failed,
        "program": program,
    }
