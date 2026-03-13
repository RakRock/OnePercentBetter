"""
Generate educational science diagrams for the Science Corner app
using the Hugging Face Inference API (FLUX.1-schnell model).

Each image is a clean, labeled, educational-style diagram suitable
for a 6th-grade science quiz.

Usage:
    export HF_TOKEN="hf_..."
    python generate_science_images.py
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

OUT_DIR = os.path.join(os.path.dirname(__file__), "science_images")
MODEL = "black-forest-labs/FLUX.1-schnell"
WIDTH = 512
HEIGHT = 384
DELAY_SECONDS = 1.5

STYLE_SUFFIX = (
    ", clean educational diagram, simple labeled illustration,"
    " bright colors on white background, textbook style,"
    " kid-friendly, clear and simple, no complex text,"
    " science poster style, 6th grade level"
)

DIAGRAMS = [
    # Life Science
    ("animal_cell", "diagram of an animal cell showing nucleus, mitochondria, cell membrane, ribosomes, and cytoplasm, labeled parts, colorful cross-section view"),
    ("plant_cell", "diagram of a plant cell showing cell wall, chloroplast, nucleus, vacuole, cell membrane, labeled parts, colorful cross-section view"),
    ("cell_membrane", "diagram of cell membrane showing phospholipid bilayer with proteins, molecules passing through, simple cross-section"),
    ("mitochondria", "diagram of a mitochondria organelle, cutaway view showing inner folds cristae, energy ATP symbols, colorful"),
    ("levels_of_organization", "diagram showing levels of biological organization: cell, tissue, organ, organ system, organism, arrows connecting each level, simple icons"),
    ("digestive_system", "simple diagram of human digestive system showing mouth, esophagus, stomach, small intestine, large intestine, labeled"),
    ("circulatory_system", "simple diagram of human circulatory system showing heart, arteries in red, veins in blue, blood flow arrows"),
    ("respiratory_system", "simple diagram of human respiratory system showing nose, trachea, lungs, diaphragm, oxygen and CO2 arrows"),
    ("nervous_system", "simple diagram of human nervous system showing brain, spinal cord, nerves branching out through the body"),
    ("skeletal_system", "simple diagram of human skeleton showing skull, ribcage, spine, pelvis, arms, legs, labeled major bones"),
    ("red_white_blood_cells", "diagram showing red blood cells carrying oxygen and white blood cells fighting germs, colorful microscope view"),
    ("kidney", "simple cross-section diagram of a human kidney showing filtering of blood, clean and labeled"),
    # Reproduction & Inheritance
    ("dna_double_helix", "diagram of DNA double helix structure showing twisted ladder shape, base pairs in different colors, sugar-phosphate backbone"),
    ("chromosomes", "diagram showing chromosomes inside a cell nucleus, paired chromosomes, X shape, colorful"),
    ("cell_division", "simple diagram of cell division mitosis stages: one cell splitting into two identical cells, step by step"),
    ("heredity_traits", "simple diagram showing inheritance: parents passing eye color genes to offspring, dominant and recessive alleles, family tree style"),
    ("sexual_vs_asexual", "split diagram comparing sexual reproduction (two parents, diverse offspring) vs asexual reproduction (one parent, identical offspring)"),
    ("pollination", "diagram of flower pollination showing bee carrying pollen from one flower to another, labeled pistil and stamen"),
    # Ecosystems & Energy
    ("food_chain", "simple food chain diagram: sun, grass, grasshopper, frog, snake, hawk, arrows showing energy flow"),
    ("food_web", "food web diagram showing multiple interconnected food chains in a meadow ecosystem, arrows between organisms"),
    ("energy_pyramid", "energy pyramid diagram showing producers at base, primary consumers, secondary consumers, tertiary consumers at top, decreasing energy"),
    ("water_cycle", "diagram of the water cycle showing evaporation, condensation, precipitation, collection, arrows and labels, clouds and rain"),
    ("carbon_cycle", "simple carbon cycle diagram showing CO2 in atmosphere, photosynthesis, respiration, decomposition, fossil fuels"),
    ("photosynthesis", "diagram of photosynthesis: sunlight plus water plus CO2 going into a leaf, glucose and oxygen coming out, labeled arrows"),
    ("ecosystem", "colorful ecosystem diagram showing living things (plants, animals, insects) and nonliving things (water, sun, rocks, soil) in a habitat"),
    ("decomposer", "diagram showing decomposers (mushrooms, bacteria, worms) breaking down dead leaves and returning nutrients to soil"),
    # Physical Science
    ("atom_structure", "diagram of an atom showing protons and neutrons in nucleus, electrons orbiting in shells, labeled with charges plus minus"),
    ("states_of_matter", "three-panel diagram showing solid (tightly packed molecules), liquid (loosely arranged), gas (spread apart), with molecule arrangements"),
    ("physical_vs_chemical", "split diagram: physical changes (ice melting, paper tearing) vs chemical changes (wood burning, iron rusting), before and after"),
    ("heat_transfer", "three-panel diagram showing conduction (spoon in pot), convection (warm air rising), radiation (sun to earth), labeled"),
    ("kinetic_potential_energy", "diagram of a roller coaster showing potential energy at top and kinetic energy at bottom, with energy labels"),
    ("periodic_table", "colorful simplified periodic table highlighting common elements like H, O, C, N, Fe, Au, Na, Cl with element symbols"),
    ("newton_third_law", "diagram illustrating Newton's third law: person pushing wall and wall pushing back, action and reaction arrows equal and opposite"),
    ("friction", "diagram showing friction force: a box being pushed on a surface, friction arrow opposing motion, labeled forces"),
    ("density", "diagram comparing density: a heavy small rock sinking in water vs a light large block of wood floating, labeled"),
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

    total = len(DIAGRAMS)
    generated = skipped = failed = 0

    print(f"Generating {total} science diagram images using model: {MODEL}\n")

    for i, (name, prompt) in enumerate(DIAGRAMS, start=1):
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
