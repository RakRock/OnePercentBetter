#!/usr/bin/env python3
"""Repair Class 10 Unit 7 (Coordinate Geometry) math and template defects."""

from __future__ import annotations

import json
import math
import re
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import harshit_class10_topics as h10t
from numeric_expression_eval import options_equivalent

UNIT07_DIR = ROOT / "HarshitMath" / "class10" / "question_banks" / "unit_07"

_COLLINEAR = re.compile(
    r"If \(1, (\d+)\), \(3, k\), \(5, (\d+)\) are collinear",
    re.I,
)
_DIST_CORRUPT = re.compile(
    r"^Distance between \((-?\d+), (-?\d+)\) and \((-?\d+), (-?\d+)\) is \d+\.\s*$",
)
_DIST_PLAIN = re.compile(
    r"^Distance between \((-?\d+), (-?\d+)\) and \((-?\d+), (-?\d+)\):?\s*$",
)
_ORIGIN = re.compile(r"Distance of \((\d+), (\d+)\) from origin:", re.I)
_PERIM = re.compile(r"Vertices \(0,0\), \((\d+),0\), \(0,(\d+)\)\. Perimeter", re.I)
_SECTION = re.compile(
    r"P divides AB with A\(([-\d.]+), ([-\d.]+)\), B\(([-\d.]+), ([-\d.]+)\), P\(([-\d.]+), ([-\d.]+)\)",
    re.I,
)
_RATIO_OPT = re.compile(r"^\s*(\d+)\s*:\s*(\d+)\s*$")


def _reduce_ratio(a: int, b: int) -> tuple[int, int]:
    g = math.gcd(a, b)
    return a // g, b // g


def _ratio_str(a: int, b: int) -> str:
    ra, rb = _reduce_ratio(a, b)
    return f"{ra} : {rb}"


def _ap_pb_from_point(x1: float, y1: float, x2: float, y2: float, px: float, py: float) -> tuple[int, int]:
    scale = 10_000
    if abs(x2 - px) > 1e-6:
        num = round((px - x1) * scale)
        den = round((x2 - px) * scale)
    else:
        num = round((py - y1) * scale)
        den = round((y2 - py) * scale)
    if den == 0:
        return 1, 1
    r = Fraction(num, den).limit_denominator(100)
    return _reduce_ratio(r.numerator, r.denominator)


def _fix_collinear_d(q: dict) -> bool:
    m = _COLLINEAR.search(str(q.get("question", "")))
    if not m:
        return False
    y1, y3 = int(m.group(1)), int(m.group(2))
    k = (y1 + y3) // 2
    correct = f"k = {k}"
    opts, ans = h10t._shuffle_options(
        correct,
        [f"k = {y3}", f"k = {k + 1}", f"k = {max(y1, k - 1)}"],
    )
    q["options"] = opts
    q["answer"] = ans
    q["explanation"] = f"Equal slope ⇒ k = ({y3}+{y1})/2 = {k}."
    return True


