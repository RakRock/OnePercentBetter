"""
Optional visual hints for Mental Math Sprint: lightweight SVG diagrams
and optional Hugging Face image generation for richer illustrations.

SVG hints work offline. HF requires HF_TOKEN (env or Streamlit secrets).
"""

from __future__ import annotations

import io
import os
from typing import Any


def _esc(x: Any) -> str:
    return str(x).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg_number_line(
    min_v: float,
    max_v: float,
    points: list[float],
    labels: list[str] | None = None,
    width: int = 420,
    height: int = 110,
) -> str:
    """Horizontal number line with tick marks at `points`."""
    if max_v <= min_v:
        max_v = min_v + 1
    labels = labels or [str(int(p)) if p == int(p) else f"{p:.1f}" for p in points]
    pad = 24
    span = max_v - min_v
    scale = (width - 2 * pad) / span

    def x_at(p: float) -> float:
        return pad + (p - min_v) * scale

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" style="max-width:100%;height:auto;">',
        f'<line x1="{pad}" y1="{height // 2}" x2="{width - pad}" y2="{height // 2}" '
        'stroke="#374151" stroke-width="2"/>',
    ]
    colors = ["#2563eb", "#dc2626", "#059669", "#7c3aed"]
    for i, p in enumerate(points):
        x = x_at(p)
        col = colors[i % len(colors)]
        parts.append(
            f'<line x1="{x:.1f}" y1="{height // 2 - 8}" x2="{x:.1f}" y2="{height // 2 + 8}" '
            f'stroke="{col}" stroke-width="3"/>'
        )
        parts.append(
            f'<text x="{x:.1f}" y="{height // 2 + 28}" text-anchor="middle" '
            f'font-size="12" fill="{col}" font-weight="600">{_esc(labels[i])}</text>'
        )
    parts.append("</svg>")
    return "\n".join(parts)


def svg_bar_percent(pct: int, caption: str = "") -> str:
    """Single bar 0–100% filled."""
    w, h = 360, 56
    fill_w = max(0, min(100, pct)) * (w - 4) / 100
    cap = f'<text x="4" y="78" font-size="11" fill="#6b7280">{_esc(caption)}</text>' if caption else ""
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="88" viewBox="0 0 {w} 88" style="max-width:100%;">
  <rect x="0" y="8" width="{w}" height="{h}" rx="6" fill="#e5e7eb" stroke="#9ca3af"/>
  <rect x="2" y="10" width="{fill_w:.1f}" height="{h - 4}" rx="4" fill="#10b981"/>
  <text x="{w/2:.1f}" y="{8 + h/2 + 5:.1f}" text-anchor="middle" font-size="14" font-weight="700" fill="#111827">{pct}%</text>
  {cap}
</svg>
""".strip()


def svg_bar_fraction(num: int, den: int, of_total: int | None = None) -> str:
    """Bar split into `den` parts with `num` parts shaded (``of`` whole)."""
    if den <= 0:
        den = 1
    num = max(0, min(num, den))
    w, h = 360, 52
    seg = (w - 4) / den
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="72" viewBox="0 0 {w} 72">',
        f'<rect x="0" y="4" width="{w}" height="{h}" rx="6" fill="#f3f4f6" stroke="#9ca3af"/>',
    ]
    for i in range(den):
        x = 2 + i * seg
        fill = "#3b82f6" if i < num else "#ffffff"
        stroke = "#1d4ed8" if i < num else "#d1d5db"
        parts.append(
            f'<rect x="{x:.2f}" y="6" width="{seg - 1:.2f}" height="{h - 4}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1"/>'
        )
    cap = f" of {of_total}" if of_total is not None else ""
    parts.append(
        f'<text x="{w/2:.1f}" y="{h + 22}" text-anchor="middle" font-size="12" fill="#374151">'
        f"{num}/{den}{_esc(cap)}</text>"
    )
    parts.append("</svg>")
    return "\n".join(parts)


def svg_rectangle_lw(length: int, width: int) -> str:
    """Rectangle with length (horizontal) and width (vertical) labeled."""
    ml, mw = max(length, 1), max(width, 1)
    scale = min(200 / ml, 120 / mw)
    rw, rh = ml * scale, mw * scale
    ox, oy = 30.0, 25.0
    w_svg, h_svg = 320, max(100.0, rh + 70)
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg:.0f}" height="{h_svg:.0f}" viewBox="0 0 {w_svg} {h_svg}" style="max-width:100%;">
  <text x="4" y="16" font-size="12" fill="#6b7280">Rectangle</text>
  <rect x="{ox:.1f}" y="{oy:.1f}" width="{rw:.1f}" height="{rh:.1f}" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>
  <text x="{ox + rw/2:.1f}" y="{oy - 6:.1f}" text-anchor="middle" font-size="13" font-weight="600" fill="#0369a1">{_esc(length)}</text>
  <text x="{ox + rw + 10:.1f}" y="{oy + rh/2:.1f}" dominant-baseline="middle" font-size="13" font-weight="600" fill="#0369a1">{_esc(width)}</text>
</svg>
""".strip()


