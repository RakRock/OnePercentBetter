#!/usr/bin/env python3
"""One-time builder: writes Edgenuity Unit 3 activity markdown notes. Run: python build_edgenuity_unit3_notes.py"""

from pathlib import Path

NOTES = Path(__file__).parent / "ArjunEdgenuityCourse3" / "notes" / "unit_3"
NOTES.mkdir(parents=True, exist_ok=True)

ACTIVITIES = {
    "activity_1_slope_intercept_read.md": '''# Activity 1: Reading Slope & Y-Intercept

[KEY]
**Slope-intercept form:** `y = mx + b` — **m** is slope (rate), **b** is y-intercept (starting value at x = 0).  
Read **m** and **b** from equations, graphs `(0, b)`, and tables (constant change in y ÷ change in x).
[/KEY]

## Quick Review Notes

### Main Idea
Linear equations show how two things change together in a straight-line pattern. The form `y = mx + b` tells you the **starting value** (b) and the **rate of change** (m). Knowing how to read m and b from a graph, table, or equation helps you predict what happens next — like how much money is left after each day, or how fast a car is going. This skill shows up on almost every exam question about lines.

### Key Vocabulary
- **Slope (m):** change in y ÷ change in x; steepness of the line
- **Y-intercept (b):** y-value when x = 0; point `(0, b)`
- **Slope-intercept form:** y = mx + b
- **Fractional slope:** still `(y₂ − y₁) ÷ (x₂ − x₁)` — simplify carefully

[DIAGRAM:slope_intercept_line]

[DIAGRAM:table_to_slope]

### Example 1 — Table with fractions (Exam Q1)

**What is this about:** You can check whether a table matches a line by plugging in a point and by computing slope from two rows.

**Problem:** A table includes the point **(−1, −3/2)**. The line has slope **3** and y-intercept **3/2**. Verify and write the equation.

**How to think about it:** If the equation is correct, substituting x = −1 should give y = −3/2. Slope tells you how much y changes each time x goes up by 1 — pick any two table rows and divide the change in y by the change in x.

**Solution (step by step):**
1. Write the equation from the given slope and intercept: `y = 3x + 3/2`.
2. Check at x = −1: `y = 3(−1) + 3/2 = −3 + 3/2 = −3/2` ✓ — the point fits.
3. Confirm slope from the table: `(y₂ − y₁) ÷ (x₂ − x₁) = 3` between any two rows.

**Answer:** **Slope = 3, y-intercept = 3/2, equation y = 3x + 3/2**

**Why this works:** A line is fully determined by its slope and y-intercept — if both checks pass, the table and equation describe the same line.

### Example 2 — Graph through (0, 3) and (4, 0) (Exam Q18)

**What is this about:** Two points on a graph are enough to find slope and y-intercept.

**Problem:** A line passes through **(0, 3)** and **(4, 0)**. Find slope and y-intercept.

**How to think about it:** When a point has x = 0, its y-value is the y-intercept — no calculation needed. For slope, imagine walking from one point to the other: how much does y change (rise) for each step in x (run)?

**Solution (step by step):**
1. Read the y-intercept: the line crosses the y-axis at **(0, 3)**, so **b = 3**.
2. Compute slope from (0, 3) to (4, 0): `(0 − 3) ÷ (4 − 0) = −3 ÷ 4 = −3/4`.
3. Write the equation: **y = −3/4 x + 3**.

**Answer:** **y-intercept 3, slope −3/4, equation y = −3/4 x + 3**

**Why this works:** Slope is always "change in y over change in x," and the y-intercept is always the y-value when x = 0.

### Example 3 — Equation y = 9x − 2 (Exam Q15)

**What is this about:** When an equation is already in `y = mx + b` form, you can read m and b directly.

**Problem:** What are the slope and y-intercept of **y = 9x − 2**?

**How to think about it:** Compare the equation to the template `y = mx + b`. The number in front of x is the slope; the standalone number at the end is the y-intercept — watch the sign!

**Solution (step by step):**
1. Match `y = 9x − 2` to `y = mx + b`: **m = 9**, **b = −2**.
2. The y-intercept as a point is **(0, −2)** — two units below the origin.

**Answer:** **Slope 9, y-intercept −2**

**Why this works:** Slope-intercept form is designed so m and b are visible without any algebra.

### Example 4 — Table with slope −2, y-intercept 12 (Exam Q22)

**What is this about:** Once you know slope and y-intercept, you can write the equation and test it on any table row.

**Problem:** A table represents a line with slope **−2** and y-intercept **12**. Write the equation and check a row.

**How to think about it:** Slope −2 means every time x increases by 1, y drops by 2. The y-intercept 12 is the value when x = 0.

**Solution (step by step):**
1. Plug m = −2 and b = 12 into `y = mx + b`: **y = −2x + 12**.
2. When x increases by 1, y decreases by 2 — that matches slope −2.
3. At x = 0, y = 12 ✓ — that matches the y-intercept.

**Answer:** **y = −2x + 12**

**Why this works:** The equation encodes the same "start at 12, go down 2 each step" pattern shown in the table.

### Example 5 — Read m and b from a graph (Exam Q2)

**What is this about:** A graph lets you see slope and y-intercept visually before you write numbers.

**Problem:** A graph shows a line crossing the y-axis below the origin and falling left to right.

**How to think about it:** "Falling left to right" means slope is negative — y gets smaller as x grows. The y-intercept is wherever the line crosses the vertical y-axis, not the x-axis.

**Solution (step by step):**
1. Find where the line crosses the y-axis — read **b** at point `(0, b)`.
2. Notice the line falls left to right → slope is **negative**.
3. Pick two clear grid points and compute `(y₂ − y₁) ÷ (x₂ − x₁)` for m.

**Answer:** Report **m** and **b** from the graph; slope negative, y-intercept read at x = 0.

**Why this works:** Rise over run on a graph is the same calculation as slope from a table — just with coordinates from the picture.

### Exam-style practice

---

**1. Equation y = −1/2 x + 5**

**Problem:** Read the slope and y-intercept from **y = −1/2 x + 5**.

**How to think about it:** The coefficient of x is the slope; the constant term is the y-intercept.

**Solution (step by step):**
1. Compare to `y = mx + b`.
2. m is the number in front of x: **−1/2**.
3. b is the constant at the end: **5**.

**Answer:** **Slope −1/2, y-intercept 5**

---

**2. Table: x = 0, 2, 4 → y = 1, 5, 9**

**Problem:** Find slope and y-intercept from the table and write the equation.

**How to think about it:** Look at the row where x = 0 — that y-value is b. Check that y increases by the same amount each time x increases by 2.

**Solution (step by step):**
1. At x = 0, y = **1** → y-intercept is 1.
2. Slope: `(9 − 1) ÷ (4 − 0) = 8 ÷ 4 = **2**`.
3. Equation: **y = 2x + 1**.

**Answer:** **y = 2x + 1**

---

**3. Which has y-intercept 0? (Exam Q19)**

**Problem:** Which equation has a y-intercept of **0**?

**How to think about it:** The y-intercept is b in `y = mx + b`. When b = 0, the line passes through the origin — there is no constant term added or subtracted.

**Solution (step by step):**
1. Y-intercept 0 means **b = 0**.
2. Look for an equation with no constant term, like **y = 4x**.
3. At x = 0, y = 0 ✓ — the line starts at the origin.

**Answer:** **y = 4x** (or any equation with b = 0)

### Common Mistakes
- Reading **x-intercept** instead of **y-intercept** (where x = 0, not y = 0).
- Sign errors with fractional slopes: `(−3/2 − 0) ÷ (−1 − 0)` needs careful subtraction.
- Confusing **9x** (slope 9) with y-intercept in **y = 9x − 2** — b is **−2**, not 9.

### Mini Summary
- **Equation:** m is the coefficient of x, b is the constant.
- **Graph:** read b at `(0, b)`, find m with rise/run.
- **Table:** slope from any two rows; b when x = 0 (or work backward).
''',

    "activity_2_two_point_equations.md": '''# Activity 2: Equations from Two Points

[KEY]
**Two-point method:**  
1. Slope: `m = (y₂ − y₁) ÷ (x₂ − x₁)`  
2. Point-slope: `y − y₁ = m(x − x₁)` with either point  
3. Simplify to **y = mx + b**
[/KEY]

## Quick Review Notes

### Main Idea
Sometimes you only know two points on a line — like two readings from a science experiment or two locations on a map. Two points are enough to find the slope, then you use one point to build the full equation. This matters because real-world data often gives you coordinates, not a ready-made formula. The three-step method (slope → point-slope → slope-intercept) works every time.

### Key Vocabulary
- **Two-point form:** slope from `(x₁, y₁)` and `(x₂, y₂)`
- **Point-slope form:** y − y₁ = m(x − x₁)
- **Slope-intercept form:** y = mx + b (final goal for most exam items)

[DIAGRAM:two_points_graph]

[DIAGRAM:equation_from_points]

### Example 1 — Points B(−2, −2) and C(−1, −4) (Exam Q3)

**What is this about:** Build a line equation when you know two specific points.

**Problem:** Write the equation of the line through **B(−2, −2)** and **C(−1, −4)**.

**How to think about it:** First find how steep the line is (slope), then use one point to write the equation. Subtracting negatives can be tricky — go slowly: `−4 − (−2) = −4 + 2 = −2`.

**Solution (step by step):**
1. Slope: `m = (−4 − (−2)) ÷ (−1 − (−2)) = −2 ÷ 1 = −2`.
2. Point-slope with B: `y − (−2) = −2(x − (−2))` → `y + 2 = −2(x + 2)`.
3. Distribute and simplify: `y + 2 = −2x − 4` → `y = −2x − 6`.
4. Check with C: `−2(−1) − 6 = 2 − 6 = −4` ✓

**Answer:** **y = −2x − 6**

**Why this works:** Any two points on a line give the same slope, and one point plus slope determines the entire line.

### Example 2 — (0, 6) and (2, 0) (Exam Q4)

**What is this about:** When one point is on the y-axis, the y-intercept is free — you only need slope.

**Problem:** Line through **(0, 6)** and **(2, 0)**.

**How to think about it:** The point (0, 6) tells you b = 6 immediately because x = 0. Then find slope from the two points.

**Solution (step by step):**
1. Y-intercept: point (0, 6) means **b = 6**.
2. Slope: `(0 − 6) ÷ (2 − 0) = −6 ÷ 2 = **−3**`.
3. Equation: **y = −3x + 6**.

**Answer:** **y = −3x + 6**

**Why this works:** (0, 6) is on the y-axis, so its y-coordinate is the y-intercept by definition.

### Example 3 — Point-slope with fractions (Exam Q5)

**What is this about:** The same method works even when coordinates are fractions.

**Problem:** Line through **(4, 1/2)** and **(8, 3)**. Write the equation in slope-intercept form.

**How to think about it:** Treat fractions like any other numbers. When subtracting, rewrite 3 as 6/2 so you can combine: `3 − 1/2 = 5/2`.

**Solution (step by step):**
1. Slope: `m = (3 − 1/2) ÷ (8 − 4) = (5/2) ÷ 4 = 5/8`.
2. Point-slope: `y − 1/2 = 5/8(x − 4)`.
3. Distribute: `y = 5/8 x − 5/2 + 1/2 = 5/8 x − 2`.

**Answer:** **y = 5/8 x − 2**

**Why this works:** Fractions do not change the method — only the arithmetic is a bit longer.

### Example 4 — (2, −1) and (5, −10) (Exam Q13)

**What is this about:** Practice the full two-point method with negative coordinates.

**Problem:** Find the equation through **(2, −1)** and **(5, −10)**.

**How to think about it:** Both y-values are negative, and y drops from −1 to −10 as x goes from 2 to 5 — expect a negative slope.

**Solution (step by step):**
1. Slope: `m = (−10 − (−1)) ÷ (5 − 2) = −9 ÷ 3 = −3`.
2. Point-slope: `y − (−1) = −3(x − 2)` → `y + 1 = −3x + 6`.
3. Solve for y: **y = −3x + 5**.

**Answer:** **y = −3x + 5**

**Why this works:** Checking with the second point confirms you distributed the −3 correctly.

### Example 5 — Fill in slope 3 (Exam Q6)

**What is this about:** Verify a claimed slope and write the equation when one point is on the y-axis.

**Problem:** A line through **(0, −7)** and **(2, −1)** has slope **3**. Verify.

**How to think about it:** Compute slope from the two points and see if it equals 3. Since (0, −7) is the y-intercept, b = −7.

**Solution (step by step):**
1. Slope check: `m = (−1 − (−7)) ÷ (2 − 0) = 6 ÷ 2 = 3` ✓
2. Y-intercept from (0, −7): **b = −7**.
3. Equation: **y = 3x − 7**.

**Answer:** **Slope = 3, equation y = 3x − 7**

**Why this works:** Slope from two points must match the claimed slope — if it does, the equation follows directly.

### Example 6 — Best method for two points (Exam Q11)

**What is this about:** Exams often ask which steps to use, not just the final answer.

**Problem:** Which steps write an equation from **(−3, 5)** and **(1, −3)**?

**How to think about it:** You cannot write `y = mx + b` until you know m. Always compute slope first, then use point-slope with either point.

**Solution (step by step):**
1. Compute slope: `m = (−3 − 5) ÷ (1 − (−3)) = −8 ÷ 4 = −2`.
2. Use point-slope with either point, e.g. `y − 5 = −2(x − (−3))`.
3. Simplify to **y = −2x − 1**.

**Answer:** **Find slope, then use point-slope form with one of the points.**

**Why this works:** Slope is the only missing piece — one point plus slope determines everything else.

### Exam-style practice

---

**1. Through (1, 4) and (3, 10)**

**Problem:** Write the equation of the line through **(1, 4)** and **(3, 10)**.

**How to think about it:** y jumps from 4 to 10 when x goes from 1 to 3 — find that rate of change first.

**Solution (step by step):**
1. Slope: `(10 − 4) ÷ (3 − 1) = 6 ÷ 2 = 3`.
2. Point-slope: `y − 4 = 3(x − 1)` → `y = 3x − 3 + 4 = 3x + 1`.

**Answer:** **y = 3x + 1**

---

**2. Through (−4, 0) and (0, 2)**

**Problem:** Write the equation through **(−4, 0)** and **(0, 2)**.

**How to think about it:** (0, 2) gives b = 2 right away. Slope tells you how y changes from x = −4 to x = 0.

**Solution (step by step):**
1. Y-intercept: **b = 2** from (0, 2).
2. Slope: `(2 − 0) ÷ (0 − (−4)) = 2 ÷ 4 = 1/2`.
3. Equation: **y = 1/2 x + 2**.

**Answer:** **y = 1/2 x + 2**

---

**3. Which table matches y = −2x + 8? (Exam Q20)**

**Problem:** Pick the table that represents **y = −2x + 8**.

**How to think about it:** At x = 0, y must be 8. Each time x increases by 1, y should drop by 2.

**Solution (step by step):**
1. Check y-intercept: when x = 0, y = 8.
2. Check slope: y should decrease by 2 for each +1 in x.
3. Pick the table with constant change **−2** in y per +1 in x and y = 8 when x = 0.

**Answer:** The table with **(0, 8)** and y dropping by 2 each step

### Common Mistakes
- Subtracting points in the wrong order — stay consistent: `(y₂ − y₁) ÷ (x₂ − x₁)`.
- Forgetting to distribute **m** when using point-slope: `−2(x + 2) = −2x − 4`.
- Using **(0, 6)** as slope instead of y-intercept in Q4.

### Mini Summary
- **Two points → slope → point-slope → y = mx + b**
- If a point is **(0, b)**, b is the y-intercept immediately.
- Always **check** with the second point.
''',

    "activity_3_point_slope_form.md": '''# Activity 3: Point-Slope Form

[KEY]
**Point-slope form:** `y − y₁ = m(x − x₁)`  
Use when you know **one point** and the **slope**. Expand and combine like terms to get **y = mx + b**.
[/KEY]

## Quick Review Notes

### Main Idea
Point-slope form is a quick way to write a line when you already know the slope and one point on the line. It is like saying: "Start at this point, and move with this steepness." You will often convert it to slope-intercept form because that form is easier to graph and compare. Watch the signs inside the parentheses — they trip up many students on exams.

### Key Vocabulary
- **Point-slope form:** y − y₁ = m(x − x₁)
- **Convert to slope-intercept:** distribute m, add y₁ to both sides
- **Verify a point:** substitute x and y into the equation

[DIAGRAM:point_slope_convert]

[DIAGRAM:line_through_point]

### Example 1 — Convert y − 5 = 6(x + 1) (Exam Q8)

**What is this about:** Expand point-slope form to get slope-intercept form.

**Problem:** Rewrite **y − 5 = 6(x + 1)** in slope-intercept form.

**How to think about it:** Distribute the 6 across (x + 1), then add 5 to both sides to isolate y. The `(x + 1)` means the known point had x₁ = −1.

**Solution (step by step):**
1. Distribute: `y − 5 = 6x + 6`.
2. Add 5 to both sides: `y = 6x + 6 + 5`.
3. Combine: **y = 6x + 11** — slope 6, y-intercept 11.

**Answer:** **y = 6x + 11**

**Why this works:** Slope-intercept form makes m and b visible for graphing and comparison.

### Example 2 — Point (−7, 2), slope 1/2 (Exam Q16)

**What is this about:** Write point-slope from a point and slope, then convert.

**Problem:** Write point-slope and slope-intercept for slope **1/2** through **(−7, 2)**.

**How to think about it:** Plug x₁ = −7 and y₁ = 2 into `y − y₁ = m(x − x₁)`. Subtracting a negative becomes addition: `x − (−7) = x + 7`.

**Solution (step by step):**
1. Point-slope: `y − 2 = 1/2(x − (−7))` → **y − 2 = 1/2(x + 7)**.
2. Distribute: `y − 2 = 1/2 x + 7/2`.
3. Add 2 (write as 4/2): **y = 1/2 x + 11/2**.

**Answer:** **y − 2 = 1/2(x + 7)** or **y = 1/2 x + 11/2**

**Why this works:** Both forms describe the same line — point-slope shows the starting point; slope-intercept shows m and b.

### Example 3 — Does (1, 6) lie on y = 4x + 2? (Exam Q9)

**What is this about:** Test whether a point satisfies an equation by substituting.

**Problem:** Is **(1, 6)** on the line **y = 4x + 2**?

**How to think about it:** Plug x = 1 into the right side. If the result equals 6, the point is on the line.

**Solution (step by step):**
1. Substitute x = 1: `4(1) + 2 = 4 + 2 = 6`.
2. The y-coordinate of the point is also 6 ✓

**Answer:** **Yes — (1, 6) is on the line.**

**Why this works:** A point is on a line when its coordinates make the equation true.

### Example 4 — Does (5, 3) lie on y = x − 2? (Exam Q14)

**What is this about:** Same verification idea with a simpler equation.

**Problem:** Verify **(5, 3)** on **y = x − 2**.

**How to think about it:** Replace x with 5 and see if you get y = 3.

**Solution (step by step):**
1. Substitute x = 5: `5 − 2 = 3`.
2. That matches the point's y-value ✓

**Answer:** **Yes — (5, 3) satisfies the equation.**

**Why this works:** If both coordinates work, the point lies on the line.

### Example 5 — Write point-slope from a graph (Exam Q10)

**What is this about:** Build an equation from slope and a point read from a graph.

**Problem:** A line has slope **−4** and passes through **(2, 1)**. Write the equation.

**How to think about it:** Slope −4 means the line falls steeply. Use (2, 1) as your known point in point-slope form.

**Solution (step by step):**
1. Point-slope: `y − 1 = −4(x − 2)`.
2. Distribute: `y − 1 = −4x + 8`.
3. Add 1: **y = −4x + 9**.

**Answer:** **y − 1 = −4(x − 2)** or **y = −4x + 9**

**Why this works:** One point and slope fully determine the line — point-slope captures both immediately.

### Example 6 — Missing y on point-slope (Exam Q12)

**What is this about:** Use point-slope to find a missing y-value at a given x.

**Problem:** Line with slope **2/3** through **(6, −4)**. Find y when x = 9.

**How to think about it:** Write point-slope, then plug in x = 9 and solve for y.

**Solution (step by step):**
1. Point-slope: `y − (−4) = 2/3(x − 6)` → `y + 4 = 2/3(x − 6)`.
2. Substitute x = 9: `y + 4 = 2/3(3) = 2`.
3. Solve: `y = 2 − 4 = **−2**`.

**Answer:** **y = −2** when x = 9

**Why this works:** Once you have the line's rule, any x-value gives you the matching y.

### Exam-style practice

---

**1. Convert y + 3 = −2(x − 1)**

**Problem:** Rewrite **y + 3 = −2(x − 1)** in slope-intercept form.

**How to think about it:** `y + 3` means y₁ = −3. Distribute −2, then subtract 3 from both sides.

**Solution (step by step):**
1. Distribute: `y + 3 = −2x + 2`.
2. Subtract 3: **y = −2x − 1**.

**Answer:** **y = −2x − 1**

---

**2. Slope −1 through (0, 5)**

**Problem:** Write the equation with slope **−1** through **(0, 5)**.

**How to think about it:** When x₁ = 0, point-slope collapses — you already have the y-intercept.

**Solution (step by step):**
1. Point-slope: `y − 5 = −1(x − 0)` → `y − 5 = −x`.
2. Add 5: **y = −x + 5**.

**Answer:** **y = −x + 5**

---

**3. Which point-slope matches slope 5 through (2, −1)? (Exam Q21)**

**Problem:** Pick the correct point-slope equation for slope 5 through **(2, −1)**.

**How to think about it:** Use `y − y₁ = m(x − x₁)` with y₁ = −1 and x₁ = 2. Watch the double negative: `y − (−1) = y + 1`.

**Solution (step by step):**
1. Plug in: `y − (−1) = 5(x − 2)`.
2. Simplify left side: **y + 1 = 5(x − 2)**.

**Answer:** **y + 1 = 5(x − 2)**

### Common Mistakes
- Sign error: **(x + 1)** means x₁ = **−1**, not 1.
- Stopping at point-slope when the question asks for **slope-intercept**.
- Checking the wrong point: substitute **both** x and y when verifying.

### Mini Summary
- Point-slope: **y − y₁ = m(x − x₁)**
- Distribute m, solve for y to convert to **y = mx + b**
- **Substitute** to test whether a point is on a line.
''',

    "activity_4_standard_form.md": '''# Activity 4: Standard Form & Conversion

[KEY]
**Standard form:** `Ax + By = C`  
To get slope-intercept, **solve for y**: isolate the y-term, divide by its coefficient.  
**Slope** = −A/B, **y-intercept** = C/B (when B ≠ 0) — but solving step-by-step avoids memorization errors.
[/KEY]

## Quick Review Notes

### Main Idea
Standard form `Ax + By = C` is another way to write the same line — you will see it on exams and in word problems. To graph it or read the slope, you need to **solve for y** and convert to slope-intercept form. The biggest trap is sign errors when you divide by a **negative** number (like −4y). Going step by step beats memorizing a shortcut, especially when fractions appear.

### Key Vocabulary
- **Standard form:** Ax + By = C (A, B, C integers; A ≥ 0 often preferred)
- **Convert to slope-intercept:** y = mx + b
- **Sign error:** dividing by −4 changes signs on **both** sides

[DIAGRAM:standard_to_slope]

[DIAGRAM:jill_error_steps]

### Example 1 — 15x − 4y = −2 (Exam Q7)

**What is this about:** Convert standard form to slope-intercept by isolating y.

**Problem:** Write **15x − 4y = −2** in slope-intercept form.

**How to think about it:** Move the x-term to the other side first, leaving −4y alone. Then divide **every term** on that side by −4 — the negative flips both signs.

**Solution (step by step):**
1. Subtract 15x from both sides: `−4y = −15x − 2`.
2. Divide both sides by −4: `y = (−15x) ÷ (−4) + (−2) ÷ (−4)`.
3. Simplify: **y = (15/4)x + 1/2** — slope 15/4, y-intercept 1/2.

**Answer:** **y = (15/4)x + 1/2**

**Why this works:** Dividing by −4 turns −15x into +15x/4 and −2 into +1/2.

### Example 2 — Jill's error on practice test Q8 ⚠️ Focus

**What is this about:** Spot a common sign mistake when converting standard form.

**Problem:** Jill converts **15x − 4y = −2** and gets **y = (15/4)x − 1/2**. What went wrong?

**How to think about it:** Jill's answer has the right slope but the wrong sign on the y-intercept. That usually means she divided by +4 instead of −4, or dropped a negative on the constant.

**Solution (step by step):**
1. Correct first step: `−4y = −15x − 2`.
2. Divide by **−4** (not +4): `y = (15/4)x + 1/2`.
3. Jill wrote −1/2 instead of +1/2 — a sign error on the constant.

**Answer:** **Jill made a sign error when dividing by −4; the y-intercept should be +1/2.**

**Why this works:** Dividing by a negative number flips the sign of every term on that side.

### Example 3 — 3x + 6y = 12 (Exam Q1 practice)

**What is this about:** Practice conversion when the y-coefficient is positive.

**Problem:** Convert **3x + 6y = 12** to slope-intercept form.

**How to think about it:** Move 3x to the right (it becomes −3x), then divide by 6 to get y alone.

**Solution (step by step):**
1. Subtract 3x: `6y = −3x + 12`.
2. Divide by 6: `y = −3x/6 + 12/6`.
3. Simplify: **y = −1/2 x + 2**.

**Answer:** **y = −1/2 x + 2**

**Why this works:** Dividing every term by the y-coefficient gives slope-intercept form directly.

### Example 4 — Find y-intercept from 2x − 5y = 10 (Exam Q4 practice)

**What is this about:** You can find the y-intercept without full conversion by setting x = 0.

**Problem:** What is the y-intercept of **2x − 5y = 10**?

**How to think about it:** The y-intercept is where x = 0. Plug in x = 0 and solve for y — much faster than converting the whole equation.

**Solution (step by step):**
1. Set x = 0: `2(0) − 5y = 10` → `−5y = 10`.
2. Divide by −5: `y = −2`.
3. Y-intercept is **(0, −2)** or **b = −2**.

**Answer:** **−2**

**Why this works:** At the y-intercept, x is always 0 — so the x-term disappears.

### Example 5 — Which is equivalent to y = 3x − 1? (Exam Q15 practice)

**What is this about:** Convert slope-intercept back to standard form to match answer choices.

**Problem:** Pick the standard-form equation for **y = 3x − 1**.

**How to think about it:** Move all terms to one side so the equation equals a constant. Multiply if needed to clear fractions.

**Solution (step by step):**
1. Subtract 3x from both sides: `−3x + y = −1`.
2. Multiply by −1 (optional, for cleaner form): **3x − y = 1**.
3. Both `3x − y = 1` and `−3x + y = −1` describe the same line.

**Answer:** **3x − y = 1**

**Why this works:** Equivalent forms differ in sign arrangement but represent the same set of (x, y) pairs.

### Example 6 — Standard form from context (Exam Q25)

**What is this about:** Build standard form from intercept information.

**Problem:** A line has x-intercept **6** and y-intercept **3**. Write standard form.

**How to think about it:** The line passes through (6, 0) and (0, 3). Intercept form `x/6 + y/3 = 1` is a shortcut to standard form.

**Solution (step by step):**
1. Intercept form: `x/6 + y/3 = 1`.
2. Multiply every term by 6: `x + 2y = 6`.

**Answer:** **x + 2y = 6**

**Why this works:** Intercept form uses both axis crossing points to build the equation without finding slope first.

### Exam-style practice

---

**1. Convert −2x + 8y = 16**

**Problem:** Write **−2x + 8y = 16** in slope-intercept form.

**How to think about it:** Add 2x to both sides, then divide by 8.

**Solution (step by step):**
1. Add 2x: `8y = 2x + 16`.
2. Divide by 8: `y = 2x/8 + 16/8`.
3. Simplify: **y = 1/4 x + 2**.

**Answer:** **y = 1/4 x + 2**

---

**2. Slope of 5x + 10y = 20**

**Problem:** Find the slope of **5x + 10y = 20**.

**How to think about it:** Convert to slope-intercept form — the coefficient of x is the slope.

**Solution (step by step):**
1. Subtract 5x: `10y = −5x + 20`.
2. Divide by 10: **y = −1/2 x + 2**.
3. Slope is **−1/2**.

**Answer:** **Slope −1/2**

---

**3. Fix the sign error (Exam Q8 style)**

**Problem:** A student converts **4x − 2y = 8** and writes **y = 2x + 4**. Find and fix the error.

**How to think about it:** When you move 4x to the right, it becomes −4x. When you divide by −2, **both** terms on the right flip signs — +8 becomes −4, not +4.

**Solution (step by step):**
1. Start: `4x − 2y = 8`.
2. Subtract 4x: `−2y = −4x + 8`.
3. Divide by −2: `y = 2x − 4` (not y = 2x + 4).
4. The student forgot that dividing by −2 changes +8 to **−4**.

**Answer:** **Correct equation is y = 2x − 4; the sign error is on the constant term (+4 should be −4).**

### Common Mistakes
- Dividing only one term when isolating y.
- **Jill trap:** dividing by +4 instead of −4 on **−4y = −15x − 2**.
- Thinking standard form gives slope **A/B** without the negative: slope is **−A/B**.

### Mini Summary
- **Solve for y** — one step at a time.
- When dividing by a **negative** coefficient of y, flip signs on the whole right side.
- Set **x = 0** for y-intercept, **y = 0** for x-intercept without full conversion.
''',

    "activity_5_context_meaning.md": '''# Activity 5: Slope & Y-Intercept in Context

[KEY]
In a model **y = mx + b**:  
- **b (y-intercept)** = starting amount when x = 0 (initial value).  
- **m (slope)** = rate of change per 1 unit of x (dollars per day, miles per hour, etc.).  
**Substitute** x to evaluate; interpret units in your answer sentence.
[/KEY]

## Quick Review Notes

### Main Idea
Real-world problems hide linear equations inside stories about money, distance, food, or time. In `y = mx + b`, **b** is where you start and **m** is how fast things change per unit of x. Identifying what x and y represent is the first step — then you can predict future values and explain the situation in plain English. This is how math connects to everyday decisions.

### Key Vocabulary
- **Initial value:** y-intercept; output at time 0 or start
- **Rate of change:** slope with units (e.g., dollars per day)
- **Evaluate:** plug a given x into y = mx + b
- **Interpret:** explain what m and b mean in the situation

[DIAGRAM:inez_phone_card]

[DIAGRAM:washing_machine_model]

### Example 1 — Inez's phone card (Exam Q6)

**What is this about:** Read the meaning of slope and y-intercept from a money story.

**Problem:** Inez's prepaid card starts with **$850** and loses **$50** per day of use. Model: **y = −50x + 850** (x = days, y = balance).

**How to think about it:** x counts days; y counts dollars left. The +850 is the starting balance (b). The −50 means money goes down $50 each day (m).

**Solution (step by step):**
1. Identify variables: x = days, y = balance in dollars.
2. Y-intercept **850** → starting balance **$850**.
3. Slope **−50** → balance **decreases $50 per day**.

**Answer:** **Initial value $850; rate −$50 per day**

**Why this works:** b is always the output when x = 0 — here, day 0 means the full starting amount.

### Example 2 — Washing machine repair (Exam Q2)

**What is this about:** A flat fee plus an hourly rate is a classic linear model.

**Problem:** Cost **y = 45x + 35** where x = hours of labor.

**How to think about it:** Even with zero hours of work, there is a base charge (b = 35). Each extra hour adds $45 (m = 45).

**Solution (step by step):**
1. Y-intercept **35** → flat **$35** service fee.
2. Slope **45** → **$45 per hour** of labor.
3. Total cost = fee + (rate × hours).

**Answer:** **$35 initial fee plus $45 per hour**

**Why this works:** The y-intercept captures fixed costs; the slope captures per-unit charges.

### Example 3 — Dog food remaining (Exam Q5)

**What is this about:** Plug in a value of x to predict y in a real situation.

**Problem:** **y = −15x + 430** models pounds of dog food left after x days. How much after **21 days**?

**How to think about it:** Substitute x = 21 into the equation. The slope −15 means 15 pounds are used each day.

**Solution (step by step):**
1. Substitute x = 21: `y = −15(21) + 430`.
2. Compute: `−315 + 430 = 115`.
3. Include units: **115 pounds** remain.

**Answer:** **115 pounds**

**Why this works:** The equation tracks the starting amount minus daily usage.

### Example 4 — Library computer time (Exam Q8 practice)

**What is this about:** Interpret slope and y-intercept even when b is negative.

**Problem:** **y = 8x − 3** where x = weeks and y = hours of computer time available.

**How to think about it:** Slope 8 means hours grow by 8 each week. A negative y-intercept can mean a starting "deficit" in the model — read the story carefully.

**Solution (step by step):**
1. Slope **8** → gain **8 hours per week**.
2. Y-intercept **−3** → at week 0, the model shows −3 hours (a baseline adjustment below zero).
3. Each week adds 8 hours to that starting point.

**Answer:** **Rate +8 hours/week; initial value −3 hours in the model**

**Why this works:** Negative b does not break the model — it just means the starting value in the story is below zero.

### Example 5 — Miles driven (Exam Q3 practice)

**What is this about:** A proportional relationship has y-intercept 0.

**Problem:** **y = 60x** models miles y after x hours at constant speed.

**How to think about it:** No constant term means you start at 0 miles. The 60 is speed — miles per hour.

**Solution (step by step):**
1. Slope **60** → **60 miles per hour**.
2. Y-intercept **0** → **0 miles** at time 0 (no head start).
3. Distance = speed × time.

**Answer:** **Speed 60 mph; starting distance 0 miles**

**Why this works:** When b = 0, the relationship is proportional — double the time, double the distance.

### Example 6 — Evaluate and interpret (Exam Q18 practice)

**What is this about:** Find a value and explain what the slope means in context.

**Problem:** A tank has **y = 120 − 6x** gallons after x minutes of draining. Find y at x = 10 and explain slope.

**How to think about it:** Substitute x = 10 to find remaining gallons. Slope −6 means the tank loses 6 gallons every minute.

**Solution (step by step):**
1. Substitute x = 10: `y = 120 − 6(10) = 120 − 60 = 60`.
2. Slope **−6** → loses **6 gallons per minute**.
3. Answer with units: **60 gallons** left.

**Answer:** **60 gallons left; drains 6 gal/min**

**Why this works:** Negative slope matches a draining tank — the amount decreases over time.

### Exam-style practice

---

**1. y = 12x + 50, x = months, y = savings ($). What do 12 and 50 mean?**

**Problem:** Interpret **m = 12** and **b = 50** in the savings model.

**How to think about it:** b is savings at month 0; m is how much is added each month.

**Solution (step by step):**
1. **50** → starting savings of **$50**.
2. **12** → saves **$12 per month**.
3. Say both with units in a sentence.

**Answer:** **$50 starting savings; saves $12 per month**

---

**2. y = −3x + 200, find y when x = 40**

**Problem:** Evaluate **y = −3x + 200** at x = 40.

**How to think about it:** Plug in 40 for x. Watch the negative: −3(40) = −120.

**Solution (step by step):**
1. Substitute: `y = −3(40) + 200`.
2. Compute: `−120 + 200 = 80`.

**Answer:** **y = 80**

---

**3. Which slope means "cost goes down each week"? (Exam Q23)**

**Problem:** Pick the slope that means cost decreases over time.

**How to think about it:** "Goes down" means a negative rate of change — y decreases as x increases.

**Solution (step by step):**
1. Decreasing quantity → **negative slope**.
2. Example: **−15** in the dog-food model (food left drops 15 lb per day).
3. Positive slope would mean cost increases.

**Answer:** The **negative** slope (e.g. **−15**)

### Common Mistakes
- Swapping **m** and **b**: $850 is the **starting** amount (b), not −50.
- Forgetting units: say **"$50 per day"**, not just "50".
- Sign errors when evaluating: **−15(21) = −315**, not +315.

### Mini Summary
- **b** = start; **m** = change per 1 unit of x (with units!).
- **Plug in** x to find y at a specific time.
- **Negative slope** = quantity decreases as x increases.
''',

    "activity_6_compare_functions.md": '''# Activity 6: Comparing Linear Functions

[KEY]
Compare lines by **slope** (steepness/rate) and **y-intercept** (starting value).  
Convert all forms to **y = mx + b** first. Same **b**, different **m** → same start, different rates.  
**Steeper** line → larger **|m|**.
[/KEY]

## Quick Review Notes

### Main Idea
Exams often give you two lines in different forms — an equation, a graph, or a table — and ask you to compare them. Convert everything to `y = mx + b` first, then compare m (steepness/rate) and b (starting value). For "which is steeper," use absolute value of slope — a line falling at −10 is steeper than one rising at 8. This skill helps you pick the better deal, faster growth, or matching representation.

### Key Vocabulary
- **Steeper:** larger |slope|
- **Same y-intercept:** same b, graphs cross y-axis at same point
- **Equivalent equations:** same m and b after simplification
- **x-intercept:** set y = 0; use slope to build equation from intercept + slope

[DIAGRAM:compare_two_lines]

[DIAGRAM:same_y_intercept]

### Example 1 — Compare y = −10x + 6 vs y − 36 = 8(x − 4) (Exam Q7)

**What is this about:** Convert point-slope to slope-intercept, then compare steepness.

**Problem:** Which line is steeper?

**How to think about it:** "Steeper" means larger |m|, not just larger m. Convert the second equation before comparing.

**Solution (step by step):**
1. Line 1: **y = −10x + 6** → m = **−10**, |m| = 10.
2. Line 2: `y − 36 = 8(x − 4)` → distribute → `y = 8x − 32 + 36 = 8x + 4` → m = **8**, |m| = 8.
3. Compare: |−10| = 10 > |8| = 8 → Line 1 is steeper.

**Answer:** **y = −10x + 6** (|m| = 10 > 8)

**Why this works:** Steepness depends on how quickly y changes, regardless of direction.

### Example 2 — Jeremy's steepness claim (Exam Q3)

**What is this about:** Negative slope can still mean a steeper line.

**Problem:** Jeremy says a line with slope **−5** is steeper than a line with slope **3**. Is he correct?

**How to think about it:** Steepness uses |m|, not the sign. |−5| = 5, which is greater than |3| = 3.

**Solution (step by step):**
1. |−5| = **5**.
2. |3| = **3**.
3. 5 > 3 → Jeremy is **correct** — ignore the negative sign for steepness only.

**Answer:** **Yes — |−5| > |3|**

**Why this works:** A falling line at slope −5 changes y faster than a rising line at slope 3.

### Example 3 — y = 2x + 2 vs graph (Exam Q17)

**What is this about:** Check whether a graph shows the same line as an equation.

**Problem:** Does a graph show the same line as **y = 2x + 2**?

**How to think about it:** Read the graph's y-intercept at (0, b) and compute slope from two points. Both must match m = 2 and b = 2.

**Solution (step by step):**
1. Read y-intercept on the graph — should be **2**.
2. Compute slope (rise/run) — should be **2**.
3. Test a second point from the graph in y = 2x + 2.

**Answer:** **Same line if graph has slope 2 and y-intercept 2**

**Why this works:** Same m and b means the same line, no matter how it is displayed.

### Example 4 — y = 4x + 5 vs table (Exam Q24)

**What is this about:** Match an equation to a table by checking b and m.

**Problem:** Which table represents **y = 4x + 5**?

**How to think about it:** At x = 0, y must be 5. Each +1 in x should add 4 to y.

**Solution (step by step):**
1. Y-intercept: at x = 0, y = **5**.
2. Slope: each +1 in x adds **4** to y.
3. Pick the table with constant difference **4** and y = 5 when x = 0.

**Answer:** Table with **y-intercept 5** and slope **4**

**Why this works:** Tables and equations describe the same pattern when m and b match.

### Example 5 — x-intercept 12, slope 3/8 vs table (Exam Q23)

**What is this about:** Build an equation from x-intercept and slope, then match a table.

**Problem:** Line has **x-intercept 12** and slope **3/8**. Which table matches?

**How to think about it:** x-intercept (12, 0) is a known point. Use point-slope or find b by plugging in the point.

**Solution (step by step):**
1. Known point: **(12, 0)**.
2. Point-slope: `y = 3/8(x − 12)` → y-intercept: `3/8(−12) = −9/2`.
3. Equation: **y = 3/8 x − 9/2** — check table rows against this.

**Answer:** Table consistent with **m = 3/8** and point **(12, 0)**

**Why this works:** One point plus slope determines the line — then every table row must satisfy the equation.

### Example 6 — Same y-intercept (Exam Q19)

**What is this about:** Find a line with the same starting value but a different rate.

**Problem:** Which equation has the **same y-intercept** as **y = −2x + 7** but a different slope?

**How to think about it:** Same y-intercept means same b = 7. Different slope means any m other than −2.

**Solution (step by step):**
1. Same b = **7** → constant term is +7.
2. Different slope → m ≠ −2.
3. Examples: **y = 3x + 7** or **y = 1/2 x + 7**.

**Answer:** Any **y = mx + 7** with m ≠ −2

**Why this works:** Lines with the same b cross the y-axis at the same point but tilt differently.

### Exam-style practice

---

**1. Are y = 5x − 1 and 10x − 2y = 2 the same line?**

**Problem:** Determine whether **y = 5x − 1** and **10x − 2y = 2** represent the same line.

**How to think about it:** Convert the standard-form equation to slope-intercept and compare m and b.

**Solution (step by step):**
1. Convert: `10x − 2y = 2` → `−2y = −10x + 2` → **y = 5x − 1**.
2. Compare: same m = 5 and same b = −1.

**Answer:** **Yes, equivalent**

---

**2. Which is steeper: y = x + 1 or y = −3x + 1?**

**Problem:** Compare steepness of **y = x + 1** and **y = −3x + 1**.

**How to think about it:** Use |m|: |1| = 1 vs |−3| = 3.

**Solution (step by step):**
1. Line 1: |m| = |1| = 1.
2. Line 2: |m| = |−3| = 3.
3. 3 > 1 → second line is steeper.

**Answer:** **y = −3x + 1**

---

**3. Table A: (0, 4), (1, 7), (2, 10). Match equation? (Exam Q22 practice)**

**Problem:** Which equation matches the table **(0, 4), (1, 7), (2, 10)**?

**How to think about it:** y goes up by 3 each time x increases by 1. At x = 0, y = 4.

**Solution (step by step):**
1. Slope: (7 − 4) ÷ (1 − 0) = **3**.
2. Y-intercept: at x = 0, y = **4**.
3. Equation: **y = 3x + 4**.

**Answer:** **y = 3x + 4**

### Common Mistakes
- Comparing steepness using **signed** slope only — use **|m|**.
- Forgetting to convert **y − 36 = 8(x − 4)** before comparing.
- Matching **x-intercept** when the question asks for **y-intercept** (Q19 vs Q23).

### Mini Summary
- Convert everything to **y = mx + b** first.
- **Steeper** → larger **|m|**; **same start** → same **b**.
- Tables: check **constant difference** (m) and value at **x = 0** (b).
''',

    "unit_3_writing_linear_equations_lesson_notes.md": '''# Unit 3: Writing Equations for Linear Relationships — Overview

| Activity | Topic | Key idea |
|----------|-------|----------|
| **1** | Reading Slope & Y-Intercept | From tables, graphs, equations (fractions); Q1, Q18, Q15, Q22 |
| **2** | Equations from Two Points | Slope → point-slope → y = mx + b; Q3, Q4, Q5, Q6, Q11, Q13 |
| **3** | Point-Slope Form | Write and convert; verify points on a line; Q8, Q9, Q14, Q16 |
| **4** | Standard Form | Ax + By = C → slope-intercept; Jill's sign error; Q7, practice Q8 |
| **5** | Context Meaning | Inez phone card, washing machine, dog food; evaluate & interpret |
| **6** | Compare Functions | Steepness, same y-intercept; equation vs graph/table; Q3, Q7, Q17, Q23, Q24 |

**Exam focus areas (33-page exam — 8 practice + 25 test questions):** Reading m and b from tables with fractions (Q1, Q22), two-point equations (Q3, Q4, Q13), point-slope conversion (Q8, Q16), standard-form sign errors (Q7, Jill Q8), context interpretation (Q6 Inez, Q5 dog food), comparing representations (Q7, Q17, Q23, Q24).

**Weak areas to review:** Jill's division-by-negative sign trap (Activity 4), fractional point-slope (Q5, Q16), x-intercept + slope to match tables (Q23), Jeremy steepness with negative slope (Q3).

Open each activity for full notes, diagrams, and worked exam-style problems. Use **Daily Practice** for quiz sets with graphs and tables.
''',
}


def main() -> list[Path]:
    created: list[Path] = []
    for filename, content in ACTIVITIES.items():
        path = NOTES / filename
        path.write_text(content.strip() + "\n", encoding="utf-8")
        created.append(path)
        print(f"  wrote {path.name}")
    print("Done.")
    return created


if __name__ == "__main__":
    main()
