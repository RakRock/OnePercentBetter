"""Send practice reports via Gmail API (HTTPS — works inside Streamlit)."""

from __future__ import annotations

import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import httpx

from practice_email.settings import EmailSettings

_TOKEN_URL = "https://oauth2.googleapis.com/token"
_SEND_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"


def _refresh_access_token(settings: EmailSettings) -> str:
    resp = httpx.post(
        _TOKEN_URL,
        data={
            "client_id": settings.gmail_client_id,
            "client_secret": settings.gmail_client_secret,
            "refresh_token": settings.gmail_refresh_token,
            "grant_type": "refresh_token",
        },
        timeout=30.0,
    )
    resp.raise_for_status()
    token = resp.json().get("access_token")
    if not token:
        raise RuntimeError("Gmail OAuth token refresh returned no access_token")
    return str(token)


def _build_raw_message(
    settings: EmailSettings,
    subject: str,
    plain: str,
    html: str,
    *,
    recipient: str | None = None,
) -> str:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.smtp_from or settings.smtp_user
    msg["To"] = recipient or settings.recipient
    msg.attach(MIMEText(plain, "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))
    return base64.urlsafe_b64encode(msg.as_bytes()).decode("ascii")


def send_gmail(
    settings: EmailSettings,
    subject: str,
    plain: str,
    html: str,
    *,
    recipient: str | None = None,
) -> None:
    """Send one report via Gmail API. Raises on failure."""
    if not settings.gmail_client_id or not settings.gmail_client_secret or not settings.gmail_refresh_token:
        raise RuntimeError("Gmail API OAuth not configured")
    token = _refresh_access_token(settings)
    raw = _build_raw_message(settings, subject, plain, html, recipient=recipient)
    resp = httpx.post(
        _SEND_URL,
        headers={"Authorization": f"Bearer {token}"},
        json={"raw": raw},
        timeout=30.0,
    )
    if resp.status_code >= 400:
        detail = resp.text.strip() or resp.reason_phrase
        raise RuntimeError(f"Gmail API send failed ({resp.status_code}): {detail}")
