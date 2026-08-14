"""Practice report email — compatibility wrapper around ``practice_email`` package."""

from __future__ import annotations

from datetime import datetime

from practice_email.delivery import EmailSendResult, flush_pending, send_report
from practice_email.format import build_failed_questions, format_practice_report_email
from practice_email.settings import email_configured, load_settings

# Back-compat names used elsewhere
load_email_config = load_settings


def send_practice_report_email(
    *,
    student_name: str,
    unit_title: str,
    unit_subtitle: str,
    report: dict,
    time_spent_seconds: int,
    when: datetime | None = None,
    session_meta: dict | None = None,
    questions: list[dict] | None = None,
    answers: list[dict] | None = None,
) -> EmailSendResult:
    return send_report(
        student_name=student_name,
        unit_title=unit_title,
        unit_subtitle=unit_subtitle,
        report=report,
        time_spent_seconds=time_spent_seconds,
        when=when,
        session_meta=session_meta,
        questions=questions,
        answers=answers,
    )


def send_linear_equation_report_email(
    *,
    student_name: str,
    report: dict,
    time_spent_seconds: int,
    session_meta: dict,
    questions: list[dict] | None = None,
    answers: list[dict] | None = None,
    when: datetime | None = None,
) -> EmailSendResult:
    week = session_meta.get("week_label", "").strip()
    subtitle = week if week else "Weekly strategy practice"
    return send_practice_report_email(
        student_name=student_name,
        unit_title="Solving Linear Equations",
        unit_subtitle=subtitle,
        report=report,
        time_spent_seconds=time_spent_seconds,
        when=when,
        session_meta=session_meta,
        questions=questions,
        answers=answers,
    )


__all__ = [
    "EmailSendResult",
    "build_failed_questions",
    "email_configured",
    "flush_pending",
    "format_practice_report_email",
    "load_email_config",
    "send_linear_equation_report_email",
    "send_practice_report_email",
]
