"""
Generate accurate US state map images from GeoJSON boundaries using matplotlib.

Reads us_states.geojson and produces:
  - One PNG per state in us_state_maps/
  - A US overview map in us_map/us_map.png
  - A JSON file with bounding boxes for coordinate conversion
"""

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
import numpy as np

GEOJSON_PATH = os.path.join(os.path.dirname(__file__), "us_states.geojson")
STATE_MAPS_DIR = os.path.join(os.path.dirname(__file__), "us_state_maps")
US_MAP_DIR = os.path.join(os.path.dirname(__file__), "us_map")
BOUNDS_PATH = os.path.join(os.path.dirname(__file__), "us_state_bounds.json")

# Map state names → file-system keys
NAME_TO_KEY = {
    "Alabama": "alabama", "Alaska": "alaska", "Arizona": "arizona",
    "Arkansas": "arkansas", "California": "california", "Colorado": "colorado",
    "Connecticut": "connecticut", "Delaware": "delaware",
    "District of Columbia": "district_of_columbia",
    "Florida": "florida", "Georgia": "georgia", "Hawaii": "hawaii",
    "Idaho": "idaho", "Illinois": "illinois", "Indiana": "indiana",
    "Iowa": "iowa", "Kansas": "kansas", "Kentucky": "kentucky",
    "Louisiana": "louisiana", "Maine": "maine", "Maryland": "maryland",
    "Massachusetts": "massachusetts", "Michigan": "michigan",
    "Minnesota": "minnesota", "Mississippi": "mississippi",
    "Missouri": "missouri", "Montana": "montana", "Nebraska": "nebraska",
    "Nevada": "nevada", "New Hampshire": "new_hampshire",
    "New Jersey": "new_jersey", "New Mexico": "new_mexico",
    "New York": "new_york", "North Carolina": "north_carolina",
    "North Dakota": "north_dakota", "Ohio": "ohio", "Oklahoma": "oklahoma",
    "Oregon": "oregon", "Pennsylvania": "pennsylvania",
    "Puerto Rico": "puerto_rico",
    "Rhode Island": "rhode_island", "South Carolina": "south_carolina",
    "South Dakota": "south_dakota", "Tennessee": "tennessee",
    "Texas": "texas", "Utah": "utah", "Vermont": "vermont",
    "Virginia": "virginia", "Washington": "washington",
    "West Virginia": "west_virginia", "Wisconsin": "wisconsin",
    "Wyoming": "wyoming",
}

STATE_COLORS = [
    "#a8d8b9", "#f7cac9", "#c5cae9", "#fff9c4", "#b2dfdb",
    "#f0e68c", "#e1bee7", "#ffccbc", "#b3e5fc", "#dcedc8",
    "#ffe0b2", "#c8e6c9", "#d1c4e9", "#ffecb3", "#b2ebf2",
    "#f8bbd0", "#aed581", "#80cbc4", "#ef9a9a", "#ce93d8",
]


def extract_polygons(geometry):
    polys = []
    if geometry["type"] == "Polygon":
        for ring in geometry["coordinates"]:
            polys.append(np.array(ring))
    elif geometry["type"] == "MultiPolygon":
        for polygon in geometry["coordinates"]:
            for ring in polygon:
                polys.append(np.array(ring))
    return polys


def get_bounds(polys):
    all_coords = np.vstack(polys)
    return (
        float(all_coords[:, 0].min()),
        float(all_coords[:, 0].max()),
        float(all_coords[:, 1].min()),
        float(all_coords[:, 1].max()),
    )


