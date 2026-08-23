"""SMTP delivery only — used by the standalone worker process."""

from __future__ import annotations

import smtplib
import socket
import ssl
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from practice_email.settings import (
    EmailSettings,
    EmailConfigError,
    assert_smtp_ready,
    format_delivery_error,
    validate_smtp_host,
)

_RETRIES = 3
_RETRY_DELAY = 1.5


def build_message(
    settings: EmailSettings,
    subject: str,
    plain: str,
    html: str,
    *,
    recipient: str | None = None,
) -> MIMEMultipart:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.smtp_from
    msg["To"] = recipient or settings.recipient
    msg.attach(MIMEText(plain, "plain", "utf-8"))
    msg.attach(MIMEText(html, "html", "utf-8"))
    return msg


def send_smtp(
    settings: EmailSettings,
    subject: str,
    plain: str,
    html: str,
    *,
    recipient: str | None = None,
) -> None:
    """Send one report email. Raises on failure."""
    assert_smtp_ready(settings)
    host_ok, host_msg = validate_smtp_host(settings.smtp_host)
    if not host_ok:
        raise EmailConfigError(host_msg)

    to_addr = recipient or settings.recipient
    msg = build_message(settings, subject, plain, html, recipient=to_addr)
    host = settings.smtp_host
    port = settings.smtp_port
    ctx = ssl.create_default_context()
    last_error: Exception | None = None

    for attempt in range(_RETRIES):
        try:
            try:
                socket.getaddrinfo(host, port, socket.AF_INET, socket.SOCK_STREAM)
            except OSError:
                socket.getaddrinfo(host, port, type=socket.SOCK_STREAM)
            with smtplib.SMTP(host, port, timeout=30) as server:
                if settings.use_tls:
                    server.starttls(context=ctx)
                server.login(settings.smtp_user, settings.smtp_password)
                server.sendmail(settings.smtp_from, [to_addr], msg.as_string())
            return
        except OSError as exc:
            last_error = exc
            if attempt + 1 < _RETRIES:
                time.sleep(_RETRY_DELAY)

    if settings.use_tls and port != 465:
        try:
            with smtplib.SMTP_SSL(host, 465, context=ctx, timeout=30) as server:
                server.login(settings.smtp_user, settings.smtp_password)
                server.sendmail(settings.smtp_from, [to_addr], msg.as_string())
            return
        except OSError as exc:
            last_error = exc

    assert last_error is not None
    raise RuntimeError(format_delivery_error(last_error, settings)) from last_error
