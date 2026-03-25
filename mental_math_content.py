"""
Mental Math Sprint — procedurally generated math questions for Arjun.

Questions are generated randomly each time so every sprint feels fresh.
Categories: Quick Arithmetic, Percentages, Fractions, Estimation, Word Problems.
Difficulty is calibrated for an 11-year-old (medium-hard).
"""

import random

CATEGORIES = {
    "percentages": {"name": "Percentages", "emoji": "💯", "color": "#10b981"},
    "fractions": {"name": "Fractions", "emoji": "🍕", "color": "#f59e0b"},
    "word_problems": {"name": "Word Problems", "emoji": "📝", "color": "#ef4444"},
    "powers": {"name": "Powers & Exponents", "emoji": "🔢", "color": "#06b6d4"},
    "ratios": {"name": "Ratios & Proportions", "emoji": "⚖️", "color": "#e11d48"},
    "proportionality": {
        "name": "Constant of Proportionality",
        "emoji": "📐",
        "color": "#0ea5e9",
    },
    "distributive": {
        "name": "Distributive Property",
        "emoji": "🔀",
        "color": "#d946ef",
    },
    "equations": {
        "name": "Solving Equations",
        "emoji": "🔤",
        "color": "#7c3aed",
    },
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
    a = random.randint(20, 99)
    b = random.randint(20, 99)
    correct = a + b
    q = f"What is {a} + {b}?"
    options, idx = _make_options(correct)
    return {"question": q, "options": options, "answer": idx, "category": "arithmetic"}


def _generate_subtraction():
    a = random.randint(30, 99)
    b = random.randint(10, a - 5)
    correct = a - b
    q = f"What is {a} − {b}?"
    options, idx = _make_options(correct)
    return {"question": q, "options": options, "answer": idx, "category": "arithmetic"}


def _generate_multiplication():
    # Include some trickier combos (single × double-digit)
    if random.random() < 0.4:
        a = random.randint(6, 25)
        b = random.randint(6, 25)
    else:
        a = random.randint(3, 12)
        b = random.randint(12, 30)
    correct = a * b
    q = f"What is {a} × {b}?"
    options, idx = _make_options(correct, spread=max(8, correct // 5))
    return {"question": q, "options": options, "answer": idx, "category": "arithmetic"}


def _generate_division():
    b = random.randint(3, 15)
    correct = random.randint(5, 25)
    a = b * correct
    q = f"What is {a} ÷ {b}?"
    options, idx = _make_options(correct)
    return {"question": q, "options": options, "answer": idx, "category": "arithmetic"}


def _generate_percentage():
    templates = [
        (10, [150, 250, 350, 450, 550, 700, 900]),
        (20, [75, 120, 180, 250, 350, 450]),
        (25, [60, 120, 160, 240, 320, 480]),
        (50, [30, 70, 110, 150, 250, 350]),
        (15, [100, 200, 300, 400, 600, 800]),
        (30, [50, 100, 150, 200, 300, 500]),
        (75, [40, 80, 120, 200, 320, 400]),
        (5, [200, 300, 400, 600, 800, 1000]),
        (40, [50, 100, 150, 200, 250]),
        (60, [50, 100, 150, 200, 250]),
    ]
    pct, bases = random.choice(templates)
    base = random.choice(bases)
    correct = int(base * pct / 100)
    q = f"What is {pct}% of {base}?"
    options, idx = _make_options(correct, spread=max(5, correct // 3))
    return {"question": q, "options": options, "answer": idx, "category": "percentages"}


def _generate_percentage_word():
    scenarios = [
        "A shirt costs ${base}. It's {pct}% off. How much do you save?",
        "You scored {pct}% on a test with {base} questions. How many did you get right?",
        "A pizza has {base} slices. You ate {pct}% of them. How many slices did you eat?",
        "A school has {base} students. {pct}% are absent today. How many are absent?",
        "A jar has {base} candies. You gave away {pct}%. How many did you give away?",
    ]
    pct = random.choice([5, 10, 15, 20, 25, 30, 40, 50, 75])
    base = random.choice([40, 60, 80, 100, 120, 150, 200, 250])
    template = random.choice(scenarios)
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
        ("3/8", "3/8", "3/4"), ("2/5", "2/5", "4/5"),
        ("3/4", "1/8", "7/8"), ("1/3", "1/6", "1/2"),
        ("5/8", "1/8", "3/4"), ("2/3", "1/3", "1"),
        ("3/10", "2/5", "7/10"), ("1/4", "1/8", "3/8"),
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
        ("1/2", 2, [30, 50, 70, 90, 110, 150]),
        ("1/3", 3, [21, 33, 42, 54, 66, 90]),
        ("1/4", 4, [24, 36, 48, 60, 80, 100]),
        ("2/3", 3, [18, 27, 36, 45, 60, 90]),
        ("3/4", 4, [20, 32, 44, 60, 80, 120]),
        ("1/5", 5, [25, 35, 45, 55, 75, 100]),
        ("2/5", 5, [20, 30, 45, 55, 75, 100]),
        ("3/5", 5, [25, 35, 50, 75, 100]),
        ("1/8", 8, [40, 56, 72, 96, 120]),
        ("3/8", 8, [40, 56, 72, 96, 120]),
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
    a = random.choice([49, 51, 99, 101, 198, 202, 301, 499, 501, 748, 997])
    b = random.randint(3, 12)
    correct = a * b
    q = f"Estimate: {a} × {b} is closest to?"
    spread = max(80, correct // 5)
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
        ("About how many hours are in a month (30 days)?", 720, 100),
        ("About how many seconds are in 1 day?", 86400, 10000),
        ("About how many minutes are in 1 week?", 10080, 1500),
        ("About how many hours are in 3 days?", 72, 12),
        ("About how many days are in 10 years?", 3650, 400),
    ]
    q_text, correct, spread = random.choice(questions)
    options, idx = _make_options(correct, spread=spread)
    return {"question": q_text, "options": options, "answer": idx, "category": "estimation"}


def _est_closest():
    a = random.randint(200, 1500)
    b = random.randint(200, 1500)
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
    price = random.choice([12, 18, 24, 35, 45, 55, 65, 78, 95])
    qty = random.randint(3, 7)
    correct = price * qty
    q = f"A {item} costs ${price}. How much do {qty} cost?"
    options, idx = _make_options(correct, spread=max(10, correct // 4))
    options = [f"${o}" if isinstance(o, int) else o for o in options]
    str_correct = f"${correct}"
    idx = options.index(str_correct)
    return {"question": q, "options": options, "answer": idx, "category": "word_problems"}


def _wp_sharing():
    total = random.choice([42, 56, 72, 84, 96, 108, 120, 144])
    people = random.choice([3, 4, 6, 7, 8, 9, 12])
    while total % people != 0:
        people = random.choice([3, 4, 6, 7, 8, 9, 12])
    correct = total // people
    item = random.choice(["stickers", "cards", "candies", "marbles", "pencils"])
    q = f"You have {total} {item} to share equally among {people} friends. How many does each get?"
    options, idx = _make_options(correct)
    return {"question": q, "options": options, "answer": idx, "category": "word_problems"}


def _wp_speed():
    speed = random.choice([35, 45, 55, 65, 72, 85])
    hours = random.choice([2, 3, 4, 5, 6])
    correct = speed * hours
    q = f"A car drives at {speed} mph for {hours} hours. How far does it go?"
    options, idx = _make_options(correct, spread=max(20, correct // 4))
    options = [f"{o} miles" for o in options]
    str_correct = f"{correct} miles"
    idx = options.index(str_correct)
    return {"question": q, "options": options, "answer": idx, "category": "word_problems"}


def _wp_money_left():
    start = random.choice([50, 100, 150, 200])
    items = random.randint(3, 5)
    costs = [random.randint(5, start // (items + 1)) for _ in range(items)]
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
    l = random.randint(5, 25)
    w = random.randint(5, 25)
    correct = l * w
    shape = "rectangle" if l != w else "square"
    q = f"A {shape} is {l} feet long and {w} feet wide. What is its area?"
    options, idx = _make_options(correct, spread=max(5, correct // 4))
    options = [f"{o} sq ft" for o in options]
    str_correct = f"{correct} sq ft"
    idx = options.index(str_correct)
    return {"question": q, "options": options, "answer": idx, "category": "word_problems"}


def _generate_squares():
    n = random.randint(2, 15)
    correct = n * n
    q = f"What is {n}²?"
    options, idx = _make_options(correct, spread=max(5, correct // 4))
    return {"question": q, "options": options, "answer": idx, "category": "powers"}


def _generate_cubes():
    n = random.randint(2, 8)
    correct = n ** 3
    q = f"What is {n}³?"
    options, idx = _make_options(correct, spread=max(10, correct // 4))
    return {"question": q, "options": options, "answer": idx, "category": "powers"}


def _generate_power_of_two():
    exp = random.randint(2, 10)
    correct = 2 ** exp
    q = f"What is 2 to the power of {exp}?"
    options, idx = _make_options(correct, spread=max(8, correct // 4))
    return {"question": q, "options": options, "answer": idx, "category": "powers"}


def _generate_power_of_ten():
    exp = random.randint(2, 6)
    correct = 10 ** exp
    q = f"What is 10 to the power of {exp}?"
    spread = correct // 5
    options, idx = _make_options(correct, spread=max(50, spread))
    return {"question": q, "options": options, "answer": idx, "category": "powers"}


def _generate_square_root():
    perfect_squares = [4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144]
    n = random.choice(perfect_squares)
    correct = int(n ** 0.5)
    q = f"What is the square root of {n}?"
    options, idx = _make_options(correct, spread=3)
    return {"question": q, "options": options, "answer": idx, "category": "powers"}


def _generate_exponent_compare():
    pairs = [
        (2, 5, 3, 3), (3, 3, 2, 5), (2, 4, 4, 2),
        (5, 2, 3, 3), (2, 6, 4, 3), (3, 4, 9, 2),
        (2, 3, 3, 2), (5, 3, 2, 7), (10, 2, 2, 7),
    ]
    base1, exp1, base2, exp2 = random.choice(pairs)
    val1 = base1 ** exp1
    val2 = base2 ** exp2
    if val1 > val2:
        correct = f"{base1}^{exp1}"
        other = f"{base2}^{exp2}"
    elif val2 > val1:
        correct = f"{base2}^{exp2}"
        other = f"{base1}^{exp1}"
    else:
        correct = "They are equal"
        other = None

    q = f"Which is bigger: {base1}^{exp1} or {base2}^{exp2}?"

    if other:
        options = [
            f"{base1}^{exp1} = {val1}",
            f"{base2}^{exp2} = {val2}",
            "They are equal",
            f"Can't tell",
        ]
        if val1 > val2:
            answer_idx = 0
        else:
            answer_idx = 1
    else:
        options = [
            f"{base1}^{exp1} = {val1}",
            f"{base2}^{exp2} = {val2}",
            f"They are equal ({val1})",
            "Can't tell",
        ]
        answer_idx = 2

    random.shuffle(options)
    answer_idx = options.index([o for o in options if str(correct) in o or (correct == "They are equal" and "equal" in o)][0])
    return {"question": q, "options": options, "answer": answer_idx, "category": "powers"}


def _generate_power_word():
    templates = [
        lambda: _pw_bacteria(),
        lambda: _pw_doubling(),
        lambda: _pw_area(),
    ]
    return random.choice(templates)()


def _pw_bacteria():
    hours = random.randint(2, 6)
    correct = 2 ** hours
    q = f"Bacteria double every hour. Starting with 1, how many after {hours} hours?"
    options, idx = _make_options(correct, spread=max(3, correct // 3))
    return {"question": q, "options": options, "answer": idx, "category": "powers"}


def _pw_doubling():
    days = random.randint(3, 7)
    correct = 2 ** days
    q = f"You save 1 penny on day 1 and double it each day. How many pennies on day {days}?"
    options, idx = _make_options(correct, spread=max(5, correct // 3))
    return {"question": q, "options": options, "answer": idx, "category": "powers"}


def _pw_area():
    side = random.randint(3, 12)
    correct = side ** 2
    q = f"A square has sides of {side} cm. What is its area in cm²?"
    options, idx = _make_options(correct, spread=max(5, correct // 4))
    return {"question": q, "options": options, "answer": idx, "category": "powers"}


def _generate_simplify_ratio():
    gcd_val = random.randint(2, 6)
    a = random.randint(1, 8)
    b = random.randint(1, 8)
    while a == b:
        b = random.randint(1, 8)
    q = f"Simplify the ratio {a * gcd_val} : {b * gcd_val}"
    correct = f"{a}:{b}"
    wrong1 = f"{a + 1}:{b}"
    wrong2 = f"{a}:{b + 1}"
    wrong3 = f"{b}:{a}"
    options = [correct, wrong1, wrong2, wrong3]
    random.shuffle(options)
    idx = options.index(correct)
    return {"question": q, "options": options, "answer": idx, "category": "ratios"}


def _generate_missing_proportion():
    a = random.randint(2, 10)
    b = random.randint(2, 10)
    multiplier = random.randint(2, 5)
    c = a * multiplier
    correct = b * multiplier
    q = f"If {a} : {b} = {c} : ?, what is the missing number?"
    options, idx = _make_options(correct, spread=max(3, correct // 3))
    return {"question": q, "options": options, "answer": idx, "category": "ratios"}


def _generate_ratio_to_fraction():
    a = random.randint(1, 6)
    b = random.randint(1, 6)
    while a == b:
        b = random.randint(1, 6)
    total = a + b
    q = f"In the ratio {a}:{b}, what fraction of the total is the first part?"
    correct = f"{a}/{total}"
    wrong1 = f"{b}/{total}"
    wrong2 = f"{a}/{b}"
    wrong3 = f"{total}/{a}"
    options = [correct, wrong1, wrong2, wrong3]
    random.shuffle(options)
    idx = options.index(correct)
    return {"question": q, "options": options, "answer": idx, "category": "ratios"}


def _generate_ratio_share():
    a = random.randint(1, 5)
    b = random.randint(1, 5)
    while a == b:
        b = random.randint(1, 5)
    total_parts = a + b
    total_amount = total_parts * random.randint(3, 10)
    per_part = total_amount // total_parts
    who = random.choice(["first", "second"])
    correct = per_part * (a if who == "first" else b)
    q = f"${total_amount} is shared in the ratio {a}:{b}. How much does the {who} person get?"
    options, idx = _make_options(correct, spread=max(3, per_part))
    return {"question": q, "options": options, "answer": idx, "category": "ratios"}


def _generate_unit_rate():
    items = random.randint(3, 8)
    price_per = random.randint(2, 9)
    total_price = items * price_per
    q = f"If {items} apples cost ${total_price}, how much does 1 apple cost?"
    correct = price_per
    options, idx = _make_options(correct, spread=3)
    return {"question": q, "options": options, "answer": idx, "category": "ratios"}


def _generate_proportion_word():
    templates = [
        lambda: _rpw_recipe(),
        lambda: _rpw_speed(),
        lambda: _rpw_map(),
    ]
    return random.choice(templates)()


def _rpw_recipe():
    base_cups = random.randint(2, 4)
    base_cookies = random.randint(10, 20)
    multiplier = random.randint(2, 4)
    target_cups = base_cups * multiplier
    correct = base_cookies * multiplier
    q = f"A recipe uses {base_cups} cups of flour for {base_cookies} cookies. How many cookies with {target_cups} cups?"
    options, idx = _make_options(correct, spread=max(5, correct // 4))
    return {"question": q, "options": options, "answer": idx, "category": "ratios"}


def _rpw_speed():
    speed = random.choice([30, 40, 50, 60])
    hours = random.randint(2, 5)
    correct = speed * hours
    q = f"A car travels at {speed} mph. How far does it go in {hours} hours?"
    options, idx = _make_options(correct, spread=max(10, correct // 5))
    return {"question": q, "options": options, "answer": idx, "category": "ratios"}


def _rpw_map():
    scale_cm = 1
    scale_km = random.choice([5, 10, 20, 25, 50])
    map_dist = random.randint(2, 8)
    correct = scale_km * map_dist
    q = f"On a map, {scale_cm} cm = {scale_km} km. What real distance is {map_dist} cm?"
    options, idx = _make_options(correct, spread=max(10, correct // 4))
    return {"question": q, "options": options, "answer": idx, "category": "ratios"}


# --- Constant of proportionality (y = kx, SpringBoard proportional relationships) ---


def _generate_k_from_xy():
    """Find k given one (x, y) pair on y = kx."""
    k = random.randint(2, 15)
    x = random.randint(2, 12)
    y = k * x
    q = f"In a proportional relationship y = kx, when x = {x}, y = {y}. What is k? (k = y ÷ x)"
    options, idx = _make_options(k, spread=max(2, k // 3))
    return {"question": q, "options": options, "answer": idx, "category": "proportionality"}


def _generate_y_from_kx():
    """Find y given k and x."""
    k = random.randint(2, 12)
    x = random.randint(3, 16)
    correct = k * x
    q = f"If y = kx and k = {k} and x = {x}, what is y?"
    options, idx = _make_options(correct, spread=max(5, correct // 4))
    return {"question": q, "options": options, "answer": idx, "category": "proportionality"}


def _generate_x_from_ky():
    """Find x given k and y (y = kx)."""
    k = random.randint(2, 12)
    x = random.randint(3, 15)
    y = k * x
    q = f"If y = kx and k = {k} and y = {y}, what is x?"
    options, idx = _make_options(x, spread=max(3, x // 3))
    return {"question": q, "options": options, "answer": idx, "category": "proportionality"}


def _generate_k_word():
    """Constant of proportionality in a short context (unit rate form)."""
    k = random.randint(3, 12)
    x = random.randint(2, 8)
    y = k * x
    templates = [
        "You earn ${y} in {x} hours at the same rate each hour. What is k (dollars per hour)?",
        "A recipe scales: {y} cups of sugar for {x} batches. Sugar is proportional to batches. What is k (cups per batch)?",
        "A plant grows {y} cm in {x} weeks. Height is proportional to time. What is k (cm per week)?",
        "You walk {y} miles in {x} hours at a steady pace. What is k (miles per hour)?",
    ]
    q = random.choice(templates).format(y=y, x=x)
    options, idx = _make_options(k, spread=max(2, k // 3))
    return {"question": q, "options": options, "answer": idx, "category": "proportionality"}


def _generate_table_k():
    """Second row of a simple table: x₁,y₁ and x₂ known, find y₂ using k = y₁/x₁."""
    k = random.randint(2, 10)
    x1 = random.randint(2, 6)
    y1 = k * x1
    x2 = random.randint(7, 18)
    correct = k * x2
    q = (
        f"x and y are proportional. When x = {x1}, y = {y1}. "
        f"When x = {x2}, what is y?"
    )
    options, idx = _make_options(correct, spread=max(5, correct // 4))
    return {"question": q, "options": options, "answer": idx, "category": "proportionality"}


# --- Solving basic one-variable equations ---


def _generate_eq_one_step_add():
    """x + a = b  →  x = b - a"""
    x = random.randint(2, 50)
    a = random.randint(2, 30)
    b = x + a
    q = f"Solve for x:  x + {a} = {b}"
    options, idx = _make_options(x, spread=max(3, a // 2))
    return {"question": q, "options": options, "answer": idx, "category": "equations"}


def _generate_eq_one_step_sub():
    """x - a = b  →  x = b + a"""
    x = random.randint(10, 60)
    a = random.randint(2, x - 1)
    b = x - a
    q = f"Solve for x:  x − {a} = {b}"
    options, idx = _make_options(x, spread=max(3, a // 2))
    return {"question": q, "options": options, "answer": idx, "category": "equations"}


def _generate_eq_one_step_mult():
    """a · x = b  →  x = b / a"""
    x = random.randint(2, 20)
    a = random.randint(2, 12)
    b = a * x
    q = f"Solve for x:  {a}x = {b}"
    options, idx = _make_options(x, spread=max(2, x // 3))
    return {"question": q, "options": options, "answer": idx, "category": "equations"}


def _generate_eq_one_step_div():
    """x / a = b  →  x = a · b"""
    b = random.randint(2, 15)
    a = random.randint(2, 10)
    x = a * b
    q = f"Solve for x:  x ÷ {a} = {b}"
    options, idx = _make_options(x, spread=max(3, x // 4))
    return {"question": q, "options": options, "answer": idx, "category": "equations"}


def _generate_eq_two_step():
    """ax + b = c  →  x = (c - b) / a"""
    x = random.randint(2, 15)
    a = random.randint(2, 8)
    b = random.randint(1, 20)
    c = a * x + b
    q = f"Solve for x:  {a}x + {b} = {c}"
    options, idx = _make_options(x, spread=max(2, x // 2))
    return {"question": q, "options": options, "answer": idx, "category": "equations"}


def _generate_eq_two_step_sub():
    """ax - b = c  →  x = (c + b) / a"""
    x = random.randint(3, 15)
    a = random.randint(2, 8)
    b = random.randint(1, 15)
    c = a * x - b
    if c < 0:
        c = a * x + b
        q = f"Solve for x:  {a}x + {b} = {c + 2 * b}"
        options, idx = _make_options(x, spread=max(2, x // 2))
        return {"question": q, "options": options, "answer": idx, "category": "equations"}
    q = f"Solve for x:  {a}x − {b} = {c}"
    options, idx = _make_options(x, spread=max(2, x // 2))
    return {"question": q, "options": options, "answer": idx, "category": "equations"}


def _generate_eq_word():
    """Simple equation word problem."""
    x = random.randint(3, 20)
    templates = []

    a = random.randint(2, 6)
    b = random.randint(5, 25)
    total = a * x + b
    templates.append(
        (f"A number is multiplied by {a}, then {b} is added. "
         f"The result is {total}. What is the number?", x)
    )

    saved = random.randint(5, 15)
    weeks = x
    goal = saved * weeks + random.randint(10, 50)
    start = goal - saved * weeks
    templates.append(
        (f"You save ${saved} each week and already have ${start}. "
         f"After how many weeks will you have ${goal}?", weeks)
    )

    q, correct = random.choice(templates)
    options, idx = _make_options(correct, spread=max(2, correct // 3))
    return {"question": q, "options": options, "answer": idx, "category": "equations"}


# --- Distributive property: a(b + c), a(b - c), expand & simplify ---


def _generate_dist_expand_add():
    """a(b + c) = ab + ac"""
    a = random.randint(2, 12)
    b = random.randint(1, 15)
    c = random.randint(1, 15)
    correct = a * b + a * c
    q = f"Use the distributive property to expand:  {a}({b} + {c})"
    options, idx = _make_options(correct, spread=max(5, correct // 4))
    return {"question": q, "options": options, "answer": idx, "category": "distributive"}


def _generate_dist_expand_sub():
    """a(b - c) = ab - ac, ensure b > c so result is positive."""
    a = random.randint(2, 12)
    b = random.randint(5, 20)
    c = random.randint(1, b - 1)
    correct = a * b - a * c
    q = f"Use the distributive property to expand:  {a}({b} − {c})"
    options, idx = _make_options(correct, spread=max(5, correct // 4))
    return {"question": q, "options": options, "answer": idx, "category": "distributive"}


def _generate_dist_fill_blank():
    """a(b + c) = a·b + a·?  →  find the missing piece."""
    a = random.randint(2, 10)
    b = random.randint(2, 12)
    c = random.randint(2, 12)
    product_ac = a * c
    q = f"{a}({b} + {c}) = {a}×{b} + {a}×__. What goes in the blank?"
    options, idx = _make_options(c, spread=max(2, c // 2))
    return {"question": q, "options": options, "answer": idx, "category": "distributive"}


def _generate_dist_reverse():
    """Given ab + ac, factor out a → a(b + c). Find a."""
    a = random.randint(2, 10)
    b = random.randint(2, 12)
    c = random.randint(2, 12)
    ab = a * b
    ac = a * c
    q = f"Factor:  {ab} + {ac} = __(  {b} + {c}  ). What number goes in the blank?"
    options, idx = _make_options(a, spread=max(2, a // 2))
    return {"question": q, "options": options, "answer": idx, "category": "distributive"}


def _generate_dist_mental_trick():
    """Use distributive property as a mental math shortcut, e.g. 7 × 98 = 7(100-2)."""
    a = random.randint(3, 9)
    base = random.choice([10, 20, 50, 100])
    offset = random.randint(1, 3)
    sign = random.choice([-1, 1])
    num = base + sign * offset
    correct = a * num
    if sign == 1:
        hint = f"{a} × {num}  (think: {a}×{base} + {a}×{offset})"
    else:
        hint = f"{a} × {num}  (think: {a}×{base} − {a}×{offset})"
    q = f"Use the distributive property to compute:  {hint}"
    options, idx = _make_options(correct, spread=max(5, correct // 5))
    return {"question": q, "options": options, "answer": idx, "category": "distributive"}


def _generate_dist_word():
    """Word problem using distributive property."""
    a = random.randint(3, 8)
    b = random.randint(5, 15)
    c = random.randint(2, 10)
    correct = a * (b + c)
    templates = [
        f"You buy {a} packs. Each pack has {b} red and {c} blue marbles. How many marbles total?",
        f"There are {a} classrooms with {b} boys and {c} girls each. How many students total?",
        f"A baker makes {a} batches with {b} cookies and {c} brownies per batch. Total treats?",
    ]
    q = random.choice(templates)
    options, idx = _make_options(correct, spread=max(5, correct // 4))
    return {"question": q, "options": options, "answer": idx, "category": "distributive"}


_GENERATORS = {
    "percentages": [_generate_percentage, _generate_percentage_word],
    "fractions": [_generate_fraction_addition, _generate_fraction_of, _generate_fraction_remaining],
    "word_problems": [_generate_word_problem],
    "powers": [_generate_squares, _generate_cubes, _generate_power_of_two, _generate_power_of_ten, _generate_square_root, _generate_exponent_compare, _generate_power_word],
    "ratios": [_generate_simplify_ratio, _generate_missing_proportion, _generate_ratio_to_fraction, _generate_ratio_share, _generate_unit_rate, _generate_proportion_word],
    "proportionality": [
        _generate_k_from_xy,
        _generate_y_from_kx,
        _generate_x_from_ky,
        _generate_k_word,
        _generate_table_k,
    ],
    "distributive": [
        _generate_dist_expand_add,
        _generate_dist_expand_sub,
        _generate_dist_fill_blank,
        _generate_dist_reverse,
        _generate_dist_mental_trick,
        _generate_dist_word,
    ],
    "equations": [
        _generate_eq_one_step_add,
        _generate_eq_one_step_sub,
        _generate_eq_one_step_mult,
        _generate_eq_one_step_div,
        _generate_eq_two_step,
        _generate_eq_two_step_sub,
        _generate_eq_word,
    ],
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
