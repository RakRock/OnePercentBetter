"""
Generate cute cartoon object images for Krish's Math App using
the Hugging Face Inference API (FLUX.1-schnell model).

Each object gets a single adorable cartoon illustration on a white background,
used to build visual counting, addition, and subtraction problems.

Usage:
    export HF_TOKEN="hf_..."
    python generate_math_images.py
"""

import os
import sys
import time

from huggingface_hub import InferenceClient

OUT_DIR = os.path.join(os.path.dirname(__file__), "math_images")
MODEL = "black-forest-labs/FLUX.1-schnell"
WIDTH = 256
HEIGHT = 256
DELAY_SECONDS = 1

STYLE_SUFFIX = (
    ", single object centered, cute kawaii cartoon style,"
    " soft pastel colors, clean white background, no text, no words,"
    " simple flat illustration, adorable, child-friendly, round shapes"
)

# Each entry: (filename, prompt describing the object)
OBJECTS = [
    ("apple", "a single red apple with a cute smiling face"),
    ("banana", "a single yellow banana with a cute smiling face"),
    ("cookie", "a single chocolate chip cookie with a cute smiling face"),
    ("strawberry", "a single red strawberry with a cute smiling face"),
    ("orange", "a single orange fruit with a cute smiling face"),
    ("star", "a single golden star with a cute smiling face"),
    ("cat", "a single cute small orange tabby kitten sitting"),
    ("dog", "a single cute small brown puppy sitting"),
    ("frog", "a single cute small green frog"),
    ("butterfly", "a single cute colorful butterfly with big wings"),
    ("bunny", "a single cute small white bunny rabbit"),
    ("flower", "a single cute pink flower with a smiling face"),
    ("car", "a single cute small red toy car"),
    ("cupcake", "a single cute cupcake with pink frosting"),
    ("fish", "a single cute small orange goldfish"),
    ("balloon", "a single cute red balloon with a string"),
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

    total = len(OBJECTS)
    generated = skipped = failed = 0

    print(f"Generating {total} math object images using model: {MODEL}\n")

    for i, (name, prompt) in enumerate(OBJECTS, start=1):
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
