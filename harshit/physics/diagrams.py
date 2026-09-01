"""NCERT-style labeled SVG diagrams for Harshit Physics Unit 1."""

from __future__ import annotations

import html as html_lib
import math
from typing import Any


def _esc(text: Any) -> str:
    return html_lib.escape(str(text))


def _svg_wrap(parts: list[str], *, w: int = 480, h: int = 280, title: str = "") -> str:
    head = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" style="max-width:100%;height:auto;display:block;margin:0 auto;">',
        f'<rect x="0" y="0" width="{w}" height="{h}" rx="10" fill="#ffffff" stroke="#d8dee6" stroke-width="1"/>',
    ]
    if title:
        head.append(
            f'<text x="{w/2:.1f}" y="22" text-anchor="middle" font-size="13" fill="#64748b" font-weight="600">{_esc(title)}</text>'
        )
    return "\n".join(head + parts + ["</svg>"])


def _label(x: float, y: float, text: str, *, color: str = "#1e293b", size: int = 12, anchor: str = "middle", bold: bool = False) -> str:
    weight = ' font-weight="700"' if bold else ""
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" fill="{color}"{weight}>{_esc(text)}</text>'


def _arrow(x1: float, y1: float, x2: float, y2: float, *, color: str = "#2563eb", width: float = 2.5, dash: str = "", marker: str = "arr") -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    marker_attr = f' marker-end="url(#{marker})"' if marker else ""
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width}"{marker_attr}{dash_attr}/>'
    )


def _defs(*markers: tuple[str, str]) -> str:
    default = markers or (("arr", "#2563eb"),)
    parts = ["<defs>"]
    for mid, color in default:
        parts.append(
            f'<marker id="{mid}" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
            f'<path d="M0,0 L6,3 L0,6 Z" fill="{color}"/></marker>'
        )
    parts.append("</defs>")
    return "".join(parts)


def _sun(x: float, y: float, *, r: float = 24, highlight: bool = False) -> str:
    stroke = "#6366f1" if highlight else "#f59e0b"
    sw = 3 if highlight else 2
    rays = ""
    for angle in range(0, 360, 45):
        rad = math.radians(angle)
        rays += (
            f'<line x1="{x + (r+4)*math.cos(rad):.1f}" y1="{y + (r+4)*math.sin(rad):.1f}" '
            f'x2="{x + (r+12)*math.cos(rad):.1f}" y2="{y + (r+12)*math.sin(rad):.1f}" '
            f'stroke="#fcd34d" stroke-width="2"/>'
        )
    return rays + f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="#fcd34d" stroke="{stroke}" stroke-width="{sw}"/>'


def _candle(x: float, y: float) -> str:
    return (
        f'<rect x="{x-6:.1f}" y="{y:.1f}" width="12" height="28" fill="#fef3c7" stroke="#d97706" stroke-width="1.5"/>'
        f'<ellipse cx="{x:.1f}" cy="{y-4:.1f}" rx="8" ry="12" fill="#fb923c" opacity="0.85"/>'
        f'<ellipse cx="{x:.1f}" cy="{y-10:.1f}" rx="4" ry="8" fill="#fbbf24"/>'
    )


def _eye(x: float, y: float, *, highlight: bool = False) -> str:
    stroke = "#6366f1" if highlight else "#64748b"
    sw = 2.5 if highlight else 1.5
    return (
        f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="28" ry="16" fill="#f8fafc" stroke="{stroke}" stroke-width="{sw}"/>'
        f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="#1e293b"/>'
        f'<circle cx="{x+3:.1f}" cy="{y-3:.1f}" r="3" fill="#ffffff"/>'
    )


def _book(x: float, y: float, *, highlight: bool = False) -> str:
    stroke = "#6366f1" if highlight else "#475569"
    return (
        f'<rect x="{x-22:.1f}" y="{y-16:.1f}" width="44" height="32" rx="3" fill="#94a3b8" stroke="{stroke}" stroke-width="2"/>'
        f'<line x1="{x:.1f}" y1="{y-16:.1f}" x2="{x:.1f}" y2="{y+16:.1f}" stroke="#64748b" stroke-width="1.5"/>'
    )


def svg_light_source_model(cfg: dict) -> str:
    hl = cfg.get("highlight", "")
    parts = [_defs(("arr", "#2563eb"), ("arrG", "#059669"))]
    parts.append(_sun(70, 130, highlight=hl == "source"))
    parts.append(_label(70, 168, "Luminous source", color="#b45309", bold=True))
    parts.append(_label(70, 182, "(emits own light)", size=10, color="#64748b"))
    parts.append(_book(230, 130, highlight=hl == "reflector"))
    parts.append(_label(230, 168, "Object", bold=True))
    parts.append(_label(230, 182, "(non-luminous)", size=10, color="#64748b"))
    parts.append(_arrow(98, 130, 205, 130, color="#2563eb", marker="arr"))
    parts.append(_label(150, 118, "incident light", size=10, color="#2563eb"))
    if hl == "reflector" or hl != "arrow_from_source":
        parts.append(_arrow(252, 130, 340, 130, color="#059669", marker="arrG"))
        parts.append(_label(295, 118, "reflected light", size=10, color="#059669"))
    parts.append(_eye(400, 130))
    parts.append(_label(400, 168, "Eye", bold=True))
    return _svg_wrap(parts, title="How we see objects")


def svg_eye_light_path(cfg: dict) -> str:
    mode = cfg.get("mode", "")
    hl = cfg.get("highlight", "")
    if mode == "dark":
        parts = [
            '<rect x="20" y="40" width="440" height="200" rx="8" fill="#1e293b"/>',
            _label(240, 120, "No light → nothing visible", color="#94a3b8", size=14, bold=True),
            _label(240, 145, "Light must enter the eye to see", color="#64748b", size=11),
        ]
        return _svg_wrap(parts, h=260, title="Darkness")
    parts = [_defs(("arr", "#2563eb"), ("arrG", "#059669"))]
    parts.append(_sun(55, 130, highlight=False))
    parts.append(_book(200, 130))
    parts.append(_eye(380, 130, highlight=hl == "eye"))
    if mode == "full_path" or hl == "path":
        parts.append(_arrow(82, 130, 175, 130, color="#2563eb"))
        parts.append(_label(128, 115, "① source", size=10, color="#2563eb"))
        parts.append(_arrow(222, 130, 348, 130, color="#059669", marker="arrG"))
        parts.append(_label(285, 115, "② reflects  →  ③ eye", size=10, color="#059669"))
    else:
        parts.append(_arrow(82, 130, 175, 130))
        parts.append(_arrow(222, 130, 348, 130, color="#059669", marker="arrG"))
    parts.append(_label(240, 200, "Source  →  Object  →  Eye", bold=True, color="#334155"))
    return _svg_wrap(parts, title="Path of light")


def svg_straight_ray(cfg: dict) -> str:
    mode = cfg.get("mode", "straight")
    hl = cfg.get("highlight", "")
    parts = [_defs(("arr", "#2563eb"), ("arrG", "#059669"))]
    if mode == "reflect":
        parts.append('<line x1="300" y1="40" x2="300" y2="220" stroke="#94a3b8" stroke-width="6"/>')
        parts.append(_label(300, 235, "Mirror", size=10))
        parts.append(_arrow(50, 170, 300, 130, color="#2563eb"))
        parts.append(_label(160, 158, "incident", size=10, color="#2563eb"))
        col = "#059669" if hl == "reflected_ray" else "#059669"
        w = 3.5 if hl == "reflected_ray" else 2.5
        parts.append(_arrow(300, 130, 430, 70, color=col, width=w, marker="arrG"))
        parts.append(_label(370, 88, "reflected", size=10, color="#059669"))
    elif mode == "beam":
        for dy in (-15, 0, 15):
            parts.append(_arrow(40, 130 + dy, 420, 130 + dy, color="#2563eb", width=1.8))
        parts.append(_label(240, 95, "Beam = many parallel rays", bold=True, color="#334155"))
    else:
        parts.append(_arrow(40, 130, 420, 130, color="#2563eb", width=3 if hl == "ray" else 2.5))
        parts.append(_label(240, 115, "Ray of light (straight line + arrow)", size=11, color="#334155"))
    return _svg_wrap(parts, title="Light travels in straight lines")


def _hatched_plane_mirror(x: float = 280, y1: float = 36, y2: float = 250) -> list[str]:
    """Vertical plane mirror, hatch on the non-reflecting (right) side — NCERT Fig 9.1 style."""
    parts = [f'<line x1="{x:.0f}" y1="{y1:.0f}" x2="{x:.0f}" y2="{y2:.0f}" stroke="#334155" stroke-width="3.2"/>']
    for y in range(int(y1) + 8, int(y2), 12):
        parts.append(f'<line x1="{x:.0f}" y1="{y}" x2="{x + 10:.0f}" y2="{y - 8}" stroke="#64748b" stroke-width="1.3"/>')
    parts.append(_label(x, y2 + 16, "M", size=11, bold=True))
    return parts


def svg_plane_mirror_reflection(cfg: dict) -> str:
    hl = cfg.get("highlight", "")
    mode = cfg.get("mode", "")
    mx = 280
    if mode == "image_properties":
        parts = _hatched_plane_mirror(mx, 40, 240)
        parts.extend(_axis_arrow(160, 180, 120, color="#1d4ed8", tip_label="A", base_label="B"))
        parts.extend(_axis_arrow(400, 180, 120, color="#dc2626", dash="4,3", tip_label="A′", base_label="B′"))
        parts.append(_label(160, 210, "Object", size=10, color="#1d4ed8", bold=True))
        parts.append(_label(400, 210, "Virtual image", size=10, color="#dc2626", bold=True))
        parts.append(_label(280, 268, "Same size · erect · as far behind as object is in front", size=11, color="#334155"))
        return _svg_wrap(parts, w=560, h=300, title="Plane mirror image")
    parts = [_defs(("arr", "#2563eb"), ("arrG", "#059669"))]
    parts.extend(_hatched_plane_mirror(mx, 36, 240))
    parts.append(_arrow(mx, 140, mx, 50, color="#64748b", width=1.5, dash="5,4"))
    parts.append(_label(mx + 14, 90, "Normal", size=10, color="#64748b", anchor="start"))
    inc_w = 3.5 if hl == "incident" else 2.2
    ref_w = 3.5 if hl == "reflected" else 2.2
    parts.append(_arrow(70, 200, mx, 140, color="#2563eb", width=inc_w))
    parts.append(_label(140, 188, "Incident ray", size=10, color="#2563eb"))
    parts.append(_arrow(mx, 140, 490, 80, color="#059669", width=ref_w, marker="arrG"))
    parts.append(_label(400, 96, "Reflected ray", size=10, color="#059669"))
    if hl == "incidence_point":
        parts.append(f'<circle cx="{mx}" cy="140" r="6" fill="#6366f1"/>')
        parts.append(_label(mx, 162, "Point of incidence", size=10, color="#6366f1", bold=True))
    if hl == "surface":
        parts.append(_label(mx + 36, 60, "Reflecting surface", size=10, color="#6366f1", bold=True, anchor="start"))
    if hl == "same_plane" or mode == "3d_hint":
        parts.append(_label(280, 268, "Incident ray, reflected ray and normal lie in one plane", size=11, color="#334155", bold=True))
    return _svg_wrap(parts, w=560, h=300, title="Reflection at a plane mirror")


def svg_normal_angle(cfg: dict) -> str:
    hl = cfg.get("highlight", "")
    mx = 280
    parts = [_defs(("arr", "#2563eb"), ("arrG", "#059669"))]
    parts.extend(_hatched_plane_mirror(mx, 36, 230))
    n_stroke = "#6366f1" if hl == "normal" else "#64748b"
    n_w = 2.6 if hl == "normal" else 1.5
    parts.append(_arrow(mx, 210, mx, 48, color=n_stroke, width=n_w, dash="6,4"))
    parts.append(_label(mx + 14, 120, "Normal (90° to mirror)", size=10, color=n_stroke, anchor="start"))
    parts.append(_arrow(60, 210, mx, 140, color="#2563eb", width=3.2 if hl == "angle_i" else 2.2))
    parts.append(_arrow(mx, 140, 500, 70, color="#059669", width=3.2 if hl == "angle_r" else 2.2, marker="arrG"))
    parts.append(f'<path d="M{mx},140 L{mx},108 A32,32 0 0,0 252,124" fill="none" stroke="#2563eb" stroke-width="2"/>')
    parts.append(f'<path d="M{mx},140 L{mx},108 A32,32 0 0,1 308,124" fill="none" stroke="#059669" stroke-width="2"/>')
    parts.append(_label(258, 118, "i", color="#2563eb", bold=True))
    parts.append(_label(298, 118, "r", color="#059669", bold=True))
    if cfg.get("show_labels") or hl == "equal_angles":
        parts.append(_label(280, 260, "Angle of incidence i = angle of reflection r", bold=True, color="#334155", size=11))
    return _svg_wrap(parts, w=560, h=290, title="Measure angles from the normal")


