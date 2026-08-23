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
    return (
        f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
        f'stroke="{color}" stroke-width="{width}" marker-end="url(#{marker})"{dash_attr}/>'
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


def svg_plane_mirror_reflection(cfg: dict) -> str:
    hl = cfg.get("highlight", "")
    mode = cfg.get("mode", "")
    if mode == "image_properties":
        parts = [
            '<line x1="240" y1="30" x2="240" y2="250" stroke="#94a3b8" stroke-width="5"/>',
            _label(240, 265, "Plane mirror", size=10),
            '<polygon points="120,180 140,120 160,180" fill="#cbd5e1" stroke="#475569" stroke-width="2"/>',
            _label(140, 200, "Object", bold=True),
            '<polygon points="320,180 340,120 360,180" fill="none" stroke="#6366f1" stroke-width="2" stroke-dasharray="5,4"/>',
            _label(340, 200, "Virtual image", color="#6366f1", bold=True),
            _label(340, 215, "(same size, erect)", size=10, color="#64748b"),
            _label(140, 95, "As far in front", size=9, color="#64748b"),
            _label(340, 95, "as image behind", size=9, color="#64748b"),
        ]
        return _svg_wrap(parts, title="Plane mirror image")
    parts = [_defs(("arr", "#2563eb"), ("arrG", "#059669"))]
    parts.append('<line x1="240" y1="30" x2="240" y2="250" stroke="#94a3b8" stroke-width="5"/>')
    parts.append(_arrow(240, 130, 240, 50, color="#64748b", width=1.5, dash="5,4"))
    parts.append(_label(252, 90, "Normal", size=10, color="#64748b"))
    inc_w = 3.5 if hl == "incident" else 2.5
    ref_w = 3.5 if hl == "reflected" else 2.5
    parts.append(_arrow(60, 190, 240, 130, color="#2563eb", width=inc_w))
    parts.append(_label(130, 175, "Incident ray", size=10, color="#2563eb"))
    parts.append(_arrow(240, 130, 420, 70, color="#059669", width=ref_w, marker="arrG"))
    parts.append(_label(350, 88, "Reflected ray", size=10, color="#059669"))
    if hl == "incidence_point":
        parts.append('<circle cx="240" cy="130" r="6" fill="#6366f1"/>')
        parts.append(_label(240, 148, "Point of incidence", size=10, color="#6366f1", bold=True))
    return _svg_wrap(parts, title="Reflection at a plane mirror")


def svg_normal_angle(cfg: dict) -> str:
    hl = cfg.get("highlight", "")
    parts = [_defs(("arr", "#2563eb"), ("arrG", "#059669"))]
    parts.append('<line x1="240" y1="30" x2="240" y2="250" stroke="#94a3b8" stroke-width="5"/>')
    n_stroke = "#6366f1" if hl == "normal" else "#64748b"
    n_w = 2.5 if hl == "normal" else 1.5
    parts.append(_arrow(240, 200, 240, 45, color=n_stroke, width=n_w, dash="6,4"))
    parts.append(_label(255, 120, "Normal (90° to mirror)", size=10, color=n_stroke))
    parts.append(_arrow(50, 200, 240, 130, color="#2563eb", width=3 if hl == "angle_i" else 2.5))
    parts.append(_arrow(240, 130, 430, 60, color="#059669", width=3 if hl == "angle_r" else 2.5, marker="arrG"))
    parts.append('<path d="M240,130 L240,100 A30,30 0 0,0 215,112" fill="none" stroke="#2563eb" stroke-width="2"/>')
    parts.append('<path d="M240,130 L240,100 A30,30 0 0,1 265,112" fill="none" stroke="#059669" stroke-width="2"/>')
    parts.append(_label(225, 108, "i", color="#2563eb", bold=True))
    parts.append(_label(252, 108, "r", color="#059669", bold=True))
    if cfg.get("show_labels") or hl == "equal_angles":
        parts.append(_label(240, 230, "Angle of incidence = Angle of reflection", bold=True, color="#334155", size=11))
    return _svg_wrap(parts, title="Measure angles from the normal")


def svg_spherical_mirror_labels(cfg: dict) -> str:
    mtype = cfg.get("mirror_type", "concave")
    hl = cfg.get("highlight", "")
    if cfg.get("mode") == "compare":
        parts = [
            '<path d="M60,170 Q120,50 180,170" fill="none" stroke="#64748b" stroke-width="4"/>',
            _label(120, 195, "Concave (inward)", bold=True, size=11),
            '<path d="M280,170 Q340,50 400,170" fill="none" stroke="#64748b" stroke-width="4"/>',
            _label(340, 195, "Convex (outward)", bold=True, size=11),
            _label(120, 155, "reflecting side faces center", size=9, color="#64748b"),
        ]
        return _svg_wrap(parts, h=240, title="Compare mirror types")
    if mtype == "convex":
        arc = '<path d="M100,200 Q240,40 380,200" fill="none" stroke="#64748b" stroke-width="5"/>'
        axis_y, p_y, f_x, c_x = 200, 188, 160, 80
    else:
        arc = '<path d="M100,60 Q240,220 380,60" fill="none" stroke="#64748b" stroke-width="5"/>'
        axis_y, p_y, f_x, c_x = 60, 72, 320, 400
    parts = [arc, f'<line x1="40" y1="{axis_y}" x2="440" y2="{axis_y}" stroke="#cbd5e1" stroke-width="1.5"/>']
    labels = {"P": (240, p_y), "F": (f_x, axis_y), "C": (c_x, axis_y)}
    for key, (x, y) in labels.items():
        hi = hl == key or (hl == "principal_axis" and key == "P")
        r = 6 if hi else 4
        stroke = ' stroke="#6366f1" stroke-width="2"' if hi else ""
        parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#1e293b"{stroke}/>')
        parts.append(_label(x + 10, y + 4, key, anchor="start", bold=hi))
    if hl == "principal_axis":
        parts[1] = f'<line x1="40" y1="{axis_y}" x2="440" y2="{axis_y}" stroke="#6366f1" stroke-width="2.5"/>'
    parts.append(_label(240, axis_y + 22, "Principal axis", size=10, color="#64748b"))
    title = "Concave mirror" if mtype == "concave" else "Convex mirror"
    return _svg_wrap(parts, title=title)


def svg_mirror_focus_ray(cfg: dict) -> str:
    mtype = cfg.get("mirror_type", "concave")
    hl = cfg.get("highlight", "")
    if mtype == "convex":
        arc = '<path d="M100,210 Q240,50 380,210" fill="none" stroke="#64748b" stroke-width="5"/>'
        ay, fx = 210, 150
    else:
        arc = '<path d="M100,50 Q240,210 380,50" fill="none" stroke="#64748b" stroke-width="5"/>'
        ay, fx = 50, 330
    parts = [_defs(("arr", "#2563eb"), ("arrG", "#059669")), arc]
    parts.append(f'<line x1="40" y1="{ay}" x2="440" y2="{ay}" stroke="#cbd5e1" stroke-width="1.5"/>')
    parts.append(_arrow(40, ay, 240, ay, color="#2563eb"))
    parts.append(_label(130, ay - 12, "Parallel incident rays", size=10, color="#2563eb"))
    if mtype == "concave":
        parts.append(_arrow(240, ay, fx, ay, color="#059669", marker="arrG"))
        parts.append(_label(285, ay - 12, "Meet at F (real focus)", size=10, color="#059669"))
    else:
        parts.append(_arrow(240, ay, 380, ay - 50, color="#059669", marker="arrG"))
        parts.append(_label(310, ay - 55, "Diverge — appear from F", size=10, color="#059669"))
    parts.append(f'<circle cx="{fx}" cy="{ay}" r="5" fill="#6366f1"/>')
    parts.append(_label(fx, ay + 18, "F", bold=True))
    parts.append(f'<circle cx="240" cy="{ay}" r="4" fill="#1e293b"/>')
    parts.append(_label(240, ay + 18, "P"))
    if hl in ("R_2f", "P_F_C"):
        cx = 400 if mtype == "concave" else 80
        parts.append(f'<circle cx="{cx}" cy="{ay}" r="4" fill="#1e293b"/>')
        parts.append(_label(cx, ay + 18, "C"))
        parts.append(f'<line x1="240" y1="{ay+28}" x2="{cx}" y2="{ay+28}" stroke="#94a3b8"/>')
        parts.append(_label((240 + cx) / 2, ay + 42, "R = 2f", color="#64748b"))
    return _svg_wrap(parts, title="Focus and parallel rays")


def svg_concave_image(cfg: dict) -> str:
    """Concave/convex mirror with object and image positions."""
    position = cfg.get("position") or cfg.get("case", "beyond_c")
    mtype = cfg.get("mirror_type", "concave")
    ay = 50
    parts = [_defs(("arr", "#2563eb"), ("arrR", "#dc2626"))]
    if mtype == "convex":
        parts.append('<path d="M100,50 Q240,210 380,50" fill="none" stroke="#64748b" stroke-width="5"/>')
    else:
        parts.append('<path d="M100,50 Q240,210 380,50" fill="none" stroke="#64748b" stroke-width="5"/>')
    parts.append(f'<line x1="40" y1="{ay}" x2="440" y2="{ay}" stroke="#cbd5e1" stroke-width="1.5"/>')
    obj_x = {
        "infinity": 30,
        "beyond_C": 360,
        "beyond_c": 360,
        "at_C": 400,
        "at_c": 400,
        "between_C_F": 320,
        "between_c_f": 320,
        "at_F": 280,
        "at_f": 280,
        "between_F_P": 260,
        "between_f_p": 260,
    }
    ox = obj_x.get(position, 360)
    if position != "infinity":
        parts.append(f'<line x1="{ox}" y1="{ay}" x2="{ox}" y2="{ay-55}" stroke="#2563eb" stroke-width="3"/>')
        parts.append(_arrow(ox, ay - 55, ox, ay - 25, color="#2563eb"))
        parts.append(_label(ox, ay - 65, "Object", size=10, color="#2563eb"))
    else:
        parts.append(_arrow(60, ay - 30, 200, ay - 30, color="#2563eb"))
        parts.append(_arrow(60, ay - 10, 200, ay - 10, color="#2563eb"))
        parts.append(_label(100, ay - 45, "Parallel rays (object at ∞)", size=10, color="#2563eb"))
    if position in ("beyond_C", "beyond_c", "at_C", "at_c", "between_C_F", "between_c_f"):
        ix = 120 if position in ("beyond_C", "beyond_c") else 400
        ih = 25 if position in ("beyond_C", "beyond_c") else 55
        parts.append(f'<line x1="{ix}" y1="{ay}" x2="{ix}" y2="{ay-ih}" stroke="#dc2626" stroke-width="3" stroke-dasharray="4,3"/>')
        parts.append(_label(ix, ay + 18, "Real image", size=10, color="#dc2626"))
    elif position in ("between_F_P", "between_f_p") or mtype == "convex":
        parts.append(_label(100, ay - 30, "Virtual image behind mirror", size=10, color="#dc2626"))
    elif position in ("at_F", "at_f"):
        parts.append(_label(120, ay - 50, "Image at infinity", size=10, color="#dc2626"))
    fx = 280 if mtype == "concave" else 200
    parts.append(f'<circle cx="{fx}" cy="{ay}" r="4" fill="#6366f1"/>')
    parts.append(_label(fx, ay + 18, "F"))
    if mtype == "concave":
        parts.append(f'<circle cx="400" cy="{ay}" r="4" fill="#1e293b"/>')
        parts.append(_label(400, ay + 18, "C"))
    label = cfg.get("label") or cfg.get("mode") or position.replace("_", " ")
    parts.append(_label(240, 195, str(label).title(), size=11, color="#64748b"))
    return _svg_wrap(parts, title="Mirror image")


def svg_mirror_ray_rules(cfg: dict) -> str:
    """Two-ray rule diagram for mirrors."""
    rule = str(cfg.get("rule", "parallel")).lower().replace("_", "")
    highlight = cfg.get("highlight", "")
    ay = 50
    parts = [_defs(("arr", "#2563eb"), ("arrG", "#059669"))]
    parts.append('<path d="M100,50 Q240,210 380,50" fill="none" stroke="#64748b" stroke-width="5"/>')
    parts.append(f'<line x1="40" y1="{ay}" x2="440" y2="{ay}" stroke="#cbd5e1" stroke-width="1.5"/>')
    ox = 350
    parts.append(f'<circle cx="280" cy="{ay}" r="4" fill="#6366f1"/>')
    parts.append(_label(280, ay + 18, "F"))
    parts.append(f'<circle cx="240" cy="{ay}" r="4" fill="#1e293b"/>')
    parts.append(_label(240, ay + 18, "P"))
    if highlight in ("backward", "intersect", "locate", "errors"):
        parts.append(_arrow(ox, ay - 40, 240, ay - 40, color="#2563eb"))
        parts.append(_arrow(240, ay - 40, 280, ay, color="#059669", marker="arrG"))
        cap = {"backward": "Extend reflected rays backward (dotted)", "intersect": "Real image = forward intersection",
               "locate": "Two rays → image tip", "errors": "Check F, C, and ray rules"}
        parts.append(_label(260, ay - 55, cap.get(highlight, highlight), size=10))
    elif rule == "parallel" or rule == "tworays":
        parts.append(_arrow(ox, ay - 40, 240, ay - 40, color="#2563eb"))
        parts.append(_arrow(240, ay - 40, 280, ay, color="#059669", marker="arrG"))
        parts.append(_label(300, ay - 50, "Parallel → through F", size=10))
    elif rule == "throughf":
        parts.append(_arrow(ox, ay, 280, ay, color="#2563eb"))
        parts.append(_arrow(280, ay, 240, ay - 50, color="#059669", marker="arrG"))
        parts.append(_label(300, ay + 25, "Through F → parallel", size=10))
    elif rule == "throughc":
        parts.append(f'<circle cx="400" cy="{ay}" r="4" fill="#1e293b"/>')
        parts.append(_label(400, ay + 18, "C"))
        parts.append(_arrow(ox, ay, 400, ay, color="#2563eb"))
        parts.append(_arrow(400, ay, 240, ay - 50, color="#059669", marker="arrG"))
        parts.append(_label(300, ay + 25, "Through C → retraces", size=10))
    else:
        parts.append(_arrow(ox, ay, 240, ay, color="#2563eb"))
        parts.append(_arrow(240, ay, 200, ay - 40, color="#059669", marker="arrG"))
        parts.append(_label(280, ay + 25, "At pole → equal angles", size=10))
    return _svg_wrap(parts, title="Mirror ray rules")


def svg_sign_axis(cfg: dict) -> str:
    """Sign convention axis for mirrors or lenses."""
    medium = cfg.get("medium") or cfg.get("topic", "mirror")
    ay = 120
    parts = [_defs(("arr", "#2563eb"))]
    parts.append(f'<line x1="40" y1="{ay}" x2="440" y2="{ay}" stroke="#1e293b" stroke-width="2"/>')
    parts.append(_arrow(240, ay, 400, ay, color="#2563eb"))
    parts.append(_label(400, ay - 15, "+ x (incident side)", size=10, color="#2563eb"))
    parts.append(_arrow(240, ay, 80, ay, color="#64748b", marker="arr"))
    parts.append(_label(60, ay - 15, "− x", size=10, color="#64748b"))
    parts.append(_arrow(240, ay - 30, 240, ay - 70, color="#059669"))
    parts.append(_label(250, ay - 75, "+ y (up)", size=10, color="#059669"))
    parts.append(_arrow(240, ay + 30, 240, ay + 70, color="#dc2626"))
    parts.append(_label(250, ay + 85, "− y (down)", size=10, color="#dc2626"))
    parts.append(f'<circle cx="240" cy="{ay}" r="5" fill="#6366f1"/>')
    parts.append(_label(240, ay + 18, "P / O", bold=True))
    if medium == "mirror":
        parts.append('<path d="M100,50 Q240,210 380,50" fill="none" stroke="#64748b" stroke-width="4"/>')
        parts.append(_label(240, 200, "Mirror: object side +x, concave f < 0", size=10, color="#64748b"))
    else:
        parts.append('<ellipse cx="240" cy="120" rx="12" ry="55" fill="none" stroke="#64748b" stroke-width="4"/>')
        parts.append(_label(240, 200, "Lens: incident side +x, convex f > 0", size=10, color="#64748b"))
    return _svg_wrap(parts, title="Sign convention")


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
        '<rect x="60" y="60" width="360" height="120" rx="10" fill="#f8fafc" stroke="#cbd5e1" stroke-width="2"/>',
        f'<text x="240" y="115" text-anchor="middle" font-family="Georgia,serif" font-size="20" fill="#1e293b">{formula}</text>',
    ]
    if note:
        parts.append(_label(240, 155, str(note), size=11, color="#64748b"))
    return _svg_wrap(parts, h=220, title="Formula")


