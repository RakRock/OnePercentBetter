"""
Math content module for Krish's Math App.
Generates random visual math problems for 4-5 year olds using cute cartoon images.

Three levels:
  - Counting:     "How many ___ do you see?" (1-20 objects)
  - Addition:     Two groups with +, "How many in all?" (sum up to 10)
  - Subtraction:  One group with some crossed out, "How many are left?"
"""

import base64
import os
import random

# ── Directory where cartoon object images live ──
_MATH_IMG_DIR = os.path.join(os.path.dirname(__file__), "math_images")

# ── Cache for base64-encoded images (loaded once per object) ──
_B64_CACHE: dict[str, str] = {}


def _get_b64(img_path: str) -> str | None:
    """Load an image file and return its base64 data URI string, cached."""
    if img_path in _B64_CACHE:
        return _B64_CACHE[img_path]
    if not os.path.exists(img_path):
        return None
    with open(img_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    data_uri = f"data:image/png;base64,{encoded}"
    _B64_CACHE[img_path] = data_uri
    return data_uri

# ── Object pool: (display_name, image_filename, fallback_emoji) ──
OBJECT_POOL = [
    ("apples", "apple.png", "🍎"),
    ("bananas", "banana.png", "🍌"),
    ("cookies", "cookie.png", "🍪"),
    ("strawberries", "strawberry.png", "🍓"),
    ("oranges", "orange.png", "🍊"),
    ("stars", "star.png", "🌟"),
    ("cats", "cat.png", "🐱"),
    ("dogs", "dog.png", "🐶"),
    ("frogs", "frog.png", "🐸"),
    ("butterflies", "butterfly.png", "🦋"),
    ("bunnies", "bunny.png", "🐰"),
    ("flowers", "flower.png", "🌸"),
    ("cars", "car.png", "🚗"),
    ("cupcakes", "cupcake.png", "🧁"),
    ("fish", "fish.png", "🐟"),
    ("balloons", "balloon.png", "🎈"),
]


def _pick_object():
    """Pick a random object, returning (name, img_path, fallback_emoji)."""
    name, filename, emoji = random.choice(OBJECT_POOL)
    img_path = os.path.join(_MATH_IMG_DIR, filename)
    return name, img_path, emoji

# ── Level definitions ──
LEVELS = {
    "counting": {
        "id": "counting",
        "title": "Counting",
        "emoji": "🔢",
        "color": "#22c55e",
        "description": "Count the objects!",
        "icon_size": "2.2rem",
    },
    "addition": {
        "id": "addition",
        "title": "Addition",
        "emoji": "➕",
        "color": "#3b82f6",
        "description": "Add two groups together!",
        "icon_size": "2.2rem",
    },
    "subtraction": {
        "id": "subtraction",
        "title": "Subtraction",
        "emoji": "➖",
        "color": "#a855f7",
        "description": "Take some away!",
        "icon_size": "2.2rem",
    },
}


def _make_options(correct, low=0, high=20):
    """Generate a list of 3 unique options including the correct answer.

    Returns (options_list, correct_index).
    """
    choices = {correct}
    attempts = 0
    while len(choices) < 3 and attempts < 50:
        offset = random.choice([-2, -1, 1, 2, -3, 3])
        wrong = correct + offset
        if low <= wrong <= high and wrong != correct:
            choices.add(wrong)
        attempts += 1

    # Fallback: pad with nearby numbers
    while len(choices) < 3:
        for v in range(max(low, correct - 5), min(high + 1, correct + 6)):
            if v not in choices:
                choices.add(v)
                break

    options = sorted(choices)
    correct_idx = options.index(correct)
    return options, correct_idx


def _img_tag(img_path, fallback_emoji, size=60):
    """Return an <img> tag using base64 data URI, or a styled emoji span as fallback."""
    data_uri = _get_b64(img_path)
    if data_uri:
        return (
            f'<img src="{data_uri}" '
            f'style="width:{size}px;height:{size}px;object-fit:contain;'
            f'margin:4px;vertical-align:middle;" />'
        )
    return f'<span style="font-size:{int(size * 0.6)}px;margin:4px;vertical-align:middle;">{fallback_emoji}</span>'


def _render_image_grid(img_path, fallback_emoji, count, per_row=5, size=60):
    """Build HTML showing `count` copies of the object image in rows."""
    tag = _img_tag(img_path, fallback_emoji, size)
    rows = []
    for i in range(0, count, per_row):
        row_count = min(per_row, count - i)
        row = "".join([tag] * row_count)
        rows.append(f'<div style="display:flex;justify-content:center;gap:4px;margin:4px 0;">{row}</div>')
    return "".join(rows)


def _render_crossed_image(img_path, fallback_emoji, size=60):
    """Return an image with a red X overlay to show it's been taken away."""
    data_uri = _get_b64(img_path)
    if data_uri:
        return (
            f'<span style="position:relative;display:inline-block;width:{size}px;height:{size}px;margin:4px;">'
            f'<img src="{data_uri}" '
            f'style="width:{size}px;height:{size}px;object-fit:contain;opacity:0.35;filter:grayscale(80%);" />'
            f'<span style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);'
            f'font-size:{int(size*0.7)}px;color:#ef4444;font-weight:bold;">✕</span>'
            f'</span>'
        )
    return f'<span style="font-size:{int(size * 0.6)}px;margin:4px;opacity:0.35;">❌</span>'


def generate_counting_problem():
    """Generate a counting problem: show N objects, ask how many."""
    obj_name, img_path, emoji = _pick_object()
    count = random.randint(1, 20)
    size = 50 if count > 10 else 60
    options, answer = _make_options(count, low=1, high=20)

    return {
        "type": "counting",
        "obj_name": obj_name,
        "img_path": img_path,
        "emoji": emoji,
        "count": count,
        "display_html": _render_image_grid(img_path, emoji, count, size=size),
        "question": f"How many {obj_name} do you see?",
        "options": options,
        "answer": answer,
    }


def generate_addition_problem():
    """Generate an addition problem: two groups, ask for the sum."""
    obj_name, img_path, emoji = _pick_object()
    a = random.randint(1, 5)
    b = random.randint(1, 9 - a)
    total = a + b
    options, answer = _make_options(total, low=2, high=10)

    tag = _img_tag(img_path, emoji, size=60)
    group_a = "".join([tag] * a)
    group_b = "".join([tag] * b)
    display_html = (
        f'<div style="display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:4px;">'
        f'<div style="display:flex;align-items:center;gap:4px;background:#e0f2fe;border-radius:16px;padding:8px 12px;">{group_a}</div>'
        f'<span style="font-size:2.5rem;margin:0 12px;color:#3b82f6;font-weight:800;">+</span>'
        f'<div style="display:flex;align-items:center;gap:4px;background:#fef3c7;border-radius:16px;padding:8px 12px;">{group_b}</div>'
        f'</div>'
    )

    return {
        "type": "addition",
        "obj_name": obj_name,
        "img_path": img_path,
        "emoji": emoji,
        "a": a,
        "b": b,
        "total": total,
        "display_html": display_html,
        "question": f"{a} {obj_name} + {b} {obj_name} = ?",
        "options": options,
        "answer": answer,
    }


def generate_subtraction_problem():
    """Generate a subtraction problem: start with a group, cross some out."""
    obj_name, img_path, emoji = _pick_object()
    total = random.randint(3, 9)
    take_away = random.randint(1, total - 1)
    remaining = total - take_away
    options, answer = _make_options(remaining, low=0, high=9)

    tag = _img_tag(img_path, emoji, size=60)
    crossed_tag = _render_crossed_image(img_path, emoji, size=60)

    kept_items = "".join([tag] * remaining)
    crossed_items = "".join([crossed_tag] * take_away)
    display_html = (
        f'<div style="display:flex;align-items:center;justify-content:center;flex-wrap:wrap;gap:4px;">'
        f'<div style="display:flex;align-items:center;gap:4px;background:#d1fae5;border-radius:16px;padding:8px 12px;">{kept_items}</div>'
        f'<span style="font-size:2.5rem;margin:0 12px;color:#a855f7;font-weight:800;">−</span>'
        f'<div style="display:flex;align-items:center;gap:4px;background:#fee2e2;border-radius:16px;padding:8px 12px;">{crossed_items}</div>'
        f'</div>'
    )

    return {
        "type": "subtraction",
        "obj_name": obj_name,
        "img_path": img_path,
        "emoji": emoji,
        "total": total,
        "take_away": take_away,
        "remaining": remaining,
        "display_html": display_html,
        "question": f"{total} {obj_name} − {take_away} {obj_name} = ?",
        "options": options,
        "answer": answer,
    }


_GENERATORS = {
    "counting": generate_counting_problem,
    "addition": generate_addition_problem,
    "subtraction": generate_subtraction_problem,
}


def generate_problem(level_id):
    """Generate a single problem for the given level."""
    gen = _GENERATORS.get(level_id)
    if not gen:
        raise ValueError(f"Unknown level: {level_id}")
    return gen()


def generate_round(level_id, num_problems=5):
    """Generate a list of problems for one practice round."""
    return [generate_problem(level_id) for _ in range(num_problems)]


def get_all_levels():
    """Return all levels as a list."""
    return list(LEVELS.values())


def get_level(level_id):
    """Return a level by ID."""
    return LEVELS.get(level_id)
