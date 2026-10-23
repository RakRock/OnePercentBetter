"""Math 3 Friday Concept Check — Unit 1 sections I–V and Unit 6 packets VI-1 / VI-2 / VI-3.

Seeds are the actual problems from Arjun's CC1–CC5 papers (plus Scientific
Notation items from a later school form, because CC1–CC5 did not include V)
and the Unit 6 packets VI-1 Representing Patterns, VI-2 Using Patterns, and
VI-3 Solving Linear Equations with Models.
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
        "unit_id": 1,
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
        "unit_id": 1,
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
        "unit_id": 1,
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
        "unit_id": 1,
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
        "session_count": 5,
        "emoji": "🔬",
        "color": "#db2777",
        "unit_id": 1,
    },
    "VI": {
        "id": "VI",
        "roman": "VI",
        "title": "Unit 6 — Patterns and Modeling",
        "short": "Tables, square/rect/triangle, bags and cubes",
        "note_files": [
            "activity_1_representing_patterns.md",
            "activity_2_using_patterns_expressions.md",
            "activity_3_solving_equations_with_models.md",
        ],
        "session_count": 5,
        "emoji": "⬛",
        "color": "#0f766e",
        "unit_id": 6,
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
        "category_label": stem.replace("_", " ").title(),
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
    _q(
        "cc_v_est", "V", "later form",
        "estimate_sci",
        "Estimate 8,345,000,676,709 in scientific notation (nearest hundredth in the coefficient).",
        ["8.35 × 10¹²", "8.34 × 10¹²", "8.35 × 10⁹", "83.5 × 10¹¹"],
        0,
        "Round to 8.35 and move the decimal 12 places: 8.35 × 10¹².",
    ),
    _q(
        "cc_v_add", "V", "later form",
        "add_sci",
        "Simplify. Write the final answer in scientific notation.\n(6.5 × 10¹⁵) + (2 × 10¹³)",
        ["6.52 × 10¹⁵", "8.5 × 10¹⁵", "6.5 × 10¹⁵", "6.52 × 10¹³"],
        0,
        "2 × 10¹³ = 0.02 × 10¹⁵. 6.5 + 0.02 = 6.52, so 6.52 × 10¹⁵.",
    ),
    _q(
        "cc_v_div", "V", "later form",
        "divide_sci",
        "Simplify. Write the final answer in proper scientific notation.\n(3 × 10³²) ÷ (4 × 10⁸)",
        ["7.5 × 10²³", "0.75 × 10²⁴", "7.5 × 10²⁴", "3/4 × 10²⁴"],
        0,
        "3/4 = 0.75 and 32 − 8 = 24, so 0.75 × 10²⁴ = 7.5 × 10²³.",
    ),
    _q(
        "cc_v_to_standard", "V", "later form",
        "sci_to_standard",
        "Write 4.2 × 10⁵ in standard form.",
        ["420,000", "42,000", "4,200,000", "0.000042"],
        0,
        "Move the decimal 5 places right: 420,000.",
    ),
    _q(
        "cc_v_form_check", "V", "later form",
        "rewrite_sci_form",
        "Which is written in proper scientific notation?",
        ["3.5 × 10⁴", "35 × 10³", "0.35 × 10⁵", "3.5 × 4¹⁰"],
        0,
        "The coefficient must satisfy 1 ≤ |a| < 10, and the 10 is the base.",
    ),
    # ── VI  Representing Patterns (VI-1 packet) ──
    _q(
        "cc_vi_vi1_expr", "VI", "VI-1",
        "expression_in_n",
        "Figure 1 has 1 dot, Figure 2 has 3 dots, Figure 3 has 5 dots. "
        "Let n be the figure number. Which expression gives the number of dots in figure n?",
        ["2n − 1", "2n", "2n + 1", "n + 2"],
        0,
        "The counts are 1, 3, 5, … (odd numbers). Each step adds 2, and Figure 1 is 1, so 2n − 1.",
    ),
    _q(
        "cc_vi_vi1_sub", "VI", "VI-1",
        "substitute_n",
        "The number of dots in figure n is 2n − 1. What value of n do you substitute to find the number of dots in the 3rd figure?",
        ["n = 3", "n = 5", "n = 2", "n = 100"],
        0,
        "The 3rd figure means figure number n = 3.",
    ),
    _q(
        "cc_vi_vi1_far", "VI", "VI-1",
        "far_figure",
        "Figure 1 has 1 dot, Figure 2 has 3 dots, Figure 3 has 5 dots. How many dots are in the 100th figure?",
        ["199", "200", "201", "101"],
        0,
        "The rule is 2n − 1. For n = 100: 2(100) − 1 = 199.",
    ),
    _q(
        "cc_vi_vi1_name", "VI", "VI-1",
        "constant_difference_name",
        "When the difference of consecutive terms is always the same, it is called:",
        ["a constant difference", "a ratio", "a square number", "a Fibonacci sequence"],
        0,
        "A repeated same gap (here +2) is a constant difference.",
    ),
    _q(
        "cc_vi_vi1_relate", "VI", "VI-1",
        "difference_relates",
        "In the dots table the difference column is 2, 2, 2, … The expression for the number of dots is 2n − 1. "
        "How does the difference column relate to the pattern?",
        [
            "You add 2 dots each figure, so the coefficient of n is 2",
            "The 100th figure has 2 dots",
            "n is always 2",
            "The first figure has 2 dots",
        ],
        0,
        "The constant difference is how many new dots appear each figure, and it is the coefficient of n.",
    ),
    _q(
        "cc_vi_vi1_table", "VI", "VI-1",
        "fill_table",
        "Figure 1 has 1 dot, Figure 2 has 3 dots, Figure 3 has 5 dots. How many dots are in Figure 6?",
        ["11", "12", "9", "13"],
        0,
        "Add 2 each time: 1, 3, 5, 7, 9, 11. Or 2(6) − 1 = 11.",
    ),
    _q(
        "cc_vi_pracA_d", "VI", "VI-1",
        "constant_difference_value",
        "A V of dots: Figure 1 has 3 dots, Figure 2 has 5 dots, Figure 3 has 7 dots. What is the constant difference?",
        ["2", "3", "4", "1"],
        0,
        "5 − 3 = 2 and 7 − 5 = 2.",
    ),
    _q(
        "cc_vi_pracA_expr", "VI", "VI-1",
        "expression_in_n",
        "A V of dots: Figure 1 has 3 dots, Figure 2 has 5 dots, Figure 3 has 7 dots. "
        "Let n be the figure number. Which expression gives the number of dots in figure n?",
        ["2n + 1", "2n − 1", "3n", "n + 3"],
        0,
        "Start at 3 and add 2 each time: 3 + 2(n − 1) = 2n + 1.",
    ),
    _q(
        "cc_vi_pracA_51", "VI", "VI-1",
        "far_figure",
        "A V of dots grows as 3, 5, 7, … (constant difference 2). How many dots are in the 51st figure?",
        ["103", "102", "101", "51"],
        0,
        "Expression 2n + 1. For n = 51: 2(51) + 1 = 103.",
    ),
    _q(
        "cc_vi_pracB_d", "VI", "VI-1",
        "constant_difference_value",
        "A stair of squares: Figure 1 has 3 squares, Figure 2 has 5 squares, Figure 3 has 7 squares. "
        "What is the constant difference?",
        ["2", "3", "4", "1"],
        0,
        "5 − 3 = 2 and 7 − 5 = 2.",
    ),
    _q(
        "cc_vi_pracB_expr", "VI", "VI-1",
        "expression_in_n",
        "A stair of squares: Figure 1 has 3 squares, Figure 2 has 5 squares, Figure 3 has 7 squares. "
        "Let n be the figure number. Which expression gives the number of squares in figure n?",
        ["2n + 1", "2n − 1", "n²", "3n"],
        0,
        "Same growth as 3, 5, 7, … so 2n + 1.",
    ),
    _q(
        "cc_vi_pracB_100", "VI", "VI-1",
        "far_figure",
        "A stair of squares grows as 3, 5, 7, … How many squares are in the 100th figure?",
        ["201", "199", "200", "103"],
        0,
        "Expression 2n + 1. For n = 100: 2(100) + 1 = 201.",
    ),
    # ── VI-2  Using Patterns to Write and Evaluate Expressions ──
    _q(
        "cc_vi2_sq_next", "VI", "VI-2",
        "square_next_figures",
        "Square numbers: Figure 1 has 1 dot, Figure 2 has 4 dots, Figure 3 has 9 dots. "
        "How many dots are in the 4th, 5th, and 6th figures?",
        ["16, 25, 36", "8, 10, 12", "9, 16, 25", "16, 20, 24"],
        0,
        "Each figure is an n by n square: 4²=16, 5²=25, 6²=36.",
    ),
    _q(
        "cc_vi2_sq_const", "VI", "VI-2",
        "square_constant_diff",
        "Square numbers go 1, 4, 9, 16, …. Does this pattern have a constant difference?",
        [
            "No — the gaps are 3, 5, 7, … and they keep growing",
            "Yes — the difference is always 3",
            "Yes — the difference is always 4",
            "No — square numbers skip every other figure",
        ],
        0,
        "4−1=3, 9−4=5, 16−9=7. The difference is not constant.",
    ),
    _q(
        "cc_vi2_sq_nth", "VI", "VI-2",
        "square_nth",
        "Square numbers: Figure 1 has 1 dot, Figure 2 has 4, Figure 3 has 9. "
        "How many dots are in the nth figure?",
        ["n²", "2n − 1", "n(n + 1)", "n(n + 1) / 2"],
        0,
        "Figure n is an n by n square, so n² dots.",
    ),
    _q(
        "cc_vi2_sq_40", "VI", "VI-2",
        "square_far",
        "How many dots are in the 40th square-number figure?",
        ["1600", "40", "80", "1640"],
        0,
        "n² with n = 40: 40² = 1600.",
    ),
    _q(
        "cc_vi2_rect_nth", "VI", "VI-2",
        "rectangular_nth",
        "Rectangular numbers: Figure 1 is 1×2 (2 dots), Figure 2 is 2×3 (6 dots), "
        "Figure 3 is 3×4 (12 dots). How many dots are in the nth figure?",
        ["n(n + 1)", "n²", "2n", "n(n + 1) / 2"],
        0,
        "n rows and (n + 1) columns: n(n + 1) dots.",
    ),
    _q(
        "cc_vi2_rect_99", "VI", "VI-2",
        "rectangular_far",
        "Rectangular numbers use n(n + 1) dots. How many dots are in the 99th figure?",
        ["9900", "9801", "99", "4950"],
        0,
        "99 × 100 = 9900. (99² would be 9801; that is the square pattern.)",
    ),
    _q(
        "cc_vi2_tri_nth", "VI", "VI-2",
        "triangular_nth",
        "Triangular numbers: Figure 1 has 1 dot, Figure 2 has 3, Figure 3 has 6. "
        "Write an expression for the number of dots in figure n.",
        ["n(n + 1) / 2", "n²", "n(n + 1)", "2n − 1"],
        0,
        "Rows 1 + 2 + … + n = n(n + 1)/2. That is half of the n by (n + 1) rectangle.",
    ),
    _q(
        "cc_vi2_classify_72", "VI", "VI-2",
        "classify_special",
        "Using the formulas from class, 72 is which of these?",
        [
            "Rectangular only (8 × 9)",
            "Square only",
            "Triangular only",
            "Square and rectangular",
        ],
        0,
        "n²=72 is not a whole n. n(n+1)=72 → 8×9=72, so rectangular. "
        "n(n+1)/2=72 → n(n+1)=144, which is not consecutive integers.",
    ),
    _q(
        "cc_vi2_pent_10", "VI", "VI-2",
        "pentagon_far",
        "Pentagon walkway: each side is 1 cm. Figure 1 is one pentagon (perimeter 5 cm). "
        "Each new pentagon shares one full side, so the perimeter grows 5, 8, 11, 14, … cm. "
        "What is the perimeter of the 10th figure?",
        ["32 cm", "50 cm", "30 cm", "35 cm"],
        0,
        "Constant difference 3. 5 + 3(10 − 1) = 5 + 27 = 32 cm.",
    ),
    _q(
        "cc_vi2_pent_expr", "VI", "VI-2",
        "pentagon_expr",
        "Same pentagon walkway (first perimeter 5 cm, add 3 cm each figure). "
        "Which expression gives the perimeter of the nth figure?",
        ["5 + 3(n − 1)  or  3n + 2", "5n", "5 + 5(n − 1)", "n + 3"],
        0,
        "First term 5, constant difference 3 → 5 + 3(n − 1) = 3n + 2.",
    ),
    _q(
        "cc_vi2_pent_50", "VI", "VI-2",
        "pentagon_eval",
        "Pentagon walkway perimeter is 3n + 2 centimeters. What is the perimeter of the 50th figure?",
        ["152 cm", "150 cm", "53 cm", "250 cm"],
        0,
        "3(50) + 2 = 150 + 2 = 152 cm.",
    ),
    _q(
        "cc_vi2_oct_40", "VI", "VI-2",
        "octagon_walkway",
        "Octagon walkway: each side is 1 m. Figure 1 is one octagon (8 m). "
        "Each new octagon shares one full side, so perimeters are 8, 14, 20, … m. "
        "What is the perimeter of a walkway of 40 octagonal blocks?",
        ["242 m", "240 m", "320 m", "48 m"],
        0,
        "Add 6 m each time: 8 + 6(40 − 1) = 6(40) + 2 = 242 m.",
    ),
    # ── VI-3  Solving Linear Equations with Models ──
    _q(
        "cc_vi3_bag_count", "VI", "VI-3",
        "scale_bag_count",
        "A balanced scale has 2 bags and 3 cubes on the left pan and 7 cubes on the right pan. "
        "Each bag holds the same number of cubes. How many cubes are in each bag?",
        ["2", "3", "4", "5"],
        0,
        "2x + 3 = 7. Subtract 3: 2x = 4. Divide by 2: x = 2.",
    ),
    _q(
        "cc_vi3_bag_eq", "VI", "VI-3",
        "scale_to_equation",
        "A balanced scale has 2 bags and 3 cubes on one side and 7 cubes on the other. "
        "If a bag is x cubes, which equation matches the scale?",
        ["2x + 3 = 7", "2x = 7", "2x + 3 = 3", "x + 3 = 7"],
        0,
        "Two bags and three cubes balance seven cubes: 2x + 3 = 7.",
    ),
    _q(
        "cc_vi3_three_bags", "VI", "VI-3",
        "three_bags_twelve",
        "3 bags are on one side of a balanced scale and 12 cubes are on the other side. "
        "How many cubes are in each bag?",
        ["4", "3", "12", "9"],
        0,
        "3x = 12, so x = 4. Check: 3 bags × 4 cubes = 12 cubes.",
    ),
    _q(
        "cc_vi3_eq3", "VI", "VI-3",
        "write_equation_bags",
        "3 bags on one side, 12 cubes on the other, scale balanced. Which equation represents the scale?",
        ["3x = 12", "3 + x = 12", "x = 12", "3x + 12 = 0"],
        0,
        "Three unknown bags balance 12 cubes: 3x = 12.",
    ),
    _q(
        "cc_vi3_two_bags_four", "VI", "VI-3",
        "two_bags_loose_cubes",
        "2 bags and 4 cubes are on one side of a balanced scale and 10 cubes are on the other side. "
        "How many cubes are in each bag?",
        ["3", "2", "5", "6"],
        0,
        "2x + 4 = 10. Subtract 4: 2x = 6. Divide by 2: x = 3.",
    ),
    _q(
        "cc_vi3_eq4", "VI", "VI-3",
        "write_equation_mixed",
        "2 bags and 4 cubes vs 10 cubes, scale balanced. Which equation represents the scale?",
        ["2x + 4 = 10", "2x = 10", "2x + 4 = 4", "x + 4 = 10"],
        0,
        "Two bags plus four cubes balance ten cubes: 2x + 4 = 10.",
    ),
    _q(
        "cc_vi3_inverse_first", "VI", "VI-3",
        "inverse_first_step",
        "Solve 2x + 4 = 10 using inverse operations. What is the first step?",
        [
            "Subtract 4 from both sides",
            "Divide both sides by 2",
            "Subtract 2x from both sides",
            "Add 4 to both sides",
        ],
        0,
        "Undo the +4 first so the bags are alone with cubes: 2x = 6, then divide by 2.",
    ),
    _q(
        "cc_vi3_solve_check", "VI", "VI-3",
        "solve_and_check",
        "Use inverse operations to solve 2x + 4 = 10. What is x?",
        ["x = 3", "x = 7", "x = 5", "x = 2"],
        0,
        "2x + 4 − 4 = 10 − 4, so 2x = 6, x = 3. Check: 2(3) + 4 = 10.",
    ),
]


def list_sections() -> list[dict]:
    return [dict(SECTIONS[key]) for key in ("I", "II", "III", "IV", "V", "VI")]


def get_section(section_id: str) -> dict | None:
    sid = str(section_id).strip().upper() or ""
    if sid in {"VI-1", "VI-2", "VI-3", "VI1", "VI2", "VI3"}:
        sid = "VI"
    return SECTIONS.get(sid)


def seeds_for_section(section_id: str) -> list[dict]:
    info = get_section(section_id)
    sid = info["id"] if info else str(section_id).strip().upper()
    return [dict(q) for q in FORM_SEED_QUESTIONS if q["section"] == sid]


def session_count_for_section(section_id: str) -> int:
    info = get_section(section_id)
    return int(info["session_count"]) if info else 5


def build_session_report(questions: list[dict], answers: list[dict]) -> dict:
    """Score + per-stem breakdown for the Concept Check results email."""
    buckets: dict[str, dict[str, int]] = {}
    for q, ans in zip(questions, answers):
        name = str(q.get("category_label") or q.get("stem") or "Concept Check")
        name = name.replace("_", " ").title() if "_" in name else name
        stats = buckets.setdefault(name, {"correct": 0, "total": 0})
        stats["total"] += 1
        if ans.get("correct"):
            stats["correct"] += 1
    strengths: list[dict] = []
    needs_revision: list[dict] = []
    for name, stats in buckets.items():
        pct = int(100 * stats["correct"] / stats["total"]) if stats["total"] else 0
        row = {
            "name": name,
            "correct": stats["correct"],
            "total": stats["total"],
            "pct": pct,
            "emoji": "✅" if pct >= 80 else "📝",
        }
        if pct >= 80:
            strengths.append(row)
        else:
            needs_revision.append({**row, "tip": f"Review {name}."})
    strengths.sort(key=lambda e: (-e["pct"], e["name"]))
    needs_revision.sort(key=lambda e: (e["pct"], e["name"]))
    correct_count = sum(1 for a in answers if a.get("correct"))
    total = len(answers)
    score_pct = int(100 * correct_count / total) if total else 0
    if needs_revision:
        tip = f"{needs_revision[0]['name']}: {needs_revision[0]['tip']}"
    elif score_pct == 100:
        tip = "Perfect Concept Check — try a fresh paper to stay sharp."
    else:
        tip = "Solid session. Start a fresh paper for more practice."
    return {
        "correct_count": correct_count,
        "total": total,
        "score_pct": score_pct,
        "strengths": strengths,
        "needs_revision": needs_revision,
        "tip": tip,
    }
