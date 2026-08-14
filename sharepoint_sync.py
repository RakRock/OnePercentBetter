"""SharePoint daily progress sync via Microsoft Graph (SharePoint list).

On app start: import rows from the SharePoint list into local SQLite.
After login / activity: append a row to the list + save locally.

Secrets (``.streamlit/secrets.toml``):

    SHAREPOINT_ENABLED = true
    SHAREPOINT_SITE_URL = "https://yourtenant.sharepoint.com/sites/OnePercent"
    SHAREPOINT_LIST_NAME = "OnePercentDailyProgress"

    [azure_app]
    tenant_id = "your-azure-ad-tenant-id"
    client_id = "your-app-registration-client-id"
    client_secret = "your-client-secret"

Azure app registration (Application permissions, admin consent):
    - Sites.ReadWrite.All  OR  Sites.Selected (with site grant)

The list acts as your daily progress "sheet" in SharePoint (grid view / export to Excel).
"""

from __future__ import annotations

import json
import os
import re
import uuid
from datetime import datetime
from typing import Any
from urllib.parse import urlparse

import httpx

import database as db

GRAPH = "https://graph.microsoft.com/v1.0"
DEFAULT_LIST_NAME = "OnePercentDailyProgress"

LIST_COLUMNS: list[tuple[str, dict[str, Any]]] = [
    ("user_name", {"text": {}}),
    ("record_type", {"choice": {"choices": ["login", "activity", "reading", "edgenuity"]}}),
    ("log_date", {"text": {}}),
    ("activity_type", {"text": {}}),
    ("activity_name", {"text": {}}),
    ("score", {"number": {}}),
    ("max_score", {"number": {}}),
    ("details", {"text": {"allowMultipleLines": True}}),
    ("time_spent_seconds", {"number": {}}),
    ("completed_at", {"text": {}}),
    ("extra_json", {"text": {"allowMultipleLines": True}}),
]


def _secret(key: str, default: str = "") -> str:
    try:
        import streamlit as st

        val = st.secrets.get(key)
        if val is not None and str(val).strip():
            return str(val).strip()
    except Exception:
        pass
    return os.environ.get(key, default).strip()


def _secret_bool(key: str, default: bool = False) -> bool:
    raw = _secret(key, "")
    if not raw:
        return default
    return raw.lower() in ("1", "true", "yes", "on")


def _azure_app() -> dict[str, str] | None:
    try:
        import streamlit as st

        if "azure_app" in st.secrets:
            cfg = dict(st.secrets["azure_app"])
            if cfg.get("tenant_id") and cfg.get("client_id") and cfg.get("client_secret"):
                return {k: str(v).strip() for k, v in cfg.items()}
    except Exception:
        pass
    tenant = os.environ.get("AZURE_TENANT_ID", "").strip()
    client = os.environ.get("AZURE_CLIENT_ID", "").strip()
    secret = os.environ.get("AZURE_CLIENT_SECRET", "").strip()
    if tenant and client and secret:
        return {"tenant_id": tenant, "client_id": client, "client_secret": secret}
    return None


def is_configured() -> bool:
    if not _secret_bool("SHAREPOINT_ENABLED", False):
        return False
    return bool(_azure_app() and _secret("SHAREPOINT_SITE_URL"))


def _access_token() -> str:
    azure = _azure_app()
    if not azure:
        raise RuntimeError("Azure app credentials not configured")
    import msal

    app = msal.ConfidentialClientApplication(
        azure["client_id"],
        authority=f"https://login.microsoftonline.com/{azure['tenant_id']}",
        client_credential=azure["client_secret"],
    )
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if not result or "access_token" not in result:
        err = result.get("error_description") or result.get("error") or "token acquisition failed"
        raise RuntimeError(str(err))
    return str(result["access_token"])


def _client() -> httpx.Client:
    token = _access_token()
    return httpx.Client(
        base_url=GRAPH,
        headers={"Authorization": f"Bearer {token}"},
        timeout=60.0,
    )


def _site_path_from_url(site_url: str) -> str:
    parsed = urlparse(site_url.strip())
    if not parsed.hostname:
        raise ValueError(f"Invalid SHAREPOINT_SITE_URL: {site_url!r}")
    path = parsed.path.strip("/") or ""
    return f"{parsed.hostname}:/{path}"


