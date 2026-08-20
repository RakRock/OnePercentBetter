"""SVG diagrams for Harshit Math practice (number-line constructions, unit square, etc.)."""

from __future__ import annotations

import math
import re
from typing import Any


def _esc(text: Any) -> str:
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _sqrt_label(n: int) -> str:
    return "1" if n == 1 else f"√{n}"


def svg_unit_square(*, show_number_line: bool = True) -> str:
    """Unit square on the number line — diagonal OB = √2 (NCERT Ex 1.2)."""
    w, h = 420, 220
    ox, oy = 70, 168
    side = 90
    ax, ay = ox + side, oy
    cx, cy = ox, oy - side
    bx, by = ax, cy
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" style="max-width:100%;height:auto;display:block;margin:0 auto;">',
        '<rect x="0" y="0" width="420" height="220" rx="12" fill="#fffbeb" stroke="#fcd34d" stroke-width="1"/>',
    ]
    if show_number_line:
        parts.append(
            f'<line x1="40" y1="{oy}" x2="380" y2="{oy}" stroke="#374151" stroke-width="2"/>'
        )
        parts.append(
            f'<polygon points="{ox},{oy} {ox-6},{oy+4} {ox-6},{oy-4}" fill="#374151"/>'
        )
        for tick, label in ((0, "0"), (1, "1"), (2, "2")):
            tx = ox + tick * side
            parts.append(
                f'<line x1="{tx:.0f}" y1="{oy-7}" x2="{tx:.0f}" y2="{oy+7}" stroke="#6b7280" stroke-width="2"/>'
            )
            parts.append(
                f'<text x="{tx:.0f}" y="{oy+24}" text-anchor="middle" font-size="13" fill="#374151">{label}</text>'
            )
    parts.extend([
        f'<rect x="{ox}" y="{cy}" width="{side}" height="{side}" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>',
        f'<line x1="{ox}" y1="{oy}" x2="{bx}" y2="{by}" stroke="#dc2626" stroke-width="3" stroke-dasharray="6 4"/>',
        f'<circle cx="{ox}" cy="{oy}" r="5" fill="#2563eb"/>',
        f'<circle cx="{bx}" cy="{by}" r="5" fill="#dc2626"/>',
        f'<text x="{ox-16}" y="{(oy+cy)/2:.0f}" text-anchor="end" font-size="14" fill="#1d4ed8" font-weight="600">1</text>',
        f'<text x="{(ox+ax)/2:.0f}" y="{oy+18}" text-anchor="middle" font-size="14" fill="#1d4ed8" font-weight="600">1</text>',
        f'<text x="{(ox+bx)/2+14}" y="{(oy+by)/2-8}" font-size="15" fill="#dc2626" font-weight="700">OB = ?</text>',
        f'<text x="{(ox+cx)/2:.0f}" y="{cy-10}" text-anchor="middle" font-size="12" fill="#6b7280">OABC — each side 1 unit</text>',
        "</svg>",
    ])
    return "\n".join(parts)