def svg_refraction(cfg: dict) -> str:
    """Refraction at a boundary."""
    mode = cfg.get("mode", "")
    direction = cfg.get("direction", "")
    if mode in ("toward", "air_glass", "denser"):
        direction = "into_denser"
    elif mode in ("away", "glass_air", "rarer"):
        direction = "into_rarer"
    elif not direction:
        direction = "into_denser"
    ay = 180
    parts = [_defs(("arr", "#2563eb"), ("arrG", "#059669"))]
    parts.append(f'<line x1="40" y1="{ay}" x2="440" y2="{ay}" stroke="#64748b" stroke-width="3"/>')
    parts.append('<rect x="40" y="180" width="400" height="60" fill="#dbeafe" opacity="0.5"/>')
    parts.append('<rect x="40" y="60" width="400" height="120" fill="#fef3c7" opacity="0.4"/>')
    parts.append(_label(80, 100, "rarer", size=10, color="#64748b"))
    parts.append(_label(80, 210, "denser", size=10, color="#64748b"))
    parts.append(f'<line x1="240" y1="40" x2="240" y2="220" stroke="#94a3b8" stroke-width="1.5" stroke-dasharray="4,3"/>')
    parts.append(_label(250, 50, "Normal", size=10, color="#64748b"))
    if direction == "into_denser":
        parts.append(_arrow(240, 80, 240, ay, color="#2563eb"))
        parts.append(_arrow(240, ay, 270, 220, color="#059669", marker="arrG"))
        parts.append(_label(300, 130, "Bends toward normal", size=10, color="#059669"))
    else:
        parts.append(_arrow(240, 220, 240, ay, color="#2563eb"))
        parts.append(_arrow(240, ay, 210, 80, color="#059669", marker="arrG"))
        parts.append(_label(160, 130, "Bends away from normal", size=10, color="#059669"))
    cap = mode or cfg.get("highlight", "")
    if cap:
        parts.append(_label(240, 235, str(cap).replace("_", " "), size=10, color="#64748b"))
    return _svg_wrap(parts, title="Refraction")


