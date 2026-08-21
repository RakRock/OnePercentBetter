"""SVG geometry diagrams for Harshit PreReq 4 (Euclidean geometry)."""

from __future__ import annotations

import math
import re
from typing import Any


def _esc(text: Any) -> str:
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _svg_wrap(parts: list[str], *, w: int = 400, h: int = 260) -> str:
    head = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" style="max-width:100%;height:auto;display:block;margin:0 auto;">',
        f'<rect x="0" y="0" width="{w}" height="{h}" rx="12" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1"/>',
    ]
    return "\n".join(head + parts + ["</svg>"])


def _label(x: float, y: float, text: str, *, color: str = "#1e293b", size: int = 15, anchor: str = "middle") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" '
        f'fill="{color}" font-weight="600">{_esc(text)}</text>'
    )


def _polygon(points: list[tuple[float, float]], *, fill: str = "#dbeafe", stroke: str = "#2563eb") -> str:
    pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="2.5"/>'


def _segment(a: tuple[float, float], b: tuple[float, float], *, stroke: str = "#2563eb", dash: str = "") -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" '
        f'stroke="{stroke}" stroke-width="2.5"{dash_attr}/>'
    )


def _quad_labels(points: dict[str, tuple[float, float]]) -> list[str]:
    offsets = {"A": (0, 14), "B": (0, 14), "C": (0, -8), "D": (0, -8)}
    parts: list[str] = []
    for name, (x, y) in points.items():
        ox, oy = offsets.get(name, (0, 0))
        parts.append(_label(x + ox, y + oy, name))
    return parts


def svg_parallelogram(*, show_diagonals: bool = False) -> str:
    pts = {"A": (70, 190), "B": (290, 190), "C": (330, 90), "D": (110, 90)}
    parts = [_polygon([pts[k] for k in "ABCD"])]
    if show_diagonals:
        parts.append(_segment(pts["A"], pts["C"], stroke="#dc2626", dash="6 4"))
        parts.append(_segment(pts["B"], pts["D"], stroke="#059669", dash="6 4"))
    parts.extend(_quad_labels(pts))
    parts.append(_label(200, 24, "Parallelogram ABCD", size=12, color="#64748b"))
    return _svg_wrap(parts)


def svg_rectangle(*, show_diagonals: bool = False) -> str:
    pts = {"A": (90, 190), "B": (310, 190), "C": (310, 70), "D": (90, 70)}
    parts = [_polygon([pts[k] for k in "ABCD"])]
    if show_diagonals:
        parts.append(_segment(pts["A"], pts["C"], stroke="#dc2626", dash="6 4"))
    parts.extend(_quad_labels(pts))
    parts.append(_label(200, 24, "Rectangle ABCD", size=12, color="#64748b"))
    return _svg_wrap(parts)


def svg_rhombus(*, show_diagonals: bool = True) -> str:
    pts = {"A": (200, 45), "B": (320, 130), "C": (200, 215), "D": (80, 130)}
    parts = [_polygon([pts[k] for k in "ABCD"], fill="#ede9fe", stroke="#7c3aed")]
    if show_diagonals:
        parts.append(_segment(pts["A"], pts["C"], stroke="#dc2626", dash="6 4"))
        parts.append(_segment(pts["B"], pts["D"], stroke="#059669", dash="6 4"))
    parts.extend(_quad_labels(pts))
    parts.append(_label(200, 24, "Rhombus ABCD", size=12, color="#64748b"))
    return _svg_wrap(parts)


def svg_trapezium() -> str:
    pts = {"A": (80, 190), "B": (320, 190), "C": (280, 80), "D": (120, 80)}
    parts = [_polygon([pts[k] for k in "ABCD"], fill="#fef3c7", stroke="#d97706")]
    parts.extend(_quad_labels(pts))
    parts.append(_segment(pts["D"], pts["C"], stroke="#d97706"))
    parts.append(_label(200, 24, "Trapezium ABCD  (AB ∥ CD)", size=12, color="#64748b"))
    return _svg_wrap(parts)


