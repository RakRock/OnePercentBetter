"""
World map rendering for Arjun's Map Explorer.

Uses the world map image generated from GeoJSON boundaries (matplotlib).
Locations use real latitude/longitude coordinates converted to image
percentages at render time using the map's bounding box.
"""

import base64
import os

_MAP_PATH = os.path.join(os.path.dirname(__file__), "world_map", "world_map.png")
_MAP_B64: str | None = None

_LON_MIN = -180
_LON_MAX = 180
_LAT_MIN = -90
_LAT_MAX = 90


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


def _latlon_to_pct(lat: float, lon: float) -> tuple[float, float]:
    """Convert lat/lon to (x%, y%) on the world map image."""
    x_pct = ((lon - _LON_MIN) / (_LON_MAX - _LON_MIN)) * 100
    y_pct = ((_LAT_MAX - lat) / (_LAT_MAX - _LAT_MIN)) * 100
    x_pct = max(1, min(99, x_pct))
    y_pct = max(1, min(99, y_pct))
    return (round(x_pct, 1), round(y_pct, 1))


def render_map_with_marker(lat: float, lon: float, label: str = "") -> str | None:
    """Return HTML for the world map with a pulsing marker at the given lat/lon.

    Returns None if the map image doesn't exist.
    """
    map_b64 = _get_map_b64()
    if not map_b64:
        return None

    x, y = _latlon_to_pct(lat, lon)
    display_label = label or f"{lat:.1f}, {lon:.1f}"

    return (
        '<div style="position:relative;display:inline-block;width:100%;max-width:700px;'
        'margin:0.5rem auto;border-radius:16px;overflow:hidden;'
        'box-shadow:0 4px 20px rgba(0,0,0,0.12);background:white;">'
        f'<img src="{map_b64}" style="width:100%;display:block;border-radius:16px;" />'
        f'<div style="position:absolute;left:{x}%;top:{y}%;'
        'transform:translate(-50%,-50%);z-index:10;">'
        '<div style="width:16px;height:16px;background:#ef4444;'
        'border:3px solid white;border-radius:50%;'
        'box-shadow:0 0 0 3px #ef4444,0 2px 8px rgba(0,0,0,0.3);'
        'animation:world-pulse 1.5s ease-in-out infinite;"></div></div>'
        f'<div style="position:absolute;left:{x}%;top:{min(y + 3.5, 95)}%;'
        'transform:translateX(-50%);z-index:10;'
        'background:rgba(0,0,0,0.8);color:white;padding:3px 10px;border-radius:8px;'
        'font-size:0.75rem;font-weight:600;white-space:nowrap;'
        f'box-shadow:0 2px 6px rgba(0,0,0,0.2);">📍 {display_label}</div>'
        '</div>'
        '<style>'
        '@keyframes world-pulse{'
        '0%{box-shadow:0 0 0 3px #ef4444,0 0 0 6px rgba(239,68,68,0.4)}'
        '50%{box-shadow:0 0 0 5px #ef4444,0 0 0 14px rgba(239,68,68,0.15)}'
        '100%{box-shadow:0 0 0 3px #ef4444,0 0 0 6px rgba(239,68,68,0.4)}}'
        '</style>'
    )