def _fix_dist_d_stem(q: dict) -> bool:
    text = str(q.get("question", "")).strip()
    m = _DIST_CORRUPT.match(text)
    if m:
        x1, y1, x2, y2 = map(int, m.groups())
        q["question"] = f"Distance between ({x1}, {y1}) and ({x2}, {y2}):"
    elif text.startswith("Distance between") and re.search(r" is \d+\.\s*$", text):
        text = re.sub(r" is \d+\.\s*$", ":", text)
        q["question"] = text if text.endswith(":") else text + ":"
    else:
        return False
    m2 = re.match(
        r"Distance between \((-?\d+), (-?\d+)\) and \((-?\d+), (-?\d+)\):",
        str(q.get("question", "")).strip(),
    )
    if not m2:
        return True
    x1, y1, x2, y2 = map(int, m2.groups())
    d = int(math.isqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
    if d * d != (x2 - x1) ** 2 + (y2 - y1) ** 2:
        d = round(math.hypot(x2 - x1, y2 - y1))
    opts, ans = h10t._shuffle_options(
        f"{d} units",
        [f"{d + 2} units", f"{abs(x2 - x1) + abs(y2 - y1)} units", f"{max(1, d - 2)} units"],
    )
    q["options"] = opts
    q["answer"] = ans
    q["explanation"] = f"√[({x2}−{x1})² + ({y2}−{y1})²] = {d}."
    return True


def _fix_origin_distance(q: dict) -> bool:
    m = _ORIGIN.search(str(q.get("question", "")))
    if not m:
        return False
    x, y = int(m.group(1)), int(m.group(2))
    d = round(math.hypot(x, y))
    correct = f"{d} units"
    opts, ans = h10t._shuffle_options(
        correct,
        [f"{d + 2} units", f"{x + y} units", f"{max(1, d - 1)} units"],
    )
    q["options"] = opts
    q["answer"] = ans
    q["explanation"] = f"√({x}² + {y}²) ≈ {d} units (nearest whole unit)."
    return True


def _fix_perimeter_e(q: dict) -> bool:
    m = _PERIM.search(str(q.get("question", "")))
    if not m:
        return False
    a, b = int(m.group(1)), int(m.group(2))
    perim = a + b + round(math.hypot(a, b))
    correct = f"{perim} units"
    opts, ans = h10t._shuffle_options(
        correct,
        [f"{a + b} units", f"{2 * (a + b)} units", f"{a * b} units"],
    )
    q["options"] = opts
    q["answer"] = ans
    q["explanation"] = f"Perimeter = {a} + {b} + √(a²+b²) ≈ {perim} units."
    return True


def _normalize_ratio_options(q: dict) -> bool:
    opts = [str(o) for o in q.get("options", [])]
    if not any(_RATIO_OPT.match(o) for o in opts):
        return False
    new_opts: list[str] = []
    seen_norm: set[str] = set()
    changed = False
    for o in opts:
        m = _RATIO_OPT.match(o.strip())
        if m:
            rs = _ratio_str(int(m.group(1)), int(m.group(2)))
            if rs.lower() in seen_norm:
                changed = True
                continue
            seen_norm.add(rs.lower())
            if rs != o.strip():
                changed = True
            new_opts.append(rs)
        else:
            new_opts.append(o)
    fillers = ["2 : 1", "3 : 2", "1 : 2", "4 : 1"]
    fi = 0
    while len(new_opts) < 4 and fi < len(fillers):
        cand = fillers[fi]
        fi += 1
        if cand.lower() not in seen_norm:
            new_opts.append(cand)
            seen_norm.add(cand.lower())
            changed = True
    if len(new_opts) > 4:
        new_opts = new_opts[:4]
    if changed or new_opts != opts:
        q["options"] = new_opts
        changed = True
    # Re-key from geometry if section question
    sm = _SECTION.search(str(q.get("question", "")))
    if sm:
        x1, y1, x2, y2, px, py = map(float, sm.groups())
        mr, nr = _ap_pb_from_point(x1, y1, x2, y2, px, py)
        correct = _ratio_str(mr, nr)
        for i, opt in enumerate(q["options"]):
            if options_equivalent(opt, correct) or opt.strip() == correct:
                q["answer"] = i
                break
        else:
            for i, opt in enumerate(q["options"]):
                m = _RATIO_OPT.match(opt)
                if m and _ratio_str(int(m.group(1)), int(m.group(2))) == correct:
                    q["answer"] = i
                    break
        changed = True
    return changed


def repair_question(q: dict) -> list[str]:
    fixes: list[str] = []
    cat = str(q.get("category", ""))
    if _fix_collinear_d(q) or cat.startswith("u7_t3_D"):
        if "collinear" in str(q.get("question", "")).lower():
            fixes.append("collinear_k")
    if cat.startswith("u7_t4_D") or _DIST_CORRUPT.match(str(q.get("question", "")).strip()):
        if _fix_dist_d_stem(q):
            fixes.append("dist_stem")
    if "from origin" in str(q.get("question", "")).lower():
        if _fix_origin_distance(q):
            fixes.append("origin_dist")
    if cat.startswith("u7_t4_E") or "Perimeter of triangle" in str(q.get("question", "")):
        if _fix_perimeter_e(q):
            fixes.append("perimeter")
    if cat.startswith("u7_t2_D") or "Ratio AP : PB" in str(q.get("question", "")):
        if _normalize_ratio_options(q):
            fixes.append("ratio_opts")
    return fixes


def repair_file(path: Path) -> dict[str, int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    stats: dict[str, int] = {}
    for bucket in data.get("questions", {}).values():
        if not isinstance(bucket, list):
            continue
        for q in bucket:
            if not isinstance(q, dict):
                continue
            for tag in repair_question(q):
                stats[tag] = stats.get(tag, 0) + 1
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return stats


def main() -> int:
    if not UNIT07_DIR.is_dir():
        print(f"Missing {UNIT07_DIR}", file=sys.stderr)
        return 1
    totals: dict[str, int] = {}
    for path in sorted(UNIT07_DIR.glob("topic_*.json")):
        stats = repair_file(path)
        if stats:
            print(f"{path.name}: {stats}")
        for k, v in stats.items():
            totals[k] = totals.get(k, 0) + v
    print("Totals:", totals)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
