"""Generate a clean world map from GeoJSON using matplotlib."""

import json
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection
import numpy as np

GEOJSON_PATH = "world_countries.geojson"
OUTPUT_DIR = "world_map"
MAP_FILE = os.path.join(OUTPUT_DIR, "world_map.png")
BOUNDS_FILE = "world_map_bounds.json"

LAND_COLOR = "#b8d4a3"
OCEAN_COLOR = "#d4e8f7"
BORDER_COLOR = "#6b8e6b"
BORDER_WIDTH = 0.3

FIG_WIDTH = 20
FIG_HEIGHT = 10


def load_geojson():
    with open(GEOJSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_polygons(feature):
    """Extract list of (xs, ys) polygon coordinate arrays from a GeoJSON feature."""
    geom = feature["geometry"]
    polys = []
    if geom["type"] == "Polygon":
        for ring in geom["coordinates"]:
            coords = np.array(ring)
            polys.append((coords[:, 0], coords[:, 1]))
    elif geom["type"] == "MultiPolygon":
        for polygon in geom["coordinates"]:
            for ring in polygon:
                coords = np.array(ring)
                polys.append((coords[:, 0], coords[:, 1]))
    return polys


def generate_world_map():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    geo = load_geojson()

    fig, ax = plt.subplots(1, 1, figsize=(FIG_WIDTH, FIG_HEIGHT))
    fig.patch.set_facecolor(OCEAN_COLOR)
    ax.set_facecolor(OCEAN_COLOR)

    patches = []
    for feature in geo["features"]:
        polys = extract_polygons(feature)
        for xs, ys in polys:
            verts = list(zip(xs, ys))
            patches.append(MplPolygon(verts, closed=True))

    pc = PatchCollection(
        patches,
        facecolor=LAND_COLOR,
        edgecolor=BORDER_COLOR,
        linewidth=BORDER_WIDTH,
    )
    ax.add_collection(pc)

    ax.set_xlim(-180, 180)
    ax.set_ylim(-90, 90)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    fig.savefig(MAP_FILE, dpi=150, bbox_inches="tight", pad_inches=0.02,
                facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Saved world map to {MAP_FILE}")

    bounds = {"min_lon": -180, "max_lon": 180, "min_lat": -90, "max_lat": 90}
    with open(BOUNDS_FILE, "w") as f:
        json.dump(bounds, f, indent=2)
    print(f"Saved bounds to {BOUNDS_FILE}")


if __name__ == "__main__":
    generate_world_map()
