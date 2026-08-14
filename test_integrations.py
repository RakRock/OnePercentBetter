#!/usr/bin/env python3
"""Standalone smoke tests for SMTP email and Google Sheets (no Streamlit UI).

Reads config from `.streamlit/secrets.toml` and/or environment variables.

Usage:
    .venv/bin/python test_integrations.py           # run both tests
    .venv/bin/python test_integrations.py --email   # email only
    .venv/bin/python test_integrations.py --sheets  # sheets only
    .venv/bin/python test_integrations.py --sharepoint  # SharePoint only
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SECRETS_PATH = ROOT / ".streamlit" / "secrets.toml"


def _load_secrets_toml() -> dict:
    if not SECRETS_PATH.is_file():
        print(f"FAIL: missing {SECRETS_PATH}")
        sys.exit(1)
    try:
        import tomllib

        with SECRETS_PATH.open("rb") as f:
            return tomllib.load(f)
    except ImportError:
        import toml

        return toml.load(SECRETS_PATH)


class _SecretsView(dict):
    """Minimal stand-in for ``st.secrets`` used by app modules."""

    def get(self, key, default=None):
        return super().get(key, default)

    def __contains__(self, key):
        return key in self


def _apply_secrets(secrets: dict) -> None:
    """Patch Streamlit secrets + export env vars for CLI runs."""
    import streamlit as st

    st.secrets = _SecretsView(secrets)

    for key in (
        "GOOGLE_SHEETS_ENABLED",
        "GOOGLE_SHEET_ID",
        "PRACTICE_REPORT_EMAIL_ENABLED",
        "PRACTICE_REPORT_EMAIL_TO",
        "SMTP_HOST",
        "SMTP_PORT",
        "SMTP_USER",
        "SMTP_PASSWORD",
        "SMTP_PASS",
        "SMTP_FROM",
        "SMTP_USE_TLS",
        "PRACTICE_EMAIL_TRANSPORT",
        "GMAIL_CLIENT_ID",
        "GMAIL_CLIENT_SECRET",
        "GMAIL_REFRESH_TOKEN",
        "SHAREPOINT_ENABLED",
        "SHAREPOINT_SITE_URL",
        "SHAREPOINT_LIST_NAME",
    ):
        if key in secrets and secrets[key] is not None:
            os.environ.setdefault(key, str(secrets[key]))

    gcp = secrets.get("gcp_service_account")
    if isinstance(gcp, dict) and gcp:
        os.environ.setdefault("GOOGLE_SERVICE_ACCOUNT_JSON", json.dumps(gcp))

    azure = secrets.get("azure_app")
    if isinstance(azure, dict) and azure:
        os.environ.setdefault("AZURE_TENANT_ID", str(azure.get("tenant_id", "")))
        os.environ.setdefault("AZURE_CLIENT_ID", str(azure.get("client_id", "")))
        os.environ.setdefault("AZURE_CLIENT_SECRET", str(azure.get("client_secret", "")))


def _mask_email(addr: str) -> str:
    if "@" not in addr:
        return addr
    local, domain = addr.split("@", 1)
    if len(local) <= 2:
        return f"**@{domain}"
    return f"{local[:2]}...@{domain}"


def test_email() -> bool:
    from practice_email.delivery import send_report
    from practice_email.settings import email_configured, load_settings

    print("\n=== Practice email test ===")
    settings = load_settings()
    from practice_email.settings import gmail_api_configured, smtp_configured

    print(f"  enabled:     {settings.enabled}")
    print(f"  transport:   {settings.transport}")
    print(f"  recipient:   {_mask_email(settings.recipient)}")
    print(f"  gmail_api:   {gmail_api_configured(settings)}")
    print(f"  smtp:        {smtp_configured(settings)}")
    if smtp_configured(settings):
        print(f"  smtp_host:   {settings.smtp_host or '(empty)'}")
        print(f"  smtp_port:   {settings.smtp_port}")
        print(f"  smtp_user:   {_mask_email(settings.smtp_user)}")

    if not email_configured():
        print("FAIL: email not fully configured (check secrets.toml)")
        return False

    report = {
        "correct_count": 12,
        "total": 15,
        "score_pct": 80,
        "strengths": [{"emoji": "✅", "name": "Integration test", "correct": 3, "total": 3, "pct": 100}],
        "needs_revision": [],
        "tip": "This is a test row from test_integrations.py",
    }
    result = send_report(
        student_name="TestUser",
        unit_title="Integration Test",
        unit_subtitle="SMTP smoke test",
        report=report,
        time_spent_seconds=60,
        when=datetime.now(),
    )

    if result.ok:
        via = result.transport or "unknown"
        print(f"OK: email sent to {_mask_email(result.recipient)} via {via}")
        return True

    if result.pending:
        print(f"OK: email pending/background send to {_mask_email(result.recipient)}")
        return True

    if result.skipped:
        print(f"SKIP: {result.error}")
    else:
        print(f"FAIL: {result.error}")
    return False


def test_google_sheets() -> bool:
    import google_sheets_sync as gss

    print("\n=== Google Sheets test ===")
    print(f"  configured:  {gss.is_configured()}")
    if not gss.is_configured():
        print("FAIL: Google Sheets not configured (check secrets.toml)")
        return False

    session_id = f"test-{int(time.time())}"
    report = {
        "score_pct": 80,
        "correct_count": 12,
        "total": 15,
        "strengths": [],
        "needs_revision": [],
        "tip": "Integration test from test_integrations.py",
    }
    failed: list[dict] = []

    try:
        gss.append_practice_result(
            session_id=session_id,
            user_name="TestUser",
            session_kind="integration_test",
            unit_id=None,
            unit_label="Integration test",
            report=report,
            failed_questions=failed,
            time_spent_seconds=42,
            completed_at=datetime.now(),
        )
        print(f"OK: appended row session_id={session_id}")
        print(f"    worksheet: {gss.WORKSHEET_NAME}")
        return True
    except Exception as exc:
        print(f"FAIL: {type(exc).__name__}: {exc}")
        return False


def test_sharepoint() -> bool:
    import sharepoint_sync as sps

    print("\n=== SharePoint daily progress test ===")
    print(f"  configured:  {sps.is_configured()}")
    if not sps.is_configured():
        print("SKIP: SharePoint not configured (check secrets.toml)")
        return True

    sync_id = sps.new_sync_id("integration-test")
    today = datetime.now().strftime("%Y-%m-%d")
    try:
        sps.append_record(
            sync_id=sync_id,
            user_name="Arjun",
            record_type="activity",
            log_date=today,
            activity_type="IntegrationTest",
            activity_name="SharePoint smoke test",
            score=100,
            max_score=100,
            details="Written by test_integrations.py",
            time_spent_seconds=30,
            completed_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        rows = sps.fetch_all_records()
        print(f"OK: appended sync_id={sync_id}")
        print(f"    list name from secrets: configured")
        print(f"    total rows in list: {len(rows)}")
        return True
    except Exception as exc:
        print(f"FAIL: {type(exc).__name__}: {exc}")
        return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Test SMTP email and Google Sheets integrations.")
    parser.add_argument("--email", action="store_true", help="Run email test only")
    parser.add_argument("--sheets", action="store_true", help="Run Google Sheets test only")
    parser.add_argument("--sharepoint", action="store_true", help="Run SharePoint test only")
    args = parser.parse_args()

    any_flag = args.email or args.sheets or args.sharepoint
    run_email = args.email or not any_flag
    run_sheets = args.sheets or not any_flag
    run_sharepoint = args.sharepoint or not any_flag

    secrets = _load_secrets_toml()
    _apply_secrets(secrets)

    print(f"Using secrets: {SECRETS_PATH}")

    ok = True
    if run_email:
        ok = test_email() and ok
    if run_sheets:
        ok = test_google_sheets() and ok
    if run_sharepoint:
        ok = test_sharepoint() and ok

    print("\n=== Summary ===")
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
