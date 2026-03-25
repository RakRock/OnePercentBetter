"""
Download real brand logos from Simple Icons (jsDelivr CDN)
and convert them to colored PNGs for the Logo Identifier quiz.

Simple Icons provides 3400+ real SVG brand icons — free and open source.

Usage:
    python download_brand_logos.py
"""

import os
import re
import sys
import time
import urllib.request

try:
    import truststore
    truststore.inject_into_ssl()
except ImportError:
    pass

import cairosvg

OUT_DIR = os.path.join(os.path.dirname(__file__), "brand_logos")
CDN_BASE = "https://cdn.jsdelivr.net/npm/simple-icons@latest/icons"
PNG_SIZE = 1024
DELAY = 0.3

# (filename, simple-icons slug, hex brand color, optional bg color)
# Colors chosen to be clearly visible on a white card background.
BRANDS = [
    # TECH & APPS
    ("apple", "apple", "000000", None),
    ("instagram", "instagram", "E4405F", None),
    ("spotify", "spotify", "1DB954", None),
    ("snapchat", "snapchat", "FFFC00", "F5F5F5"),
    ("youtube", "youtube", "FF0000", None),
    ("tiktok", "tiktok", "000000", None),
    ("discord", "discord", "5865F2", None),
    ("google", "google", "4285F4", None),
    ("amazon", "amazon", "FF9900", None),
    ("microsoft", "microsoft", "5E5E5E", None),
    ("whatsapp", "whatsapp", "25D366", None),
    ("duolingo", "duolingo", "58CC02", None),

    # FOOD & DRINKS
    ("mcdonalds", "mcdonalds", "FBC817", None),
    ("starbucks", "starbucks", "006241", None),
    ("pepsi", "pepsi", "004B93", None),
    ("kfc", "kfc", "F40027", None),
    ("dominos", "dominos", "006491", None),
    ("tacobell", "tacobell", "702082", None),
    ("chickfila", "chickfila", "E51636", None),
    ("redbull", "redbull", "DB0A40", None),
    ("pringles", "pringles", "007B00", None),

    # SPORTS & OUTDOORS
    ("nike", "nike", "111111", None),
    ("adidas", "adidas", "000000", None),
    ("puma", "puma", "000000", None),
    ("jordan", "jordan", "000000", None),
    ("under_armour", "underarmour", "1D1D1D", None),
    ("north_face", "thenorthface", "000000", None),
    ("premierleague", "premierleague", "3D195B", None),
    ("formula1", "f1", "E10600", None),

    # CARS & TRANSPORT
    ("tesla", "tesla", "CC0000", None),
    ("bmw", "bmw", "0066B1", None),
    ("mercedes", "mercedes", "242424", None),
    ("ferrari", "ferrari", "D40000", None),
    ("lamborghini", "lamborghini", "DDB320", "222222"),
    ("porsche", "porsche", "B12B28", None),
    ("audi", "audi", "BB0A30", None),
    ("toyota", "toyota", "EB0A1E", None),
    ("volkswagen", "volkswagen", "151F5D", None),

    # ENTERTAINMENT & MEDIA
    ("playstation", "playstation", "003791", None),
    ("xbox", "xbox", "107C10", None),
    ("nintendo", "nintendo", "E60012", None),
    ("netflix", "netflix", "E50914", None),
    ("disney", "waltdisneyworld", "1B3D82", None),
    ("roblox", "roblox", "000000", None),
    ("lego", "lego", "D01012", None),
    ("marvel", "marvel", "EC1D24", None),
    ("epic_games", "epicgames", "313131", None),

    # FASHION & LIFESTYLE
    ("target", "target", "CC0000", None),
    ("converse", "converse", "000000", None),
    ("crocs", "crocs", "1BA23C", None),
]


def colorize_svg(svg_text: str, fill_color: str) -> str:
    """Set fill color on the SVG path elements."""
    svg_text = re.sub(
        r'<svg ',
        f'<svg fill="#{fill_color}" ',
        svg_text,
        count=1,
    )
    return svg_text


def add_bg_circle(svg_text: str, bg_color: str) -> str:
    """Add a background rectangle behind the icon for contrast."""
    svg_text = svg_text.replace(
        '<path',
        f'<rect width="24" height="24" rx="4" fill="#{bg_color}"/><path',
        1,
    )
    return svg_text


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    total = len(BRANDS)
    downloaded = skipped = failed = 0

    force = "--force" in sys.argv

    print(f"Downloading {total} brand logos from Simple Icons via jsDelivr\n")

    for i, (filename, slug, color, bg) in enumerate(BRANDS, start=1):
        out_path = os.path.join(OUT_DIR, f"{filename}.png")

        if not force and os.path.exists(out_path):
            existing_size = os.path.getsize(out_path)
            if existing_size > 500:
                print(f"  [{i}/{total}] {filename}: already exists ({existing_size//1024}KB), skipping")
                skipped += 1
                continue

        url = f"{CDN_BASE}/{slug}.svg"
        print(f"  [{i}/{total}] {filename}: downloading {slug}.svg ...")

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                svg_text = resp.read().decode("utf-8")

            svg_text = colorize_svg(svg_text, color)
            if bg:
                svg_text = add_bg_circle(svg_text, bg)

            cairosvg.svg2png(
                bytestring=svg_text.encode("utf-8"),
                write_to=out_path,
                output_width=PNG_SIZE,
                output_height=PNG_SIZE,
                background_color="white",
            )
            downloaded += 1
            print(f"  [{i}/{total}] {filename}: saved! ({os.path.getsize(out_path)//1024}KB)")

        except Exception as exc:
            failed += 1
            print(f"  [{i}/{total}] {filename}: FAILED - {exc}")

        time.sleep(DELAY)

    print(f"\nDone!  Downloaded: {downloaded}  Skipped: {skipped}  Failed: {failed}")
    print(f"Images saved to: {OUT_DIR}/")


if __name__ == "__main__":
    main()
