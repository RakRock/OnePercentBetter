"""Pick Gmail API (HTTPS) or SMTP and deliver in-process."""

from __future__ import annotations

from practice_email.gmail_client import send_gmail
from practice_email.settings import (
    EmailConfigError,
    EmailSettings,
    format_config_error,
    gmail_api_configured,
    in_streamlit_runtime,
    smtp_configured,
)
from practice_email.smtp_client import send_smtp


def deliver_now(settings: EmailSettings, subject: str, plain: str, html: str) -> str:
    """Send email now. Returns transport name used ('gmail_api' or 'smtp')."""
    mode = (settings.transport or "auto").lower()
    in_streamlit = in_streamlit_runtime()

    # Hosted Streamlit sandboxes often block outbound SMTP; HTTPS Gmail API is reliable.
    if in_streamlit and gmail_api_configured(settings) and mode in ("auto", "smtp"):
        send_gmail(settings, subject, plain, html)
        return "gmail_api"

    if mode == "gmail_api":
        if not gmail_api_configured(settings):
            raise EmailConfigError(format_config_error(settings, "gmail_api"))
        send_gmail(settings, subject, plain, html)
        return "gmail_api"

    if mode == "smtp":
        if not smtp_configured(settings):
            raise EmailConfigError(format_config_error(settings, "smtp"))
        send_smtp(settings, subject, plain, html)
        return "smtp"

    # auto — prefer Gmail API (HTTPS) when OAuth is complete
    if gmail_api_configured(settings):
        send_gmail(settings, subject, plain, html)
        return "gmail_api"
    if smtp_configured(settings):
        send_smtp(settings, subject, plain, html)
        return "smtp"

    raise EmailConfigError(format_config_error(settings, "auto"))