def svg_spherical_mirror_labels(cfg: dict) -> str:
    mtype = cfg.get("mirror_type", "concave")
    hl = cfg.get("highlight", "")
    concave = str(mtype) != "convex"
    if cfg.get("mode") == "compare":
        parts = [_defs()]
        parts.append(_label(120, 210, "Concave (inward)", bold=True, size=11))
        parts.append(_label(400, 210, "Convex (outward)", bold=True, size=11))
        # Two compact side-view sketches sharing the NCERT orientation.
        parts.append('<polyline points="80,70 100,90 110,120 100,150 80,170" fill="none" stroke="#334155" stroke-width="3"/>')
        for y1, y2 in ((74, 64), (90, 82), (120, 120), (150, 158), (166, 176)):
            parts.append(f'<line x1="100" y1="{y1}" x2="112" y2="{y2}" stroke="#64748b" stroke-width="1.2"/>')
        parts.append('<line x1="30" y1="120" x2="200" y2="120" stroke="#94a3b8"/>')
        parts.append(_label(110, 136, "P", size=10, bold=True))
        parts.append(_label(80, 136, "F", size=10, bold=True))
        parts.append(_label(50, 136, "C", size=10, bold=True))
        parts.append('<polyline points="400,70 380,90 370,120 380,150 400,170" fill="none" stroke="#334155" stroke-width="3"/>')
        for y1, y2 in ((74, 64), (90, 82), (120, 120), (150, 158), (166, 176)):
            parts.append(f'<line x1="380" y1="{y1}" x2="392" y2="{y2}" stroke="#64748b" stroke-width="1.2"/>')
        parts.append('<line x1="280" y1="120" x2="450" y2="120" stroke="#94a3b8"/>')
        parts.append(_label(370, 136, "P", size=10, bold=True))
        parts.append(_label(400, 136, "F", size=10, bold=True))
        parts.append(_label(430, 136, "C", size=10, bold=True))
        parts.append(_label(240, 230, "Side view — same as the NCERT ray diagrams", size=10, color="#64748b"))
        return _svg_wrap(parts, h=260, title="Compare mirror types")
    g = _ncert_axis_geom(concave=concave)
    parts = _ncert_mirror_arc(g, concave=concave)
    ay, px, fx, cx = g["ay"], g["px"], g["fx"], g["cx"]
    if hl == "principal_axis":
        parts.append(f'<line x1="28" y1="{ay:.1f}" x2="548" y2="{ay:.1f}" stroke="#6366f1" stroke-width="2.6"/>')
        parts.append(_label(90, 70, "Principal axis", size=12, color="#6366f1", bold=True))
    if hl in ("P", "F", "C"):
        x = {"P": px, "F": fx, "C": cx}[hl]
        parts.append(f'<circle cx="{x:.1f}" cy="{ay:.1f}" r="7" fill="none" stroke="#6366f1" stroke-width="2"/>')
        names = {"P": "Pole P — midpoint of the mirror", "F": "Principal focus F", "C": "Centre of curvature C"}
        parts.append(_label(150, 52, names[hl], size=12, color="#6366f1", bold=True))
    if hl in ("R",) or cfg.get("show_R_segment"):
        parts.append(f'<line x1="{cx:.1f}" y1="{ay + 28:.1f}" x2="{px:.1f}" y2="{ay + 28:.1f}" stroke="#6366f1" stroke-width="2"/>')
        parts.append(_label((cx + px) / 2, ay + 46, "R = 2f", size=12, color="#6366f1", bold=True))
    if hl == "aperture":
        parts.append(f'<line x1="368" y1="48" x2="368" y2="288" stroke="#6366f1" stroke-width="1.6" stroke-dasharray="4,3"/>')
        parts.append(_label(150, 52, "Aperture = opening MN", size=12, color="#6366f1", bold=True))
    if hl in ("reflecting_side", "reflecting_inward", "curved_surface"):
        parts.append(_label(150, 52, "Inner face is the reflecting surface", size=12, color="#6366f1", bold=True))
    if hl == "reflecting_outward":
        parts.append(_label(200, 52, "Outer bulge is the reflecting surface", size=12, color="#6366f1", bold=True))
    parts.append(_label(280, 326, "Principal axis · P pole · F focus · C centre  (R = 2f)", size=11, color="#334155"))
    title = "Concave mirror" if concave else "Convex mirror"
    return _svg_wrap(parts, w=560, h=340, title=title)


def svg_mirror_focus_ray(cfg: dict) -> str:
    mtype = cfg.get("mirror_type", "concave")
    hl = cfg.get("highlight", "")
    concave = str(mtype) != "convex"
    g = _ncert_axis_geom(concave=concave)
    ay, px, fx, cx, r = g["ay"], g["px"], g["fx"], g["cx"], g["R"]
    side = int(g["side"])
    parts = [_defs(("arr", "#2563eb"), ("arrG", "#059669"))]
    parts.extend(_ncert_mirror_arc(g, concave=concave))
    for yoff in (-28, 28):
        y = ay + yoff
        hx = _circ_x_at_y(cx, ay, r, y, side=side)
        if hx is None:
            continue
        parts.append(_clipped_ray(40, y, hx, y, color="#2563eb"))
        if concave:
            parts.append(_clipped_ray(hx, y, fx, ay, color="#059669", marker="arrG"))
        else:
            left = _extend_to_x(hx, y, hx - 50, y - 1.2 * yoff, 36)
            parts.append(_clipped_ray(hx, y, left[0], left[1], color="#059669", marker="arrG"))
            parts.append(_arrow(hx, y, fx, ay, color="#2563eb", dash="5,4", marker=""))
    notes = {
        "F": "F is the principal focus",
        "f_segment": "Focal length f = PF",
        "real_focus": "Concave: rays actually meet at F (real focus)",
        "virtual_focus": "Convex: rays only appear to come from F (virtual focus)",
        "converging": "Concave mirror is converging",
        "diverging": "Convex mirror is diverging",
        "parallel_incident": "Incident rays are parallel to the principal axis",
        "reflected": "After reflection the rays follow the focus rule",
        "R_2f": "Radius R = PC = 2f",
        "P_F_C": "F lies midway between P and C",
    }
    if hl in notes:
        parts.append(_label(200, 52, notes[hl], size=12, color="#6366f1", bold=True))
    elif concave:
        parts.append(_label(200, 70, "Parallel rays meet at F", size=11, color="#059669", bold=True))
    else:
        parts.append(_label(280, 70, "Rays diverge — appear to come from F", size=11, color="#059669", bold=True))
    if hl in ("R_2f", "P_F_C", "f_segment") or cfg.get("show_segments"):
        parts.append(f'<line x1="{min(px, cx):.1f}" y1="{ay + 30:.1f}" x2="{max(px, cx):.1f}" y2="{ay + 30:.1f}" stroke="#6366f1" stroke-width="1.8"/>')
        parts.append(_label((px + cx) / 2, ay + 48, "R = 2f", size=12, color="#334155", bold=True))
    if cfg.get("mode") == "both":
        parts.append(_label(280, 326, "Concave meets at F · convex appears to come from F", size=11, color="#334155"))
    return _svg_wrap(parts, w=560, h=340, title="Focus and parallel rays")


def _ncert_axis_geom(*, concave: bool = True) -> dict[str, float]:
    """NCERT Fig 9.7 layout: object on the left, mirror on the right, R = 2f."""
    ay = 168.0
    f = 78.0
    if concave:
        px = 428.0
        cx = px - 2 * f
        fx = px - f
        side = "right"
    else:
        px = 148.0
        cx = px + 2 * f
        fx = px + f
        side = "left"
    return {"ay": ay, "f": f, "px": px, "cx": cx, "fx": fx, "R": 2 * f, "side": 1 if side == "right" else -1}


def _circ_x_at_y(cx: float, ay: float, r: float, y: float, *, side: int) -> float | None:
    dy = y - ay
    disc = r * r - dy * dy
    if disc < 1:
        return None
    return cx + side * math.sqrt(disc)


def _intersect_lines(
    x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, x4: float, y4: float
) -> tuple[float, float] | None:
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(den) < 1e-8:
        return None
    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / den
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / den
    return px, py


def _line_circle_hit(
    x1: float, y1: float, x2: float, y2: float, cx: float, ay: float, r: float, *, min_t: float = 1.02
) -> tuple[float, float] | None:
    dx, dy = x2 - x1, y2 - y1
    fx, fy = x1 - cx, y1 - ay
    a = dx * dx + dy * dy
    if a < 1e-9:
        return None
    b = 2 * (fx * dx + fy * dy)
    c = fx * fx + fy * fy - r * r
    disc = b * b - 4 * a * c
    if disc < 0:
        return None
    root = math.sqrt(disc)
    hits = [(-b + root) / (2 * a), (-b - root) / (2 * a)]
    ts = [t for t in hits if t >= min_t]
    if not ts:
        return None
    t = min(ts)
    return x1 + t * dx, y1 + t * dy


def _line_circle_first_hit(
    x1: float, y1: float, x2: float, y2: float, cx: float, ay: float, r: float, *, min_t: float = 0.02
) -> tuple[float, float] | None:
    """Nearest intersection in the forward direction — the reflecting surface."""
    return _line_circle_hit(x1, y1, x2, y2, cx, ay, r, min_t=min_t)


def _extend_to_x(x1: float, y1: float, x2: float, y2: float, x: float) -> tuple[float, float]:
    dx = x2 - x1
    if abs(dx) < 1e-8:
        return x1, y1
    t = (x - x1) / dx
    return x, y1 + t * (y2 - y1)


def _clamp_seg(x1: float, y1: float, x2: float, y2: float, *, x_lo: float = 24, x_hi: float = 536, y_lo: float = 36, y_hi: float = 308) -> tuple[float, float, float, float]:
    """Clip a segment so both ends stay inside the diagram frame."""
    dx, dy = x2 - x1, y2 - y1
    if abs(dx) < 1e-9 and abs(dy) < 1e-9:
        return x1, y1, x2, y2
    t0, t1 = 0.0, 1.0
    for p, q, lo, hi in ((dx, x1, x_lo, x_hi), (dy, y1, y_lo, y_hi)):
        if abs(p) < 1e-9:
            if q < lo or q > hi:
                return x1, y1, x1, y1
            continue
        t_enter = (lo - q) / p
        t_leave = (hi - q) / p
        if t_enter > t_leave:
            t_enter, t_leave = t_leave, t_enter
        t0 = max(t0, t_enter)
        t1 = min(t1, t_leave)
    if t1 < t0:
        return x1, y1, x1, y1
    return x1 + t0 * dx, y1 + t0 * dy, x1 + t1 * dx, y1 + t1 * dy


def _ray_line(
    x1: float, y1: float, x2: float, y2: float, *, color: str = "#2563eb", width: float = 1.8, dash: str = "", marker: str = "arr"
) -> str:
    return _arrow(x1, y1, x2, y2, color=color, width=width, dash=dash, marker=marker)


def _axis_arrow(
    x: float,
    y0: float,
    y1: float,
    *,
    color: str,
    dash: str = "",
    tip_label: str = "",
    base_label: str = "",
    label: str = "",
) -> list[str]:
    parts = [
        f'<line x1="{x:.1f}" y1="{y0:.1f}" x2="{x:.1f}" y2="{y1:.1f}" '
        f'stroke="{color}" stroke-width="2.4"{" stroke-dasharray=\"" + dash + "\"" if dash else ""}/>'
    ]
    tip = -1 if y1 < y0 else 1
    parts.append(
        f'<polygon points="{x-5:.1f},{y1 + 10 * tip:.1f} {x:.1f},{y1:.1f} {x+5:.1f},{y1 + 10 * tip:.1f}" fill="{color}"/>'
    )
    if tip_label:
        parts.append(_label(x - 10, y1 + (4 if y1 < y0 else 16), tip_label, size=11, color=color, bold=True, anchor="end"))
    if base_label:
        parts.append(_label(x - 10, y0 + 20, base_label, size=11, color=color, bold=True, anchor="end"))
    if label and not tip_label:
        parts.append(_label(x + 12, min(y0, y1) - 4 if y1 < y0 else max(y0, y1) + 14, label, size=11, color=color, bold=True, anchor="start"))
    return parts


def _clipped_ray(x1: float, y1: float, x2: float, y2: float, **kwargs) -> str:
    cx1, cy1, cx2, cy2 = _clamp_seg(x1, y1, x2, y2)
    return _arrow(cx1, cy1, cx2, cy2, **kwargs)


