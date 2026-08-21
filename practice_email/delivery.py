"""Queue + in-process delivery — Streamlit uses HTTPS (Gmail API) when configured."""

from __future__ import annotations

import json
import subprocess
import sys
import uuid
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from practice_email.format import build_failed_questions, format_practice_report_email
from practice_email.settings import (
    EmailConfigError,
    delivery_ready,
    format_config_error,
    format_delivery_error,
    load_settings,
)
from practice_email.transport import deliver_now

ROOT = Path(__file__).resolve().parent.parent
QUEUE_DIR = ROOT / ".email_queue"
WORKER = ROOT / "send_practice_email.py"


@dataclass
class EmailSendResult:
    ok: bool
    skipped: bool = False
    pending: bool = False
    error: str = ""
    recipient: str = ""
    transport: str = ""


def _ensure_queue() -> None:
    QUEUE_DIR.mkdir(exist_ok=True)


def _python_executable() -> str:
    venv_python = ROOT / ".venv" / "bin" / "python3"
    if venv_python.is_file():
        return str(venv_python)
    return sys.executable


def _write_payload(*, subject: str, plain: str, html: str) -> Path:
    _ensure_queue()
    path = QUEUE_DIR / f"{uuid.uuid4().hex}.json"
    path.write_text(
        json.dumps({"subject": subject, "plain": plain, "html": html}, ensure_ascii=False),
        encoding="utf-8",
    )
    return path


def _run_worker(path: Path, *, wait: bool) -> tuple[bool, str]:
    """Run standalone worker for queued payloads. Returns (success, error_message)."""
    cmd = [_python_executable(), str(WORKER), str(path)]
    try:
        if wait:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=90,
                cwd=str(ROOT),
                start_new_session=True,
            )
            if proc.returncode == 0:
                path.unlink(missing_ok=True)
                return True, ""
            detail = (proc.stderr or proc.stdout or "").strip()
            return False, detail or f"worker exit {proc.returncode}"
        subprocess.Popen(
            cmd,
            cwd=str(ROOT),
            start_new_session=True,
            close_fds=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True, ""
    except Exception as exc:
        return False, str(exc)


def _is_retryable(exc: Exception) -> bool:
    """Config and DNS/host errors should not spawn background SMTP retries."""
    if isinstance(exc, EmailConfigError):
        return False
    msg = str(exc).lower()
    if "not configured" in msg or "secrets.toml" in msg:
        return False
    if "errno 8" in msg or "nodename nor servname" in msg or "name or service not known" in msg:
        return False
    if "smtp_host" in msg and ("missing" in msg or "valid hostname" in msg):
        return False
    return True


def flush_pending(*, max_items: int = 10, blocking: bool = True) -> tuple[int, int]:
    """Try to send queued emails. Returns (sent_count, remaining_count)."""
    _ensure_queue()
    sent = 0
    for path in sorted(QUEUE_DIR.glob("*.json"))[:max_items]:
        if not path.is_file():
            continue
        ok, _ = _run_worker(path, wait=blocking)
        if blocking:
            if ok and not path.exists():
                sent += 1
        # Non-blocking: spawn worker only; worker deletes the file on success.
    remaining = len(list(QUEUE_DIR.glob("*.json")))
    return sent, remaining


def send_report(
    *,
    student_name: str,
    unit_title: str,
    unit_subtitle: str,
    report: dict,
    time_spent_seconds: int,
    when: datetime | None = None,
    session_meta: dict | None = None,
    questions: list[dict] | None = None,
    answers: list[dict] | None = None,
    program_name: str = "Edgenuity Course 3",
    report_heading: str = "Edgenuity Practice Report",
) -> EmailSendResult:
    """Send a practice report email (Gmail API in-process, SMTP via worker fallback)."""
    settings = load_settings()
    if not settings.enabled:
        return EmailSendResult(ok=False, skipped=True, error="Email disabled")
    if not settings.recipient:
        return EmailSendResult(ok=False, skipped=True, error="PRACTICE_REPORT_EMAIL_TO is not set")

    ready, _transport, config_err = delivery_ready(settings)
    if not ready:
        return EmailSendResult(
            ok=False,
            skipped=True,
            error=config_err or format_config_error(settings),
        )

    failed = report.get("failed_questions")
    if failed is None and questions and answers:
        failed = build_failed_questions(questions, answers)

    subject, plain, html = format_practice_report_email(
        student_name=student_name,
        unit_title=unit_title,
        unit_subtitle=unit_subtitle,
        report=report,
        time_spent_seconds=time_spent_seconds,
        when=when,
        session_meta=session_meta,
        failed_questions=failed,
        program_name=program_name,
        report_heading=report_heading,
    )

    try:
        transport = deliver_now(settings, subject, plain, html)
        return EmailSendResult(ok=True, recipient=settings.recipient, transport=transport)
    except Exception as exc:
        user_err = format_delivery_error(exc, settings)
        if isinstance(exc, EmailConfigError) or not _is_retryable(exc):
            return EmailSendResult(
                ok=False,
                skipped=True,
                pending=False,
                recipient=settings.recipient,
                error=user_err,
            )

        path = _write_payload(subject=subject, plain=plain, html=html)
        ok, worker_err = _run_worker(path, wait=True)
        if ok and not path.exists():
            return EmailSendResult(ok=True, recipient=settings.recipient, transport="worker")
        sent, _remaining = flush_pending(max_items=3, blocking=True)
        if sent and not path.exists():
            return EmailSendResult(ok=True, recipient=settings.recipient, transport="worker")
        err = format_delivery_error(
            RuntimeError(worker_err or user_err or "Send failed"),
            settings,
        )
        return EmailSendResult(
            ok=False,
            pending=path.exists(),
            recipient=settings.recipient,
            error=err,
        )
