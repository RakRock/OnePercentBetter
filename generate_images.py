"""
Generate AI cartoon illustrations for story pages using
the free Hugging Face Inference API (FLUX.1-schnell model).

Can be used two ways:
  1. CLI — run ``python generate_images.py`` to generate images for ALL stories.
  2. Library — import ``generate_images_for_story()`` to generate images for a
     single story (used by the in-app story generator).

Prerequisites:
  1. Create a free HF account at https://huggingface.co/join
  2. Create an access token at https://huggingface.co/settings/tokens
     (enable "Make calls to Inference Providers")
  3. Export it:  export HF_TOKEN="hf_..."
"""

import os
import sys
import time

from huggingface_hub import InferenceClient

import reading_content as rc

# ── Configuration ──
OUT_DIR = os.path.join(os.path.dirname(__file__), "images")
MODEL = "black-forest-labs/FLUX.1-schnell"
WIDTH = 512
HEIGHT = 384
DELAY_SECONDS = 1

STYLE_SUFFIX = (
    ", children's picture book illustration, cute simple cartoon,"
    " soft pastel colors, white background, no text, no words"
)


def generate_images_for_story(story, hf_token, progress_callback=None):
    """Generate illustrations for every page in a single story.

    Args:
        story: A story dict with ``id`` and ``pages`` (each page must have
               an ``image_prompt`` field).
        hf_token: HuggingFace API token string.
        progress_callback: Optional callable ``(page_num, total, status_msg)``
                           invoked after each page is processed.  Useful for
                           updating a Streamlit progress indicator.

    Returns:
        tuple ``(generated, skipped, failed)`` counts.
    """
    os.makedirs(OUT_DIR, exist_ok=True)
    client = InferenceClient(provider="auto", api_key=hf_token)

    story_id = story["id"]
    pages = story["pages"]
    total = len(pages)
    generated = skipped = failed = 0

    for i, page in enumerate(pages, start=1):
        out_path = os.path.join(OUT_DIR, f"{story_id}_{i}.png")

        if os.path.exists(out_path):
            skipped += 1
            if progress_callback:
                progress_callback(i, total, f"Page {i}/{total}: already exists")
            continue

        prompt = page["image_prompt"] + STYLE_SUFFIX
        if progress_callback:
            progress_callback(i, total, f"Drawing page {i}/{total}...")

        try:
            image = client.text_to_image(
                prompt,
                model=MODEL,
                width=WIDTH,
                height=HEIGHT,
            )
            image.save(out_path)
            generated += 1
        except Exception as exc:
            failed += 1
            if progress_callback:
                progress_callback(i, total, f"Page {i} failed: {exc}")

        time.sleep(DELAY_SECONDS)

    return generated, skipped, failed


# ── CLI entry point ──
def main():
    token = os.environ.get("HF_TOKEN")
    if not token:
        print("ERROR: HF_TOKEN environment variable is not set.")
        print("  1. Get a free token at https://huggingface.co/settings/tokens")
        print('  2. Run:  export HF_TOKEN="hf_..."')
        sys.exit(1)

    stories = rc.get_all_stories()
    total_images = sum(len(s["pages"]) for s in stories)
    grand_generated = grand_skipped = grand_failed = 0

    print(f"Generating {total_images} images using model: {MODEL}\n")

    for story in stories:
        title = story["title"]
        sid = story["id"]
        print(f"── {title} ({sid}) ──")

        def _cli_progress(page, total, msg):
            print(f"  {msg}")

        gen, skip, fail = generate_images_for_story(story, token, _cli_progress)
        grand_generated += gen
        grand_skipped += skip
        grand_failed += fail
        print()

    print(
        f"Done!  Generated: {grand_generated}  "
        f"Skipped: {grand_skipped}  "
        f"Failed: {grand_failed}  "
        f"Total: {total_images}"
    )


if __name__ == "__main__":
    main()
