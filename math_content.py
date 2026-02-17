"""
Math content module for Krish's Math App.
Generates random visual math problems for 4-5 year olds using emoji objects.

Three levels:
  - Counting:     "How many ___ do you see?" (1-20 objects)
  - Addition:     Two groups with +, "How many in all?" (sum up to 20)
  - Subtraction:  One group with some crossed out, "How many are left?"
"""

import random

# ── Emoji objects used in problems ──
EMOJI_POOL = [
    "🍎", "🍌", "🍪", "🍓", "🍊", "🌟", "⭐", "❤️",
    "🐟", "🐱", "🐶", "🐸", "🦋", "🐝", "🐢", "🐰",
    "🌸", "🌻", "🎈", "🚗", "⚽", "🧁", "🍩", "🍕",
]

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


def _render_emoji_grid(emoji, count, per_row=5):
    """Build an HTML string showing `count` copies of `emoji` in rows."""
    rows = []
    for i in range(0, count, per_row):
        row_count = min(per_row, count - i)
        row = " ".join([emoji] * row_count)
        rows.append(row)
    return "<br>".join(rows)


def generate_counting_problem():
    """Generate a counting problem: show N objects, ask how many."""
    emoji = random.choice(EMOJI_POOL)
    count = random.randint(1, 20)
    options, answer = _make_options(count, low=1, high=20)

    return {
        "type": "counting",
        "emoji": emoji,
        "count": count,
        "display_html": _render_emoji_grid(emoji, count),
        "question": f"How many {emoji} do you see?",
        "options": options,
        "answer": answer,
    }


def generate_addition_problem():
    """Generate an addition problem: two groups, ask for the sum."""
    emoji = random.choice(EMOJI_POOL)
    a = random.randint(1, 5)
    b = random.randint(1, 9 - a)
    total = a + b
    options, answer = _make_options(total, low=2, high=10)

    group_a = " ".join([emoji] * a)
    group_b = " ".join([emoji] * b)
    display_html = (
        f'<span style="display:inline-block">{group_a}</span>'
        f'<span style="display:inline-block;margin:0 0.8rem;font-size:2rem;vertical-align:middle;">+</span>'
        f'<span style="display:inline-block">{group_b}</span>'
    )

    return {
        "type": "addition",
        "emoji": emoji,
        "a": a,
        "b": b,
        "total": total,
        "display_html": display_html,
        "question": f"{a} {emoji} + {b} {emoji} = ?",
        "options": options,
        "answer": answer,
    }


def generate_subtraction_problem():
    """Generate a subtraction problem: start with a group, cross some out."""
    emoji = random.choice(EMOJI_POOL)
    total = random.randint(3, 9)
    take_away = random.randint(1, total - 1)
    remaining = total - take_away
    options, answer = _make_options(remaining, low=0, high=9)

    kept = " ".join([emoji] * remaining)
    crossed = " ".join(["❌"] * take_away)
    display_html = (
        f'<div style="margin-bottom:0.3rem;">'
        f'{"  ".join([emoji] * total)}'
        f'</div>'
        f'<div style="opacity:0.7;">'
        f'{kept} {crossed}'
        f'</div>'
    )

    return {
        "type": "subtraction",
        "emoji": emoji,
        "total": total,
        "take_away": take_away,
        "remaining": remaining,
        "display_html": display_html,
        "question": f"{total} {emoji} - {take_away} {emoji} = ?",
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