def _ncert_mirror_arc(g: dict, *, concave: bool) -> list[str]:
    cx, ay, r, px = g["cx"], g["ay"], g["R"], g["px"]
    span = 52 if concave else 52
    pts = []
    for deg in range(-span, span + 1, 2):
        rad = math.radians(deg)
        # Concave: P is the rightmost point of the circle (opens left). Convex: leftmost (bulges left).
        if concave:
            x = cx + r * math.cos(rad)
            y = ay + r * math.sin(rad)
        else:
            x = cx - r * math.cos(rad)
            y = ay + r * math.sin(rad)
        pts.append(f"{x:.1f},{y:.1f}")
    parts = [f'<polyline points="{" ".join(pts)}" fill="none" stroke="#334155" stroke-width="3.2"/>']
    # Hatch marks on the non-reflecting side (NCERT style).
    for deg in range(-span + 4, span, 8):
        rad = math.radians(deg)
        if concave:
            x = cx + r * math.cos(rad)
            y = ay + r * math.sin(rad)
            hx, hy = x + 9 * math.cos(rad), y + 9 * math.sin(rad)
        else:
            x = cx - r * math.cos(rad)
            y = ay + r * math.sin(rad)
            # Non-reflecting side is behind the bulge (to the right of P).
            hx, hy = x + 9 * math.cos(rad), y + 9 * math.sin(rad)
        parts.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="#64748b" stroke-width="1.4"/>')
    top = pts[0].split(",")
    bot = pts[-1].split(",")
    parts.append(_label(float(top[0]), float(top[1]) - 8, "M", size=11, bold=True))
    parts.append(_label(float(bot[0]), float(bot[1]) + 16, "N", size=11, bold=True))
    parts.append(f'<line x1="28" y1="{ay:.1f}" x2="548" y2="{ay:.1f}" stroke="#94a3b8" stroke-width="1.4"/>')
    for name, x, dy in (("C", g["cx"], 16), ("F", g["fx"], 16), ("P", px, 16)):
        parts.append(f'<circle cx="{x:.1f}" cy="{ay:.1f}" r="3.4" fill="#1e293b"/>')
        parts.append(_label(x, ay + dy, name, size=12, bold=True))
    return parts


def _normalize_mirror_position(raw: str) -> str:
    key = str(raw or "beyond_c").strip().lower().replace(" ", "_")
    aliases = {
        "beyond_c": "beyond_C",
        "at_c": "at_C",
        "between_c_f": "between_C_F",
        "at_f": "at_F",
        "between_f_p": "between_F_P",
        "between_p_f": "between_F_P",
        "infinity": "infinity",
    }
    return aliases.get(key, raw if raw in aliases.values() else aliases.get(key, "beyond_C"))


def _svg_table_9_1() -> str:
    """NCERT Table 9.1 — image formation by a concave mirror."""
    rows = [
        ("Object", "Image", "Size", "Nature"),
        ("At infinity", "At F", "Point-sized", "Real, inverted"),
        ("Beyond C", "Between F and C", "Diminished", "Real, inverted"),
        ("At C", "At C", "Same size", "Real, inverted"),
        ("Between C and F", "Beyond C", "Enlarged", "Real, inverted"),
        ("At F", "At infinity", "Highly enlarged", "Real, inverted"),
        ("Between F and P", "Behind mirror", "Enlarged", "Virtual, erect"),
    ]
    parts = ['<rect x="24" y="40" width="512" height="268" rx="8" fill="#f8fafc" stroke="#cbd5e1"/>']
    y = 68
    for i, cols in enumerate(rows):
        weight = True if i == 0 else False
        color = "#0f172a" if i == 0 else "#334155"
        xs = (70, 200, 340, 460)
        if i == 0:
            parts.append(f'<rect x="24" y="40" width="512" height="36" fill="#e2e8f0"/>')
        for x, text in zip(xs, cols):
            parts.append(_label(x, y, text, size=11, color=color, bold=weight))
        y += 34
    parts.append(_label(280, 326, "NCERT Table 9.1 — move the object from infinity toward P", size=11, color="#334155"))
    return _svg_wrap(parts, w=560, h=340, title="Image formation by a concave mirror")


def _mirror_formula(px: float, ox: float, f_signed: float) -> tuple[float | None, float]:
    """NCERT signs: u is negative on the object side. Returns (v, m) or (None, 0) at infinity."""
    u = -(px - ox)
    if abs(u) < 1e-6:
        return None, 0.0
    inv_v = (1 / f_signed) - (1 / u)
    if abs(inv_v) < 1e-5:
        return None, 0.0
    v = 1 / inv_v
    return v, -v / u


def svg_concave_image(cfg: dict) -> str:
    """NCERT Fig 9.7 / 9.8 ray diagram for one object position."""
    mtype = str(cfg.get("mirror_type", "concave")).lower()
    concave = mtype != "convex"
    highlight = str(cfg.get("highlight") or "")
    mode = str(cfg.get("mode") or "")
    if mode == "sequence":
        return _svg_table_9_1()
    default_pos = "between_F_P" if highlight in ("virtual", "erect", "behind") else "between_C_F"
    position = _normalize_mirror_position(str(cfg.get("position") or cfg.get("case") or default_pos))
    g = _ncert_axis_geom(concave=concave)
    ay, px, cx, fx, r = g["ay"], g["px"], g["cx"], g["fx"], g["R"]
    side = int(g["side"])
    h_obj = 46.0
    ay_tip = ay - h_obj

    captions = {
        "infinity": "Object at infinity: image at F (highly diminished, real)",
        "beyond_C": "Object beyond C: image between F and C (diminished, real, inverted)",
        "at_C": "Object at C: image at C (same size, real, inverted)",
        "between_C_F": "Object between C and F: image beyond C (enlarged, real, inverted)",
        "at_F": "Object at F: reflected rays are parallel (image at infinity)",
        "between_F_P": "Object between F and P: virtual, erect, enlarged image behind the mirror",
    }
    convex_caption = "Convex mirror: virtual, erect, diminished image behind the mirror"

    parts = [_defs(("arr", "#2563eb"), ("arrR", "#dc2626"), ("arrG", "#059669"))]
    parts.extend(_ncert_mirror_arc(g, concave=concave))

    if not concave:
        ox = 70.0
        v, m = _mirror_formula(px, ox, abs(g["f"]))
        ix = px + (v or 40.0)
        ih = h_obj * m
        h1x = _circ_x_at_y(cx, ay, r, ay_tip, side=side) or px
        parts.extend(_axis_arrow(ox, ay, ay_tip, color="#1d4ed8", tip_label="A", base_label="B"))
        parts.append(_clipped_ray(ox, ay_tip, h1x, ay_tip, color="#2563eb"))
        left = _extend_to_x(h1x, ay_tip, h1x - 40, ay_tip - 28, 36)
        parts.append(_clipped_ray(h1x, ay_tip, left[0], left[1], color="#2563eb"))
        parts.append(_arrow(h1x, ay_tip, fx, ay, color="#2563eb", dash="5,4", marker=""))
        hit_c = _line_circle_first_hit(ox, ay_tip, cx, ay, cx, ay, r)
        if hit_c:
            parts.append(_clipped_ray(ox, ay_tip, hit_c[0], hit_c[1], color="#0f766e"))
            back = _extend_to_x(hit_c[0], hit_c[1], ox, ay_tip, 36)
            parts.append(_clipped_ray(hit_c[0], hit_c[1], back[0], back[1], color="#0f766e"))
            parts.append(_arrow(hit_c[0], hit_c[1], cx, ay, color="#0f766e", dash="5,4", marker=""))
        parts.extend(_axis_arrow(ix, ay, ay - ih, color="#dc2626", dash="4,3", tip_label="A′", base_label="B′"))
        extra = {
            "behind": "Image always lies behind the mirror",
            "erect": "Image is always erect",
            "diminished": "Image is always diminished",
            "wide_view": "Wide field of view — more of the scene fits in",
            "object_move": "Move the object: nature stays virtual, erect, diminished",
        }.get(highlight or mode, "")
        if extra:
            parts.append(_label(200, 52, extra, size=12, color="#6366f1", bold=True))
        parts.append(_label(280, 326, convex_caption, size=11, color="#334155"))
        return _svg_wrap(parts, w=560, h=340, title="Image formation by a convex mirror")

    obj_x = {
        "infinity": None,
        "beyond_C": cx - 88,
        "at_C": cx,
        "between_C_F": (cx + fx) / 2,
        "at_F": fx,
        "between_F_P": (fx + px) / 2,
    }
    ox = obj_x.get(position)

    if position == "infinity" or ox is None:
        for yoff in (-36, -18, 18, 36):
            y = ay + yoff
            hx = _circ_x_at_y(cx, ay, r, y, side=side)
            if hx is None:
                continue
            parts.append(_clipped_ray(36, y, hx, y, color="#2563eb"))
            parts.append(_clipped_ray(hx, y, fx, ay, color="#2563eb"))
        parts.append(f'<circle cx="{fx:.1f}" cy="{ay:.1f}" r="5" fill="#dc2626"/>')
        parts.append(_label(fx, ay - 14, "A′B′ at F", size=10, color="#dc2626", bold=True))
        parts.append(_label(280, 326, captions["infinity"], size=11, color="#334155"))
        return _svg_wrap(parts, w=560, h=340, title="Image formation by a concave mirror")

    parts.extend(_axis_arrow(ox, ay, ay_tip, color="#1d4ed8", tip_label="A", base_label="B"))
    h1x = _circ_x_at_y(cx, ay, r, ay_tip, side=side)

    if position == "at_F":
        # Fig 9.7(e): reflected rays do not meet. Parallel incident + ray along C–A.
        if h1x is not None:
            parts.append(_clipped_ray(ox, ay_tip, h1x, ay_tip, color="#2563eb"))
            through_f = _extend_to_x(h1x, ay_tip, fx, ay, 36)
            parts.append(_clipped_ray(h1x, ay_tip, through_f[0], through_f[1], color="#2563eb"))
        hit_c = _line_circle_hit(cx, ay, ox, ay_tip, cx, ay, r, min_t=1.02)
        if hit_c:
            parts.append(_clipped_ray(ox, ay_tip, hit_c[0], hit_c[1], color="#0f766e"))
            back = _extend_to_x(hit_c[0], hit_c[1], cx, ay, 36)
            parts.append(_clipped_ray(hit_c[0], hit_c[1], back[0], back[1], color="#0f766e"))
        parts.append(_label(118, 70, "Reflected rays are parallel", size=11, color="#dc2626", bold=True))
        parts.append(_label(118, 88, "Image at infinity", size=11, color="#dc2626"))
    elif position == "between_F_P":
        # Fig 9.7(f): through-F misses the mirror, so use pole (i = r) as the second ray.
        v, m = _mirror_formula(px, ox, -g["f"])
        ix = px + (v or 70.0)
        ih = h_obj * m
        if h1x is not None:
            parts.append(_clipped_ray(ox, ay_tip, h1x, ay_tip, color="#2563eb"))
            through_f = _extend_to_x(h1x, ay_tip, fx, ay, 36)
            parts.append(_clipped_ray(h1x, ay_tip, through_f[0], through_f[1], color="#2563eb"))
            parts.append(_arrow(h1x, ay_tip, ix, ay - ih, color="#dc2626", dash="5,4", marker=""))
        parts.append(_clipped_ray(ox, ay_tip, px, ay, color="#0f766e"))
        # Reflection at P: equal angles with the axis (normal).
        inc_x, inc_y = px - ox, ay - ay_tip
        ref = _extend_to_x(px, ay, px - inc_x, ay + inc_y, 36)
        parts.append(_clipped_ray(px, ay, ref[0], ref[1], color="#0f766e"))
        parts.append(_arrow(px, ay, ix, ay - ih, color="#dc2626", dash="5,4", marker=""))
        parts.extend(_axis_arrow(ix, ay, ay - ih, color="#dc2626", dash="4,3", tip_label="A′", base_label="B′"))
        parts.append(_label(min(ix, 500), ay + 32, "behind the mirror", size=10, color="#dc2626"))
    else:
        # Fig 9.7(b–d): parallel → through F, and through F → parallel.
        hit_f = _line_circle_hit(ox, ay_tip, fx, ay, cx, ay, r, min_t=1.01)
        meet: tuple[float, float] | None = None
        if h1x is not None and hit_f is not None:
            meet = _intersect_lines(h1x, ay_tip, fx, ay, hit_f[0], hit_f[1], 36, hit_f[1])
        if position == "at_C":
            meet = (cx, ay + h_obj)
        if h1x is not None:
            parts.append(_clipped_ray(ox, ay_tip, h1x, ay_tip, color="#2563eb"))
            dest = meet if meet else (fx, ay)
            parts.append(_clipped_ray(h1x, ay_tip, dest[0], dest[1], color="#2563eb"))
        if hit_f:
            parts.append(_clipped_ray(ox, ay_tip, hit_f[0], hit_f[1], color="#0f766e"))
            dest = meet if meet else (36, hit_f[1])
            parts.append(_clipped_ray(hit_f[0], hit_f[1], dest[0], dest[1], color="#0f766e"))
        if meet and 20 < meet[0] < 540:
            ix, iy = meet
        else:
            v, m = _mirror_formula(px, ox, -g["f"])
            ix = px + (v or -80.0)
            iy = ay - h_obj * m
        dash = "4,3" if highlight in ("real_screen", "screen") else ""
        parts.extend(_axis_arrow(ix, ay, iy, color="#dc2626", dash=dash, tip_label="A′", base_label="B′"))
        if highlight in ("real_screen", "screen"):
            top, bot = min(ay, iy) - 8, max(ay, iy) + 8
            parts.append(
                f'<rect x="{ix - 10:.1f}" y="{top:.1f}" width="20" height="{bot - top:.1f}" '
                f'fill="#fef3c7" stroke="#d97706" stroke-width="1.5" opacity="0.85"/>'
            )
            parts.append(_label(ix + 18, top + 8, "screen", size=10, color="#b45309", anchor="start"))

    if highlight in ("inverted", "size_compare", "enlarged", "diminished", "same_size", "image_beyond_C", "virtual", "erect", "behind"):
        note = {
            "inverted": "A′B′ is inverted (real image)",
            "size_compare": "Compare heights of AB and A′B′",
            "enlarged": "|A′B′| > |AB|  (enlarged)",
            "diminished": "|A′B′| < |AB|  (diminished)",
            "same_size": "|A′B′| = |AB|  (same size)",
            "image_beyond_C": "Image lies beyond C",
            "virtual": "Virtual image — dotted rays meet behind the mirror",
            "erect": "A′B′ is erect (same way up as AB)",
            "behind": "Image is behind the mirror",
        }.get(highlight, "")
        if note:
            parts.append(_label(150, 52, note, size=11, color="#b45309", bold=True))

    cap = captions.get(position, captions["between_C_F"])
    if cfg.get("label") and str(cfg.get("label")) not in ("sequence", "wide_view", "object_move"):
        cap = str(cfg["label"])
    parts.append(_label(280, 326, cap, size=11, color="#334155"))
    return _svg_wrap(parts, w=560, h=340, title="Image formation by a concave mirror")


