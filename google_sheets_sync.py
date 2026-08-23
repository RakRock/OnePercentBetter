"""Google Sheets backup for Edgenuity practice results (Streamlit Cloud–friendly).

On app start: rows in the sheet are imported into local SQLite (if missing).
After each test: append one row to the sheet + save locally.

Secrets (``.streamlit/secrets.toml``):

    GOOGLE_SHEETS_ENABLED = true
    GOOGLE_SHEET_ID = "your-spreadsheet-id-from-url"

    [gcp_service_account]
    type = "service_account"
    project_id = "..."
    private_key_id = "..."
    private_key = "-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n"
    client_email = "...@....iam.gserviceaccount.com"
    client_id = "..."
    token_uri = "https://oauth2.googleapis.com/token"

Share the spreadsheet with ``client_email`` (Editor access).
"""

from __future__ import annotations

import json
import os
import re
import time
from datetime import datetime
from typing import Any, Callable, TypeVar

import database as db
from practice_quality.serialize import sanitize_report_for_storage

WORKSHEET_NAME = "EdgenuityPractice"
WEEK_PLAN_WORKSHEET = "LinearEqWeekPlan"
HARSHIT_PREREQ_PLAN_WORKSHEET = "HarshitPreReqWeekPlan"
HARSHIT_CONCEPT_PROGRESS_WORKSHEET = "HarshitConceptProgress"
HARSHIT_DAY_PROGRESS_WORKSHEET = "HarshitDayProgress"
HEADERS = [
    "session_id",
    "user_name",
    "session_kind",
    "unit_id",
    "unit_label",
    "score_pct",
    "correct_count",
    "total_count",
    "time_spent_seconds",
    "report_json",
    "failed_json",
    "completed_at",
    "log_date",
]
WEEK_PLAN_HEADERS = ["plan_id", "week_label", "config_json", "updated_at"]
HARSHIT_PREREQ_PLAN_HEADERS = ["prereq_id", "week_label", "config_json", "updated_at"]
HARSHIT_CONCEPT_PROGRESS_HEADERS = [
    "user_name",
    "module",
    "unit_id",
    "concept_id",
    "viewed",
    "marked_review",
    "simpler_requests",
    "example_requests",
    "updated_at",
]
HARSHIT_DAY_PROGRESS_HEADERS = [
    "user_name",
    "module",
    "unit_id",
    "day_id",
    "status",
    "concepts_viewed",
    "concepts_total",
    "updated_at",
]
WEEK_PLAN_ID = "1"
DAILY_LOGINS_WORKSHEET = "DailyLogins"
USER_STREAKS_WORKSHEET = "UserStreaks"
DAILY_SUMMARY_WORKSHEET = "UserDailySummary"
DAILY_LOGINS_HEADERS = ["user_name", "log_date", "logged_at"]
USER_STREAKS_HEADERS = ["user_name", "streak", "total_days", "updated_at"]
DAILY_SUMMARY_HEADERS = [
    "user_name",
    "log_date",
    "activities_count",
    "avg_score_pct",
    "time_spent_seconds",
    "updated_at",
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


def _service_account_info() -> dict[str, Any] | None:
    try:
        import streamlit as st

        if "gcp_service_account" in st.secrets:
            return dict(st.secrets["gcp_service_account"])
    except Exception:
        pass
    raw = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    if raw:
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return None
    return None


def is_configured() -> bool:
    if not _secret_bool("GOOGLE_SHEETS_ENABLED", False):
        return False
    return bool(_service_account_info() and _secret("GOOGLE_SHEET_ID"))


def cloud_sync_enabled() -> bool:
    """False when local dev opts out of blocking Google Sheets I/O."""
    if skip_cloud_sync():
        return False
    return is_configured()


def skip_cloud_sync() -> bool:
    """Skip Google Sheets / SharePoint sync (set SKIP_CLOUD_SYNC=true for fast local dev)."""
    if _secret_bool("SKIP_CLOUD_SYNC", False):
        return True
    if os.environ.get("SKIP_CLOUD_SYNC", "").strip().lower() in ("1", "true", "yes", "on"):
        return True
    return False


_spreadsheet_cache: dict[str, object] = {}
_HEADERS_VERIFIED: set[int] = set()

T = TypeVar("T")


def _retry_sheets_api(action: Callable[[], T], *, attempts: int = 4) -> T:
    """Retry Google Sheets calls when the per-minute read/write quota is hit."""
    delays = (1.0, 2.5, 6.0, 12.0)
    last_exc: Exception | None = None
    for attempt in range(min(attempts, len(delays))):
        try:
            return action()
        except Exception as exc:
            last_exc = exc
            msg = str(exc).lower()
            if "429" not in msg and "quota" not in msg:
                raise
            if attempt < min(attempts, len(delays)) - 1:
                time.sleep(delays[attempt])
    assert last_exc is not None
    raise last_exc


def _appended_row_index(resp: object, ws) -> int:
    """Parse the 1-based row number from an append_row response."""
    updated = ""
    if isinstance(resp, dict):
        updates = resp.get("updates") or {}
        updated = str(updates.get("updatedRange") or resp.get("updatedRange") or "")
    else:
        updated = str(getattr(resp, "updatedRange", "") or "")
    match = re.search(r"!A(\d+):", updated)
    if match:
        return int(match.group(1))
    return int(getattr(ws, "row_count", 1) or 1)


def _ensure_header_row(ws, headers: list[str], verified: set[int]) -> None:
    ws_id = int(getattr(ws, "id", id(ws)))
    if ws_id in verified:
        return

    def _check_and_fix() -> None:
        first = ws.row_values(1)
        if first != headers:
            ws.update(range_name="A1", values=[headers])

    _retry_sheets_api(_check_and_fix)
    verified.add(ws_id)


def _spreadsheet():
    """Reuse one gspread client + spreadsheet handle (avoids ~3s auth per call)."""
    sheet_id = _secret("GOOGLE_SHEET_ID")
    if not sheet_id:
        raise RuntimeError("GOOGLE_SHEET_ID not configured")
    cached = _spreadsheet_cache.get(sheet_id)
    if cached is not None:
        return cached

    import gspread
    from google.oauth2.service_account import Credentials

    info = _service_account_info()
    if not info:
        raise RuntimeError("Google Sheets service account not configured")

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_info(info, scopes=scopes)
    client = gspread.authorize(creds)
    _spreadsheet_cache[sheet_id] = client.open_by_key(sheet_id)
    return _spreadsheet_cache[sheet_id]


def _worksheet():
    import gspread

    spreadsheet = _spreadsheet()
    try:
        return spreadsheet.worksheet(WORKSHEET_NAME)
    except gspread.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(title=WORKSHEET_NAME, rows=1000, cols=len(HEADERS))
        ws.append_row(HEADERS, value_input_option="USER_ENTERED")
        return ws


def _week_plan_worksheet():
    import gspread

    spreadsheet = _spreadsheet()
    try:
        return spreadsheet.worksheet(WEEK_PLAN_WORKSHEET)
    except gspread.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(title=WEEK_PLAN_WORKSHEET, rows=10, cols=len(WEEK_PLAN_HEADERS))
        ws.append_row(WEEK_PLAN_HEADERS, value_input_option="USER_ENTERED")
        return ws


def _daily_logins_worksheet():
    import gspread

    spreadsheet = _spreadsheet()
    try:
        return spreadsheet.worksheet(DAILY_LOGINS_WORKSHEET)
    except gspread.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(
            title=DAILY_LOGINS_WORKSHEET, rows=500, cols=len(DAILY_LOGINS_HEADERS)
        )
        ws.append_row(DAILY_LOGINS_HEADERS, value_input_option="USER_ENTERED")
        return ws


def _user_streaks_worksheet():
    import gspread

    spreadsheet = _spreadsheet()
    try:
        return spreadsheet.worksheet(USER_STREAKS_WORKSHEET)
    except gspread.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(
            title=USER_STREAKS_WORKSHEET, rows=20, cols=len(USER_STREAKS_HEADERS)
        )
        ws.append_row(USER_STREAKS_HEADERS, value_input_option="USER_ENTERED")
        return ws


def _daily_summary_worksheet():
    import gspread

    spreadsheet = _spreadsheet()
    try:
        return spreadsheet.worksheet(DAILY_SUMMARY_WORKSHEET)
    except gspread.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(
            title=DAILY_SUMMARY_WORKSHEET, rows=500, cols=len(DAILY_SUMMARY_HEADERS)
        )
        ws.append_row(DAILY_SUMMARY_HEADERS, value_input_option="USER_ENTERED")
        return ws


def _ensure_headers(ws) -> None:
    _ensure_header_row(ws, HEADERS, _HEADERS_VERIFIED)


def _ensure_week_plan_headers(ws) -> None:
    _ensure_header_row(ws, WEEK_PLAN_HEADERS, _HEADERS_VERIFIED)


def _ensure_daily_logins_headers(ws) -> None:
    _ensure_header_row(ws, DAILY_LOGINS_HEADERS, _HEADERS_VERIFIED)


def _ensure_user_streaks_headers(ws) -> None:
    _ensure_header_row(ws, USER_STREAKS_HEADERS, _HEADERS_VERIFIED)


def _ensure_daily_summary_headers(ws) -> None:
    _ensure_header_row(ws, DAILY_SUMMARY_HEADERS, _HEADERS_VERIFIED)


def _login_push_key(user_id: int, log_date: str) -> str:
    return f"login:{user_id}:{log_date}"


def _summary_row_key(user_id: int, log_date: str) -> str:
    return f"summary_row:{user_id}:{log_date}"


def _streak_row_key(user_id: int) -> str:
    return f"streak_row:{user_id}"


def _sheet_has_daily_login(ws, user_name: str, log_date: str) -> bool:
    for row in ws.get_all_values()[1:]:
        if len(row) >= 2 and row[0].strip() == user_name and row[1].strip()[:10] == log_date:
            return True
    return False


def append_daily_login(user_name: str, log_date: str, *, user_id: int | None = None) -> None:
    """Append one login row if not already present (user + date unique)."""
    if user_id is None:
        user = db.get_user(user_name)
        user_id = user["id"] if user else None
    if user_id and db.gss_push_state_get(_login_push_key(user_id, log_date)):
        return

    ws = _daily_logins_worksheet()
    _ensure_daily_logins_headers(ws)
    when = datetime.now()
    row = [user_name, log_date, when.strftime("%Y-%m-%d %H:%M:%S")]

    def _append() -> None:
        ws.append_row(row, value_input_option="USER_ENTERED")

    _retry_sheets_api(_append)
    if user_id:
        db.gss_push_state_set(_login_push_key(user_id, log_date), "1")


def sync_daily_logins_from_sheet() -> int:
    """Import DailyLogins rows into SQLite. Returns rows inserted."""
    if not is_configured():
        return 0

    ws = _daily_logins_worksheet()
    _ensure_daily_logins_headers(ws)
    imported = 0
    for rec in ws.get_all_records():
        user_name = str(rec.get("user_name", "")).strip()
        log_date = str(rec.get("log_date", "")).strip()[:10]
        if not user_name or not log_date:
            continue
        user = db.get_user(user_name)
        if user and db.import_daily_login(user["id"], log_date):
            imported += 1
    return imported


def push_local_daily_logins_to_sheet() -> int:
    """Upload local login dates missing from the sheet."""
    if not is_configured():
        return 0

    pushed = 0
    for user in db.get_all_users():
        for log_date in db.get_user_log_dates(user["id"]):
            if db.gss_push_state_get(_login_push_key(user["id"], log_date)):
                continue
            append_daily_login(user["name"], log_date, user_id=user["id"])
            pushed += 1
    return pushed


def refresh_user_streaks_sheet() -> None:
    """Rewrite UserStreaks tab with computed streak and total days per user."""
    if not is_configured():
        return

    ws = _user_streaks_worksheet()
    _ensure_user_streaks_headers(ws)
    when = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rows = [USER_STREAKS_HEADERS]
    for user in db.get_all_users():
        rows.append(
            [
                user["name"],
                db.get_login_streak(user["id"]),
                db.get_total_login_days(user["id"]),
                when,
            ]
        )
    ws.update(range_name="A1", values=rows)


def _summary_row_index(ws, user_name: str, log_date: str) -> int | None:
    """1-based sheet row for user+date, or None."""
    for idx, row in enumerate(ws.get_all_values()[1:], start=2):
        if len(row) >= 2 and row[0].strip() == user_name and row[1].strip()[:10] == log_date:
            return idx
    return None


def upsert_daily_summary_row(
    user_name: str,
    log_date: str,
    *,
    activities_count: int,
    avg_score_pct: int,
    time_spent_seconds: int,
    user_id: int | None = None,
) -> None:
    """Upsert one user/day summary row in UserDailySummary."""
    if user_id is None:
        user = db.get_user(user_name)
        user_id = user["id"] if user else None

    ws = _daily_summary_worksheet()
    _ensure_daily_summary_headers(ws)
    when = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [
        user_name,
        log_date,
        int(activities_count),
        int(avg_score_pct),
        int(time_spent_seconds),
        when,
    ]
    row_key = _summary_row_key(user_id, log_date) if user_id else None
    stored = db.gss_push_state_get(row_key) if row_key else None
    target = int(stored) if stored else None

    def _write() -> None:
        nonlocal target
        if target:
            ws.update(range_name=f"A{target}:F{target}", values=[row])
            return
        resp = ws.append_row(row, value_input_option="USER_ENTERED")
        if row_key:
            target = _appended_row_index(resp, ws)
            db.gss_push_state_set(row_key, str(target))

    _retry_sheets_api(_write)


def refresh_user_daily_summary_sheet(log_date: str | None = None) -> None:
    """Push computed today stats for every user to UserDailySummary."""
    if not is_configured():
        return

    log_date = log_date or datetime.now().strftime("%Y-%m-%d")
    for user in db.get_all_users():
        stats = db.compute_user_daily_summary(user["id"], log_date)
        upsert_daily_summary_row(
            user["name"],
            log_date,
            activities_count=stats["activities_count"],
            avg_score_pct=stats["avg_score_pct"],
            time_spent_seconds=stats["time_spent_seconds"],
        )


def sync_daily_summaries_from_sheet() -> int:
    """Import UserDailySummary rows into SQLite daily_summaries cache."""
    if not is_configured():
        return 0

    ws = _daily_summary_worksheet()
    _ensure_daily_summary_headers(ws)
    imported = 0
    for rec in ws.get_all_records():
        user_name = str(rec.get("user_name", "")).strip()
        log_date = str(rec.get("log_date", "")).strip()[:10]
        if not user_name or not log_date:
            continue
        user = db.get_user(user_name)
        if not user:
            continue
        try:
            activities_count = int(rec.get("activities_count") or 0)
            avg_score_pct = int(rec.get("avg_score_pct") or 0)
            time_spent_seconds = int(rec.get("time_spent_seconds") or 0)
        except (TypeError, ValueError):
            continue
        db.import_daily_summary(
            user["id"],
            log_date,
            activities_count=activities_count,
            avg_score_pct=avg_score_pct,
            time_spent_seconds=time_spent_seconds,
            updated_at=str(rec.get("updated_at") or ""),
        )
        imported += 1
    return imported


def persist_daily_summary(*, user_id: int, log_date: str) -> tuple[bool, str | None]:
    """Upsert today's summary for one user after an activity completes."""
    return flush_user_session_to_sheets(user_id, log_date)


def upsert_user_streak_row(user_name: str, user_id: int) -> None:
    """Update one user's streak row without rewriting the whole tab."""
    ws = _user_streaks_worksheet()
    _ensure_user_streaks_headers(ws)
    when = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [
        user_name,
        db.get_login_streak(user_id),
        db.get_total_login_days(user_id),
        when,
    ]
    row_key = _streak_row_key(user_id)
    target = db.gss_push_state_get(row_key)
    target_idx = int(target) if target else None

    def _write() -> None:
        nonlocal target_idx
        if target_idx:
            ws.update(range_name=f"A{target_idx}:D{target_idx}", values=[row])
            return
        resp = ws.append_row(row, value_input_option="USER_ENTERED")
        target_idx = _appended_row_index(resp, ws)
        db.gss_push_state_set(row_key, str(target_idx))

    _retry_sheets_api(_write)


def flush_user_session_to_sheets(
    user_id: int,
    log_date: str | None = None,
) -> tuple[bool, str | None]:
    """One batched Google Sheets push after a practice/activity session completes."""
    if not cloud_sync_enabled():
        return False, None
    user = db.get_user_by_id(user_id)
    if not user:
        return False, "user not found"
    log_date = log_date or datetime.now().strftime("%Y-%m-%d")
    try:
        append_daily_login(user["name"], log_date, user_id=user_id)
        stats = db.compute_user_daily_summary(user_id, log_date)
        upsert_daily_summary_row(
            user["name"],
            log_date,
            activities_count=stats["activities_count"],
            avg_score_pct=stats["avg_score_pct"],
            time_spent_seconds=stats["time_spent_seconds"],
            user_id=user_id,
        )
        upsert_user_streak_row(user["name"], user_id)
        return True, None
    except Exception as exc:
        return False, str(exc)


def sync_streaks_and_logins() -> int:
    """Bidirectional login sync, daily summary sync, and refresh streak tab."""
    imported = sync_daily_logins_from_sheet()
    push_local_daily_logins_to_sheet()
    refresh_user_streaks_sheet()
    summary_imported = sync_daily_summaries_from_sheet()
    refresh_user_daily_summary_sheet()
    return imported + summary_imported


def persist_daily_login(*, user_name: str, user_id: int, log_date: str) -> tuple[bool, str | None]:
    """Append login + streak for one user (prefer flush_user_session_to_sheets)."""
    return flush_user_session_to_sheets(user_id, log_date)


def _week_plan_payload(
    week_label: str,
    strategies: list[dict],
    *,
    mental_math: list[dict] | None = None,
    mental_math_count: int = 5,
    use_llm: bool,
) -> dict:
    return {
        "week_label": week_label,
        "strategies": strategies,
        "mental_math": mental_math or [],
        "mental_math_count": max(0, min(15, int(mental_math_count))),
        "use_llm": use_llm,
    }


def save_week_plan_to_sheet(
    week_label: str,
    strategies: list[dict],
    *,
    mental_math: list[dict] | None = None,
    mental_math_count: int = 5,
    use_llm: bool = False,
) -> None:
    """Upsert the active linear-equations weekly plan (single row, plan_id=1)."""
    when = datetime.now()
    ws = _week_plan_worksheet()
    _ensure_week_plan_headers(ws)
    payload = _week_plan_payload(
        week_label,
        strategies,
        mental_math=mental_math,
        mental_math_count=mental_math_count,
        use_llm=use_llm,
    )
    row = [
        WEEK_PLAN_ID,
        week_label,
        json.dumps(payload, ensure_ascii=False),
        when.strftime("%Y-%m-%d %H:%M:%S"),
    ]
    values = ws.get_all_values()
    target_row = None
    for idx, existing in enumerate(values[1:], start=2):
        if existing and str(existing[0]).strip() == WEEK_PLAN_ID:
            target_row = idx
            break
    if target_row is None:
        ws.append_row(row, value_input_option="USER_ENTERED")
    else:
        ws.update(range_name=f"A{target_row}:D{target_row}", values=[row])


def _harshit_prereq_plan_worksheet():
    import gspread

    spreadsheet = _spreadsheet()
    try:
        return spreadsheet.worksheet(HARSHIT_PREREQ_PLAN_WORKSHEET)
    except gspread.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(
            title=HARSHIT_PREREQ_PLAN_WORKSHEET,
            rows=20,
            cols=len(HARSHIT_PREREQ_PLAN_HEADERS),
        )
        ws.append_row(HARSHIT_PREREQ_PLAN_HEADERS, value_input_option="USER_ENTERED")
        return ws


def save_harshit_prereq_week_plan(prereq_id: int, week_label: str, payload: dict) -> None:
    """Upsert weekly plan for one Harshit PreReq bucket."""
    when = datetime.now()
    ws = _harshit_prereq_plan_worksheet()
    first = ws.row_values(1)
    if first != HARSHIT_PREREQ_PLAN_HEADERS:
        ws.update(range_name="A1", values=[HARSHIT_PREREQ_PLAN_HEADERS])
    row = [
        str(prereq_id),
        week_label,
        json.dumps(payload, ensure_ascii=False),
        when.strftime("%Y-%m-%d %H:%M:%S"),
    ]
    values = ws.get_all_values()
    target_row = None
    pid_str = str(prereq_id)
    for idx, existing in enumerate(values[1:], start=2):
        if existing and str(existing[0]).strip() == pid_str:
            target_row = idx
            break
    if target_row is None:
        ws.append_row(row, value_input_option="USER_ENTERED")
    else:
        ws.update(range_name=f"A{target_row}:D{target_row}", values=[row])


def sync_harshit_prereq_plans_from_sheet() -> int:
    """Import Harshit PreReq week plans from Google Sheets. Returns count applied."""
    if not is_configured():
        return 0
    import database as db

    try:
        ws = _harshit_prereq_plan_worksheet()
    except Exception:
        return 0
    applied = 0
    for rec in ws.get_all_records():
        try:
            prereq_id = int(rec.get("prereq_id", 0))
        except (TypeError, ValueError):
            continue
        if prereq_id < 1 or prereq_id > 6:
            continue
        week_label = str(rec.get("week_label", "")).strip()
        raw = rec.get("config_json") or "{}"
        try:
            data = json.loads(raw) if isinstance(raw, str) else dict(raw)
        except (json.JSONDecodeError, TypeError):
            continue
        topics = data.get("topics") if isinstance(data.get("topics"), list) else []
        db.save_harshit_prereq_week_config(
            prereq_id,
            week_label,
            topics,
            warmup_count=int(data.get("warmup_count", 0)),
            use_llm=bool(data.get("use_llm", False)),
            use_chapter_llm=bool(data.get("use_chapter_llm", True)),
        )
        applied += 1
    return applied


def _harshit_concept_progress_worksheet():
    import gspread

    spreadsheet = _spreadsheet()
    try:
        return spreadsheet.worksheet(HARSHIT_CONCEPT_PROGRESS_WORKSHEET)
    except gspread.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(
            title=HARSHIT_CONCEPT_PROGRESS_WORKSHEET,
            rows=2000,
            cols=len(HARSHIT_CONCEPT_PROGRESS_HEADERS),
        )
        ws.append_row(HARSHIT_CONCEPT_PROGRESS_HEADERS, value_input_option="USER_ENTERED")
        return ws


def _harshit_day_progress_worksheet():
    import gspread

    spreadsheet = _spreadsheet()
    try:
        return spreadsheet.worksheet(HARSHIT_DAY_PROGRESS_WORKSHEET)
    except gspread.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(
            title=HARSHIT_DAY_PROGRESS_WORKSHEET,
            rows=500,
            cols=len(HARSHIT_DAY_PROGRESS_HEADERS),
        )
        ws.append_row(HARSHIT_DAY_PROGRESS_HEADERS, value_input_option="USER_ENTERED")
        return ws


def _harshit_concept_row_key(user_id: int, module: str, unit_id: int, concept_id: str) -> str:
    return f"harshit_concept:{user_id}:{module}:{unit_id}:{concept_id}"


def _harshit_day_row_key(user_id: int, module: str, unit_id: int, day_id: int) -> str:
    return f"harshit_day:{user_id}:{module}:{unit_id}:{day_id}"


def _find_harshit_sheet_row(
    ws,
    *,
    user_name: str,
    module: str,
    unit_id: int,
    key_val: str,
) -> int | None:
    """Return 1-based row index matching user/module/unit/key, or None."""
    values = ws.get_all_values()
    module = module.strip().lower()
    unit_str = str(unit_id)
    for idx, row in enumerate(values[1:], start=2):
        if len(row) < 4:
            continue
        if (
            row[0].strip() == user_name
            and row[1].strip().lower() == module
            and str(row[2]).strip() == unit_str
            and str(row[3]).strip() == key_val
        ):
            return idx
    return None


def upsert_harshit_concept_progress(
    user_name: str,
    user_id: int,
    module: str,
    unit_id: int,
    concept_id: str,
    *,
    viewed: int,
    marked_review: int,
    simpler_requests: int,
    example_requests: int,
    updated_at: str = "",
) -> None:
    """Upsert one Harshit concept progress row to Google Sheets."""
    if not cloud_sync_enabled():
        return
    when = updated_at.strip() or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ws = _harshit_concept_progress_worksheet()
    _ensure_header_row(ws, HARSHIT_CONCEPT_PROGRESS_HEADERS, _HEADERS_VERIFIED)
    row = [
        user_name,
        module,
        str(unit_id),
        concept_id,
        str(int(viewed)),
        str(int(marked_review)),
        str(int(simpler_requests)),
        str(int(example_requests)),
        when,
    ]
    row_key = _harshit_concept_row_key(user_id, module, unit_id, concept_id)
    target_idx = db.gss_push_state_get(row_key)
    target_row = int(target_idx) if target_idx and target_idx.isdigit() else None
    if target_row is None:
        target_row = _find_harshit_sheet_row(
            ws,
            user_name=user_name,
            module=module,
            unit_id=unit_id,
            key_val=concept_id,
        )

    def _write() -> None:
        nonlocal target_row
        ncols = len(HARSHIT_CONCEPT_PROGRESS_HEADERS)
        col_end = chr(ord("A") + ncols - 1)
        if target_row:
            ws.update(range_name=f"A{target_row}:{col_end}{target_row}", values=[row])
        else:
            resp = ws.append_row(row, value_input_option="USER_ENTERED")
            target_row = _appended_row_index(resp, ws)
        db.gss_push_state_set(row_key, str(target_row))

    _retry_sheets_api(_write)


def upsert_harshit_day_progress(
    user_name: str,
    user_id: int,
    module: str,
    unit_id: int,
    day_id: int,
    *,
    status: str,
    concepts_viewed: int,
    concepts_total: int,
    updated_at: str = "",
) -> None:
    """Upsert one Harshit day progress row to Google Sheets."""
    if not cloud_sync_enabled():
        return
    when = updated_at.strip() or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ws = _harshit_day_progress_worksheet()
    _ensure_header_row(ws, HARSHIT_DAY_PROGRESS_HEADERS, _HEADERS_VERIFIED)
    row = [
        user_name,
        module,
        str(unit_id),
        str(day_id),
        status,
        str(int(concepts_viewed)),
        str(int(concepts_total)),
        when,
    ]
    row_key = _harshit_day_row_key(user_id, module, unit_id, day_id)
    target_idx = db.gss_push_state_get(row_key)
    target_row = int(target_idx) if target_idx and target_idx.isdigit() else None
    if target_row is None:
        target_row = _find_harshit_sheet_row(
            ws,
            user_name=user_name,
            module=module,
            unit_id=unit_id,
            key_val=str(day_id),
        )

    def _write() -> None:
        nonlocal target_row
        ncols = len(HARSHIT_DAY_PROGRESS_HEADERS)
        col_end = chr(ord("A") + ncols - 1)
        if target_row:
            ws.update(range_name=f"A{target_row}:{col_end}{target_row}", values=[row])
        else:
            resp = ws.append_row(row, value_input_option="USER_ENTERED")
            target_row = _appended_row_index(resp, ws)
        db.gss_push_state_set(row_key, str(target_row))

    _retry_sheets_api(_write)


def sync_harshit_concept_progress_from_sheet() -> int:
    """Import Harshit Physics/Chemistry concept progress from Google Sheets."""
    if not is_configured():
        return 0
    try:
        ws = _harshit_concept_progress_worksheet()
    except Exception:
        return 0
    applied = 0
    for rec in ws.get_all_records():
        user_name = str(rec.get("user_name", "")).strip()
        module = str(rec.get("module", "")).strip().lower()
        if module not in ("physics", "chemistry"):
            continue
        user = db.get_user(user_name) if user_name else None
        if not user:
            continue
        concept_id = str(rec.get("concept_id", "")).strip()
        if not concept_id:
            continue
        try:
            unit_id = int(rec.get("unit_id", 0))
            viewed = int(rec.get("viewed", 0) or 0)
            marked_review = int(rec.get("marked_review", 0) or 0)
            simpler_requests = int(rec.get("simpler_requests", 0) or 0)
            example_requests = int(rec.get("example_requests", 0) or 0)
        except (TypeError, ValueError):
            continue
        if unit_id < 1:
            continue
        db.merge_harshit_concept_progress_from_sheet(
            user["id"],
            module=module,
            unit_id=unit_id,
            concept_id=concept_id,
            viewed=viewed,
            marked_review=marked_review,
            simpler_requests=simpler_requests,
            example_requests=example_requests,
        )
        applied += 1
    return applied


def sync_harshit_day_progress_from_sheet() -> int:
    """Import Harshit Physics/Chemistry day progress from Google Sheets."""
    if not is_configured():
        return 0
    try:
        ws = _harshit_day_progress_worksheet()
    except Exception:
        return 0
    applied = 0
    for rec in ws.get_all_records():
        user_name = str(rec.get("user_name", "")).strip()
        module = str(rec.get("module", "")).strip().lower()
        if module not in ("physics", "chemistry"):
            continue
        user = db.get_user(user_name) if user_name else None
        if not user:
            continue
        try:
            unit_id = int(rec.get("unit_id", 0))
            day_id = int(rec.get("day_id", 0))
            concepts_viewed = int(rec.get("concepts_viewed", 0) or 0)
            concepts_total = int(rec.get("concepts_total", 0) or 0)
        except (TypeError, ValueError):
            continue
        if unit_id < 1 or day_id < 1:
            continue
        status = str(rec.get("status", "not_started") or "not_started").strip()
        db.merge_harshit_day_progress_from_sheet(
            user["id"],
            module=module,
            unit_id=unit_id,
            day_id=day_id,
            status=status,
            concepts_viewed=concepts_viewed,
            concepts_total=concepts_total,
        )
        applied += 1
    return applied


def sync_week_plan_from_sheet() -> bool:
    """Import weekly plan from Google Sheets into SQLite. Returns True if applied."""
    if not is_configured():
        return False

    ws = _week_plan_worksheet()
    _ensure_week_plan_headers(ws)
    for rec in ws.get_all_records():
        if str(rec.get("plan_id", "")).strip() != WEEK_PLAN_ID:
            continue
        week_label = str(rec.get("week_label", "")).strip()
        config_json = rec.get("config_json") or "{}"
        if isinstance(config_json, dict):
            data = config_json
        else:
            try:
                data = json.loads(str(config_json))
            except json.JSONDecodeError:
                continue
        if not isinstance(data, dict):
            continue
        strategies = data.get("strategies")
        if not isinstance(strategies, list):
            strategies = []
        mental_math = data.get("mental_math")
        if not isinstance(mental_math, list):
            mental_math = []
        raw_mm_count = data.get("mental_math_count", 5)
        try:
            mental_math_count = max(0, min(15, int(raw_mm_count)))
        except (TypeError, ValueError):
            mental_math_count = 5
        if not week_label and not strategies and not mental_math:
            continue
        db.import_linear_eq_week_config(
            week_label or str(data.get("week_label", "")).strip(),
            strategies,
            mental_math=mental_math,
            mental_math_count=mental_math_count,
            use_llm=bool(data.get("use_llm", False)),
        )
        return True
    return False


def persist_week_plan(
    week_label: str,
    strategies: list[dict],
    *,
    mental_math: list[dict] | None = None,
    mental_math_count: int = 5,
    use_llm: bool = False,
) -> tuple[bool, str | None]:
    """Save weekly plan to Google Sheets. Returns (sheet_ok, error_message)."""
    if not is_configured():
        return False, None
    try:
        save_week_plan_to_sheet(
            week_label,
            strategies,
            mental_math=mental_math,
            mental_math_count=mental_math_count,
            use_llm=use_llm,
        )
        return True, None
    except Exception as exc:
        return False, str(exc)


def append_practice_result(
    *,
    session_id: str,
    user_name: str,
    session_kind: str,
    unit_id: int | None,
    unit_label: str,
    report: dict,
    failed_questions: list[dict],
    time_spent_seconds: int,
    completed_at: datetime | None = None,
) -> None:
    """Append one practice session row to Google Sheets."""
    when = completed_at or datetime.now()
    ws = _worksheet()
    _ensure_headers(ws)

    row = [
        session_id,
        user_name,
        session_kind,
        "" if unit_id is None else str(unit_id),
        unit_label,
        int(report.get("score_pct", 0)),
        int(report.get("correct_count", 0)),
        int(report.get("total", 0)),
        time_spent_seconds,
        json.dumps(report, ensure_ascii=False),
        json.dumps(failed_questions, ensure_ascii=False),
        when.strftime("%Y-%m-%d %H:%M:%S"),
        when.strftime("%Y-%m-%d"),
    ]

    def _append() -> None:
        ws.append_row(row, value_input_option="USER_ENTERED")

    _retry_sheets_api(_append)


def sync_from_sheet_to_db() -> int:
    """Import sheet rows missing from local SQLite. Returns rows imported."""
    if not is_configured():
        return 0

    ws = _worksheet()
    _ensure_headers(ws)
    records = ws.get_all_records()
    imported = 0

    for rec in records:
        session_id = str(rec.get("session_id", "")).strip()
        if not session_id:
            continue
        user_name = str(rec.get("user_name", "")).strip()
        user = db.get_user(user_name) if user_name else None
        if not user:
            continue

        unit_raw = str(rec.get("unit_id", "")).strip()
        unit_id = int(unit_raw) if unit_raw.isdigit() else None

        try:
            score_pct = int(rec.get("score_pct", 0))
            correct_count = int(rec.get("correct_count", 0))
            total_count = int(rec.get("total_count", 0))
            time_spent = int(rec.get("time_spent_seconds", 0) or 0)
        except (TypeError, ValueError):
            continue

        report_json = rec.get("report_json") or "{}"
        failed_json = rec.get("failed_json") or "[]"
        if isinstance(report_json, dict):
            report_json = json.dumps(report_json)
        if isinstance(failed_json, list):
            failed_json = json.dumps(failed_json)

        completed_at = str(rec.get("completed_at") or datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        log_date = str(rec.get("log_date") or completed_at[:10])

        if db.import_ec3_practice_result_row(
            session_id=session_id,
            user_id=user["id"],
            session_kind=str(rec.get("session_kind") or "unit"),
            unit_id=unit_id,
            unit_label=str(rec.get("unit_label") or ""),
            score_pct=score_pct,
            correct_count=correct_count,
            total_count=total_count,
            time_spent_seconds=time_spent,
            report_json=str(report_json),
            failed_json=str(failed_json),
            completed_at=completed_at,
            log_date=log_date,
        ):
            imported += 1

    sync_week_plan_from_sheet()
    sync_harshit_prereq_plans_from_sheet()
    concept_rows = sync_harshit_concept_progress_from_sheet()
    day_rows = sync_harshit_day_progress_from_sheet()
    return imported + concept_rows + day_rows


def persist_edgenuity_practice(
    *,
    user_name: str,
    user_id: int,
    session_id: str,
    session_kind: str,
    unit_id: int | None,
    unit_label: str,
    report: dict,
    failed_questions: list[dict],
    time_spent_seconds: int,
    question_ids: list[str] | None = None,
) -> tuple[bool, str | None]:
    """Save locally and append to Google Sheets. Returns (sheet_ok, error_message)."""
    report = sanitize_report_for_storage(report)
    db.save_ec3_practice_result(
        user_id,
        session_id=session_id,
        session_kind=session_kind,
        unit_id=unit_id,
        unit_label=unit_label,
        report=report,
        failed_questions=failed_questions,
        time_spent_seconds=time_spent_seconds,
    )

    if question_ids is not None and unit_id is not None:
        db.save_ec3_practice_session(user_id, unit_id, question_ids)

    if not is_configured():
        return False, None

    try:
        _retry_sheets_api(
            lambda: append_practice_result(
                session_id=session_id,
                user_name=user_name,
                session_kind=session_kind,
                unit_id=unit_id,
                unit_label=unit_label,
                report=report,
                failed_questions=failed_questions,
                time_spent_seconds=time_spent_seconds,
            )
        )
        flush_err: str | None = None
        try:
            _, flush_err = flush_user_session_to_sheets(user_id)
        except Exception as exc:
            flush_err = str(exc)
        if flush_err:
            return True, f"Practice saved to sheet; daily sync deferred: {flush_err}"
        return True, None
    except Exception as exc:
        return False, str(exc)


COURSE3_SESSION_UNIT_OFFSET = 100


def persist_course3_practice(
    *,
    user_name: str,
    user_id: int,
    session_id: str,
    unit_id: int | None,
    unit_label: str,
    report: dict,
    failed_questions: list[dict],
    time_spent_seconds: int,
    question_ids: list[str] | None = None,
) -> tuple[bool, str | None]:
    """Save Course 3 Math practice locally and append to Google Sheets."""
    report = sanitize_report_for_storage(report)
    db.save_ec3_practice_result(
        user_id,
        session_id=session_id,
        session_kind="course3",
        unit_id=unit_id,
        unit_label=unit_label,
        report=report,
        failed_questions=failed_questions,
        time_spent_seconds=time_spent_seconds,
    )

    if question_ids is not None and unit_id is not None:
        db.save_ec3_practice_session(user_id, unit_id + COURSE3_SESSION_UNIT_OFFSET, question_ids)

    if not is_configured():
        return False, None

    try:
        _retry_sheets_api(
            lambda: append_practice_result(
                session_id=session_id,
                user_name=user_name,
                session_kind="course3",
                unit_id=unit_id,
                unit_label=unit_label,
                report=report,
                failed_questions=failed_questions,
                time_spent_seconds=time_spent_seconds,
            )
        )
        flush_err: str | None = None
        try:
            _, flush_err = flush_user_session_to_sheets(user_id)
        except Exception as exc:
            flush_err = str(exc)
        if flush_err:
            return True, f"Practice saved to sheet; daily sync deferred: {flush_err}"
        return True, None
    except Exception as exc:
        return False, str(exc)
