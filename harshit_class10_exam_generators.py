"""MCQ generators for CBSE Class 10 board-exam question types (units 1–12)."""

from __future__ import annotations

import math
import random

import harshit_class10_exam_types as h10et
import harshit_class10_topics as h10t

# Re-export helpers used throughout generators.
_mcq = h10t._mcq
_shuffle_options = h10t._shuffle_options
_variant_mcq = h10t._variant_mcq
_random_quadratic = h10t._random_quadratic
_poly_quadratic = h10t._poly_quadratic
_lin_eq = h10t._lin_eq
_random_lin_sys = h10t._random_lin_sys
_ap_nth = h10t._ap_nth
_ap_sum = h10t._ap_sum
_random_ap = h10t._random_ap
_coord_dist = h10t._coord_dist
_section_point = h10t._section_point
_sector_area = h10t._sector_area
_arc_length = h10t._arc_length
_bpt_ec = h10t._bpt_ec
_tangent_pairs = h10t._tangent_pairs
_nature_from_disc = h10t._nature_from_disc
_quad_std = h10t._quad_std
_factor_string = h10t._factor_string
_random_bpt_segments = h10t._random_bpt_segments
_random_right_triangle = h10t._random_right_triangle
_parallel_sys = h10t._parallel_sys
_coincident_sys = h10t._coincident_sys
_ap_terms_str = h10t._ap_terms_str
_eval_poly = h10t._eval_poly
_surd_zeroes_mcq = h10t._surd_zeroes_mcq
_random_surd_conjugate_zeroes = h10t._random_surd_conjugate_zeroes
_fmt_surd_zero = h10t._fmt_surd_zero
_cubic_factor_mcq = h10t._cubic_factor_mcq
_u1_multistep_mcq = h10t._u1_multistep_mcq
_u3_multistep_mcq = h10t._u3_multistep_mcq
_STD_TRIG = h10t._STD_TRIG  # noqa: SLF001


def _et(exam_type_id: str) -> h10et.ExamType:
    return h10et.EXAM_TYPE_BY_ID[exam_type_id]


def _slot(exam_type_id: str) -> tuple[int, int, str]:
    et = _et(exam_type_id)
    return et.unit_id, et.topic_id, et.level


def _make(exam_type_id: str, q: dict) -> dict:
    out = dict(q)
    out["exam_type"] = exam_type_id
    out["source"] = "exam_template"
    return out


def _exam_mcq(exam_type_id: str, question: str, correct: str, wrong: list[str], expl: str = "") -> dict:
    u, t, l = _slot(exam_type_id)
    opts, ans = _shuffle_options(correct, wrong)
    return _make(exam_type_id, _mcq(u, t, l, question, opts, ans, expl))


def _exam_variant(exam_type_id: str, variants: list[tuple[str, str, list[str], str]]) -> dict:
    u, t, l = _slot(exam_type_id)
    return _make(exam_type_id, _variant_mcq(u, t, l, variants))


# ── Unit 1 — Real Numbers ──