def svg_triangle_bh(base: int, height: int) -> str:
    """Triangle with horizontal base and dashed height to apex."""
    b = max(base, 1)
    h = max(height, 1)
    scale = min(200 / b, 100 / h)
    bw, hh = b * scale, h * scale
    ox, base_y = 40.0, 130.0
    ax, ay = ox + bw / 2.0, base_y - hh
    w_svg, h_svg = 300, 150
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w_svg}" height="{h_svg}" viewBox="0 0 {w_svg} {h_svg}" style="max-width:100%;">
  <text x="4" y="14" font-size="12" fill="#6b7280">Triangle (height ⊥ base)</text>
  <line x1="{ox:.1f}" y1="{base_y:.1f}" x2="{ox + bw:.1f}" y2="{base_y:.1f}" stroke="#0f766e" stroke-width="2"/>
  <line x1="{ox:.1f}" y1="{base_y:.1f}" x2="{ax:.1f}" y2="{ay:.1f}" stroke="#0f766e" stroke-width="2"/>
  <line x1="{ox + bw:.1f}" y1="{base_y:.1f}" x2="{ax:.1f}" y2="{ay:.1f}" stroke="#0f766e" stroke-width="2"/>
  <line x1="{ax:.1f}" y1="{ay:.1f}" x2="{ax:.1f}" y2="{base_y:.1f}" stroke="#64748b" stroke-width="1.5" stroke-dasharray="5,4"/>
  <text x="{ox + bw/2:.1f}" y="{base_y + 16:.1f}" text-anchor="middle" font-size="12" fill="#0f766e" font-weight="600">{_esc(base)}</text>
  <text x="{ax + 8:.1f}" y="{(ay + base_y)/2:.1f}" font-size="12" fill="#64748b" font-weight="600">{_esc(height)}</text>
</svg>
""".strip()


def svg_square_side(side: int, caption: str = "") -> str:
    """Square with one side labeled."""
    s = max(side, 1)
    scale = min(160 / s, 160 / s)
    sz = s * scale
    ox, oy = 50.0, 34.0
    cap = f'<text x="4" y="16" font-size="11" fill="#6b7280">{_esc(caption)}</text>' if caption else ""
    h_svg = 108 if caption else 100
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="260" height="{h_svg}" viewBox="0 0 260 {h_svg}" style="max-width:100%;">
  {cap}
  <rect x="{ox:.1f}" y="{oy:.1f}" width="{sz:.1f}" height="{sz:.1f}" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
  <text x="{ox + sz/2:.1f}" y="{oy + sz + 18:.1f}" text-anchor="middle" font-size="13" font-weight="600" fill="#b45309">{_esc(side)}</text>
</svg>
""".strip()