def _ncert_lens_geom() -> dict[str, float]:
    """NCERT lens layout: object on the left, lens at centre, F₁ / F₂ marked."""
    ay, ox, f = 168.0, 280.0, 70.0
    return {
        "ay": ay,
        "ox": ox,
        "f": f,
        "F1": ox - f,
        "F2": ox + f,
        "twoF1": ox - 2 * f,
        "twoF2": ox + 2 * f,
    }


def _ncert_lens_shape(lg: dict, *, convex: bool) -> list[str]:
    ay, o = lg["ay"], lg["ox"]
    if convex:
        shape = (
            f'<path d="M{o:.0f},72 Q{o - 22:.0f},{ay:.0f} {o:.0f},264 '
            f'Q{o + 22:.0f},{ay:.0f} {o:.0f},72 Z" fill="#e0f2fe" stroke="#334155" stroke-width="2.6"/>'
        )
    else:
        shape = (
            f'<path d="M{o - 16:.0f},72 Q{o + 10:.0f},{ay:.0f} {o - 16:.0f},264" fill="none" stroke="#334155" stroke-width="2.6"/>'
            f'<path d="M{o + 16:.0f},72 Q{o - 10:.0f},{ay:.0f} {o + 16:.0f},264" fill="none" stroke="#334155" stroke-width="2.6"/>'
        )
    parts = [shape, f'<line x1="28" y1="{ay:.1f}" x2="548" y2="{ay:.1f}" stroke="#94a3b8" stroke-width="1.4"/>']
    for name, x in (("2F₁", lg["twoF1"]), ("F₁", lg["F1"]), ("O", o), ("F₂", lg["F2"]), ("2F₂", lg["twoF2"])):
        parts.append(f'<circle cx="{x:.1f}" cy="{ay:.1f}" r="3.2" fill="#1e293b"/>')
        parts.append(_label(x, ay + 16, name, size=11, bold=True))
    return parts


def svg_mirror_ray_rules(cfg: dict) -> str:
    """NCERT Fig 9.3–9.6 construction-ray rules."""
    rule = str(cfg.get("rule", "parallel")).lower().replace("_", "")
    highlight = str(cfg.get("highlight") or "")
    mode = str(cfg.get("mode") or "")
    if mode == "applications":
        parts = [
            _label(280, 80, "Concave: torches, headlights, dentist / shaving mirrors", size=13, bold=True),
            _label(280, 120, "Convex: rear-view and shop-security mirrors", size=13, bold=True, color="#0f766e"),
            _label(280, 170, "Plane: dressing mirrors (same-size virtual image)", size=13, bold=True, color="#334155"),
            _label(280, 230, "Choose the mirror by the image you need", size=11, color="#64748b"),
        ]
        return _svg_wrap(parts, w=560, h=280, title="Uses of mirrors")
    g = _ncert_axis_geom(concave=True)
    ay, px, fx, cx, r = g["ay"], g["px"], g["fx"], g["cx"], g["R"]
    side = int(g["side"])
    y_tip = ay - 40
    hx = _circ_x_at_y(cx, ay, r, y_tip, side=side) or px
    parts = [_defs(("arr", "#2563eb"), ("arrG", "#059669"))]
    parts.extend(_ncert_mirror_arc(g, concave=True))
    cap = "Use two standard rays to locate the image"
    if highlight == "backward" or rule == "backward":
        parts.append(_clipped_ray(90, y_tip, hx, y_tip, color="#2563eb"))
        parts.append(_clipped_ray(hx, y_tip, 40, y_tip - 30, color="#059669", marker="arrG"))
        parts.append(_arrow(hx, y_tip, fx, ay, color="#dc2626", dash="5,4", marker=""))
        cap = "Virtual image: extend reflected rays backward (dotted)"
    elif highlight in ("intersect", "locate") or rule == "tworays":
        hit_f = _line_circle_hit(200, y_tip, fx, ay, cx, ay, r, min_t=1.01)
        meet = _intersect_lines(hx, y_tip, fx, ay, *(hit_f or (hx, y_tip)), 36, (hit_f or (36, y_tip))[1]) if hit_f else None
        parts.append(_clipped_ray(200, y_tip, hx, y_tip, color="#2563eb"))
        dest = meet or (fx, ay)
        parts.append(_clipped_ray(hx, y_tip, dest[0], dest[1], color="#2563eb"))
        if hit_f:
            parts.append(_clipped_ray(200, y_tip, hit_f[0], hit_f[1], color="#0f766e"))
            parts.append(_clipped_ray(hit_f[0], hit_f[1], dest[0], dest[1], color="#0f766e"))
        if meet:
            parts.extend(_axis_arrow(meet[0], ay, meet[1], color="#dc2626", tip_label="A′", base_label="B′"))
        cap = "Two rays are enough — their intersection is A′"
    elif highlight == "errors":
        cap = "Check: angles from the normal, F vs C, and arrow direction"
        parts.append(_clipped_ray(80, y_tip, hx, y_tip, color="#2563eb"))
        parts.append(_clipped_ray(hx, y_tip, fx, ay, color="#059669", marker="arrG"))
    elif rule == "throughf":
        hit_f = _line_circle_hit(80, y_tip, fx, ay, cx, ay, r, min_t=1.01)
        if hit_f:
            parts.append(_clipped_ray(80, y_tip, hit_f[0], hit_f[1], color="#2563eb"))
            left = _extend_to_x(hit_f[0], hit_f[1], 36, hit_f[1], 36)
            parts.append(_clipped_ray(hit_f[0], hit_f[1], left[0], left[1], color="#059669", marker="arrG"))
        cap = "Through F: reflects parallel to the principal axis"
    elif rule == "throughc":
        hit_c = _line_circle_hit(80, y_tip, cx, ay, cx, ay, r, min_t=1.01)
        if hit_c:
            parts.append(_clipped_ray(80, y_tip, hit_c[0], hit_c[1], color="#2563eb"))
            parts.append(_clipped_ray(hit_c[0], hit_c[1], 80, y_tip, color="#059669", marker="arrG"))
        cap = "Through C: hits along the normal and retraces its path"
    elif rule == "pole":
        parts.append(_clipped_ray(90, y_tip, px, ay, color="#2563eb"))
        inc_x, inc_y = px - 90, ay - y_tip
        ref = _extend_to_x(px, ay, px - inc_x, ay + inc_y, 36)
        parts.append(_clipped_ray(px, ay, ref[0], ref[1], color="#059669", marker="arrG"))
        cap = "At pole P: i = r, measured from the principal axis"
    else:
        parts.append(_clipped_ray(80, y_tip, hx, y_tip, color="#2563eb"))
        through_f = _extend_to_x(hx, y_tip, fx, ay, 36)
        parts.append(_clipped_ray(hx, y_tip, through_f[0], through_f[1], color="#059669", marker="arrG"))
        parts.append(f'<line x1="{cx:.1f}" y1="{ay:.1f}" x2="{hx:.1f}" y2="{y_tip:.1f}" stroke="#94a3b8" stroke-dasharray="4,3"/>')
        cap = "Parallel to the axis: reflects through F (Fig 9.3)"
    parts.append(_label(280, 326, cap, size=11, color="#334155"))
    return _svg_wrap(parts, w=560, h=340, title="Mirror ray rules")


def svg_sign_axis(cfg: dict) -> str:
    """NCERT New Cartesian sign convention — side view."""
    medium = str(cfg.get("medium") or cfg.get("topic") or "mirror")
    hl = str(cfg.get("highlight") or "")
    lens = medium == "lens" or str(cfg.get("topic") or "") == "lens"
    mtype = str(cfg.get("mirror_type") or ("convex" if lens else "concave"))
    parts = [_defs(("arr", "#2563eb"), ("arrG", "#059669"), ("arrR", "#dc2626"))]
    if lens:
        lg = _ncert_lens_geom()
        ay, o = lg["ay"], lg["ox"]
        parts.extend(_ncert_lens_shape(lg, convex=mtype != "concave"))
        parts.append(f'<line x1="28" y1="{ay:.1f}" x2="548" y2="{ay:.1f}" stroke="#94a3b8" stroke-width="1.4"/>')
        parts.append(f'<circle cx="{o:.1f}" cy="{ay:.1f}" r="3.4" fill="#1e293b"/>')
        parts.append(_label(o, ay + 16, "O", size=12, bold=True))
        origin = o
        foot = "Lens: incident light left to right · origin at O"
    else:
        g = _ncert_axis_geom(concave=mtype != "convex")
        ay, origin = g["ay"], g["px"]
        parts.extend(_ncert_mirror_arc(g, concave=mtype != "convex"))
        foot = "Mirror: incident light left to right · origin at P"
    plus_end = min(origin + 90, 520)
    minus_end = max(origin - 150, 40)
    parts.append(_arrow(origin, ay, plus_end, ay, color="#2563eb", width=2.2))
    parts.append(_label((origin + plus_end) / 2, ay - 14, "+ x", size=10, color="#2563eb"))
    parts.append(_arrow(origin, ay, minus_end, ay, color="#64748b", width=2.2, marker="arr"))
    parts.append(_label((origin + minus_end) / 2, ay - 14, "− x", size=10, color="#64748b"))
    parts.append(_arrow(max(origin - 180, 40), ay - 52, origin - 16, ay - 52, color="#2563eb", width=1.8))
    parts.append(_label(max(origin - 98, 90), ay - 66, "incident light", size=10, color="#2563eb"))
    parts.append(_arrow(origin, ay - 16, origin, ay - 70, color="#059669", width=2.2, marker="arrG"))
    parts.append(_label(origin + 10, ay - 74, "+ y (up)", size=10, color="#059669", anchor="start"))
    parts.append(_arrow(origin, ay + 16, origin, ay + 70, color="#dc2626", width=2.2, marker="arrR"))
    parts.append(_label(origin + 10, ay + 84, "− y (down)", size=10, color="#dc2626", anchor="start"))
    notes = {
        "P": "Origin is the pole P (mirrors) or optical centre O (lenses)",
        "light_direction": "Incident light travels left to right",
        "positive_x": "Distances with the incident light are positive",
        "negative_x": "Distances opposite the incident light are negative",
        "positive_h": "Upright heights are positive",
        "negative_h": "Inverted heights are negative",
        "u": "u is measured from P/O to the object (usually negative)",
        "v": "v is measured from P/O to the image",
        "f": "Concave mirror / concave lens: f is negative · convex lens / convex mirror: f is positive",
        "convention": "New Cartesian signs — measure from P or O",
    }
    if hl in notes:
        parts.append(_label(280, 52, notes[hl], size=12, color="#6366f1", bold=True))
    parts.append(_label(280, 326, foot, size=11, color="#334155"))
    return _svg_wrap(parts, w=560, h=340, title="Sign convention")


