#!/usr/bin/env python3
"""
Optional: pre-generate everyday illustrations for Harshit Physics Unit 1 via Hugging Face.

These supplement the labeled SVG diagrams — they do NOT replace ray/mirror diagrams
(AI images often get angles and labels wrong).

Usage:
    export HF_TOKEN="hf_..."   # already in ~/.zshrc for local dev
    python generate_physics_unit1_diagrams.py              # Release 1 only, skip existing
    python generate_physics_unit1_diagrams.py --day 1       # one day
    python generate_physics_unit1_diagrams.py --force      # overwrite all
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

try:
    import truststore

    truststore.inject_into_ssl()
except ImportError:
    pass

from huggingface_hub import InferenceClient

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "HarshitPhysics" / "unit1" / "logic_schema.json"
OUT_DIR = ROOT / "HarshitPhysics" / "unit1" / "diagrams"
MODEL = "black-forest-labs/FLUX.1-schnell"
WIDTH = 768
HEIGHT = 512
DELAY_SECONDS = 2.0

STYLE = (
    ", clean NCERT Class 10 physics textbook illustration, white background, "
    "simple labeled educational diagram, bright friendly colors, no photorealistic faces, "
    "large readable labels, middle school science poster, accurate everyday objects only, "
    "no complex equations, no incorrect ray angles"
)


def _prompt_for_concept(concept: dict) -> str:
    name = concept.get("name", "")
    simple = concept.get("simple_answer", "")
    example = concept.get("example", "")
    return (
        f"Educational physics diagram for Indian Class 10 students: {name}. "
        f"{simple} Example: {example}. "
        f"Show clear labels for each part. Focus on helping a student visualize the idea."
        f"{STYLE}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--day", type=int, default=0, help="Only this day (1–4 for Release 1)")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    token = os.environ.get("HF_TOKEN")
    if not token:
        print("ERROR: Set HF_TOKEN (see ~/.zshrc or .streamlit/secrets.toml)")
        sys.exit(1)

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    client = InferenceClient(provider="auto", api_key=token)

    tasks: list[tuple[str, str, dict]] = []
    for day in schema.get("days", []):
        if not day.get("active"):
            continue
        if args.day and day["day"] != args.day:
            continue
        for concept in day.get("concepts") or []:
            if concept.get("stub"):
                continue
            cid = concept["id"]
            out = OUT_DIR / f"{cid}.png"
            if out.exists() and not args.force:
                print(f"skip {cid} (exists)")
                continue
            tasks.append((cid, str(out), concept))

    if not tasks:
        print("Nothing to generate.")
        return

    print(f"Generating {len(tasks)} illustration(s) → {OUT_DIR}")
    for i, (cid, out_path, concept) in enumerate(tasks, 1):
        prompt = _prompt_for_concept(concept)
        print(f"[{i}/{len(tasks)}] {cid} — {concept.get('name', '')}")
        try:
            image = client.text_to_image(prompt, model=MODEL, width=WIDTH, height=HEIGHT)
            with open(out_path, "wb") as f:
                f.write(image)
            print(f"  saved {out_path}")
        except Exception as exc:
            print(f"  FAILED: {exc}")
        if i < len(tasks):
            time.sleep(DELAY_SECONDS)


if __name__ == "__main__":
    main()