def svg_glass_slab(cfg: dict) -> str:
    """Rectangular glass slab — lateral displacement."""
    ay = 120
    parts = [_defs(("arr", "#2563eb"), ("arrG", "#059669"))]
    parts.append('<rect x="160" y="60" width="160" height="120" fill="#dbeafe" stroke="#64748b" stroke-width="2" opacity="0.7"/>')
    parts.append(_label(240, 55, "Glass slab", size=10, color="#64748b"))
    parts.append(_arrow(60, ay, 160, ay, color="#2563eb"))
    parts.append(_arrow(160, ay, 200, 100, color="#2563eb"))
    parts.append(_arrow(200, 100, 280, 100, color="#2563eb"))
    parts.append(_arrow(280, 100, 320, ay, color="#059669", marker="arrG"))
    parts.append(_arrow(320, ay, 420, ay, color="#059669", marker="arrG"))
    parts.append(f'<line x1="60" y1="{ay}" x2="420" y2="{ay}" stroke="#cbd5e1" stroke-width="1" stroke-dasharray="4,3"/>')
    parts.append(_label(240, ay + 25, "Emergent ray ∥ incident (lateral shift)", size=10, color="#64748b"))
    return _svg_wrap(parts, title="Glass slab")


def svg_lens_labels(cfg: dict) -> str:
    """Convex or concave lens with labels."""
    ltype = cfg.get("lens") or cfg.get("lens_type", "convex")
    ay = 120
    parts = [_defs()]
    parts.append(f'<line x1="40" y1="{ay}" x2="440" y2="{ay}" stroke="#cbd5e1" stroke-width="1.5"/>')
    if ltype == "convex":
        parts.append('<path d="M230,60 Q240,120 230,180 Q250,120 250,60 Q240,120 250,180" fill="none" stroke="#64748b" stroke-width="4"/>')
        parts.append('<ellipse cx="240" cy="120" rx="10" ry="60" fill="none" stroke="#64748b" stroke-width="3"/>')
        parts.append(_label(240, 200, "Convex (converging)", size=10, color="#059669"))
        fx1, fx2 = 180, 300
    else:
        parts.append('<path d="M230,60 Q220,120 230,180 M250,60 Q260,120 250,180" fill="none" stroke="#64748b" stroke-width="4"/>')
        parts.append(_label(240, 200, "Concave (diverging)", size=10, color="#dc2626"))
        fx1, fx2 = 300, 180
    parts.append(f'<circle cx="240" cy="{ay}" r="4" fill="#6366f1"/>')
    parts.append(_label(240, ay + 18, "O"))
    parts.append(f'<circle cx="{fx1}" cy="{ay}" r="4" fill="#6366f1"/>')
    parts.append(_label(fx1, ay + 18, "F₁"))
    parts.append(f'<circle cx="{fx2}" cy="{ay}" r="4" fill="#6366f1"/>')
    parts.append(_label(fx2, ay + 18, "F₂"))
    return _svg_wrap(parts, title="Lens labels")