def svg_formula_panel(cfg: dict) -> str:
    """Formula display panel."""
    symbol_map = {
        "u": "u = object distance",
        "v": "v = image distance",
        "f": "f = focal length",
        "mirror_formula": "1/v + 1/u = 1/f",
        "lens_formula": "1/v − 1/u = 1/f",
        "compare_formulas": "Mirror: 1/v + 1/u = 1/f  |  Lens: 1/v − 1/u = 1/f",
        "m": "m = h′/h = −v/u  (mirror)",
        "m_h": "m = h′/h",
        "m_vu": "m = −v/u",
        "m_lens": "m = h′/h = v/u  (lens)",
        "interpret_m": "Use sign and |m| → orientation & size",
        "interpret_m_lens": "Use sign and |m| → orientation & size",
        "reciprocals": "1/v + 1/u = 1/f",
        "substitute": "Substitute signed u, v, f first",
        "c": "c ≈ 3 × 10⁸ m/s",
        "v_speed": "v = speed in medium",
        "n": "n = c / v",
        "P": "P = 1/f  (f in metres)",
        "dioptre": "1 D = power of f = 1 m lens",
        "metres": "f (m) = f (cm) ÷ 100",
        "snell": "n₁ sin i = n₂ sin r",
        "n_cv": "n = c / v",
        "c_meaning": "c = speed in vacuum",
        "v_meaning": "v = speed in medium",
        "n_unit": "n is unitless (ratio)",
    }
    sym = cfg.get("symbol", "")
    formula = cfg.get("formula") or symbol_map.get(sym, sym or "Formula")
    note = cfg.get("note", cfg.get("topic", ""))
    parts = [
        '<rect x="40" y="70" width="480" height="160" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>',
        f'<text x="280" y="140" text-anchor="middle" font-family="Georgia,serif" font-size="22" fill="#1e293b">{_esc(formula)}</text>',
    ]
    if note:
        parts.append(_label(280, 185, str(note), size=12, color="#64748b"))
    return _svg_wrap(parts, w=560, h=280, title="Formula")


def svg_refraction(cfg: dict) -> str:
    """NCERT-style refraction at a plane boundary (Fig 9.9)."""
    mode = str(cfg.get("mode") or "")
    hl = str(cfg.get("highlight") or "")
    if mode in ("toward", "air_glass", "denser"):
        direction = "into_denser"
    elif mode in ("away", "glass_air", "rarer"):
        direction = "into_rarer"
    else:
        direction = "into_denser"
    ay = 168
    mx = 280
    parts = [_defs(("arr", "#2563eb"), ("arrG", "#059669"))]
    parts.append('<rect x="28" y="40" width="504" height="128" fill="#fef9c3" opacity="0.45"/>')
    parts.append('<rect x="28" y="168" width="504" height="128" fill="#bfdbfe" opacity="0.45"/>')
    parts.append(f'<line x1="28" y1="{ay}" x2="532" y2="{ay}" stroke="#334155" stroke-width="2.4"/>')
    parts.append(_label(70, 70, "Air (rarer)", size=11, color="#92400e", bold=True, anchor="start"))
    parts.append(_label(70, 280, "Glass (denser)", size=11, color="#1e3a8a", bold=True, anchor="start"))
    n_w = 2.6 if hl == "normal" else 1.5
    parts.append(_arrow(mx, 48, mx, 288, color="#64748b", width=n_w, dash="6,4"))
    parts.append(_label(mx + 12, 56, "Normal", size=10, color="#64748b", anchor="start"))
    if direction == "into_denser":
        parts.append(_arrow(140, 70, mx, ay, color="#2563eb", width=3 if hl == "incident" else 2.2))
        parts.append(_arrow(mx, ay, 330, 268, color="#059669", width=3 if hl == "refracted" else 2.2, marker="arrG"))
        parts.append('<path d="M280,168 L280,132 A36,36 0 0,0 250,148" fill="none" stroke="#2563eb" stroke-width="2"/>')
        parts.append('<path d="M280,168 L280,204 A36,36 0 0,1 302,196" fill="none" stroke="#059669" stroke-width="2"/>')
        parts.append(_label(248, 140, "i", color="#2563eb", bold=True))
        parts.append(_label(308, 202, "r", color="#059669", bold=True))
        cap = "Into a denser medium: ray bends toward the normal"
    else:
        parts.append(_arrow(330, 268, mx, ay, color="#2563eb", width=3 if hl == "incident" else 2.2))
        parts.append(_arrow(mx, ay, 140, 70, color="#059669", width=3 if hl == "refracted" else 2.2, marker="arrG"))
        cap = "Into a rarer medium: ray bends away from the normal"
    notes = {
        "incident": "Incident ray — travelling toward the boundary",
        "refracted": "Refracted ray — travelling in the second medium",
        "normal": "Normal is drawn perpendicular to the boundary",
        "speed": "Light slows down in the denser medium",
        "angle_i": "Angle of incidence i is from the normal",
        "angle_r": "Angle of refraction r is from the normal",
        "transparent": "A transparent medium lets light pass through",
        "boundary": "Refraction happens at the boundary",
        "coplanar": "Incident ray, refracted ray and normal are coplanar",
        "n_speed": "Higher n means lower speed (n = c / v)",
        "compare_n": "Compare n: glass > water > air",
        "optical_vs_physical": "Optical density is not the same as mass density",
    }
    if hl in notes:
        parts.append(_label(280, 52, notes[hl], size=12, color="#6366f1", bold=True))
    elif mode in notes:
        parts.append(_label(280, 52, notes[mode], size=12, color="#6366f1", bold=True))
    parts.append(_label(280, 326, cap, size=11, color="#334155"))
    return _svg_wrap(parts, w=560, h=340, title="Refraction")


def svg_glass_slab(cfg: dict) -> str:
    """NCERT Fig 9.10 — rectangular glass slab and lateral shift."""
    hl = str(cfg.get("highlight") or "")
    parts = [_defs(("arr", "#2563eb"), ("arrG", "#059669"), ("arrR", "#dc2626"))]
    parts.append('<rect x="200" y="48" width="160" height="220" fill="#bfdbfe" stroke="#334155" stroke-width="2.2" opacity="0.7"/>')
    parts.append(_label(280, 40, "Glass slab", size=11, color="#1e3a8a", bold=True))
    parts.append('<line x1="200" y1="90" x2="360" y2="90" stroke="#94a3b8" stroke-dasharray="4,3"/>')
    parts.append('<line x1="200" y1="226" x2="360" y2="226" stroke="#94a3b8" stroke-dasharray="4,3"/>')
    parts.append(_label(372, 88, "N₁", size=10, color="#64748b", anchor="start"))
    parts.append(_label(372, 224, "N₂", size=10, color="#64748b", anchor="start"))
    parts.append(_arrow(70, 70, 200, 90, color="#2563eb", width=3 if hl == "incident" else 2.2))
    parts.append(_arrow(200, 90, 360, 226, color="#0f766e", width=2.2))
    parts.append(_arrow(360, 226, 500, 246, color="#059669", width=3 if hl == "emergent" else 2.2, marker="arrG"))
    parts.append('<line x1="70" y1="70" x2="500" y2="246" stroke="#cbd5e1" stroke-dasharray="5,4"/>')
    if hl in ("shift", "parallel"):
        parts.append(_arrow(430, 200, 430, 246, color="#dc2626", width=1.8, marker="arrR"))
        parts.append(_label(442, 226, "lateral shift", size=10, color="#dc2626", anchor="start"))
    notes = {
        "emergent": "Emergent ray leaves the second face",
        "parallel": "Emergent ray is parallel to the incident ray",
        "shift": "The ray is displaced sideways — lateral displacement",
        "slab": "Two parallel faces: two refractions",
    }
    if hl in notes:
        parts.append(_label(150, 52, notes[hl], size=12, color="#6366f1", bold=True))
    parts.append(_label(280, 326, "Incident and emergent rays are parallel (lateral shift)", size=11, color="#334155"))
    return _svg_wrap(parts, w=560, h=340, title="Glass slab")


def svg_lens_labels(cfg: dict) -> str:
    """NCERT lens labels — O, F₁, F₂, 2F, principal axis."""
    ltype = str(cfg.get("lens") or cfg.get("lens_type") or "convex")
    hl = str(cfg.get("highlight") or "")
    mode = str(cfg.get("mode") or "")
    convex = ltype != "concave"
    lg = _ncert_lens_geom()
    parts = [_defs()]
    parts.extend(_ncert_lens_shape(lg, convex=convex))
    notes = {
        "O": "O is the optical centre — a ray through O goes undeviated",
        "axis": "Principal axis: the symmetry line through O",
        "F1_F2": "Two principal foci, one on each side",
        "f": "Focal length f = OF₁ = OF₂",
        "intro": "A lens has two spherical refracting surfaces",
        "thin_symbol": "A thin lens is drawn as this double-arc outline",
    }
    title = "Convex lens (converging)" if convex else "Concave lens (diverging)"
    if hl in notes or mode in notes:
        parts.append(_label(280, 52, notes.get(hl) or notes.get(mode, ""), size=12, color="#6366f1", bold=True))
    if hl == "f":
        parts.append(f'<line x1="{lg["ox"]:.1f}" y1="{lg["ay"] + 28:.1f}" x2="{lg["F2"]:.1f}" y2="{lg["ay"] + 28:.1f}" stroke="#6366f1" stroke-width="2"/>')
        parts.append(_label((lg["ox"] + lg["F2"]) / 2, lg["ay"] + 46, "f", size=12, color="#6366f1", bold=True))
    parts.append(_label(280, 326, title, size=11, color="#334155"))
    return _svg_wrap(parts, w=560, h=340, title="Lens labels")


def svg_lens_ray(cfg: dict) -> str:
    """NCERT lens construction-ray rules."""
    rule = str(cfg.get("rule") or "parallel").lower().replace("-", "_")
    ltype = str(cfg.get("lens") or cfg.get("lens_type") or "convex")
    convex = ltype != "concave"
    lg = _ncert_lens_geom()
    ay, o, f1, f2 = lg["ay"], lg["ox"], lg["F1"], lg["F2"]
    y = ay - 40
    parts = [_defs(("arr", "#2563eb"), ("arrG", "#059669"))]
    parts.extend(_ncert_lens_shape(lg, convex=convex))
    if rule in ("through_f", "throughf"):
        if convex:
            hit = _extend_to_x(60, y, f1, ay, o)
            parts.append(_clipped_ray(60, y, hit[0], hit[1], color="#2563eb"))
            parts.append(_clipped_ray(hit[0], hit[1], 520, hit[1], color="#059669", marker="arrG"))
            cap = "Through F₁: emerges parallel to the principal axis"
        else:
            parts.append(_clipped_ray(60, y, o, y, color="#2563eb"))
            parts.append(_clipped_ray(o, y, 520, y + 36, color="#059669", marker="arrG"))
            cap = "Toward F₂: emerges parallel (concave lens)"
    elif rule in ("through_o", "througho"):
        parts.append(_clipped_ray(70, y, o, ay, color="#2563eb"))
        ext = _extend_to_x(70, y, o, ay, 520)
        parts.append(_clipped_ray(o, ay, ext[0], ext[1], color="#059669", marker="arrG"))
        cap = "Through O: goes on undeviated"
    else:
        parts.append(_clipped_ray(60, y, o, y, color="#2563eb"))
        if convex:
            parts.append(_clipped_ray(o, y, f2, ay, color="#059669", marker="arrG"))
            cap = "Parallel to the axis: refracts through F₂"
        else:
            parts.append(_arrow(o, y, f1, ay, color="#2563eb", dash="5,4", marker=""))
            parts.append(_clipped_ray(o, y, 520, y + 36, color="#059669", marker="arrG"))
            cap = "Parallel to the axis: appears to come from F₁"
        if rule in ("two_rays", "tworays"):
            ext = _extend_to_x(70, y, o, ay, 520)
            parts.append(_clipped_ray(70, y, o, ay, color="#0f766e"))
            parts.append(_clipped_ray(o, ay, ext[0], ext[1], color="#0f766e"))
            cap = "Two rays locate the image tip"
    parts.append(_label(280, 326, cap, size=11, color="#334155"))
    return _svg_wrap(parts, w=560, h=340, title="Lens rays")


