"""Format practice report emails (subject, plain text, HTML)."""

from __future__ import annotations

import html as html_lib
from datetime import datetime


def _question_text(q: dict) -> str:
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


def _picked_and_correct(q: dict, ans: dict) -> tuple[str, str]:
    if "picked" in ans:
        return str(ans.get("picked", "?")), str(ans.get("correct_val", "?"))
    opts = q.get("options") or []
    choice = ans.get("choice")
    picked = opts[choice] if isinstance(choice, int) and 0 <= choice < len(opts) else "?"
    correct_idx = q.get("answer")
    correct = opts[correct_idx] if isinstance(correct_idx, int) and 0 <= correct_idx < len(opts) else "?"
    return str(picked), str(correct)


def build_failed_questions(questions: list[dict], answers: list[dict]) -> list[dict]:
    failed: list[dict] = []
    for idx, (q, ans) in enumerate(zip(questions, answers)):
        if ans.get("correct"):
            continue
        topic = q.get("category_label") or q.get("category", "")
        if topic and not q.get("category_label"):
            topic = str(topic).replace("_", " ").title()
        picked, correct = _picked_and_correct(q, ans)
        failed.append({
            "number": idx + 1,
            "topic": topic,
            "question": _question_text(q),
            "picked": picked,
            "correct": correct,
            "explanation": str(q.get("explanation", "")).strip(),
        })
    return failed


