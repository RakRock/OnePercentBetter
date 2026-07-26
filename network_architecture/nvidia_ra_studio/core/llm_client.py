"""Claude / Anthropic client for learning plans and agent coach."""

from __future__ import annotations

import json
import os
import re

try:
    import truststore

    truststore.inject_into_ssl()
except ImportError:
    pass

import httpx

DEFAULT_MODEL = os.environ.get("NVIDIA_RA_MODEL", os.environ.get("AI_FORGE_MODEL", "claude-sonnet-4-20250514"))
ANTHROPIC_MESSAGES_URL = "https://api.anthropic.com/v1/messages"


def get_anthropic_api_key(explicit: str | None = None) -> str | None:
    """
    Resolve Anthropic API key (same pattern as OnePercent AI Forge).

    Order: explicit arg → Streamlit secrets → ANTHROPIC_API_KEY / CLAUDE_API_KEY env
    (env is set from ~/.zshrc when you launch Streamlit from a login shell).
    """
    if explicit and explicit.strip():
        return explicit.strip()
    try:
        import streamlit as st

        if key := st.session_state.get("nra_anthropic_key"):
            if str(key).strip():
                return str(key).strip()
        try:
            secret = st.secrets.get("ANTHROPIC_API_KEY")
            if secret:
                return str(secret).strip()
        except Exception:
            pass
    except Exception:
        pass
    for env_name in ("ANTHROPIC_API_KEY", "CLAUDE_API_KEY"):
        if key := os.environ.get(env_name):
            if key.strip():
                return key.strip()
    return None


def llm_available(explicit: str | None = None) -> bool:
    return bool(get_anthropic_api_key(explicit))


def _post_messages(
    api_key: str,
    *,
    system: str,
    user: str,
    max_tokens: int = 2048,
    temperature: float = 0.4,
) -> str:
    resp = httpx.post(
        ANTHROPIC_MESSAGES_URL,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": DEFAULT_MODEL,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        },
        timeout=120.0,
    )
    resp.raise_for_status()
    data = resp.json()
    blocks = data.get("content", [])
    parts = [b.get("text", "") for b in blocks if b.get("type") == "text"]
    text = "".join(parts).strip()
    if not text:
        raise ValueError("Empty response from Claude")
    return text


def claude_chat(
    system: str,
    user: str,
    *,
    api_key: str | None = None,
    max_tokens: int = 2048,
    temperature: float = 0.4,
) -> str | None:
    key = get_anthropic_api_key(api_key)
    if not key:
        return None
    try:
        return _post_messages(
            key,
            system=system,
            user=user,
            max_tokens=max_tokens,
            temperature=temperature,
        )
    except httpx.HTTPStatusError as exc:
        raise RuntimeError(f"Claude API error ({exc.response.status_code})") from exc


def claude_json(
    system: str,
    user: str,
    *,
    api_key: str | None = None,
    max_tokens: int = 4096,
) -> dict | None:
    """Ask Claude for JSON; extracts first {...} block if wrapped in markdown."""
    raw = claude_chat(
        system + "\n\nRespond with valid JSON only. No markdown fences.",
        user,
        api_key=api_key,
        max_tokens=max_tokens,
        temperature=0.3,
    )
    if not raw:
        return None
    text = raw.strip()
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if fence:
        text = fence.group(1).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}")
        if start >= 0 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                return None
    return None