def svg_rectangle_perimeter(l: int, w: int) -> str:
    """Rectangle with all four sides labeled (perimeter context)."""
    ml, mw = max(l, 1), max(w, 1)
    scale = min(180 / ml, 100 / mw)
    rw, rh = ml * scale, mw * scale
    ox, oy = 45.0, 35.0
    h_svg = max(120.0, rh + 55)
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="300" height="{h_svg:.0f}" viewBox="0 0 300 {h_svg:.0f}" style="max-width:100%;">
  <text x="4" y="16" font-size="12" fill="#6b7280">Perimeter = sum of sides</text>
  <rect x="{ox:.1f}" y="{oy:.1f}" width="{rw:.1f}" height="{rh:.1f}" fill="#fae8ff" stroke="#a21caf" stroke-width="2"/>
  <text x="{ox + rw/2:.1f}" y="{oy - 6:.1f}" text-anchor="middle" font-size="12" font-weight="600" fill="#86198f">{_esc(l)}</text>
  <text x="{ox + rw/2:.1f}" y="{oy + rh + 16:.1f}" text-anchor="middle" font-size="12" font-weight="600" fill="#86198f">{_esc(l)}</text>
  <text x="{ox - 12:.1f}" y="{oy + rh/2:.1f}" dominant-baseline="middle" font-size="12" font-weight="600" fill="#86198f">{_esc(w)}</text>
  <text x="{ox + rw + 10:.1f}" y="{oy + rh/2:.1f}" dominant-baseline="middle" font-size="12" font-weight="600" fill="#86198f">{_esc(w)}</text>
</svg>
""".strip()


def svg_rectangle_find_width(perimeter: int, length: int) -> str:
    """Rectangle: known perimeter and length; width is unknown (diagram does not encode the answer)."""
    ml = max(length, 1)
    scale = 150 / ml
    rw = ml * scale
    rh = rw * 0.55
    ox, oy = 50.0, 38.0
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="280" height="118" viewBox="0 0 280 118" style="max-width:100%;">
  <text x="4" y="14" font-size="11" fill="#6b7280">P = {_esc(perimeter)}  →  L + W = {_esc(perimeter // 2)}</text>
  <rect x="{ox:.1f}" y="{oy:.1f}" width="{rw:.1f}" height="{rh:.1f}" fill="#ecfccb" stroke="#65a30d" stroke-width="2"/>
  <text x="{ox + rw/2:.1f}" y="{oy - 5:.1f}" text-anchor="middle" font-size="12" font-weight="600">{_esc(length)}</text>
  <text x="{ox + rw + 8:.1f}" y="{oy + rh/2:.1f}" dominant-baseline="middle" font-size="12" font-weight="700" fill="#4d7c0f">W = ?</text>
</svg>
""".strip()


def svg_triangle_angles(deg_a: int, deg_b: int, deg_c: int) -> str:
    """Triangle with three interior angles labeled at corners."""
    p1x, p1y = 40.0, 120.0
    p2x, p2y = 220.0, 120.0
    p3x, p3y = 130.0, 35.0
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="260" height="135" viewBox="0 0 260 135" style="max-width:100%;">
  <text x="4" y="14" font-size="12" fill="#6b7280">Angles sum to 180°</text>
  <polygon points="{p1x:.0f},{p1y:.0f} {p2x:.0f},{p2y:.0f} {p3x:.0f},{p3y:.0f}" fill="#fff7ed" stroke="#ea580c" stroke-width="2"/>
  <text x="{p1x - 8:.0f}" y="{p1y + 18:.0f}" font-size="13" font-weight="700" fill="#c2410c">{_esc(deg_a)}°</text>
  <text x="{p2x - 18:.0f}" y="{p2y + 18:.0f}" font-size="13" font-weight="700" fill="#c2410c">{_esc(deg_b)}°</text>
  <text x="{p3x - 12:.0f}" y="{p3y - 6:.0f}" font-size="13" font-weight="700" fill="#c2410c">{_esc(deg_c)}°</text>