def svg_sqrt_number_line(base: int, perp: int) -> str:
    """Segment `base` on the number line + perpendicular `perp` → hypotenuse OB = √(base²+perp²)."""
    base = max(1, int(base))
    perp = max(1, int(perp))
    unit = 52
    w, h = 440, 210
    ox, line_y = 56, 165
    ax = ox + base * unit
    bx, by = ax, line_y - perp * unit
    max_tick = max(base + 1, 3)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" style="max-width:100%;height:auto;display:block;margin:0 auto;">',
        '<rect x="0" y="0" width="440" height="210" rx="12" fill="#fffbeb" stroke="#fcd34d" stroke-width="1"/>',
        f'<line x1="36" y1="{line_y}" x2="404" y2="{line_y}" stroke="#374151" stroke-width="2"/>',
        f'<polygon points="{ox},{line_y} {ox-6},{line_y+4} {ox-6},{line_y-4}" fill="#374151"/>',
    ]
    for t in range(0, max_tick + 1):
        tx = ox + t * unit
        parts.append(
            f'<line x1="{tx:.0f}" y1="{line_y-7}" x2="{tx:.0f}" y2="{line_y+7}" stroke="#6b7280" stroke-width="2"/>'
        )
        parts.append(
            f'<text x="{tx:.0f}" y="{line_y+24}" text-anchor="middle" font-size="13" fill="#374151">{t}</text>'
        )
    parts.extend([
        f'<line x1="{ox}" y1="{line_y}" x2="{ax}" y2="{line_y}" stroke="#2563eb" stroke-width="4"/>',
        f'<line x1="{ax}" y1="{line_y}" x2="{bx}" y2="{by}" stroke="#059669" stroke-width="3"/>',
        f'<line x1="{ox}" y1="{line_y}" x2="{bx}" y2="{by}" stroke="#dc2626" stroke-width="3" stroke-dasharray="7 4"/>',
        f'<circle cx="{ox}" cy="{line_y}" r="5" fill="#2563eb"/>',
        f'<circle cx="{ax}" cy="{line_y}" r="5" fill="#2563eb"/>',
        f'<circle cx="{bx}" cy="{by}" r="5" fill="#dc2626"/>',
        f'<text x="{(ox+ax)/2:.0f}" y="{line_y+42}" text-anchor="middle" font-size="14" fill="#1d4ed8" font-weight="600">{base}</text>',
        f'<text x="{ax+18}" y="{(line_y+by)/2:.0f}" font-size="14" fill="#047857" font-weight="600">{perp}</text>',
        f'<text x="{(ox+bx)/2+12}" y="{(line_y+by)/2-10}" font-size="15" fill="#dc2626" font-weight="700">OB = ?</text>',
        f'<text x="220" y="24" text-anchor="middle" font-size="12" fill="#6b7280">Use the diagram — find hypotenuse OB</text>',
        "</svg>",
    ])
    return "\n".join(parts)


def svg_sqrt_extend(base_label: str, perp: int) -> str:
    """Extend from a surd on the number line (e.g. √2) with perpendicular `perp` → √3."""
    perp = max(1, int(perp))
    unit = 52
    w, h = 440, 210
    ox, line_y = 56, 165
    # Draw √2 ≈ 1.414 visually as ~1.4 units for illustration
    base_units = 1.414 if "2" in base_label else 1.0
    ax = ox + base_units * unit
    bx, by = ax, line_y - perp * unit
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" style="max-width:100%;height:auto;display:block;margin:0 auto;">',
        '<rect x="0" y="0" width="440" height="210" rx="12" fill="#fffbeb" stroke="#fcd34d" stroke-width="1"/>',
        f'<line x1="36" y1="{line_y}" x2="404" y2="{line_y}" stroke="#374151" stroke-width="2"/>',
        f'<polygon points="{ox},{line_y} {ox-6},{line_y+4} {ox-6},{line_y-4}" fill="#374151"/>',
    ]
    for t, lbl in ((0, "0"), (1, "1"), (2, "2")):
        tx = ox + t * unit
        parts.append(
            f'<line x1="{tx:.0f}" y1="{line_y-7}" x2="{tx:.0f}" y2="{line_y+7}" stroke="#6b7280" stroke-width="2"/>'
        )
        parts.append(
            f'<text x="{tx:.0f}" y="{line_y+24}" text-anchor="middle" font-size="13" fill="#374151">{lbl}</text>'
        )
    parts.extend([
        f'<line x1="{ox}" y1="{line_y}" x2="{ax}" y2="{line_y}" stroke="#2563eb" stroke-width="4"/>',
        f'<line x1="{ax}" y1="{line_y}" x2="{bx}" y2="{by}" stroke="#059669" stroke-width="3"/>',
        f'<line x1="{ox}" y1="{line_y}" x2="{bx}" y2="{by}" stroke="#dc2626" stroke-width="3" stroke-dasharray="7 4"/>',
        f'<circle cx="{ox}" cy="{line_y}" r="5" fill="#2563eb"/>',
        f'<circle cx="{ax}" cy="{line_y}" r="5" fill="#7c3aed"/>',
        f'<text x="{ax:.0f}" y="{line_y+42}" text-anchor="middle" font-size="14" fill="#7c3aed" font-weight="600">{_esc(base_label)}</text>',
        f'<text x="{ax+18}" y="{(line_y+by)/2:.0f}" font-size="14" fill="#047857" font-weight="600">{perp}</text>',
        f'<text x="{(ox+bx)/2+12}" y="{(line_y+by)/2-10}" font-size="15" fill="#dc2626" font-weight="700">OB = ?</text>',
        f'<text x="220" y="24" text-anchor="middle" font-size="12" fill="#6b7280">Right triangle from O — find hypotenuse OB</text>',
        "</svg>",
    ])
    return "\n".join(parts)


