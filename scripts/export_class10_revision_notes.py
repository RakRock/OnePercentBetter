#!/usr/bin/env python3
"""Export Class 10 unit revision lesson notes to Markdown (print to PDF)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import harshit_class10_revision_notes as h10rn


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
        lines.append(f"## {sec.get('title', 'Section')}")
        lines.append("")
        body = str(sec.get("body", "")).strip()
        if body:
            lines.append(body)
            lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Harshit Math · Class 10 · NCERT revision sheet*")
    return "\n".join(lines)


def export_all(out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for unit_id in h10rn.all_unit_ids_with_revision():
        guide = h10rn.get_unit_revision_guide(unit_id)
        if not guide:
            continue
        path = out_dir / f"unit_{unit_id:02d}_revision.md"
        path.write_text(guide_to_markdown(guide), encoding="utf-8")
        written.append(path)
    return written


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "HarshitMath" / "class10" / "revision_notes",
        help="Output directory for Markdown files",
    )
    args = parser.parse_args()
    paths = export_all(args.out)
    for p in paths:
        print(p)
    print(f"Exported {len(paths)} revision note(s). Open in browser or Word → Print to PDF.")


if __name__ == "__main__":
    main()