def _get_site_id(client: httpx.Client) -> str:
    site_path = _site_path_from_url(_secret("SHAREPOINT_SITE_URL"))
    resp = client.get(f"/sites/{site_path}")
    resp.raise_for_status()
    return str(resp.json()["id"])


def _list_display_name() -> str:
    return _secret("SHAREPOINT_LIST_NAME", DEFAULT_LIST_NAME) or DEFAULT_LIST_NAME


def _find_list(client: httpx.Client, site_id: str, name: str) -> dict | None:
    safe = name.replace("'", "''")
    resp = client.get(f"/sites/{site_id}/lists", params={"$filter": f"displayName eq '{safe}'"})
    resp.raise_for_status()
    items = resp.json().get("value") or []
    return items[0] if items else None


def _ensure_columns(client: httpx.Client, site_id: str, list_id: str) -> None:
    resp = client.get(f"/sites/{site_id}/lists/{list_id}/columns")
    resp.raise_for_status()
    existing = {c.get("name") for c in resp.json().get("value") or []}
    for col_name, schema in LIST_COLUMNS:
        if col_name in existing:
            continue
        body = {"name": col_name, **schema}
        col_resp = client.post(f"/sites/{site_id}/lists/{list_id}/columns", json=body)
        if col_resp.status_code not in (200, 201):
            # Column may already exist under a different internal name
            continue


def _get_or_create_list(client: httpx.Client, site_id: str) -> str:
    name = _list_display_name()
    found = _find_list(client, site_id, name)
    if found:
        list_id = str(found["id"])
        _ensure_columns(client, site_id, list_id)
        return list_id

    resp = client.post(
        f"/sites/{site_id}/lists",
        json={"displayName": name, "list": {"template": "genericList"}},
    )
    resp.raise_for_status()
    list_id = str(resp.json()["id"])
    _ensure_columns(client, site_id, list_id)
    return list_id


def _list_item_exists(client: httpx.Client, site_id: str, list_id: str, sync_id: str) -> bool:
    safe = sync_id.replace("'", "''")
    resp = client.get(
        f"/sites/{site_id}/lists/{list_id}/items",
        params={"$filter": f"fields/Title eq '{safe}'", "$expand": "fields", "$top": 1},
    )
    resp.raise_for_status()
    return bool(resp.json().get("value"))


def append_record(
    *,
    sync_id: str,
    user_name: str,
    record_type: str,
    log_date: str,
    activity_type: str = "",
    activity_name: str = "",
    score: int | None = None,
    max_score: int | None = None,
    details: str = "",
    time_spent_seconds: int = 0,
    completed_at: str | None = None,
    extra_json: str = "{}",
) -> None:
    """Append one progress row to the SharePoint list (idempotent on sync_id)."""
    when = completed_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fields: dict[str, Any] = {
        "Title": sync_id,
        "user_name": user_name,
        "record_type": record_type,
        "log_date": log_date,
        "activity_type": activity_type or "",
        "activity_name": activity_name or "",
        "details": details or "",
        "time_spent_seconds": int(time_spent_seconds or 0),
        "completed_at": when,
        "extra_json": extra_json or "{}",
    }
    if score is not None:
        fields["score"] = int(score)
    if max_score is not None:
        fields["max_score"] = int(max_score)

    with _client() as client:
        site_id = _get_site_id(client)
        list_id = _get_or_create_list(client, site_id)
        if _list_item_exists(client, site_id, list_id, sync_id):
            return
        resp = client.post(
            f"/sites/{site_id}/lists/{list_id}/items",
            json={"fields": fields},
        )
        resp.raise_for_status()


def fetch_all_records() -> list[dict[str, Any]]:
    """Return all list rows as flat dicts (includes sync_id from Title)."""
    if not is_configured():
        return []

    rows: list[dict[str, Any]] = []
    with _client() as client:
        site_id = _get_site_id(client)
        list_id = _get_or_create_list(client, site_id)
        url: str | None = f"/sites/{site_id}/lists/{list_id}/items"
        params: dict[str, Any] | None = {"$expand": "fields", "$top": 200}

        while url:
            resp = client.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
            for item in data.get("value") or []:
                fields = dict(item.get("fields") or {})
                fields["sync_id"] = str(fields.get("Title") or "").strip()
                rows.append(fields)
            url = data.get("@odata.nextLink")
            params = None

    return rows


