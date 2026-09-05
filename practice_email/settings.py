"""Load email settings from secrets.toml, Streamlit secrets, and environment."""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SECRETS_PATH = ROOT / ".streamlit" / "secrets.toml"

# Practical hostname check — catches emails, URLs, and obvious typos before DNS.
_HOSTNAME_RE = re.compile(
    r"^(?=.{1,253}$)(?!-)[A-Za-z0-9-]{1,63}(?<!-)"
    r"(\.(?!-)[A-Za-z0-9-]{1,63}(?<!-))*\.?$"
)


class EmailConfigError(RuntimeError):
    """Non-retryable misconfiguration — fix secrets.toml before retrying."""


DEFAULT_HARSHIT_STUDENT_EMAIL = "harshitsai.rv@gmail.com"


@dataclass(frozen=True)
class EmailSettings:
    enabled: bool
    recipients: tuple[str, ...]
    harshit_student_email: str
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

    @property
    def recipient(self) -> str:
        """Primary recipient (first in list) — backward compatible."""
        return self.recipients[0] if self.recipients else ""


def parse_email_recipients(raw: str) -> list[str]:
    """Split comma/semicolon-separated addresses; dedupe case-insensitively."""
    if not raw:
        return []
    seen: set[str] = set()
    out: list[str] = []
    for part in re.split(r"[,;]+", raw):
        addr = part.strip()
        if not addr or "@" not in addr:
            continue
        key = addr.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(addr)
    return out


def merge_recipients(*groups: str) -> tuple[str, ...]:
    """Combine multiple recipient strings into one deduped tuple."""
    seen: set[str] = set()
    out: list[str] = []
    for group in groups:
        for addr in parse_email_recipients(group):
            key = addr.lower()
            if key in seen:
                continue
            seen.add(key)
            out.append(addr)
    return tuple(out)


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


def _streamlit_secret(key: str):
    try:
        import streamlit as st

        return st.secrets.get(key)
    except Exception:
        return None


def _streamlit_gmail_oauth() -> dict | None:
    try:
        import streamlit as st

        block = st.secrets.get("gmail_oauth")
        if isinstance(block, dict):
            return dict(block)
    except Exception:
        pass
    return None


# Values copied from secrets.toml.example — treated as "not configured".
_PLACEHOLDER_EXACT = frozenset(
    {
        "your-email@example.com",
        "your-app-password",
        "your-client-id",
        "your-client-secret",
        "your-refresh-token",
        "...",
        "....",
    }
)


def _is_placeholder(value: object) -> bool:
    """True when a secret value is empty or still an example/placeholder."""
    if value is None:
        return True
    s = str(value).strip()
    if not s:
        return True
    lower = s.lower()
    if lower in _PLACEHOLDER_EXACT:
        return True
    if lower.startswith("your-") or lower.startswith("your_"):
        return True
    if lower.endswith("@example.com"):
        return True
    if "...." in s and "googleusercontent.com" not in lower:
        return True
    return False


def _first_real_value(*candidates: object, default: str = "") -> str:
    """Return the first non-empty, non-placeholder candidate."""
    for val in candidates:
        if val is None:
            continue
        s = str(val).strip()
        if s and not _is_placeholder(s):
            return s
    return default.strip()


def _get(toml: dict, key: str, default: str = "") -> str:
    """Merge st.secrets, secrets.toml, and env — skip empty/placeholder overrides."""
    file_val = toml.get(key) if key in toml else None
    st_val = _streamlit_secret(key)
    if _is_placeholder(st_val):
        st_val = None
    return _first_real_value(st_val, file_val, os.environ.get(key), default=default)


def in_streamlit_runtime() -> bool:
    """True when code runs inside an active Streamlit script (not CLI/tests)."""
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        return get_script_run_ctx() is not None
    except Exception:
        return False


def _bool_val(raw: str, default: bool) -> bool:
    if not raw:
        return default
    return raw.lower() in ("1", "true", "yes", "on")


def _gmail_oauth_field(toml: dict, field: str, env_key: str) -> str:
    """Per-field merge: st.secrets [gmail_oauth] overrides file only when real."""
    st_block = _streamlit_gmail_oauth() or {}
    file_block = toml.get("gmail_oauth")
    file_val = file_block.get(field) if isinstance(file_block, dict) else None
    st_val = st_block.get(field) if isinstance(st_block, dict) else None
    return _first_real_value(st_val, file_val, os.environ.get(env_key))


