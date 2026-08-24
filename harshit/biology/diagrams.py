"""NCERT-style labeled SVG diagrams for Harshit Biology Unit 1."""

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
