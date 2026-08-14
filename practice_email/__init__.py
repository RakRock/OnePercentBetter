"""Practice report email — public API."""

from practice_email.delivery import EmailSendResult, flush_pending, send_report
from practice_email.format import build_failed_questions, format_practice_report_email
from practice_email.settings import email_configured, load_settings

__all__ = [
    "EmailSendResult",
    "build_failed_questions",
    "email_configured",
    "flush_pending",
    "format_practice_report_email",
    "load_settings",
    "send_report",
]
