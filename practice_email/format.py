"""Format practice report emails (subject, plain text, HTML)."""

from __future__ import annotations

import html as html_lib
from datetime import datetime


def _format_math_for_email_html(text: str) -> str:
    try:
        import harshit_math_render as hmr

        return hmr.format_math_display(text)
    except Exception:
        return html_lib.escape(str(text))


def _format_math_for_email_plain(text: str) -> str:
    try:
        import harshit_math_render as hmr

        return hmr.format_math_plain(text)
    except Exception:
        return str(text).strip()


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
        if q.get("is_warmup") or ans.get("correct"):
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


def _failed_from_report(report: dict, questions: list[dict] | None, answers: list[dict] | None) -> list[dict]:
    if report.get("failed_questions"):
        return report["failed_questions"]
    if questions and answers:
        return build_failed_questions(questions, answers)
    return []


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
    program_name: str = "Edgenuity Course 3",
    report_heading: str = "Edgenuity Practice Report",
) -> tuple[str, str, str]:
    when = when or datetime.now()
    date_str = when.strftime("%A, %B %d, %Y")
    time_str = when.strftime("%I:%M %p").lstrip("0")
    minutes, seconds = divmod(max(time_spent_seconds, 0), 60)
    cc = report.get("correct_count", 0)
    tot = report.get("total", 0)
    score_line = f"{cc:g}/{tot:g} ({report['score_pct']}%)"
    first_name = student_name.split()[0] if student_name.strip() else "Student"
    overall_status = report.get("overall_status", "Developing")
    narrative = report.get("summary_narrative") or (
        f"{first_name} completed {report['total']} questions and scored {score_line}."
    )

    subject = (
        f"{student_name} — {program_name} {unit_title} "
        f"({cc:g}/{tot:g}, {report['score_pct']}%)"
    )

    missed = failed_questions if failed_questions is not None else _failed_from_report(report, None, None)
    mastery = report.get("mastery") or {}
    patterns = report.get("mistake_patterns") or report.get("error_analysis", {}).get("patterns", [])
    coaching = report.get("coaching_concepts") or []
    rec = report.get("recommendations") or {}

    def _category_lines(items: list[dict]) -> list[str]:
        return [f"  • {i.get('emoji', '')} {i['name']} — {i['correct']}/{i['total']} ({i['pct']}%)" for i in items]

    strengths = report.get("strengths") or []
    revision = report.get("needs_revision") or []
    skills_mastered = report.get("skills_mastered") or mastery.get("mastered_strategies", [])
    skills_needing = report.get("skills_needing_practice") or []

    plain_parts = [
        narrative,
        "",
        "OVERALL PERFORMANCE",
        "-------------------",
        f"Score: {score_line}",
        f"Time: {minutes}m {seconds}s",
        f"Status: {overall_status}",
        "",
    ]

    if skills_mastered:
        plain_parts.append("SKILLS MASTERED")
        for s in skills_mastered:
            plain_parts.append(f"  • {s.get('name', s)} — {s.get('pct', 100)}%")
        plain_parts.append("")

    if skills_needing:
        plain_parts.append("SKILLS NEEDING PRACTICE")
        for s in skills_needing:
            plain_parts.append(f"  • {s.get('name', s.get('key', s))} — {s.get('pct', 0)}%")
        plain_parts.append("")
    elif revision:
        plain_parts.append("SKILLS NEEDING PRACTICE")
        plain_parts.extend(_category_lines(revision))
        plain_parts.append("")

    if patterns:
        plain_parts.append("WHAT WE LEARNED FROM THE MISTAKES")
        for p in patterns:
            plain_parts.append(f"  • {p.get('label', p.get('pattern', ''))} ({p.get('count', 1)}×)")
            if p.get("narrative"):
                plain_parts.append(f"    {p['narrative']}")
        plain_parts.append("")

    coaching = report.get("coaching_concepts") or []
    if coaching:
        plain_parts.append("GO OVER TOGETHER — KEY CONCEPTS TO REVIEW")
        plain_parts.append("-------------------------------------------")
        if coaching[0].get("intro"):
            plain_parts.append(coaching[0]["intro"])
            plain_parts.append("")
        for i, c in enumerate(coaching, start=1):
            plain_parts.append(f"{i}. {c['title']} ({c.get('mistake_count', 0)} missed question(s))")
            plain_parts.append(f"   Idea: {c['idea']}")
            plain_parts.append(f"   Rule: {c['rule']}")
            plain_parts.append(f"   Example: {_format_math_for_email_plain(c['example'])}")
            plain_parts.append(f"   Walk through: {c['walkthrough']}")
            plain_parts.append("")

    if rec.get("summary"):
        plain_parts.append("RECOMMENDED NEXT STEP")
        plain_parts.append(f"  {rec['summary']}")
        plain_parts.append("")

    if strengths:
        plain_parts.append("Topic breakdown — doing well:")
        plain_parts.extend(_category_lines(strengths))
        plain_parts.append("")

    if missed:
        plain_parts.append("DETAILED QUESTION REVIEW")
        plain_parts.append("-----------------------")
        for item in missed:
            topic = f" ({item['topic']})" if item.get("topic") else ""
            plain_parts.append(f"Q{item['number']}{topic}: {_format_math_for_email_plain(item['question'])}")
            plain_parts.append(f"  Your answer: {_format_math_for_email_plain(item['picked'])}")
            plain_parts.append(f"  Correct: {_format_math_for_email_plain(item['correct'])}")
            if item.get("explanation"):
                plain_parts.append(f"  Why: {_format_math_for_email_plain(item['explanation'])}")
            plain_parts.append("")

    plain_parts.append(f"— OnePercent {program_name}")
    plain = "\n".join(plain_parts)

    def _html_list(items: list[dict], color: str) -> str:
        if not items:
            return "<p><em>None this session.</em></p>"
        rows = "".join(
            f"<li><strong>{html_lib.escape(str(i.get('name', i.get('key', ''))))}</strong>"
            f" — {i.get('correct', '')}/{i.get('total', '')} ({i.get('pct', '')}%)</li>"
            for i in items
        )
        return f'<ul style="color:{color};margin:0.4rem 0 0 1rem;">{rows}</ul>'

    def _html_patterns(items: list[dict]) -> str:
        if not items:
            return ""
        blocks = []
        for p in items:
            nar = (
                f'<p style="margin:0.2rem 0 0 0;color:#4b5563;font-size:0.9rem;">{html_lib.escape(p.get("narrative", ""))}</p>'
                if p.get("narrative")
                else ""
            )
            blocks.append(
                f"<li><strong>{html_lib.escape(p.get('label', ''))}</strong> "
                f"({p.get('count', 1)} question{'s' if p.get('count', 1) != 1 else ''}){nar}</li>"
            )
        return (
            '<h3 style="color:#7c3aed;margin:1.1rem 0 0.3rem 0;">🔍 What we learned from the mistakes</h3>'
            f'<ul style="margin:0.2rem 0 0 1rem;color:#374151;">{"".join(blocks)}</ul>'
        )

    def _html_coaching(items: list[dict]) -> str:
        if not items:
            return ""
        intro = ""
        if items[0].get("intro"):
            intro = f'<p style="margin:0 0 0.75rem 0;color:#374151;line-height:1.5;">{html_lib.escape(items[0]["intro"])}</p>'
        blocks = []
        for i, c in enumerate(items, start=1):
            session_note = (
                ' <span style="color:#6b7280;font-size:0.85rem;">(from this session)</span>'
                if c.get("from_session")
                else ""
            )
            blocks.append(
                f"""
                <div style="background:#f5f3ff;border-left:4px solid #8b5cf6;padding:0.85rem 1rem;
                     border-radius:8px;margin-bottom:0.75rem;">
                  <p style="margin:0;font-weight:700;color:#5b21b6;">
                    {i}. {html_lib.escape(c["title"])}
                    <span style="font-weight:500;color:#7c3aed;">({c.get("mistake_count", 0)} missed)</span>
                  </p>
                  <p style="margin:0.4rem 0 0 0;color:#374151;"><strong>Idea:</strong> {html_lib.escape(c["idea"])}</p>
                  <p style="margin:0.25rem 0 0 0;color:#374151;"><strong>Rule:</strong> {html_lib.escape(c["rule"])}</p>
                  <p style="margin:0.35rem 0 0 0;color:#1f2937;"><strong>Example:</strong> {_format_math_for_email_html(c["example"])}{session_note}</p>
                  <p style="margin:0.35rem 0 0 0;color:#4b5563;font-size:0.92rem;"><strong>Walk through:</strong> {html_lib.escape(c["walkthrough"])}</p>
                </div>
                """
            )
        return (
            '<h3 style="color:#5b21b6;margin:1.1rem 0 0.3rem 0;">👨‍👩‍👧 Go over together — key concepts to review</h3>'
            + intro
            + "".join(blocks)
        )

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
                f'<strong>Why:</strong> {_format_math_for_email_html(item["explanation"])}</p>'
                if item.get("explanation")
                else ""
            )
            blocks.append(
                f"""
                <div style="background:#fef2f2;border-left:4px solid #ef4444;padding:0.75rem 0.9rem;
                     border-radius:8px;margin-bottom:0.65rem;">
                  <p style="margin:0;font-weight:700;color:#991b1b;">Q{item["number"]}{topic}</p>
                  <p style="margin:0.35rem 0 0 0;color:#1f2937;">{_format_math_for_email_html(item["question"])}</p>
                  <p style="margin:0.35rem 0 0 0;color:#991b1b;"><strong>Your answer:</strong> {_format_math_for_email_html(item["picked"])}</p>
                  <p style="margin:0.15rem 0 0 0;color:#047857;"><strong>Correct answer:</strong> {_format_math_for_email_html(item["correct"])}</p>
                  {expl}
                </div>
                """
            )
        return (
            '<h3 style="color:#ef4444;margin:1.25rem 0 0.3rem 0;">📋 Detailed question review</h3>'
            + "".join(blocks)
        )

    rec_html = ""
    if rec.get("summary"):
        rec_html = f"""
      <div style="background:#eff6ff;border-left:4px solid #3b82f6;padding:0.85rem 1rem;margin-top:1rem;border-radius:8px;">
        <strong>Recommended next step:</strong> {html_lib.escape(rec["summary"])}
      </div>
      """

    html_body = f"""
    <div style="font-family:sans-serif;max-width:560px;color:#1f2937;">
      <h2 style="color:#6366f1;margin:0 0 0.5rem 0;">{html_lib.escape(report_heading)}</h2>
      <p style="font-size:1.05rem;line-height:1.5;margin:0 0 1rem 0;">{html_lib.escape(narrative)}</p>
      <table style="border-collapse:collapse;margin-bottom:0.75rem;">
        <tr><td style="padding:4px 12px 4px 0;color:#6b7280;">Date</td><td><strong>{date_str}</strong> at {time_str}</td></tr>
        <tr><td style="padding:4px 12px 4px 0;color:#6b7280;">Student</td><td><strong>{html_lib.escape(student_name)}</strong></td></tr>
        <tr><td style="padding:4px 12px 4px 0;color:#6b7280;">Unit</td><td><strong>{html_lib.escape(unit_title)}</strong>{f" — {html_lib.escape(unit_subtitle)}" if unit_subtitle else ""}</td></tr>
        <tr><td style="padding:4px 12px 4px 0;color:#6b7280;">Score</td><td><strong>{score_line}</strong></td></tr>
        <tr><td style="padding:4px 12px 4px 0;color:#6b7280;">Time</td><td>{minutes}m {seconds}s</td></tr>
        <tr><td style="padding:4px 12px 4px 0;color:#6b7280;">Status</td><td><strong>{html_lib.escape(overall_status)}</strong></td></tr>
      </table>
      <h3 style="color:#10b981;margin:1rem 0 0.3rem 0;">✅ Skills mastered</h3>
      {_html_list(skills_mastered or strengths, "#047857")}
      <h3 style="color:#f59e0b;margin:1rem 0 0.3rem 0;">📚 Skills needing practice</h3>
      {_html_list(skills_needing or revision, "#b45309")}
      {_html_patterns(patterns)}
      {_html_coaching(coaching)}
      {rec_html}
      {_html_failed(missed)}
      <p style="color:#9ca3af;font-size:0.85rem;margin-top:1.5rem;">OnePercent {html_lib.escape(program_name)}</p>
    </div>
    """
    return subject, plain, html_body


