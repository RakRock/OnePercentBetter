"""
India map data for Sangeetha's GK app.

Uses REAL geographic data:
  - India map image generated from GeoJSON boundaries (matplotlib).
  - All locations use real latitude/longitude coordinates.
  - Lat/lon is converted to image (x%, y%) at render time using the map's bounds.
"""

import base64
import os

_MAP_PATH = os.path.join(os.path.dirname(__file__), "india_map", "india_map.png")
_MAP_B64: str | None = None

# India map bounds (set in generate_state_maps_geo.py → plot_india)
_INDIA_LON_MIN = 67
_INDIA_LON_MAX = 98
_INDIA_LAT_MIN = 6
_INDIA_LAT_MAX = 38


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


def _latlon_to_india_pct(lat: float, lon: float) -> tuple[float, float]:
    """Convert lat/lon to (x%, y%) on the India map image."""
    x_pct = ((lon - _INDIA_LON_MIN) / (_INDIA_LON_MAX - _INDIA_LON_MIN)) * 100
    y_pct = ((_INDIA_LAT_MAX - lat) / (_INDIA_LAT_MAX - _INDIA_LAT_MIN)) * 100
    x_pct = max(2, min(98, x_pct))
    y_pct = max(2, min(98, y_pct))
    return (round(x_pct, 1), round(y_pct, 1))


# ══════════════════════════════════════════════════════════════════
# REAL LAT/LON COORDINATES — (latitude, longitude)
# All positions are actual geographic coordinates.
# ══════════════════════════════════════════════════════════════════

