"""Shared xAI OpenAI-compatible client with reliable TLS on macOS."""

from __future__ import annotations

try:
    import truststore

    truststore.inject_into_ssl()
except ImportError:
    pass

from openai import OpenAI

XAI_BASE_URL = "https://api.x.ai/v1"
DEFAULT_TIMEOUT = 120.0


def make_xai_client(api_key: str, *, timeout: float = DEFAULT_TIMEOUT) -> OpenAI:
    """Return an OpenAI SDK client pointed at xAI.

    Uses the SDK default HTTP stack (truststore hooks SSL globally on macOS).
    Avoid a custom httpx client here — creating many short-lived clients under
    parallel load can trigger connection pool exhaustion and spurious errors.
    """
    return OpenAI(api_key=api_key, base_url=XAI_BASE_URL, timeout=timeout)
