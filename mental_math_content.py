"""
Mental Math Sprint — procedurally generated math questions for Arjun.

Questions are generated randomly each time so every sprint feels fresh.
Categories: Quick Arithmetic, Percentages, Fractions, Estimation, Word Problems.
Difficulty is calibrated for an 11-year-old (medium).
"""

import random

CATEGORIES = {
    "arithmetic": {"name": "Quick Arithmetic", "emoji": "⚡", "color": "#3b82f6"},
    "percentages": {"name": "Percentages", "emoji": "💯", "color": "#10b981"},
    "fractions": {"name": "Fractions", "emoji": "🍕", "color": "#f59e0b"},
    "estimation": {"name": "Estimation", "emoji": "🎯", "color": "#8b5cf6"},
    "word_problems": {"name": "Word Problems", "emoji": "📝", "color": "#ef4444"},
}


def _make_options(correct, spread=None, force_int=True):
    """Generate 4 options including the correct answer with plausible distractors."""
    if spread is None:
        spread = max(3, abs(correct) // 4) if correct != 0 else 5

    options = {correct}
    attempts = 0
    while len(options) < 4 and attempts < 50:
        offset = random.randint(1, spread)
        sign = random.choice([-1, 1])
        distractor = correct + sign * offset
        if force_int:
            distractor = int(distractor)
        if distractor != correct and distractor not in options:
            if distractor >= 0 or correct < 0:
                options.add(distractor)
        attempts += 1

    while len(options) < 4:
        options.add(correct + len(options) * 2)

    options = list(options)
    random.shuffle(options)
    answer_idx = options.index(correct)
    if force_int:
        options = [int(o) for o in options]
    return options, answer_idx


def _generate_addition():
    a = random.randint(10, 99)
    b = random.randint(10, 99)
    correct = a + b
    q = f"What is {a} + {b}?"
    options, idx = _make_options(correct)
    return {"question": q, "options": options, "answer": idx, "category": "arithmetic"}


def _generate_subtraction():
    a = random.randint(30, 150)
    b = random.randint(5, a - 5)
    correct = a - b
    q = f"What is {a} − {b}?"
    options, idx = _make_options(correct)
    return {"question": q, "options": options, "answer": idx, "category": "arithmetic"}


def _generate_multiplication():
    a = random.randint(2, 15)
    b = random.randint(2, 15)
    correct = a * b
    q = f"What is {a} × {b}?"
    options, idx = _make_options(correct, spread=max(5, correct // 5))
    return {"question": q, "options": options, "answer": idx, "category": "arithmetic"}


def _generate_division():
    b = random.randint(2, 12)
    correct = random.randint(2, 15)
    a = b * correct
    q = f"What is {a} ÷ {b}?"
    options, idx = _make_options(correct)
    return {"question": q, "options": options, "answer": idx, "category": "arithmetic"}


def _generate_percentage():
    templates = [
        (10, [100, 200, 300, 400, 500, 150, 250, 350]),
        (20, [50, 100, 150, 200, 250, 300]),
        (25, [40, 80, 100, 120, 160, 200, 240]),
        (50, [20, 40, 60, 80, 100, 120, 150, 200]),
        (15, [100, 200, 300, 400]),
        (30, [50, 100, 150, 200]),
        (75, [20, 40, 80, 100, 200]),
    ]
    pct, bases = random.choice(templates)
    base = random.choice(bases)
    correct = int(base * pct / 100)
    q = f"What is {pct}% of {base}?"
    options, idx = _make_options(correct, spread=max(5, correct // 3))
    return {"question": q, "options": options, "answer": idx, "category": "percentages"}


def _generate_percentage_word():
    scenarios = [
        ("A shirt costs ${base}. It's {pct}% off. How much do you save?", None),
        ("You scored {pct}% on a test with {base} questions. How many did you get right?", None),
        ("A pizza has {base} slices. You ate {pct}% of them. How many slices did you eat?", None),
    ]
    pct = random.choice([10, 20, 25, 50, 75])
    base = random.choice([20, 40, 50, 60, 80, 100])
    template, _ = random.choice(scenarios)
    q = template.format(base=base, pct=pct)
    correct = int(base * pct / 100)
    options, idx = _make_options(correct, spread=max(3, correct // 3))
    return {"question": q, "options": options, "answer": idx, "category": "percentages"}


def _generate_fraction_addition():
    pairs = [
        ("1/2", "1/4", "3/4"), ("1/3", "1/3", "2/3"),
        ("1/4", "1/4", "1/2"), ("1/2", "1/3", "5/6"),
        ("2/5", "1/5", "3/5"), ("1/4", "3/4", "1"),
        ("1/6", "1/6", "1/3"), ("3/8", "1/8", "1/2"),
        ("1/2", "1/6", "2/3"), ("2/3", "1/6", "5/6"),
    ]
    a, b, correct_str = random.choice(pairs)
    q = f"What is {a} + {b}?"

    all_fractions = [
        "1/4", "1/3", "1/2", "2/3", "3/4", "1", "5/6",
        "3/5", "2/5", "1/6", "7/8", "5/8", "1/8", "3/8",
    ]
    distractors = [f for f in all_fractions if f != correct_str]
    random.shuffle(distractors)
    options = [correct_str] + distractors[:3]
    random.shuffle(options)
    idx = options.index(correct_str)
    return {"question": q, "options": options, "answer": idx, "category": "fractions"}


def _generate_fraction_of():
    combos = [
        ("1/2", 2, [10, 20, 30, 40, 50, 60]),
        ("1/3", 3, [12, 15, 18, 21, 24, 27, 30]),
        ("1/4", 4, [8, 12, 16, 20, 24, 28, 32]),
        ("2/3", 3, [9, 12, 15, 18, 21, 24]),
        ("3/4", 4, [8, 12, 16, 20, 24, 28]),
        ("1/5", 5, [10, 15, 20, 25, 30, 35]),
        ("2/5", 5, [10, 15, 20, 25, 30]),
    ]
    frac_str, denom, bases = random.choice(combos)
    base = random.choice(bases)
    num = int(frac_str.split("/")[0])
    correct = int(base * num / denom)
    q = f"What is {frac_str} of {base}?"
    options, idx = _make_options(correct, spread=max(3, correct // 3))
    return {"question": q, "options": options, "answer": idx, "category": "fractions"}


def _generate_fraction_remaining():
    parts = random.choice([4, 6, 8, 10, 12])
    eaten = random.randint(1, parts - 1)
    items = random.choice(["slices of pizza", "pieces of cake", "cookies", "candies"])
    q = f"You have {parts} {items} and eat {eaten}. What fraction is left?"
    left = parts - eaten
    from math import gcd
    g = gcd(left, parts)
    correct_str = f"{left // g}/{parts // g}" if parts // g != 1 else str(left // g)

    all_frac = set()
    for n in range(1, parts):
        g2 = gcd(n, parts)
        all_frac.add(f"{n // g2}/{parts // g2}")
    all_frac.discard(correct_str)
    distractors = list(all_frac)
    random.shuffle(distractors)
    while len(distractors) < 3:
        distractors.append(f"{random.randint(1, 5)}/{random.randint(2, 8)}")
    options = [correct_str] + distractors[:3]
    random.shuffle(options)
    idx = options.index(correct_str)
    return {"question": q, "options": options, "answer": idx, "category": "fractions"}


def _generate_estimation():
    templates = [
        lambda: _est_product(),
        lambda: _est_minutes(),
        lambda: _est_closest(),
    ]
    return random.choice(templates)()


def _est_product():
    a = random.choice([49, 51, 99, 101, 198, 202, 301, 499, 501])
    b = random.randint(2, 9)
    correct = a * b
    rounded_a = round(a, -1) if a < 100 else round(a, -2)
    q = f"Estimate: {a} × {b} is closest to?"
    spread = max(50, correct // 5)
    options, idx = _make_options(correct, spread=spread)
    return {"question": q, "options": options, "answer": idx, "category": "estimation"}


def _est_minutes():
    questions = [
        ("About how many minutes are in 1 day?", 1440, 200),
        ("About how many seconds are in 1 hour?", 3600, 500),
        ("About how many hours are in 1 week?", 168, 30),
        ("About how many days are in 2 years?", 730, 100),
        ("About how many minutes are in 2 hours?", 120, 20),
        ("About how many seconds are in 10 minutes?", 600, 100),
        ("About how many weeks are in 1 year?", 52, 8),
        ("About how many months are in 5 years?", 60, 10),
    ]
    q_text, correct, spread = random.choice(questions)
    options, idx = _make_options(correct, spread=spread)
    return {"question": q_text, "options": options, "answer": idx, "category": "estimation"}


def _est_closest():
    a = random.randint(100, 900)
    b = random.randint(100, 900)
    correct = a + b
    q = f"Without calculating exactly, {a} + {b} is closest to?"
    rounded = round(correct, -2)
    distractors = {rounded - 200, rounded - 100, rounded, rounded + 100, rounded + 200}
    distractors.discard(correct)
    distractors = [d for d in distractors if d > 0]
    random.shuffle(distractors)
    options = [correct] + distractors[:3]
    while len(options) < 4:
        options.append(correct + random.choice([-150, 150, -250, 250]))
    random.shuffle(options)
    options = [int(o) for o in options]
    idx = options.index(correct)
    return {"question": q, "options": options, "answer": idx, "category": "estimation"}


def _generate_word_problem():
    templates = [
        _wp_shopping,
        _wp_sharing,
        _wp_speed,
        _wp_money_left,
        _wp_area,
    ]
    return random.choice(templates)()


def _wp_shopping():
    item = random.choice(["book", "toy", "game", "backpack", "shirt", "pair of shoes"])
    price = random.choice([10, 15, 20, 25, 30, 40, 50, 60])
    qty = random.randint(2, 5)
    correct = price * qty
    q = f"A {item} costs ${price}. How much do {qty} cost?"
    options, idx = _make_options(correct, spread=max(10, correct // 4))
    options = [f"${o}" if isinstance(o, int) else o for o in options]
    str_correct = f"${correct}"
    idx = options.index(str_correct)
    return {"question": q, "options": options, "answer": idx, "category": "word_problems"}


def _wp_sharing():
    total = random.choice([24, 30, 36, 40, 48, 60])
    people = random.choice([3, 4, 5, 6, 8])
    while total % people != 0:
        people = random.choice([3, 4, 5, 6, 8])
    correct = total // people
    item = random.choice(["stickers", "cards", "candies", "marbles", "pencils"])
    q = f"You have {total} {item} to share equally among {people} friends. How many does each get?"
    options, idx = _make_options(correct)
    return {"question": q, "options": options, "answer": idx, "category": "word_problems"}


def _wp_speed():
    speed = random.choice([30, 40, 50, 60])
    hours = random.choice([2, 3, 4, 5])
    correct = speed * hours
    q = f"A car drives at {speed} mph for {hours} hours. How far does it go?"
    options, idx = _make_options(correct, spread=max(20, correct // 4))
    options = [f"{o} miles" for o in options]
    str_correct = f"{correct} miles"
    idx = options.index(str_correct)
    return {"question": q, "options": options, "answer": idx, "category": "word_problems"}


def _wp_money_left():
    start = random.choice([20, 50, 100])
    items = random.randint(2, 4)
    costs = [random.randint(3, start // (items + 1)) for _ in range(items)]
    spent = sum(costs)
    correct = start - spent
    cost_str = " + ".join(f"${c}" for c in costs)
    q = f"You have ${start}. You spend {cost_str}. How much is left?"
    options, idx = _make_options(correct, spread=max(5, correct // 3))
    options = [f"${o}" if isinstance(o, int) else o for o in options]
    str_correct = f"${correct}"
    idx = options.index(str_correct)
    return {"question": q, "options": options, "answer": idx, "category": "word_problems"}


def _wp_area():
    l = random.randint(3, 15)
    w = random.randint(3, 15)
    correct = l * w
    shape = "rectangle" if l != w else "square"
    q = f"A {shape} is {l} feet long and {w} feet wide. What is its area?"
    options, idx = _make_options(correct, spread=max(5, correct // 4))
    options = [f"{o} sq ft" for o in options]
    str_correct = f"{correct} sq ft"
    idx = options.index(str_correct)
    return {"question": q, "options": options, "answer": idx, "category": "word_problems"}


_GENERATORS = {
    "arithmetic": [_generate_addition, _generate_subtraction, _generate_multiplication, _generate_division],
    "percentages": [_generate_percentage, _generate_percentage_word],
    "fractions": [_generate_fraction_addition, _generate_fraction_of, _generate_fraction_remaining],
    "estimation": [_generate_estimation],
    "word_problems": [_generate_word_problem],
}


def generate_sprint(num_questions: int = 10, category: str | None = None) -> list:
    """Generate a set of math questions for a sprint round.

    If category is None, picks a mix across all categories.
    Returns a list of question dicts.
    """
    questions = []

    if category and category in _GENERATORS:
        gens = _GENERATORS[category]
        for _ in range(num_questions):
            gen = random.choice(gens)
            questions.append(gen())
    else:
        cats = list(_GENERATORS.keys())
        for i in range(num_questions):
            cat = cats[i % len(cats)]
            gen = random.choice(_GENERATORS[cat])
            questions.append(gen())
        random.shuffle(questions)

    return questions