def plot_state(polys, out_path, fill_color="#a8d8b9", border_color="#4a7c59",
               bg_polys=None, figsize=(6, 6), pad_frac=0.08):
    min_lon, max_lon, min_lat, max_lat = get_bounds(polys)
    lon_range = max_lon - min_lon or 1
    lat_range = max_lat - min_lat or 1
    pad_lon = lon_range * pad_frac
    pad_lat = lat_range * pad_frac

    fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=100)
    ax.set_xlim(min_lon - pad_lon, max_lon + pad_lon)
    ax.set_ylim(min_lat - pad_lat, max_lat + pad_lat)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("white")

    if bg_polys:
        for poly_arr in bg_polys:
            patch = MplPolygon(poly_arr[:, :2], closed=True,
                               facecolor="#f0f0f0", edgecolor="#d0d0d0",
                               linewidth=0.3, alpha=0.4)
            ax.add_patch(patch)

    for poly_arr in polys:
        patch = MplPolygon(poly_arr[:, :2], closed=True,
                           facecolor=fill_color, edgecolor=border_color,
                           linewidth=1.2)
        ax.add_patch(patch)

    plt.tight_layout(pad=0)
    fig.savefig(out_path, dpi=100, bbox_inches="tight", pad_inches=0.02,
                facecolor="white", transparent=False)
    plt.close(fig)


def plot_us(all_features, out_path, figsize=(10, 6)):
    """Plot the full US map (contiguous 48 only for the overview)."""
    fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=120)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("white")

    for i, (name, polys) in enumerate(all_features):
        color = STATE_COLORS[i % len(STATE_COLORS)]
        for poly_arr in polys:
            patch = MplPolygon(poly_arr[:, :2], closed=True,
                               facecolor=color, edgecolor="#5a5a5a",
                               linewidth=0.4)
            ax.add_patch(patch)

    # Contiguous US bounds (exclude Alaska/Hawaii for overview)
    ax.set_xlim(-125, -66)
    ax.set_ylim(24, 50)

    plt.tight_layout(pad=0)
    fig.savefig(out_path, dpi=120, bbox_inches="tight", pad_inches=0.02,
                facecolor="white", transparent=False)
    plt.close(fig)


def main():
    with open(GEOJSON_PATH) as f:
        geojson = json.load(f)

    os.makedirs(STATE_MAPS_DIR, exist_ok=True)
    os.makedirs(US_MAP_DIR, exist_ok=True)

    features_data = {}
    all_polys_flat = []

    for feat in geojson["features"]:
        name = feat["properties"]["name"]
        polys = extract_polygons(feat["geometry"])
        key = NAME_TO_KEY.get(name)
        if not key:
            print(f"  WARNING: No key for '{name}', skipping")
            continue
        features_data[key] = {"name": name, "polys": polys}
        all_polys_flat.extend(polys)

    bounds_data = {}
    total = len(features_data)
    print(f"Generating maps for {total} US states/territories...\n")

    # Filter contiguous-only background polys (exclude Alaska/Hawaii for bg context)
    contiguous_polys = []
    for k, d in features_data.items():
        if k not in ("alaska", "hawaii", "puerto_rico"):
            contiguous_polys.extend(d["polys"])

    for i, (key, data) in enumerate(sorted(features_data.items())):
        name = data["name"]
        polys = data["polys"]
        out_path = os.path.join(STATE_MAPS_DIR, f"{key}.png")
        color = STATE_COLORS[i % len(STATE_COLORS)]

        # Use contiguous states as background for contiguous states
        if key in ("alaska", "hawaii", "puerto_rico"):
            bg = []
        else:
            bg = [p for p in contiguous_polys if not any(np.array_equal(p, sp) for sp in polys)]

        print(f"  [{i+1}/{total}] {name} ({key}): generating...")
        plot_state(polys, out_path, fill_color=color, bg_polys=bg)

        min_lon, max_lon, min_lat, max_lat = get_bounds(polys)
        bounds_data[key] = {
            "name": name,
            "min_lon": min_lon, "max_lon": max_lon,
            "min_lat": min_lat, "max_lat": max_lat,
        }

    # US overview (contiguous only)
    us_path = os.path.join(US_MAP_DIR, "us_map.png")
    print(f"\n  Generating US overview map...")
    contiguous_features = [(d["name"], d["polys"]) for k, d in features_data.items()
                           if k not in ("alaska", "hawaii", "puerto_rico")]
    plot_us(contiguous_features, us_path)

    with open(BOUNDS_PATH, "w") as f:
        json.dump(bounds_data, f, indent=2)

    print(f"\nDone! Generated {total} state maps + 1 US overview map")
    print(f"Bounds saved to {BOUNDS_PATH}")


if __name__ == "__main__":
    main()