def format_practice_report_email(
    *,
    student_name: str,
    unit_title: str,
    unit_subtitle: str,
    report: dict,
    time_spent_seconds: int,
    when: datetime | None = None,
    session_meta: dict | None = None,
    failed_questions: list[dict] | None = None,
) -> tuple[str, str, str]:
    when = when or datetime.now()
    date_str = when.strftime("%A, %B %d, %Y")
    time_str = when.strftime("%I:%M %p").lstrip("0")
    minutes, seconds = divmod(max(time_spent_seconds, 0), 60)
    score_line = f"{report['correct_count']}/{report['total']} ({report['score_pct']}%)"

    subject = (
        f"{student_name} — Edgenuity {unit_title} Practice "
        f"({report['correct_count']}/{report['total']}, {report['score_pct']}%)"
    )

    def _lines(items: list[dict]) -> list[str]:
        return [f"  • {i['emoji']} {i['name']} — {i['correct']}/{i['total']} ({i['pct']}%)" for i in items]

    strengths = report.get("strengths") or []
    revision = report.get("needs_revision") or []
    tip = report.get("tip") or ""
    missed = failed_questions or []
    plan_lines: list[str] = []
    if session_meta:
        summary = session_meta.get("plan_summary", "").strip()
        if summary:
            plan_lines = ["STRATEGIES & LEVELS THIS SESSION", "--------------------------------"]
            plan_lines.extend(summary.split("\n"))
            plan_lines.append("")

    plain_parts = [
        f"Date: {date_str} at {time_str}",
        f"Student: {student_name}",
        f"Unit: {unit_title}" + (f" — {unit_subtitle}" if unit_subtitle else ""),
        f"Score: {score_line}",
        f"Time: {minutes}m {seconds}s",
        "",
    ]
    plain_parts.extend(plan_lines)
    plain_parts.extend(["SUMMARY", "-------"])
    if strengths:
        plain_parts.append("Doing well:")
        plain_parts.extend(_lines(strengths))
    else:
        plain_parts.append("Doing well: (no topic reached 80% this session)")
    plain_parts.append("")
    if revision:
        plain_parts.append("Needs revision:")
        plain_parts.extend(_lines(revision))
    else:
        plain_parts.append("Needs revision: none — great session!")
    if tip:
        plain_parts.extend(["", f"Focus next: {tip}"])
    if missed:
        plain_parts.extend(["", "MISSED QUESTIONS", "----------------"])
        for item in missed:
            topic = f" ({item['topic']})" if item.get("topic") else ""
            plain_parts.append(f"Q{item['number']}{topic}: {item['question']}")
            plain_parts.append(f"  Your answer: {item['picked']}")
            plain_parts.append(f"  Correct answer: {item['correct']}")
            if item.get("explanation"):
                plain_parts.append(f"  Why: {item['explanation']}")
            plain_parts.append("")
    plain_parts.extend(["", "— OnePercent Edgenuity Course 3"])
    plain = "\n".join(plain_parts)

    def _html_list(items: list[dict], color: str) -> str:
        if not items:
            return "<p><em>None this session.</em></p>"
        rows = "".join(
            f"<li><strong>{i['name']}</strong> — {i['correct']}/{i['total']} ({i['pct']}%)</li>"
            for i in items
        )
        return f'<ul style="color:{color};margin:0.4rem 0 0 1rem;">{rows}</ul>'

    def _html_failed(items: list[dict]) -> str:
        if not items:
            return ""
        blocks = []
        for item in items:
            topic = (
                f'<span style="color:#6b7280;font-size:0.85rem;"> — {html_lib.escape(item["topic"])}</span>'
                if item.get("topic")
                else ""
            )
            expl = (
                f'<p style="margin:0.35rem 0 0 0;color:#374151;font-size:0.9rem;">'
                f'<strong>Why:</strong> {html_lib.escape(item["explanation"])}</p>'
                if item.get("explanation")
                else ""
            )
            blocks.append(
                f"""
                <div style="background:#fef2f2;border-left:4px solid #ef4444;padding:0.75rem 0.9rem;
                     border-radius:8px;margin-bottom:0.65rem;">
                  <p style="margin:0;font-weight:700;color:#991b1b;">Q{item["number"]}{topic}</p>
                  <p style="margin:0.35rem 0 0 0;color:#1f2937;">{html_lib.escape(item["question"])}</p>
                  <p style="margin:0.35rem 0 0 0;color:#991b1b;"><strong>Your answer:</strong> {html_lib.escape(item["picked"])}</p>
                  <p style="margin:0.15rem 0 0 0;color:#047857;"><strong>Correct answer:</strong> {html_lib.escape(item["correct"])}</p>
                  {expl}
                </div>
                """
            )
        return (
            '<h3 style="color:#ef4444;margin:1.25rem 0 0.3rem 0;">❌ Missed questions</h3>'
            + "".join(blocks)
        )

    plan_html = ""
    if session_meta and session_meta.get("plan_summary"):
        plan_items = "".join(
            f"<li>{line}</li>" for line in session_meta["plan_summary"].split("\n") if line.strip()
        )
        plan_html = f"""
      <h3 style="color:#6366f1;margin:1rem 0 0.3rem 0;">📋 Strategies &amp; Levels</h3>
      <ul style="margin:0.2rem 0 0 1rem;color:#374151;">{plan_items}</ul>
      """

    html_body = f"""
    <div style="font-family:sans-serif;max-width:560px;color:#1f2937;">
      <h2 style="color:#6366f1;margin:0 0 0.5rem 0;">Edgenuity Practice Report</h2>
      <table style="border-collapse:collapse;margin-bottom:1rem;">
        <tr><td style="padding:4px 12px 4px 0;color:#6b7280;">Date</td><td><strong>{date_str}</strong> at {time_str}</td></tr>
        <tr><td style="padding:4px 12px 4px 0;color:#6b7280;">Student</td><td><strong>{student_name}</strong></td></tr>
        <tr><td style="padding:4px 12px 4px 0;color:#6b7280;">Unit</td><td><strong>{unit_title}</strong>{f" — {unit_subtitle}" if unit_subtitle else ""}</td></tr>
        <tr><td style="padding:4px 12px 4px 0;color:#6b7280;">Score</td><td><strong>{score_line}</strong></td></tr>
        <tr><td style="padding:4px 12px 4px 0;color:#6b7280;">Time</td><td>{minutes}m {seconds}s</td></tr>
      </table>
      {plan_html}
      <h3 style="color:#10b981;margin:1rem 0 0.3rem 0;">✅ Doing well</h3>
      {_html_list(strengths, "#047857")}
      <h3 style="color:#f59e0b;margin:1rem 0 0.3rem 0;">📚 Needs revision</h3>
      {_html_list(revision, "#b45309")}
      {_html_failed(missed)}
      {f'<p style="background:#eff6ff;border-left:4px solid #3b82f6;padding:0.75rem;margin-top:1rem;"><strong>Focus next:</strong> {html_lib.escape(tip)}</p>' if tip else ""}
      <p style="color:#9ca3af;font-size:0.85rem;margin-top:1.5rem;">OnePercent Edgenuity Course 3</p>
    </div>
    """
    return subject, plain, html_body