def svg_triangle(
    *,
    angle_a: int | None = None,
    angle_b: int | None = None,
    midpoints: bool = False,
    exterior: bool = False,
) -> str:
    pts = {"A": (80, 200), "B": (320, 200), "C": (210, 55)}
    parts = [_polygon([pts[k] for k in "ABC"], fill="#dcfce7", stroke="#16a34a")]
    for name, (x, y) in pts.items():
        parts.append(_label(x, y + (14 if name != "C" else -10), name))
    if angle_a is not None:
        parts.append(_label(105, 185, f"{angle_a}°", size=13, color="#dc2626"))
    if angle_b is not None:
        parts.append(_label(295, 185, f"{angle_b}°", size=13, color="#dc2626"))
    if midpoints:
        e = ((pts["A"][0] + pts["B"][0]) / 2, (pts["A"][1] + pts["B"][1]) / 2)
        f = ((pts["A"][0] + pts["C"][0]) / 2, (pts["A"][1] + pts["C"][1]) / 2)
        parts.append(_segment(e, f, stroke="#dc2626"))
        parts.append(_label(e[0], e[1] + 16, "E", color="#dc2626"))
        parts.append(_label(f[0] - 14, f[1], "F", color="#dc2626"))
    if exterior:
        ext = (360, 200)
        parts.append(_segment(pts["B"], ext, stroke="#64748b"))
        parts.append(_label(345, 188, " exterior", size=11, color="#64748b", anchor="start"))
    parts.append(_label(200, 24, "△ABC", size=12, color="#64748b"))
    return _svg_wrap(parts)


def svg_circle(*, variant: str = "basic", angle: int | None = None, hide_center_label: bool = False) -> str:
    cx, cy, r = 200, 135, 78

    def _pt(deg: float) -> tuple[float, float]:
        rad = math.radians(deg)
        return cx + r * math.cos(rad), cy - r * math.sin(rad)

    if variant == "center_angle":
        central = int(angle or 90)
        a_deg = 215.0
        b_deg = a_deg + central
        ax, ay = _pt(a_deg)
        bx, by = _pt(b_deg)
        p_deg = a_deg + central / 2 + 180
        px, py = _pt(p_deg)
        parts = [
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#eff6ff" stroke="#2563eb" stroke-width="2.5"/>',
            _segment((cx, cy), (ax, ay), stroke="#2563eb"),
            _segment((cx, cy), (bx, by), stroke="#2563eb"),
            _segment((ax, ay), (bx, by), stroke="#7c3aed", dash="5 3"),
            _segment((px, py), (ax, ay), stroke="#94a3b8"),
            _segment((px, py), (bx, by), stroke="#94a3b8"),
            _label(cx - 10, cy + 6, "O"),
            _label(ax - 12, ay + 4, "A"),
            _label(bx + 10, by + 4, "B"),
            _label(px + 10, py - 6, "P", color="#dc2626"),
            _label(px - 8, py + 14, "?", color="#dc2626", size=17),
        ]
        if not hide_center_label and angle is not None:
            parts.append(_label(cx - 28, cy - 36, f"{central}°", color="#2563eb", size=13))
        parts.append(_label(200, 24, "Find ∠APB — P is on the major arc", size=12, color="#64748b"))
        return _svg_wrap(parts)

    parts = [
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#eff6ff" stroke="#2563eb" stroke-width="2.5"/>',
        _segment((cx, cy), (cx + r, cy), stroke="#dc2626"),
        _label(cx + r / 2, cy + 18, "r", color="#dc2626"),
        _label(cx - 6, cy + 6, "O"),
    ]
    if variant in ("chord", "cyclic"):
        ax, ay = _pt(-35)
        bx, by = _pt(145)
        parts.append(_segment((ax, ay), (bx, by), stroke="#7c3aed", dash="5 3"))
        parts.append(_label(ax + 8, ay, "A"))
        parts.append(_label(bx - 8, by, "B"))
    if variant == "cyclic":
        qx, qy = _pt(60)
        px, py = _pt(200)
        rx, ry = _pt(300)
        sx, sy = _pt(120)
        parts.append(_polygon([(px, py), (qx, qy), (rx, ry), (sx, sy)], fill="none", stroke="#059669"))
        parts.append(_label(200, 24, "Cyclic quadrilateral", size=12, color="#64748b"))
    else:
        parts.append(_label(200, 24, "Circle with centre O", size=12, color="#64748b"))
    return _svg_wrap(parts)


