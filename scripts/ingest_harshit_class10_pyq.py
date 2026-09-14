#!/usr/bin/env python3
"""Extract PYQs from Class 10 PDFs, bucket by NCERT unit, merge into board_paper_seeds."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import harshit_class10_pyq_catalog as cat
import harshit_class10_pyq_parse as parse
from harshit_chapter_pdf import extract_pdf_text

SEEDS_DIR = ROOT / "HarshitMath" / "class10" / "board_paper_seeds"
IMPORT_DIR = ROOT / "HarshitMath" / "class10" / "pyq_import"


def _read_pdf(path: Path, max_chars: int) -> str:
    if not path.is_file():
        return ""
    return extract_pdf_text(path, max_chars=max_chars)


def _read_text(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _aggregate_blocks(paths: list[tuple[str, Path]], max_chars: int) -> dict[int, dict[str, list]]:
    combined: dict[int, dict[str, list]] = {}
    for label, path in paths:
        if path.suffix.lower() == ".pdf":
            text = _read_pdf(path, max_chars=max_chars)
        else:
            text = _read_text(path)
        if not text.strip():
            continue
        by_unit = cat.split_text_by_chapter(text)
        for unit_id, chunks in by_unit.items():
            bucket = combined.setdefault(
                unit_id,
                {"mcq": [], "assertion_reason": [], "vsa": [], "sa": [], "la": []},
            )
            for chunk in chunks:
                parsed = parse.parse_chapter_block(unit_id, chunk, source_label=label)
                for key in bucket:
                    bucket[key].extend(parsed.get(key, []))
    return combined


def _load_seed_file(unit_id: int) -> dict:
    path = SEEDS_DIR / f"unit_{unit_id:02d}.json"
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {
        "meta": {
            "unit_id": unit_id,
            "chapter": cat.chapter_title_for_unit(unit_id),
            "sources": [],
        },
        "mcq": [],
        "assertion_reason": [],
        "vsa": [],
        "sa": [],
        "la": [],
    }


def _existing_keys(data: dict) -> tuple[set[str], set[str]]:
    ids: set[str] = set()
    keys: set[str] = set()
    for bucket in ("mcq", "assertion_reason", "vsa", "sa", "la"):
        for item in data.get(bucket, []):
            ids.add(str(item.get("id", "")))
            text = item.get("question") or item.get("assertion") or ""
            keys.add(parse._norm_key(str(text)))
    return ids, keys


def main() -> int:
    defaults = cat.default_pdf_paths()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chapter-wise", type=Path, default=defaults["chapter_wise"])
    parser.add_argument("--most-repeated", type=Path, default=defaults["most_repeated"])
    parser.add_argument("--objective", type=Path, default=defaults["objective"])
    parser.add_argument(
        "--text",
        type=Path,
        action="append",
        help="Pre-extracted .txt (label:path or path only)",
    )
    parser.add_argument("--max-chars", type=int, default=2_500_000)
    parser.add_argument("--import-dir", type=Path, default=IMPORT_DIR)
    parser.add_argument("--apply", action="store_true", help="Merge into board_paper_seeds/")
    parser.add_argument("--dry-run", action="store_true", help="Print counts only")
    args = parser.parse_args()

    inputs: list[tuple[str, Path]] = [
        ("chapter_wise_pyq", args.chapter_wise),
        ("most_repeated_pyq", args.most_repeated),
        ("objective_pyq", args.objective),
    ]
    if args.text:
        for raw in args.text:
            if ":" in raw:
                label, p = raw.split(":", 1)
                inputs.append((label.strip(), Path(p.strip())))
            else:
                inputs.append((raw.stem, Path(raw)))

    # Prefer cached extract when PDF is huge.
    cached = ROOT / ".tmp_pyq_extract" / "chapter_wise_full.txt"
    if cached.is_file() and cached.stat().st_size > 1000:
        inputs.insert(0, ("chapter_wise_cached", cached))

    aggregated = _aggregate_blocks(inputs, max_chars=args.max_chars)

    args.import_dir.mkdir(parents=True, exist_ok=True)
    summary: dict[str, dict[str, int]] = {}
    total_added = 0

    for unit_id in sorted(aggregated):
        parsed = aggregated[unit_id]
        counts = {k: len(parsed.get(k, [])) for k in ("mcq", "assertion_reason", "vsa", "sa", "la")}
        if sum(counts.values()) == 0:
            continue
        summary[f"unit_{unit_id:02d}"] = counts
        out_path = args.import_dir / f"unit_{unit_id:02d}.json"
        payload = {
            "meta": {
                "unit_id": unit_id,
                "chapter": cat.chapter_title_for_unit(unit_id),
                "import_sources": [label for label, _ in inputs],
            },
            **parsed,
        }
        if not args.dry_run:
            out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

        if args.apply:
            seed = _load_seed_file(unit_id)
            removed = parse.strip_pyq_items(seed)
            if removed and not args.dry_run:
                pass  # stripped before merge
            seed.setdefault("meta", {})
            sources = list(seed["meta"].get("sources", []))
            for label, _ in inputs:
                tag = f"PYQ:{label}"
                if tag not in sources:
                    sources.append(tag)
            seed["meta"]["sources"] = sources
            existing_ids, existing_keys = _existing_keys(seed)
            added = parse.merge_seed_buckets(seed, parsed, existing_ids=existing_ids, existing_keys=existing_keys)
            total_added += added
            if not args.dry_run:
                (SEEDS_DIR / f"unit_{unit_id:02d}.json").write_text(
                    json.dumps(seed, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8",
                )

    print(json.dumps({"parsed_counts": summary, "merged_new_items": total_added}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