def svg_lens_image(cfg: dict) -> str:
    """NCERT Fig 9.16-style lens image for one object position."""
    ltype = str(cfg.get("lens") or cfg.get("lens_type") or "convex")
    raw = str(cfg.get("position") or cfg.get("case") or "beyond_2f").lower().replace(" ", "_")
    aliases = {
        "beyond_f": "beyond_2f",
        "beyond_2f": "beyond_2f",
        "at_2f": "at_2f",
        "f_to_2f": "f_to_2f",
        "between_f_2f": "f_to_2f",
        "inside_f": "inside_f",
    }
    case = aliases.get(raw, raw if raw in aliases.values() else "beyond_2f")
    convex = ltype != "concave"
    lg = _ncert_lens_geom()
    ay, o, f1, f2 = lg["ay"], lg["ox"], lg["F1"], lg["F2"]
    h = 40.0
    y = ay - h
    obj_x = {"beyond_2f": 80.0, "at_2f": lg["twoF1"], "f_to_2f": (lg["F1"] + lg["twoF1"]) / 2, "inside_f": (lg["F1"] + o) / 2}
    ox = 90.0 if not convex else obj_x.get(case, 80.0)
    parts = [_defs(("arr", "#2563eb"), ("arrG", "#059669"), ("arrR", "#dc2626"))]
    parts.extend(_ncert_lens_shape(lg, convex=convex))
    parts.extend(_axis_arrow(ox, ay, y, color="#1d4ed8", tip_label="A", base_label="B"))
    parts.append(_clipped_ray(ox, y, o, y, color="#2563eb"))
    if convex:
        if case == "inside_f":
            # Parallel rule: through F2 after lens; virtual = backward through F2? 
            # Parallel → through F2 (forward). Through O undeviated. They diverge; extend back.
            parts.append(_clipped_ray(o, y, f2, ay, color="#2563eb"))
            onward = _extend_to_x(o, y, f2, ay, 520)
            parts.append(_clipped_ray(f2, ay, onward[0], onward[1], color="#2563eb"))
            ext = _extend_to_x(ox, y, o, ay, 520)
            parts.append(_clipped_ray(ox, y, ext[0], ext[1], color="#0f766e"))
            back = _intersect_lines(o, y, f2, ay, ox, y, o, ay)
            if back:
                parts.append(_arrow(o, y, back[0], back[1], color="#dc2626", dash="5,4", marker=""))
                parts.append(_arrow(o, ay, back[0], back[1], color="#dc2626", dash="5,4", marker=""))
                parts.extend(_axis_arrow(back[0], ay, back[1], color="#dc2626", dash="4,3", tip_label="A′", base_label="B′"))
            cap = "Object inside F: virtual, erect, enlarged (same side)"
        else:
            onward = _extend_to_x(o, y, f2, ay, 530)
            parts.append(_clipped_ray(o, y, onward[0], onward[1], color="#2563eb"))
            ext = _extend_to_x(ox, y, o, ay, 530)
            parts.append(_clipped_ray(ox, y, ext[0], ext[1], color="#0f766e"))
            meet = _intersect_lines(o, y, f2, ay, ox, y, o, ay)
            if meet and meet[0] > o:
                parts.extend(_axis_arrow(meet[0], ay, meet[1], color="#dc2626", tip_label="A′", base_label="B′"))
            caps = {
                "beyond_2f": "Object beyond 2F: real, inverted, diminished (between F₂ and 2F₂)",
                "at_2f": "Object at 2F: real, inverted, same size (at 2F₂)",
                "f_to_2f": "Object between F and 2F: real, inverted, enlarged (beyond 2F₂)",
            }
            cap = caps.get(case, caps["beyond_2f"])
    else:
        parts.append(_arrow(o, y, f1, ay, color="#2563eb", dash="5,4", marker=""))
        parts.append(_clipped_ray(o, y, 520, y + 28, color="#2563eb"))
        ext = _extend_to_x(ox, y, o, ay, 520)
        parts.append(_clipped_ray(ox, y, ext[0], ext[1], color="#0f766e"))
        meet = _intersect_lines(f1, ay, o, y, ox, y, o, ay)
        if meet:
            parts.append(_arrow(o, y, meet[0], meet[1], color="#dc2626", dash="5,4", marker=""))
            parts.extend(_axis_arrow(meet[0], ay, meet[1], color="#dc2626", dash="4,3", tip_label="A′", base_label="B′"))
        cap = "Concave lens: virtual, erect, diminished (between O and F₁)"
    parts.append(_label(280, 326, cap, size=11, color="#334155"))
    return _svg_wrap(parts, w=560, h=340, title="Lens image")


def svg_placeholder(cfg: dict) -> str:
    label = str(cfg.get("label", "Diagram"))
    parts = [
        f'<rect x="80" y="80" width="320" height="100" rx="8" fill="#eef1f5" stroke="#d8dee6"/>',
        _label(240, 135, label, color="#64748b"),
    ]
    return _svg_wrap(parts, h=240)


def svg_eye_structure(cfg: dict) -> str:
    hl = cfg.get("highlight", "")
    mode = cfg.get("mode", "")
    parts = [_defs(("arr", "#2563eb"), ("arrG", "#059669"))]
    # Simplified NCERT Fig 10.1 side view
    parts.append('<ellipse cx="240" cy="130" rx="90" ry="55" fill="#f8fafc" stroke="#64748b" stroke-width="2"/>')
    parts.append('<path d="M150,130 Q240,75 330,130 Q240,185 150,130" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>')
    parts.append('<ellipse cx="240" cy="130" rx="28" ry="20" fill="#1e293b" opacity="0.15"/>')
    parts.append('<ellipse cx="240" cy="130" rx="14" ry="14" fill="none" stroke="#6366f1" stroke-width="2.5"/>')
    labels = [
        (175, 95, "Cornea", hl == "cornea"),
        (210, 118, "Iris", hl == "iris_pupil"),
        (240, 108, "Pupil", hl == "iris_pupil"),
        (268, 130, "Lens", hl == "lens"),
        (305, 140, "Retina", hl == "retina"),
        (340, 115, "Optic nerve", hl == "optic_nerve"),
    ]
    for x, y, text, bold in labels:
        parts.append(_label(x, y, text, size=10, bold=bold, color="#6366f1" if bold else "#334155"))
    if hl == "inverted_image":
        parts.append(_label(300, 165, "Inverted image", size=10, color="#dc2626", bold=True))
    if mode == "camera_analogy":
        parts.append(_label(240, 210, "Camera: lens + retina screen", size=11, bold=True))
    elif mode == "checklist" or mode == "map":
        parts.append(_label(240, 210, cfg.get("mode", "").replace("_", " ").title(), size=11))
    elif hl == "overview":
        parts.append(_label(240, 210, "Human eye (NCERT Fig 10.1 style)", size=11))
    parts.append(_book(70, 130))
    parts.append(_arrow(95, 130, 145, 130, color="#2563eb"))
    parts.append(_label(115, 118, "Light in", size=10, color="#2563eb"))
    return _svg_wrap(parts, h=260, title="The human eye")


def svg_eye_accommodation(cfg: dict) -> str:
    mode = cfg.get("mode", "")
    hl = cfg.get("highlight", "")
    parts = [_defs()]
    parts.append('<ellipse cx="240" cy="130" rx="85" ry="50" fill="#f8fafc" stroke="#64748b" stroke-width="2"/>')
    thick = mode in ("near",) or hl == "ciliary"
    ry = 22 if thick else 14
    parts.append(f'<ellipse cx="240" cy="130" rx="18" ry="{ry}" fill="#c7d2fe" stroke="#6366f1" stroke-width="2.5"/>')
    parts.append(_label(200, 100, "Ciliary muscles", size=10, bold=hl == "ciliary"))
    if mode == "distant" or hl == "far_point":
        parts.append(_label(240, 175, "Relaxed → thin lens → far objects clear", size=11, bold=True))
    elif mode == "near":
        parts.append(_label(240, 175, "Contracted → thick lens → near objects clear", size=11, bold=True))
    elif mode == "range":
        parts.append(_label(240, 175, "Clear vision: 25 cm to ∞", size=11, bold=True))
    else:
        parts.append(_label(240, 175, "Accommodation adjusts focal length", size=11, bold=True))
    return _svg_wrap(parts, h=240, title="Power of accommodation")


def svg_vision_defect(cfg: dict) -> str:
    defect = cfg.get("defect", "overview")
    hl = cfg.get("highlight", "")
    parts = [_defs(("arr", "#2563eb"), ("arrR", "#dc2626"))]
    parts.append('<ellipse cx="240" cy="130" rx="85" ry="50" fill="#f8fafc" stroke="#64748b" stroke-width="2"/>')
    parts.append('<line x1="305" y1="130" x2="305" y2="100" stroke="#64748b" stroke-width="2" stroke-dasharray="3,2"/>')
    parts.append(_label(315, 95, "Retina", size=10))
    if defect == "myopia" or hl == "image_front":
        parts.append(_arrow(60, 120, 270, 125, color="#2563eb"))
        parts.append('<circle cx="285" cy="127" r="4" fill="#dc2626"/>')
        parts.append(_label(285, 145, "Image before retina", size=10, color="#dc2626", bold=True))
        if hl == "correction":
            parts.append('<path d="M120,120 L120,140 L140,130 Z" fill="none" stroke="#7c3aed" stroke-width="2"/>')
            parts.append(_label(95, 155, "Concave lens", size=10, color="#7c3aed"))
    elif defect == "hypermetropia" or hl == "image_behind":
        parts.append(_arrow(60, 140, 270, 135, color="#2563eb"))
        parts.append('<circle cx="318" cy="133" r="4" fill="#dc2626"/>')
        parts.append(_label(318, 150, "Image behind retina", size=10, color="#dc2626", bold=True))
        if hl == "correction":
            parts.append('<ellipse cx="130" cy="135" rx="8" ry="22" fill="none" stroke="#7c3aed" stroke-width="2"/>')
            parts.append(_label(95, 160, "Convex lens", size=10, color="#7c3aed"))
    elif defect == "bifocal":
        parts.append(_label(240, 175, "Bifocal: top concave (far), bottom convex (near)", size=10, bold=True))
    elif defect == "presbyopia":
        parts.append(_label(240, 175, "Age → weaker accommodation", size=11, bold=True))
    else:
        parts.append(_label(240, 175, "Myopia · Hypermetropia · Presbyopia", size=11, bold=True))
    return _svg_wrap(parts, h=240, title="Defects of vision")


def svg_prism_refraction(cfg: dict) -> str:
    hl = cfg.get("highlight", "")
    parts = [_defs(("arr", "#2563eb"), ("arrG", "#059669"))]
    # Triangle prism
    parts.append('<polygon points="200,180 280,70 360,180" fill="#e0f2fe" stroke="#0284c7" stroke-width="2"/>')
    parts.append(_label(280, 55, "A", size=12, bold=hl == "angle_A"))
    parts.append(_arrow(80, 150, 198, 155, color="#2563eb"))
    parts.append(_label(130, 138, "PE incident", size=10, color="#2563eb", bold=hl == "incident"))
    parts.append(_arrow(250, 130, 310, 165, color="#7c3aed"))
    parts.append(_label(270, 125, "EF refracted", size=10, color="#7c3aed", bold=hl == "refracted"))
    parts.append(_arrow(340, 172, 420, 120, color="#059669", marker="arrG"))
    parts.append(_label(400, 108, "FS emergent", size=10, color="#059669", bold=hl == "emergent"))
    if hl == "deviation":
        parts.append(_label(280, 210, "∠D angle of deviation", size=11, bold=True, color="#dc2626"))
    elif hl == "angles":
        parts.append(_label(280, 210, "∠i  ∠r  ∠e measured from normals", size=10))
    else:
        parts.append(_label(280, 210, "Refraction through a prism (Fig 10.4)", size=10))
    return _svg_wrap(parts, h=260, title="Prism refraction")


def svg_dispersion_spectrum(cfg: dict) -> str:
    hl = cfg.get("highlight", "")
    colors = ["#7c3aed", "#4f46e5", "#2563eb", "#059669", "#eab308", "#f97316", "#dc2626"]
    parts = [_defs(("arr", "#2563eb"))]
    parts.append('<polygon points="180,170 230,90 280,170" fill="#f1f5f9" stroke="#64748b" stroke-width="2"/>')
    parts.append(_arrow(60, 140, 178, 145, color="#2563eb"))
    x = 300
    for i, c in enumerate(colors):
        parts.append(_arrow(282, 140 + i * 2, x + i * 18, 200 - i * 8, color=c, width=2))
    parts.append('<rect x="295" y="115" width="130" height="18" rx="4" fill="#e2e8f0"/>')
    parts.append(_label(360, 128, "VIBGYOR spectrum", size=10, bold=hl == "vibgyor"))
    if hl == "bending":
        parts.append(_label(360, 210, "Red bends least · Violet bends most", size=11, bold=True))
    elif hl == "dispersion":
        parts.append(_label(360, 210, "Dispersion splits white light", size=11, bold=True))
    else:
        parts.append(_label(360, 210, "White light → colour band", size=11))
    return _svg_wrap(parts, h=260, title="Dispersion")


