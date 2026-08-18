"""Harshit Math — Class 9 PreReq buckets and chapter asset discovery."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PREREQS_DIR = ROOT / "HarshitMath" / "prereqs"
CATALOG_PATH = PREREQS_DIR / "catalog.json"
REPO_CHAPTERS_DIR = ROOT / "HarshitMath" / "class9_chapters"

def _configured_search_paths() -> list[Path]:
    """Repo path always; external path only when explicitly configured and readable."""
    paths: list[Path] = [REPO_CHAPTERS_DIR]
    external = os.environ.get("HARSHIT_CLASS9_CHAPTERS", "").strip()
    if external:
        paths.append(Path(external))
    return paths


def _path_readable(base: Path) -> bool:
    try:
        if not base.exists() or not base.is_dir():
            return False
        with os.scandir(base):
            pass
        return True
    except (PermissionError, OSError):
        return False

MARKDOWN_EXTS = {".md", ".markdown", ".txt"}
DOC_EXTS = {".pdf", ".docx"}


def _load_catalog() -> dict:
    with CATALOG_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def list_prereqs() -> list[dict]:
    return _load_catalog()["prereqs"]


def get_prereq(prereq_id: int) -> dict | None:
    return next((p for p in list_prereqs() if p["id"] == prereq_id), None)


def get_prereq_by_slug(slug: str) -> dict | None:
    return next((p for p in list_prereqs() if p["slug"] == slug), None)


def chapter_search_paths() -> list[Path]:
    return [p for p in _configured_search_paths() if _path_readable(p)]


def _chapter_num_from_name(name: str) -> int | None:
    m = re.search(r"(?:chapter|ch)[\s_-]*(\d{1,2})", name, re.I)
    if m:
        return int(m.group(1))
    m = re.match(r"^(\d{1,2})(?:[\s._-]|$)", name)
    if m:
        return int(m.group(1))
    return None


def _matches_chapter(entry: Path, chapter_num: int, aliases: list[str]) -> bool:
    stem = entry.stem.lower()
    name = entry.name.lower()
    num_str = f"{chapter_num:02d}"
    if num_str in name or str(chapter_num) in re.split(r"[\s._-]", name):
        return True
    for alias in aliases:
        if alias.lower() in name or alias.lower().replace(" ", "") in stem:
            return True
    detected = _chapter_num_from_name(entry.name)
    return detected == chapter_num


def _collect_files(base: Path, chapter_num: int, aliases: list[str]) -> list[Path]:
    found: list[Path] = []
    if not _path_readable(base):
        return found

    try:
        entries = list(base.iterdir())
    except (PermissionError, OSError):
        return found

    # Direct file in root: chapter_01.pdf
    for entry in entries:
        if entry.is_file() and _matches_chapter(entry, chapter_num, aliases):
            found.append(entry)

    # Subfolder: Chapter 1/, chapter_01/
    for entry in entries:
        if not entry.is_dir():
            continue
        if not _matches_chapter(entry, chapter_num, aliases):
            continue
        try:
            for child in entry.rglob("*"):
                if child.is_file() and child.suffix.lower() in MARKDOWN_EXTS | DOC_EXTS:
                    found.append(child)
        except (PermissionError, OSError):
            continue

    return sorted(set(found))


def resolve_chapter_assets(chapter_num: int, aliases: list[str] | None = None) -> dict:
    """Find markdown/PDF assets for a Class 9 chapter across configured paths."""
    aliases = aliases or [f"chapter_{chapter_num:02d}", f"Chapter {chapter_num}"]
    all_files: list[Path] = []
    sources: list[str] = []

    for base in _configured_search_paths():
        if not _path_readable(base):
            continue
        hits = _collect_files(base, chapter_num, aliases)
        if hits:
            all_files.extend(hits)
            sources.append(str(base))

    markdown: list[Path] = []
    pdfs: list[Path] = []
    other: list[Path] = []
    for f in all_files:
        ext = f.suffix.lower()
        if ext in MARKDOWN_EXTS:
            markdown.append(f)
        elif ext == ".pdf":
            pdfs.append(f)
        else:
            other.append(f)

    return {
        "chapter_num": chapter_num,
        "markdown": markdown,
        "pdfs": pdfs,
        "other": other,
        "has_content": bool(markdown or pdfs or other),
        "sources": sources,
    }


def chapter_status_label(assets: dict) -> str:
    if assets["has_content"]:
        parts = []
        if assets["markdown"]:
            parts.append(f"{len(assets['markdown'])} note(s)")
        if assets["pdfs"]:
            parts.append(f"{len(assets['pdfs'])} PDF(s)")
        return "Ready · " + ", ".join(parts)
    return "Awaiting chapter files"


def read_markdown_preview(path: Path, max_chars: int = 12000) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (PermissionError, OSError) as exc:
        return f"*Could not read file: {exc}*"
    if len(text) > max_chars:
        return text[:max_chars] + "\n\n… *(preview truncated)*"
    return text
