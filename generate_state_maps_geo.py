"""
Generate accurate state/UT map images from GeoJSON boundaries using matplotlib.

Reads india_adarsh.geojson (real geographic boundaries) and produces:
  - One PNG per state/UT in state_maps/
  - An India-wide overview map in india_map/india_map.png
  - A JSON file with bounding boxes for coordinate conversion

Usage:
    python generate_state_maps_geo.py
"""

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon as MplPolygon
import numpy as np

GEOJSON_PATH = os.path.join(os.path.dirname(__file__), "india_adarsh.geojson")
STATE_MAPS_DIR = os.path.join(os.path.dirname(__file__), "state_maps")
INDIA_MAP_DIR = os.path.join(os.path.dirname(__file__), "india_map")
BOUNDS_PATH = os.path.join(os.path.dirname(__file__), "state_bounds.json")

# Map GeoJSON state names → file-system keys
NAME_TO_KEY = {
    "Andaman and Nicobar Islands": "andaman_nicobar",
    "Andhra Pradesh":       "andhra_pradesh",
    "Arunachal Pradesh":    "arunachal_pradesh",
    "Assam":                "assam",
    "Bihar":                "bihar",
    "Chandigarh":           "chandigarh",
    "Chhattisgarh":         "chhattisgarh",
    "Dadra and Nagar Haveli": "dadra_daman_diu",
    "Daman and Diu":        "dadra_daman_diu",
    "Delhi":                "delhi",
    "Goa":                  "goa",
    "Gujarat":              "gujarat",
    "Haryana":              "haryana",
    "Himachal Pradesh":     "himachal_pradesh",
    "Jammu and Kashmir":    "jammu_and_kashmir",
    "Jharkhand":            "jharkhand",
    "Karnataka":            "karnataka",
    "Kerala":               "kerala",
    "Ladakh":               "ladakh",
    "Lakshadweep":          "lakshadweep",
    "Madhya Pradesh":       "madhya_pradesh",
    "Maharashtra":          "maharashtra",
    "Manipur":              "manipur",
    "Meghalaya":            "meghalaya",
    "Mizoram":              "mizoram",
    "Nagaland":             "nagaland",
    "Odisha":               "odisha",
    "Puducherry":           "puducherry",
    "Punjab":               "punjab",
    "Rajasthan":            "rajasthan",
    "Sikkim":               "sikkim",
    "Tamil Nadu":           "tamil_nadu",
    "Telangana":            "telangana",
    "Tripura":              "tripura",
    "Uttar Pradesh":        "uttar_pradesh",
    "Uttarakhand":          "uttarakhand",
    "West Bengal":          "west_bengal",
}

# Soft pastel fill colors for states
STATE_COLORS = [
    "#a8d8b9", "#f7cac9", "#c5cae9", "#fff9c4", "#b2dfdb",
    "#f0e68c", "#e1bee7", "#ffccbc", "#b3e5fc", "#dcedc8",
    "#ffe0b2", "#c8e6c9", "#d1c4e9", "#ffecb3", "#b2ebf2",
    "#f8bbd0", "#aed581", "#80cbc4", "#ef9a9a", "#ce93d8",
]


def extract_polygons(geometry):
    """Extract list of (lon, lat) polygon arrays from a GeoJSON geometry."""
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
    """Get (min_lon, max_lon, min_lat, max_lat) for a list of polygons."""
    all_coords = np.vstack(polys)
    return (
        float(all_coords[:, 0].min()),
        float(all_coords[:, 0].max()),
        float(all_coords[:, 1].min()),
        float(all_coords[:, 1].max()),
    )