def sync_from_sharepoint_to_db() -> int:
    """Import SharePoint list rows missing from local SQLite."""
    if not is_configured():
        return 0

    imported = 0
    for rec in fetch_all_records():
        sync_id = str(rec.get("sync_id") or "").strip()
        if not sync_id:
            continue
        user_name = str(rec.get("user_name") or "").strip()
        user = db.get_user(user_name) if user_name else None
        if not user:
            continue

        record_type = str(rec.get("record_type") or "").strip().lower()
        log_date = str(rec.get("log_date") or "")[:10]
        if not log_date:
            continue

        if record_type == "login":
            if db.import_daily_login(user["id"], log_date):
                imported += 1
            continue

        if record_type == "activity":
            try:
                score = int(rec.get("score") or 0)
                max_score = int(rec.get("max_score") or 100)
                time_spent = int(rec.get("time_spent_seconds") or 0)
            except (TypeError, ValueError):
                continue
            if db.import_activity_score_row(
                sync_id=sync_id,
                user_id=user["id"],
                activity_type=str(rec.get("activity_type") or ""),
                activity_name=str(rec.get("activity_name") or ""),
                score=score,
                max_score=max_score,
                log_date=log_date,
                details=str(rec.get("details") or ""),
                time_spent_seconds=time_spent,
                completed_at=str(rec.get("completed_at") or ""),
            ):
                imported += 1
            continue

        if record_type == "reading":
            extra_raw = rec.get("extra_json") or "{}"
            try:
                extra = json.loads(extra_raw) if isinstance(extra_raw, str) else dict(extra_raw)
            except json.JSONDecodeError:
                extra = {}
            try:
                if db.import_reading_progress_row(
                    sync_id=sync_id,
                    user_id=user["id"],
                    story_id=str(extra.get("story_id") or ""),
                    story_title=str(extra.get("story_title") or rec.get("activity_name") or ""),
                    questions_total=int(extra.get("questions_total") or 0),
                    questions_correct=int(extra.get("questions_correct") or 0),
                    time_spent_seconds=int(rec.get("time_spent_seconds") or 0),
                    log_date=log_date,
                    completed_at=str(rec.get("completed_at") or ""),
                ):
                    imported += 1
            except (TypeError, ValueError):
                continue

    return imported


def _safe_push(fn, *args, **kwargs) -> tuple[bool, str | None]:
    if not is_configured():
        return False, None
    try:
        fn(*args, **kwargs)
        return True, None
    except Exception as exc:
        return False, str(exc)


def persist_daily_login(*, user_name: str, user_id: int, log_date: str) -> tuple[bool, str | None]:
    sync_id = f"login|{user_name}|{log_date}"
    return _safe_push(
        append_record,
        sync_id=sync_id,
        user_name=user_name,
        record_type="login",
        log_date=log_date,
    )


def persist_activity_score(
    *,
    sync_id: str,
    user_name: str,
    user_id: int,
    activity_type: str,
    activity_name: str,
    score: int,
    max_score: int,
    log_date: str,
    details: str,
    time_spent_seconds: int,
    completed_at: str,
) -> tuple[bool, str | None]:
    return _safe_push(
        append_record,
        sync_id=sync_id,
        user_name=user_name,
        record_type="activity",
        log_date=log_date,
        activity_type=activity_type,
        activity_name=activity_name,
        score=score,
        max_score=max_score,
        details=details,
        time_spent_seconds=time_spent_seconds,
        completed_at=completed_at,
    )


def persist_reading_progress(
    *,
    sync_id: str,
    user_name: str,
    user_id: int,
    story_id: str,
    story_title: str,
    questions_total: int,
    questions_correct: int,
    time_spent_seconds: int,
    log_date: str,
    completed_at: str,
) -> tuple[bool, str | None]:
    score_pct = int(100 * questions_correct / questions_total) if questions_total else 0
    extra = json.dumps(
        {
            "story_id": story_id,
            "story_title": story_title,
            "questions_total": questions_total,
            "questions_correct": questions_correct,
        },
        ensure_ascii=False,
    )
    return _safe_push(
        append_record,
        sync_id=sync_id,
        user_name=user_name,
        record_type="reading",
        log_date=log_date,
        activity_type="Reading",
        activity_name=story_title,
        score=score_pct,
        max_score=100,
        details=f"{questions_correct}/{questions_total} correct",
        time_spent_seconds=time_spent_seconds,
        completed_at=completed_at,
        extra_json=extra,
    )


def new_sync_id(prefix: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9_-]", "", prefix)[:24]
    return f"{safe}|{uuid.uuid4().hex[:12]}"
