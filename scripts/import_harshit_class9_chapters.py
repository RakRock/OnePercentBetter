#!/usr/bin/env python3
"""Copy NCERT Class 9 chapter files from Downloads into the repo.

Run from Terminal (needs read access to ~/Downloads):

    python3 scripts/import_harshit_class9_chapters.py

Optional source override:

    HARSHIT_CLASS9_CHAPTERS=/path/to/chapters python3 scripts/import_harshit_class9_chapters.py
"""

from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "HarshitMath" / "class9_chapters"
DEFAULT_SRC = Path.home() / "Downloads" / "Harshit-Math" / "Class9-Chapter"
REPO_SRC = ROOT / "Harshit-Math" / "Class9-Chapter"
REPO_CHAPTERS = ROOT / "HarshitMath" / "class9_chapters"

CHAPTER_NUMS = {1, 2, 3, 4, 5, 6, 7, 8, 10, 12, 13, 14, 15}
DOC_EXTS = {".pdf", ".md", ".markdown", ".txt", ".docx"}


def chapter_num_from_name(name: str) -> int | None:
    m = re.search(r"(?:chapter|ch)[\s_-]*(\d{1,2})", name, re.I)
    if m:
        return int(m.group(1))
    m = re.match(r"^(\d{1,2})(?:[\s._-]|$)", name)
    if m:
        return int(m.group(1))
    return None


def dest_for_chapter(num: int) -> Path:
    folder = DEST / f"chapter_{num:02d}"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def copy_file(src: Path, chapter_num: int) -> Path:
    dest_dir = dest_for_chapter(chapter_num)
    dest = dest_dir / src.name
    if dest.exists() and dest.stat().st_size == src.stat().st_size:
        return dest
    shutil.copy2(src, dest)
    return dest


def _assert_readable(src: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(f"Source not found: {src}")
    try:
        with os.scandir(src):
            pass
    except PermissionError as exc:
        raise PermissionError(
            f"Cannot read {src}. Run this script from Terminal.app "
            "(or grant Full Disk Access to your terminal), then re-run."
        ) from exc


def import_from_path(src: Path) -> list[Path]:
    _assert_readable(src)
    copied: list[Path] = []

    for entry in sorted(src.rglob("*")):
        if not entry.is_file():
            continue
        if entry.suffix.lower() not in DOC_EXTS:
            continue
        num = chapter_num_from_name(entry.parent.name) or chapter_num_from_name(entry.name)
        if num is None or num not in CHAPTER_NUMS:
            print(f"  skip (no chapter match): {entry.relative_to(src)}")
            continue
        dest = copy_file(entry, num)
        copied.append(dest)
        print(f"  chapter {num:02d} ← {entry.name}")

    return copied


def main() -> None:
    sources = [
        Path(os.environ.get("HARSHIT_CLASS9_CHAPTERS", "")),
        REPO_SRC,
        DEFAULT_SRC,
        REPO_CHAPTERS,
    ]
    total = 0
    for src in sources:
        if not str(src) or not src.exists():
            continue
        try:
            with os.scandir(src):
                pass
        except (PermissionError, OSError):
            continue
        print(f"Importing from: {src}")
        print(f"Destination:    {DEST}\n")
        total += len(import_from_path(src))
        if total:
            break
    print(f"\nDone — {total} file(s) copied.")
    if not total:
        print("No matching chapter files found. Check folder layout and file extensions.")


if __name__ == "__main__":
    main()