LOCATIONS: dict[str, tuple[float, float]] = {
    # ── Major Cities ──
    "New Delhi":        (28.61, 77.21),
    "Delhi":            (28.65, 77.23),
    "Mumbai":           (19.08, 72.88),
    "Kolkata":          (22.57, 88.36),
    "Chennai":          (13.08, 80.27),
    "Bengaluru":        (12.97, 77.59),
    "Bangalore":        (12.97, 77.59),
    "Hyderabad":        (17.38, 78.49),
    "Ahmedabad":        (23.02, 72.57),
    "Pune":             (18.52, 73.86),
    "Jaipur":           (26.91, 75.79),
    "Lucknow":          (26.85, 80.95),
    "Chandigarh":       (30.73, 76.78),
    "Bhopal":           (23.26, 77.41),
    "Patna":            (25.61, 85.14),
    "Thiruvananthapuram": (8.52, 76.94),
    "Kochi":            (9.93, 76.27),
    "Bhubaneswar":      (20.30, 85.82),
    "Guwahati":         (26.14, 91.74),
    "Srinagar":         (34.08, 74.80),
    "Shimla":           (31.10, 77.17),
    "Dehradun":         (30.32, 78.03),
    "Ranchi":           (23.34, 85.31),
    "Raipur":           (21.25, 81.63),
    "Indore":           (22.72, 75.86),
    "Varanasi":         (25.32, 83.01),
    "Agra":             (27.18, 78.02),
    "Amritsar":         (31.63, 74.87),
    "Coimbatore":       (11.00, 76.96),
    "Visakhapatnam":    (17.69, 83.22),
    "Mysuru":           (12.30, 76.65),
    "Mysore":           (12.30, 76.65),
    "Madurai":          (9.92, 78.12),
    "Nagpur":           (21.15, 79.09),
    "Jodhpur":          (26.29, 73.02),
    "Udaipur":          (24.59, 73.68),
    "Goa":              (15.50, 73.83),
    "Panaji":           (15.50, 73.83),
    "Imphal":           (24.82, 93.95),
    "Gangtok":          (27.33, 88.61),
    "Shillong":         (25.57, 91.88),
    "Itanagar":         (27.10, 93.62),
    "Kohima":           (25.67, 94.12),
    "Aizawl":           (23.73, 92.72),
    "Agartala":         (23.83, 91.28),
    "Port Blair":       (11.67, 92.73),
    "Dispur":           (26.14, 91.79),

    # ── States (approximate center positions) ──
    "Rajasthan":        (26.50, 73.80),
    "Maharashtra":      (19.50, 76.00),
    "Karnataka":        (15.00, 76.00),
    "Tamil Nadu":       (11.00, 78.50),
    "Kerala":           (10.50, 76.20),
    "Gujarat":          (22.30, 71.80),
    "Uttar Pradesh":    (27.00, 81.00),
    "Madhya Pradesh":   (23.50, 78.50),
    "Bihar":            (25.80, 85.80),
    "West Bengal":      (24.00, 87.80),
    "Odisha":           (20.50, 84.50),
    "Andhra Pradesh":   (16.00, 80.50),
    "Telangana":        (17.80, 79.30),
    "Punjab":           (31.00, 75.50),
    "Haryana":          (29.00, 76.00),
    "Uttarakhand":      (30.00, 79.30),
    "Himachal Pradesh": (31.80, 77.30),
    "Jammu and Kashmir": (33.70, 75.10),
    "Jharkhand":        (23.60, 85.50),
    "Chhattisgarh":     (21.50, 82.30),
    "Assam":            (26.20, 92.90),
    "Meghalaya":        (25.50, 91.30),
    "Tripura":          (23.75, 91.75),
    "Manipur":          (24.80, 93.90),
    "Mizoram":          (23.30, 92.85),
    "Nagaland":         (26.00, 94.50),
    "Arunachal Pradesh": (28.00, 94.50),
    "Sikkim":           (27.50, 88.50),

    # ── Union Territories ──
    "Andaman and Nicobar Islands": (11.67, 92.73),
    "Andaman and Nicobar": (11.67, 92.73),
    "Dadra and Nagar Haveli and Daman and Diu": (20.40, 73.00),
    "Daman and Diu":    (20.40, 73.00),
    "Dadra and Nagar Haveli": (20.40, 73.00),
    "NCT of Delhi":     (28.61, 77.21),
    "Ladakh":           (34.16, 77.58),
    "Lakshadweep":      (10.57, 72.64),
    "Puducherry":       (11.93, 79.83),
    "Pondicherry":      (11.93, 79.83),

    # ── Rivers ──
    "Ganga":            (25.50, 81.50),
    "Ganges":           (25.50, 81.50),
    "Yamuna":           (27.50, 77.70),
    "Brahmaputra":      (26.50, 93.00),
    "Godavari":         (17.50, 81.00),
    "Krishna":          (16.50, 78.50),
    "Narmada":          (22.50, 76.00),
    "Kaveri":           (11.50, 77.50),
    "Cauvery":          (11.50, 77.50),
    "Tapti":            (21.20, 75.50),
    "Mahanadi":         (20.50, 84.50),
    "Sutlej":           (31.00, 76.00),
    "Indus":            (34.00, 76.00),
    "Chambal":          (26.00, 76.50),
    "Tungabhadra":      (15.50, 76.50),
    "Sabarmati":        (23.06, 72.58),

    # ── South Indian Rivers ──
    "Vaigai":           (9.90, 78.10),
    "Periyar":          (9.47, 77.17),
    "Pamba":            (9.40, 76.70),
    "Bharathappuzha":   (10.78, 75.95),
    "Nila":             (10.78, 75.95),
    "Chaliyar":         (11.17, 75.90),
    "Pennar":           (14.60, 79.80),
    "Chitravathi":      (14.50, 77.60),
    "Hemavathi":        (13.10, 76.05),
    "Kabini":           (11.95, 76.30),
    "Arkavathi":        (12.90, 77.50),
    "Nethravathi":      (12.80, 75.00),
    "Sharavathi":       (14.10, 74.80),
    "Moyar":            (11.55, 76.55),
    "Amaravathi":       (11.00, 78.20),
    "Tamiraparani":     (8.75, 77.70),
    "Bhavani":          (11.45, 77.68),

    # ── Mountains & Ranges ──
    "Himalayas":        (30.50, 79.00),
    "Western Ghats":    (13.00, 75.50),
    "Eastern Ghats":    (15.50, 80.00),
    "Aravalli":         (25.00, 73.50),
    "Vindhya":          (23.50, 78.00),
    "Satpura":          (22.50, 77.50),
    "Nilgiri":          (11.40, 76.70),
    "Mount Everest":    (27.99, 86.93),
    "Kanchenjunga":     (27.70, 88.15),
    "K2":               (35.88, 76.51),

    # ── Seas & Coasts ──
    "Arabian Sea":      (15.00, 68.50),
    "Bay of Bengal":    (15.00, 88.00),
    "Indian Ocean":     (8.00, 78.00),
    "Lakshadweep Sea":  (10.00, 73.00),
    "Andaman Sea":      (12.00, 93.50),

    # ── Historical & Famous Places ──
    "Taj Mahal":        (27.17, 78.04),
    "Red Fort":         (28.66, 77.24),
    "Qutub Minar":      (28.52, 77.19),
    "Gateway of India":  (18.92, 72.83),
    "Hampi":            (15.33, 76.46),
    "Konark":           (19.88, 86.09),
    "Khajuraho":        (24.85, 79.92),
    "Ajanta":           (20.55, 75.70),
    "Ellora":           (20.02, 75.18),
    "Sanchi":           (23.48, 77.74),
    "Meenakshi Temple": (9.92, 78.12),
    "Golden Temple":    (31.62, 74.88),
    "Hawa Mahal":       (26.92, 75.83),
    "Charminar":        (17.36, 78.47),
    "Victoria Memorial": (22.54, 88.34),
    "Jallianwala Bagh": (31.62, 74.88),
    "Sabarmati Ashram": (23.06, 72.58),
    "Dandi":            (20.92, 72.83),

    # ── National Monuments ──
    "India Gate":           (28.61, 77.23),
    "Sanchi Stupa":         (23.48, 77.74),
    "Konark Sun Temple":    (19.88, 86.09),
    "Brihadeeswarar Temple": (10.78, 79.13),
    "Meenakshi Amman Temple": (9.92, 78.12),
    "Ajanta Caves":         (20.55, 75.70),
    "Ellora Caves":         (20.02, 75.18),
    "Fatehpur Sikri":       (27.09, 77.66),
    "Jantar Mantar":        (26.92, 75.83),
    "Buland Darwaza":       (27.09, 77.66),
    "Golconda Fort":        (17.38, 78.40),
    "Mysore Palace":        (12.30, 76.65),
    "Rashtrapati Bhavan":   (28.62, 77.20),
    "Parliament House":     (28.62, 77.21),
    "Cellular Jail":        (11.69, 92.75),
}


