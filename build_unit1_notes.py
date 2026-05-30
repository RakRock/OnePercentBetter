#!/usr/bin/env python3
"""One-time builder: writes Unit 1 activity markdown notes. Run: python build_unit1_notes.py"""

from pathlib import Path

NOTES = Path(__file__).parent / "ArjunCourse3" / "notes" / "unit_1"
NOTES.mkdir(parents=True, exist_ok=True)

ACTIVITIES = {
    "activity_1_investigating_patterns.md": '''# Activity 1: Investigating Patterns

[KEY]
A **sequence** is an ordered list of numbers or figures that follow a **pattern**.  
Describe patterns with words, tables, or formulas; predict the **next term** or the **nth term** when you see a constant difference or a clear rule.
[/KEY]

## Quick Review Notes

### Main Idea
Math often starts with **noticing patterns** — in shapes, dots, or numbers. A **conjecture** is your best guess about the pattern; you support it with evidence from several terms. Sequences can be **increasing**, **decreasing**, or neither.

### Key Vocabulary
- **Sequence:** Ordered list of numbers or figures.
- **Term:** One number or figure in a sequence.
- **Conjecture:** Educated guess about a pattern.
- **Constant difference:** Same amount added or subtracted each step (e.g. +4).
- **Increasing / decreasing sequence:** Terms go up or down.
- **Fibonacci sequence:** Each term is the sum of the two before it (1, 1, 2, 3, 5, 8, …).

### Important Formulas / Rules

| Pattern type | How to describe | nth term (when applicable) |
|--------------|-----------------|----------------------------|
| Add same amount | Constant difference | `aₙ = a₁ + d(n − 1)` |
| Multiply same amount | Geometric | `aₙ = a₁ · rⁿ⁻¹` |
| Fibonacci | Sum of previous two | No simple single formula in this unit |

[DIAGRAM:sequence_pattern]

[DIAGRAM:fibonacci]

### Example 1 — Constant difference

**Problem:** Sequence 3, 7, 11, 15, … What are the next two terms?

**Solution:**
1. Differences: `7 − 3 = 4`, `11 − 7 = 4` → constant difference **+4**  
2. Next: `15 + 4 = 19`, then `19 + 4 = 23`  

**Answer:** **19, 23**

### Example 2 — Fibonacci

**Problem:** 1, 1, 2, 3, 5, 8, … What are the next three terms?

**Solution:**
1. `8 + 5 = 13`, `13 + 8 = 21`, `21 + 13 = 34`  

**Answer:** **13, 21, 34**

### Textbook practice (from the PDF)

---

**1. Lesson 1-3 Item 1a — `3, 6, 12, 24, …`**

**Solution:** Each term × 2 → **increasing**. Next term: **48**.

**Answer:** Increasing; next term **48**

---

**2. Lesson 1-3 Item 1b — `17, 14, 11, 8, …`**

**Solution:** Subtract 3 each time → **decreasing**. Next: **5**.

**Answer:** Decreasing; next term **5**

---

**3. Activity 1 Practice #12 — Fibonacci**

**Problem:** `1, 1, 2, 3, 5, 8, …` — next three numbers?

**Solution:** `8+5=13`, `13+8=21`, `21+13=34`.

**Answer:** **13, 21, 34**

---

**4. Activity 1 Practice #13 — `5, 2, −1, …`**

**Solution:** Difference **−3** each step → next: **−4, −7, −10**.

**Answer:** Decreasing; **−4, −7, −10**

---

**5. Activity 1 Practice #14 — `0.25, 0.5, 1, …`**

**Solution:** Multiply by 2 → **increasing**. Next: **2, 4, 8**.

**Answer:** Increasing; **2, 4, 8**

---

**6. Lesson 1-2 Item 9 — Dots 3, 7, 11, … ninth figure**

**Solution:** Pattern +4 dots → terms 3, 7, 11, 15, 19, 23, 27, 31, **35**.

**Answer:** **35 dots** in the 9th figure

### Common Mistakes
- Guessing one term without checking **several** differences.
- Calling any pattern “Fibonacci” when it is only **+ constant**.
- Forgetting **ellipsis (…)** means the pattern continues the same way.

### Mini Summary
- Look for **constant difference** or **ratio** between terms.
- **Increasing** vs **decreasing** describes direction.
- **Fibonacci:** add the two previous terms.
- Always justify a conjecture with **evidence**.
''',
    "activity_2_operations_with_fractions.md": '''# Activity 2: Operations with Fractions

[KEY]
**Same denominator** to add/subtract; **multiply tops and bottoms**; for division, **multiply by the reciprocal**.  
Always **simplify** and convert improper fractions to mixed numbers when needed.
[/KEY]

## Quick Review Notes

### Main Idea
Fractions describe **parts of a whole**. You add and subtract with a **common denominator (LCD)**. You multiply **numerators × numerators** and **denominators × denominators**. To divide, multiply by the **reciprocal** (flip the second fraction).

### Key Vocabulary
- **Numerator / denominator:** Top and bottom of a fraction.
- **LCD (least common denominator):** Smallest shared denominator for addition.
- **Improper fraction:** Numerator ≥ denominator (e.g. `13/6`).
- **Mixed number:** Whole number + fraction (e.g. `2 1/6`).
- **Reciprocal:** Flip the fraction (`2/3` → `3/2`).

### Important Formulas / Rules

| Operation | Rule |
|-----------|------|
| Add/subtract | Find LCD, rewrite, then add/subtract numerators |
| Multiply | `(a/b)(c/d) = ac/bd` then simplify |
| Divide | `(a/b) ÷ (c/d) = (a/b)(d/c)` |

[DIAGRAM:add_fractions]

[DIAGRAM:multiply_fractions]

### Example 1 — Add

**Problem:** `3/5 + 4/6`

**Solution:**
1. LCD = 6: `3/5 = 18/30`, `4/6 = 20/30` — or `9/6 + 4/6`  
2. `9/6 + 4/6 = 13/6 = 2 1/6`  

**Answer:** **`13/6` or `2 1/6`**

### Example 2 — Multiply

**Problem:** `(2/5)(7/12)`

**Solution:**
1. `2×7 = 14`, `5×12 = 60` → `14/60`  
2. Simplify: `7/30`  

**Answer:** **`7/30`**

### Textbook practice (from the PDF)

---

**1. Activity 2 Practice #1 — `3/5 + 4/6`**

**Solution:** LCD 30 or 6 → **`13/6 = 2 1/6`**.

**Answer:** **`2 1/6`**

---

**2. Activity 2 Practice #2 — `5/8 − 1/3`**

**Solution:** LCD 24: `15/24 − 8/24 = 7/24`.

**Answer:** **`7/24`**

---

**3. Activity 2 Practice #7 — Fabric**

**Problem:** Judy `4 2/3` yd + Marie `5 1/2` yd.

**Solution:** `14/3 + 11/2 = 28/6 + 33/6 = 61/6 = 10 1/6`.

**Answer:** **`10 1/6` yards**

---

**4. Activity 2 Practice #9 — Birth weights**

**Problem:** Carmen `7 1/2` lb, Angelo `5 1/4` lb — how much heavier?

**Solution:** `7.5 − 5.25 = 2.25 = 2 1/4` lb.

**Answer:** **`2 1/4` pounds** heavier

---

**5. Activity 2 Practice #14 — `2/5 × 7/12`**

**Solution:** `14/60 = 7/30`.

**Answer:** **`7/30`**

---

**6. Lesson 2-1 Practice #17 — Trail mix**

**Problem:** `1 1/2 + 3/4 + 2/3` cups.

**Solution:** `3/2 + 3/4 + 2/3` → LCD 12: `18/12 + 9/12 + 8/12 = 35/12 = 2 11/12`.

**Answer:** **`2 11/12` cups**

### Common Mistakes
- Adding **denominators** when adding fractions (wrong).
- Forgetting to **simplify** the final answer.
- Not converting **mixed numbers** to improper fractions first when needed.

### Mini Summary
- **+/−** → LCD first. **×** → multiply across. **÷** → reciprocal.
- Simplify using GCF. Use **mixed numbers** for answers when appropriate.
''',
}

