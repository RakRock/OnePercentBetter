"""Practice report email — compatibility wrapper around ``practice_email`` package."""

from __future__ import annotations

from datetime import datetime

import streamlit as st

from practice_email.delivery import EmailSendResult, flush_pending, send_harshit_session_emails, send_report
from practice_email.format import build_failed_questions, format_practice_report_email
from practice_email.settings import (
    delivery_ready,
    email_configured,
    format_config_error,
    load_settings,
    practice_email_enabled,
)

# Back-compat names used elsewhere
load_email_config = load_settings


def email_status_message() -> str:
    """One-line status for practice home / setup panels (Arjun + Harshit)."""
    settings = load_settings()
    if not practice_email_enabled():
        return "Practice report email is disabled (set PRACTICE_REPORT_EMAIL_TO in secrets)."
    ready, transport, err = delivery_ready(settings)
    if ready:
        via = "Gmail API" if transport == "gmail_api" else "SMTP"
        dest = " + ".join(settings.recipients) if len(settings.recipients) > 1 else settings.recipient
        return f"Report email ready → {dest} via {via}"
    return err or format_config_error(settings)


def render_practice_email_result(result: EmailSendResult) -> None:
    """Shared UI feedback — same for Arjun Course 3, Edgenuity, Linear Eq, and Harshit."""
    if result.ok:
        st.success(f"📧 Report emailed to {result.recipient}")
        if result.error:
            st.warning(result.error)
        return
    if result.pending:
        st.warning(
            f"📧 Email queued for retry to {result.recipient}. "
            f"{result.error or 'Will retry automatically on next page load.'}"
        )
        return
    if result.skipped and result.error:
        st.warning(f"📧 Email not sent: {result.error}")
        return
    if result.error:
        st.warning(f"Could not send email: {result.error}")


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


def send_harshit_report_email(
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
    return send_harshit_session_emails(
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


def send_harshit_unit_test_report_email(
    *,
    student_name: str,
    unit_title: str,
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
        unit_subtitle="Unit Test — 25 min board format",
        report=report,
        time_spent_seconds=time_spent_seconds,
        when=when,
        session_meta=session_meta,
        questions=questions,
        answers=answers,
        program_name="Harshit Math",
        report_heading="Harshit Math Unit Test Report",
    )


def send_course3_report_email(
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
        program_name="Course 3 Math",
        report_heading="Course 3 Math Practice Report",
    )


__all__ = [
    "EmailSendResult",
    "build_failed_questions",
    "delivery_ready",
    "email_configured",
    "email_status_message",
    "flush_pending",
    "format_config_error",
    "format_practice_report_email",
    "load_email_config",
    "practice_email_enabled",
    "render_practice_email_result",
    "send_harshit_unit_test_report_email",
    "send_course3_report_email",
    "send_harshit_report_email",
    "send_linear_equation_report_email",
    "send_practice_report_email",
]