def _gen_u1_euclid_hcf() -> dict:
    pairs = [(135, 225), (867, 255), (4052, 1936), (96, 404)]
    a, b = random.choice(pairs) if random.random() < 0.4 else sorted(
        [random.randint(60, 400), random.randint(60, 400)], reverse=True
    )
    hcf = math.gcd(a, b)
    return _exam_mcq(
        "u1_euclid_hcf",
        f"Using Euclid's division algorithm, HCF({a}, {b}) = ?",
        str(hcf),
        [str(a + b), str(a * b // hcf if hcf else a), str(hcf + 3)],
        f"Repeated division until remainder 0 gives HCF = {hcf}.",
    )


def _gen_u1_hcf_lcm_prime() -> dict:
    a, b = random.choice([(96, 404), (140, 156), (180, 225), (26, 91)])
    if random.random() < 0.5:
        a, b = random.randint(24, 180), random.randint(24, 180)
    hcf, lcm = math.gcd(a, b), a * b // math.gcd(a, b)
    if random.random() < 0.5:
        q, ans = f"HCF({a}, {b}) by prime factorisation = ?", str(hcf)
        wrong = [str(lcm), str(a + b), str(hcf + 2)]
    else:
        q, ans = f"LCM({a}, {b}) by prime factorisation = ?", str(lcm)
        wrong = [str(hcf), str(a * b), str(lcm + 4)]
    return _exam_mcq("u1_hcf_lcm_prime", q, ans, wrong)


def _gen_u1_sqrt_irrational(root: int, exam_id: str) -> dict:
    sym = f"√{root}"
    return _exam_variant(exam_id, [
        (
            f"Proof that {sym} is irrational begins by:",
            f"Assume {sym} is rational (= p/q in lowest terms)",
            [f"Assume {sym} is irrational", "Square both sides first", "Set p = q"],
            "Proof by contradiction: assume rational, derive p | q² ⇒ p | q.",
        ),
        (
            f"After assuming {sym} = p/q (lowest terms), squaring gives:",
            f"p² = {root}q², so {root} divides p²",
            ["p² = q²", f"q² = {root}p²", "p = q"],
            f"Then {root} | p, contradicting lowest terms unless p, q share a factor.",
        ),
        (
            f"Which conclusion follows in the proof that {sym} is irrational?",
            f"{sym} is irrational",
            [f"{sym} is rational", f"{root} is composite", f"{sym} = {root}/2"],
            "",
        ),
    ])


def _gen_u1_sqrt2_irrational() -> dict:
    return _gen_u1_sqrt_irrational(2, "u1_sqrt2_irrational")


def _gen_u1_sqrt3_irrational() -> dict:
    return _gen_u1_sqrt_irrational(3, "u1_sqrt3_irrational")


def _gen_u1_sqrt5_irrational() -> dict:
    return _gen_u1_sqrt_irrational(5, "u1_sqrt5_irrational")


def _gen_u1_sum_irrational() -> dict:
    a, b = random.choice([(3, 5), (5, 3), (2, 7), (4, 6)])
    expr = f"{a} + {random.randint(1, 4)}√{b}"
    return _exam_mcq(
        "u1_sum_irrational",
        f"Which is correct about {expr}?",
        f"{expr} is irrational",
        [f"{expr} is rational", f"√{b} is rational", "Sum of two rationals is irrational"],
        "Assuming rational leads to √ being rational — contradiction.",
    )


def _gen_u1_hcf_from_product_lcm() -> dict:
    a, b = random.randint(12, 80), random.randint(12, 80)
    hcf = math.gcd(a, b)
    product, lcm = a * b, a * b // hcf
    return _exam_mcq(
        "u1_hcf_from_product_lcm",
        f"Two numbers have product {product} and LCM {lcm}. Their HCF = ?",
        str(hcf),
        [str(lcm), str(product // lcm if lcm else hcf + 1), str(hcf + 4)],
        "HCF × LCM = product for two positive integers.",
    )


def _gen_u1_hcf_lcm_pairs() -> dict:
    hcf, lcm = random.choice([(12, 420), (6, 180), (8, 240), (15, 300)])
    a = hcf * random.choice([2, 3, 4, 5, 7])
    b = lcm * hcf // a
    while math.gcd(a, b) != hcf or a * b // math.gcd(a, b) != lcm:
        a = hcf * random.randint(2, 12)
        b = lcm * hcf // a
    return _exam_mcq(
        "u1_hcf_lcm_pairs",
        f"If HCF(a, b) = {hcf} and LCM(a, b) = {lcm}, one possible pair (a, b) is:",
        f"({a}, {b})",
        [f"({a + hcf}, {b})", f"({hcf}, {lcm})", f"({a}, {b + hcf})"],
        f"Check: gcd({a},{b})={hcf}, lcm={lcm}.",
    )


def _gen_u1_euclid_first_remainder() -> dict:
    return _make(
        "u1_euclid_first_remainder",
        _u1_multistep_mcq(1, 2, "D", step="euclid_r1", canonical=random.random() < 0.35),
    )


def _gen_u1_prime_factor_step() -> dict:
    return _make(
        "u1_prime_factor_step",
        _u1_multistep_mcq(1, 2, "B", step="prime_factor_a", canonical=random.random() < 0.35),
    )


def _gen_u1_prime_hcf_step() -> dict:
    return _make(
        "u1_prime_hcf_step",
        _u1_multistep_mcq(1, 2, "B", step="prime_hcf", canonical=random.random() < 0.35),
    )


def _gen_u1_prime_lcm_step() -> dict:
    return _make(
        "u1_prime_lcm_step",
        _u1_multistep_mcq(1, 2, "C", step="prime_lcm", canonical=random.random() < 0.35),
    )


def _gen_u1_hcf_lcm_pair_step() -> dict:
    return _make(
        "u1_hcf_lcm_pair_step",
        _u1_multistep_mcq(1, 2, "E", step="hcf_lcm_pair"),
    )


def _gen_u1_irrational_assume_step() -> dict:
    return _make(
        "u1_irrational_assume_step",
        _u1_multistep_mcq(1, 3, "D", step="irrational_assume", canonical=random.random() < 0.25),
    )


def _gen_u1_irrational_contradiction_step() -> dict:
    return _make(
        "u1_irrational_contradiction_step",
        _u1_multistep_mcq(1, 3, "D", step="irrational_contradiction", canonical=random.random() < 0.25),
    )


# ── Unit 2 — Polynomials ──


def _gen_u2_zeroes_verify() -> dict:
    r1, r2, b, c = _random_quadratic()
    poly = _poly_quadratic(b, c)
    sum_z, prod_z = r1 + r2, r1 * r2
    return _exam_mcq(
        "u2_zeroes_verify",
        f"Zeroes of p(x) = {poly} are {r1} and {r2}. Verify: sum = −b and product = c gives:",
        f"sum = {sum_z}, product = {prod_z}",
        [f"sum = {prod_z}, product = {sum_z}", f"sum = {b}, product = {c}", f"sum = {sum_z + 1}, product = {prod_z}"],
        f"For x² + bx + c: sum = −b = {sum_z}, product = c = {prod_z}.",
    )


def _gen_u2_alpha_beta_sum() -> dict:
    a_coef = random.choice([1, 2, 3])
    r1, r2 = random.randint(-5, 5), random.randint(-5, 5)
    b, c = -a_coef * (r1 + r2), a_coef * r1 * r2
    poly = _poly_quadratic(b, c, a_coef)
    s, p = r1 + r2, r1 * r2
    return _exam_mcq(
        "u2_alpha_beta_sum",
        f"If α, β are zeroes of p(x) = {poly}, then α + β and αβ are:",
        f"{s} and {p}",
        [f"{p} and {s}", f"{-s} and {p}", f"{s} and {-p}"],
        f"α + β = −b/a = {s}; αβ = c/a = {p}.",
    )


def _gen_u2_form_from_zeroes() -> dict:
    if random.random() < 0.35:
        return _make("u2_form_from_zeroes", _surd_zeroes_mcq(2, 3, "C", step="polynomial"))
    z1, z2 = random.randint(-6, 6), random.randint(-6, 6)
    while z1 == z2:
        z2 = random.randint(-6, 6)
    correct = _poly_quadratic(-(z1 + z2), z1 * z2)
    wrong = [_poly_quadratic(z1 + z2, z1 * z2), _poly_quadratic(-(z1 + z2), -z1 * z2), _poly_quadratic(z1, z2)]
    return _exam_mcq(
        "u2_form_from_zeroes",
        f"A quadratic polynomial with zeroes {z1} and {z2} is:",
        correct,
        wrong,
        "Use x² − (sum)x + (product).",
    )


def _gen_u2_find_k_one_zero() -> dict:
    r1 = random.randint(2, 6)
    r2 = random.randint(-5, 5)
    while r2 == r1:
        r2 = random.randint(-5, 5)
    a = random.choice([1, 2])
    k = -a * (r1 + r2)
    c = a * r1 * r2
    return _exam_mcq(
        "u2_find_k_one_zero",
        f"If one zero of {a}x² + kx + {c} is {r1}, then k and the other zero are:",
        f"k = {k}, other zero = {r2}",
        [f"k = {-k}, other zero = {r2}", f"k = {k}, other zero = {r1}", f"k = {c}, other zero = {r2}"],
        f"Sum of zeroes = −k/a ⇒ k = {k}; product gives other zero {r2}.",
    )


def _gen_u2_equal_zeroes_k() -> dict:
    r = random.randint(2, 7)
    k = 2 * r
    return _exam_mcq(
        "u2_equal_zeroes_k",
        f"Zeroes of x² − (k + 3)x + k are equal. Then k = ?",
        str(k),
        [str(k + 2), str(r), str(k - 1)],
        f"Equal zeroes ⇒ Δ = 0 ⇒ (k+3)² = 4k ⇒ k = {k}.",
    )


def _gen_u2_form_sum_product() -> dict:
    s, p = random.randint(-8, 8), random.randint(-12, 12)
    correct = _poly_quadratic(-s, p)
    return _exam_mcq(
        "u2_form_sum_product",
        f"Quadratic with sum of zeroes {s} and product {p}:",
        correct,
        [_poly_quadratic(s, p), _poly_quadratic(-s, -p), _poly_quadratic(s, -p)],
        "Standard form: x² − (sum)x + (product).",
    )


def _gen_u2_graphical_zeroes() -> dict:
    r1, r2, b, c = _random_quadratic()
    count = 2 if r1 != r2 else 1
    poly = _poly_quadratic(b, c)
    return _exam_mcq(
        "u2_graphical_zeroes",
        f"Graph of p(x) = {poly} meets the x-axis at:",
        f"{count} point(s) — zeroes {r1}" + (f" and {r2}" if r1 != r2 else " (repeated)"),
        ["0 points", "3 points", "Infinitely many points"],
        "x-intercepts correspond to zeroes.",
    )


def _gen_u2_zeroes_x2_7x_12() -> dict:
    r1, r2, b, c = (3, 4, -7, 12) if random.random() < 0.3 else _random_quadratic()
    poly = _poly_quadratic(b, c)
    return _exam_mcq(
        "u2_zeroes_x2_7x_12",
        f"Zeroes of p(x) = {poly} are {r1} and {r2}. Verify α + β = −b and αβ = c:",
        f"α + β = {r1 + r2} = −({b}); αβ = {r1 * r2} = {c}",
        [f"α + β = {c}; αβ = {b}", f"α + β = {b}; αβ = {c}", "Relations do not hold"],
        "NCERT Ex 2.2 style verification.",
    )


def _gen_u2_surd_zero_polynomial() -> dict:
    if random.random() < 0.25:
        a, b, rad, s, p = 5, 2, 3, 10, 13
    else:
        a, b, rad, s, p = _random_surd_conjugate_zeroes()
    z_minus = _fmt_surd_zero(a, b, rad, plus=False)
    z_plus = _fmt_surd_zero(a, b, rad, plus=True)
    correct = _poly_quadratic(-s, p)
    wrong_product = a * a + b * b * rad
    return _exam_mcq(
        "u2_surd_zero_polynomial",
        f"Find a quadratic polynomial whose zeroes are {z_minus} and {z_plus}.",
        correct,
        [_poly_quadratic(s, p), _poly_quadratic(-s, wrong_product), _poly_quadratic(-(s + 1), p)],
        (
            f"Step 1: sum α+β = {s}. Step 2: product = {a}² − ({b}√{rad})² = {a * a} − {b * b * rad} = {p}. "
            f"Step 3: x² − (sum)x + (product) = {correct}."
        ),
    )


def _gen_u2_surd_zero_product() -> dict:
    return _make("u2_surd_zero_product", _surd_zeroes_mcq(2, 3, "D", step="product"))


def _gen_u2_surd_zero_sum() -> dict:
    return _make("u2_surd_zero_sum", _surd_zeroes_mcq(2, 3, "C", step="sum"))


def _gen_u2_cubic_factor_all_zeroes() -> dict:
    canonical = random.random() < 0.3
    return _make(
        "u2_cubic_factor_all_zeroes",
        _cubic_factor_mcq(2, 4, "E", step="all_zeroes", canonical=canonical),
    )


def _gen_u2_cubic_factor_quotient() -> dict:
    return _make(
        "u2_cubic_factor_quotient",
        _cubic_factor_mcq(2, 4, "E", step="quotient", canonical=random.random() < 0.25),
    )


def _gen_u2_cubic_verify_quadratic() -> dict:
    step = random.choice(["quad_sum", "quad_product"])
    return _make(
        "u2_cubic_verify_quadratic",
        _cubic_factor_mcq(2, 4, "E", step=step, canonical=random.random() < 0.25),
    )


# ── Unit 3 — Pair of Linear Equations ──


def _gen_u3_substitution() -> dict:
    x, y, (a1, b1, c1), (a2, b2, c2) = _random_lin_sys()
    eq1, eq2 = _lin_eq(a1, b1, c1), _lin_eq(a2, b2, c2)
    return _exam_mcq(
        "u3_substitution",
        f"Solve by substitution: {eq1} and {eq2}. Solution:",
        f"x = {x}, y = {y}",
        [f"x = {y}, y = {x}", f"x = {x + 1}, y = {y}", f"x = {x}, y = {y + 1}"],
        "Express one variable and substitute into the second equation.",
    )


def _gen_u3_elimination() -> dict:
    x, y, (a1, b1, c1), (a2, b2, c2) = _random_lin_sys()
    return _exam_mcq(
        "u3_elimination",
        f"Solve by elimination: {_lin_eq(a1, b1, c1)} and {_lin_eq(a2, b2, c2)}:",
        f"x = {x}, y = {y}",
        [f"x = {y}, y = {x}", f"x = {x + 1}, y = {y}", f"x = {x}, y = {y + 2}"],
        "Make coefficients equal and add/subtract equations.",
    )


def _gen_u3_cross_mult() -> dict:
    x, y, (a1, b1, c1), (a2, b2, c2) = _random_lin_sys()
    det = a1 * b2 - a2 * b1
    x_c = (c1 * b2 - c2 * b1) // det
    y_c = (a1 * c2 - a2 * c1) // det
    return _exam_mcq(
        "u3_cross_mult",
        f"Cross-multiplication on {_lin_eq(a1, b1, c1)} and {_lin_eq(a2, b2, c2)} gives:",
        f"x = {x_c}, y = {y_c}",
        [f"x = {y_c}, y = {x_c}", f"x = {x_c + 1}, y = {y_c}", f"x = {x_c}, y = {y_c + 1}"],
        f"Det = {det}; x = (c₁b₂ − c₂b₁)/det.",
    )


def _gen_u3_unique_k() -> dict:
    x, y, (a1, b1, c1), (a2, b2, c2) = _random_lin_sys()
    return _exam_mcq(
        "u3_unique_k",
        f"For {_lin_eq(a1, b1, c1)} and {_lin_eq(a2, b2, c2)}, the pair has a unique solution because:",
        "a₁/a₂ ≠ b₁/b₂",
        ["a₁/a₂ = b₁/b₂ = c₁/c₂", "a₁/a₂ = b₁/b₂ ≠ c₁/c₂", "Lines are coincident"],
        f"Solution: x = {x}, y = {y}.",
    )


def _gen_u3_infinite_k() -> dict:
    (a1, b1, c1), (a2, b2, c2) = _coincident_sys()
    return _exam_mcq(
        "u3_infinite_k",
        f"The pair {_lin_eq(a1, b1, c1)} and {_lin_eq(a2, b2, c2)} has infinitely many solutions because:",
        "a₁/a₂ = b₁/b₂ = c₁/c₂ (coincident lines)",
        ["a₁/a₂ ≠ b₁/b₂", "a₁/a₂ = b₁/b₂ ≠ c₁/c₂", "Lines are parallel distinct"],
        "Coincident lines → dependent equations.",
    )


def _gen_u3_no_solution_k() -> dict:
    (a1, b1, c1), (a2, b2, c2) = _parallel_sys()
    return _exam_mcq(
        "u3_no_solution_k",
        f"The pair {_lin_eq(a1, b1, c1)} and {_lin_eq(a2, b2, c2)} has no solution because:",
        "a₁/a₂ = b₁/b₂ ≠ c₁/c₂ (parallel distinct lines)",
        ["a₁/a₂ ≠ b₁/b₂", "a₁/a₂ = b₁/b₂ = c₁/c₂", "Lines intersect"],
        "Parallel distinct lines → inconsistent system.",
    )


def _gen_u3_word_ages() -> dict:
    mult = random.choice([2, 3])
    years = random.randint(8, 15)
    son = 12
    father = mult * son
    diff = father - son
    return _exam_mcq(
        "u3_word_ages",
        f"Father is {mult}× son's age; in {years} years he will be {mult - 1}× son's age. Age difference now?",
        f"{diff} years",
        [f"{diff + years} years", f"{son} years", f"{father} years"],
        f"son = {son}, father = {father}; difference = {diff}.",
    )


def _gen_u3_word_two_digit() -> dict:
    tens, ones = random.randint(2, 7), random.randint(1, 9)
    num, rev = 10 * tens + ones, 10 * ones + tens
    return _exam_mcq(
        "u3_word_two_digit",
        f"A two-digit number has tens digit {tens} and units {ones}. "
        f"Difference between the number and its reverse is:",
        str(abs(num - rev)),
        [str(num + rev), str(tens + ones), str(abs(num - rev) + 9)],
        f"Number = {num}, reverse = {rev}.",
    )


def _gen_u3_substitution_express() -> dict:
    return _make(
        "u3_substitution_express",
        _u3_multistep_mcq(3, 2, "B", step="sub_express"),
    )


def _gen_u3_substitution_y_step() -> dict:
    return _make(
        "u3_substitution_y_step",
        _u3_multistep_mcq(3, 2, "D", step="sub_y"),
    )


def _gen_u3_substitution_full() -> dict:
    return _make(
        "u3_substitution_full",
        _u3_multistep_mcq(3, 2, "C", step="sub_full"),
    )


def _gen_u3_elimination_y_step() -> dict:
    return _make(
        "u3_elimination_y_step",
        _u3_multistep_mcq(3, 3, "D", step="elim_y"),
    )


def _gen_u3_elimination_full() -> dict:
    return _make(
        "u3_elimination_full",
        _u3_multistep_mcq(3, 3, "C", step="elim_full"),
    )


def _gen_u3_consistency_ratios() -> dict:
    return _make(
        "u3_consistency_ratios",
        _u3_multistep_mcq(3, 4, "D", step="consistency"),
    )


def _gen_u3_word_ages_setup() -> dict:
    return _make(
        "u3_word_ages_setup",
        _u3_multistep_mcq(3, 4, "D", step="word_ages_setup"),
    )


def _gen_u3_word_ages_solve() -> dict:
    return _make(
        "u3_word_ages_solve",
        _u3_multistep_mcq(3, 4, "D", step="word_ages_solve"),
    )


def _gen_u3_word_income() -> dict:
    inc, exp = random.randint(8000, 15000), random.randint(5000, 12000)
    saving = inc - exp
    return _exam_mcq(
        "u3_word_income",
        f"Income = ₹{inc}, expenditure = ₹{exp}. Monthly savings = ?",
        f"₹{saving}",
        [f"₹{inc + exp}", f"₹{exp}", f"₹{saving + 500}"],
        "Form linear equations for income/expenditure word problems.",
    )


def _gen_u3_word_speed() -> dict:
    d, t = random.randint(120, 480), random.randint(2, 8)
    speed = d // t
    return _exam_mcq(
        "u3_word_speed",
        f"A train covers {d} km in {t} hours. Speed = ? km/h",
        str(speed),
        [str(speed + 10), str(d + t), str(speed - 5)],
        f"Speed = distance/time = {d}/{t} = {speed}.",
    )


def _gen_u3_word_cost() -> dict:
    pa, pb = random.randint(15, 40), random.randint(8, 25)
    na, nb = random.randint(2, 6), random.randint(3, 8)
    total = pa * na + pb * nb
    return _exam_mcq(
        "u3_word_cost",
        f"{na} pens at ₹{pa} each and {nb} pencils at ₹{pb} each cost:",
        f"₹{total}",
        [f"₹{total + pa}", f"₹{pa + pb}", f"₹{na + nb}"],
        "Two linear equations in pen and pencil counts/prices.",
    )


# ── Unit 4 — Quadratic Equations ──


def _gen_u4_factorisation() -> dict:
    r1, r2, b, c = h10t._random_quad_roots()
    eq = _quad_std(1, b, c)
    roots = f"x = {r1}, {r2}" if r1 != r2 else f"x = {r1} (repeated)"
    return _exam_mcq(
        "u4_factorisation",
        f"Solve by factorisation: {eq}",
        roots,
        [f"x = {-r1}, {-r2}", f"x = {r1 + r2}", f"x = {r1 * r2}"],
        f"Factor: (x − {r1})(x − {r2}) = 0.",
    )


def _gen_u4_quadratic_formula() -> dict:
    r1, r2, b, c = h10t._random_quad_roots()
    eq = _quad_std(1, b, c)
    d = b * b - 4 * c
    roots = f"x = {r1}, {r2}" if r1 != r2 else f"x = {r1}"
    return _exam_mcq(
        "u4_quadratic_formula",
        f"Using the quadratic formula on {eq} (Δ = {d}):",
        roots,
        [f"x = {b}, {c}", f"x = {-r1}, {-r2}", "No real roots"],
        f"x = (−b ± √Δ)/2.",
    )


def _gen_u4_solve_2x2_7x_3() -> dict:
    if random.random() < 0.4:
        eq, r1, r2 = "2x² − 7x + 3 = 0", 3, 0.5
        ans = "x = 3, 1/2"
    else:
        r1, r2, b, c = h10t._random_quad_roots()
        a = random.choice([1, 2])
        eq = _quad_std(a, a * b, a * c)
        ans = f"x = {r1}, {r2}" if r1 != r2 else f"x = {r1}"
    return _exam_mcq("u4_solve_2x2_7x_3", f"Solutions of {eq}:", ans, ["x = 0, 1", "x = 7, 3", "No real roots"])


def _gen_u4_nature_roots() -> dict:
    b, c = random.randint(-10, 10), random.randint(-12, 12)
    d = b * b - 4 * c
    nature = _nature_from_disc(d)
    return _exam_mcq(
        "u4_nature_roots",
        f"For x² + {b}x + {c} = 0, Δ = {d}. Nature of roots:",
        nature,
        [x for x in ["Two distinct real roots", "Two equal real roots", "No real roots"] if x != nature],
        f"Δ = b² − 4ac = {d}.",
    )


def _gen_u4_equal_roots_k() -> dict:
    r = random.randint(2, 8)
    k = -2 * r
    return _exam_mcq(
        "u4_equal_roots_k",
        f"x² + kx + {r * r} = 0 has equal roots. Then k = ?",
        str(k),
        [str(-k), str(r), str(k + 2)],
        f"Equal roots ⇒ Δ = k² − 4r² = 0 ⇒ k = ±{abs(k)}.",
    )


def _gen_u4_no_real_roots_k() -> dict:
    k = random.randint(1, 8)
    c = k * k + random.randint(1, 6)
    return _exam_mcq(
        "u4_no_real_roots_k",
        f"x² + {k}x + {c} = 0 has no real roots because:",
        f"Δ = {k}² − 4×{c} = {k * k - 4 * c} < 0",
        ["Δ > 0", "Δ = 0", "Roots are always real"],
        "Discriminant negative ⇒ no real roots.",
    )


def _gen_u4_form_from_roots() -> dict:
    r1, r2 = random.randint(-6, 6), random.randint(-6, 6)
    correct = _quad_std(1, -(r1 + r2), r1 * r2)
    return _exam_mcq(
        "u4_form_from_roots",
        f"Quadratic equation with roots {r1} and {r2}:",
        correct,
        [_quad_std(1, r1 + r2, r1 * r2), _quad_std(1, -(r1 + r2), -r1 * r2), _quad_std(2, -(r1 + r2), r1 * r2)],
        "(x − α)(x − β) = 0.",
    )


def _gen_u4_consecutive_integers() -> dict:
    n = random.randint(3, 12)
    product = n * (n + 1)
    return _exam_mcq(
        "u4_consecutive_integers",
        f"Product of two consecutive integers is {product}. The integers are:",
        f"{n} and {n + 1}",
        [f"{n - 1} and {n}", f"{n + 1} and {n + 2}", f"{n} and {n + 2}"],
        f"n(n+1) = {product} ⇒ n = {n}.",
    )


def _gen_u4_rectangle_area() -> dict:
    l = random.randint(5, 15)
    w = random.randint(3, 10)
    area = l * w
    return _exam_mcq(
        "u4_rectangle_area",
        f"A rectangle has length {l} m more than width. Area = {area} m². Width = ?",
        f"{w} m",
        [f"{l} m", f"{w + 1} m", f"{area} m"],
        f"Let width = x; x(x+{l}) = {area}.",
    )


def _gen_u4_speed_time() -> dict:
    d, extra = random.randint(100, 300), random.randint(1, 3)
    t1, t2 = d // 60, d // (60 + 10)
    return _exam_mcq(
        "u4_speed_time",
        f"A train travels {d} km at 60 km/h, then {d} km at 70 km/h. Total time ≈ ? hours",
        f"{t1 + t2} hours",
        [f"{t1} hours", f"{t2} hours", f"{t1 + t2 + extra} hours"],
        "Form equation: distance/speed for each leg.",
    )


def _gen_u4_verify_sum_product() -> dict:
    r1, r2, b, c = h10t._random_quad_roots()
    eq = _quad_std(1, b, c)
    return _exam_mcq(
        "u4_verify_sum_product",
        f"Roots of {eq} are {r1} and {r2}. Verify sum and product:",
        f"sum = {r1 + r2} = −({b}); product = {r1 * r2} = {c}",
        [f"sum = {c}; product = {b}", "Do not match", f"sum = {b}; product = {c}"],
        "For ax² + bx + c: sum = −b/a, product = c/a.",
    )


# ── Unit 5 — AP ──


def _gen_u5_nth_term() -> dict:
    a, d = _random_ap()
    n = random.randint(5, 15)
    term = _ap_nth(a, d, n)
    return _exam_mcq(
        "u5_nth_term",
        f"{n}th term of AP with a = {a}, d = {d}:",
        str(term),
        [str(term + d), str(a + n * d), str(term - d)],
        f"aₙ = a + (n−1)d = {term}.",
    )


def _gen_u5_20th_term() -> dict:
    a, d = _random_ap()
    term = _ap_nth(a, d, 20)
    return _exam_mcq(
        "u5_20th_term",
        f"20th term of AP {_ap_terms_str(a, d)}:",
        str(term),
        [str(_ap_nth(a, d, 19)), str(term + d), str(a + 20 * d)],
        f"a₂₀ = {a} + 19×{d} = {term}.",
    )


def _gen_u5_first_term_d() -> dict:
    a, d = _random_ap()
    a3, a7 = _ap_nth(a, d, 3), _ap_nth(a, d, 7)
    return _exam_mcq(
        "u5_first_term_d",
        f"AP whose 3rd term is {a3} and 7th term is {a7}: first term a and d are:",
        f"a = {a}, d = {d}",
        [f"a = {a + d}, d = {d + 1}", f"a = {a - 1}, d = {d}", f"a = {a}, d = 0"],
        "Solve a + 2d and a + 6d simultaneously.",
    )


def _gen_u5_sum_n_terms() -> dict:
    a, d = _random_ap()
    n = random.randint(5, 12)
    total = _ap_sum(a, d, n)
    return _exam_mcq(
        "u5_sum_n_terms",
        f"Sum of first {n} terms of AP (a = {a}, d = {d}):",
        str(total),
        [str(total + n), str(_ap_nth(a, d, n)), str(total - d)],
        f"Sₙ = n/2[2a + (n−1)d] = {total}.",
    )


def _gen_u5_sum_20_terms() -> dict:
    a, d = _random_ap()
    total = _ap_sum(a, d, 20)
    return _exam_mcq(
        "u5_sum_20_terms",
        f"Sum of first 20 terms of AP with a = {a}, d = {d}:",
        str(total),
        [str(_ap_sum(a, d, 19)), str(total + 20), str(a + d)],
        f"S₂₀ = 20/2[2×{a} + 19×{d}] = {total}.",
    )


def _gen_u5_which_term() -> dict:
    a, d = _random_ap()
    n = random.randint(8, 20)
    val = _ap_nth(a, d, n)
    return _exam_mcq(
        "u5_which_term",
        f"Which term of AP {_ap_terms_str(a, d)} equals {val}?",
        str(n),
        [str(n + 1), str(n - 1), str(n + 2)],
        f"Solve {val} = {a} + (n−1)({d}).",
    )


def _gen_u5_number_of_terms() -> dict:
    a, d = _random_ap()
    n = random.randint(6, 10)
    s_val = _ap_sum(a, d, n)
    return _exam_mcq(
        "u5_number_of_terms",
        f"Sum of AP is {s_val} with a = {a}, d = {d}. Number of terms n = ?",
        str(n),
        [str(n + 1), str(n - 1), str(n + 2)],
        f"Solve Sₙ = {s_val}.",
    )


def _gen_u5_word_savings() -> dict:
    start, inc, yr = random.choice([(8000, 500, 5), (5000, 300, 4), (10000, 600, 3)])
    salary = start + (yr - 1) * inc
    return _exam_mcq(
        "u5_word_savings",
        f"Monthly savings start at ₹{start} with ₹{inc} annual increment. Amount in year {yr}?",
        f"₹{salary}",
        [f"₹{salary + inc}", f"₹{start + yr * inc}", f"₹{start}"],
        f"AP: a = {start}, d = {inc}.",
    )


def _gen_u5_word_seating() -> dict:
    first, diff, last = random.choice([(23, -2, 5), (20, -3, 2), (30, -5, 5)])
    n = (last - first) // diff + 1
    return _exam_mcq(
        "u5_word_seating",
        f"Rows in a lawn: {first}, {first + diff}, …, {last} plants. Number of rows = ?",
        str(n),
        [str(n + 1), str(n - 1), str(abs(n))],
        f"Last term = first + (n−1)d.",
    )


def _gen_u5_three_numbers_ap() -> dict:
    d = random.choice([2, 3, 4, 5])
    mid = random.randint(5, 15)
    a, b, c = mid - d, mid, mid + d
    s, p = a + b + c, a * b * c
    return _exam_mcq(
        "u5_three_numbers_ap",
        f"Three numbers in AP with sum {s} and product {p} are:",
        f"{a}, {b}, {c}",
        [f"{a - 1}, {b}, {c + 1}", f"{b}, {a}, {c}", f"{a}, {c}, {b}"],
        f"Let numbers be a−d, a, a+d.",
    )


# ── Unit 6 — Triangles ──


def _gen_u6_bpt_state() -> dict:
    return _exam_variant("u6_bpt_state", [
        (
            "Basic Proportionality Theorem (BPT) states:",
            "A line parallel to one side of a triangle divides the other two sides proportionally",
            ["Parallel lines are equal in length", "All triangles are congruent", "Angles sum to 360°"],
            "Theorem 6.1 — Thales theorem.",
        ),
        (
            "To prove BPT, which construction is standard?",
            "Draw BE ∥ AD meeting AC produced at E (or similar auxiliary line)",
            ["Assume the triangle is equilateral", "Use coordinate geometry only", "Measure with ruler"],
            "",
        ),
        (
            "Converse of BPT: if AD/DB = AE/EC, then:",
            "DE ∥ BC",
            ["DE = BC", "ΔABC is isosceles", "AB = AC"],
            "",
        ),
    ])


def _gen_u6_bpt_side() -> dict:
    ad, db, ae, ec = _random_bpt_segments()
    return _exam_mcq(
        "u6_bpt_side",
        f"In ΔABC, DE ∥ BC. AD = {ad} cm, DB = {db} cm, AE = {ae} cm. EC = ?",
        f"{ec} cm",
        [f"{ae} cm", f"{db} cm", f"{ec + ad} cm"],
        f"AD/DB = AE/EC ⇒ EC = {ae}×{db}/{ad} = {ec}.",
    )


def _gen_u6_aa_similar() -> dict:
    return _exam_variant("u6_aa_similar", [
        (
            "To prove ΔABC ~ ΔDEF using AA criterion:",
            "Show two pairs of corresponding angles are equal",
            ["Show one side equal", "Show perimeters equal", "Show areas equal"],
            "AAA ⇒ similarity.",
        ),
        (
            "If ∠A = ∠D and ∠B = ∠E, then ΔABC ~ ΔDEF by:",
            "AA similarity criterion",
            ["SSS only", "RHS", "Congruence"],
            "",
        ),
    ])


def _gen_u6_sss_similar() -> dict:
    triple = random.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17)])
    a, b, c = triple
    k = random.randint(2, 5)
    return _exam_mcq(
        "u6_sss_similar",
        f"Δ with sides {a}, {b}, {c} is similar to Δ with sides:",
        f"{k * a}, {k * b}, {k * c}",
        [f"{a + k}, {b + k}, {c + k}", f"{a}, {b}, {c + 1}", f"{k}, {k + 1}, {k + 2}"],
        "SSS similarity: all sides in same ratio.",
    )


def _gen_u6_sas_similar() -> dict:
    return _exam_variant("u6_sas_similar", [
        (
            "SAS similarity criterion requires:",
            "One equal angle and the sides including it are proportional",
            ["All three sides equal", "Two sides equal only", "Same perimeter"],
            "Theorem 6.5.",
        ),
        (
            "If AB/DE = AC/DF and ∠A = ∠D, then:",
            "ΔABC ~ ΔDEF by SAS",
            ["ΔABC ≅ ΔDEF", "No relation", "AB = DE"],
            "",
        ),
    ])


def _gen_u6_similar_sides() -> dict:
    r1, r2 = random.randint(2, 4), random.randint(3, 6)
    side_small = random.randint(4, 12)
    side_large = side_small * r2 // r1
    return _exam_mcq(
        "u6_similar_sides",
        f"ΔABC ~ ΔDEF with AB/DE = {r1}/{r2}. If AB = {side_small} cm, then DE = ?",
        f"{side_large} cm",
        [f"{side_small} cm", f"{side_large + r1} cm", f"{side_small * r1 // r2} cm"],
        f"DE = AB × {r2}/{r1}.",
    )


def _gen_u6_pythagoras_similar() -> dict:
    return _exam_variant("u6_pythagoras_similar", [
        (
            "Pythagoras theorem is proved using similarity by:",
            "Drop altitude on hypotenuse — creates three similar right triangles",
            ["Assume c = a + b", "Use factorisation", "Measure only"],
            "NCERT proof via similarity.",
        ),
        (
            "In the similarity proof of a² + b² = c², which triangles are similar?",
            "The two smaller right triangles and the original triangle",
            ["Only the two legs", "No similar triangles", "All equilateral"],
            "",
        ),
    ])


def _gen_u6_area_ratio() -> dict:
    k = random.randint(2, 5)
    area_ratio = k * k
    return _exam_mcq(
        "u6_area_ratio",
        f"Two similar triangles have sides in ratio 1:{k}. Ratio of their areas is:",
        f"{area_ratio}:1",
        [f"{k}:1", f"{2 * k}:1", f"{k + 1}:1"],
        "Area ratio = (scale factor)².",
    )


def _gen_u6_ratio_areas() -> dict:
    k = random.randint(2, 4)
    return _exam_mcq(
        "u6_ratio_areas",
        f"If areas of two similar triangles are in ratio {k * k}:1, side ratio is:",
        f"{k}:1",
        [f"{k * k}:1", f"{k + 1}:1", f"1:{k}"],
        "Side ratio = √(area ratio).",
    )


def _gen_u6_similar_proof() -> dict:
    return _exam_variant("u6_similar_proof", [
        (
            "To prove a line divides sides proportionally using similarity:",
            "Show triangles formed are similar (AA), then equate ratios",
            ["Assume lengths equal", "Use only angle chasing", "Apply Pythagoras directly"],
            "",
        ),
        (
            "In a trapezium ABCD (AB ∥ DC), EF ∥ AB. Then AE/ED equals:",
            "BF/FC",
            ["AB/DC", "AE = BF always", "EF = AB"],
            "BPT in trapezium.",
        ),
    ])


# ── Unit 7 — Coordinate Geometry ──


def _gen_u7_distance_two_points() -> dict:
    x1, y1 = random.randint(0, 5), random.randint(0, 5)
    x2, y2 = x1 + random.randint(3, 6), y1 + random.randint(4, 8)
    d = int(_coord_dist(x1, y1, x2, y2))
    return _exam_mcq(
        "u7_distance_two_points",
        f"Distance between ({x1}, {y1}) and ({x2}, {y2}):",
        f"{d} units",
        [f"{d + 3} units", f"{x2 - x1 + y2 - y1} units", f"{d - 2} units"],
        f"√[({x2}−{x1})² + ({y2}−{y1})²] = {d}.",
    )


def _gen_u7_distance_origin() -> dict:
    x, y = random.randint(3, 12), random.randint(4, 12)
    d = int(_coord_dist(0, 0, x, y))
    return _exam_mcq(
        "u7_distance_origin",
        f"Distance of ({x}, {y}) from origin:",
        f"{d} units",
        [f"{x + y} units", f"{d + 2} units", f"{abs(x - y)} units"],
        f"√({x}² + {y}²) = {d}.",
    )


def _gen_u7_midpoint() -> dict:
    x1, y1 = random.randint(0, 4), random.randint(0, 4)
    x2, y2 = x1 + random.randint(4, 8), y1 + random.randint(4, 8)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    return _exam_mcq(
        "u7_midpoint",
        f"Midpoint of ({x1}, {y1}) and ({x2}, {y2}):",
        f"({mx:g}, {my:g})",
        [f"({x1}, {y2})", f"({x2}, {y1})", f"({mx + 1:g}, {my:g})"],
        "Mid-point formula: average of coordinates.",
    )


def _gen_u7_section_formula() -> dict:
    x1, y1 = random.randint(0, 4), random.randint(0, 4)
    x2, y2 = x1 + random.randint(4, 8), y1 + random.randint(4, 8)
    m, n = random.randint(1, 3), random.randint(1, 3)
    px, py = _section_point(x1, y1, x2, y2, m, n)
    return _exam_mcq(
        "u7_section_formula",
        f"Point dividing ({x1}, {y1}) and ({x2}, {y2}) internally in ratio {m}:{n}:",
        f"({px:g}, {py:g})",
        [f"({x1}, {y1})", f"({x2}, {y2})", f"({(x1 + x2) / 2:g}, {(y1 + y2) / 2:g})"],
        "Section formula: ((mx₂+nx₁)/(m+n), (my₂+ny₁)/(m+n)).",
    )


def _gen_u7_find_ratio() -> dict:
    x1, y1, x2, y2 = 0, 0, random.randint(6, 12), random.randint(6, 12)
    m, n = random.randint(1, 3), random.randint(1, 3)
    px, py = _section_point(x1, y1, x2, y2, m, n)
    return _exam_mcq(
        "u7_find_ratio",
        f"P({px:g}, {py:g}) divides A({x1}, {y1}) and B({x2}, {y2}). Ratio AP : PB = ?",
        f"{m} : {n}",
        [f"{n} : {m}", f"{m + n} : 1", "1 : 1"],
        "Use section formula in reverse.",
    )


def _gen_u7_collinear() -> dict:
    k = random.randint(2, 5)
    return _exam_mcq(
        "u7_collinear",
        f"Are (1, 2), (1 + {k}, 2 + 2{k}), (1 + 2{k}, 2 + 4{k}) collinear?",
        "Yes",
        ["No", "Only if k = 0", "Cannot tell"],
        "Constant slope 2 ⇒ collinear.",
    )


def _gen_u7_triangle_area() -> dict:
    base, height = random.randint(3, 8), random.randint(3, 8)
    area = base * height // 2
    return _exam_mcq(
        "u7_triangle_area",
        f"Area of triangle with vertices (0, 0), ({base}, 0), (0, {height}):",
        f"{area} sq units",
        [f"{base + height} sq units", f"{base * height} sq units", "0 sq units"],
        f"Area = ½ × {base} × {height} = {area}.",
    )


def _gen_u7_right_triangle() -> dict:
    pts = [(0, 0), (3, 0), (0, 4)]
    return _exam_mcq(
        "u7_right_triangle",
        "Do (0, 0), (3, 0), (0, 4) form a right-angled triangle?",
        "Yes — right angle at origin",
        ["No", "Equilateral", "Collinear"],
        "3-4-5 triangle: 3² + 4² = 5².",
    )


def _gen_u7_missing_coordinate() -> dict:
    x1, y = random.randint(1, 5), random.randint(1, 5)
    x2 = x1 + random.randint(3, 6)
    dist = int(_coord_dist(x1, y, x2, y))
    return _exam_mcq(
        "u7_missing_coordinate",
        f"Distance between ({x1}, {y}) and ({x2}, {y}) is {dist} units. Verify x₂:",
        f"x₂ = {x2}",
        [f"x₂ = {x1}", f"x₂ = {x2 + 2}", f"x₂ = {dist}"],
        f"|x₂ − x₁| = {dist}.",
    )


# ── Unit 8 — Trigonometry ──


def _gen_u8_standard_angles() -> dict:
    angle = random.choice([0, 30, 45, 60, 90])
    ratio = random.choice(["sin", "cos", "tan"])
    idx = {"sin": 0, "cos": 1, "tan": 2}[ratio]
    correct = _STD_TRIG[angle][idx]
    others = [v for j, v in enumerate(_STD_TRIG[angle]) if j != idx]
    return _exam_mcq("u8_standard_angles", f"{ratio} {angle}° = ?", correct, others + ["1"])


def _gen_u8_eval_expression() -> dict:
    a, b = random.choice([(30, 60), (45, 45), (60, 30)])
    ans_val = "1"
    if (a, b) == (45, 45):
        ans_val = "√2"
    return _exam_mcq(
        "u8_eval_expression",
        f"sin {a}° + cos {b}° = ?",
        ans_val,
        ["0", "√3", "1/2"],
        "Use standard trigonometric values.",
    )


def _gen_u8_sin_to_cos_tan() -> dict:
    opp, adj, hyp = _random_right_triangle()
    sin_v = f"{opp}/{hyp}"
    cos_v = f"{adj}/{hyp}"
    tan_v = f"{opp}/{adj}"
    return _exam_mcq(
        "u8_sin_to_cos_tan",
        f"If sin θ = {sin_v}, then cos θ and tan θ are:",
        f"cos θ = {cos_v}, tan θ = {tan_v}",
        [f"cos θ = {opp}/{hyp}, tan θ = {adj}/{opp}", f"cos θ = {hyp}/{adj}, tan θ = 1", "Cannot determine"],
        "Use sin²θ + cos²θ = 1 and tan = sin/cos.",
    )


def _gen_u8_tan_to_sin_cos() -> dict:
    opp, adj, hyp = _random_right_triangle()
    tan_v = f"{opp}/{adj}"
    return _exam_mcq(
        "u8_tan_to_sin_cos",
        f"If tan θ = {tan_v}, then sin θ and cos θ are:",
        f"sin θ = {opp}/{hyp}, cos θ = {adj}/{hyp}",
        [f"sin θ = {adj}/{hyp}, cos θ = {opp}/{hyp}", f"sin θ = 1, cos θ = 0", "Equal"],
        "From tan = opp/adj, build right triangle.",
    )


def _gen_u8_prove_identity() -> dict:
    return _exam_variant("u8_prove_identity", [
        (
            "To prove a trig identity, the first step is often:",
            "Express all ratios in terms of sin θ and cos θ",
            ["Substitute θ = 90°", "Multiply by sec θ only", "Assume identity false"],
            "",
        ),
        (
            "Which identity helps simplify (1 − sin²θ)?",
            "cos²θ",
            ["sin²θ", "tan²θ", "sec²θ"],
            "sin²θ + cos²θ = 1.",
        ),
    ])


def _gen_u8_sin2_cos2() -> dict:
    return _exam_variant("u8_sin2_cos2", [
        (
            "Fundamental identity sin²θ + cos²θ = 1 implies:",
            "1 − sin²θ = cos²θ",
            ["1 + sin²θ = cos²θ", "sin²θ = cos²θ", "tan²θ = 1"],
            "",
        ),
        (
            "For any angle θ where defined, sin²θ + cos²θ equals:",
            "1",
            ["0", "sin θ + cos θ", "tan θ"],
            "",
        ),
    ])


def _gen_u8_one_plus_tan2() -> dict:
    return _exam_variant("u8_one_plus_tan2", [
        (
            "Identity 1 + tan²θ equals:",
            "sec²θ",
            ["cosec²θ", "cos²θ", "sin²θ"],
            "Divide sin²θ + cos²θ = 1 by cos²θ.",
        ),
        (
            "sec²θ − tan²θ equals:",
            "1",
            ["0", "sin²θ", "cos²θ"],
            "Rearrange 1 + tan²θ = sec²θ.",
        ),
    ])


def _gen_u8_simplify() -> dict:
    return _exam_variant("u8_simplify", [
        (
            "(1 − sin²θ)(1 + tan²θ) simplifies to:",
            "1",
            ["sin²θ", "0", "sec²θ"],
            "Use sin²θ + cos²θ = 1 and 1 + tan²θ = sec²θ.",
        ),
        (
            "sin²θ + cos²θ − 1 equals:",
            "0",
            ["1", "sin²θ", "cos²θ"],
            "",
        ),
    ])


def _gen_u8_find_angle() -> dict:
    angle = random.choice([30, 45, 60])
    ratio = random.choice(["sin", "cos", "tan"])
    idx = {"sin": 0, "cos": 1, "tan": 2}[ratio]
    val = _STD_TRIG[angle][idx]
    return _exam_mcq(
        "u8_find_angle",
        f"If {ratio} θ = {val}, then θ = ?",
        f"{angle}°",
        ["90°", "0°", f"{90 - angle}°"],
        "Standard angle table.",
    )


# ── Unit 9 — Applications of Trigonometry ──


def _gen_u9_elevation_height() -> dict:
    dist = random.randint(20, 100)
    angle = random.choice([30, 45, 60])
    if angle == 45:
        height = dist
    elif angle == 30:
        height = round(dist / math.sqrt(3))
    else:
        height = round(dist * math.sqrt(3))
    return _exam_mcq(
        "u9_elevation_height",
        f"From {dist} m away, angle of elevation {angle}°. Tower height ≈ ?",
        f"{height} m",
        [f"{dist} m", f"{height // 2} m", f"{height * 2} m"],
        f"tan {angle}° = height/{dist}.",
    )


def _gen_u9_elevation_distance() -> dict:
    height = random.randint(20, 80)
    angle = random.choice([30, 45, 60])
    if angle == 45:
        dist = height
    elif angle == 30:
        dist = round(height * math.sqrt(3))
    else:
        dist = round(height / math.sqrt(3))
    return _exam_mcq(
        "u9_elevation_distance",
        f"Tower height {height} m, angle of elevation {angle}°. Distance from foot ≈ ?",
        f"{dist} m",
        [f"{height} m", f"{dist + 10} m", f"{dist // 2} m"],
        f"Distance = height/tan {angle}°.",
    )


def _gen_u9_depression() -> dict:
    angle = random.choice([30, 45, 60])
    height = random.randint(10, 60)
    dist = round(height / math.tan(math.radians(angle)))
    return _exam_mcq(
        "u9_depression",
        f"From a cliff {height} m high, angle of depression to a boat is {angle}°. Boat is ≈ ? m away",
        f"{dist} m",
        [f"{height} m", f"{dist + 5} m", f"{dist // 2} m"],
        "Angle of depression = angle of elevation from boat.",
    )


def _gen_u9_two_angles_height() -> dict:
    d1, d2 = random.randint(20, 40), random.randint(10, 25)
    ang1, ang2 = 30, 60
    h = round(d1 * math.tan(math.radians(ang1)))
    return _exam_mcq(
        "u9_two_angles_height",
        f"Building viewed from {d1} m (30°) and {d1 + d2} m (60°). Height ≈ ? m",
        f"{h} m",
        [f"{d1} m", f"{h + 10} m", f"{d2} m"],
        "Two right triangles with same height.",
    )


def _gen_u9_two_position() -> dict:
    dist = random.randint(40, 100)
    h = round(dist * math.tan(math.radians(30)))
    return _exam_mcq(
        "u9_two_position",
        f"Tower seen at 30° from point A and 60° from point B (A–B = {dist} m). Height ≈ ?",
        f"{h} m",
        [f"{dist} m", f"{h + 15} m", f"{dist // 2} m"],
        "Set up two equations in height and distances.",
    )


def _gen_u9_ladder_wall() -> dict:
    base, hyp = random.choice([(6, 10), (8, 10), (5, 13)])
    height = int(math.isqrt(hyp * hyp - base * base))
    return _exam_mcq(
        "u9_ladder_wall",
        f"A ladder {hyp} m long rests against a wall with foot {base} m away. Height on wall = ?",
        f"{height} m",
        [f"{base} m", f"{hyp} m", f"{height + 2} m"],
        f"h² = {hyp}² − {base}².",
    )


# ── Unit 10 — Circles ──


def _gen_u10_tangent_perp() -> dict:
    return _exam_variant("u10_tangent_perp", [
        (
            "Theorem 10.1 states that the tangent at any point of a circle:",
            "Is perpendicular to the radius through the point of contact",
            ["Is parallel to the radius", "Equals the diameter", "Makes 45° with radius"],
            "",
        ),
        (
            "At point of contact P, ∠ between radius OP and tangent PQ equals:",
            "90°",
            ["45°", "60°", "180°"],
            "",
        ),
    ])


def _gen_u10_equal_tangents() -> dict:
    return _exam_variant("u10_equal_tangents", [
        (
            "Theorem 10.2: tangents drawn from an external point to a circle are:",
            "Equal in length",
            ["Perpendicular to each other", "Parallel", "Half the radius"],
            "",
        ),
        (
            "From external point P, tangents PQ and PR satisfy:",
            "PQ = PR",
            ["PQ = 2PR", "PQ ⊥ PR always", "PQ ∥ PR"],
            "",
        ),
    ])


def _gen_u10_tangent_length() -> dict:
    r, op, pq = random.choice(_tangent_pairs())
    return _exam_mcq(
        "u10_tangent_length",
        f"Radius {r} cm, point {op} cm from centre. Tangent length = ?",
        f"{pq} cm",
        [f"{op} cm", f"{r} cm", f"{pq + 2} cm"],
        f"PQ = √({op}² − {r}²) = {pq}.",
    )


def _gen_u10_radius_from_tangent() -> dict:
    r, op, pq = random.choice(_tangent_pairs())
    return _exam_mcq(
        "u10_radius_from_tangent",
        f"Tangent length {pq} cm from point {op} cm from centre. Radius = ?",
        f"{r} cm",
        [f"{op} cm", f"{pq} cm", f"{r + op} cm"],
        f"r = √({op}² − {pq}²) = {r}.",
    )


def _gen_u10_tangent_proof() -> dict:
    angle = random.choice([40, 60, 80, 100, 120])
    return _exam_mcq(
        "u10_tangent_proof",
        f"Two tangents from P make {angle}° at P. OP bisects this angle, so each half is:",
        f"{angle // 2}°",
        [f"{angle}°", "90°", f"{angle + 30}°"],
        "OP bisects ∠QPR between equal tangents.",
    )


def _gen_u10_tangent_numerical() -> dict:
    r, op, pq = random.choice(_tangent_pairs())
    return _exam_mcq(
        "u10_tangent_numerical",
        f"From P, OQ = {op} cm (O centre), radius = {r} cm. Length of tangent PQ = ?",
        f"{pq} cm",
        [f"{op} cm", f"{r + pq} cm", f"{r} cm"],
        f"Right triangle: PQ = √({op}² − {r}²).",
    )


# ── Unit 11 — Areas Related to Circles ──


def _gen_u11_sector_area() -> dict:
    r = random.randint(5, 42)
    angle = random.choice(list(range(30, 181, 15)))
    area = _sector_area(r, angle)
    return _exam_mcq(
        "u11_sector_area",
        f"Sector: r = {r} cm, θ = {angle}°. Area ≈ ?",
        f"{area} cm²",
        [f"{area * 2} cm²", f"{r * r} cm²", f"{area / 2} cm²"],
        f"(θ/360)πr².",
    )


def _gen_u11_arc_length() -> dict:
    r = random.randint(5, 42)
    angle = random.choice(list(range(30, 181, 10)))
    arc = _arc_length(r, angle)
    return _exam_mcq(
        "u11_arc_length",
        f"Arc length: r = {r} cm, θ = {angle}° ≈ ?",
        f"{arc} cm",
        [f"{arc * 2} cm", f"{2 * math.pi * r:.1f} cm", f"{r} cm"],
        f"(θ/360) × 2πr.",
    )


def _gen_u11_segment_area() -> dict:
    r = random.randint(5, 35)
    angle = random.choice(list(range(30, 151, 10)))
    sector = _sector_area(r, angle)
    tri = round(r * r * math.sin(math.radians(angle)) / 2, 2)
    segment = round(sector - tri, 2)
    return _exam_mcq(
        "u11_segment_area",
        f"Minor segment: r = {r} cm, θ = {angle}°. Area ≈ ?",
        f"{segment} cm²",
        [f"{sector} cm²", f"{tri} cm²", f"{segment * 2} cm²"],
        "Segment = sector − triangle.",
    )


def _gen_u11_shaded_circle_square() -> dict:
    r = random.randint(5, 28)
    side = 2 * r
    sq = side * side
    quad_area = round(math.pi * r * r / 4, 2)
    shaded = round(sq - 4 * quad_area, 2)
    return _exam_mcq(
        "u11_shaded_circle_square",
        f"Square side {side} cm with four quadrants (r = {r}) at corners. Shaded centre area ≈ ?",
        f"{shaded} cm²",
        [f"{sq} cm²", f"{quad_area} cm²", f"{4 * quad_area} cm²"],
        "Square minus four quadrants.",
    )


def _gen_u11_shaded_circle_triangle() -> dict:
    r = random.randint(4, 14)
    tri_area = round(r * r, 2)
    semi = round(math.pi * r * r / 2, 2)
    shaded = round(semi - tri_area, 2)
    return _exam_mcq(
        "u11_shaded_circle_triangle",
        f"Semicircle radius {r} cm with inscribed right isosceles triangle. Shaded area ≈ ?",
        f"{abs(shaded)} cm²",
        [f"{semi} cm²", f"{tri_area} cm²", f"{semi + tri_area} cm²"],
        "Semicircle minus triangle.",
    )


def _gen_u11_sector_perimeter() -> dict:
    r = random.randint(5, 42)
    angle = random.choice(list(range(30, 181, 10)))
    arc = _arc_length(r, angle)
    perim = round(arc + 2 * r, 2)
    return _exam_mcq(
        "u11_sector_perimeter",
        f"Perimeter of sector (r = {r} cm, θ = {angle}°) ≈ ?",
        f"{perim} cm",
        [f"{arc} cm", f"{2 * r} cm", f"{perim + r} cm"],
        "Arc + two radii.",
    )


def _gen_u11_semicircles_composite() -> dict:
    r = random.randint(4, 14)
    combined = round(math.pi * r * r, 2)
    return _exam_mcq(
        "u11_semicircles_composite",
        f"Two semicircles of radius {r} cm on opposite sides of a diameter form a composite figure. Total area ≈ ?",
        f"{combined} cm²",
        [f"{round(math.pi * r * r / 2, 2)} cm²", f"{r} cm²", f"{combined * 2} cm²"],
        "Two semicircles = one full circle.",
    )


# ── Unit 12 — Surface Areas & Volumes ──


def _gen_u12_combo_sa_volume() -> dict:
    r, h = random.randint(2, 14), random.randint(4, 20)
    csa = round(2 * math.pi * r * h, 2)
    vol = round(math.pi * r * r * h, 2)
    return _exam_mcq(
        "u12_combo_sa_volume",
        f"Cylinder r = {r} cm, h = {h} cm. CSA ≈ ? cm² and volume ≈ ? cm³:",
        f"CSA = {csa}, V = {vol}",
        [f"CSA = {vol}, V = {csa}", f"CSA = {csa * 2}, V = {vol}", f"CSA = {csa}, V = {vol * 2}"],
        "CSA = 2πrh; V = πr²h.",
    )


def _gen_u12_cone_cylinder() -> dict:
    r, h = random.randint(3, 10), random.randint(6, 15)
    vol_cyl = round(math.pi * r * r * h, 2)
    vol_cone = round(math.pi * r * r * h / 3, 2)
    return _exam_mcq(
        "u12_cone_cylinder",
        f"Cone and cylinder each have r = {r} cm, h = {h} cm. Ratio of cone volume to cylinder volume = ?",
        "1 : 3",
        ["1 : 2", "2 : 3", "3 : 1"],
        "Cone volume is one-third of cylinder with same base and height.",
    )


def _gen_u12_joined_solids_volume() -> dict:
    r, h = random.randint(2, 14), random.randint(4, 20)
    vol = round(math.pi * r * r * h / 3 + 2 * math.pi * r ** 3 / 3, 2)
    return _exam_mcq(
        "u12_joined_solids_volume",
        f"Solid: cone (h = {h}, r = {r}) surmounted by hemisphere (r = {r}). Volume ≈ ?",
        f"{vol} cm³",
        [f"{round(math.pi * r * r * h / 3, 2)} cm³", f"{round(4 * math.pi * r ** 3 / 3, 2)} cm³", f"{vol * 2} cm³"],
        "Add cone and hemisphere volumes.",
    )


def _gen_u12_melting_conversion() -> dict:
    r = random.randint(3, 9)
    vol_sph = round(4 * math.pi * r ** 3 / 3, 2)
    return _exam_mcq(
        "u12_melting_conversion",
        f"A metallic sphere of radius {r} cm is melted and recast. Volume is conserved, so volume ≈ ?",
        f"{vol_sph} cm³",
        [f"{round(4 * math.pi * r * r, 2)} cm²", f"{vol_sph * 2} cm³", f"{r ** 3} cm³"],
        "Volume unchanged during melting/recasting.",
    )


def _gen_u12_dimensions_from_volume() -> dict:
    r, h = random.randint(2, 14), random.randint(4, 20)
    vol = round(math.pi * r * r * h, 2)
    return _exam_mcq(
        "u12_dimensions_from_volume",
        f"Cylinder volume = {vol} cm³, r = {r} cm. Height h ≈ ?",
        f"{h} cm",
        [f"{r} cm", f"{h + 2} cm", f"{vol} cm"],
        f"h = V/(πr²).",
    )


# ── Registry & public API ──

EXAM_GENERATOR_REGISTRY: dict[str, callable] = {
    "u1_euclid_hcf": _gen_u1_euclid_hcf,
    "u1_hcf_lcm_prime": _gen_u1_hcf_lcm_prime,
    "u1_sqrt2_irrational": _gen_u1_sqrt2_irrational,
    "u1_sqrt3_irrational": _gen_u1_sqrt3_irrational,
    "u1_sqrt5_irrational": _gen_u1_sqrt5_irrational,
    "u1_sum_irrational": _gen_u1_sum_irrational,
    "u1_hcf_from_product_lcm": _gen_u1_hcf_from_product_lcm,
    "u1_hcf_lcm_pairs": _gen_u1_hcf_lcm_pairs,
    "u1_euclid_first_remainder": _gen_u1_euclid_first_remainder,
    "u1_prime_factor_step": _gen_u1_prime_factor_step,
    "u1_prime_hcf_step": _gen_u1_prime_hcf_step,
    "u1_prime_lcm_step": _gen_u1_prime_lcm_step,
    "u1_hcf_lcm_pair_step": _gen_u1_hcf_lcm_pair_step,
    "u1_irrational_assume_step": _gen_u1_irrational_assume_step,
    "u1_irrational_contradiction_step": _gen_u1_irrational_contradiction_step,
    "u2_zeroes_verify": _gen_u2_zeroes_verify,
    "u2_alpha_beta_sum": _gen_u2_alpha_beta_sum,
    "u2_form_from_zeroes": _gen_u2_form_from_zeroes,
    "u2_find_k_one_zero": _gen_u2_find_k_one_zero,
    "u2_equal_zeroes_k": _gen_u2_equal_zeroes_k,
    "u2_form_sum_product": _gen_u2_form_sum_product,
    "u2_graphical_zeroes": _gen_u2_graphical_zeroes,
    "u2_zeroes_x2_7x_12": _gen_u2_zeroes_x2_7x_12,
    "u2_surd_zero_polynomial": _gen_u2_surd_zero_polynomial,
    "u2_surd_zero_product": _gen_u2_surd_zero_product,
    "u2_surd_zero_sum": _gen_u2_surd_zero_sum,
    "u2_cubic_factor_all_zeroes": _gen_u2_cubic_factor_all_zeroes,
    "u2_cubic_factor_quotient": _gen_u2_cubic_factor_quotient,
    "u2_cubic_verify_quadratic": _gen_u2_cubic_verify_quadratic,
    "u3_substitution": _gen_u3_substitution,
    "u3_elimination": _gen_u3_elimination,
    "u3_cross_mult": _gen_u3_cross_mult,
    "u3_unique_k": _gen_u3_unique_k,
    "u3_infinite_k": _gen_u3_infinite_k,
    "u3_no_solution_k": _gen_u3_no_solution_k,
    "u3_word_ages": _gen_u3_word_ages,
    "u3_word_two_digit": _gen_u3_word_two_digit,
    "u3_word_income": _gen_u3_word_income,
    "u3_word_speed": _gen_u3_word_speed,
    "u3_word_cost": _gen_u3_word_cost,
    "u3_substitution_express": _gen_u3_substitution_express,
    "u3_substitution_y_step": _gen_u3_substitution_y_step,
    "u3_substitution_full": _gen_u3_substitution_full,
    "u3_elimination_y_step": _gen_u3_elimination_y_step,
    "u3_elimination_full": _gen_u3_elimination_full,
    "u3_consistency_ratios": _gen_u3_consistency_ratios,
    "u3_word_ages_setup": _gen_u3_word_ages_setup,
    "u3_word_ages_solve": _gen_u3_word_ages_solve,
    "u4_factorisation": _gen_u4_factorisation,
    "u4_quadratic_formula": _gen_u4_quadratic_formula,
    "u4_solve_2x2_7x_3": _gen_u4_solve_2x2_7x_3,
    "u4_nature_roots": _gen_u4_nature_roots,
    "u4_equal_roots_k": _gen_u4_equal_roots_k,
    "u4_no_real_roots_k": _gen_u4_no_real_roots_k,
    "u4_form_from_roots": _gen_u4_form_from_roots,
    "u4_consecutive_integers": _gen_u4_consecutive_integers,
    "u4_rectangle_area": _gen_u4_rectangle_area,
    "u4_speed_time": _gen_u4_speed_time,
    "u4_verify_sum_product": _gen_u4_verify_sum_product,
    "u5_nth_term": _gen_u5_nth_term,
    "u5_20th_term": _gen_u5_20th_term,
    "u5_first_term_d": _gen_u5_first_term_d,
    "u5_sum_n_terms": _gen_u5_sum_n_terms,
    "u5_sum_20_terms": _gen_u5_sum_20_terms,
    "u5_which_term": _gen_u5_which_term,
    "u5_number_of_terms": _gen_u5_number_of_terms,
    "u5_word_savings": _gen_u5_word_savings,
    "u5_word_seating": _gen_u5_word_seating,
    "u5_three_numbers_ap": _gen_u5_three_numbers_ap,
    "u6_bpt_state": _gen_u6_bpt_state,
    "u6_bpt_side": _gen_u6_bpt_side,
    "u6_aa_similar": _gen_u6_aa_similar,
    "u6_sss_similar": _gen_u6_sss_similar,
    "u6_sas_similar": _gen_u6_sas_similar,
    "u6_similar_sides": _gen_u6_similar_sides,
    "u6_pythagoras_similar": _gen_u6_pythagoras_similar,
    "u6_area_ratio": _gen_u6_area_ratio,
    "u6_ratio_areas": _gen_u6_ratio_areas,
    "u6_similar_proof": _gen_u6_similar_proof,
    "u7_distance_two_points": _gen_u7_distance_two_points,
    "u7_distance_origin": _gen_u7_distance_origin,
    "u7_midpoint": _gen_u7_midpoint,
    "u7_section_formula": _gen_u7_section_formula,
    "u7_find_ratio": _gen_u7_find_ratio,
    "u7_collinear": _gen_u7_collinear,
    "u7_triangle_area": _gen_u7_triangle_area,
    "u7_right_triangle": _gen_u7_right_triangle,
    "u7_missing_coordinate": _gen_u7_missing_coordinate,
    "u8_standard_angles": _gen_u8_standard_angles,
    "u8_eval_expression": _gen_u8_eval_expression,
    "u8_sin_to_cos_tan": _gen_u8_sin_to_cos_tan,
    "u8_tan_to_sin_cos": _gen_u8_tan_to_sin_cos,
    "u8_prove_identity": _gen_u8_prove_identity,
    "u8_sin2_cos2": _gen_u8_sin2_cos2,
    "u8_one_plus_tan2": _gen_u8_one_plus_tan2,
    "u8_simplify": _gen_u8_simplify,
    "u8_find_angle": _gen_u8_find_angle,
    "u9_elevation_height": _gen_u9_elevation_height,
    "u9_elevation_distance": _gen_u9_elevation_distance,
    "u9_depression": _gen_u9_depression,
    "u9_two_angles_height": _gen_u9_two_angles_height,
    "u9_two_position": _gen_u9_two_position,
    "u9_ladder_wall": _gen_u9_ladder_wall,
    "u10_tangent_perp": _gen_u10_tangent_perp,
    "u10_equal_tangents": _gen_u10_equal_tangents,
    "u10_tangent_length": _gen_u10_tangent_length,
    "u10_radius_from_tangent": _gen_u10_radius_from_tangent,
    "u10_tangent_proof": _gen_u10_tangent_proof,
    "u10_tangent_numerical": _gen_u10_tangent_numerical,
    "u11_sector_area": _gen_u11_sector_area,
    "u11_arc_length": _gen_u11_arc_length,
    "u11_segment_area": _gen_u11_segment_area,
    "u11_shaded_circle_square": _gen_u11_shaded_circle_square,
    "u11_shaded_circle_triangle": _gen_u11_shaded_circle_triangle,
    "u11_sector_perimeter": _gen_u11_sector_perimeter,
    "u11_semicircles_composite": _gen_u11_semicircles_composite,
    "u12_combo_sa_volume": _gen_u12_combo_sa_volume,
    "u12_cone_cylinder": _gen_u12_cone_cylinder,
    "u12_joined_solids_volume": _gen_u12_joined_solids_volume,
    "u12_melting_conversion": _gen_u12_melting_conversion,
    "u12_dimensions_from_volume": _gen_u12_dimensions_from_volume,
}


def generate(exam_type_id: str) -> dict | None:
    fn = EXAM_GENERATOR_REGISTRY.get(exam_type_id)
    if not fn:
        return None
    try:
        return fn()
    except Exception:
        return None


def generate_for_slot(unit_id: int, topic_id: int, level: str) -> dict | None:
    ids = h10et.exam_types_for_slot(unit_id, topic_id, level)
    if not ids:
        return None
    random.shuffle(ids)
    for eid in ids:
        q = generate(eid)
        if q:
            return q
    return None


def all_generators() -> list[str]:
    return sorted(EXAM_GENERATOR_REGISTRY.keys())