def svg_lens_ray(cfg: dict) -> str:
    """Lens ray diagram."""
    rule = cfg.get("rule", "parallel")
    ltype = cfg.get("lens", "convex")
    ay = 120
    parts = [_defs(("arr", "#2563eb"), ("arrG", "#059669"))]
    parts.append(f'<line x1="40" y1="{ay}" x2="440" y2="{ay}" stroke="#cbd5e1" stroke-width="1.5"/>')
    parts.append('<ellipse cx="240" cy="120" rx="10" ry="60" fill="none" stroke="#64748b" stroke-width="3"/>')
    parts.append(f'<circle cx="300" cy="{ay}" r="4" fill="#6366f1"/>')
    parts.append(_label(300, ay + 18, "F"))
    parts.append(f'<circle cx="240" cy="{ay}" r="4" fill="#6366f1"/>')
    parts.append(_label(240, ay + 18, "O"))
    ox = 80
    if rule == "parallel":
        parts.append(_arrow(ox, ay - 40, 240, ay - 40, color="#2563eb"))
        parts.append(_arrow(240, ay - 40, 300, ay, color="#059669", marker="arrG"))
        parts.append(_label(320, ay - 50, "Parallel → through F", size=10))
    elif rule == "through_f":
        parts.append(_arrow(ox, ay, 300, ay, color="#2563eb"))
        parts.append(_arrow(300, ay, 240, ay - 50, color="#059669", marker="arrG"))
        parts.append(_label(320, ay + 25, "Through F → parallel", size=10))
    else:
        parts.append(_arrow(ox, ay, 240, ay, color="#2563eb"))
        parts.append(_arrow(240, ay, 380, ay, color="#059669", marker="arrG"))
        parts.append(_label(320, ay + 25, "Through O → undeviated", size=10))
    return _svg_wrap(parts, title="Lens rays")