def _normalize_diagram(spec: Any) -> dict | None:
    if spec is None:
        return None
    if isinstance(spec, dict) and spec.get("type"):
        return spec
    if isinstance(spec, str) and ":" in spec:
        kind, rest = spec.split(":", 1)
        parts = [p.strip() for p in rest.split(",") if p.strip()]
        if kind == "unit_square":
            return {"type": "unit_square"}
        if kind == "sqrt_number_line" and len(parts) >= 2:
            d: dict[str, Any] = {
                "type": "sqrt_number_line",
                "base": int(parts[0]),
                "perp": int(parts[1]),
            }
            if len(parts) >= 3:
                d["target"] = int(parts[2])
            return d
        if kind == "sqrt_extend" and len(parts) >= 2:
            return {
                "type": "sqrt_extend",
                "base_label": parts[0],
                "perp": int(parts[1]),
                "target": int(parts[2]) if len(parts) >= 3 else None,
            }
    return None


def infer_diagram(question: dict) -> dict | None:
    """Guess diagram metadata from question wording when not stored explicitly."""
    text = str(question.get("question", "")).lower()
    if re.search(r"unit square|square oabc|square of side 1|diagonal ob|diagonal of a square with side 1", text):
        return {"type": "unit_square", "target": 2}
    m = re.search(
        r"segment of length (\d+).*perpendicular of length (\d+)|"
        r"legs (\d+) and (\d+).*locate √(\d+)",
        text,
    )
    if m:
        groups = [g for g in m.groups() if g is not None]
        if len(groups) >= 2 and groups[0].isdigit() and groups[1].isdigit():
            base, perp = int(groups[0]), int(groups[1])
            target = base * base + perp * perp
            return {"type": "sqrt_number_line", "base": base, "perp": perp, "target": target}
    if re.search(r"leg.*√2.*\b1\b|legs 1 and √2|one leg of length √2 and the other of length 1", text):
        return {"type": "sqrt_extend", "base_label": "√2", "perp": 1, "target": 3}
    if "locate √3" in text and "√2" in text:
        return {"type": "sqrt_extend", "base_label": "√2", "perp": 1, "target": 3}
    if "locate √5" in text or ("segment of length 2" in text and "perpendicular" in text):
        return {"type": "sqrt_number_line", "base": 2, "perp": 1, "target": 5}
    if "locate √2" in text and ("construction" in text or "pythagoras" in text):
        return {"type": "unit_square", "target": 2}
    if "unit square diagonal" in text:
        return {"type": "unit_square", "target": 2}
    return None


def diagram_spec(question: dict) -> dict | None:
    spec = _normalize_diagram(question.get("diagram"))
    if spec:
        return spec
    return infer_diagram(question)


def render_svg(question: dict) -> str | None:
    spec = diagram_spec(question)
    if not spec:
        return None
    kind = spec.get("type")
    if kind == "unit_square":
        return svg_unit_square()
    if kind == "sqrt_number_line":
        return svg_sqrt_number_line(int(spec.get("base", 1)), int(spec.get("perp", 1)))
    if kind == "sqrt_extend":
        return svg_sqrt_extend(str(spec.get("base_label", "√2")), int(spec.get("perp", 1)))
    return None


