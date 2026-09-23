"""School-aligned Unit 1 items — cloned from the Course 3 teacher packet through 9/22.

Worksheet pattern (every sheet uses the same template):
  1. Header code + title (IV-1, III-5, …)
  2. Vocab / big idea / fill-in rule
  3. Guided example with numbered steps
  4. You Try — same verb, new numbers
  5. Mix of: rewrite, convert, estimate, order, compare, nested 'of', error analysis

Prompt verbs we clone:
  Rewrite in exponential form. Then simplify. Keep exponential form.
  Name the rational numbers in the set.
  Estimate to the nearest tenth.
  Was ___ correct? Explain.
  Place in INCREASING / DECREASING order.
  Convert the repeating decimal into a fraction.
  Write ___ as a percent and a fraction.
  Complete. Show work. Simplest form.
  Of the … Of those … What fraction …?
"""

from __future__ import annotations

SCHOOL_PACKET_LABEL = "School packet through 9/22 — Numerical Relationships"

SCHOOL_PACKET_TOPICS: list[dict] = [
    {"id": "patterns", "levels": ["B", "C"]},
    {"id": "fractions", "levels": ["B", "C"]},
    {"id": "powers_roots", "levels": ["B", "C"]},
    {"id": "rational_numbers", "levels": ["B", "C", "D"]},
    {"id": "irrational_numbers", "levels": ["B", "C", "D"]},
    {"id": "exponents", "levels": ["B", "C"]},
]


def _q(
    qid: str,
    category: str,
    level: str,
    question: str,
    options: list[str],
    answer: int,
    explanation: str,
    sheet: str,
) -> dict:
    return {
        "id": qid,
        "category": category,
        "level": level,
        "question": question,
        "options": options,
        "answer": answer,
        "explanation": explanation,
        "source": "school_packet_9_22",
        "school_sheet": sheet,
    }


