#!/usr/bin/env python3
"""Extract NCERT Class 9 chapter PDFs from the combined maths textbook.

Book page numbers (footer) map to PDF page index as: pdf_index = book_page + 10
for chapters 12–15 in ncert-books-for-class-9-maths.pdf.

Examples:
    python3 scripts/extract_ncert_chapters_from_book.py \\
        --source ~/Downloads/Harshit-Math/ncert-books-for-class-9-maths.pdf \\
        --chapters 13 14 15
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "HarshitMath" / "class9_chapters"

# (chapter_num, book_page_start, book_page_end, output_filename)
CHAPTER_RANGES: dict[int, tuple[int, int, str]] = {
    13: (208, 237, "Chapter_13_Surface_Areas_and_Volumes.pdf"),
    14: (238, 270, "Chapter_14_Statistics.pdf"),
    15: (271, 285, "Chapter_15_Probability.pdf"),
}


def _book_page_to_pdf_index(book_page: int) -> int:
    """NCERT combined PDF: footer book page N is at 0-based index N + 9."""
    return book_page + 9


def extract_chapter(source: Path, chapter_num: int) -> Path:
    from pypdf import PdfReader, PdfWriter

    if chapter_num not in CHAPTER_RANGES:
        raise ValueError(f"No range configured for chapter {chapter_num}")

    start_book, end_book, filename = CHAPTER_RANGES[chapter_num]
    start_idx = _book_page_to_pdf_index(start_book)
    end_idx = _book_page_to_pdf_index(end_book)

    reader = PdfReader(str(source))
    if end_idx >= len(reader.pages):
        raise ValueError(f"Chapter {chapter_num}: end page {end_idx + 1} exceeds PDF length {len(reader.pages)}")

    writer = PdfWriter()
    for i in range(start_idx, end_idx + 1):
        writer.add_page(reader.pages[i])

    dest_dir = OUT_DIR / f"chapter_{chapter_num:02d}"
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / filename
    with dest.open("wb") as f:
        writer.write(f)

    return dest


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract NCERT Class 9 chapters from combined PDF")
    parser.add_argument(
        "--source",
        type=Path,
        default=Path.home() / "Downloads" / "Harshit-Math" / "ncert-books-for-class-9-maths.pdf",
        help="Path to combined NCERT Class 9 maths PDF",
    )
    parser.add_argument(
        "--chapters",
        type=int,
        nargs="+",
        default=[13, 14, 15],
        help="Chapter numbers to extract (default: 13 14 15)",
    )
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    if not source.is_file():
        print(f"Source PDF not found: {source}", file=sys.stderr)
        sys.exit(1)

    for ch in args.chapters:
        dest = extract_chapter(source, ch)
        start_book, end_book, _ = CHAPTER_RANGES[ch]
        print(f"Chapter {ch}: book pages {start_book}–{end_book} → {dest.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
