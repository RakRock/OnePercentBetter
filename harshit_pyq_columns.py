"""Rebuild two-column PYQ pages into reading order (left column, then right)."""

from __future__ import annotations

import re

_CHAP_NUM = re.compile(r"Chap\s*(\d+)", re.I)
_CHAP_TITLE = re.compile(r"Chap\s*\d+\s*:\s*(.+)", re.I)


def _lines_from_blocks(blocks: list[dict], *, y_min: float, y_max: float, x_mid: float) -> str:
    left: list[tuple[float, str]] = []
    right: list[tuple[float, str]] = []
    for block in blocks:
        if block.get("type") != 0:
            continue
        x0, y0, x1, y1 = block["bbox"]
        if y1 < y_min or y0 > y_max:
            continue
        lines: list[str] = []
        for line in block.get("lines", []):
            text = "".join(span["text"] for span in line.get("spans", [])).strip()
            if text:
                lines.append(text)
        if not lines:
            continue
        cx = (x0 + x1) / 2
        bucket = left if cx < x_mid else right
        bucket.append((y0, "\n".join(lines)))
    left.sort(key=lambda item: item[0])
    right.sort(key=lambda item: item[0])
    return "\n".join(text for _, text in left + right)


def page_chapter_number(page) -> int | None:
    """Chapter number printed in the running header (Chap N)."""
    words = page.get_text("words") or []
    header = [w for w in words if w[1] < 72]
    header.sort(key=lambda w: (round(w[1], 0), w[0]))
    text = " ".join(w[4] for w in header)
    match = _CHAP_NUM.search(text)
    if not match:
        # Some science pages put the chap line slightly lower in the right column.
        full = page.get_text("text") or ""
        match = _CHAP_NUM.search(full[:400])
    if not match:
        return None
    return int(match.group(1))


def page_chapter_title(page) -> str:
    full = page.get_text("text") or ""
    match = _CHAP_TITLE.search(full[:800])
    if not match:
        return ""
    return re.sub(r"\s+", " ", match.group(1)).strip()


def page_body_text(page) -> str:
    """Left-then-right body, skipping the running header and footer."""
    rect = page.rect
    data = page.get_text("dict")
    return _lines_from_blocks(
        data.get("blocks", []),
        y_min=68,
        y_max=rect.height - 28,
        x_mid=rect.width / 2,
    )