# Additional activities 3-8 written in continuation
ACTIVITIES.update({
    "activity_3_powers_and_roots.md": '''# Activity 3: Powers and Roots

[KEY]
**Exponent** tells how many times to use a base as a factor: `8² = 8×8`.  
**Square** → area (`s²`); **cube** → volume (`s³`). **Square root** undoes squaring: if `s² = 49`, `s = 7`.
[/KEY]

## Quick Review Notes

### Main Idea
**Exponents** are shorthand for repeated multiplication. **Perfect squares** and **perfect cubes** come from whole-number side lengths. **Square roots** find the side when you know the area.

### Key Vocabulary
- **Base / exponent:** In `5³`, base 5, exponent 3.
- **Squared:** To the second power (`n²`).
- **Cubed:** To the third power (`n³`).
- **Perfect square:** `1, 4, 9, 16, 25, …`
- **Square root (√):** Number that squares to a given value.

### Important Formulas / Rules

| Idea | Formula |
|------|---------|
| Square area | `A = s²` |
| Cube volume | `V = s³` |
| Square root | If `x² = a`, then `x = √a` (positive root in this course) |

[DIAGRAM:square_area]

[DIAGRAM:cube_volume]

### Example 1 — Area

**Problem:** Side length 7.2 in. Find area.

**Solution:** `A = 7.2² = 51.84` in².

**Answer:** **51.84 square inches**

### Example 2 — Solve `x² = 81`

**Solution:** `x = 9` or `x = −9` (if negatives allowed); usually **9** for length.

**Answer:** **`x = 9`** (or ±9)

### Textbook practice (from the PDF)

---

**1. Activity 3 Practice #1a — `8¹`**

**Answer:** **8**

---

**2. Activity 3 Practice #2 — Square side 7.2 in.**

**Answer:** **`51.84` in²**

---

**3. Activity 3 Practice #4 — Which is NOT `8²`?**

**Answer:** **A** — “eight multiplied by two” is `16`, not `64`.

---

**4. Activity 3 Practice #8a — `x² = 81`**

**Answer:** **`x = 9`** or **`x = −9`**

---

**5. Activity 3 Practice #9 — Area 16 cm², trim 1 cm per side**

**Solution:** Side was 4; new side 2; new area `2² = 4` cm².

**Answer:** **4 cm²**

---

**6. Activity 3 Practice #13 — Cube volume 216 ft³**

**Solution:** `c³ = 216` → `c = 6`.

**Answer:** **6 feet**

### Common Mistakes
- Confusing **`2x`** with **`x²`**.
- Forgetting **units** (in², ft³).
- Using **3 × s** instead of **`s³`** for cube volume.

### Mini Summary
- **`n²`** = square; **`n³`** = cube; **√** undoes square.
- Area of square = **side squared**. Volume of cube = **edge cubed**.
''',
    "activity_4_rational_numbers.md": '''# Activity 4: Rational Numbers

[KEY]
A **rational number** can be written as **a/b** (b ≠ 0). Its decimal **terminates** or **repeats**.  
Convert between **fraction ↔ decimal ↔ percent** by dividing or multiplying by 100.
[/KEY]

## Quick Review Notes

### Main Idea
**Rational numbers** include fractions, integers, and decimals that stop or repeat. You move between **fractions, decimals, and percents** to compare and compute. **Repeating decimals** (like `0.333…`) are still rational.

### Key Vocabulary
- **Rational number:** Can be written as `p/q`.
- **Terminating decimal:** Ends (e.g. `0.75`).
- **Repeating decimal:** Block of digits repeats (`0.666…`).
- **Percent:** Per hundred (`60% = 60/100`).

### Important Formulas / Rules

| Convert | Steps |
|---------|--------|
| Fraction → decimal | Divide numerator ÷ denominator |
| Decimal → percent | × 100 and add % |
| Fraction → percent | decimal × 100 |

[DIAGRAM:frac_decimal_percent]

[DIAGRAM:repeating_decimal]

### Example 1 — `3/5` to decimal and percent

**Solution:** `3 ÷ 5 = 0.6` → **60%**.

**Answer:** **0.6** and **60%**

### Example 2 — Is `0.232323…` repeating?

**Solution:** The block **23** repeats → **yes**, rational.

**Answer:** **Yes**, repeating decimal

### Textbook practice (from the PDF)

---

**1. Activity 4 Practice #3a — `3/5`**

**Answer:** **0.6** and **60%**

---

**2. Activity 4 Practice #4a — `0.8`**

**Answer:** **4/5** and **80%**

---

**3. Activity 4 Practice #5a — `20%`**

**Answer:** **0.2** and **1/5**

---

**4. Activity 4 Practice #7 — NOT equivalent to `60/80`**

**Solution:** `60/80 = 3/4 = 0.75`; **0.6** is wrong.

**Answer:** **B. 0.6**

---

**5. Activity 4 Practice #8 — NOT rational**

**Answer:** **B** — non-terminating, **non-repeating** decimal

---

**6. Activity 4 Practice #15 — Repeating decimal for `1/9`**

**Solution:** `1 ÷ 9 = 0.111… = 0.1̄`.

**Answer:** **`0.111…` or `0.1̄`**

### Common Mistakes
- Thinking **all decimals** are rational (non-repeating infinite decimals are not).
- Moving the decimal the **wrong direction** for percent.

### Mini Summary
- Rational = **fraction or terminating/repeating decimal**.
- **Divide** to get decimal; **×100** for percent.
''',
    "activity_5_rational_irrational_numbers.md": '''# Activity 5: Rational and Irrational Numbers

[KEY]
**Irrational** numbers cannot be written as `a/b`; decimals **never terminate or repeat** (e.g. **π**, **√2**).  
**Estimate** roots by finding perfect squares on each side of the number line.
[/KEY]

## Quick Review Notes

### Main Idea
The number line holds **rationals** (fractions, terminating/repeating decimals) and **irrationals** (like √2, √3, π). You **estimate** square roots by bracketing between perfect squares.

### Key Vocabulary
- **Irrational number:** Not equal to any `p/q`; non-repeating, non-terminating decimal.
- **Perfect square:** `1, 4, 9, 16, …` — helps estimate √.
- **Estimate:** Approximate to a given place value.

### Important Formulas / Rules

| Estimate √n | Find perfect squares around n |
|-------------|------------------------------|
| √18 | Between √16=4 and √25=5 → about **4.2** |
| √130 | Between 11²=121 and 12²=144 → about **11.4** |

[DIAGRAM:sqrt_number_line]

[DIAGRAM:rational_irrational]

### Example 1 — Name irrationals in `{5/6, 2.1, √45, √78, 2/3}`

**Solution:** √45 and √78 are not perfect squares → **irrational**.

**Answer:** **√45, √78**

### Example 2 — Estimate √18 to tenths

**Solution:** Between 4 and 5; closer to 4 → **4.2** or **4.3**.

**Answer:** **≈ 4.2** (reasonable estimate)

### Textbook practice (from the PDF)

---

**1. Activity 5 Practice #5 — Estimate √18**

**Answer:** Between **4** and **5**; about **4.2**

---

**2. Activity 5 Practice #13 — √ between 5 and 6?**

**Solution:** 5²=25, 6²=36. √32≈5.66, √29≈5.39, √37≈6.08, √27≈5.2. **√37** is NOT between 5 and 6.

**Answer:** **C. √37**

---

**3. Activity 5 Practice #18 — NOT irrational**

**Answer:** **B. √16 = 4** (rational)

---

**4. Activity 5 Practice #19 — Between 12.1 and 12.2**

**Solution:** Rational: **12.15**; irrational: **√147** (≈12.12) or **π/26** etc.

**Answer:** Example: rational **12.15**, irrational **√147**

---

**5. Activity 5 Practice #24 — Order √27, 5.5, √24, 5**

**Solution:** √24≈4.9, √27≈5.2 → **√24, 5, √27, 5.5**

**Answer:** **√24, 5, √27, 5.5**

---

**6. Activity 5 Practice #15 — Relationship**

**Answer:** Rationals and irrationals together fill the line; irrationals **cannot** be written as fractions; no overlap.

### Common Mistakes
- Thinking **√16** is irrational (it equals **4**).
- Estimating √ without checking **perfect squares** on both sides.

### Mini Summary
- **Rational:** fraction or terminating/repeating decimal.
- **Irrational:** π, non-perfect roots, non-repeating decimals.
- **Estimate √n** using nearby perfect squares.
''',
    "activity_6_properties_of_exponents.md": '''# Activity 6: Properties of Exponents

[KEY]
**Same base:** multiply → **add exponents**; divide → **subtract exponents**.  
**Power to a power:** multiply exponents. **Negative exponent:** `a⁻ⁿ = 1/aⁿ`.
[/KEY]

## Quick Review Notes

### Main Idea
Exponent **properties** let you simplify without expanding long products. Same base → add or subtract exponents. **Negative** exponents mean **reciprocal**.

### Key Vocabulary
- **Product rule:** `aᵐ · aⁿ = aᵐ⁺ⁿ`
- **Quotient rule:** `aᵐ / aⁿ = aᵐ⁻ⁿ`
- **Power rule:** `(aᵐ)ⁿ = aᵐⁿ`
- **Zero exponent:** `a⁰ = 1` (a ≠ 0)

### Important Formulas / Rules

| Rule | Formula |
|------|---------|
| Product | `aᵐ · aⁿ = aᵐ⁺ⁿ` |
| Quotient | `aᵐ / aⁿ = aᵐ⁻ⁿ` |
| Negative | `a⁻ⁿ = 1/aⁿ` |
| Power of power | `(aᵐ)ⁿ = aᵐⁿ` |

[DIAGRAM:product_rule]

[DIAGRAM:negative_exponent]

### Example 1 — `3⁵ · 3⁴`

**Solution:** `3⁵⁺⁴ = 3⁹`.

**Answer:** **`3⁹`**

### Example 2 — `3⁻²`

**Solution:** `1/3² = 1/9`.

**Answer:** **`1/9`**

### Textbook practice (from the PDF)

---

**1. Activity 6 Practice #1 — `3⁵ · 3⁴`**

**Answer:** **`3⁹`**

---

**2. Activity 6 Practice #6 — `x¹¹/x⁴`**

**Answer:** **`x⁷`**

---

**3. Activity 6 Practice #7 — `12⁶ · 12⁴`**

**Answer:** **`12¹⁰`** (choice B)

---

**4. Activity 6 Practice #9 — Kwon: `5⁵ · 5⁴ = 5¹`?**

**Solution:** Should be `5⁹`, not `5¹`. **Disagree** with Kwon.

**Answer:** **No** — correct answer **`5⁹`**

---

**5. Activity 6 Practice #12 — `3⁻²`**

**Answer:** **`1/9`**

---

**6. Lesson 6-1 Practice #12a — `t² · t⁵`**

**Answer:** **`t⁷`**

### Common Mistakes
- Multiplying **bases** instead of adding exponents.
- Forgetting **`a⁻ⁿ = 1/aⁿ`**.
- Treating **`(ab)²`** as `ab²` (should be `a²b²`).

### Mini Summary
- Multiply same base → **add** exponents. Divide → **subtract**.
- Negative exponent → **reciprocal**. Simplify completely.
''',
    "activity_7_scientific_notation.md": '''# Activity 7: Scientific Notation

[KEY]
**Scientific notation:** `a × 10ⁿ` where **1 ≤ |a| < 10**.  
Positive **n** → large numbers (move decimal right); negative **n** → small numbers (move decimal left).
[/KEY]

## Quick Review Notes

### Main Idea
Scientific notation writes very large or very small numbers compactly. The **coefficient** is one digit (or a few) before the decimal; the **power of 10** tells the size.

### Key Vocabulary
- **Scientific notation:** `d × 10ⁿ` with `1 ≤ |d| < 10`.
- **Standard form:** Usual decimal notation.
- **Coefficient / mantissa:** The `d` part.

### Important Formulas / Rules

| Direction | Rule |
|-----------|------|
| Large number → sci. | Move decimal left; **n** positive |
| Small number → sci. | Move decimal right; **n** negative |
| Sci. → standard | Use exponent to move decimal |

[DIAGRAM:sci_notation_form]

[DIAGRAM:standard_form]

### Example 1 — `25,000,000,000`

**Solution:** `2.5 × 10¹⁰`.

**Answer:** **`2.5 × 10¹⁰`**

### Example 2 — `8.92 × 10⁸`

**Solution:** Move 8 places right → **892,000,000**.

**Answer:** **892,000,000**

### Textbook practice (from the PDF)

---

**1. Activity 7 Practice #1 — `25,000,000,000`**

**Answer:** **`2.5 × 10¹⁰`**

---

**2. Activity 7 Practice #5 — `7 × 10²`**

**Answer:** **700**

---

**3. Activity 7 Practice #9 — Is `10.2 × 10⁴` correct form?**

**Answer:** **No** — coefficient must be `< 10`; use **`1.02 × 10⁵`**

---

**4. Activity 7 Practice #11 — `9,200,000,000,000,000`**

**Solution:** `9.2 × 10¹⁵`.

**Answer:** **D. `9.2 × 10¹⁵`**

---

**5. Activity 7 Practice #13 — Sun 93 million miles**

**Answer:** **`9.3 × 10⁷` miles** (approx.)

---

**6. Activity 7 Practice #22 — `8.6 × 10⁻⁵`**

**Answer:** **0.000086**

### Common Mistakes
- Coefficient **≥ 10** (not proper scientific notation).
- Wrong **direction** when moving the decimal.

### Mini Summary
- Form: **`a × 10ⁿ`**, `1 ≤ |a| < 10`.
- **+n** = big; **−n** = small. Count decimal jumps carefully.
''',
    "activity_8_operations_scientific_notation.md": '''# Activity 8: Operations with Scientific Notation

[KEY]
**Multiply:** multiply coefficients, **add** exponents. **Divide:** divide coefficients, **subtract** exponents.  
**Add/subtract:** exponents must **match** first (adjust coefficient if needed).
[/KEY]

## Quick Review Notes

### Main Idea
Use exponent rules on the **10ⁿ** part and regular arithmetic on **coefficients**. For addition, rewrite so both terms have the **same power of 10**.

### Key Vocabulary
- **Coefficient:** Number before `× 10ⁿ`.
- **Order of magnitude:** Rough size from the exponent.

### Important Formulas / Rules

| Operation | Rule |
|-----------|------|
| `(a×10ᵐ)(b×10ⁿ)` | `(ab)×10ᵐ⁺ⁿ` |
| `(a×10ᵐ)/(b×10ⁿ)` | `(a/b)×10ᵐ⁻ⁿ` |
| Add/subtract | Same `10ⁿ`, then add coefficients |

[DIAGRAM:multiply_sci]

[DIAGRAM:add_sci]

### Example 1 — `(2.2×10⁵)(4×10⁷)`

**Solution:** `8.8 × 10¹²`.

**Answer:** **`8.8 × 10¹²`**

### Example 2 — `3.4×10⁵ + 9.1×10⁵`

**Solution:** `12.5 × 10⁵ = 1.25 × 10⁶`.

**Answer:** **`1.25 × 10⁶`**

### Textbook practice (from the PDF)

---

**1. Activity 8 Practice #1 — `(2.2×10⁵)(4×10⁷)`**

**Answer:** **`8.8 × 10¹²`**

---

**2. Activity 8 Practice #4 — `(6.5×10⁻¹³)(2×10⁻⁴)`**

**Solution:** `13 × 10⁻¹⁷ = 1.3 × 10⁻¹⁶`.

**Answer:** **`1.3 × 10⁻¹⁶`**

---

**3. Activity 8 Practice #8 — Multiplying: exponents?**

**Answer:** **A. Add the exponents**

---

**4. Activity 8 Practice #10 — Brigitte `(7.4×10⁶)÷(5×10⁻²)`**

**Solution:** `1.48 × 10⁸` — **agree**.

**Answer:** **Yes**, **`1.48 × 10⁸`**

---

**5. Activity 8 Practice #16 — `3.4×10⁵ + 9.1×10⁵`**

**Answer:** **`12.5 × 10⁵` or `1.25 × 10⁶`**

---

**6. Activity 8 Practice #17 — `7.5×10⁻³ − 2.1×10⁻³`**

**Solution:** `5.4 × 10⁻³`.

**Answer:** **`5.4 × 10⁻³`**

### Common Mistakes
- Adding **exponents** when you should add **coefficients** (same power of 10).
- Leaving answer with coefficient **≥ 10** (normalize).

### Mini Summary
- **×** → multiply coeffs, add exponents. **÷** → divide coeffs, subtract exponents.
- **+/−** → match `10ⁿ` first, then combine coefficients.
''',
})

