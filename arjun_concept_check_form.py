"""Math 3 Friday Concept Check — Unit 1 sections I–V.

Seeds are the actual problems from Arjun's CC1–CC5 papers (plus Scientific
Notation items from a later school form, because CC1–CC5 did not include V).
"""

from __future__ import annotations

SECTIONS: dict[str, dict] = {
    "I": {
        "id": "I",
        "roman": "I",
        "title": "Numerical Relationships",
        "short": "Fractions, mixed numbers, sequences",
        "note_files": [
            "activity_1_investigating_patterns.md",
            "activity_2_operations_with_fractions.md",
        ],
        "session_count": 5,
        "emoji": "🔢",
        "color": "#2563eb",
    },
    "II": {
        "id": "II",
        "roman": "II",
        "title": "Powers and Roots",
        "short": "Squares, cubes, order of operations",
        "note_files": ["activity_3_powers_and_roots.md"],
        "session_count": 5,
        "emoji": "⬜",
        "color": "#7c3aed",
    },
    "III": {
        "id": "III",
        "roman": "III",
        "title": "Rational and Irrational Numbers",
        "short": "Convert, estimate roots, repeating decimals",
        "note_files": [
            "activity_4_rational_numbers.md",
            "activity_5_rational_irrational_numbers.md",
        ],
        "session_count": 5,
        "emoji": "√",
        "color": "#059669",
    },
    "IV": {
        "id": "IV",
        "roman": "IV",
        "title": "Exponent Properties",
        "short": "Product, quotient, power rules; positive exponents",
        "note_files": ["activity_6_properties_of_exponents.md"],
        "session_count": 4,
        "emoji": "𝑥ⁿ",
        "color": "#d97706",
    },
    "V": {
        "id": "V",
        "roman": "V",
        "title": "Scientific Notation",
        "short": "Convert, multiply, subtract in scientific notation",
        "note_files": [
            "activity_7_scientific_notation.md",
            "activity_8_operations_scientific_notation.md",
        ],
        "session_count": 3,
        "emoji": "🔬",
        "color": "#db2777",
    },
}


def _q(
    qid: str,
    section: str,
    paper: str,
    stem: str,
    question: str,
    options: list[str],
    answer: int,
    explanation: str,
) -> dict:
    return {
        "id": qid,
        "section": section,
        "paper": paper,
        "stem": stem,
        "question": question,
        "options": options,
        "answer": answer,
        "explanation": explanation,
        "source": "concept_check_form",
    }


