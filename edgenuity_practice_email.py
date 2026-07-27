"""Email practice session reports (Edgenuity Course 3).

Configure in `.streamlit/secrets.toml` (or environment variables):

    PRACTICE_REPORT_EMAIL_TO = "you@example.com"
    SMTP_HOST = "smtp.gmail.com"
    SMTP_PORT = 587
    SMTP_USER = "you@example.com"
    SMTP_PASSWORD = "your-app-password"
    SMTP_FROM = "you@example.com"   # optional; defaults to SMTP_USER
    PRACTICE_REPORT_EMAIL_ENABLED = true   # optional; default true when TO is set
"""

from __future__ import annotations

import os
import smtplib
import ssl
from dataclasses import dataclass
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any


@dataclass
class EmailSendResult:
    ok: bool
    skipped: bool = False
    error: str = ""
    recipient: str = ""


def _secret(key: str, default: str = "") -> str:
    try:
        import streamlit as st

        val = st.secrets.get(key)
        if val is not None and str(val).strip():
            return str(val).strip()
    except Exception:
        pass
    return os.environ.get(key, default).strip()


def _secret_bool(key: str, default: bool) -> bool:
    raw = _secret(key, "")
    if not raw:
        return default
    return raw.lower() in ("1", "true", "yes", "on")


def email_configured() -> bool:
    cfg = load_email_config()
    return bool(
        cfg["enabled"]
        and cfg["recipient"]
        and cfg["smtp_host"]
        and cfg["smtp_user"]
        and cfg["smtp_password"]
    )


def load_email_config() -> dict[str, Any]:
    recipient = _secret("PRACTICE_REPORT_EMAIL_TO")
    enabled = _secret_bool("PRACTICE_REPORT_EMAIL_ENABLED", bool(recipient))
    smtp_user = _secret("SMTP_USER")
    return {
        "enabled": enabled,
        "recipient": recipient,
        "smtp_host": _secret("SMTP_HOST"),
        "smtp_port": int(_secret("SMTP_PORT", "587") or "587"),
        "smtp_user": smtp_user,
        "smtp_password": _secret("SMTP_PASSWORD"),
        "smtp_from": _secret("SMTP_FROM", smtp_user),
        "use_tls": _secret_bool("SMTP_USE_TLS", True),
    }


def format_practice_report_email(
    *,
    student_name: str,
    unit_title: str,
    unit_subtitle: str,
    report: dict,
    time_spent_seconds: int,
    when: datetime | None = None,
    session_meta: dict | None = None,
) -> tuple[str, str, str]:
    """Return (subject, plain_text, html)."""
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
    plain_parts.extend([
        "SUMMARY",
        "-------",
    ])
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

    plan_html = ""
    if session_meta and session_meta.get("plan_summary"):
        plan_items = "".join(
            f"<li>{line}</li>"
            for line in session_meta["plan_summary"].split("\n")
            if line.strip()
        )
        plan_html = f"""
      <h3 style="color:#6366f1;margin:1rem 0 0.3rem 0;">📋 Strategies &amp; Levels</h3>
      <ul style="margin:0.2rem 0 0 1rem;color:#374151;">{plan_items}</ul>
      """

    html = f"""
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
      {f'<p style="background:#eff6ff;border-left:4px solid #3b82f6;padding:0.75rem;margin-top:1rem;"><strong>Focus next:</strong> {tip}</p>' if tip else ""}
      <p style="color:#9ca3af;font-size:0.85rem;margin-top:1.5rem;">OnePercent Edgenuity Course 3</p>
    </div>
    """
    return subject, plain, html


def send_practice_report_email(
    *,
    student_name: str,
    unit_title: str,
    unit_subtitle: str,
    report: dict,
    time_spent_seconds: int,
    when: datetime | None = None,
    session_meta: dict | None = None,
) -> EmailSendResult:
    cfg = load_email_config()
    if not cfg["enabled"]:
        return EmailSendResult(ok=False, skipped=True, error="Email disabled")
    if not cfg["recipient"]:
        return EmailSendResult(ok=False, skipped=True, error="PRACTICE_REPORT_EMAIL_TO not set")
    if not cfg["smtp_host"] or not cfg["smtp_user"] or not cfg["smtp_password"]:
        return EmailSendResult(ok=False, skipped=True, error="SMTP not configured")

    subject, plain, html = format_practice_report_email(
        student_name=student_name,
        unit_title=unit_title,
        unit_subtitle=unit_subtitle,
        report=report,
        time_spent_seconds=time_spent_seconds,
        when=when,
        session_meta=session_meta,
    )

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = cfg["smtp_from"]
    msg["To"] = cfg["recipient"]
    msg.attach(MIMEText(plain, "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))

    try:
        with smtplib.SMTP(cfg["smtp_host"], cfg["smtp_port"], timeout=30) as server:
            if cfg["use_tls"]:
                server.starttls(context=ssl.create_default_context())
            server.login(cfg["smtp_user"], cfg["smtp_password"])
            server.sendmail(cfg["smtp_from"], [cfg["recipient"]], msg.as_string())
        return EmailSendResult(ok=True, recipient=cfg["recipient"])
    except Exception as exc:
        return EmailSendResult(ok=False, error=str(exc), recipient=cfg["recipient"])


def send_linear_equation_report_email(
    *,
    student_name: str,
    report: dict,
    time_spent_seconds: int,
    session_meta: dict,
    when: datetime | None = None,
) -> EmailSendResult:
    """Email for Solving Linear Equations tab (includes strategy/level plan)."""
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
    )