SCHOOL_PACKET_UNIT1_QUESTIONS: list[dict] = [
    # ── IV-1  Exponents: recap table, rewrite, product, quotient, You Try ──
    _q(
        "u1_sch_exp1", "exponents", "B",
        "EXPONENTS RECAP — For the expression 5³, which row is complete and correct?\n"
        "Base · Exponent · Expanded form · Exponential form · Standard form",
        [
            "3 · 5 · 5+5+5 · 3⁵ · 15",
            "5 · 3 · 5×5×5 · 5³ · 125",
            "5 · 3 · 5×3 · 5³ · 15",
            "5 · 3 · 5×5×5 · 3⁵ · 125",
        ],
        1,
        "Base is 5, exponent is 3, expanded is 5×5×5, exponential is 5³, standard form is 125.",
        "IV-1",
    ),
    _q(
        "u1_sch_exp2", "exponents", "B",
        "Rewrite in exponential form. Then simplify.\n4 × 4 × 4 × 4 × 4",
        ["4⁵", "4×5", "5⁴", "20"],
        0,
        "Five factors of 4 is 4⁵.",
        "IV-1",
    ),
    _q(
        "u1_sch_exp3", "exponents", "B",
        "Rewrite in exponential form. Then simplify.\n(4 × 4 × 4) × (4 × 4)",
        ["4⁵", "4⁶", "16⁵", "4³"],
        0,
        "Three fours times two fours is five fours: 4³ · 4² = 4⁵ (product of powers — add exponents).",
        "IV-1",
    ),
    _q(
        "u1_sch_exp4", "exponents", "B",
        "Rewrite in exponential form. Then simplify.\n(x · x · x) · (x · x)",
        ["x⁵", "x⁶", "2x⁵", "x³"],
        0,
        "Five factors of x is x⁵. Same as x³ · x² = x⁵.",
        "IV-1",
    ),
    _q(
        "u1_sch_exp5", "exponents", "B",
        "Product of Powers: When you multiply two exponential expressions with the same base, you _____ the exponents.\n"
        "Example: 3⁴ · 3² = ?",
        ["multiply → 3⁸", "add → 3⁶", "subtract → 3²", "add the bases → 6⁶"],
        1,
        "Same base → add exponents: 4+2=6, so 3⁶.",
        "IV-1",
    ),
    _q(
        "u1_sch_exp6", "exponents", "B",
        "Simplify the expression. Ensure your solution remains in exponential form.\n6⁷ · 6⁴",
        ["6¹¹", "6²⁸", "6³", "42¹¹"],
        0,
        "Add exponents: 7+4=11, so 6¹¹.",
        "IV-1",
    ),
    _q(
        "u1_sch_exp7", "exponents", "B",
        "Simplify. Keep exponential form.\na⁵ · a⁶",
        ["a¹¹", "a³⁰", "a¹", "2a¹¹"],
        0,
        "Same base → add: 5+6=11, so a¹¹.",
        "IV-1",
    ),
    _q(
        "u1_sch_exp8", "exponents", "B",
        "Quotient of Powers: When you divide two exponential expressions with the same base, you _____ the exponents.\n"
        "Rewrite in expanded form, then simplify: x⁸ / x³",
        ["add → x¹¹", "subtract → x⁵", "divide exponents → x²", "x⁸⁻³ = x²⁴"],
        1,
        "x·x·x·x·x·x·x·x over x·x·x leaves five x’s: x⁸⁻³ = x⁵.",
        "IV-1",
    ),
    _q(
        "u1_sch_exp9", "exponents", "C",
        "Simplify. Keep exponential form.\n10⁹ / 10⁴",
        ["10⁵", "10¹³", "10³⁶", "1"],
        0,
        "Subtract exponents: 9−4=5, so 10⁵.",
        "IV-1",
    ),
    _q(
        "u1_sch_exp10", "exponents", "C",
        "You Try — simplify. Keep exponential form.\n7³ · 7⁵ · 7",
        ["7⁸", "7⁹", "7¹⁵", "21⁹"],
        1,
        "7 = 7¹. Add: 3+5+1=9, so 7⁹.",
        "IV-1",
    ),
    _q(
        "u1_sch_exp11", "exponents", "C",
        "You Try — simplify. Keep exponential form.\n15⁶ · 15⁷",
        ["15¹³", "15⁴²", "15¹", "30¹³"],
        0,
        "Add exponents: 6+7=13, so 15¹³.",
        "IV-1",
    ),
    _q(
        "u1_sch_exp12", "exponents", "C",
        "Solve for x. Keep bases matching.\n8ˣ / 8² = 8⁵",
        ["x = 3", "x = 7", "x = 10", "x = 5"],
        1,
        "8ˣ⁻² = 8⁵, so x−2=5 and x=7.",
        "IV-1",
    ),
    _q(
        "u1_sch_exp13", "exponents", "C",
        "Robert and Deevan are examining 4⁸ · 4³. Deevan says the answer is 4⁵ because he subtracted. "
        "Help Robert explain what Deevan did incorrectly.",
        [
            "Deevan is correct — product of powers subtracts",
            "Deevan used the quotient rule. Product of powers adds: 4⁸⁺³ = 4¹¹",
            "The answer should be 4²⁴",
            "The base becomes 16¹¹",
        ],
        1,
        "Multiply same base → add exponents. Subtracting is the quotient rule.",
        "IV-1",
    ),
    # ── I-N  Fraction operations: “Complete. Simplest form.” + nested of ──
    _q(
        "u1_sch_frac1", "fractions", "B",
        "Directions: Complete. Show work. Ensure the answer is in simplest form.\n1/6 + 3/8",
        ["4/14", "11/24", "4/8", "1/2"],
        1,
        "LCD 24: 4/24 + 9/24 = 13/24. Wait — 1/6=4/24, 3/8=9/24, 4+9=13, so 13/24.",
        "I-N",
    ),
    _q(
        "u1_sch_frac1b", "fractions", "B",
        "Complete. Simplest form.\n1/6 + 3/8",
        ["4/14", "13/24", "4/24", "1/2"],
        1,
        "LCD 24: 1/6=4/24, 3/8=9/24. 4/24+9/24=13/24.",
        "I-N",
    ),
    _q(
        "u1_sch_frac2", "fractions", "B",
        "Complete. Simplest form.\n5/12 + 1/4",
        ["6/16", "2/3", "6/12", "8/12"],
        1,
        "LCD 12: 5/12 + 3/12 = 8/12 = 2/3.",
        "I-N",
    ),
    _q(
        "u1_sch_frac3", "fractions", "B",
        "Complete. Simplest form.\n5/6 − 1/3",
        ["4/3", "1/2", "4/6", "1/6"],
        1,
        "1/3=2/6, so 5/6−2/6=3/6=1/2.",
        "I-N",
    ),
    _q(
        "u1_sch_frac4", "fractions", "C",
        "Complete. Simplest form.\n2 1/4 + 1 2/3",
        ["3 3/7", "3 11/12", "4 1/12", "3 1/2"],
        1,
        "2+1=3 and 1/4+2/3=3/12+8/12=11/12 → 3 11/12.",
        "I-N",
    ),
    _q(
        "u1_sch_frac5", "fractions", "C",
        "Complete. Simplest form.\n13/2 − 1 1/4",
        ["5", "5 1/4", "6 1/4", "11/4"],
        1,
        "13/2=6 1/2=6 2/4. 6 2/4 − 1 1/4 = 5 1/4.",
        "I-N",
    ),
    _q(
        "u1_sch_frac6", "fractions", "B",
        "Complete. Simplest form.\n1/2 × 3/10",
        ["4/12", "3/20", "3/10", "1/5"],
        1,
        "Multiply tops and bottoms: 3/20.",
        "I-N",
    ),
    _q(
        "u1_sch_frac7", "fractions", "C",
        "Complete. Simplest form.\n2 1/3 × 3/4",
        ["7/4", "6/12", "7/12", "2"],
        0,
        "2 1/3=7/3. 7/3 × 3/4 = 7/4 (or 1 3/4).",
        "I-N",
    ),
    _q(
        "u1_sch_frac8", "fractions", "C",
        "Complete. Simplest form.\n3/4 ÷ 9/8",
        ["27/32", "2/3", "3/2", "8/9"],
        1,
        "3/4 × 8/9 = 24/36 = 2/3.",
        "I-N",
    ),
    _q(
        "u1_sch_frac9", "fractions", "C",
        "Complete. Simplest form.\n4 2/3 ÷ 7/3",
        ["2", "14/9", "32/21", "7/2"],
        0,
        "4 2/3=14/3. 14/3 × 3/7 = 2.",
        "I-N",
    ),
    _q(
        "u1_sch_w_frac_nested1", "fractions", "C",
        "Jack is baking cookies. Of all the cookies he makes, 1/2 are chocolate chip. "
        "Of the chocolate chip, he gives 1/4 to Casey and keeps the rest himself. "
        "What fraction of cookies were chocolate and kept by Jack?",
        ["1/8", "3/8", "1/4", "1/2"],
        1,
        "Nested of: (1/2)×(3/4 kept) = 3/8 of all cookies.",
        "Concepts 1–5",
    ),
    _q(
        "u1_sch_w_frac_nested2", "fractions", "C",
        "Thaddeus baked pancakes. Of the pancakes, 2/3 were filled with cheese and the rest were plain. "
        "Of the plain pancakes, 1/2 were given to Brooklyn. "
        "What fraction of pancakes were plain and given to Brooklyn?",
        ["1/3", "1/6", "1/2", "2/3"],
        1,
        "Plain = 1−2/3=1/3. Of those, 1/2 given: (1/3)×(1/2)=1/6.",
        "I-N",
    ),
    _q(
        "u1_sch_w_frac_oven", "fractions", "C",
        "Oven has 3 3/4 lbs of flour. A cake recipe says 3 layers can be made using 3/4 lb of flour. "
        "How many layers can Zoey make?",
        ["5 layers", "4 layers", "15 layers", "9 layers"],
        2,
        "How many 3/4-lb batches in 15/4 lbs: (15/4)÷(3/4)=5 batches. Each batch is 3 layers → 15 layers.",
        "Concepts 1–5",
    ),
    _q(
        "u1_sch_w_frac_rice", "fractions", "C",
        "Cari made a tray of mango sticky rice 5 1/4 ft long. She slices it into servings that were each 1 1/4 ft long. "
        "How many servings of mango sticky rice did Cari make?",
        ["4", "5", "4 1/5", "6"],
        2,
        "5 1/4 ÷ 1 1/4 = 21/4 ÷ 5/4 = 21/5 = 4 1/5 servings.",
        "I-N",
    ),
    _q(
        "u1_sch_w_frac_book", "fractions", "C",
        "Anderson’s reading log: Monday 1/8 of the book, Tuesday 3/16, Wednesday 1/4. "
        "After reading on Wednesday, how much of the book remains unread?",
        ["9/16 unread", "7/16 unread", "5/16 unread", "1/2 unread"],
        1,
        "LCD 16: 2/16+3/16+4/16=9/16 read. Unread: 7/16.",
        "I-N",
    ),
    _q(
        "u1_sch_w_frac_book2", "fractions", "B",
        "Use Anderson’s log: Monday 1/8, Tuesday 3/16. After Mon and Tues, how much of the book did Anderson read in total?",
        ["4/16", "5/16", "1/4", "3/8"],
        1,
        "1/8=2/16. 2/16+3/16=5/16.",
        "I-N",
    ),
    # ── III-5  Fraction–decimal–percent triangle ──
    _q(
        "u1_sch_rat1", "rational_numbers", "B",
        "You Try: Write 0.73 as a percent and as a fraction.",
        ["7.3% and 73/10", "73% and 73/100", "0.73% and 73/100", "73% and 7.3/10"],
        1,
        "Decimal ×100 for percent → 73%. 0.73=73/100.",
        "III-5",
    ),
    _q(
        "u1_sch_rat2", "rational_numbers", "B",
        "Write 96% as a decimal and as a fraction in simplest form.",
        ["0.96 and 24/25", "9.6 and 96/10", "0.096 and 96/100", "0.96 and 96/10"],
        0,
        "96%=0.96=96/100=24/25.",
        "III-5",
    ),
    _q(
        "u1_sch_rat3", "rational_numbers", "B",
        "Write 1/8 as a percent and as a decimal.",
        ["8% and 0.8", "12.5% and 0.125", "18% and 0.18", "1.25% and 0.0125"],
        1,
        "1÷8=0.125 and 0.125×100=12.5%.",
        "III-5",
    ),
    _q(
        "u1_sch_rat4", "rational_numbers", "C",
        "Compare using <, >, or =.\n3/4  ?  21/25",
        ["3/4 > 21/25", "3/4 < 21/25", "3/4 = 21/25", "Cannot compare"],
        1,
        "3/4=0.75 and 21/25=0.84, so 3/4 < 21/25.",
        "III-5",
    ),
    _q(
        "u1_sch_rat5", "rational_numbers", "C",
        "Write 0.05% as a decimal.",
        ["0.05", "0.005", "0.0005", "5"],
        2,
        "Percent means ÷100: 0.05÷100=0.0005.",
        "III-5",
    ),
    _q(
        "u1_sch_rat6", "rational_numbers", "B",
        "Write 120% as a decimal and as a fraction in simplest form.",
        ["0.12 and 3/25", "1.2 and 6/5", "12 and 12/1", "1.20 and 120/10"],
        1,
        "120%=1.2=6/5.",
        "III-5",
    ),
    _q(
        "u1_sch_rat_table", "rational_numbers", "B",
        "Complete the table (decimal to nearest hundredth). Fraction 2/5 belongs with which pair?",
        ["0.40 and 40%", "0.25 and 25%", "0.50 and 20%", "2.5 and 250%"],
        0,
        "2÷5=0.40=40%.",
        "III-5",
    ),
    # ── III-2  Repeating decimals — 5-step method, order, vocab ──
    _q(
        "u1_sch_rep1", "rational_numbers", "C",
        "Converting repeating decimals into fractions — use the class steps.\n"
        "Convert 0.4̅ (0.444…) into a fraction in simplest form.",
        ["4/10", "4/9", "4/99", "2/5"],
        1,
        "Let x=0.444…. 10x=4.444…. Subtract: 9x=4, so x=4/9.",
        "III-2",
    ),
    _q(
        "u1_sch_rep2", "rational_numbers", "D",
        "Convert 0.5̅4̅ (0.545454…) into a fraction in simplest form.",
        ["54/100", "54/99", "6/11", "27/50"],
        2,
        "Let x=0.5454…. 100x=54.5454…. Subtract: 99x=54 → 54/99=6/11.",
        "III-2",
    ),
    _q(
        "u1_sch_rep3", "rational_numbers", "C",
        "Convert 0.2̅7̅ (0.272727…) into a fraction in simplest form.",
        ["27/100", "27/99", "3/11", "27/90"],
        2,
        "Two repeating digits → multiply by 100. 99x=27 → 27/99=3/11.",
        "III-2",
    ),
    _q(
        "u1_sch_rep4", "rational_numbers", "C",
        "Determine which is greater: 1/2 or 0.005555…",
        ["1/2", "0.005555…", "They are equal", "Cannot tell"],
        0,
        "1/2=0.5, much greater than 0.005555…",
        "III-2",
    ),
    _q(
        "u1_sch_rep5", "rational_numbers", "C",
        "Place the numbers in INCREASING order: 25%, 3/4, 0.2̅",
        [
            "25%, 0.2̅, 3/4",
            "0.2̅, 25%, 3/4",
            "3/4, 25%, 0.2̅",
            "25%, 3/4, 0.2̅",
        ],
        1,
        "0.2̅=2/9≈0.222; 25%=0.25; 3/4=0.75.",
        "III-2",
    ),
    _q(
        "u1_sch_rep6", "rational_numbers", "C",
        "Place the numbers in DECREASING order: 3/5, 0.33, 33.5%",
        [
            "3/5, 33.5%, 0.33",
            "0.33, 33.5%, 3/5",
            "33.5%, 3/5, 0.33",
            "3/5, 0.33, 33.5%",
        ],
        0,
        "3/5=0.60, 33.5%=0.335, 0.33=0.33. Decreasing: 0.60, 0.335, 0.33.",
        "III-2",
    ),
    _q(
        "u1_sch_rep7", "rational_numbers", "B",
        "What is the difference between a terminating decimal and a repeating decimal?",
        [
            "Terminating decimals never end",
            "Terminating decimals end; repeating decimals have a digit block that continues forever",
            "Repeating decimals are always irrational",
            "There is no difference",
        ],
        1,
        "0.25 terminates. 0.333… or 0.54̅ repeats a block forever. Both can still be rational.",
        "III-2",
    ),
    _q(
        "u1_sch_rep8", "rational_numbers", "C",
        "Your friend says 0.333… is not a repeating decimal because only one digit shows. Are they correct?",
        [
            "Yes — you need at least two digits in the repeating block",
            "No — 0.333… is 0.3̅, which is a one-digit repeating block",
            "Yes — 0.333… terminates",
            "No — 0.333… is irrational",
        ],
        1,
        "A repeating block can be one digit. 0.3̅=1/3.",
        "III-2",
    ),
    _q(
        "u1_sch_rep9", "rational_numbers", "C",
        "Reyna says 0.7̅ is equivalent to one. Is Reyna correct? Show work to justify.",
        [
            "Yes, because repeating decimals equal 1",
            "No — 0.7̅ = 7/9, which is not 1",
            "Yes — 0.7̅ is the same as 0.9̅",
            "No — repeating decimals are irrational",
        ],
        1,
        "Let x=0.777…. 10x=7.777…. 9x=7, x=7/9 ≠ 1. (0.9̅ is the one that equals 1.)",
        "III-2",
    ),
    # ── III-3 / III-4 / III-6  Rationals vs irrationals ──
    _q(
        "u1_sch_irr1", "irrational_numbers", "B",
        "Name the rational numbers in the set: {8.4, √12, π, √64, √0.25}",
        [
            "8.4, √64, and √0.25",
            "√12 and π only",
            "All of them",
            "π and √64",
        ],
        0,
        "√64=8 and √0.25=0.5 (rational). 8.4 terminates. √12 and π do not terminate or repeat.",
        "III-6",
    ),
    _q(
        "u1_sch_irr2", "irrational_numbers", "B",
        "Estimate the number to the nearest tenth.\n√18",
        ["4.0", "4.2", "4.5", "5.0"],
        1,
        "Surrounding perfect squares: √16=4 and √25=5. 18 is a little past 16 → about 4.2.",
        "III-3",
    ),
    _q(
        "u1_sch_irr3", "irrational_numbers", "B",
        "Estimate to the nearest tenth.\n√7",
        ["2.4", "2.6", "3.0", "7.0"],
        1,
        "√4=2, √9=3. 7 is closer to 9 than to 4? Mid is 6.5, 7 is a bit past mid → about 2.6.",
        "III-3",
    ),
    _q(
        "u1_sch_irr4", "irrational_numbers", "C",
        "Ayden marked the approximate value of √52 on a number line near 6. Was Ayden correct? Explain.",
        [
            "Yes — 52 is close to 36, and √36=6",
            "No — √49=7 and √64=8, so √52 is a little more than 7",
            "Yes — √52 is between 5 and 6",
            "No — √52 is about 10",
        ],
        1,
        "Closest perfect squares 49 and 64. √52≈7.2, not 6.",
        "III-6",
    ),
    _q(
        "u1_sch_irr5", "irrational_numbers", "C",
        "Which of the following square roots would NOT be between 5 and 6?",
        ["√27", "√32", "√29", "√37"],
        3,
        "√25=5 and √36=6. √37>6.",
        "III-6",
    ),
    _q(
        "u1_sch_irr6", "irrational_numbers", "C",
        "Order the numbers from least to greatest: ∛8, π, 2.85, √8",
        [
            "∛8, √8, 2.85, π",
            "∛8, 2.85, √8, π",
            "√8, ∛8, π, 2.85",
            "π, 2.85, √8, ∛8",
        ],
        1,
        "∛8=2, 2.85, √8≈2.83 wait — √8≈2.828, so 2.85 > √8. Order: 2, 2.83, 2.85, 3.14 → ∛8, √8, 2.85, π.",
        "III-6",
    ),
    _q(
        "u1_sch_irr6b", "irrational_numbers", "C",
        "Order from least to greatest: ∛8, √8, 2.85, π",
        [
            "∛8, 2.85, √8, π",
            "∛8, √8, 2.85, π",
            "√8, ∛8, 2.85, π",
            "∛8, π, √8, 2.85",
        ],
        1,
        "∛8=2; √8≈2.83; 2.85; π≈3.14.",
        "III-6",
    ),
    _q(
        "u1_sch_irr7", "irrational_numbers", "C",
        "From {∛8, ∛9, ∛27, ∛42, ∛64, ∛125}, which cube roots are rational?",
        [
            "∛8, ∛27, ∛64, ∛125",
            "∛9 and ∛42 only",
            "All of them",
            "None of them",
        ],
        0,
        "Perfect cubes 8, 27, 64, 125. Write a conjecture: a cube root is rational only if the inside is a perfect cube.",
        "III-6",
    ),
    _q(
        "u1_sch_irr8", "irrational_numbers", "B",
        "Identify the irrational number in the set {1/2, √8, √81}.",
        ["1/2", "√8", "√81", "None — all are rational"],
        1,
        "√81=9 (rational). √8 is not a perfect square.",
        "III-3",
    ),
    _q(
        "u1_sch_irr9", "irrational_numbers", "C",
        "Compare with <, >, or =.\n√50  ?  7",
        ["√50 < 7", "√50 = 7", "√50 > 7", "Cannot compare without a calculator"],
        2,
        "√49=7 and 50>49, so √50>7.",
        "III-4",
    ),
    _q(
        "u1_sch_irr10", "irrational_numbers", "D",
        "Given an example of a rational AND an irrational number between 4.8 and 4.9. "
        "How many numbers exist between 4.8 and 4.9?",
        [
            "None — 4.8 and 4.9 are next to each other",
            "Exactly one number: 4.85",
            "Infinitely many; e.g. 4.83 (rational) and √24 ≈ 4.899 (irrational)",
            "Only the integers between them",
        ],
        2,
        "Density: infinitely many rationals and irrationals between any two numbers.",
        "III-4",
    ),
    _q(
        "u1_sch_irr11", "irrational_numbers", "C",
        "Aisha says √50 is less than 7 because 50 is close to 49. Was Aisha correct? Explain.",
        [
            "Yes — √50 ≈ 6.9",
            "No — √49=7 and 50>49, so √50 is a little more than 7",
            "Yes — round down to the lesser perfect square",
            "No — √50 is about 10",
        ],
        1,
        "Greater radicand → greater square root. √50≈7.07.",
        "III-4",
    ),
    # ── Concepts 1–5  Sequences + powers ──
    _q(
        "u1_sch_pat1", "patterns", "C",
        "Numerical Relationships (Sequences) — Figure 1 has 1 dot, Figure 2 has 3 dots, Figure 3 has 6 dots "
        "(each figure adds one more row). Make a conjecture: how many dots are in the 12th term?",
        ["24", "66", "78", "144"],
        2,
        "Triangular numbers n(n+1)/2. For n=12: 12×13/2=78.",
        "Concepts 1–5",
    ),
    _q(
        "u1_sch_pat2", "patterns", "B",
        "Same dot pattern (1, 3, 6, …). How many dots are in the 5th term?",
        ["10", "12", "15", "21"],
        2,
        "5×6/2=15 dots (draw 5 rows: 1+2+3+4+5).",
        "Concepts 1–5",
    ),
    _q(
        "u1_sch_pat3", "patterns", "B",
        "Arrange the following to create an INCREASING sequence:\n|5| + 1    ·    |−8 − 7|    ·    |42 − 63|",
        ["1, 6, 15", "6, 15, 21", "15, 6, 21", "21, 15, 6"],
        1,
        "|5|+1=6, |−15|=15, |−21|=21. Increasing: 6, 15, 21.",
        "Concepts 1–5",
    ),
    _q(
        "u1_sch_pat4", "patterns", "B",
        "A square-tile pattern: Figure 1 has 1 small square, Figure 2 has 4, Figure 3 has 9. "
        "How many small squares will Figure 10 have?",
        ["19", "40", "81", "100"],
        3,
        "The figures are n². Figure 10: 10²=100.",
        "I-N",
    ),
    _q(
        "u1_sch_pow1", "powers_roots", "B",
        "Powers / Roots — solve for x.\nx² = 144",
        ["x = 12 only", "x = −12 only", "x = 12 or x = −12", "x = 72"],
        2,
        "12²=144 and (−12)²=144.",
        "Concepts 1–5",
    ),
    _q(
        "u1_sch_pow2", "powers_roots", "B",
        "Solve for y.\ny³ = 729",
        ["y = 9", "y = 27", "y = 243", "y = ±9"],
        0,
        "9×9×9=729. One real cube root.",
        "Concepts 1–5",
    ),
    _q(
        "u1_sch_pow3", "powers_roots", "C",
        "Evaluate the expression.\n5² − (3² + √16) + 2³",
        ["20", "24", "28", "12"],
        0,
        "25 − (9+4) + 8 = 25−13+8=20.",
        "Concepts 1–5",
    ),
    _q(
        "u1_sch_pow4", "powers_roots", "B",
        "Convert 3/4 to a percentage.",
        ["34%", "43%", "75%", "0.75%"],
        2,
        "3/4=0.75=75%.",
        "Concepts 1–5",
    ),
    _q(
        "u1_sch_pow5", "powers_roots", "B",
        "A square photo has area 81 cm². What is the side length?",
        ["9 cm", "18 cm", "40.5 cm", "√40 cm"],
        0,
        "Side = √81 = 9 cm.",
        "Concepts 1–5",
    ),
    _q(
        "u1_sch_pow6", "powers_roots", "C",
        "A cube gift box has volume 64 in³. Liam says the edge is irrational because it is a root. Is Liam correct?",
        [
            "Yes — all roots are irrational",
            "No — edge = ∛64 = 4, which is rational",
            "Yes — 64 is not a perfect cube",
            "No — the edge is √64 = 8",
        ],
        1,
        "∛64=4 because 4³=64. Perfect-cube roots are rational.",
        "III-6",
    ),
]

# Drop the duplicate broken frac1 if both exist — keep frac1b as canonical 1/6+3/8.
SCHOOL_PACKET_UNIT1_QUESTIONS = [
    q for q in SCHOOL_PACKET_UNIT1_QUESTIONS if q["id"] != "u1_sch_frac1"
]
SCHOOL_PACKET_UNIT1_QUESTIONS = [
    q for q in SCHOOL_PACKET_UNIT1_QUESTIONS if q["id"] != "u1_sch_irr6"
]