def svg_parallel_transversal(angle: int | None = None) -> str:
    parts = [
        _segment((50, 80), (350, 80)),
        _segment((50, 180), (350, 180)),
        _segment((120, 40), (280, 220), stroke="#dc2626"),
        _label(360, 84, "l", anchor="start"),
        _label(360, 184, "m", anchor="start"),
        _label(285, 228, "t", color="#dc2626", anchor="start"),
    ]
    if angle is not None:
        parts.append(_label(155, 168, f"{angle}°", color="#dc2626"))
    parts.append(_label(200, 24, "Parallel lines cut by a transversal", size=12, color="#64748b"))
    return _svg_wrap(parts)


def svg_intersecting_lines(angle_a: int | None = None, angle_b: int | None = None) -> str:
    parts = [
        _segment((80, 60), (320, 200)),
        _segment((320, 60), (80, 200)),
    ]
    if angle_a is not None:
        parts.append(_label(210, 118, f"{angle_a}°", color="#dc2626"))
    if angle_b is not None:
        parts.append(_label(175, 155, f"{angle_b}°", color="#2563eb"))
    parts.append(_label(200, 24, "Intersecting lines", size=12, color="#64748b"))
    return _svg_wrap(parts)


def svg_angle_arc(degrees: int) -> str:
    ox, oy = 120, 190
    parts = [
        _segment((ox, oy), (320, oy)),
        _segment((ox, oy), (280, 70), stroke="#dc2626"),
        f'<path d="M {ox + 50} {oy} A 50 50 0 0 0 {ox + 35} {oy - 35}" fill="none" stroke="#dc2626" stroke-width="2"/>',
        _label(ox + 55, oy - 25, f"{degrees}°", color="#dc2626"),
        _label(200, 24, "Angle", size=12, color="#64748b"),
    ]
    return _svg_wrap(parts)


def _parse_two_angles(text: str) -> tuple[int | None, int | None]:
    m = re.search(
        r"two angles are\s*(\d+)\s*°\s*and\s*(\d+)\s*°|"
        r"angles are\s*(\d+)\s*°\s*and\s*(\d+)\s*°",
        text,
        re.I,
    )
    if not m:
        return None, None
    groups = [g for g in m.groups() if g is not None]
    if len(groups) >= 2:
        return int(groups[0]), int(groups[1])
    return None, None


def _parse_one_angle(text: str) -> int | None:
    m = re.search(
        r"(?:angle measures|acute angle measures|interior angle is|one angle is|angle of)\s*(\d+)\s*°",
        text,
        re.I,
    )
    return int(m.group(1)) if m else None


def _angle_option_value(opt: str) -> float | None:
    m = re.search(r"(-?\d+(?:\.\d+)?)\s*°", str(opt))
    return float(m.group(1)) if m else None


def _half_angle_answer_index(options: list[str], center: int | float) -> int | None:
    target = float(center) / 2
    for i, opt in enumerate(options):
        val = _angle_option_value(opt)
        if val is not None and abs(val - target) < 0.01:
            return i
    return None


def fix_circle_center_angle_question(question: dict) -> dict:
    """Fix wrong answer keys and diagram labels for angle-at-centre vs circumference MCQs."""
    text = str(question.get("question", ""))
    lower = text.lower()
    if "subtended at the centre" not in lower or "half of this" not in lower:
        return question
    center = _parse_one_angle(text)
    if center is None:
        return question
    out = dict(question)
    opts = [str(o).strip() for o in out.get("options", [])]
    idx = _half_angle_answer_index(opts, center)
    if idx is not None:
        out["answer"] = idx
    spec = out.get("diagram")
    if isinstance(spec, dict) and spec.get("variant") == "center_angle":
        out["diagram"] = {**spec, "hide_center_label": True}
    return out