</svg>
""".strip()


def svg_triangle_two_angles_known(deg_a: int, deg_b: int) -> str:
    """Two given angles; third shown as ? (find missing angle)."""
    p1x, p1y = 40.0, 120.0
    p2x, p2y = 220.0, 120.0
    p3x, p3y = 130.0, 35.0
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="260" height="135" viewBox="0 0 260 135" style="max-width:100%;">
  <text x="4" y="14" font-size="12" fill="#6b7280">Angles sum to 180°</text>
  <polygon points="{p1x:.0f},{p1y:.0f} {p2x:.0f},{p2y:.0f} {p3x:.0f},{p3y:.0f}" fill="#fff7ed" stroke="#ea580c" stroke-width="2"/>
  <text x="{p1x - 8:.0f}" y="{p1y + 18:.0f}" font-size="13" font-weight="700" fill="#c2410c">{_esc(deg_a)}°</text>
  <text x="{p2x - 18:.0f}" y="{p2y + 18:.0f}" font-size="13" font-weight="700" fill="#c2410c">{_esc(deg_b)}°</text>
  <text x="{p3x - 14:.0f}" y="{p3y - 6:.0f}" font-size="13" font-weight="700" fill="#ea580c">?</text>
</svg>
""".strip()


def svg_circle_radius(r: int) -> str:
    """Circle with radius marked."""
    cx, cy = 90.0, 75.0
    rad = min(55, 12 + r * 3)
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="200" height="130" viewBox="0 0 200 130" style="max-width:100%;">
  <text x="4" y="14" font-size="12" fill="#6b7280">Circle, radius r</text>
  <circle cx="{cx:.0f}" cy="{cy:.0f}" r="{rad:.1f}" fill="#f0f9ff" stroke="#0369a1" stroke-width="2"/>
  <line x1="{cx:.1f}" y1="{cy:.1f}" x2="{cx + rad:.1f}" y2="{cy:.1f}" stroke="#0284c7" stroke-width="2"/>
  <text x="{cx + rad/2 - 8:.1f}" y="{cy - 8:.1f}" font-size="12" font-weight="600" fill="#0369a1">r = {_esc(r)}</text>
</svg>
""".strip()


def svg_area_model_split(a: int, b: int, c: int) -> str:
    """Visual: a×b and a×c as two side-by-side rectangles (mental factoring)."""
    w, h = 380, 120
    scale = min(80 / max(a, 1), 120 / max(b + c, 1))
    bw, bh2 = b * scale, c * scale
    ah = a * scale
    return f"""
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <text x="4" y="16" font-size="12" fill="#6b7280">Same height ×{a} — split the width ({b} + {c})</text>
  <rect x="20" y="28" width="{bw:.1f}" height="{ah:.1f}" fill="#bfdbfe" stroke="#2563eb" stroke-width="2"/>
  <rect x="{20 + bw:.1f}" y="28" width="{bh2:.1f}" height="{ah:.1f}" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
  <text x="{20 + bw/2:.1f}" y="{28 + ah/2 + 4:.1f}" text-anchor="middle" font-size="13" font-weight="600">{a}×{b}</text>
  <text x="{20 + bw + bh2/2:.1f}" y="{28 + ah/2 + 4:.1f}" text-anchor="middle" font-size="13" font-weight="600">{a}×{c}</text>
