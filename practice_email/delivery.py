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
from practice_email.settings import email_configured, load_settings
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


def flush_pending(*, max_items: int = 10) -> tuple[int, int]:
    """Try to send queued emails. Returns (sent_count, remaining_count)."""
    _ensure_queue()
    sent = 0
    for path in sorted(QUEUE_DIR.glob("*.json"))[:max_items]:
        ok, _ = _run_worker(path, wait=True)
        if ok and not path.exists():
            sent += 1
        elif ok and path.exists():
            try:
                path.unlink(missing_ok=True)
                sent += 1
            except OSError:
                pass
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
) -> EmailSendResult:
    """Send a practice report email (Gmail API in-process, SMTP via worker fallback)."""
    settings = load_settings()
    if not settings.enabled:
        return EmailSendResult(ok=False, skipped=True, error="Email disabled")
    if not email_configured():
        return EmailSendResult(ok=False, skipped=True, error="Email not configured")

    subject, plain, html = format_practice_report_email(
        student_name=student_name,
        unit_title=unit_title,
        unit_subtitle=unit_subtitle,
        report=report,
        time_spent_seconds=time_spent_seconds,
        when=when,
        session_meta=session_meta,
        failed_questions=build_failed_questions(questions, answers) if questions and answers else None,
    )

    try:
        transport = deliver_now(settings, subject, plain, html)
        return EmailSendResult(ok=True, recipient=settings.recipient, transport=transport)
    except Exception as exc:
        path = _write_payload(subject=subject, plain=plain, html=html)
        ok, worker_err = _run_worker(path, wait=True)
        if ok or not path.exists():
            return EmailSendResult(ok=True, recipient=settings.recipient, transport="worker")
        _run_worker(path, wait=False)
        flush_pending(max_items=3)
        if not path.exists():
            return EmailSendResult(ok=True, recipient=settings.recipient, transport="worker")
        err = str(exc) or worker_err or "Send failed"
        return EmailSendResult(
            ok=False,
            pending=True,
            recipient=settings.recipient,
            error=err,
        )
