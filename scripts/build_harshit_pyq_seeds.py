#!/usr/bin/env python3
"""Split Class 10 PYQ PDFs into Math and Science unit seeds for daily practice."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pymupdf

import harshit_class10_pyq_catalog as cat
import harshit_class10_pyq_parse as parse
import harshit_pyq_books as books
import harshit_pyq_columns as cols

MATH_SEEDS = ROOT / "HarshitMath" / "class10" / "board_paper_seeds"
SCIENCE_DIRS = {
    "chemistry": ROOT / "HarshitChemistry" / "pyq_seeds",
    "physics": ROOT / "HarshitPhysics" / "pyq_seeds",
    "biology": ROOT / "HarshitBiology" / "pyq_seeds",
}

DEFAULTS = {
    "chapter_wise": Path.home() / "Downloads" / "math Chapter wise pyq 10th.pdf",
    "most_repeated": Path.home() / "Downloads" / "Math 10th PYQ Most repeated Question.pdf",
    "math_objective": Path.home() / "Downloads" / "Math 10th Objective PYQ.pdf",
    "science_objective": Path.home() / "Downloads" / "Science Objective pyq 2014 to 2026 !!.pdf",
}


def _empty_math() -> dict[int, dict[str, list]]:
    out: dict[int, dict[str, list]] = {}
    for unit_id, _title in cat.load_unit_titles():
        out[unit_id] = {"mcq": [], "assertion_reason": [], "vsa": [], "sa": [], "la": []}
    return out


def _extend_math(base: dict[int, dict[str, list]], extra: dict[int, dict[str, list]]) -> None:
    for unit_id, buckets in extra.items():
        dest = base.setdefault(
            unit_id, {"mcq": [], "assertion_reason": [], "vsa": [], "sa": [], "la": []}
        )
        for key in dest:
            dest[key].extend(buckets.get(key, []))


def _read_text(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _math_objective(path: Path, *, limit_pages: int | None) -> dict[int, dict[str, list]]:
    buckets = _empty_math()
    if not path.is_file():
        return buckets
    doc = pymupdf.open(path)
    last = doc.page_count if not limit_pages else min(limit_pages, doc.page_count)
    for index in range(last):
        page = doc[index]
        unit_id = cols.page_chapter_number(page)
        if not unit_id:
            continue
        body = cols.page_body_text(page)
        for item in books.parse_objective_mcq_page(unit_id, body, source_label="math_objective_pyq"):
            buckets[unit_id]["mcq"].append(item)
    doc.close()
    return buckets


def _science_objective(path: Path, *, limit_pages: int | None) -> dict[tuple[str, int], list[dict]]:
    grouped: dict[tuple[str, int], list[dict]] = {}
    titles: dict[tuple[str, int], str] = {}
    if not path.is_file():
        return grouped
    doc = pymupdf.open(path)
    last = doc.page_count if not limit_pages else min(limit_pages, doc.page_count)
    current: tuple[str, int, str] | None = None
    for index in range(last):
        page = doc[index]
        number = cols.page_chapter_number(page)
        title = cols.page_chapter_title(page)
        mapped = books.science_unit_for(number, title) if number else None
        # Chapter banners appear on the opening page only; later pages stay in that chapter.
        if mapped:
            current = mapped
        if not current:
            continue
        subject, unit_id, chapter = current
        titles[(subject, unit_id)] = chapter
        body = cols.page_body_text(page)
        items = books.parse_science_short_answers(
            body,
            subject=subject,
            unit_id=unit_id,
            source_label="science_objective_pyq",
        )
        grouped.setdefault((subject, unit_id), []).extend(items)
    doc.close()
    grouped["_titles"] = titles  # type: ignore[assignment]
    return grouped


def _dedupe_math(buckets: dict[int, dict[str, list]]) -> None:
    for unit_id, data in buckets.items():
        data["mcq"] = books.dedupe_items(data.get("mcq", []), "question")
        for key in ("vsa", "sa", "la"):
            data[key] = books.dedupe_items(data.get(key, []), "question")


def _load_seed(unit_id: int) -> dict:
    path = MATH_SEEDS / f"unit_{unit_id:02d}.json"
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return {
        "meta": {"unit_id": unit_id, "chapter": cat.chapter_title_for_unit(unit_id), "sources": []},
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


def _apply_math(buckets: dict[int, dict[str, list]], labels: list[str]) -> int:
    added = 0
    for unit_id, parsed in buckets.items():
        if not any(parsed.get(k) for k in ("mcq", "vsa", "sa", "la")):
            continue
        seed = _load_seed(unit_id)
        parse.strip_pyq_items(seed)
        seed.setdefault("meta", {})
        sources = list(seed["meta"].get("sources", []))
        for label in labels:
            tag = f"PYQ:{label}"
            if tag not in sources:
                sources.append(tag)
        seed["meta"]["sources"] = sources
        seed["meta"]["chapter"] = cat.chapter_title_for_unit(unit_id)
        ids, keys = _existing_keys(seed)
        added += parse.merge_seed_buckets(seed, parsed, existing_ids=ids, existing_keys=keys)
        path = MATH_SEEDS / f"unit_{unit_id:02d}.json"
        path.write_text(json.dumps(seed, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return added


def _apply_science(grouped: dict, titles: dict[tuple[str, int], str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    by_subject: dict[str, dict[int, list]] = {name: {} for name in SCIENCE_DIRS}
    for key, items in grouped.items():
        if not isinstance(key, tuple):
            continue
        subject, unit_id = key
        deduped = books.dedupe_items(items, "question")
        by_subject.setdefault(subject, {})[unit_id] = deduped
    for subject, units in by_subject.items():
        folder = SCIENCE_DIRS[subject]
        folder.mkdir(parents=True, exist_ok=True)
        for unit_id, items in sorted(units.items()):
            payload = {
                "meta": {
                    "subject": subject,
                    "unit_id": unit_id,
                    "chapter": titles.get((subject, unit_id), ""),
                    "sources": ["PYQ:science_objective_pyq"],
                },
                "mcq": [],
                "short_answer": items,
            }
            path = folder / f"unit_{unit_id:02d}.json"
            path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
            counts[f"{subject}_u{unit_id:02d}"] = len(items)
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chapter-wise-text", type=Path, default=ROOT / ".tmp_pyq_extract" / "math_chapter_wise.txt")
    parser.add_argument("--most-repeated-text", type=Path, default=ROOT / ".tmp_pyq_extract" / "math_most_repeated.txt")
    parser.add_argument("--math-objective", type=Path, default=DEFAULTS["math_objective"])
    parser.add_argument("--science-objective", type=Path, default=DEFAULTS["science_objective"])
    parser.add_argument("--limit-pages", type=int, default=0, help="Debug: only the first N PDF pages")
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    limit = args.limit_pages or None

    math_buckets = _empty_math()
    chapter_text = _read_text(args.chapter_wise_text)
    if chapter_text:
        _extend_math(
            math_buckets,
            books.parse_question_solution_blocks(chapter_text, source_label="chapter_wise_pyq"),
        )
        by_unit = cat.split_text_by_chapter(chapter_text)
        for unit_id, chunks in by_unit.items():
            for chunk in chunks:
                parsed = parse.parse_chapter_block(unit_id, chunk, source_label="chapter_wise_pyq")
                parsed["mcq"] = [item for item in parsed.get("mcq", []) if books._mcq_answer_supported(item)]
                for key in math_buckets[unit_id]:
                    math_buckets[unit_id][key].extend(parsed.get(key, []))
    repeated = _read_text(args.most_repeated_text)
    if repeated:
        _extend_math(math_buckets, books.parse_inline_written(repeated, source_label="most_repeated_pyq"))
    _extend_math(math_buckets, _math_objective(args.math_objective, limit_pages=limit))
    _dedupe_math(math_buckets)

    science_raw = _science_objective(args.science_objective, limit_pages=limit)
    titles = science_raw.pop("_titles", {})

    summary = {
        "math": {
            f"unit_{uid:02d}": {k: len(v) for k, v in buckets.items() if v}
            for uid, buckets in math_buckets.items()
            if any(buckets.values())
        },
        "science": {},
    }
    for key, items in science_raw.items():
        if isinstance(key, tuple):
            summary["science"][f"{key[0]}_u{key[1]:02d}"] = len(books.dedupe_items(items, "question"))

    added = 0
    science_counts: dict[str, int] = {}
    if args.apply:
        added = _apply_math(
            math_buckets,
            ["chapter_wise_pyq", "most_repeated_pyq", "math_objective_pyq"],
        )
        science_counts = _apply_science(science_raw, titles)
    print(json.dumps({"parsed": summary, "math_merged_new": added, "science_written": science_counts}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
