"""Load email settings from secrets.toml and environment (no Streamlit)."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SECRETS_PATH = ROOT / ".streamlit" / "secrets.toml"


@dataclass(frozen=True)
class EmailSettings:
    enabled: bool
    recipient: str
    transport: str
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    smtp_from: str
    use_tls: bool
    gmail_client_id: str
    gmail_client_secret: str
    gmail_refresh_token: str


def _load_toml() -> dict:
    if not SECRETS_PATH.is_file():
        return {}
    try:
        import tomllib

        with SECRETS_PATH.open("rb") as f:
            return tomllib.load(f)
    except ImportError:
        import toml

        return toml.load(SECRETS_PATH)
    except Exception:
        return {}


def _get(toml: dict, key: str, default: str = "") -> str:
    if key in toml and toml[key] is not None and str(toml[key]).strip():
        return str(toml[key]).strip()
    return os.environ.get(key, default).strip()


def _bool_val(raw: str, default: bool) -> bool:
    if not raw:
        return default
    return raw.lower() in ("1", "true", "yes", "on")


def _gmail_oauth_field(toml: dict, field: str, env_key: str) -> str:
    block = toml.get("gmail_oauth")
    if isinstance(block, dict):
        val = block.get(field)
        if val is not None and str(val).strip():
            return str(val).strip()
    return _get(toml, env_key)


def load_settings() -> EmailSettings:
    toml = _load_toml()
    recipient = _get(toml, "PRACTICE_REPORT_EMAIL_TO")
    enabled = _bool_val(_get(toml, "PRACTICE_REPORT_EMAIL_ENABLED"), bool(recipient))
    smtp_user = _get(toml, "SMTP_USER")
    password = (_get(toml, "SMTP_PASSWORD") or _get(toml, "SMTP_PASS")).replace(" ", "")
    transport = _get(toml, "PRACTICE_EMAIL_TRANSPORT", "auto").lower() or "auto"
    return EmailSettings(
        enabled=enabled,
        recipient=recipient,
        transport=transport,
        smtp_host=_get(toml, "SMTP_HOST"),
        smtp_port=int(_get(toml, "SMTP_PORT", "587") or "587"),
        smtp_user=smtp_user,
        smtp_password=password,
        smtp_from=_get(toml, "SMTP_FROM", smtp_user),
        use_tls=_bool_val(_get(toml, "SMTP_USE_TLS"), True),
        gmail_client_id=_gmail_oauth_field(toml, "client_id", "GMAIL_CLIENT_ID"),
        gmail_client_secret=_gmail_oauth_field(toml, "client_secret", "GMAIL_CLIENT_SECRET"),
        gmail_refresh_token=_gmail_oauth_field(toml, "refresh_token", "GMAIL_REFRESH_TOKEN"),
    )


def gmail_api_configured(settings: EmailSettings | None = None) -> bool:
    s = settings or load_settings()
    return bool(s.gmail_client_id and s.gmail_client_secret and s.gmail_refresh_token)


def smtp_configured(settings: EmailSettings | None = None) -> bool:
    s = settings or load_settings()
    return bool(s.smtp_host and s.smtp_user and s.smtp_password)


def email_configured() -> bool:
    s = load_settings()
    if not s.enabled or not s.recipient:
        return False
    if s.transport == "gmail_api":
        return gmail_api_configured(s)
    if s.transport == "smtp":
        return smtp_configured(s)
    return gmail_api_configured(s) or smtp_configured(s)
