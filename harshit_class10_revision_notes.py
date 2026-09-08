"""Condensed 2–3 page revision lesson notes per Class 10 unit (1–14)."""

from __future__ import annotations

import re
from typing import Any

import harshit_class10_unit_notes as h10un
import harshit_class10_units as h10u

_REVISION_CACHE: dict[int, dict[str, Any]] = {}


def _section_by_id(guide: dict, section_id: str) -> dict[str, Any] | None:
    return next((s for s in guide.get("sections", []) if s.get("id") == section_id), None)


def _checklist_body(full_guide: dict) -> str:
    ncert = _section_by_id(full_guide, "ncert")
    teaching = _section_by_id(full_guide, "teaching")
    parts: list[str] = ["**Before practice or a unit test, Harshit should be able to:**\n"]

    if ncert:
        body = str(ncert.get("body", ""))
        if "**By the end of the unit**" in body:
            chunk = body.split("**By the end of the unit**", 1)[1]
            if "**Comes next:**" in chunk:
                chunk = chunk.split("**Comes next:**", 1)[0]
            chunk = chunk.strip()
            if chunk:
                parts.append(chunk)
        if "**Comes next:**" in body:
            nxt = body.split("**Comes next:**", 1)[1].strip().split("\n")[0]
            parts.append(f"\n**Comes next:** {nxt}")

    if teaching:
        tbody = str(teaching.get("body", ""))
        if "**One sentence for Harshit:**" in tbody:
            line = tbody.split("**One sentence for Harshit:**", 1)[1].strip()
            line = re.sub(r"\s+", " ", line)
            parts.append(f"\n\n> **One line to remember:** {line}")

    return "\n".join(parts) if len(parts) > 1 else "Review the formula sheet and NCERT worked examples."


def build_unit_revision_guide(unit_id: int) -> dict[str, Any] | None:
    """Single revision sheet per unit — big ideas, NCERT map, formulas, checklist."""
    if unit_id in _REVISION_CACHE:
        return _REVISION_CACHE[unit_id]

    full = h10un.get_unit_guide(unit_id)
    unit = h10u.get_unit(unit_id)
    if not full or not unit:
        return None

    sections: list[dict[str, Any]] = []
    overview = _section_by_id(full, "overview")
    ncert = _section_by_id(full, "ncert")
    formulas = _section_by_id(full, "formulas")

    if overview:
        sections.append(
            {
                "id": "overview",
                "title": "1. Big ideas",
                "diagrams": [],
                "body": str(overview.get("body", "")).strip(),
            }
        )
    if ncert:
        sections.append(
            {
                "id": "ncert",
                "title": "2. NCERT map & goals",
                "diagrams": [],
                "body": str(ncert.get("body", "")).strip(),
            }
        )
    if formulas:
        sections.append(
            {
                "id": "formulas",
                "title": "3. Formulas & rules to remember",
                "diagrams": [],
                "body": str(formulas.get("body", "")).strip(),
            }
        )
    sections.append(
        {
            "id": "checklist",
            "title": "4. Revision checklist",
            "diagrams": [],
            "body": _checklist_body(full),
        }
    )

    guide = {
        "title": unit["title"],
        "subtitle": f"Unit {unit_id} · NCERT Chapter {unit_id} · Revision sheet",
        "sections": sections,
    }
    _REVISION_CACHE[unit_id] = guide
    return guide


def get_unit_revision_guide(unit_id: int) -> dict[str, Any] | None:
    return build_unit_revision_guide(unit_id)


def has_unit_revision_notes(unit_id: int) -> bool:
    return get_unit_revision_guide(unit_id) is not None


def all_unit_ids_with_revision() -> list[int]:
    return [
        u["id"]
        for u in h10u.list_units()
        if u.get("active") and has_unit_revision_notes(u["id"])
    ]