def plot_state(polys, out_path, fill_color="#a8d8b9", border_color="#4a7c59",
               bg_polys=None, figsize=(6, 6), pad_frac=0.08):
    """Plot a single state with optional faded background of neighbouring states."""
    min_lon, max_lon, min_lat, max_lat = get_bounds(polys)

    # Add padding
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

    # Draw faded background states (if provided)
    if bg_polys:
        for poly_arr in bg_polys:
            patch = MplPolygon(poly_arr[:, :2], closed=True,
                               facecolor="#f0f0f0", edgecolor="#d0d0d0",
                               linewidth=0.3, alpha=0.4)
            ax.add_patch(patch)

    # Draw the target state
    for poly_arr in polys:
        patch = MplPolygon(poly_arr[:, :2], closed=True,
                           facecolor=fill_color, edgecolor=border_color,
                           linewidth=1.2)
        ax.add_patch(patch)

    plt.tight_layout(pad=0)
    fig.savefig(out_path, dpi=100, bbox_inches="tight", pad_inches=0.02,
                facecolor="white", transparent=False)
    plt.close(fig)


def plot_india(all_features, out_path, figsize=(6, 8)):
    """Plot the full India map with all states colored."""
    fig, ax = plt.subplots(1, 1, figsize=figsize, dpi=100)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("white")

    for i, (name, polys) in enumerate(all_features):
        color = STATE_COLORS[i % len(STATE_COLORS)]
        for poly_arr in polys:
            patch = MplPolygon(poly_arr[:, :2], closed=True,
                               facecolor=color, edgecolor="#5a5a5a",
                               linewidth=0.5)
            ax.add_patch(patch)

    # Set bounds to India's extent
    ax.set_xlim(67, 98)
    ax.set_ylim(6, 38)

    plt.tight_layout(pad=0)
    fig.savefig(out_path, dpi=120, bbox_inches="tight", pad_inches=0.02,
                facecolor="white", transparent=False)
    plt.close(fig)


def main():
    with open(GEOJSON_PATH) as f:
        geojson = json.load(f)

    os.makedirs(STATE_MAPS_DIR, exist_ok=True)
    os.makedirs(INDIA_MAP_DIR, exist_ok=True)

    # Parse all features
    features_data = {}  # key → (display_name, polys)
    all_polys_flat = []  # for background rendering

    # Collect Dadra and Daman/Diu polygons together
    merged = {}

    for feat in geojson["features"]:
        name = feat["properties"]["st_nm"]
        polys = extract_polygons(feat["geometry"])
        key = NAME_TO_KEY.get(name)

        if not key:
            print(f"  WARNING: No key mapping for '{name}', skipping")
            continue

        if key in merged:
            merged[key]["polys"].extend(polys)
        else:
            merged[key] = {"name": name, "polys": polys}

        all_polys_flat.extend(polys)

    # Build bounds dict for coordinate conversion
    bounds_data = {}

    print(f"Generating maps for {len(merged)} states/UTs...\n")

    for i, (key, data) in enumerate(sorted(merged.items())):
        name = data["name"]
        polys = data["polys"]
        out_path = os.path.join(STATE_MAPS_DIR, f"{key}.png")
        color = STATE_COLORS[i % len(STATE_COLORS)]

        # Get neighbouring context polygons (all other states)
        bg = [p for p in all_polys_flat if not any(np.array_equal(p, sp) for sp in polys)]

        print(f"  [{i+1}/{len(merged)}] {name} ({key}): generating...")
        plot_state(polys, out_path, fill_color=color, bg_polys=bg)

        # Store bounds
        min_lon, max_lon, min_lat, max_lat = get_bounds(polys)
        bounds_data[key] = {
            "name": name,
            "min_lon": min_lon, "max_lon": max_lon,
            "min_lat": min_lat, "max_lat": max_lat,
        }

    # Generate India overview map
    india_path = os.path.join(INDIA_MAP_DIR, "india_map.png")
    print(f"\n  Generating India overview map...")
    all_features = [(d["name"], d["polys"]) for d in merged.values()]
    plot_india(all_features, india_path)

    # Save bounds for coordinate conversion
    with open(BOUNDS_PATH, "w") as f:
        json.dump(bounds_data, f, indent=2)

    print(f"\nDone! Generated {len(merged)} state maps + 1 India map")
    print(f"Bounds saved to {BOUNDS_PATH}")


if __name__ == "__main__":
    main()
