"""
Generate maps for the remaining 7 states + 7 union territories.
"""

import os
import sys
import time

from huggingface_hub import InferenceClient

OUT_DIR = os.path.join(os.path.dirname(__file__), "state_maps")
MODEL = "black-forest-labs/FLUX.1-schnell"
WIDTH = 512
HEIGHT = 512
DELAY_SECONDS = 2

STYLE_SUFFIX = (
    ", clean simple illustrated map, soft pastel colors, "
    "clear outline shape, light district boundaries, "
    "ABSOLUTELY NO TEXT, NO LABELS, NO WRITING, NO LETTERS, NO WORDS, "
    "no city names, no annotations, clean minimalist cartographic style, "
    "white background outside the boundary, "
    "soft green and beige tones inside, high quality illustration"
)

REGIONS = [
    # Missing 7 states (all NE India)
    ("arunachal_pradesh", "outline map of Arunachal Pradesh state India, northeast mountainous state"),
    ("manipur", "outline map of Manipur state India, small northeast state oval shape"),
    ("meghalaya", "outline map of Meghalaya state India, northeast state plateau"),
    ("mizoram", "outline map of Mizoram state India, small narrow northeast state"),
    ("nagaland", "outline map of Nagaland state India, small northeast hill state"),
    ("sikkim", "outline map of Sikkim state India, tiny northeast himalayan state"),
    ("tripura", "outline map of Tripura state India, small northeast state"),

    # 7 Union Territories (J&K already generated)
    ("andaman_nicobar", "outline map of Andaman and Nicobar Islands India, chain of islands in Bay of Bengal"),
    ("chandigarh", "outline map of Chandigarh union territory India, small planned city"),
    ("dadra_daman_diu", "outline map of Dadra and Nagar Haveli and Daman and Diu India, western coast"),
    ("delhi", "outline map of Delhi NCT India, national capital territory"),
    ("ladakh", "outline map of Ladakh union territory India, high altitude mountainous region"),
    ("lakshadweep", "outline map of Lakshadweep Islands India, small coral islands in Arabian Sea"),
    ("puducherry", "outline map of Puducherry union territory India, small coastal territory"),
]


def main():
    token = os.environ.get("HF_TOKEN")
    if not token:
        print("ERROR: HF_TOKEN environment variable is not set.")
        sys.exit(1)

    os.makedirs(OUT_DIR, exist_ok=True)
    client = InferenceClient(provider="auto", api_key=token)

    total = len(REGIONS)
    generated = skipped = failed = 0

    print(f"Generating {total} remaining map images using model: {MODEL}\n")

    for i, (name, prompt) in enumerate(REGIONS, start=1):
        out_path = os.path.join(OUT_DIR, f"{name}.png")

        if os.path.exists(out_path):
            print(f"  [{i}/{total}] {name}: already exists, skipping")
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
            print(f"  [{i}/{total}] {name}: saved!")
        except Exception as exc:
            failed += 1
            print(f"  [{i}/{total}] {name}: FAILED - {exc}")

        time.sleep(DELAY_SECONDS)

    print(f"\nDone!  Generated: {generated}  Skipped: {skipped}  Failed: {failed}")


if __name__ == "__main__":
    main()