def svg_rainbow(cfg: dict) -> str:
    parts = [_defs(("arr", "#f59e0b"))]
    parts.append(_sun(70, 200, highlight=False))
    parts.append(_label(70, 235, "Sun", size=10))
    parts.append(_eye(400, 200, highlight=True))
    parts.append(_label(400, 235, "Observer", size=10))
    # Rainbow arc
    parts.append('<path d="M120,200 A120,120 0 0 1 360,200" fill="none" stroke="#dc2626" stroke-width="4"/>')
    parts.append('<path d="M130,200 A110,110 0 0 1 350,200" fill="none" stroke="#f97316" stroke-width="3"/>')
    parts.append('<path d="M140,200 A100,100 0 0 1 340,200" fill="none" stroke="#2563eb" stroke-width="3"/>')
    parts.append('<circle cx="280" cy="120" r="12" fill="#bae6fd" stroke="#0284c7"/>')
    parts.append(_label(280, 145, "Raindrop", size=10, bold=cfg.get("highlight") == "droplet"))
    parts.append(_arrow(95, 195, 268, 125, color="#fcd34d"))
    parts.append(_label(240, 215, "Rainbow opposite the Sun", size=11, bold=True))
    return _svg_wrap(parts, h=260, title="Rainbow formation")


def svg_atmospheric_refraction(cfg: dict) -> str:
    mode = cfg.get("mode", "")
    parts = [_defs(("arr", "#2563eb"))]
    if mode == "twinkle" or mode == "brightness":
        parts.append(_label(240, 50, "★", size=28, color="#fcd34d"))
        parts.append(_label(240, 80, "Star light bends in moving air layers", size=11, bold=True))
        for y in (120, 150, 180):
            parts.append(f'<line x1="100" y1="{y}" x2="380" y2="{y}" stroke="#94a3b8" stroke-width="1" stroke-dasharray="4,3"/>')
        parts.append(_label(240, 210, "Apparent position keeps shifting → twinkle", size=10))
    elif mode in ("sunrise", "sunset", "sunrise_exam"):
        parts.append('<line x1="40" y1="170" x2="440" y2="170" stroke="#64748b" stroke-width="2"/>')
        parts.append(_label(450, 174, "Horizon", size=10))
        parts.append(_sun(280, 170, highlight=True))
        parts.append(_sun(280, 200, highlight=False))
        parts.append(_label(320, 155, "Apparent", size=10, color="#f59e0b"))
        parts.append(_label(320, 220, "Actual", size=10, color="#64748b"))
        parts.append(_label(240, 230, "≈2 min advance / delay", size=11, bold=True))
    elif mode == "planets" or mode == "planets_detail":
        parts.append(_label(240, 90, "Planet = many points", size=12, bold=True))
        parts.append('<circle cx="240" cy="150" r="35" fill="#cbd5e1" stroke="#64748b" stroke-width="2"/>')
        parts.append(_label(240, 210, "Variations average out → no twinkle", size=11))
    else:
        parts.append(_label(240, 130, "Earth's atmosphere bends light", size=12, bold=True))
        parts.append(_label(240, 160, "Density changes → refractive index changes", size=10))
    return _svg_wrap(parts, h=260, title="Atmospheric refraction")


def svg_scattering_sky(cfg: dict) -> str:
    hl = cfg.get("highlight", "")
    mode = cfg.get("mode", "")
    parts = []
    if mode == "red_sun" or mode == "exam_red":
        parts.append('<rect x="0" y="0" width="480" height="280" fill="#fb923c" opacity="0.25"/>')
        parts.append(_sun(240, 200, highlight=True))
        parts.append(_label(240, 240, "Long path → blue scattered away → red Sun", size=11, bold=True))
    elif hl == "red_signal":
        parts.append('<rect x="160" y="100" width="50" height="50" rx="6" fill="#dc2626" stroke="#991b1b" stroke-width="2"/>')
        parts.append(_label(240, 175, "Red least scattered → visible in fog", size=11, bold=True))
    else:
        parts.append('<rect x="0" y="0" width="480" height="200" fill="#93c5fd" opacity="0.5"/>')
        parts.append(_sun(80, 80))
        parts.append(_arrow(110, 85, 200, 120, color="#2563eb"))
        parts.append(_arrow(110, 85, 320, 100, color="#2563eb"))
        parts.append(_arrow(110, 85, 400, 140, color="#2563eb"))
        parts.append(_label(240, 220, "Blue scattered strongly → sky looks blue", size=11, bold=True))
    return _svg_wrap(parts, h=260, title="Scattering of light")


def svg_tyndall_effect(cfg: dict) -> str:
    parts = [_defs(("arr", "#fcd34d"))]
    parts.append('<rect x="0" y="0" width="480" height="280" fill="#1e293b" opacity="0.85"/>')
    parts.append(_arrow(40, 140, 440, 140, color="#fcd34d", width=3))
    parts.append(_label(240, 120, "Visible sunbeam through smoke/mist", size=11, bold=True, color="#fcd34d"))
    parts.append(_label(240, 200, "Tyndall effect — scattering by colloidal particles", size=10, color="#94a3b8"))
    return _svg_wrap(parts, h=240, title="Tyndall effect")


def svg_electric_circuit(cfg: dict) -> str:
    hl = cfg.get("highlight", "")
    mode = cfg.get("mode", "")
    parts = [_defs(("arr", "#2563eb"))]
    # Simple rectangular circuit: cell bottom, bulb top, ammeter right
    parts.append('<rect x="100" y="70" width="280" height="160" rx="8" fill="none" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="4,3"/>')
    # Cell
    parts.append('<line x1="140" y1="230" x2="140" y2="210" stroke="#334155" stroke-width="3"/>')
    parts.append('<line x1="150" y1="230" x2="150" y2="215" stroke="#334155" stroke-width="5"/>')
    parts.append(_label(120, 245, "Cell", size=10, bold=hl == "cell"))
    # Bulb
    parts.append('<circle cx="240" cy="80" r="18" fill="#fef9c3" stroke="#f59e0b" stroke-width="2"/>')
    parts.append('<line x1="228" y1="68" x2="252" y2="92" stroke="#f59e0b" stroke-width="2"/>')
    parts.append('<line x1="252" y1="68" x2="228" y2="92" stroke="#f59e0b" stroke-width="2"/>')
    parts.append(_label(240, 55, "Bulb", size=10, bold=hl == "overview"))
    # Ammeter
    parts.append('<circle cx="360" cy="150" r="16" fill="#eef2ff" stroke="#6366f1" stroke-width="2"/>')
    parts.append(_label(360, 154, "A", size=12, bold=hl == "ammeter", color="#6366f1"))
    # Wires with current arrow
    parts.append(_arrow(150, 230, 150, 150, color="#2563eb"))
    parts.append(_arrow(150, 150, 360, 150, color="#2563eb"))
    parts.append(_arrow(360, 150, 360, 98, color="#2563eb"))
    parts.append(_arrow(258, 80, 150, 80, color="#2563eb"))
    parts.append(_arrow(150, 80, 150, 210, color="#2563eb"))
    if mode == "open_circuit":
        parts.append(_label(240, 130, "Open switch → no current", size=11, bold=True, color="#dc2626"))
    elif hl == "conventional":
        parts.append(_label(240, 130, "Conventional current: + → −", size=11, bold=True))
    else:
        parts.append(_label(240, 130, "Closed circuit (Fig 11.1 style)", size=10))
    return _svg_wrap(parts, h=280, title="Electric circuit")


def svg_circuit_symbols(cfg: dict) -> str:
    hl = cfg.get("highlight", "")
    parts = []
    items = [
        (70, 70, "Cell", "cell"),
        (170, 70, "Battery", "battery"),
        (270, 70, "Switch", "switch"),
        (370, 70, "Bulb", "bulb_resistor"),
        (70, 170, "R", "bulb_resistor"),
        (170, 170, "Rheostat", "rheostat"),
        (270, 170, "A", "meters"),
        (370, 170, "V", "meters"),
    ]
    for x, y, label, key in items:
        bold = hl == key
        parts.append(f'<rect x="{x-25}" y="{y-20}" width="50" height="40" rx="6" fill="#f8fafc" stroke="#6366f1" stroke-width="2" opacity="{1 if bold else 0.6}"/>')
        parts.append(_label(x, y + 5, label, size=10, bold=bold))
    parts.append(_label(240, 230, "NCERT Table 11.1 — circuit symbols", size=11, bold=True))
    return _svg_wrap(parts, h=260, title="Circuit symbols")


def svg_ohms_law_graph(cfg: dict) -> str:
    hl = cfg.get("highlight", "")
    mode = cfg.get("mode", "")
    parts = [_defs(("arr", "#2563eb"))]
    parts.append('<line x1="80" y1="200" x2="400" y2="200" stroke="#64748b" stroke-width="1.5"/>')
    parts.append('<line x1="80" y1="200" x2="80" y2="60" stroke="#64748b" stroke-width="1.5"/>')
    parts.append(_label(410, 205, "I (A)", size=11))
    parts.append(_label(65, 55, "V (V)", size=11))
    parts.append('<line x1="80" y1="200" x2="360" y2="80" stroke="#2563eb" stroke-width="3"/>')
    parts.append(_label(300, 100, "slope = R", size=10, color="#2563eb", bold=True))
    if hl == "statement" or mode == "definition":
        parts.append(_label(240, 230, "V ∝ I → straight line through origin", size=11, bold=True))
    else:
        parts.append(_label(240, 230, "Ohm's law: V = I R", size=11, bold=True))
    return _svg_wrap(parts, h=260, title="Ohm's law graph")


def svg_resistance_wire(cfg: dict) -> str:
    hl = cfg.get("highlight", "")
    mode = cfg.get("mode", "")
    parts = [_defs()]
    parts.append('<rect x="120" y="120" width="240" height="24" rx="4" fill="#cbd5e1" stroke="#64748b" stroke-width="2"/>')
    if hl == "length":
        parts.append(_label(240, 105, "Longer wire → higher R", size=11, bold=True))
    elif hl == "area":
        parts.append('<rect x="120" y="110" width="240" height="44" rx="4" fill="#94a3b8" stroke="#64748b" stroke-width="2"/>')
        parts.append(_label(240, 175, "Thicker wire → lower R", size=11, bold=True))
    elif mode == "compare" or hl == "material":
        parts.append(_label(240, 175, "Material sets resistivity ρ", size=11, bold=True))
    else:
        parts.append(_label(240, 175, "R = ρ l / A", size=12, bold=True))
    return _svg_wrap(parts, h=220, title="Resistance of a wire")


def svg_resistors_series(cfg: dict) -> str:
    hl = cfg.get("highlight", "")
    parts = [_defs(("arr", "#2563eb"))]
    xs = [140, 210, 280]
    for i, x in enumerate(xs):
        parts.append(f'<rect x="{x}" y="120" width="50" height="24" rx="3" fill="#e0e7ff" stroke="#6366f1" stroke-width="2"/>')
        parts.append(_label(x + 25, 135, f"R{i+1}", size=10, bold=True))
        if i < 2:
            parts.append(f'<line x1="{x+50}" y1="132" x2="{xs[i+1]}" y2="132" stroke="#64748b" stroke-width="2"/>')
    parts.append(_arrow(80, 132, 135, 132, color="#2563eb"))
    parts.append(_arrow(335, 132, 400, 132, color="#2563eb"))
    if hl == "current":
        parts.append(_label(240, 165, "Same current I through each resistor", size=11, bold=True))
    elif hl == "voltage":
        parts.append(_label(240, 165, "V = V1 + V2 + V3", size=11, bold=True))
    else:
        parts.append(_label(240, 165, "R_s = R1 + R2 + R3", size=11, bold=True))
    return _svg_wrap(parts, h=220, title="Resistors in series")


def svg_resistors_parallel(cfg: dict) -> str:
    hl = cfg.get("highlight", "")
    parts = [_defs(("arr", "#2563eb"))]
    parts.append('<line x1="80" y1="80" x2="80" y2="200" stroke="#64748b" stroke-width="2"/>')
    parts.append('<line x1="400" y1="80" x2="400" y2="200" stroke="#64748b" stroke-width="2"/>')
    for y, label in [(100, "R1"), (140, "R2"), (180, "R3")]:
        parts.append(f'<line x1="80" y1="{y}" x2="130" y2="{y}" stroke="#64748b" stroke-width="2"/>')
        parts.append(f'<rect x="130" y="{y-12}" width="60" height="24" rx="3" fill="#ecfdf5" stroke="#059669" stroke-width="2"/>')
        parts.append(_label(160, y + 4, label, size=10, bold=True))
        parts.append(f'<line x1="190" y1="{y}" x2="400" y2="{y}" stroke="#64748b" stroke-width="2"/>')
    parts.append(_arrow(40, 140, 78, 140, color="#2563eb"))
    parts.append(_arrow(402, 140, 440, 140, color="#2563eb"))
    if hl == "current":
        parts.append(_label(240, 220, "I = I1 + I2 + I3", size=11, bold=True))
    elif hl == "voltage":
        parts.append(_label(240, 220, "Same V across each branch", size=11, bold=True))
    else:
        parts.append(_label(240, 220, "1/R_p = 1/R1 + 1/R2 + 1/R3", size=10, bold=True))
    return _svg_wrap(parts, h=260, title="Resistors in parallel")


