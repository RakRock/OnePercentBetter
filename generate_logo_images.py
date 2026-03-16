"""
Generate brand logo images for the Logo Identifier app
using the Hugging Face Inference API (FLUX.1-schnell model).

Each image is a clean, stylised representation of a well-known brand logo
suitable for a recognition quiz.

Usage:
    export HF_TOKEN="hf_..."
    python generate_logo_images.py
"""

import os
import sys
import time

try:
    import truststore
    truststore.inject_into_ssl()
except ImportError:
    pass

from huggingface_hub import InferenceClient

OUT_DIR = os.path.join(os.path.dirname(__file__), "brand_logos")
MODEL = "black-forest-labs/FLUX.1-schnell"
WIDTH = 512
HEIGHT = 512
DELAY_SECONDS = 1.5

STYLE_SUFFIX = (
    ", clean minimalist logo design on pure white background,"
    " centered, high contrast, sharp vector-style illustration,"
    " professional brand identity, isolated icon, no text, no words,"
    " simple flat design"
)

LOGOS = [
    # TECH & APPS
    ("apple", "a bitten apple silhouette, smooth rounded shape with a leaf on top, solid black apple logo"),
    ("instagram", "a rounded square icon with a gradient from purple to orange to pink, containing a simple camera outline with a circle lens and a dot"),
    ("spotify", "a bright green circle with three curved white lines representing sound waves inside, streaming music icon"),
    ("snapchat", "a white ghost outline silhouette on a bright yellow background, cute friendly ghost shape"),
    ("whatsapp", "a green circle with a white telephone handset icon inside a speech bubble, messaging app icon"),
    ("reddit", "an orange circle with a white alien face, round head with antenna on top and two dot eyes, the reddit Snoo alien"),
    ("github", "a black silhouette of an Octocat, a cat shape with octopus tentacles, on white background"),
    ("discord", "a purple rounded shape with a white smiling game controller robot face, two eyes and a wide mouth"),
    ("twitch", "a purple background with a white speech bubble shape containing two glowing eyes, streaming platform icon"),
    ("dropbox", "an open blue box shape made of five diamond facets forming an unfolded box, blue on white"),
    ("airbnb", "a coral red symbol that combines a heart shape with an A letter and a location pin, rounded curves"),
    ("slack", "a hashtag shape made of four colourful rounded bars in blue, green, red, and yellow, with rounded dots"),
    ("microsoft", "four squares arranged in a 2x2 grid, top left red, top right green, bottom left blue, bottom right yellow, with small gaps between"),
    ("tiktok", "a stylised musical note shape in 3D effect with cyan and red neon glow on a dark black background"),
    ("pinterest", "a white stylised letter P shaped like a map pin on a bold red circle background"),
    ("youtube", "a red rounded rectangle with a white right-pointing play button triangle in the center"),
    ("shazam", "a blue circle with a stylised white S shape inside, resembling a lightning bolt S"),
    ("zoom", "a blue circle with a white video camera icon inside, video conferencing symbol"),
    ("evernote", "a green elephant head silhouette in profile view with a curled ear, simple elephant icon"),
    ("firefox", "a fox with a flaming orange tail curled around a blue-purple globe, the firefox browser icon"),
    ("android", "a bright green robot with a semicircular head, two antenna, rectangular body, simple cute robot mascot"),
    ("duolingo", "a bright lime green owl with large round white eyes, cute cartoon owl mascot, language learning"),
    ("waze", "a white ghost-like friendly face shape with a smile on a light blue background, navigation app icon"),
    ("opera", "a bold red O letter shape on white background, browser logo"),

    # FOOD & DRINKS
    ("starbucks", "a green circle containing a white stylised twin-tailed mermaid siren, symmetrical, coffee brand"),
    ("mcdonalds", "two tall golden yellow arches forming an M shape on a red background, fast food golden arches"),
    ("pepsi", "a circle divided by a wavy white line into a red upper half and blue lower half, soda brand globe"),
    ("redbull", "two red bulls charging at each other head to head with a golden yellow sun circle behind them, energy drink"),
    ("kfc", "a portrait illustration of an elderly gentleman with white hair, glasses, goatee, bow tie and white suit, Colonel Sanders face"),
    ("dominos", "a red and blue domino tile piece with three white dots, two on one side one on other, pizza brand"),
    ("tacobell", "a large bell shape in pink and purple gradient tones, simple bell silhouette"),
    ("chickfila", "a bold red stylised letter C that contains a hidden chicken silhouette in the negative space"),
    ("wendys", "a circular portrait of a smiling girl with red braided pigtails and freckles on a blue background"),
    ("pringles", "a cartoon face of a man with a large brown handlebar moustache, red bow tie, and parted brown hair, chip mascot"),
    ("monster_energy", "three vertical green claw scratch marks on a black background forming the letter M, energy drink"),
    ("dunkin", "an orange and hot pink colored icon with a coffee cup shape, donut and coffee brand"),

    # SPORTS & OUTDOORS
    ("nike", "a single smooth curved swoosh checkmark shape in solid black, athletic brand swoosh"),
    ("adidas", "three thick parallel diagonal stripes arranged to form a mountain or triangle peak shape, athletic brand"),
    ("puma", "a black silhouette of a leaping puma big cat mid-jump, athletic cat logo"),
    ("under_armour", "two overlapping U shapes interlocked that also form an A letter, athletic brand monogram in black"),
    ("lacoste", "a small green crocodile or alligator facing right with an open mouth, preppy fashion brand"),
    ("north_face", "three curved concentric arcs forming a quarter dome or half dome mountain shape, outdoor brand"),
    ("ferrari_horse", "a black prancing rearing horse on a bright yellow shield background, Italian sports car emblem"),

    # CARS & TRANSPORT
    ("tesla", "a stylised T letter that resembles a cross section of an electric motor, sharp pointed top, red on white"),
    ("bmw", "a circle divided into four quadrants, two opposite quadrants in blue and two in white, German car roundel"),
    ("mercedes", "a three-pointed silver star inside a circle, each point evenly spaced at 120 degrees, luxury car emblem"),
    ("ferrari", "a black prancing horse rearing up on hind legs on a yellow shield with green white red stripe on top"),
    ("lamborghini", "a golden charging bull silhouette on a dark black shield shape, Italian supercar emblem"),
    ("audi", "four silver interlocking rings in a horizontal row, each ring overlapping the next, car brand"),
    ("porsche", "an ornate crest shield with a rearing horse in center, antlers and red-black stripes, luxury car badge"),
    ("volkswagen", "a V stacked on top of a W inside a circle, simple silver letters in circle, German car brand"),
    ("toyota", "three overlapping ovals forming a symmetrical pattern, the inner ovals form a T shape inside the outer oval"),
    ("chevrolet", "a golden bowtie cross shape, elongated horizontal diamond or bowtie, American car brand"),
    ("subaru", "a dark blue oval containing a cluster of six silver stars, the Pleiades constellation, Japanese car"),
    ("mitsubishi", "three red diamond rhombus shapes arranged in a triangular pinwheel pattern, Japanese brand"),
    ("jaguar_car", "a silver leaping jaguar big cat in mid-pounce, sleek profile, British luxury car mascot"),

    # ENTERTAINMENT & MEDIA
    ("playstation", "a stylised P standing upright with an S lying flat crossing through it creating a 3D effect, gaming brand"),
    ("xbox", "a green sphere with a white X crossing through the center, gaming console brand"),
    ("steam", "a dark blue circle with a gear cog and a piston lever shape inside, PC gaming platform"),
    ("roblox", "a dark tilted square with a square hole punched through it, gaming platform icon"),
    ("nintendo", "a bold red rounded rectangle shape with a white N letter inside, gaming company"),
    ("netflix", "a bold red letter N with a shadow effect on dark background, streaming service"),
    ("disney", "a fairy tale castle silhouette with towers and spires against a blue sky with stars"),
    ("epic_games", "a dark silhouette of a human face in profile, side view of a head, game developer"),
    ("lego", "bold white letters on a bright red rounded square background, toy brick brand"),

    # FASHION & LIFESTYLE
    ("target", "a red and white bullseye, two concentric circles with a red center dot, retail brand"),
    ("ikea", "blue and yellow color scheme, bold letters inside a yellow oval on blue rectangle, Swedish furniture"),
    ("converse", "a five-pointed star inside a circle, the classic All Star emblem, shoe brand"),
    ("ralph_lauren", "a silhouette of a polo player on horseback swinging a mallet, preppy fashion brand"),
    ("crocs", "a cartoon green crocodile alligator character wearing sunglasses with a big smile, shoe brand mascot"),
    ("versace", "a golden Medusa head from Greek mythology with flowing serpent hair in a circle, luxury fashion"),
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

    total = len(LOGOS)
    generated = skipped = failed = 0

    print(f"Generating {total} brand logo images using model: {MODEL}\n")

    for i, (name, prompt) in enumerate(LOGOS, start=1):
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
    print(f"Images saved to: {OUT_DIR}/")


if __name__ == "__main__":
    main()