def normalize_smtp_host(host: str) -> str:
    """Strip accidental scheme/path from SMTP_HOST values."""
    h = (host or "").strip()
    if "://" in h:
        h = h.split("://", 1)[1]
    if "/" in h:
        h = h.split("/", 1)[0]
    if ":" in h and not h.startswith("["):  # IPv6 bracket hosts keep ':'
        host_part, _, port_part = h.rpartition(":")
        if port_part.isdigit():
            h = host_part
    return h.strip()


def validate_smtp_host(host: str) -> tuple[bool, str]:
    """Return (ok, user-facing fix message)."""
    h = normalize_smtp_host(host)
    if not h:
        return False, (
            "SMTP_HOST is missing. In `.streamlit/secrets.toml` set "
            'SMTP_HOST = "smtp.gmail.com" (or use Gmail API — see below).'
        )
    if "@" in h:
        return False, (
            "SMTP_HOST looks like an email address, not a mail server. "
            'Use SMTP_HOST = "smtp.gmail.com" and put your address in SMTP_USER.'
        )
    if not _HOSTNAME_RE.match(h):
        return False, (
            f'SMTP_HOST "{h}" is not a valid hostname. '
            'For Gmail use SMTP_HOST = "smtp.gmail.com".'
        )
    return True, ""


