"""Pick Gmail API (HTTPS) or SMTP and deliver in-process."""

from __future__ import annotations

from practice_email.gmail_client import send_gmail
from practice_email.settings import EmailSettings, gmail_api_configured
from practice_email.smtp_client import send_smtp


def deliver_now(settings: EmailSettings, subject: str, plain: str, html: str) -> str:
    """Send email now. Returns transport name used ('gmail_api' or 'smtp')."""
    mode = (settings.transport or "auto").lower()
    if mode == "gmail_api" or (mode == "auto" and gmail_api_configured(settings)):
        send_gmail(settings, subject, plain, html)
        return "gmail_api"
    send_smtp(settings, subject, plain, html)
    return "smtp"
