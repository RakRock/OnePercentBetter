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
PNG_SIZE = 512
DELAY = 0.3

# (filename, simple-icons slug, hex brand color, optional bg color)
BRANDS = [
    # TECH & APPS
    ("apple", "apple", "000000", None),
    ("instagram", "instagram", "E4405F", None),
    ("spotify", "spotify", "1DB954", None),
    ("snapchat", "snapchat", "FFFC00", "F5F5F5"),
    ("whatsapp", "whatsapp", "25D366", None),
    ("reddit", "reddit", "FF4500", None),
    ("github", "github", "181717", None),
    ("discord", "discord", "5865F2", None),
    ("twitch", "twitch", "9146FF", None),
    ("dropbox", "dropbox", "0061FF", None),
    ("airbnb", "airbnb", "FF5A5F", None),
    ("slack", "slack", "4A154B", None),
    ("microsoft", "microsoft", "5E5E5E", None),
    ("tiktok", "tiktok", "000000", None),
    ("pinterest", "pinterest", "BD081C", None),
    ("youtube", "youtube", "FF0000", None),
    ("shazam", "shazam", "0088FF", None),
    ("zoom", "zoom", "0B5CFF", None),
    ("evernote", "evernote", "00A82D", None),
    ("firefox", "firefoxbrowser", "FF7139", None),
    ("android", "android", "34A853", None),
    ("duolingo", "duolingo", "58CC02", None),
    ("waze", "waze", "33CCFF", None),
    ("opera", "opera", "FF1B2D", None),

    # FOOD & DRINKS
    ("starbucks", "starbucks", "006241", None),
    ("mcdonalds", "mcdonalds", "FBC817", None),
    ("pepsi", "pepsi", "004B93", None),
    ("redbull", "redbull", "DB0A40", None),
    ("kfc", "kfc", "F40027", None),
    ("dominos", "dominos", "006491", None),
    ("tacobell", "tacobell", "702082", None),
    ("chickfila", "chickfila", "E51636", None),
    ("wendys", "wendys", "E2203D", None),
    ("pringles", "pringles", "007B00", None),
    ("monster_energy", "monsterenergy", "95D600", "222222"),
    ("dunkin", "dunkindonuts", "DD4A21", None),

    # SPORTS & OUTDOORS
    ("nike", "nike", "111111", None),
    ("adidas", "adidas", "000000", None),
    ("puma", "puma", "000000", None),
    ("under_armour", "underarmour", "1D1D1D", None),
    ("lacoste", "lacoste", "004526", None),
    ("north_face", "thenorthface", "000000", None),
    ("ferrari_horse", "ferrari", "D40000", None),

    # CARS & TRANSPORT
    ("tesla", "tesla", "CC0000", None),
    ("bmw", "bmw", "0066B1", None),
    ("mercedes", "mercedes", "242424", None),
    ("ferrari", "ferrari", "D40000", None),
    ("lamborghini", "lamborghini", "DDB320", "222222"),
    ("audi", "audi", "BB0A30", None),
    ("porsche", "porsche", "B12B28", None),
    ("volkswagen", "volkswagen", "151F5D", None),
    ("toyota", "toyota", "EB0A1E", None),
    ("chevrolet", "chevrolet", "CD9834", None),
    ("subaru", "subaru", "013C74", None),
    ("mitsubishi", "mitsubishi", "E60012", None),
    ("jaguar_car", "jaguar", "000000", None),

    # ENTERTAINMENT & MEDIA
    ("playstation", "playstation", "003791", None),
    ("xbox", "xbox", "107C10", None),
    ("steam", "steam", "000000", None),
    ("roblox", "roblox", "000000", None),
    ("nintendo", "nintendo", "E60012", None),
    ("netflix", "netflix", "E50914", None),
    ("disney", "waltdisneyworld", "1B3D82", None),
    ("epic_games", "epicgames", "313131", None),
    ("lego", "lego", "D01012", None),

    # FASHION & LIFESTYLE
    ("target", "target", "CC0000", None),
    ("ikea", "ikea", "0058A3", None),
    ("converse", "converse", "000000", None),
    ("ralph_lauren", "ralphlauren", "041E42", None),
    ("crocs", "crocs", "1BA23C", None),
    ("versace", "versace", "000000", None),
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
    """Add a background circle behind the icon for contrast."""
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

    print(f"Downloading {total} brand logos from Simple Icons via jsDelivr\n")

    for i, (filename, slug, color, bg) in enumerate(BRANDS, start=1):
        out_path = os.path.join(OUT_DIR, f"{filename}.png")

        if os.path.exists(out_path):
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
