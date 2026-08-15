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
from datetime import datetime
from typing import Any

import database as db

WORKSHEET_NAME = "EdgenuityPractice"
WEEK_PLAN_WORKSHEET = "LinearEqWeekPlan"
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
WEEK_PLAN_ID = "1"


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


def _worksheet():
    import gspread
    from google.oauth2.service_account import Credentials

    info = _service_account_info()
    sheet_id = _secret("GOOGLE_SHEET_ID")
    if not info or not sheet_id:
        raise RuntimeError("Google Sheets credentials or GOOGLE_SHEET_ID not configured")

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    creds = Credentials.from_service_account_info(info, scopes=scopes)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(sheet_id)
    try:
        return spreadsheet.worksheet(WORKSHEET_NAME)
    except gspread.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(title=WORKSHEET_NAME, rows=1000, cols=len(HEADERS))
        ws.append_row(HEADERS, value_input_option="USER_ENTERED")
        return ws


def _week_plan_worksheet():
    import gspread

    spreadsheet = _worksheet().spreadsheet
    try:
        return spreadsheet.worksheet(WEEK_PLAN_WORKSHEET)
    except gspread.WorksheetNotFound:
        ws = spreadsheet.add_worksheet(title=WEEK_PLAN_WORKSHEET, rows=10, cols=len(WEEK_PLAN_HEADERS))
        ws.append_row(WEEK_PLAN_HEADERS, value_input_option="USER_ENTERED")
        return ws


def _ensure_headers(ws) -> None:
    first = ws.row_values(1)
    if first != HEADERS:
        ws.update(range_name="A1", values=[HEADERS])


def _ensure_week_plan_headers(ws) -> None:
    first = ws.row_values(1)
    if first != WEEK_PLAN_HEADERS:
        ws.update(range_name="A1", values=[WEEK_PLAN_HEADERS])


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
    ws.append_row(row, value_input_option="USER_ENTERED")


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

    return imported


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
        append_practice_result(
            session_id=session_id,
            user_name=user_name,
            session_kind=session_kind,
            unit_id=unit_id,
            unit_label=unit_label,
            report=report,
            failed_questions=failed_questions,
            time_spent_seconds=time_spent_seconds,
        )
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
        append_practice_result(
            session_id=session_id,
            user_name=user_name,
            session_kind="course3",
            unit_id=unit_id,
            unit_label=unit_label,
            report=report,
            failed_questions=failed_questions,
            time_spent_seconds=time_spent_seconds,
        )
        return True, None
    except Exception as exc:
        return False, str(exc)
