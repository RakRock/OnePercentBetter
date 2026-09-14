"""NCERT chapter titles and PYQ PDF source metadata for Class 10 Mathematics."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CATALOG_PATH = ROOT / "HarshitMath" / "class10" / "units" / "catalog.json"

# Extra headings seen in third-party PYQ compilations (not always in NCERT titles).
CHAPTER_ALIASES: dict[str, int] = {
    "quadratic equations": 4,
    "solution of pair of linear equations": 3,
    "pair of linear equations": 3,
}

_DEFAULT_PDF_PATHS = {
    "chapter_wise": Path.home() / "Downloads" / "math Chapter wise pyq 10th.pdf",
    "most_repeated": Path.home() / "Downloads" / "Math 10th PYQ Most repeated Question.pdf",
    "objective": Path.home() / "Downloads" / "Math 10th Objective PYQ.pdf",
}


def load_unit_titles() -> list[tuple[int, str]]:
    data = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    rows: list[tuple[int, str]] = []
    for unit in data["units"]:
        uid = int(unit["id"])
        if uid > 14:
            continue
        rows.append((uid, str(unit["title"]).strip()))
    return rows


def chapter_title_for_unit(unit_id: int) -> str:
    for uid, title in load_unit_titles():
        if uid == unit_id:
            return title
    return f"Unit {unit_id}"


def normalize_chapter_heading(line: str) -> str:
    text = re.sub(r"\s+", " ", line.strip().lower())
    text = re.sub(r"[^\w\s]", "", text)
    return text


def match_unit_id_for_heading(line: str) -> int | None:
    stripped = line.strip()
    if not stripped or len(stripped) > 80:
        return None
    if re.match(r"^\d+[\.\)]\s", stripped):
        return None
    norm = normalize_chapter_heading(stripped)
    if norm in CHAPTER_ALIASES:
        return CHAPTER_ALIASES[norm]
    for uid, title in load_unit_titles():
        if normalize_chapter_heading(title) == norm:
            return uid
    # Aliases only on exact heading lines (avoid matching "quadratic polynomial" in stems).
    for alias, uid in CHAPTER_ALIASES.items():
        if norm == alias:
            return uid
    return None


def split_text_by_chapter(text: str) -> dict[int, list[str]]:
    """Return unit_id -> list of text blocks (one per heading occurrence)."""
    lines = text.splitlines()
    blocks: dict[int, list[str]] = {uid: [] for uid, _ in load_unit_titles()}
    current_unit: int | None = None
    buf: list[str] = []

    def flush() -> None:
        nonlocal buf, current_unit
        if current_unit is not None and buf:
            chunk = "\n".join(buf).strip()
            if chunk:
                blocks[current_unit].append(chunk)
        buf = []

    for line in lines:
        uid = match_unit_id_for_heading(line)
        if uid is not None:
            flush()
            current_unit = uid
            continue
        if current_unit is not None:
            buf.append(line)
    flush()
    return blocks


def default_pdf_paths() -> dict[str, Path]:
    return dict(_DEFAULT_PDF_PATHS)
