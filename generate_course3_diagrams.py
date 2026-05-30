"""
Generate math diagrams for Arjun Course 3 lesson notes (Unit 2)
using the Hugging Face Inference API (FLUX.1-schnell).

Usage:
    export HF_TOKEN="hf_..."
    python generate_course3_diagrams.py              # all unit 2 (skip existing)
    python generate_course3_diagrams.py --activity 9 --force   # Activity 9 only, overwrite
"""

from __future__ import annotations

import argparse
import os
import sys
import time

try:
    import truststore

    truststore.inject_into_ssl()
except ImportError:
    pass

from huggingface_hub import InferenceClient

OUT_DIR = os.path.join(os.path.dirname(__file__), "ArjunCourse3", "images", "unit_2")
MODEL = "black-forest-labs/FLUX.1-schnell"
WIDTH = 768
HEIGHT = 512
DELAY_SECONDS = 2.0

STYLE_SUFFIX = (
    ", crisp educational math infographic, clean vector-like illustration,"
    " white background, bold colors, large clear shapes, middle school textbook,"
    " labeled diagrams, easy to read, no blurry text, no photorealistic people"
)

# Activity 9 — enhanced pattern diagrams (student-friendly, not vague dots)
ACTIVITY_9_DIAGRAMS = [
    (
        "activity_9_constant_difference.png",
        "Educational math poster with three panels labeled Figure 1 Figure 2 Figure 3. "
        "Each panel shows a neat vertical column of blue circular tiles on a grid: "
        "Figure 1 has 2 tiles, Figure 2 has 5 tiles, Figure 3 has 8 tiles. "
        "Green arrows between panels labeled plus 3. Title: Constant Difference Pattern. "
        "Formula box: first term plus difference times n minus 1. Very clear layout.",
    ),
    (
        "activity_9_square_numbers.png",
        "Educational diagram showing square number patterns in three panels labeled n=1 n=2 n=3. "
        "n=1 is a single orange square tile, n=2 is a 2 by 2 grid of four orange squares, "
        "n=3 is a 3 by 3 grid of nine orange squares. Caption: Square Numbers expression n squared. "
        "Clean grid lines, white background, bright colors.",
    ),
    (
        "activity_9_rectangular_numbers.png",
        "Educational diagram of rectangular number patterns, three panels. "
        "Panel 1: 1 row 2 columns of purple tiles (2 tiles). "
        "Panel 2: 2 rows 3 columns grid (6 tiles). Panel 3: 3 rows 4 columns grid (12 tiles). "
        "Labels n times n plus 1. Clear rectangular grids, math textbook style.",
    ),
    (
        "activity_9_triangular_numbers.png",
        "Educational diagram of triangular numbers in three steps. "
        "Step 1: one green dot. Step 2: triangle of 3 dots in rows 1 and 2. "
        "Step 3: triangle of 6 dots in rows 1 2 3. Step 4 small panel: 10 dots. "
        "Label: Triangular Numbers n times n plus 1 divided by 2. Stacked row pattern, very clear.",
    ),
    (
        "activity_9_table_to_expression.png",
        "Educational infographic: left side a table with columns Step n and Tiles, "
        "rows showing n=1 tiles 4, n=2 tiles 9, n=3 tiles 14, n=4 tiles 19. "
        "Right side shows arrows: constant difference 5 highlighted. "
        "Large formula: 4 plus 5 times n minus 1. Middle school algebra lesson chart, clean design.",
    ),
]

UNIT_2_DIAGRAMS = [
    *ACTIVITY_9_DIAGRAMS,
    (
        "activity_10_balance.png",
        "balance scale diagram solving equation 3x plus 4 equals 16, "
        "equal weights on both sides, simple algebra illustration for students",
    ),
    (
        "activity_11_rise_run.png",
        "coordinate plane showing slope as rise over run, two points connected "
        "by line, vertical arrow labeled rise, horizontal arrow labeled run, grid",
    ),
    (
        "activity_12_y_mx_b.png",
        "graph of linear equation y equals mx plus b, line crossing y-axis at point b, "
        "slope triangle showing rise 2 run 1, labeled m and b, coordinate axes",
    ),
    (
        "activity_13_proportional.png",
        "two graphs comparison proportional line through origin versus "
        "nonproportional line with y-intercept, simple labeled math diagram",
    ),
    (
        "activity_14_intersection.png",
        "coordinate plane with two intersecting straight lines, "
        "point of intersection circled and labeled solution x y, system of equations",
    ),
    (
        "activity_15_systems.png",
        "educational diagram showing solving system of equations by substitution "
        "and elimination, two methods side by side, simple flow arrows, algebra",
    ),
]


def diagrams_for_activity(activity_num: int | None) -> list[tuple[str, str]]:
    if activity_num == 9:
        return ACTIVITY_9_DIAGRAMS
    if activity_num is not None:
        prefix = f"activity_{activity_num}_"
        return [(n, p) for n, p in UNIT_2_DIAGRAMS if n.startswith(prefix)]
    return UNIT_2_DIAGRAMS


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit", type=int, default=2)
    parser.add_argument("--activity", type=int, default=None, help="Only this activity (e.g. 9)")
    parser.add_argument("--force", action="store_true", help="Overwrite existing images")
    args = parser.parse_args()
    if args.unit != 2:
        print("Only unit 2 diagrams are defined so far.")
        sys.exit(1)

    token = os.environ.get("HF_TOKEN")
    if not token:
        print("ERROR: HF_TOKEN environment variable is not set.")
        print('  export HF_TOKEN="hf_..."')
        sys.exit(1)

    os.makedirs(OUT_DIR, exist_ok=True)
    client = InferenceClient(provider="auto", api_key=token)
    diagrams = diagrams_for_activity(args.activity)
    total = len(diagrams)
    generated = skipped = failed = 0

    label = f"activity {args.activity}" if args.activity else f"unit {args.unit}"
    print(f"Generating {total} Course 3 diagrams ({label}, {MODEL}, {WIDTH}x{HEIGHT})\n")

    for i, (name, prompt) in enumerate(diagrams, start=1):
        out_path = os.path.join(OUT_DIR, name)
        if os.path.exists(out_path) and not args.force:
            print(f"  [{i}/{total}] {name}: skip (exists, use --force to replace)")
            skipped += 1
            continue
        full_prompt = prompt + STYLE_SUFFIX
        print(f"  [{i}/{total}] {name}: generating...")
        try:
            image = client.text_to_image(
                full_prompt,
                model=MODEL,
                width=WIDTH,
                height=HEIGHT,
            )
            image.save(out_path)
            generated += 1
            print(f"  [{i}/{total}] {name}: saved")
        except Exception as exc:
            failed += 1
            print(f"  [{i}/{total}] {name}: FAILED — {exc}")
        time.sleep(DELAY_SECONDS)

    print(f"\nDone. Generated: {generated}  Skipped: {skipped}  Failed: {failed}")
    print(f"Output: {OUT_DIR}/")


if __name__ == "__main__":
    main()
