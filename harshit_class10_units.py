"""NCERT Class 10 unit catalog and PDF asset discovery."""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CLASS10_DIR = ROOT / "HarshitMath" / "class10"
CATALOG_PATH = CLASS10_DIR / "units" / "catalog.json"
UNITS_DIR = CLASS10_DIR / "units"


def _load_catalog() -> dict:
    with CATALOG_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def list_units() -> list[dict]:
    return _load_catalog()["units"]


def get_unit(unit_id: int) -> dict | None:
    return next((u for u in list_units() if u["id"] == unit_id), None)


def unit_pdf_path(unit_id: int) -> Path | None:
    unit = get_unit(unit_id)
    if not unit:
        return None
    pdf_name = unit.get("pdf") or f"unit_{unit_id:02d}.pdf"
    folder = UNITS_DIR / f"unit_{unit_id:02d}"
    candidate = folder / pdf_name
    if candidate.is_file():
        return candidate
    for path in folder.glob("*.pdf"):
        return path
    external = os.environ.get("HARSHIT_CLASS10_UNITS", "").strip()
    if external:
        ext_folder = Path(external) / f"unit_{unit_id:02d}"
        if ext_folder.is_dir():
            for path in ext_folder.glob("*.pdf"):
                return path
    return None


def extract_unit_text(unit_id: int, max_chars: int = 18_000) -> dict:
    """Extract text from the unit PDF for LLM / display."""
    path = unit_pdf_path(unit_id)
    if not path:
        return {"unit_id": unit_id, "text": "", "has_text": False, "sources": []}
    try:
        from harshit_chapter_pdf import extract_pdf_text

        text = extract_pdf_text(path, max_chars=max_chars)
    except Exception:
        text = ""
    return {
        "unit_id": unit_id,
        "text": text,
        "has_text": bool(text.strip()),
        "sources": [str(path)],
    }
