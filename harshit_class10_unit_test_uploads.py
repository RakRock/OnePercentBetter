"""Persist unit-test written work photos (one attachment for the whole paper)."""

from __future__ import annotations

import re
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK_ROOT = ROOT / "HarshitMath" / "class10" / "unit_test_work"

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
MAX_FILE_BYTES = 8 * 1024 * 1024
MAX_IMAGES_PER_TEST = 1


def _slug(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9_-]+", "_", str(text or "student").strip())
    return s[:48] or "student"


def new_session_id(unit_id: int) -> str:
    return f"hm10-ut-u{unit_id}-{int(time.time())}"


def session_dir(session_id: str, student_name: str) -> Path:
    return WORK_ROOT / _slug(student_name) / _slug(session_id)


def paper_dir(session_id: str, student_name: str, unit_id: int) -> Path:
    return session_dir(session_id, student_name) / f"unit_{unit_id:02d}" / "paper"


def _as_file_list(uploaded_files) -> list:
    if uploaded_files is None:
        return []
    if isinstance(uploaded_files, (list, tuple)):
        return list(uploaded_files)
    return [uploaded_files]


def save_session_work_images(
    *,
    session_id: str,
    student_name: str,
    unit_id: int,
    uploaded_files,
    existing: list[dict] | None = None,
) -> tuple[list[dict], str | None]:
    """Save one paper photo for the whole unit test; a new upload replaces the previous one."""
    files = _as_file_list(uploaded_files)
    if not files:
        return list(existing or []), None

    dest_root = paper_dir(session_id, student_name, unit_id)
    dest_root.mkdir(parents=True, exist_ok=True)

    upload = files[0]
    name = str(getattr(upload, "name", "") or "work.jpg")
    ext = Path(name).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        return list(existing or []), "Only JPG and PNG photos are allowed."
    data = upload.getvalue()
    if len(data) > MAX_FILE_BYTES:
        return list(existing or []), "The photo must be 8 MB or smaller."

    stamp = int(time.time() * 1000)
    safe = re.sub(r"[^a-zA-Z0-9._-]+", "_", name)
    path = dest_root / f"{stamp}_{safe}"
    path.write_bytes(data)
    return (
        [
            {
                "filename": name,
                "path": str(path),
                "size": len(data),
            }
        ],
        None,
    )


def save_work_images(
    *,
    session_id: str,
    student_name: str,
    unit_id: int,
    q_num: int = 0,
    uploaded_files=None,
    existing: list[dict] | None = None,
) -> tuple[list[dict], str | None]:
    """Compatibility wrapper — work is stored once per test, not per question."""
    del q_num
    return save_session_work_images(
        session_id=session_id,
        student_name=student_name,
        unit_id=unit_id,
        uploaded_files=uploaded_files,
        existing=existing,
    )


def test_requires_work_photo(questions: list[dict] | None) -> bool:
    return any(q.get("type") == "written" for q in (questions or []))


def work_upload_required(q: dict) -> bool:
    """True for board-style written items (used to decide if the paper needs a photo)."""
    return q.get("type") == "written"


def has_session_work_upload(images: list[dict] | None) -> bool:
    return bool(images)


def has_work_upload(resp: dict) -> bool:
    return bool(resp.get("work_images"))


def work_upload_label(q: dict | None = None) -> str:
    del q
    return (
        "Photograph your full written paper (Sections B–D) as one photo, "
        "then save it before you submit the test."
    )
