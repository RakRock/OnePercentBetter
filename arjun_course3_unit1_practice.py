"""Arjun Course 3 Unit 1 — Numerical Relationships practice bank."""

from __future__ import annotations

UNIT1_CATEGORIES = {
    "patterns": {"name": "Patterns", "emoji": "🔢", "color": "#3b82f6", "weight": 1},
    "fractions": {"name": "Fractions", "emoji": "🍕", "color": "#f97316", "weight": 2},
    "powers_roots": {"name": "Powers & Roots", "emoji": "²", "color": "#8b5cf6", "weight": 1},
    "rational_numbers": {"name": "Rational Numbers", "emoji": "🔁", "color": "#10b981", "weight": 1},
    "irrational_numbers": {"name": "Irrational Numbers", "emoji": "π", "color": "#ef4444", "weight": 1},
    "exponents": {"name": "Exponents", "emoji": "⚡", "color": "#f59e0b", "weight": 2},
    "scientific_notation": {"name": "Scientific Notation", "emoji": "🔬", "color": "#06b6d4", "weight": 1},
    "sci_notation_ops": {"name": "Sci Notation Ops", "emoji": "✖️", "color": "#6366f1", "weight": 1},
}

UNIT1_CATEGORY_ACTIVITY = {
    "patterns": "activity_1_investigating_patterns",
    "fractions": "activity_2_operations_with_fractions",
    "powers_roots": "activity_3_powers_and_roots",
    "rational_numbers": "activity_4_rational_numbers",
    "irrational_numbers": "activity_5_rational_irrational_numbers",
    "exponents": "activity_6_properties_of_exponents",
    "scientific_notation": "activity_7_scientific_notation",
    "sci_notation_ops": "activity_8_operations_scientific_notation",
}

UNIT1_REVISION_TIPS = {
    "patterns": "Check several differences or ratios before guessing the next term.",
    "fractions": "Add/subtract with LCD first; multiply tops and bottoms separately.",
    "powers_roots": "Area = side²; volume = edge³; √ undoes squaring.",
    "rational_numbers": "Divide to get decimal; ×100 for percent.",
    "irrational_numbers": "Non-perfect roots and π are irrational; √16 = 4 is rational.",
    "exponents": "Same base: multiply → add exponents; divide → subtract.",
    "scientific_notation": "Coefficient must satisfy 1 ≤ |a| < 10.",
    "sci_notation_ops": "Match powers of 10 before adding coefficients.",
}

