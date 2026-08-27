"""Persist unit-test written work photos (VSA / SA / LA)."""

from __future__ import annotations

import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK_ROOT = ROOT / "HarshitMath" / "class10" / "unit_test_work"

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_IMAGES_PER_QUESTION = 6


def _slug(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_-]+", "_", str(text or "student").strip())
    return s[:48] or "student"


def new_session_id(unit_id: int) -> str:
    return f"hm10-ut-u{unit_id}-{int(time.time())}"


def session_dir(session_id: str, student_name: str) -> Path:
    return WORK_ROOT / _slug(student_name) / _slug(session_id)


def question_dir(session_id: str, student_name: str, unit_id: int, q_num: int) -> Path:
    return session_dir(session_id, student_name) / f"unit_{unit_id:02d}" / f"q{q_num:02d}"


def save_work_images(
    *,
    session_id: str,
    student_name: str,
    unit_id: int,
    q_num: int,
    uploaded_files,
    existing: list[dict] | None = None,
) -> tuple[list[dict], str | None]:
    """Save uploaded Streamlit files; return metadata list and optional error."""
    existing = list(existing or [])
    if len(existing) >= MAX_IMAGES_PER_QUESTION:
        return existing, f"Maximum {MAX_IMAGES_PER_QUESTION} photos per question."

    dest_root = question_dir(session_id, student_name, unit_id, q_num)
    dest_root.mkdir(parents=True, exist_ok=True)

    saved_names = {m.get("filename") for m in existing}
    out = list(existing)

    for upload in uploaded_files or []:
        if len(out) >= MAX_IMAGES_PER_QUESTION:
            break
        name = str(getattr(upload, "name", "") or "work.jpg")
        ext = Path(name).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            return out, "Only JPG and PNG photos are allowed."
        data = upload.getvalue()
        if len(data) > MAX_FILE_BYTES:
            return out, "Each photo must be 8 MB or smaller."
        if name in saved_names:
            continue
        stamp = int(time.time() * 1000)
        safe = re.sub(r"[^a-zA-Z0-9._-]+", "_", name)
        path = dest_root / f"{stamp}_{safe}"
        path.write_bytes(data)
        out.append(
            {
                "filename": name,
                "path": str(path),
                "size": len(data),
            }
        )
        saved_names.add(name)

    return out, None


def work_upload_required(q: dict) -> bool:
    """Board-style written questions should include work photos."""
    return q.get("type") == "written"


def has_work_upload(resp: dict) -> bool:
    return bool(resp.get("work_images"))


def work_upload_label(q: dict) -> str:
    marks = int(q.get("marks", 0))
    section = str(q.get("section", ""))
    if section == "D" or marks >= 5:
        return "Required for 5-mark questions: photograph every page of your work (including diagrams)."
    return "Photograph your written work on paper before checking the model answer."