def svg_heating_element(cfg: dict) -> str:
    hl = cfg.get("highlight", "")
    parts = [_defs()]
    parts.append('<path d="M140,150 Q160,110 180,150 T220,150 T260,150 T300,150" fill="none" stroke="#dc2626" stroke-width="4"/>')
    parts.append(_label(220, 100, "Heating coil (high R)", size=11, bold=True, color="#dc2626"))
    parts.append('<line x1="80" y1="150" x2="135" y2="150" stroke="#64748b" stroke-width="3"/>')
    parts.append('<line x1="305" y1="150" x2="360" y2="150" stroke="#64748b" stroke-width="3"/>')
    parts.append(_label(220, 185, "H = I² R t", size=12, bold=True))
    if hl == "fuse":
        parts.append(_label(220, 210, "Fuse melts if I too high", size=10, color="#b45309"))
    return _svg_wrap(parts, h=240, title="Heating effect")


def svg_electric_power(cfg: dict) -> str:
    mode = cfg.get("mode", "")
    parts = [_defs()]
    parts.append(_label(240, 90, "P = V I", size=16, bold=True, color="#6366f1"))
    parts.append(_label(240, 120, "P = I² R = V² / R", size=11))
    if mode == "billing":
        parts.append(_label(240, 160, "Energy (kWh) = Power (kW) × time (h)", size=11, bold=True))
    else:
        parts.append(_label(240, 160, "1 W = 1 V × 1 A", size=11, bold=True))
    parts.append(_label(240, 200, "Unit on bill: kilowatt-hour (kWh)", size=10, color="#64748b"))
    return _svg_wrap(parts, h=240, title="Electric power")


def svg_magnetic_field_lines(cfg: dict) -> str:
    hl = cfg.get("highlight", "")
    mode = cfg.get("mode", "")
    parts = [_defs(("arr", "#6366f1"))]
    # Bar magnet
    parts.append('<rect x="200" y="115" width="80" height="30" rx="4" fill="#cbd5e1" stroke="#64748b" stroke-width="2"/>')
    parts.append(_label(215, 135, "N", size=12, bold=True, color="#dc2626"))
    parts.append(_label(255, 135, "S", size=12, bold=True, color="#2563eb"))
    # Field curves
    for i, (x1, y1, x2, y2) in enumerate([
        (180, 80, 300, 80), (160, 100, 320, 100), (150, 130, 330, 130),
        (160, 160, 320, 160), (180, 180, 300, 180),
    ]):
        parts.append(f'<path d="M{x1},{y1} Q240,60 {x2},{y2}" fill="none" stroke="#6366f1" stroke-width="1.5" marker-end="url(#arr)"/>')
    if hl == "no_cross" or mode == "properties":
        parts.append(_label(240, 220, "Closed curves; no crossing; density = strength", size=10, bold=True))
    elif hl == "poles":
        parts.append(_label(240, 220, "N pole and S pole", size=11, bold=True))
    else:
        parts.append(_label(240, 220, "Magnetic field lines around bar magnet", size=10))
    return _svg_wrap(parts, h=260, title="Magnetic field lines")


def svg_current_magnetic_field(cfg: dict) -> str:
    hl = cfg.get("highlight", "")
    mode = cfg.get("mode", "")
    parts = [_defs(("arr", "#2563eb"))]
    # Vertical wire through center
    parts.append('<line x1="240" y1="50" x2="240" y2="230" stroke="#334155" stroke-width="4"/>')
    parts.append(_arrow(240, 60, 240, 90, color="#dc2626"))
    parts.append(_label(260, 75, "I", size=12, bold=True, color="#dc2626"))
    # Concentric circles
    for r in [35, 55, 75, 95]:
        parts.append(f'<circle cx="240" cy="140" r="{r}" fill="none" stroke="#2563eb" stroke-width="1.5" stroke-dasharray="4,2"/>')
    parts.append('<polygon points="275,140 265,135 265,145" fill="#2563eb"/>')
    if hl == "concentric" or mode == "exam":
        parts.append(_label(240, 250, "Concentric circles around straight wire", size=11, bold=True))
    elif hl == "oersted" or mode == "activity_12_1":
        parts.append('<circle cx="120" cy="140" r="12" fill="#fef9c3" stroke="#f59e0b" stroke-width="2"/>')
        parts.append(_label(120, 144, "N", size=9, bold=True))
        parts.append(_label(120, 165, "Compass deflects", size=10, bold=True))
    else:
        parts.append(_label(240, 250, "Magnetic field due to current", size=10))
    return _svg_wrap(parts, h=280, title="Field due to current")


def svg_right_hand_rule(cfg: dict) -> str:
    hl = cfg.get("highlight", "")
    parts = [_defs()]
    parts.append(_label(240, 70, "Right-hand thumb rule", size=13, bold=True, color="#6366f1"))
    parts.append('<line x1="240" y1="100" x2="240" y2="200" stroke="#334155" stroke-width="4"/>')
    parts.append(_label(260, 150, "Thumb → current (I)", size=11, bold=hl == "rule", color="#dc2626"))
    parts.append('<path d="M180,150 A60,60 0 1,1 300,150" fill="none" stroke="#2563eb" stroke-width="2"/>')
    parts.append(_label(240, 220, "Curled fingers → field direction (B)", size=11, bold=True, color="#2563eb"))
    return _svg_wrap(parts, h=260, title="Right-hand thumb rule")


def svg_solenoid_field(cfg: dict) -> str:
    hl = cfg.get("highlight", "")
    mode = cfg.get("mode", "")
    parts = [_defs(("arr", "#6366f1"))]
    # Coil
    for x in range(130, 350, 22):
        parts.append(f'<ellipse cx="{x}" cy="140" rx="10" ry="28" fill="none" stroke="#6366f1" stroke-width="2"/>')
    if mode == "electromagnet" or hl == "soft_iron":
        parts.append('<rect x="170" y="125" width="140" height="30" rx="4" fill="#94a3b8" stroke="#64748b" stroke-width="2"/>')
        parts.append(_label(240, 145, "Soft iron core", size=10, bold=True))
    # Uniform field inside
    for y in [130, 140, 150]:
        parts.append(f'<line x1="170" y1="{y}" x2="310" y2="{y}" stroke="#059669" stroke-width="1.5" marker-end="url(#arr)"/>')
    if hl == "uniform":
        parts.append(_label(240, 200, "Uniform field inside solenoid", size=11, bold=True))
    elif hl == "bar_magnet":
        parts.append(_label(240, 200, "External field like bar magnet", size=11, bold=True))
    else:
        parts.append(_label(240, 200, "Solenoid magnetic field", size=10))
    return _svg_wrap(parts, h=260, title="Solenoid")


def svg_flemings_left_hand(cfg: dict) -> str:
    hl = cfg.get("highlight", "")
    mode = cfg.get("mode", "")
    parts = [_defs()]
    parts.append(_label(240, 55, "Fleming's left-hand rule", size=13, bold=True, color="#6366f1"))
    parts.append(_label(120, 100, "First finger → B (field)", size=10, bold=hl == "rule", color="#2563eb"))
    parts.append(_label(120, 130, "Second finger → I (current)", size=10, bold=True, color="#dc2626"))
    parts.append(_label(120, 160, "Thumb → F (force/motion)", size=10, bold=True, color="#059669"))
    # Wire between magnet poles
    parts.append('<rect x="160" y="180" width="160" height="8" rx="2" fill="#64748b"/>')
    parts.append('<rect x="150" y="160" width="20" height="60" fill="#cbd5e1" stroke="#64748b"/>')
    parts.append(_label(160, 195, "N", size=10, bold=True))
    parts.append('<rect x="310" y="160" width="20" height="60" fill="#cbd5e1" stroke="#64748b"/>')
    parts.append(_label(320, 195, "S", size=10, bold=True))
    parts.append(_arrow(240, 220, 240, 195, color="#059669"))
    parts.append(_label(255, 215, "F", size=11, bold=True, color="#059669"))
    if mode == "activity_12_7":
        parts.append(_label(240, 245, "Rod displaces when current flows in field", size=10, bold=True))
    return _svg_wrap(parts, h=280, title="Fleming's left-hand rule")


def svg_domestic_circuit(cfg: dict) -> str:
    hl = cfg.get("highlight", "")
    mode = cfg.get("mode", "")
    parts = [_defs(("arr", "#2563eb"))]
    # Live (red) and neutral (black) rails
    parts.append('<line x1="80" y1="80" x2="400" y2="80" stroke="#dc2626" stroke-width="3"/>')
    parts.append('<line x1="80" y1="200" x2="400" y2="200" stroke="#334155" stroke-width="3"/>')
    parts.append(_label(60, 85, "Live", size=10, bold=hl == "live", color="#dc2626"))
    parts.append(_label(55, 205, "Neutral", size=10, bold=hl == "neutral", color="#334155"))
    # Earth wire
    parts.append('<line x1="80" y1="240" x2="400" y2="240" stroke="#059669" stroke-width="2" stroke-dasharray="6,3"/>')
    parts.append(_label(55, 245, "Earth", size=10, bold=hl == "earth", color="#059669"))
    # Parallel branches
    for x, label in [(140, "Bulb"), (240, "Fan"), (340, "Geyser")]:
        parts.append(f'<line x1="{x}" y1="80" x2="{x}" y2="120" stroke="#64748b" stroke-width="2"/>')
        parts.append(f'<rect x="{x-20}" y="120" width="40" height="30" rx="4" fill="#f8fafc" stroke="#6366f1" stroke-width="2"/>')
        parts.append(_label(x, 138, label, size=9, bold=True))
        parts.append(f'<line x1="{x}" y1="150" x2="{x}" y2="200" stroke="#64748b" stroke-width="2"/>')
    if hl == "parallel" or mode == "fig_12_15":
        parts.append(_label(240, 265, "Appliances in parallel — 220 V each", size=10, bold=True))
    elif hl == "colours":
        parts.append(_label(240, 265, "Red live · Black neutral · Green earth", size=10, bold=True))
    elif hl == "fuse":
        parts.append(_label(100, 65, "Fuse", size=10, bold=True, color="#b45309"))
    else:
        parts.append(_label(240, 265, "Domestic electric circuit (Fig 12.15)", size=10))
    return _svg_wrap(parts, h=290, title="Domestic circuit")


_RENDERERS = {
    "light_source_model": svg_light_source_model,
    "eye_light_path": svg_eye_light_path,
    "straight_ray": svg_straight_ray,
    "plane_mirror_reflection": svg_plane_mirror_reflection,
    "normal_angle": svg_normal_angle,
    "spherical_mirror_labels": svg_spherical_mirror_labels,
    "mirror_focus_ray": svg_mirror_focus_ray,
    "concave_image": svg_concave_image,
    "mirror_ray_rules": svg_mirror_ray_rules,
    "sign_axis": svg_sign_axis,
    "formula_panel": svg_formula_panel,
    "refraction": svg_refraction,
    "glass_slab": svg_glass_slab,
    "lens_labels": svg_lens_labels,
    "lens_ray": svg_lens_ray,
    "lens_image": svg_lens_image,
    "eye_structure": svg_eye_structure,
    "eye_accommodation": svg_eye_accommodation,
    "vision_defect": svg_vision_defect,
    "prism_refraction": svg_prism_refraction,
    "dispersion_spectrum": svg_dispersion_spectrum,
    "rainbow": svg_rainbow,
    "atmospheric_refraction": svg_atmospheric_refraction,
    "scattering_sky": svg_scattering_sky,
    "tyndall_effect": svg_tyndall_effect,
    "electric_circuit": svg_electric_circuit,
    "circuit_symbols": svg_circuit_symbols,
    "ohms_law_graph": svg_ohms_law_graph,
    "resistance_wire": svg_resistance_wire,
    "resistors_series": svg_resistors_series,
    "resistors_parallel": svg_resistors_parallel,
    "heating_element": svg_heating_element,
    "electric_power": svg_electric_power,
    "magnetic_field_lines": svg_magnetic_field_lines,
    "current_magnetic_field": svg_current_magnetic_field,
    "right_hand_rule": svg_right_hand_rule,
    "solenoid_field": svg_solenoid_field,
    "flemings_left_hand": svg_flemings_left_hand,
    "domestic_circuit": svg_domestic_circuit,
    "placeholder": svg_placeholder,
}


def render_diagram_html(visual: dict) -> str:
    vtype = visual.get("type", "placeholder")
    fn = _RENDERERS.get(vtype, svg_placeholder)
    inner = fn(visual)
    return f'<div class="hp-diagram-wrap">{inner}</div>'