UNIT1_QUESTION_BANK: list[dict] = [
    # ── Patterns (5) ──
    {
        "id": "u1_pat1", "category": "patterns",
        "question": (
            "Look at this number pattern: 3, 7, 11, 15, … "
            "Each number is 4 more than the one before it. "
            "What are the next two numbers in the pattern?"
        ),
        "options": ["17, 19", "19, 23", "15, 19", "23, 27"],
        "answer": 1,
        "explanation": "Add 4 each time: 15 + 4 = 19, then 19 + 4 = 23.",
    },
    {
        "id": "u1_pat2", "category": "patterns",
        "question": (
            "This is a Fibonacci pattern: 1, 1, 2, 3, 5, 8, … "
            "Each number is the sum of the two numbers right before it "
            "(for example, 3 = 1 + 2). What are the next three numbers?"
        ),
        "options": ["10, 11, 12", "13, 21, 34", "9, 14, 20", "11, 16, 22"],
        "answer": 1,
        "explanation": "8 + 5 = 13, then 13 + 8 = 21, then 21 + 13 = 34.",
    },
    {
        "id": "u1_pat3", "category": "patterns",
        "question": (
            "Look at this number pattern: 3, 6, 12, 24, … "
            "Each number is double the one before it. "
            "Is the pattern increasing or decreasing, and what is the next number?"
        ),
        "options": ["Decreasing; 12", "Increasing; 48", "Increasing; 36", "Constant; 24"],
        "answer": 1,
        "explanation": "The numbers go up (increasing). Double 24 to get 48.",
    },
    {
        "id": "u1_pat4", "category": "patterns",
        "question": (
            "Look at this number pattern: 17, 14, 11, 8, … "
            "Each number is 3 less than the one before it. "
            "What is the next number in the pattern?"
        ),
        "options": ["11", "6", "5", "7"],
        "answer": 2,
        "explanation": "Subtract 3 from 8: the next number is 5.",
    },
    {
        "id": "u1_pat5", "category": "patterns",
        "question": (
            "You are making a dot pattern with rows of dots. "
            "Figure 1 has 3 dots, Figure 2 has 7 dots, and Figure 3 has 11 dots. "
            "Each new figure has 4 more dots than the figure before it. "
            "How many dots will Figure 9 have?"
        ),
        "options": ["31 dots", "35 dots", "39 dots", "27 dots"],
        "answer": 1,
        "explanation": (
            "Figure 1 has 3 dots. You add 4 dots eight times to reach Figure 9 "
            "(from Figure 1 to Figure 9 is 8 steps). "
            "3 + 4 × 8 = 35 dots."
        ),
    },
    # ── Fractions (6) ──
    {
        "id": "u1_frac1", "category": "fractions",
        "question": (
            "Add these fractions and write the answer in simplest form: "
            "What is 3/5 + 4/6?"
        ),
        "options": ["13/6", "1 4/15", "7/11", "2 1/6"],
        "answer": 1,
        "explanation": (
            "Find the LCD (30): 3/5 = 18/30 and 4/6 = 20/30. "
            "Add: 18/30 + 20/30 = 38/30 = 19/15 = 1 4/15."
        ),
    },
    {
        "id": "u1_frac2", "category": "fractions",
        "question": (
            "Subtract and write the answer in simplest form: "
            "What is 5/8 − 1/3?"
        ),
        "options": ["4/5", "7/24", "1/24", "4/24"],
        "answer": 1,
        "explanation": "LCD 24: 15/24 − 8/24 = 7/24.",
    },
    {
        "id": "u1_frac3", "category": "fractions",
        "question": (
            "Multiply these two fractions and write the answer in simplest form: "
            "What is 2/5 × 7/12?"
        ),
        "options": ["14/17", "7/30", "9/17", "14/60 (not fully simplified)"],
        "answer": 1,
        "explanation": (
            "Multiply tops: 2 × 7 = 14. Multiply bottoms: 5 × 12 = 60. "
            "So 14/60, which simplifies to 7/30."
        ),
    },
    {
        "id": "u1_frac4", "category": "fractions",
        "question": (
            "Judy has 4 2/3 yards of fabric and Marie has 5 1/2 yards. "
            "How many yards of fabric do they have together?"
        ),
        "options": ["9 1/6 yd", "10 1/6 yd", "9 5/6 yd", "10 5/6 yd"],
        "answer": 1,
        "explanation": "14/3 + 11/2 = 28/6 + 33/6 = 61/6 = 10 1/6 yards.",
    },
    {
        "id": "u1_frac5", "category": "fractions",
        "question": (
            "Carmen weighed 7 1/2 pounds at birth and Angelo weighed 5 1/4 pounds. "
            "How many pounds heavier was Carmen than Angelo?"
        ),
        "options": ["2 lb", "2 1/4 lb", "2 1/2 lb", "1 3/4 lb"],
        "answer": 1,
        "explanation": "7.5 − 5.25 = 2.25 = 2 1/4 pounds.",
    },
    {
        "id": "u1_frac6", "category": "fractions",
        "question": (
            "You are mixing trail mix. You add 1 1/2 cups of nuts, 3/4 cup of raisins, "
            "and 2/3 cup of chocolate chips. How many cups of trail mix is that in all?"
        ),
        "options": ["2 11/12 cups", "3 cups", "2 1/2 cups", "3 1/12 cups"],
        "answer": 0,
        "explanation": "LCD 12: 18/12 + 9/12 + 8/12 = 35/12 = 2 11/12 cups.",
    },
    # ── Powers & roots (5) ──
    {
        "id": "u1_pow1", "category": "powers_roots",
        "question": "A square has side 7.2 in. What is its area?",
        "options": ["14.4 in²", "51.84 in²", "28.8 in²", "72 in²"],
        "answer": 1,
        "explanation": "A = s² = 7.2² = 51.84 in².",
    },
    {
        "id": "u1_pow2", "category": "powers_roots",
        "question": "Solve x² = 81 (positive root for length).",
        "options": ["8", "9", "81", "±9 only — not a single length"],
        "answer": 1,
        "explanation": "9² = 81; use 9 for a length.",
    },
    {
        "id": "u1_pow3", "category": "powers_roots",
        "question": "Square area 16 cm²; trim 1 cm from each side. New area?",
        "options": ["9 cm²", "4 cm²", "8 cm²", "12 cm²"],
        "answer": 1,
        "explanation": "Side was 4; new side 2; 2² = 4 cm².",
    },
    {
        "id": "u1_pow4", "category": "powers_roots",
        "question": "Cube volume is 216 ft³. Edge length?",
        "options": ["6 ft", "36 ft", "72 ft", "18 ft"],
        "answer": 0,
        "explanation": "6³ = 216.",
    },
    {
        "id": "u1_pow5", "category": "powers_roots",
        "question": "Which is NOT equal to 8²?",
        "options": ["64", "8 × 8", "Eight multiplied by two", "2⁶"],
        "answer": 2,
        "explanation": "8 × 2 = 16, not 64.",
    },
    # ── Rational numbers (5) ──
    {
        "id": "u1_rat1", "category": "rational_numbers",
        "question": "Write 3/5 as a decimal and percent.",
        "options": ["0.35 and 35%", "0.6 and 60%", "0.53 and 53%", "3.5 and 350%"],
        "answer": 1,
        "explanation": "3 ÷ 5 = 0.6 = 60%.",
    },
    {
        "id": "u1_rat2", "category": "rational_numbers",
        "question": "0.8 as a fraction and percent?",
        "options": ["8/10 and 8%", "4/5 and 80%", "8/100 and 80%", "4/5 and 8%"],
        "answer": 1,
        "explanation": "0.8 = 4/5 = 80%.",
    },
    {
        "id": "u1_rat3", "category": "rational_numbers",
        "question": "Which is NOT equivalent to 60/80?",
        "options": ["3/4", "0.75", "0.6", "75%"],
        "answer": 2,
        "explanation": "60/80 = 3/4 = 0.75; 0.6 is wrong.",
    },
    {
        "id": "u1_rat4", "category": "rational_numbers",
        "question": "1/9 as a decimal is:",
        "options": ["0.9", "0.111…", "0.19", "Terminating 0.1"],
        "answer": 1,
        "explanation": "1 ÷ 9 = 0.111… (repeating).",
    },
    {
        "id": "u1_rat5", "category": "rational_numbers",
        "question": "Which number is NOT rational?",
        "options": ["0.75", "0.333…", "π", "−4/5"],
        "answer": 2,
        "explanation": "π is non-terminating and non-repeating → irrational.",
    },
    # ── Irrational numbers (5) ──
    {
        "id": "u1_irr1", "category": "irrational_numbers",
        "question": "Estimate √18 to the nearest tenth.",
        "options": ["3.0", "4.2", "5.0", "6.0"],
        "answer": 1,
        "explanation": "√18 ≈ 4.24 → about 4.2; between 4 and 5.",
    },
    {
        "id": "u1_irr2", "category": "irrational_numbers",
        "question": "Which value is NOT between 5 and 6?",
        "options": ["√27", "√32", "√29", "√37"],
        "answer": 3,
        "explanation": "√37 ≈ 6.08, which is above 6.",
    },
    {
        "id": "u1_irr3", "category": "irrational_numbers",
        "question": "Which is NOT irrational?",
        "options": ["√45", "√78", "√16", "π"],
        "answer": 2,
        "explanation": "√16 = 4, a rational integer.",
    },
    {
        "id": "u1_irr4", "category": "irrational_numbers",
        "question": "Order from least to greatest: √24, 5, √27, 5.5",
        "options": ["5, √24, √27, 5.5", "√24, 5, √27, 5.5", "√24, √27, 5, 5.5", "5, 5.5, √24, √27"],
        "answer": 1,
        "explanation": "√24 ≈ 4.9, √27 ≈ 5.2.",
    },
    {
        "id": "u1_irr5", "category": "irrational_numbers",
        "question": "From {5/6, 2.1, √45, √78, 2/3}, which are irrational?",
        "options": ["5/6 and 2/3", "√45 and √78", "2.1 only", "All of them"],
        "answer": 1,
        "explanation": "√45 and √78 are not perfect squares.",
    },
    # ── Exponents (5) ──
    {
        "id": "u1_exp1", "category": "exponents",
        "question": "Simplify 3⁵ · 3⁴.",
        "options": ["3¹", "3⁹", "3²⁰", "9⁹"],
        "answer": 1,
        "explanation": "Add exponents: 3⁵⁺⁴ = 3⁹.",
    },
    {
        "id": "u1_exp2", "category": "exponents",
        "question": "Simplify x¹¹ ÷ x⁴.",
        "options": ["x⁴⁴", "x⁷", "x¹⁵", "x⁴"],
        "answer": 1,
        "explanation": "Subtract exponents: x⁷.",
    },
    {
        "id": "u1_exp3", "category": "exponents",
        "question": "Kwon says 5⁵ · 5⁴ = 5¹. Is he correct?",
        "options": ["Yes", "No — should be 5⁹", "No — should be 25⁹", "No — should be 5²⁰"],
        "answer": 1,
        "explanation": "Multiply same base → add exponents → 5⁹.",
    },
    {
        "id": "u1_exp4", "category": "exponents",
        "question": "Evaluate 3⁻².",
        "options": ["−9", "1/9", "−1/9", "9"],
        "answer": 1,
        "explanation": "3⁻² = 1/3² = 1/9.",
    },
    {
        "id": "u1_exp5", "category": "exponents",
        "question": "Simplify t² · t⁵.",
        "options": ["t¹⁰", "t⁷", "t³", "2t⁷"],
        "answer": 1,
        "explanation": "Add exponents: t⁷.",
    },
    # ── Scientific notation (5) ──
    {
        "id": "u1_sci1", "category": "scientific_notation",
        "question": "Write 25,000,000,000 in scientific notation.",
        "options": ["25 × 10⁹", "2.5 × 10¹⁰", "2.5 × 10⁹", "250 × 10⁸"],
        "answer": 1,
        "explanation": "Move decimal 10 places → 2.5 × 10¹⁰.",
    },
    {
        "id": "u1_sci2", "category": "scientific_notation",
        "question": "Write 7 × 10² in standard form.",
        "options": ["70", "700", "7000", "0.7"],
        "answer": 1,
        "explanation": "Move decimal 2 places right → 700.",
    },
    {
        "id": "u1_sci3", "category": "scientific_notation",
        "question": "Is 10.2 × 10⁴ written in correct scientific notation?",
        "options": ["Yes", "No — use 1.02 × 10⁵", "No — use 102 × 10³", "No — coefficient too small"],
        "answer": 1,
        "explanation": "Coefficient must be less than 10.",
    },
    {
        "id": "u1_sci4", "category": "scientific_notation",
        "question": "9,200,000,000,000,000 in scientific notation?",
        "options": ["9.2 × 10¹⁴", "9.2 × 10¹⁵", "92 × 10¹⁴", "0.92 × 10¹⁶"],
        "answer": 1,
        "explanation": "9.2 × 10¹⁵.",
    },
    {
        "id": "u1_sci5", "category": "scientific_notation",
        "question": "Write 8.6 × 10⁻⁵ in standard form.",
        "options": ["86000", "0.00086", "0.000086", "8.6"],
        "answer": 2,
        "explanation": "Negative exponent → move decimal left → 0.000086.",
    },
    # ── Sci notation operations (4) ──
    {
        "id": "u1_scio1", "category": "sci_notation_ops",
        "question": "(2.2 × 10⁵)(4 × 10⁷) = ?",
        "options": ["8.8 × 10¹²", "6.2 × 10¹²", "8.8 × 10³⁵", "88 × 10¹²"],
        "answer": 0,
        "explanation": "Multiply coefficients; add exponents: 5+7=12.",
    },
    {
        "id": "u1_scio2", "category": "sci_notation_ops",
        "question": "(7.4 × 10⁶) ÷ (5 × 10⁻²) = ?",
        "options": ["1.48 × 10⁸", "1.48 × 10⁴", "14.8 × 10⁷", "1.48 × 10⁶"],
        "answer": 0,
        "explanation": "7.4/5 = 1.48; 6−(−2)=8.",
    },
    {
        "id": "u1_scio3", "category": "sci_notation_ops",
        "question": "3.4 × 10⁵ + 9.1 × 10⁵ = ?",
        "options": ["12.5 × 10⁵", "1.25 × 10⁶", "Both A and B", "12.5 × 10¹⁰"],
        "answer": 2,
        "explanation": "Same power of 10 → 12.5 × 10⁵ = 1.25 × 10⁶.",
    },
    {
        "id": "u1_scio4", "category": "sci_notation_ops",
        "question": "7.5 × 10⁻³ − 2.1 × 10⁻³ = ?",
        "options": ["5.4 × 10⁻³", "5.4 × 10⁻⁶", "9.6 × 10⁻³", "5.4 × 10³"],
        "answer": 0,
        "explanation": "Subtract coefficients when exponents match.",
    },
]
