"""
India map data for Sangeetha's GK app.

Provides:
  - Base64-encoded India map image for HTML embedding.
  - Coordinate database mapping location names to (x%, y%) positions on the map.
  - HTML renderer that overlays a pulsing marker on the map at a given location.
"""

import base64
import os

_MAP_PATH = os.path.join(os.path.dirname(__file__), "india_map", "india_map.png")
_MAP_B64: str | None = None


def _get_map_b64() -> str | None:
    """Load the India map as a base64 data URI (cached)."""
    global _MAP_B64
    if _MAP_B64:
        return _MAP_B64
    if not os.path.exists(_MAP_PATH):
        return None
    with open(_MAP_PATH, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    _MAP_B64 = f"data:image/png;base64,{encoded}"
    return _MAP_B64


# ── Location coordinates as (x%, y%) on the 512x640 map image ──
# These are approximate positions calibrated to the AI-generated map.
# x% = horizontal (0=left, 100=right), y% = vertical (0=top, 100=bottom)

LOCATIONS: dict[str, tuple[float, float]] = {
    # ── Major Cities ──
    "New Delhi":        (38, 28),
    "Delhi":            (38, 28),
    "Mumbai":           (22, 52),
    "Kolkata":          (62, 44),
    "Chennai":          (50, 70),
    "Bengaluru":        (42, 70),
    "Bangalore":        (42, 70),
    "Hyderabad":        (44, 58),
    "Ahmedabad":        (22, 40),
    "Pune":             (26, 55),
    "Jaipur":           (30, 32),
    "Lucknow":          (47, 32),
    "Chandigarh":       (34, 22),
    "Bhopal":           (36, 42),
    "Patna":            (55, 34),
    "Thiruvananthapuram":(38, 82),
    "Kochi":            (36, 76),
    "Bhubaneswar":      (56, 50),
    "Guwahati":         (72, 32),
    "Srinagar":         (32, 12),
    "Shimla":           (35, 20),
    "Dehradun":         (38, 22),
    "Ranchi":           (56, 42),
    "Raipur":           (48, 48),
    "Indore":           (30, 44),
    "Varanasi":         (50, 36),
    "Agra":             (40, 32),
    "Amritsar":         (30, 20),
    "Coimbatore":       (42, 74),
    "Visakhapatnam":    (54, 56),
    "Mysuru":           (40, 72),
    "Mysore":           (40, 72),
    "Madurai":          (44, 78),
    "Nagpur":           (40, 48),
    "Jodhpur":          (24, 34),
    "Udaipur":          (25, 38),
    "Goa":              (26, 62),
    "Panaji":           (26, 62),
    "Imphal":           (78, 36),
    "Gangtok":          (64, 30),
    "Shillong":         (72, 34),
    "Itanagar":         (76, 28),
    "Kohima":           (78, 34),
    "Aizawl":           (76, 38),
    "Agartala":         (74, 38),
    "Port Blair":       (76, 72),
    "Dispur":           (72, 32),

    # ── States (center-ish positions) ──
    "Rajasthan":        (24, 34),
    "Maharashtra":      (28, 54),
    "Karnataka":        (38, 68),
    "Tamil Nadu":       (44, 76),
    "Kerala":           (36, 78),
    "Gujarat":          (18, 40),
    "Uttar Pradesh":    (44, 34),
    "Madhya Pradesh":   (36, 44),
    "Bihar":            (56, 36),
    "West Bengal":      (62, 42),
    "Odisha":           (54, 50),
    "Andhra Pradesh":   (48, 62),
    "Telangana":        (44, 58),
    "Punjab":           (30, 22),
    "Haryana":          (34, 26),
    "Uttarakhand":      (38, 22),
    "Himachal Pradesh": (34, 18),
    "Jammu and Kashmir":(30, 12),
    "Jharkhand":        (56, 42),
    "Chhattisgarh":     (48, 48),
    "Assam":            (72, 32),
    "Goa":              (26, 62),
    "Meghalaya":        (70, 34),
    "Tripura":          (74, 38),
    "Manipur":          (78, 36),
    "Mizoram":          (76, 38),
    "Nagaland":         (78, 34),
    "Arunachal Pradesh":(76, 26),
    "Sikkim":           (64, 30),

    # ── Rivers ──
    "Ganga":            (50, 34),
    "Ganges":           (50, 34),
    "Yamuna":           (40, 30),
    "Brahmaputra":      (72, 30),
    "Godavari":         (46, 56),
    "Krishna":          (42, 62),
    "Narmada":          (30, 44),
    "Kaveri":           (42, 72),
    "Cauvery":          (42, 72),
    "Tapti":            (28, 48),
    "Mahanadi":         (52, 48),
    "Sutlej":           (32, 20),
    "Indus":            (26, 14),
    "Chambal":          (32, 38),
    "Tungabhadra":      (40, 64),
    "Sabarmati":        (20, 40),

    # ── South Indian Rivers ──
    "Vaigai":           (46, 78),
    "Periyar":          (36, 76),
    "Pamba":            (38, 80),
    "Bharathappuzha":   (36, 76),
    "Nila":             (36, 76),
    "Chaliyar":         (34, 74),
    "Pennar":           (48, 64),
    "Chitravathi":      (44, 64),
    "Hemavathi":        (40, 70),
    "Kabini":           (40, 72),
    "Arkavathi":        (42, 70),
    "Nethravathi":      (36, 72),
    "Sharavathi":       (34, 68),
    "Moyar":            (40, 74),
    "Amaravathi":       (42, 74),
    "Tamiraparani":     (44, 82),
    "Bhavani":          (42, 74),

    # ── Mountains & Ranges ──
    "Himalayas":        (42, 16),
    "Western Ghats":    (30, 66),
    "Eastern Ghats":    (50, 64),
    "Aravalli":         (26, 34),
    "Vindhya":          (36, 42),
    "Satpura":          (32, 44),
    "Nilgiri":          (40, 74),
    "Mount Everest":    (60, 26),
    "Kanchenjunga":     (64, 28),
    "K2":               (28, 8),

    # ── Seas & Coasts ──
    "Arabian Sea":      (10, 58),
    "Bay of Bengal":    (68, 58),
    "Indian Ocean":     (44, 90),
    "Lakshadweep Sea":  (28, 76),
    "Andaman Sea":      (80, 66),

    # ── Historical & Famous Places ──
    "Taj Mahal":        (40, 32),
    "Red Fort":         (38, 28),
    "Qutub Minar":      (38, 28),
    "Gateway of India":  (22, 52),
    "Hampi":            (38, 64),
    "Konark":           (56, 50),
    "Khajuraho":        (42, 40),
    "Ajanta":           (30, 52),
    "Ellora":           (30, 52),
    "Sanchi":           (36, 42),
    "Meenakshi Temple": (44, 78),
    "Golden Temple":    (30, 20),
    "Hawa Mahal":       (30, 32),
    "Charminar":        (44, 58),
    "Victoria Memorial":(62, 44),
    "Jallianwala Bagh": (30, 20),
    "Sabarmati Ashram": (20, 40),
    "Dandi":            (18, 46),

    # ── Union Territories ──
    "Andaman and Nicobar Islands": (76, 72),
    "Andaman and Nicobar": (76, 72),
    "Chandigarh":       (34, 22),
    "Dadra and Nagar Haveli and Daman and Diu": (18, 46),
    "Daman and Diu":    (18, 46),
    "Dadra and Nagar Haveli": (18, 46),
    "Delhi":            (38, 28),
    "NCT of Delhi":     (38, 28),
    "Ladakh":           (28, 8),
    "Lakshadweep":      (22, 80),
    "Puducherry":       (52, 72),
    "Pondicherry":      (52, 72),

    # ── National Monuments ──
    "India Gate":           (38, 28),
    "Sanchi Stupa":         (36, 42),
    "Konark Sun Temple":    (56, 50),
    "Brihadeeswarar Temple":(46, 74),
    "Meenakshi Amman Temple":(44, 78),
    "Ajanta Caves":         (30, 52),
    "Ellora Caves":         (30, 52),
    "Fatehpur Sikri":       (40, 32),
    "Jantar Mantar":        (30, 32),
    "Buland Darwaza":       (40, 32),
    "Golconda Fort":        (44, 58),
    "Mysore Palace":        (40, 72),
    "Rashtrapati Bhavan":   (38, 28),
    "Parliament House":     (38, 28),
    "Cellular Jail":        (76, 72),
}


def get_location_coords(location_name: str) -> tuple[float, float] | None:
    """Look up coordinates for a location name (case-insensitive fuzzy match)."""
    if not location_name:
        return None

    # Exact match
    if location_name in LOCATIONS:
        return LOCATIONS[location_name]

    # Case-insensitive match
    lower = location_name.lower().strip()
    for key, coords in LOCATIONS.items():
        if key.lower() == lower:
            return coords

    # Partial match (location name contains or is contained in a key)
    for key, coords in LOCATIONS.items():
        if lower in key.lower() or key.lower() in lower:
            return coords

    return None


# ── Permanent geographic features shown on every map render ──
# Each: (label, x%, y%, color, icon)

MAP_RIVERS = [
    ("Ganga",       50, 34, "#2563eb", "〰️"),
    ("Yamuna",      38, 30, "#2563eb", "〰️"),
    ("Brahmaputra", 74, 30, "#2563eb", "〰️"),
    ("Godavari",    46, 57, "#2563eb", "〰️"),
    ("Krishna",     40, 63, "#2563eb", "〰️"),
    ("Narmada",     28, 45, "#2563eb", "〰️"),
    ("Kaveri",      40, 73, "#2563eb", "〰️"),
    ("Tungabhadra", 38, 65, "#3b82f6", "〰️"),
    ("Periyar",     34, 77, "#3b82f6", "〰️"),
    ("Vaigai",      46, 78, "#3b82f6", "〰️"),
    ("Pennar",      48, 64, "#3b82f6", "〰️"),
]

MAP_MOUNTAINS = [
    ("Himalayas",     42, 14, "#92400e", "▲"),
    ("Western Ghats", 24, 67, "#92400e", "▲"),
    ("Eastern Ghats", 52, 64, "#92400e", "▲"),
    ("Aravalli",      24, 32, "#92400e", "▲"),
]

MAP_SEAS = [
    ("Arabian Sea",  8,  58, "#0891b2", "🌊"),
    ("Bay of Bengal", 70, 58, "#0891b2", "🌊"),
    ("Indian Ocean", 44, 92, "#0891b2", "🌊"),
]


def _render_feature_labels() -> str:
    """Build HTML for all permanent geographic feature labels."""
    html_parts = []

    for label, x, y, color, icon in MAP_RIVERS:
        html_parts.append(
            f'<div style="position:absolute;left:{x}%;top:{y}%;transform:translate(-50%,-50%);z-index:3;'
            f'font-size:0.5rem;font-weight:700;color:{color};white-space:nowrap;'
            f'text-shadow:0 0 3px white, 0 0 3px white, 0 0 3px white;'
            f'pointer-events:none;">'
            f'{icon} {label}</div>'
        )

    for label, x, y, color, icon in MAP_MOUNTAINS:
        html_parts.append(
            f'<div style="position:absolute;left:{x}%;top:{y}%;transform:translate(-50%,-50%);z-index:3;'
            f'font-size:0.5rem;font-weight:700;color:{color};white-space:nowrap;'
            f'text-shadow:0 0 3px white, 0 0 3px white, 0 0 3px white;'
            f'pointer-events:none;">'
            f'{icon} {label}</div>'
        )

    for label, x, y, color, icon in MAP_SEAS:
        html_parts.append(
            f'<div style="position:absolute;left:{x}%;top:{y}%;transform:translate(-50%,-50%);z-index:3;'
            f'font-size:0.55rem;font-weight:700;color:{color};white-space:nowrap;font-style:italic;'
            f'text-shadow:0 0 3px white, 0 0 3px white, 0 0 3px white;'
            f'pointer-events:none;">'
            f'{icon} {label}</div>'
        )

    return "\n".join(html_parts)


def render_map_with_marker(location_name: str, label: str = "") -> str | None:
    """Return HTML for the India map with geographic labels and a pulsing
    marker at the given location.

    Returns None if the map image doesn't exist or the location isn't found.
    """
    map_b64 = _get_map_b64()
    if not map_b64:
        return None

    coords = get_location_coords(location_name)
    if not coords:
        return None

    x, y = coords
    display_label = label or location_name
    feature_labels = _render_feature_labels()

    return f"""
    <div style="position:relative;display:inline-block;width:100%;max-width:420px;margin:0.5rem auto;border-radius:20px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.12);">
        <img src="{map_b64}" style="width:100%;display:block;border-radius:20px;" />
        {feature_labels}
        <div style="position:absolute;left:{x}%;top:{y}%;transform:translate(-50%,-50%);z-index:10;">
            <div style="
                width:18px;height:18px;
                background:#ef4444;
                border:3px solid white;
                border-radius:50%;
                box-shadow:0 0 0 3px #ef4444, 0 2px 8px rgba(0,0,0,0.3);
                animation: map-pulse 1.5s ease-in-out infinite;
            "></div>
        </div>
        <div style="position:absolute;left:{x}%;top:{min(y + 4, 94)}%;transform:translateX(-50%);z-index:10;
                    background:rgba(0,0,0,0.8);color:white;padding:3px 10px;border-radius:8px;
                    font-size:0.7rem;font-weight:600;white-space:nowrap;
                    box-shadow:0 2px 6px rgba(0,0,0,0.2);">
            📍 {display_label}
        </div>
    </div>
    <style>
        @keyframes map-pulse {{
            0%   {{ box-shadow: 0 0 0 3px #ef4444, 0 0 0 6px rgba(239,68,68,0.4); }}
            50%  {{ box-shadow: 0 0 0 5px #ef4444, 0 0 0 14px rgba(239,68,68,0.15); }}
            100% {{ box-shadow: 0 0 0 3px #ef4444, 0 0 0 6px rgba(239,68,68,0.4); }}
        }}
    </style>
    """