</svg>
""".strip()


def hint_svg_html(hint_meta: dict[str, Any]) -> str | None:
    """Return HTML wrapping an inline SVG, or None."""
    if not hint_meta:
        return None
    kind = hint_meta.get("kind")
    try:
        if kind == "number_line":
            svg = svg_number_line(
                float(hint_meta["min"]),
                float(hint_meta["max"]),
                [float(x) for x in hint_meta["points"]],
                hint_meta.get("labels"),
            )
        elif kind == "bar_percent":
            svg = svg_bar_percent(int(hint_meta["pct"]), hint_meta.get("caption", ""))
        elif kind == "bar_fraction":
            svg = svg_bar_fraction(
                int(hint_meta["num"]),
                int(hint_meta["den"]),
                hint_meta.get("of_total"),
            )
        elif kind == "area_model":
            svg = svg_area_model_split(
                int(hint_meta["a"]),
                int(hint_meta["b"]),
                int(hint_meta["c"]),
            )
        elif kind == "geo_rect_area":
            svg = svg_rectangle_lw(int(hint_meta["length"]), int(hint_meta["width"]))
        elif kind == "geo_triangle_area":
            svg = svg_triangle_bh(int(hint_meta["base"]), int(hint_meta["height"]))
        elif kind == "geo_rect_perimeter":
            svg = svg_rectangle_perimeter(int(hint_meta["length"]), int(hint_meta["width"]))
        elif kind == "geo_square":
            svg = svg_square_side(int(hint_meta["side"]), hint_meta.get("caption", ""))
        elif kind == "geo_find_width":
            svg = svg_rectangle_find_width(
                int(hint_meta["perimeter"]),
                int(hint_meta["length"]),
            )
        elif kind == "geo_triangle_angles_q":
            svg = svg_triangle_two_angles_known(
                int(hint_meta["angle_a"]),
                int(hint_meta["angle_b"]),
            )
        elif kind == "geo_triangle_angles_all":
            svg = svg_triangle_angles(
                int(hint_meta["angle_a"]),
                int(hint_meta["angle_b"]),
                int(hint_meta["angle_c"]),
            )
        elif kind == "geo_circle":
            svg = svg_circle_radius(int(hint_meta["radius"]))
        else:
            return None
    except (KeyError, TypeError, ValueError):
        return None
    return f'<div style="margin:0.5rem 0;">{svg}</div>'


def hf_prompt_for_diagram(hint_meta: dict[str, Any]) -> str:
    """Build a safe, educational prompt for text-to-image (no PII)."""
    kind = hint_meta.get("kind", "")
    if kind == "number_line":
        pts = hint_meta.get("points", [])
        return (
            "Clean educational math diagram: horizontal number line, ticks at "
            f"positions {pts}, minimalist black on white, no words, no letters, "
            "vector textbook style, high contrast, child-friendly"
        )
    if kind == "bar_percent":
        return (
            "Educational horizontal bar chart showing a percentage fill in green on gray, "
            f"approximately {hint_meta.get('pct', 0)} percent filled, simple flat design, "
            "white background, no text labels"
        )
    if kind == "bar_fraction":
        return (
            "Educational fraction bar model: rectangle divided into equal vertical sections, "
            f"{hint_meta.get('num', 0)} of {hint_meta.get('den', 1)} parts shaded blue, "
            "white background, no numbers printed, simple textbook diagram"
        )
    if kind == "area_model":
        return (
            "Two adjacent rectangles same height different widths, one light blue one light yellow, "
            "simple area model for multiplication, white background, no text, flat educational style"
        )
    if kind == "geo_rect_area":
        return (
            "Simple rectangle diagram labeled length and width, light blue fill, textbook geometry style, "
            "white background, minimal"
        )
    if kind == "geo_triangle_area":
        return (
            "Triangle with horizontal base and height shown as dashed line to top vertex, "
            "educational geometry diagram, white background, no text"
        )
    if kind == "geo_rect_perimeter":
        return (
            "Rectangle with all four sides labeled, purple outline, flat math textbook style, white background"
        )
    if kind == "geo_square":
        return (
            "Square shape with one side labeled, soft yellow fill, simple geometry diagram, white background"
        )
    if kind == "geo_find_width":
        return (
            "Rectangle diagram for perimeter problem, one side unknown question mark, green accent, "
            "educational, white background"
        )
    if kind in ("geo_triangle_angles_q", "geo_triangle_angles_all"):
        return (
            "Triangle with angle arcs at corners, orange outline, simple geometry textbook style, "
            "white background, no words"
        )
    if kind == "geo_circle":
        return (
            "Circle with radius line from center to edge, light blue fill, simple diagram, white background"
        )
    return (
        "Simple educational math diagram, white background, clean line art, no text, child-friendly"
    )


def generate_hf_diagram_image(prompt: str, api_key: str | None = None) -> bytes | None:
    """
    Generate a PNG using Hugging Face Inference API (FLUX.1-schnell).
    Returns PNG bytes or None on failure.
    """
    key = api_key or os.environ.get("HF_TOKEN")
    if not key:
        return None
    try:
        from huggingface_hub import InferenceClient
    except ImportError:
        return None
    try:
        client = InferenceClient(provider="auto", api_key=key)
        image = client.text_to_image(
            prompt[:500],
            model="black-forest-labs/FLUX.1-schnell",
            width=512,
            height=320,
        )
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        return buf.getvalue()
    except Exception:
        return None
