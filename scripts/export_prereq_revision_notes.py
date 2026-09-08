#!/usr/bin/env python3
"""Export PreReq revision lesson notes to Markdown (print to PDF from browser or Word)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import harshit_prereq_revision_notes as hprn


def guide_to_markdown(guide: dict) -> str:
    lines = [
        f"# {guide['title']}",
        "",
        f"*{guide.get('subtitle', '')}*",
        "",
        "---",
        "",
    ]
    for sec in guide.get("sections") or []:
        title = sec.get("title", "Section")
        lines.append(f"## {title}")
        lines.append("")
        body = str(sec.get("body", "")).strip()
        if body:
            lines.append(body)
            lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Harshit Math · PreReq revision sheet · NCERT Class 9*")
    return "\n".join(lines)


def export_all(out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for prereq_id in hprn.all_prereq_ids_with_revision():
        guide = hprn.get_revision_guide(prereq_id)
        if not guide:
            continue
        path = out_dir / f"prereq_{prereq_id:02d}_revision.md"
        path.write_text(guide_to_markdown(guide), encoding="utf-8")
        written.append(path)
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "HarshitMath" / "prereqs" / "revision_notes",
        help="Output directory for Markdown files",
    )
    args = parser.parse_args()
    paths = export_all(args.out)
    for p in paths:
        print(p)
    print(f"Exported {len(paths)} revision note(s). Open in a browser or Word → Print to PDF.")


if __name__ == "__main__":
    main()