def infer_geometry_diagram(question: dict) -> dict | None:
    """Attach a geometry diagram to PreReq 4 questions from wording or topic."""
    if int(question.get("prereq_id", 0)) != 4:
        return None

    text = str(question.get("question", ""))
    lower = text.lower()
    topic = int(question.get("topic", 0))

    if "rhombus" in lower:
        return {"type": "rhombus", "show_diagonals": "diagonal" in lower}
    if "rectangle" in lower:
        return {"type": "rectangle", "show_diagonals": "diagonal" in lower}
    if "trapezium" in lower or "trapezoid" in lower:
        return {"type": "trapezium"}
    if "parallelogram" in lower or re.search(r"\babcd\b", lower):
        return {"type": "parallelogram", "show_diagonals": "diagonal" in lower}

    if re.search(r"triangle|δabc|△abc|△\s*abc", lower):
        a, b = _parse_two_angles(text)
        return {
            "type": "triangle",
            "angle_a": a,
            "angle_b": b,
            "midpoints": "mid-point" in lower or "midpoint" in lower,
            "exterior": "exterior angle" in lower,
        }

    if re.search(r"\bcircle\b|chord|radius|diameter|circumference|cyclic", lower):
        variant = "basic"
        if "cyclic" in lower:
            variant = "cyclic"
        elif "chord" in lower or "subtend" in lower:
            variant = "center_angle" if "centre" in lower or "center" in lower else "chord"
        angle = _parse_one_angle(text)
        hide_label = variant == "center_angle" and angle is not None and "half of this" in lower
        return {
            "type": "circle",
            "variant": variant,
            "angle": angle,
            "hide_center_label": hide_label,
        }

    if "parallel" in lower and ("transversal" in lower or "co-interior" in lower):
        return {"type": "parallel_transversal", "angle": _parse_one_angle(text)}

    if "vertically opposite" in lower or ("intersect" in lower and "angle" in lower):
        a = _parse_one_angle(text)
        b = None
        m = re.search(r"adjacent angle is\s*(\d+)\s*°", text, re.I)
        if m:
            b = int(m.group(1))
        return {"type": "intersecting_lines", "angle_a": a, "angle_b": b}

    deg = _parse_one_angle(text)
    if deg is not None and ("complement" in lower or "supplement" in lower or "angle" in lower):
        return {"type": "angle_arc", "degrees": deg}

    # Topic defaults for property-style questions without a named figure
    if topic == 4:
        return {"type": "circle", "variant": "basic"}
    if topic == 3:
        if "trapezium" in lower:
            return {"type": "trapezium"}
        return {"type": "parallelogram"}
    if topic == 2:
        return {"type": "triangle"}
    if topic == 1:
        return {"type": "angle_arc", "degrees": deg or 50}
    return None


def render_geometry_svg(spec: dict) -> str | None:
    kind = spec.get("type")
    if kind == "parallelogram":
        return svg_parallelogram(show_diagonals=bool(spec.get("show_diagonals")))
    if kind == "rectangle":
        return svg_rectangle(show_diagonals=bool(spec.get("show_diagonals")))
    if kind == "rhombus":
        return svg_rhombus(show_diagonals=bool(spec.get("show_diagonals", True)))
    if kind == "trapezium":
        return svg_trapezium()
    if kind == "triangle":
        return svg_triangle(
            angle_a=spec.get("angle_a"),
            angle_b=spec.get("angle_b"),
            midpoints=bool(spec.get("midpoints")),
            exterior=bool(spec.get("exterior")),
        )
    if kind == "circle":
        return svg_circle(
            variant=str(spec.get("variant", "basic")),
            angle=spec.get("angle"),
            hide_center_label=bool(spec.get("hide_center_label")),
        )
    if kind == "parallel_transversal":
        return svg_parallel_transversal(angle=spec.get("angle"))
    if kind == "intersecting_lines":
        return svg_intersecting_lines(angle_a=spec.get("angle_a"), angle_b=spec.get("angle_b"))
    if kind == "angle_arc":
        return svg_angle_arc(int(spec.get("degrees", 45)))
    return None