CHEAT = '''# Unit 1: Numerical Relationships — Overview

| Activity | Topic | Key idea |
|----------|-------|----------|
| **1** | Investigating Patterns | Sequences, conjectures, Fibonacci, increasing/decreasing |
| **2** | Operations with Fractions | LCD, multiply/divide fractions |
| **3** | Powers and Roots | `n²`, `n³`, square roots |
| **4** | Rational Numbers | Fraction ↔ decimal ↔ percent; repeating decimals |
| **5** | Rational & Irrational | √ estimates; π, non-perfect roots |
| **6** | Properties of Exponents | Product/quotient rules; negative exponents |
| **7** | Scientific Notation | `a × 10ⁿ` |
| **8** | Operations with Sci. Notation | ×, ÷, +, − with powers of 10 |

Open each activity for full notes, diagrams, and **PDF practice** with step-by-step solutions.
'''

def main():
    for name, body in ACTIVITIES.items():
        (NOTES / name).write_text(body.strip() + "\n", encoding="utf-8")
        print(f"wrote {name}")
    (NOTES / "unit_1_numerical_relationships_lesson_notes.md").write_text(CHEAT.strip() + "\n", encoding="utf-8")
    print("wrote unit_1_numerical_relationships_lesson_notes.md")


if __name__ == "__main__":
    main()