def load_settings() -> EmailSettings:
    toml = _load_toml()
    recipient_to = _get(toml, "PRACTICE_REPORT_EMAIL_TO")
    recipient_cc = _get(toml, "PRACTICE_REPORT_EMAIL_CC")
    recipients = merge_recipients(recipient_to, recipient_cc)
    harshit_student = _get(toml, "HARSHIT_STUDENT_EMAIL", DEFAULT_HARSHIT_STUDENT_EMAIL)
    enabled = _bool_val(_get(toml, "PRACTICE_REPORT_EMAIL_ENABLED"), bool(recipients))
    smtp_user = _get(toml, "SMTP_USER")
    password = (_get(toml, "SMTP_PASSWORD") or _get(toml, "SMTP_PASS")).replace(" ", "")
    transport = _get(toml, "PRACTICE_EMAIL_TRANSPORT", "auto").lower() or "auto"
    smtp_host = normalize_smtp_host(_get(toml, "SMTP_HOST"))
    return EmailSettings(
        enabled=enabled,
        recipients=recipients,
        harshit_student_email=harshit_student,
        transport=transport,
        smtp_host=smtp_host,
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
    return bool(
        s.gmail_client_id
        and s.gmail_client_secret
        and s.gmail_refresh_token
        and not _is_placeholder(s.gmail_client_id)
        and not _is_placeholder(s.gmail_client_secret)
        and not _is_placeholder(s.gmail_refresh_token)
    )


def gmail_oauth_partial(settings: EmailSettings | None = None) -> bool:
    """True when OAuth client credentials exist but refresh token is missing."""
    s = settings or load_settings()
    has_client = bool(s.gmail_client_id and s.gmail_client_secret)
    return has_client and not s.gmail_refresh_token


def smtp_configured(settings: EmailSettings | None = None) -> bool:
    s = settings or load_settings()
    host_ok, _ = validate_smtp_host(s.smtp_host)
    return bool(
        host_ok
        and s.smtp_user
        and s.smtp_password
        and not _is_placeholder(s.smtp_user)
        and not _is_placeholder(s.smtp_password)
    )


def delivery_ready(settings: EmailSettings | None = None) -> tuple[bool, str, str]:
    """Same transport selection as deliver_now — (ready, transport, error)."""
    s = settings or load_settings()
    mode = (s.transport or "auto").lower()
    if in_streamlit_runtime() and gmail_api_configured(s) and mode in ("auto", "smtp"):
        return True, "gmail_api", ""
    if mode == "gmail_api":
        if gmail_api_configured(s):
            return True, "gmail_api", ""
        return False, "", format_config_error(s, "gmail_api")
    if mode == "smtp":
        if smtp_configured(s):
            return True, "smtp", ""
        return False, "", format_config_error(s, "smtp")
    if gmail_api_configured(s):
        return True, "gmail_api", ""
    if smtp_configured(s):
        return True, "smtp", ""
    return False, "", format_config_error(s, "auto")


def email_configured() -> bool:
    s = load_settings()
    if not s.enabled or not s.recipients:
        return False
    ready, _, _ = delivery_ready(s)
    return ready


def practice_email_enabled() -> bool:
    """Recipient wants reports — may still need OAuth/SMTP setup."""
    s = load_settings()
    return bool(s.enabled and s.recipients)


def format_config_error(settings: EmailSettings | None = None, mode: str | None = None) -> str:
    """Actionable message when email transport cannot be selected."""
    s = settings or load_settings()
    transport = (mode or s.transport or "auto").lower()
    lines: list[str] = []

    if transport in ("gmail_api", "auto") and not gmail_api_configured(s):
        if gmail_oauth_partial(s):
            lines.append(
                "Gmail OAuth is incomplete: add a refresh_token under [gmail_oauth] in "
                "`.streamlit/secrets.toml`. Run `.venv/bin/python setup_gmail_oauth.py` "
                "to generate one, then redeploy on Streamlit Cloud."
            )
        elif transport == "gmail_api":
            lines.append(
                "Gmail API is not configured. Add a [gmail_oauth] block with client_id, "
                "client_secret, and refresh_token to `.streamlit/secrets.toml`, or set "
                'PRACTICE_EMAIL_TRANSPORT = "smtp".'
            )

    if transport in ("smtp", "auto") and not smtp_configured(s):
        host_ok, host_msg = validate_smtp_host(s.smtp_host)
        if not host_ok:
            lines.append(host_msg)
        elif not s.smtp_user or not s.smtp_password:
            lines.append(
                "SMTP credentials are incomplete. Set SMTP_USER and SMTP_PASSWORD "
                "(Gmail app password) in `.streamlit/secrets.toml`."
            )

    if transport == "auto" and not lines:
        lines.append(
            "Email transport is set to auto but neither Gmail API nor SMTP is fully configured. "
            "Recommended: add [gmail_oauth] or set SMTP_USER + SMTP_PASSWORD in "
            "`.streamlit/secrets.toml`, then restart the app."
        )

    return " ".join(lines) if lines else "Email is not configured."


def format_delivery_error(exc: Exception, settings: EmailSettings | None = None) -> str:
    """Turn low-level send failures into secrets.toml fix instructions."""
    s = settings or load_settings()
    msg = str(exc).strip()
    lower = msg.lower()

    if "not configured" in lower or "oauth" in lower:
        return format_config_error(s)

    host_ok, host_msg = validate_smtp_host(s.smtp_host)
    if not host_ok:
        return host_msg

    if "nodename nor servname" in lower or "errno 8" in lower or "name or service not known" in lower:
        host = s.smtp_host or "(empty)"
        if gmail_api_configured(s):
            return (
                f"Could not resolve SMTP host \"{host}\" ([Errno 8]). "
                "Gmail OAuth is configured — set PRACTICE_EMAIL_TRANSPORT = \"gmail_api\" "
                "or \"auto\" in `.streamlit/secrets.toml` to use HTTPS instead of SMTP."
            )
        return (
            f"Could not resolve SMTP host \"{host}\" ([Errno 8]). "
            "Fix SMTP_HOST in `.streamlit/secrets.toml` (Gmail: \"smtp.gmail.com\"), "
            "or configure [gmail_oauth] and use PRACTICE_EMAIL_TRANSPORT = \"auto\"."
        )

    if "gmail api" in lower:
        return f"Gmail API send failed: {msg}. Re-run setup_gmail_oauth.py if the refresh token expired."

    return msg or "Email send failed."


def assert_smtp_ready(settings: EmailSettings) -> None:
    """Validate SMTP settings before opening a socket."""
    host_ok, host_msg = validate_smtp_host(settings.smtp_host)
    if not host_ok:
        raise EmailConfigError(host_msg)
    if not settings.smtp_user or not settings.smtp_password:
        raise EmailConfigError(format_config_error(settings, "smtp"))