def svg_lens_image(cfg: dict) -> str:
    """Lens image formation sketch."""
    case = cfg.get("case", "beyond_2f")
    ay = 120
    parts = [_defs(("arr", "#2563eb"), ("arrR", "#dc2626"))]
    parts.append(f'<line x1="40" y1="{ay}" x2="440" y2="{ay}" stroke="#cbd5e1" stroke-width="1.5"/>')
    parts.append('<ellipse cx="240" cy="120" rx="10" ry="60" fill="none" stroke="#64748b" stroke-width="3"/>')
    obj_x = {"beyond_2f": 100, "at_2f": 140, "between_f_2f": 170, "inside_f": 200}
    ox = obj_x.get(case, 100)
    parts.append(f'<line x1="{ox}" y1="{ay}" x2="{ox}" y2="{ay-50}" stroke="#2563eb" stroke-width="3"/>')
    parts.append(_label(ox, ay - 60, "Object", size=10, color="#2563eb"))
    if case == "inside_f":
        parts.append(_label(350, ay - 40, "Virtual, erect, enlarged", size=10, color="#dc2626"))
    else:
        ix = 340 if case != "at_2f" else 340
        parts.append(f'<line x1="{ix}" y1="{ay}" x2="{ix}" y2="{ay-30}" stroke="#dc2626" stroke-width="3" stroke-dasharray="4,3"/>')
        parts.append(_label(ix, ay + 18, "Real image", size=10, color="#dc2626"))
    parts.append(_label(240, 200, cfg.get("label", case.replace("_", " ")), size=10, color="#64748b"))
    return _svg_wrap(parts, title="Lens image")


def svg_placeholder(cfg: dict) -> str:
    label = str(cfg.get("label", "Diagram"))
    parts = [
        f'<rect x="80" y="80" width="320" height="100" rx="8" fill="#eef1f5" stroke="#d8dee6"/>',
        _label(240, 135, label, color="#64748b"),
    ]
    return _svg_wrap(parts, h=240)


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
    "placeholder": svg_placeholder,
}


def render_diagram_html(visual: dict) -> str:
    vtype = visual.get("type", "placeholder")
    fn = _RENDERERS.get(vtype, svg_placeholder)
    inner = fn(visual)
    return f'<div class="hp-diagram-wrap">{inner}</div>'
