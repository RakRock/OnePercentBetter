"""Extract NCERT Class 9 chapter text from PDFs and notes."""

from __future__ import annotations

import re
import subprocess
from functools import lru_cache
from pathlib import Path

import harshit_math_prereqs as hmp

MAX_CHAPTER_CHARS = 24_000
MAX_PDF_CHARS = 18_000


def _clean_text(text: str) -> str:
    text = text.replace("\x00", "")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pdf_text(path: Path, max_chars: int = MAX_PDF_CHARS) -> str:
    """Extract text from a PDF using pypdf, with pdftotext fallback."""
    text = ""
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        parts: list[str] = []
        for page in reader.pages:
            parts.append(page.extract_text() or "")
            if sum(len(p) for p in parts) >= max_chars:
                break
        text = "\n".join(parts)
    except Exception:
        text = ""

    if len(text.strip()) < 80:
        try:
            proc = subprocess.run(
                ["pdftotext", "-layout", str(path), "-"],
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
            if proc.stdout and len(proc.stdout.strip()) > len(text.strip()):
                text = proc.stdout
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            pass

    text = _clean_text(text)
    if len(text) > max_chars:
        return text[:max_chars] + "\n\n… *(excerpt truncated)*"
    return text


def _read_text_file(path: Path, max_chars: int) -> str:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (PermissionError, OSError):
        return ""
    text = _clean_text(text)
    if len(text) > max_chars:
        return text[:max_chars] + "\n\n… *(excerpt truncated)*"
    return text


def extract_chapter_text(chapter_num: int, aliases: list[str] | None = None) -> dict:
    """Load combined text for a chapter from PDFs and markdown notes."""
    alias_key = tuple(aliases) if aliases else None
    return _extract_chapter_text_cached(chapter_num, alias_key)


@lru_cache(maxsize=32)
def _extract_chapter_text_cached(chapter_num: int, aliases: tuple[str, ...] | None) -> dict:
    return _extract_chapter_text_uncached(chapter_num, list(aliases) if aliases else None)


def _extract_chapter_text_uncached(chapter_num: int, aliases: list[str] | None = None) -> dict:
    """Load combined text for a chapter from PDFs and markdown notes."""
    assets = hmp.resolve_chapter_assets(chapter_num, aliases)
    chunks: list[str] = []
    sources: list[str] = []

    for md in assets.get("markdown", []):
        text = _read_text_file(md, MAX_PDF_CHARS)
        if text:
            chunks.append(f"--- {md.name} ---\n{text}")
            sources.append(str(md))

    for pdf in assets.get("pdfs", []):
        text = extract_pdf_text(pdf)
        if text:
            chunks.append(f"--- {pdf.name} ---\n{text}")
            sources.append(str(pdf))

    combined = _clean_text("\n\n".join(chunks))
    if len(combined) > MAX_CHAPTER_CHARS:
        combined = combined[:MAX_CHAPTER_CHARS] + "\n\n… *(chapter excerpt truncated)*"

    return {
        "chapter_num": chapter_num,
        "text": combined,
        "has_text": bool(combined),
        "sources": sources,
        "assets": assets,
    }


def excerpt_for_topic(chapter_text: str, topic_name: str, level_desc: str) -> str:
    """Pick a relevant slice of chapter text for a topic (keyword windows)."""
    if not chapter_text:
        return ""

    keywords = [
        w.lower()
        for w in re.findall(r"[A-Za-z]{4,}", f"{topic_name} {level_desc}")
        if w.lower() not in {"level", "with", "from", "that", "this", "into", "given"}
    ]
    keywords.extend(["exercise", "example", "solution"])

    # Prefer a window that contains an EXERCISE block when possible
    exercise_match = re.search(r"EXERCISE\s+[\d.]+", chapter_text, re.I)
    if exercise_match:
        start = max(0, exercise_match.start() - 800)
        return chapter_text[start : start + 5000]

    if not keywords:
        return chapter_text[:6000]

    lower = chapter_text.lower()
    best_start = 0
    best_score = -1
    window = 4500
    step = 900
    for start in range(0, max(1, len(chapter_text) - window), step):
        snippet = lower[start : start + window]
        score = sum(snippet.count(k) for k in keywords)
        if score > best_score:
            best_score = score
            best_start = start

    if best_score <= 0:
        return chapter_text[:6000]
    return chapter_text[best_start : best_start + window]