def get_location_coords(location_name: str) -> tuple[float, float] | None:
    """Look up (x%, y%) image coordinates for a location on the India map."""
    if not location_name:
        return None

    latlon = None

    # Exact match
    if location_name in LOCATIONS:
        latlon = LOCATIONS[location_name]
    else:
        # Case-insensitive match
        lower = location_name.lower().strip()
        for key, coords in LOCATIONS.items():
            if key.lower() == lower:
                latlon = coords
                break
        if not latlon:
            # Partial match
            for key, coords in LOCATIONS.items():
                if lower in key.lower() or key.lower() in lower:
                    latlon = coords
                    break

    if latlon:
        return _latlon_to_india_pct(latlon[0], latlon[1])

    return None


# ── Permanent geographic features shown on every map render ──
# Each: (label, lat, lon, color, icon)

MAP_RIVERS = [
    ("Ganga",       25.50, 81.50, "#2563eb", "〰️"),
    ("Yamuna",      27.50, 77.70, "#2563eb", "〰️"),
    ("Brahmaputra", 26.50, 93.00, "#2563eb", "〰️"),
    ("Godavari",    17.50, 81.00, "#2563eb", "〰️"),
    ("Krishna",     16.50, 78.50, "#2563eb", "〰️"),
    ("Narmada",     22.50, 76.00, "#2563eb", "〰️"),
    ("Kaveri",      11.50, 77.50, "#2563eb", "〰️"),
    ("Tungabhadra", 15.50, 76.50, "#3b82f6", "〰️"),
    ("Periyar",     9.47, 77.17, "#3b82f6", "〰️"),
    ("Vaigai",      9.90, 78.10, "#3b82f6", "〰️"),
    ("Pennar",      14.60, 79.80, "#3b82f6", "〰️"),
]

MAP_MOUNTAINS = [
    ("Himalayas",     30.50, 79.00, "#92400e", "▲"),
    ("Western Ghats", 13.00, 75.50, "#92400e", "▲"),
    ("Eastern Ghats", 15.50, 80.00, "#92400e", "▲"),
    ("Aravalli",      25.00, 73.50, "#92400e", "▲"),
]

MAP_SEAS = [
    ("Arabian Sea",  15.00, 68.50, "#0891b2", "🌊"),
    ("Bay of Bengal", 15.00, 88.00, "#0891b2", "🌊"),
    ("Indian Ocean", 8.00, 78.00, "#0891b2", "🌊"),
]


def _render_feature_labels() -> str:
    """Build HTML for all permanent geographic feature labels."""
    html_parts = []

    for label, lat, lon, color, icon in MAP_RIVERS:
        x, y = _latlon_to_india_pct(lat, lon)
        html_parts.append(
            f'<div style="position:absolute;left:{x}%;top:{y}%;transform:translate(-50%,-50%);z-index:3;'
            f'font-size:0.5rem;font-weight:700;color:{color};white-space:nowrap;'
            f'text-shadow:0 0 3px white, 0 0 3px white, 0 0 3px white;'
            f'pointer-events:none;">'
            f'{icon} {label}</div>'
        )

    for label, lat, lon, color, icon in MAP_MOUNTAINS:
        x, y = _latlon_to_india_pct(lat, lon)
        html_parts.append(
            f'<div style="position:absolute;left:{x}%;top:{y}%;transform:translate(-50%,-50%);z-index:3;'
            f'font-size:0.5rem;font-weight:700;color:{color};white-space:nowrap;'
            f'text-shadow:0 0 3px white, 0 0 3px white, 0 0 3px white;'
            f'pointer-events:none;">'
            f'{icon} {label}</div>'
        )

    for label, lat, lon, color, icon in MAP_SEAS:
        x, y = _latlon_to_india_pct(lat, lon)
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
    <div style="position:relative;display:inline-block;width:100%;max-width:420px;margin:0.5rem auto;border-radius:20px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.12);background:white;">
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