def build_review_concepts_from_failures(
    failed: list[dict],
    *,
    needs_revision: list[dict] | None = None,
) -> list[dict]:
    """Group missed questions into student-facing topics with review tips."""
    by_topic: dict[str, dict] = {}
    for item in failed:
        topic = (item.get("topic") or "Practice").strip()
        bucket = by_topic.setdefault(
            topic,
            {"topic": topic, "count": 0, "tips": [], "examples": []},
        )
        bucket["count"] += 1
        expl = (item.get("explanation") or "").strip()
        if expl and expl not in bucket["tips"]:
            bucket["tips"].append(expl)
        q = (item.get("question") or "").strip()
        if q and len(bucket["examples"]) < 2:
            bucket["examples"].append(q)

    for rev in needs_revision or []:
        name = (rev.get("name") or "").strip()
        if not name or name in by_topic:
            continue
        missed_count = int(rev.get("total", 0)) - int(rev.get("correct", 0))
        if missed_count <= 0:
            continue
        by_topic[name] = {
            "topic": name,
            "count": missed_count,
            "tips": [rev.get("tip") or f"Review {name} and try similar problems."],
            "examples": [],
        }

    return sorted(by_topic.values(), key=lambda x: (-x["count"], x["topic"]))


def format_harshit_student_review_email(
    *,
    student_name: str,
    unit_title: str,
    unit_subtitle: str,
    report: dict,
    time_spent_seconds: int,
    when: datetime | None = None,
    failed_questions: list[dict] | None = None,
) -> tuple[str, str, str]:
    """Student-facing email: score plus concepts to review from missed questions."""
    when = when or datetime.now()
    date_str = when.strftime("%A, %B %d, %Y")
    minutes, seconds = divmod(max(time_spent_seconds, 0), 60)
    cc = report.get("correct_count", 0)
    tot = report.get("total", 0)
    score_line = f"{cc:g}/{tot:g} ({report['score_pct']}%)"
    first_name = student_name.split()[0] if student_name.strip() else "Student"

    missed = failed_questions if failed_questions is not None else _failed_from_report(report, None, None)
    concepts = build_review_concepts_from_failures(
        missed,
        needs_revision=report.get("needs_revision") or [],
    )

    subject = f"{first_name} — review from {unit_title} ({report['score_pct']}%)"

    plain_parts = [
        f"Hi {first_name},",
        "",
        f"You finished {unit_title}" + (f" ({unit_subtitle})" if unit_subtitle else "") + f" on {date_str}.",
        f"Score: {score_line} · Time: {minutes}m {seconds}s",
        "",
    ]

    if concepts:
        plain_parts.append("CONCEPTS TO REVIEW (from questions you missed)")
        plain_parts.append("----------------------------------------------")
        for i, c in enumerate(concepts, start=1):
            plain_parts.append(f"{i}. {c['topic']} — {c['count']} question(s) to revisit")
            for tip in c.get("tips") or []:
                plain_parts.append(f"   • {_format_math_for_email_plain(tip)}")
            for ex in c.get("examples") or []:
                plain_parts.append(f"   Example: {_format_math_for_email_plain(ex)}")
            plain_parts.append("")
        plain_parts.append("Try one similar problem for each topic, then explain your steps out loud.")
    else:
        plain_parts.append("Great session — no missed questions this time. Keep it up!")

    plain_parts.append("")
    plain_parts.append("— OnePercent Harshit Math")
    plain = "\n".join(plain_parts)

    if concepts:
        concept_blocks = []
        for i, c in enumerate(concepts, start=1):
            tips_html = "".join(
                f'<li style="margin:0.2rem 0;">{_format_math_for_email_html(t)}</li>'
                for t in (c.get("tips") or [])
            )
            examples_html = "".join(
                f'<p style="margin:0.25rem 0 0 0;color:#4b5563;font-size:0.9rem;">'
                f'<strong>Example:</strong> {_format_math_for_email_html(ex)}</p>'
                for ex in (c.get("examples") or [])
            )
            concept_blocks.append(
                f"""
                <div style="background:#fffbeb;border-left:4px solid #f59e0b;padding:0.85rem 1rem;
                     border-radius:8px;margin-bottom:0.75rem;">
                  <p style="margin:0;font-weight:700;color:#b45309;">
                    {i}. {html_lib.escape(c["topic"])}
                    <span style="font-weight:500;">({c["count"]} missed)</span>
                  </p>
                  <ul style="margin:0.35rem 0 0 1rem;color:#374151;padding:0;">{tips_html}</ul>
                  {examples_html}
                </div>
                """
            )
        review_section = (
            '<h3 style="color:#b45309;margin:1rem 0 0.3rem 0;">📚 Concepts to review</h3>'
            + "".join(concept_blocks)
            + '<p style="color:#374151;margin:0.75rem 0 0 0;">Try one similar problem for each topic, '
            "then explain your steps out loud.</p>"
        )
    else:
        review_section = (
            '<p style="background:#ecfdf5;border-left:4px solid #10b981;padding:0.85rem 1rem;'
            'border-radius:8px;color:#047857;margin:1rem 0 0 0;">'
            "Great session — no missed questions this time. Keep it up!</p>"
        )

    unit_line = html_lib.escape(unit_title)
    if unit_subtitle:
        unit_line += f" — {html_lib.escape(unit_subtitle)}"

    html_body = f"""
    <div style="font-family:sans-serif;max-width:560px;color:#1f2937;">
      <h2 style="color:#6366f1;margin:0 0 0.5rem 0;">Hi {html_lib.escape(first_name)} 👋</h2>
      <p style="line-height:1.5;margin:0 0 1rem 0;">
        You finished <strong>{unit_line}</strong> on {date_str}.
      </p>
      <table style="border-collapse:collapse;margin-bottom:0.5rem;">
        <tr><td style="padding:4px 12px 4px 0;color:#6b7280;">Score</td><td><strong>{score_line}</strong></td></tr>
        <tr><td style="padding:4px 12px 4px 0;color:#6b7280;">Time</td><td>{minutes}m {seconds}s</td></tr>
      </table>
      {review_section}
      <p style="color:#9ca3af;font-size:0.85rem;margin-top:1.5rem;">OnePercent Harshit Math</p>
    </div>
    """
    return subject, plain, html_body