def wrap_svg(svg: str) -> str:
    return f'<div style="margin:0.5rem auto 1rem auto;max-width:460px;">{svg}</div>'


def kid_friendly_prompt(question: dict, spec: dict | None = None) -> str | None:
    """Shorter question text when a diagram carries the construction details."""
    spec = spec or diagram_spec(question)
    if not spec:
        return None
    kind = spec.get("type")
    if kind == "unit_square":
        return "Look at the diagram. Square OABC has sides of length 1. What is the length of diagonal OB?"
    if kind == "sqrt_number_line":
        return "Look at the diagram. What is the length of the hypotenuse OB?"
    if kind == "sqrt_extend":
        return "Look at the diagram. What is the length of the hypotenuse OB?"
    return None


def _shuffle_options(correct: str, wrong: list[str]) -> tuple[list[str], int]:
    import random

    correct = str(correct)
    seen = {correct}
    unique_wrong: list[str] = []
    for item in wrong:
        candidate = str(item)
        if candidate in seen:
            continue
        seen.add(candidate)
        unique_wrong.append(candidate)
    opts = [correct, *unique_wrong[:3]]
    random.shuffle(opts)
    return opts, opts.index(correct)


def _needs_option_fix(question: dict, spec: dict) -> bool:
    target = spec.get("target")
    if not target:
        if spec.get("type") == "unit_square":
            target = 2
        elif spec.get("type") == "sqrt_number_line":
            base, perp = int(spec.get("base", 1)), int(spec.get("perp", 1))
            target = base * base + perp * perp
        elif spec.get("type") == "sqrt_extend":
            target = 3
    if not target:
        return False
    correct = _sqrt_label(int(target))
    opts = [str(o) for o in question.get("options", [])]
    if correct in opts:
        return False
    joined = " ".join(opts).lower()
    return "hypotenuse" in joined or joined.startswith("sum ") or correct not in opts


def _fix_options_for_diagram(question: dict, spec: dict) -> None:
    """Normalize answer options for construction hypotenuse questions."""
    kind = spec.get("type")
    target = spec.get("target")
    if not target:
        if kind == "unit_square":
            target = 2
        elif kind == "sqrt_number_line":
            base, perp = int(spec.get("base", 1)), int(spec.get("perp", 1))
            target = base * base + perp * perp
        elif kind == "sqrt_extend":
            target = 3
    if not target:
        return
    correct = _sqrt_label(int(target))
    wrong = []
    if kind == "sqrt_number_line":
        base, perp = int(spec.get("base", 1)), int(spec.get("perp", 1))
        wrong = [str(base + perp), _sqrt_label(base * base), _sqrt_label(perp * perp)]
    elif kind == "unit_square":
        wrong = ["1", "2", "√3"]
    elif kind == "sqrt_extend":
        wrong = ["√2", "2", "√4"]
    seen = {correct}
    opts = [correct]
    for w in wrong:
        if w not in seen:
            seen.add(w)
            opts.append(w)
    while len(opts) < 4:
        for extra in ("3", "√5", "1.5", "2.5"):
            if extra not in seen:
                seen.add(extra)
                opts.append(extra)
                break
        else:
            break
    new_opts, ans = _shuffle_options(correct, opts[1:])
    question["options"] = new_opts
    question["answer"] = ans


def enrich_question(question: dict, *, rewrite_prompt: bool = True) -> dict:
    """Attach diagram metadata and optional kid-friendly prompt to a question dict."""
    spec = diagram_spec(question)
    if not spec:
        return question
    out = dict(question)
    out["diagram"] = spec
    if rewrite_prompt:
        short = kid_friendly_prompt(out, spec)
        if short:
            out["question"] = short
    if spec.get("type") in ("unit_square", "sqrt_number_line", "sqrt_extend"):
        if _needs_option_fix(out, spec):
            _fix_options_for_diagram(out, spec)
    return out