FORM_SEED_QUESTIONS: list[dict] = [
    # ── I  Numerical Relationships (CC1, CC2, CC4) ──
    _q(
        "cc_i_cc1_1", "I", "CC1",
        "evaluate_mixed",
        "Evaluate. Write the answer in simplest form.\n5¼ − ⅔",
        ["4 7/12", "4 1/12", "5 1/12", "3 7/12"],
        0,
        "5¼=21/4=63/12 and ⅔=8/12. 63/12−8/12=55/12=4 7/12.",
    ),
    _q(
        "cc_i_cc1_2", "I", "CC1",
        "division_how_many_fit",
        "Bella has a guitar-pick display case 40½ cm long. Each pick is 2¼ cm wide. "
        "How many picks will fit in the case?",
        ["18", "38¼", "16", "90"],
        0,
        "40½÷2¼ = 81/2 ÷ 9/4 = 81/2 × 4/9 = 18.",
    ),
    _q(
        "cc_i_cc1_3", "I", "CC1",
        "order_absolute_value",
        "Arrange these terms to create a DECREASING sequence.\n|−100 − 8|    ·    |5 − 9|    ·    |3| · |−4|",
        ["108, 12, 4", "108, 4, 12", "4, 12, 108", "12, 108, 4"],
        0,
        "|−108|=108, |−4|=4, 3×4=12. Decreasing: 108, 12, 4.",
    ),
    _q(
        "cc_i_cc1_4", "I", "CC1",
        "describe_sequence",
        "The sequence is 6⅓, 7, 7⅔, 8⅓, … Describe the pattern.",
        [
            "Each term is ⅔ more than the previous term",
            "Each term is ⅓ more than the previous term",
            "Each term is twice the previous term",
            "The terms alternate even and odd",
        ],
        0,
        "7 − 6⅓ = ⅔, and each later step is also ⅔.",
    ),
    _q(
        "cc_i_cc1_5", "I", "CC1",
        "next_term",
        "The sequence is 6⅓, 7, 7⅔, 8⅓, … What is the next term?",
        ["9", "8⅔", "9⅓", "10"],
        0,
        "8⅓ + ⅔ = 9.",
    ),
    _q(
        "cc_i_cc2_1", "I", "CC2",
        "multi_step_mixed",
        "Mason had 10¼ lb of sinigang for a party. At the party 6⅔ lb were eaten. "
        "Then his cousin took 2½ lb home. How many pounds are left?",
        ["1 1/12 lb", "1 1/4 lb", "2 1/12 lb", "13/4 lb"],
        0,
        "10¼−6⅔−2½ = 41/4 − 20/3 − 5/2. LCD 12: 123/12 − 80/12 − 30/12 = 13/12 = 1 1/12.",
    ),
    _q(
        "cc_i_cc2_2", "I", "CC2",
        "nested_of",
        "Enaya’s burrito club: ⅔ of the burritos have pinto beans; the rest have black beans. "
        "Of the black-bean burritos, ⅛ have pico de gallo. What portion of all burritos "
        "have black beans and pico de gallo?",
        ["1/24", "1/8", "1/3", "2/24"],
        0,
        "Black beans are 1/3 of the burritos. (1/3)×(1/8)=1/24.",
    ),
    _q(
        "cc_i_cc2_3", "I", "CC2",
        "evaluate_mixed",
        "Evaluate. Write the answer in simplest form.\n4 8/9 ÷ 1 4/7",
        ["3 1/9", "3 1/7", "4 1/9", "28/11"],
        0,
        "44/9 ÷ 11/7 = 44/9 × 7/11 = 28/9 = 3 1/9.",
    ),
    _q(
        "cc_i_cc4_1", "I", "CC4",
        "evaluate_mixed",
        "Evaluate. Write the answer in simplest form.\n15⅔ − 11⅝",
        ["4 1/24", "4 1/8", "3 23/24", "31/24"],
        0,
        "15⅔=47/3=376/24 and 11⅝=93/8=279/24. 376/24−279/24=97/24=4 1/24.",
    ),
    _q(
        "cc_i_cc4_2", "I", "CC4",
        "evaluate_mixed",
        "Evaluate. Write the answer in simplest form.\n3 4/5 ÷ 5 1/20",
        ["76/101", "19/101", "76/20", "4"],
        0,
        "19/5 ÷ 101/20 = 19/5 × 20/101 = 76/101.",
    ),
    _q(
        "cc_i_cc4_3", "I", "CC4",
        "nested_of",
        "Duncan is baking cakes. Of all the cakes, ⅛ are chocolate and the rest are vanilla. "
        "Of the vanilla cakes, he hid 4/9 from his sister Emma. What fraction of all cakes "
        "were vanilla and hidden from Emma?",
        ["7/18", "4/9", "7/8", "4/72"],
        0,
        "Vanilla is 7/8. (7/8)×(4/9)=28/72=7/18.",
    ),
    _q(
        "cc_i_cc4_4", "I", "CC4",
        "sequence_conjecture",
        "Figure 1 is 1 small up-triangle. Figure 2 is a large triangle made of 4 small triangles. "
        "Write a conjecture for the number of small triangles in Figure 3.",
        [
            "Figure n has n² small triangles, so Figure 3 has 9",
            "Add 3 each time, so Figure 3 has 7",
            "Double each time, so Figure 3 has 8",
            "Figure 3 has 4 small triangles",
        ],
        0,
        "1, 4, 9, … are square numbers. Figure 3 has 3²=9 small triangles.",
    ),
    # ── II  Powers and Roots (CC2, CC4, CC5) ──
    _q(
        "cc_ii_cc2_5", "II", "CC2",
        "solve_square",
        "Solve for x.\nx² = 121",
        ["x = 11 or x = −11", "x = 11 only", "x = 60.5", "x = √11"],
        0,
        "11²=121 and (−11)²=121.",
    ),
    _q(
        "cc_ii_cc2_6", "II", "CC2",
        "cube_edge",
        "A cube has volume 343 cubic ft. What is the length of an edge?",
        ["7 ft", "11 ft", "171.5 ft", "√343 ft"],
        0,
        "7³=343, so the edge is 7 ft.",
    ),
    _q(
        "cc_ii_cc2_7", "II", "CC2",
        "error_perimeter_area",
        "Kevin has 36 feet of fencing. He wants a perfect-square pen. He says that if he uses "
        "all 36 feet, each side will be 6 ft. Describe Kevin’s error.",
        [
            "36 ft is the perimeter, so each side is 36÷4=9 ft, not √36=6 ft",
            "He should use 36² for the side",
            "A square cannot have perimeter 36",
            "He is correct: side = √36 = 6",
        ],
        0,
        "Fencing is perimeter. Side = 36/4 = 9 ft. Kevin treated 36 as area.",
    ),
    _q(
        "cc_ii_cc2_8", "II", "CC2",
        "order_of_ops",
        "Evaluate.\n8² ÷ (5 + 3) · 6 − 10 + 2",
        ["40", "7", "−10", "48"],
        0,
        "8²=64, 5+3=8, 64÷8=8, 8·6=48, 48−10+2=40.",
    ),
    _q(
        "cc_ii_cc2_9", "II", "CC2",
        "error_order_of_ops",
        "Jung and Kook both start with 70 ÷ 2(4 + 1).\n"
        "Jung: 70 ÷ 2(5) = 70 ÷ 10 = 7.\n"
        "Kook: 70 ÷ 2 × 5 = 35 × 5 = 175.\n"
        "Who solved it incorrectly, and why?",
        [
            "Jung — multiply and divide left to right, so 70÷2×5=175",
            "Kook — parentheses force 2(5)=10 first",
            "Both are wrong",
            "Both are right; the expression has two values",
        ],
        0,
        "Parentheses first: 4+1=5. Then ÷ and × left to right: 70÷2×5=175. Jung grouped 2(5) as one step.",
    ),
    _q(
        "cc_ii_cc4_5", "II", "CC4",
        "solve_cube",
        "Solve for x.\nx³ = 729",
        ["x = 9", "x = 27", "x = ±9", "x = 243"],
        0,
        "9×9×9=729. One real cube root.",
    ),
    _q(
        "cc_ii_cc4_6", "II", "CC4",
        "evaluate_square",
        "Evaluate 7².",
        ["49", "14", "21", "7"],
        0,
        "7×7=49.",
    ),
    _q(
        "cc_ii_cc4_7", "II", "CC4",
        "cube_fraction_height",
        "A cubical snake tank has volume 216 cubic inches. The sand is ⅓ the height of the tank. "
        "How high is the sand?",
        ["2 in", "6 in", "72 in", "3 in"],
        0,
        "Edge = ∛216 = 6 in. Sand height = (1/3)×6 = 2 in.",
    ),
    _q(
        "cc_ii_cc4_8", "II", "CC4",
        "order_of_ops",
        "Evaluate.\n10 · 4 − 2(4² + 8) ÷ 2 · 3 + 1",
        ["−31", "35", "5", "−11"],
        0,
        "4²+8=24, 2×24=48, 10×4=40, 48÷2=24, 24×3=72, 40−72+1=−31.",
    ),
    _q(
        "cc_ii_cc5_1", "II", "CC5",
        "perimeter_to_area",
        "Saleem is making enough BBQ to fit on a square plate with perimeter 24 cm. "
        "How much area does Saleem have to work with?",
        ["36 cm²", "24 cm²", "6 cm²", "96 cm²"],
        0,
        "Side = 24/4 = 6 cm. Area = 6² = 36 cm².",
    ),
    _q(
        "cc_ii_cc5_2", "II", "CC5",
        "cube_compare_height",
        "The biggest Rubik’s cube in the world has volume 343 ft³. If Cris is 5 ft tall, "
        "how much taller is this Rubik’s cube than Cris?",
        ["2 ft", "7 ft", "338 ft", "12 ft"],
        0,
        "Edge = ∛343 = 7 ft. 7 − 5 = 2 ft taller.",
    ),
    _q(
        "cc_ii_cc5_3", "II", "CC5",
        "order_of_ops",
        "Simplify.\n1 − 4(3 + 12)",
        ["−59", "−47", "61", "−15"],
        0,
        "3+12=15, 4×15=60, 1−60=−59.",
    ),
    _q(
        "cc_ii_cc5_4", "II", "CC5",
        "order_of_ops",
        "Simplify.\n24 ÷ 4 − 5 · 7 + 9² ÷ 3",
        ["−2", "27", "52", "6"],
        0,
        "24÷4=6, 5·7=35, 9²=81, 81÷3=27. 6−35+27=−2.",
    ),
    # ── III  Rational and Irrational (CC4, CC5) ──
    _q(
        "cc_iii_cc4_9", "III", "CC4",
        "between_perfect_squares",
        "Which of the following is between 8 and 9?",
        ["√65", "√60", "√85", "√20"],
        0,
        "8²=64 and 9²=81, so √65 is between 8 and 9.",
    ),
    _q(
        "cc_iii_cc4_10", "III", "CC4",
        "identify_irrational",
        "Which of these is an irrational number?",
        ["√20", "√16", "0.24 with a bar over 24", "0.242424…"],
        0,
        "√16=4 is rational. Repeating decimals are rational. √20 is not a perfect square.",
    ),
    _q(
        "cc_iii_cc4_11", "III", "CC4",
        "fraction_to_percent_method",
        "Explain how to convert a fraction to a percentage.",
        [
            "Divide numerator by denominator, then multiply by 100",
            "Add 100 to the numerator",
            "Multiply numerator and denominator by 100, then add them",
            "Flip the fraction and multiply by 10",
        ],
        0,
        "a/b = a÷b. Then ×100 to make a percent. (Or ×100 first, then divide by b.)",
    ),
    _q(
        "cc_iii_cc4_12", "III", "CC4",
        "estimate_root",
        "Estimate √10 to the nearest tenth.",
        ["3.2", "3.1", "3.0", "3.3"],
        0,
        "3.1²=9.61 and 3.2²=10.24. 10 is closer to 10.24, so √10≈3.2.",
    ),
    _q(
        "cc_iii_cc4_13", "III", "CC4",
        "repeating_to_fraction",
        "USING THE METHOD SHOWN IN CLASS. Write 0.24 with the bar ONLY over the 4 as a fraction "
        "in simplest form. (That is 0.2444…)",
        ["11/45", "24/99", "6/25", "22/90"],
        0,
        "Let x=0.2444…. 10x=2.444…, 100x=24.444…. Subtract: 90x=22, x=22/90=11/45.",
    ),
    _q(
        "cc_iii_cc5_5", "III", "CC5",
        "identify_rational_set",
        "Which of the following are rational? You may need more than one.\n"
        "4.8 with a bar over 8,  √65,  √64,  π,  7/8,  ∛125",
        [
            "4.8̅, √64, 7/8, and ∛125",
            "√65 and π only",
            "All six numbers",
            "√64 and 7/8 only",
        ],
        0,
        "Repeating 4.8, √64=8, 7/8, and ∛125=5 are rational. √65 and π are irrational.",
    ),
    _q(
        "cc_iii_cc5_6", "III", "CC5",
        "estimate_root",
        "Estimate √70 to the nearest tenth.",
        ["8.4", "8.3", "8.0", "9.0"],
        0,
        "8.3²=68.89 and 8.4²=70.56. 70 is closer to 70.56, so √70≈8.4.",
    ),
    _q(
        "cc_iii_cc5_7", "III", "CC5",
        "repeating_to_fraction",
        "USING THE METHOD SHOWN IN CLASS. Write 0.012 with the bar ONLY over the 12 as a fraction "
        "in simplest form. (That is 0.0121212…)",
        ["2/165", "12/999", "12/990", "1/83"],
        0,
        "x=0.0121212…. 100x=1.21212…, 100x−x=1.2, 99x=1.2, x=12/990=2/165.",
    ),
    # ── IV  Exponent Properties (CC5 + later form) ──
    _q(
        "cc_iv_cc5_8", "IV", "CC5",
        "product_same_base",
        "Express with only positive exponents.\n8⁻¹⁰ · 8⁸",
        ["1/8²", "8⁻²", "8¹⁸", "1/8¹⁸"],
        0,
        "Add exponents: 8⁻¹⁰⁺⁸=8⁻²=1/8².",
    ),
    _q(
        "cc_iv_cc5_9", "IV", "CC5",
        "quotient_variables",
        "Express with only positive exponents.\n(x¹² y⁹) / (x⁻¹⁸ y)",
        ["x³⁰ y⁸", "x⁻⁶ y⁸", "x³⁰ / y¹⁰", "x⁶ y⁸"],
        0,
        "x¹²⁻(⁻¹⁸)=x³⁰ and y⁹⁻¹=y⁸.",
    ),
    _q(
        "cc_iv_cc5_10", "IV", "CC5",
        "power_of_power_solve",
        "Solve for x.\n(7ˣ)⁵ = 7¹⁰⁰",
        ["x = 20", "x = 5", "x = 95", "x = 500"],
        0,
        "(7ˣ)⁵=7⁵ˣ. So 5x=100 and x=20.",
    ),
    _q(
        "cc_iv_later_1", "IV", "later form",
        "product_of_powers",
        "Simplify. Write the final answer with only positive exponents.\n(6x⁶y⁷)(7x⁴y)",
        ["42 x¹⁰ y⁸", "13 x¹⁰ y⁸", "42 x²⁴ y⁷", "42 x² y⁶"],
        0,
        "6×7=42, x⁶x⁴=x¹⁰, y⁷y=y⁸.",
    ),
    _q(
        "cc_iv_later_2", "IV", "later form",
        "quotient_negative",
        "Simplify. Write the final answer with only positive exponents.\n(60 x⁴ y⁻⁵) / (4 x¹⁰ y²⁰)",
        ["15 / (x⁶ y²⁵)", "15 x⁶ / y²⁵", "15 x¹⁴ y⁻²⁵", "64 / (x⁶ y²⁵)"],
        0,
        "60/4=15, x⁴⁻¹⁰=x⁻⁶, y⁻⁵⁻²⁰=y⁻²⁵, so 15/(x⁶ y²⁵).",
    ),
    _q(
        "cc_iv_later_3", "IV", "later form",
        "negative_to_reciprocal",
        "Simplify. Write the final answer with only positive exponents.\n5x⁻⁴ / (9 y¹⁰)",
        ["5 / (9 x⁴ y¹⁰)", "5 x⁴ / (9 y¹⁰)", "45 / (x⁴ y¹⁰)", "5x⁴ y¹⁰ / 9"],
        0,
        "x⁻⁴ = 1/x⁴, so 5/(9 x⁴ y¹⁰).",
    ),
    # ── V  Scientific Notation (later school form; not on CC1–CC5) ──
    _q(
        "cc_v_later_4", "V", "later form",
        "convert_to_sci",
        "Convert 60,000,000 to scientific notation.",
        ["6 × 10⁷", "6 × 10⁶", "60 × 10⁶", "6 × 10⁸"],
        0,
        "6.0 with the decimal moved 7 places: 6 × 10⁷.",
    ),
    _q(
        "cc_v_later_5", "V", "later form",
        "multiply_sci",
        "Simplify. Write the final answer in scientific notation.\n(6.2 × 10¹⁵) · (2 × 10³)",
        ["1.24 × 10¹⁹", "12.4 × 10¹⁸", "8.2 × 10¹⁸", "1.24 × 10¹⁸"],
        0,
        "6.2×2=12.4 and 10¹⁵×10³=10¹⁸, so 12.4×10¹⁸=1.24×10¹⁹.",
    ),
    _q(
        "cc_v_later_6", "V", "later form",
        "subtract_sci_word",
        "Last year, Bobissa ate her Halloween candy in 8.4 × 10⁴ seconds. This year she did it "
        "in 4 × 10² seconds. How much longer did it take her last year? Write scientific notation.",
        ["8.36 × 10⁴ seconds", "4.4 × 10⁴ seconds", "8.4 × 10² seconds", "4 × 10⁶ seconds"],
        0,
        "4×10²=0.04×10⁴. 8.4×10⁴ − 0.04×10⁴ = 8.36×10⁴ seconds.",
    ),
]


def list_sections() -> list[dict]:
    return [dict(SECTIONS[key]) for key in ("I", "II", "III", "IV", "V")]


def get_section(section_id: str) -> dict | None:
    return SECTIONS.get(str(section_id).strip().upper() or "")


def seeds_for_section(section_id: str) -> list[dict]:
    sid = str(section_id).strip().upper()
    return [dict(q) for q in FORM_SEED_QUESTIONS if q["section"] == sid]


def session_count_for_section(section_id: str) -> int:
    info = get_section(section_id)
    return int(info["session_count"]) if info else 5
