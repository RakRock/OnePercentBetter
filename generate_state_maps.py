"""
Generate clean outline map images for Indian states using
the Hugging Face Inference API (FLUX.1-schnell model).

Each state gets a simple, clean map with state boundaries visible,
no text labels, used for Sangeetha's GK app to show locations within a state.

Usage:
    export HF_TOKEN="hf_..."
    python generate_state_maps.py
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
    "clear state outline shape, light district boundaries, "
    "ABSOLUTELY NO TEXT, NO LABELS, NO WRITING, NO LETTERS, NO WORDS, "
    "no city names, no annotations, clean minimalist cartographic style, "
    "white background outside the state boundary, "
    "soft green and beige tones inside, high quality illustration"
)

# Each entry: (state_name, prompt describing the state map)
STATES = [
    ("karnataka", "outline map of Karnataka state India, showing districts"),
    ("tamil_nadu", "outline map of Tamil Nadu state India, showing districts"),
    ("kerala", "outline map of Kerala state India, narrow long shape"),
    ("andhra_pradesh", "outline map of Andhra Pradesh state India, showing districts"),
    ("telangana", "outline map of Telangana state India, showing districts"),
    ("maharashtra", "outline map of Maharashtra state India, large western state"),
    ("rajasthan", "outline map of Rajasthan state India, large desert state"),
    ("gujarat", "outline map of Gujarat state India, western coast"),
    ("uttar_pradesh", "outline map of Uttar Pradesh state India, large northern state"),
    ("madhya_pradesh", "outline map of Madhya Pradesh state India, central India"),
    ("west_bengal", "outline map of West Bengal state India, eastern state"),
    ("odisha", "outline map of Odisha state India, eastern coast"),
    ("bihar", "outline map of Bihar state India, eastern state"),
    ("punjab", "outline map of Punjab state India, northern state"),
    ("goa", "outline map of Goa state India, small coastal state"),
    ("jharkhand", "outline map of Jharkhand state India"),
    ("chhattisgarh", "outline map of Chhattisgarh state India, central state"),
    ("uttarakhand", "outline map of Uttarakhand state India, himalayan state"),
    ("himachal_pradesh", "outline map of Himachal Pradesh state India, hill state"),
    ("jammu_and_kashmir", "outline map of Jammu and Kashmir India, northern state"),
    ("assam", "outline map of Assam state India, northeast state"),
    ("haryana", "outline map of Haryana state India, northern state"),
]


def main():
    token = os.environ.get("HF_TOKEN")
    if not token:
        print("ERROR: HF_TOKEN environment variable is not set.")
        print("  1. Get a free token at https://huggingface.co/settings/tokens")
        print('  2. Run:  export HF_TOKEN="hf_..."')
        sys.exit(1)

    os.makedirs(OUT_DIR, exist_ok=True)
    client = InferenceClient(provider="auto", api_key=token)

    total = len(STATES)
    generated = skipped = failed = 0

    print(f"Generating {total} state map images using model: {MODEL}\n")

    for i, (name, prompt) in enumerate(STATES, start=1):
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
