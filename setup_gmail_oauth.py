#!/usr/bin/env python3
"""One-time helper: obtain Gmail API refresh token for practice report emails."""

from __future__ import annotations

import json
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent
SECRETS_PATH = ROOT / ".streamlit" / "secrets.toml"
REDIRECT_URI = "http://127.0.0.1:8765/oauth/callback"
SCOPES = "https://www.googleapis.com/auth/gmail.send"


def _load_existing() -> dict[str, str]:
    if not SECRETS_PATH.is_file():
        return {}
    try:
        import tomllib

        data = tomllib.loads(SECRETS_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}
    block = data.get("gmail_oauth")
    return block if isinstance(block, dict) else {}


def _prompt(label: str, default: str = "") -> str:
    if default:
        val = input(f"{label} [{default}]: ").strip()
        return val or default
    return input(f"{label}: ").strip()


def main() -> None:
    print("Gmail API OAuth setup for OnePercent practice emails\n")
    existing = _load_existing()
    client_id = _prompt("OAuth client_id", existing.get("client_id", ""))
    client_secret = _prompt("OAuth client_secret", existing.get("client_secret", ""))
    if not client_id or not client_secret:
        raise SystemExit("client_id and client_secret are required.")

    params = {
        "client_id": client_id,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
        "access_type": "offline",
        "prompt": "consent",
    }
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)
    code_holder: dict[str, str] = {}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):  # noqa: N802
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path != "/oauth/callback":
                self.send_response(404)
                self.end_headers()
                return
            qs = urllib.parse.parse_qs(parsed.query)
            code = (qs.get("code") or [""])[0]
            code_holder["code"] = code
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(
                b"<html><body><h2>Authorization complete.</h2>"
                b"<p>You can close this tab and return to the terminal.</p></body></html>"
            )

        def log_message(self, format, *args):  # noqa: A003
            return

    print("\nOpening browser for Google sign-in...")
    print(f"If it does not open, visit:\n{auth_url}\n")
    webbrowser.open(auth_url)
    with HTTPServer(("127.0.0.1", 8765), Handler) as server:
        server.handle_request()

    code = code_holder.get("code", "").strip()
    if not code:
        raise SystemExit("No authorization code received.")

    token_resp = httpx.post(
        "https://oauth2.googleapis.com/token",
        data={
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": REDIRECT_URI,
            "grant_type": "authorization_code",
        },
        timeout=30.0,
    )
    token_resp.raise_for_status()
    tokens = token_resp.json()
    refresh = tokens.get("refresh_token")
    if not refresh:
        raise SystemExit(
            "No refresh_token returned. Revoke app access at "
            "https://myaccount.google.com/permissions and run again with prompt=consent."
        )

    block = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh,
    }
    print("\nAdd this block to .streamlit/secrets.toml (and Streamlit Cloud secrets):\n")
    print("[gmail_oauth]")
    for key, val in block.items():
        print(f'{key} = "{val}"')
    print("\nAlso set PRACTICE_EMAIL_TRANSPORT = \"auto\" (or \"gmail_api\").")
    print(f"\nFull JSON (optional backup):\n{json.dumps(block, indent=2)}")


if __name__ == "__main__":
    main()
