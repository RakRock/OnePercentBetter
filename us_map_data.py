"""
US map data for Rakesh's GK app.

Uses REAL geographic data:
  - US map image generated from GeoJSON boundaries (matplotlib).
  - All locations use real latitude/longitude coordinates.
  - Lat/lon is converted to image (x%, y%) at render time.
"""

import base64
import os

_MAP_PATH = os.path.join(os.path.dirname(__file__), "us_map", "us_map.png")
_MAP_B64: str | None = None

# Contiguous US map bounds (set in generate_us_maps.py → plot_us)
_US_LON_MIN = -125
_US_LON_MAX = -66
_US_LAT_MIN = 24
_US_LAT_MAX = 50


def _get_map_b64() -> str | None:
    global _MAP_B64
    if _MAP_B64:
        return _MAP_B64
    if not os.path.exists(_MAP_PATH):
        return None
    with open(_MAP_PATH, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    _MAP_B64 = f"data:image/png;base64,{encoded}"
    return _MAP_B64


def _latlon_to_us_pct(lat: float, lon: float) -> tuple[float, float]:
    """Convert lat/lon to (x%, y%) on the US map image."""
    x_pct = ((lon - _US_LON_MIN) / (_US_LON_MAX - _US_LON_MIN)) * 100
    y_pct = ((_US_LAT_MAX - lat) / (_US_LAT_MAX - _US_LAT_MIN)) * 100
    x_pct = max(2, min(98, x_pct))
    y_pct = max(2, min(98, y_pct))
    return (round(x_pct, 1), round(y_pct, 1))


# ══════════════════════════════════════════════
# REAL LAT/LON COORDINATES — (latitude, longitude)
# ══════════════════════════════════════════════

LOCATIONS: dict[str, tuple[float, float]] = {
    # ── Major Cities ──
    "Washington D.C.":  (38.91, -77.04),
    "New York City":    (40.71, -74.01),
    "New York":         (40.71, -74.01),
    "Los Angeles":      (34.05, -118.24),
    "Chicago":          (41.88, -87.63),
    "Houston":          (29.76, -95.37),
    "Phoenix":          (33.45, -112.07),
    "Philadelphia":     (39.95, -75.17),
    "San Antonio":      (29.42, -98.49),
    "San Diego":        (32.72, -117.16),
    "Dallas":           (32.78, -96.80),
    "San Francisco":    (37.77, -122.42),
    "Austin":           (30.27, -97.74),
    "Seattle":          (47.61, -122.33),
    "Denver":           (39.74, -104.99),
    "Boston":           (42.36, -71.06),
    "Nashville":        (36.16, -86.78),
    "Las Vegas":        (36.17, -115.14),
    "Portland":         (45.52, -122.68),
    "Miami":            (25.76, -80.19),
    "Atlanta":          (33.75, -84.39),
    "Minneapolis":      (44.98, -93.27),
    "New Orleans":      (29.95, -90.07),
    "Detroit":          (42.33, -83.05),
    "Salt Lake City":   (40.76, -111.89),
    "Honolulu":         (21.31, -157.86),

    # ── State Capitals ──
    "Sacramento":       (38.58, -121.49),
    "Tallahassee":      (30.44, -84.28),
    "Columbus":         (39.96, -82.99),
    "Raleigh":          (35.78, -78.64),
    "Richmond":         (37.54, -77.44),
    "Harrisburg":       (40.27, -76.88),
    "Annapolis":        (38.97, -76.49),
    "Baton Rouge":      (30.45, -91.19),
    "Montgomery":       (32.38, -86.30),
    "Jackson":          (32.30, -90.18),
    "Springfield":      (39.80, -89.65),
    "Indianapolis":     (39.77, -86.16),
    "Madison":          (43.07, -89.40),
    "St. Paul":         (44.94, -93.09),
    "Des Moines":       (41.59, -93.62),
    "Topeka":           (39.05, -95.68),
    "Jefferson City":   (38.58, -92.17),
    "Little Rock":      (34.75, -92.29),
    "Oklahoma City":    (35.47, -97.52),
    "Santa Fe":         (35.69, -105.94),
    "Helena":           (46.59, -112.04),
    "Boise":            (43.62, -116.21),
    "Olympia":          (47.04, -122.90),
    "Salem":            (44.94, -123.03),
    "Carson City":      (39.16, -119.77),
    "Juneau":           (58.30, -134.42),
    "Cheyenne":         (41.14, -104.82),
    "Bismarck":         (46.81, -100.78),
    "Pierre":           (44.37, -100.35),
    "Lincoln":          (40.81, -96.70),
    "Concord":          (43.21, -71.54),
    "Montpelier":       (44.26, -72.58),
    "Augusta":          (44.31, -69.78),
    "Hartford":         (41.76, -72.68),
    "Providence":       (41.82, -71.41),
    "Trenton":          (40.22, -74.76),
    "Dover":            (39.16, -75.52),
    "Frankfort":        (38.20, -84.87),
    "Charleston":       (38.35, -81.63),
    "Columbia":         (34.00, -81.03),

    # ── States (approximate centers) ──
    "Alabama":          (32.80, -86.80),
    "Alaska":           (64.00, -153.00),
    "Arizona":          (34.30, -111.70),
    "Arkansas":         (34.80, -92.20),
    "California":       (37.00, -120.00),
    "Colorado":         (39.00, -105.50),
    "Connecticut":      (41.60, -72.70),
    "Delaware":         (39.00, -75.50),
    "District of Columbia": (38.91, -77.04),
    "Florida":          (28.50, -82.00),
    "Georgia":          (33.00, -83.50),
    "Hawaii":           (21.31, -157.86),
    "Idaho":            (44.50, -114.50),
    "Illinois":         (40.00, -89.50),
    "Indiana":          (39.80, -86.20),
    "Iowa":             (42.00, -93.50),
    "Kansas":           (38.50, -98.50),
    "Kentucky":         (37.80, -85.50),
    "Louisiana":        (31.00, -92.00),
    "Maine":            (45.50, -69.00),
    "Maryland":         (39.00, -76.70),
    "Massachusetts":    (42.30, -71.80),
    "Michigan":         (44.00, -84.50),
    "Minnesota":        (46.00, -94.50),
    "Mississippi":      (32.75, -89.70),
    "Missouri":         (38.50, -92.50),
    "Montana":          (47.00, -110.00),
    "Nebraska":         (41.50, -100.00),
    "Nevada":           (39.50, -117.00),
    "New Hampshire":    (43.70, -71.60),
    "New Jersey":       (40.20, -74.70),
    "New Mexico":       (34.50, -106.00),
    "New York":         (43.00, -75.50),
    "North Carolina":   (35.50, -80.00),
    "North Dakota":     (47.50, -100.50),
    "Ohio":             (40.30, -82.50),
    "Oklahoma":         (35.50, -97.50),
    "Oregon":           (44.00, -120.50),
    "Pennsylvania":     (41.00, -77.50),
    "Rhode Island":     (41.70, -71.50),
    "South Carolina":   (34.00, -81.00),
    "South Dakota":     (44.50, -100.50),
    "Tennessee":        (35.80, -86.50),
    "Texas":            (31.50, -99.50),
    "Utah":             (39.50, -111.50),
    "Vermont":          (44.00, -72.70),
    "Virginia":         (37.50, -79.00),
    "Washington":       (47.50, -120.50),
    "West Virginia":    (38.60, -80.60),
    "Wisconsin":        (44.50, -90.00),
    "Wyoming":          (43.00, -107.50),

    # ── Rivers ──
    "Mississippi River": (32.30, -90.90),
    "Missouri River":   (41.00, -96.00),
    "Colorado River":   (36.00, -111.80),
    "Ohio River":       (38.50, -85.00),
    "Rio Grande":       (31.00, -104.50),
    "Columbia River":   (46.00, -121.00),
    "Hudson River":     (42.00, -73.80),
    "Potomac River":    (38.90, -77.05),

    # ── Mountains ──
    "Rocky Mountains":  (40.00, -105.50),
    "Appalachian Mountains": (37.00, -80.00),
    "Sierra Nevada":    (37.50, -119.50),
    "Cascade Range":    (46.00, -121.50),
    "Mount Rushmore":   (43.88, -103.46),
    "Grand Canyon":     (36.10, -112.11),

    # ── National Monuments & Landmarks ──
    "Statue of Liberty": (40.69, -74.04),
    "Golden Gate Bridge": (37.82, -122.48),
    "White House":      (38.90, -77.04),
    "Capitol Building": (38.89, -77.01),
    "Lincoln Memorial": (38.89, -77.05),
    "Mount Rushmore":   (43.88, -103.46),
    "Grand Canyon":     (36.10, -112.11),
    "Yellowstone":      (44.43, -110.59),
    "Niagara Falls":    (43.08, -79.07),
    "Kennedy Space Center": (28.57, -80.65),
    "Hollywood":        (34.09, -118.33),
    "Times Square":     (40.76, -73.99),
    "Alcatraz":         (37.83, -122.42),
    "Pearl Harbor":     (21.36, -157.95),
    "Independence Hall": (39.95, -75.15),
    "Liberty Bell":     (39.95, -75.15),
    "Gateway Arch":     (38.63, -90.19),
    "Space Needle":     (47.62, -122.35),

    # ── Great Lakes ──
    "Lake Superior":    (47.50, -88.00),
    "Lake Michigan":    (44.00, -87.00),
    "Lake Huron":       (44.80, -83.00),
    "Lake Erie":        (42.20, -81.20),
    "Lake Ontario":     (43.60, -77.50),

    # ── National Parks ──
    "Yosemite":         (37.87, -119.54),
    "Everglades":       (25.29, -80.90),
    "Glacier National Park": (48.70, -113.80),
    "Zion":             (37.30, -113.05),
    "Acadia":           (44.34, -68.21),
}


def get_location_coords(location_name: str) -> tuple[float, float] | None:
    """Look up (x%, y%) image coordinates for a location on the US map."""
    if not location_name:
        return None

    latlon = None
    if location_name in LOCATIONS:
        latlon = LOCATIONS[location_name]
    else:
        lower = location_name.lower().strip()
        for key, coords in LOCATIONS.items():
            if key.lower() == lower:
                latlon = coords
                break
        if not latlon:
            for key, coords in LOCATIONS.items():
                if lower in key.lower() or key.lower() in lower:
                    latlon = coords
                    break

    if latlon:
        return _latlon_to_us_pct(latlon[0], latlon[1])
    return None


# ── Permanent geographic features shown on the map ──
MAP_RIVERS = [
    ("Mississippi",  32.30, -90.90, "#2563eb", "〰️"),
    ("Missouri",     41.00, -96.00, "#2563eb", "〰️"),
    ("Colorado",     36.00, -111.80, "#2563eb", "〰️"),
    ("Ohio",         38.50, -85.00, "#3b82f6", "〰️"),
    ("Columbia",     46.00, -121.00, "#3b82f6", "〰️"),
    ("Rio Grande",   31.00, -104.50, "#3b82f6", "〰️"),
]

MAP_MOUNTAINS = [
    ("Rocky Mtns",    40.00, -105.50, "#92400e", "▲"),
    ("Appalachians",  37.00, -80.00, "#92400e", "▲"),
    ("Sierra Nevada", 37.50, -119.50, "#92400e", "▲"),
]

MAP_LAKES = [
    ("L. Superior", 47.50, -88.00, "#0891b2", "🌊"),
    ("L. Michigan", 44.00, -87.00, "#0891b2", "🌊"),
    ("L. Erie",     42.20, -81.20, "#0891b2", "🌊"),
]

MAP_OCEANS = [
    ("Atlantic Ocean", 33.00, -70.00, "#0891b2", "🌊"),
    ("Pacific Ocean",  37.00, -127.00, "#0891b2", "🌊"),
    ("Gulf of Mexico", 26.00, -90.00, "#0891b2", "🌊"),
]


def _render_feature_labels() -> str:
    html_parts = []

    for label, lat, lon, color, icon in MAP_RIVERS:
        x, y = _latlon_to_us_pct(lat, lon)
        html_parts.append(
            f'<div style="position:absolute;left:{x}%;top:{y}%;transform:translate(-50%,-50%);z-index:3;'
            f'font-size:0.45rem;font-weight:700;color:{color};white-space:nowrap;'
            f'text-shadow:0 0 3px white, 0 0 3px white, 0 0 3px white;'
            f'pointer-events:none;">'
            f'{icon} {label}</div>'
        )

    for label, lat, lon, color, icon in MAP_MOUNTAINS:
        x, y = _latlon_to_us_pct(lat, lon)
        html_parts.append(
            f'<div style="position:absolute;left:{x}%;top:{y}%;transform:translate(-50%,-50%);z-index:3;'
            f'font-size:0.45rem;font-weight:700;color:{color};white-space:nowrap;'
            f'text-shadow:0 0 3px white, 0 0 3px white, 0 0 3px white;'
            f'pointer-events:none;">'
            f'{icon} {label}</div>'
        )

    for label, lat, lon, color, icon in MAP_LAKES + MAP_OCEANS:
        x, y = _latlon_to_us_pct(lat, lon)
        html_parts.append(
            f'<div style="position:absolute;left:{x}%;top:{y}%;transform:translate(-50%,-50%);z-index:3;'
            f'font-size:0.45rem;font-weight:700;color:{color};white-space:nowrap;font-style:italic;'
            f'text-shadow:0 0 3px white, 0 0 3px white, 0 0 3px white;'
            f'pointer-events:none;">'
            f'{icon} {label}</div>'
        )

    return "\n".join(html_parts)


def render_map_with_marker(location_name: str, label: str = "") -> str | None:
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
    <div style="position:relative;display:inline-block;width:100%;max-width:480px;margin:0.5rem auto;border-radius:20px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.12);background:white;">
        <img src="{map_b64}" style="width:100%;display:block;border-radius:20px;" />
        {feature_labels}
        <div style="position:absolute;left:{x}%;top:{y}%;transform:translate(-50%,-50%);z-index:10;">
            <div style="
                width:16px;height:16px;
                background:#ef4444;
                border:3px solid white;
                border-radius:50%;
                box-shadow:0 0 0 3px #ef4444, 0 2px 8px rgba(0,0,0,0.3);
                animation: us-map-pulse 1.5s ease-in-out infinite;
            "></div>
        </div>
        <div style="position:absolute;left:{x}%;top:{min(y + 4, 94)}%;transform:translateX(-50%);z-index:10;
                    background:rgba(0,0,0,0.8);color:white;padding:3px 10px;border-radius:8px;
                    font-size:0.65rem;font-weight:600;white-space:nowrap;
                    box-shadow:0 2px 6px rgba(0,0,0,0.2);">
            📍 {display_label}
        </div>
    </div>
    <style>
        @keyframes us-map-pulse {{
            0%   {{ box-shadow: 0 0 0 3px #ef4444, 0 0 0 6px rgba(239,68,68,0.4); }}
            50%  {{ box-shadow: 0 0 0 5px #ef4444, 0 0 0 14px rgba(239,68,68,0.15); }}
            100% {{ box-shadow: 0 0 0 3px #ef4444, 0 0 0 6px rgba(239,68,68,0.4); }}
        }}
    </style>
    """
