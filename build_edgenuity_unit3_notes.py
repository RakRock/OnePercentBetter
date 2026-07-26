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
Every linear relationship can be written `y = mx + b`. From a table, compute slope between any two rows and find b by substituting a point. From a graph, read where the line crosses the y-axis and count rise/run. From an equation, identify m and b directly — watch fractions and negative signs.

### Key Vocabulary
- **Slope (m):** change in y ÷ change in x; steepness of the line
- **Y-intercept (b):** y-value when x = 0; point `(0, b)`
- **Slope-intercept form:** y = mx + b
- **Fractional slope:** still `(y₂ − y₁) ÷ (x₂ − x₁)` — simplify carefully

[DIAGRAM:slope_intercept_line]

[DIAGRAM:table_to_slope]

### Example 1 — Table with fractions (Exam Q1)

**Problem:** A table includes the point **(−1, −3/2)**. The line has slope **3** and y-intercept **3/2**. Verify and write the equation.

**Solution:**
- Equation: `y = 3x + 3/2`
- Check at x = −1: `y = 3(−1) + 3/2 = −3 + 3/2 = **−3/2**` ✓
- Slope from two table rows: `(y₂ − y₁) ÷ (x₂ − x₁) = **3**`

**Answer:** **Slope = 3, y-intercept = 3/2, equation y = 3x + 3/2**

### Example 2 — Graph through (0, 3) and (4, 0) (Exam Q18)

**Problem:** A line passes through **(0, 3)** and **(4, 0)**. Find slope and y-intercept.

**Solution:**
- **Y-intercept:** line crosses y-axis at **(0, 3)** → **b = 3**
- **Slope:** `(0 − 3) ÷ (4 − 0) = −3 ÷ 4 = **−3/4**`

**Answer:** **y-intercept 3, slope −3/4, equation y = −3/4 x + 3**

### Example 3 — Equation y = 9x − 2 (Exam Q15)

**Problem:** What are the slope and y-intercept of **y = 9x − 2**?

**Solution:**
- Compare to `y = mx + b`: **m = 9**, **b = −2**
- Y-intercept point: **(0, −2)**

**Answer:** **Slope 9, y-intercept −2**

### Example 4 — Table with slope −2, y-intercept 12 (Exam Q22)

**Problem:** A table represents a line with slope **−2** and y-intercept **12**. Write the equation and check a row.

**Solution:**
- Equation: **y = −2x + 12**
- When x increases by 1, y decreases by 2 (slope −2)
- At x = 0, y = **12** ✓

**Answer:** **y = −2x + 12**

### Example 5 — Read m and b from a graph (Exam Q2)

**Problem:** A graph shows a line crossing the y-axis below the origin and falling left to right.

**Solution:**
- Read **b** at `(0, b)` on the y-axis
- Slope is **negative** (line falls left to right)
- Use two clear grid points: `(y₂ − y₁) ÷ (x₂ − x₁)`

**Answer:** Report **m** and **b** from the graph; slope negative, y-intercept read at x = 0.

### Exam-style practice

---

**1. Equation y = −1/2 x + 5**

**Solution:** Slope **−1/2**, y-intercept **5**.

---

**2. Table: x = 0, 2, 4 → y = 1, 5, 9**

**Solution:** Slope `(9 − 1) ÷ (4 − 0) = **2**`; at x = 0, y = **1** → **y = 2x + 1**.

---

**3. Which has y-intercept 0? (Exam Q19)**

**Solution:** Equation with **b = 0** (no constant term), e.g. **y = 4x**.

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
When you know two points on a line, find the slope first, then plug one point into point-slope form and solve for b. If one point is on the y-axis, its y-value is b directly and you only need the slope.

### Key Vocabulary
- **Two-point form:** slope from `(x₁, y₁)` and `(x₂, y₂)`
- **Point-slope form:** y − y₁ = m(x − x₁)
- **Slope-intercept form:** y = mx + b (final goal for most exam items)

[DIAGRAM:two_points_graph]

[DIAGRAM:equation_from_points]

### Example 1 — Points B(−2, −2) and C(−1, −4) (Exam Q3)

**Problem:** Write the equation of the line through **B(−2, −2)** and **C(−1, −4)**.

**Solution:**
```
m = (−4 − (−2)) ÷ (−1 − (−2)) = −2 ÷ 1 = −2
y − (−2) = −2(x − (−2))
y + 2 = −2(x + 2)
y = −2x − 4 − 2 = −2x − 6
```
Check C: `−2(−1) − 6 = 2 − 6 = −4` ✓

**Answer:** **y = −2x − 6**

### Example 2 — (0, 6) and (2, 0) (Exam Q4)

**Problem:** Line through **(0, 6)** and **(2, 0)**.

**Solution:**
- Y-intercept is **6** (point on y-axis)
- `m = (0 − 6) ÷ (2 − 0) = −6 ÷ 2 = **−3**`

**Answer:** **y = −3x + 6**

### Example 3 — Point-slope with fractions (Exam Q5)

**Problem:** Line through **(4, 1/2)** and **(8, 3)**. Write the equation in slope-intercept form.

**Solution:**
```
m = (3 − 1/2) ÷ (8 − 4) = (5/2) ÷ 4 = 5/8
y − 1/2 = 5/8(x − 4)
y = 5/8 x − 5/2 + 1/2 = 5/8 x − 2
```

**Answer:** **y = 5/8 x − 2**

### Example 4 — (2, −1) and (5, −10) (Exam Q13)

**Problem:** Find the equation through **(2, −1)** and **(5, −10)**.

**Solution:**
```
m = (−10 − (−1)) ÷ (5 − 2) = −9 ÷ 3 = −3
y − (−1) = −3(x − 2)
y + 1 = −3x + 6
y = −3x + 5
```

**Answer:** **y = −3x + 5**

### Example 5 — Fill in slope 3 (Exam Q6)

**Problem:** A line through **(0, −7)** and **(2, −1)** has slope **3**. Verify.

**Solution:**
```
m = (−1 − (−7)) ÷ (2 − 0) = 6 ÷ 2 = 3 ✓
b = −7 → y = 3x − 7
```

**Answer:** **Slope = 3, equation y = 3x − 7**

### Example 6 — Best method for two points (Exam Q11)

**Problem:** Which steps write an equation from **(−3, 5)** and **(1, −3)**?

**Solution:**
1. Compute **m = (−3 − 5) ÷ (1 − (−3)) = −8 ÷ 4 = −2**
2. Use point-slope with either point
3. Simplify to **y = −2x − 1**

**Answer:** **Find slope, then use point-slope form with one of the points.**

### Exam-style practice

---

**1. Through (1, 4) and (3, 10)**

**Solution:** m = 3 → **y = 3x + 1**

---

**2. Through (−4, 0) and (0, 2)**

**Solution:** m = 1/2, b = 2 → **y = 1/2 x + 2**

---

**3. Which table matches y = −2x + 8? (Exam Q20)**

**Solution:** Pick rows with constant change **−2** in y per +1 in x, and y = 8 when x = 0.

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
Point-slope is the fastest way to write a line when slope and one point are given. Watch signs inside parentheses: `(x − 5)` means x₁ = 5; `(x + 1)` means x₁ = −1. Convert to slope-intercept for comparing lines or reading the y-intercept.

### Key Vocabulary
- **Point-slope form:** y − y₁ = m(x − x₁)
- **Convert to slope-intercept:** distribute m, add y₁ to both sides
- **Verify a point:** substitute x and y into the equation

[DIAGRAM:point_slope_convert]

[DIAGRAM:line_through_point]

### Example 1 — Convert y − 5 = 6(x + 1) (Exam Q8)

**Problem:** Rewrite **y − 5 = 6(x + 1)** in slope-intercept form.

**Solution:**
```
y − 5 = 6x + 6
y = 6x + 6 + 5
y = 6x + 11
```
Slope **6**, y-intercept **11**.

**Answer:** **y = 6x + 11**

### Example 2 — Point (−7, 2), slope 1/2 (Exam Q16)

**Problem:** Write point-slope and slope-intercept for slope **1/2** through **(−7, 2)**.

**Solution:**
```
y − 2 = 1/2(x − (−7))
y − 2 = 1/2(x + 7)
y = 1/2 x + 7/2 + 2 = 1/2 x + 11/2
```

**Answer:** **y − 2 = 1/2(x + 7)** or **y = 1/2 x + 11/2**

### Example 3 — Does (1, 6) lie on y = 4x + 2? (Exam Q9)

**Problem:** Is **(1, 6)** on the line **y = 4x + 2**?

**Solution:**
```
4(1) + 2 = 4 + 2 = 6 ✓
```

**Answer:** **Yes — (1, 6) is on the line.**

### Example 4 — Does (5, 3) lie on y = x − 2? (Exam Q14)

**Problem:** Verify **(5, 3)** on **y = x − 2**.

**Solution:**
```
5 − 2 = 3 ✓
```

**Answer:** **Yes — (5, 3) satisfies the equation.**

### Example 5 — Write point-slope from a graph (Exam Q10)

**Problem:** A line has slope **−4** and passes through **(2, 1)**. Write the equation.

**Solution:**
```
y − 1 = −4(x − 2)
y = −4x + 8 + 1 = −4x + 9
```

**Answer:** **y − 1 = −4(x − 2)** or **y = −4x + 9**

### Example 6 — Missing y on point-slope (Exam Q12)

**Problem:** Line with slope **2/3** through **(6, −4)**. Find y when x = 9.

**Solution:**
```
y − (−4) = 2/3(x − 6)
y + 4 = 2/3(3) = 2
y = −2
```

**Answer:** **y = −2** when x = 9

### Exam-style practice

---

**1. Convert y + 3 = −2(x − 1)**

**Solution:** **y = −2x − 1**

---

**2. Slope −1 through (0, 5)**

**Solution:** **y = −x + 5** (point-slope collapses because x₁ = 0)

---

**3. Which point-slope matches slope 5 through (2, −1)? (Exam Q21)**

**Solution:** **y − (−1) = 5(x − 2)** → **y + 1 = 5(x − 2)**

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
Standard form appears on exams and in word problems. Move all x-terms and constants to one side, then divide every term by the coefficient of y. Sign errors when dividing by a **negative** (like −4y) are the most common trap — Jill's mistake below.

### Key Vocabulary
- **Standard form:** Ax + By = C (A, B, C integers; A ≥ 0 often preferred)
- **Convert to slope-intercept:** y = mx + b
- **Sign error:** dividing by −4 changes signs on **both** sides

[DIAGRAM:standard_to_slope]

[DIAGRAM:jill_error_steps]

### Example 1 — 15x − 4y = −2 (Exam Q7)

**Problem:** Write **15x − 4y = −2** in slope-intercept form.

**Solution:**
```
−4y = −15x − 2
y = (−15x − 2) ÷ (−4)
y = (15/4)x + 1/2
```
Slope **15/4**, y-intercept **1/2**.

**Answer:** **y = (15/4)x + 1/2**

### Example 2 — Jill's error on practice test Q8 ⚠️ Focus

**Problem:** Jill converts **15x − 4y = −2** and gets **y = (15/4)x − 1/2**. What went wrong?

**Solution:**
- Jill likely divided by **+4** instead of **−4**, or dropped a negative on the constant.
- Correct: `−4y = −15x − 2` → divide by **−4** → **y = (15/4)x + 1/2** (not −1/2).

**Answer:** **Jill made a sign error when dividing by −4; the y-intercept should be +1/2.**

### Example 3 — 3x + 6y = 12 (Exam Q1 practice)

**Problem:** Convert **3x + 6y = 12** to slope-intercept form.

**Solution:**
```
6y = −3x + 12
y = −1/2 x + 2
```

**Answer:** **y = −1/2 x + 2**

### Example 4 — Find y-intercept from 2x − 5y = 10 (Exam Q4 practice)

**Problem:** What is the y-intercept of **2x − 5y = 10**?

**Solution:** Set x = 0:
```
−5y = 10 → y = −2
```
Y-intercept **(0, −2)** or **b = −2**.

**Answer:** **−2**

### Example 5 — Which is equivalent to y = 3x − 1? (Exam Q15 practice)

**Problem:** Pick the standard-form equation for **y = 3x − 1**.

**Solution:**
```
3x − y = 1
```
(or **−3x + y = −1** — same line, different signs)

**Answer:** **3x − y = 1**

### Example 6 — Standard form from context (Exam Q25)

**Problem:** A line has x-intercept **6** and y-intercept **3**. Write standard form.

**Solution:**
Intercept form: x/6 + y/3 = 1 → multiply by 6: **x + 2y = 6**

**Answer:** **x + 2y = 6**

### Exam-style practice

---

**1. Convert −2x + 8y = 16**

**Solution:** **y = 1/4 x + 2**

---

**2. Slope of 5x + 10y = 20**

**Solution:** **y = −1/2 x + 2** → slope **−1/2**

---

**3. Fix the error: "4x − 2y = 8 → y = 2x − 4"**

**Solution:** `−2y = −4x + 8` → **y = 2x − 4** is actually **correct**. If student wrote **y = 2x + 4**, that is the sign error.

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
Word problems give meaning to m and b. Identify what x and y represent first, then read b as the beginning amount and m as how much y changes each time x increases by 1. Negative slope means quantity decreases as x grows.

### Key Vocabulary
- **Initial value:** y-intercept; output at time 0 or start
- **Rate of change:** slope with units (e.g., dollars per day)
- **Evaluate:** plug a given x into y = mx + b
- **Interpret:** explain what m and b mean in the situation

[DIAGRAM:inez_phone_card]

[DIAGRAM:washing_machine_model]

### Example 1 — Inez's phone card (Exam Q6)

**Problem:** Inez's prepaid card starts with **$850** and loses **$50** per day of use. Model: **y = −50x + 850** (x = days, y = balance).

**Solution:**
- **Y-intercept 850:** starting balance **$850**
- **Slope −50:** balance **decreases $50 per day**

**Answer:** **Initial value $850; rate −$50 per day**

### Example 2 — Washing machine repair (Exam Q2)

**Problem:** Cost **y = 45x + 35** where x = hours of labor.

**Solution:**
- **35:** flat **$35** service fee (y-intercept)
- **45:** **$45 per hour** of labor (slope)

**Answer:** **$35 initial fee plus $45 per hour**

### Example 3 — Dog food remaining (Exam Q5)

**Problem:** **y = −15x + 430** models pounds of dog food left after x days. How much after **21 days**?

**Solution:**
```
y = −15(21) + 430 = −315 + 430 = 115
```

**Answer:** **115 pounds**

### Example 4 — Library computer time (Exam Q8 practice)

**Problem:** **y = 8x − 3** where x = weeks and y = hours of computer time available.

**Solution:**
- **Slope 8:** gain **8 hours per week**
- **Y-intercept −3:** starting adjustment (3 hours "debt" or baseline below zero at week 0 in the model)

**Answer:** **Rate +8 hours/week; initial value −3 hours in the model**

### Example 5 — Miles driven (Exam Q3 practice)

**Problem:** **y = 60x** models miles y after x hours at constant speed.

**Solution:**
- **Slope 60:** **60 miles per hour**
- **Y-intercept 0:** no miles at time 0 — proportional (no starting offset)

**Answer:** **Speed 60 mph; starting distance 0 miles**

### Example 6 — Evaluate and interpret (Exam Q18 practice)

**Problem:** A tank has **y = 120 − 6x** gallons after x minutes of draining. Find y at x = 10 and explain slope.

**Solution:**
```
y = 120 − 6(10) = 60 gallons
```
Slope **−6:** loses **6 gallons per minute**.

**Answer:** **60 gallons left; drains 6 gal/min**

### Exam-style practice

---

**1. y = 12x + 50, x = months, y = savings ($). What do 12 and 50 mean?**

**Solution:** **$50** starting savings; saves **$12 per month**.

---

**2. y = −3x + 200, find y when x = 40**

**Solution:** **y = −120 + 200 = 80**

---

**3. Which slope means "cost goes down each week"? (Exam Q23)**

**Solution:** The **negative** slope (e.g. **−15** in the dog-food model).

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
Exam items pit an equation against a graph, table, or another equation. Put both in slope-intercept form, then compare m and b. For "which is steeper," compare absolute values of slope. For "same y-intercept," match b only.

### Key Vocabulary
- **Steeper:** larger |slope|
- **Same y-intercept:** same b, graphs cross y-axis at same point
- **Equivalent equations:** same m and b after simplification
- **x-intercept:** set y = 0; use slope to build equation from intercept + slope

[DIAGRAM:compare_two_lines]

[DIAGRAM:same_y_intercept]

### Example 1 — Compare y = −10x + 6 vs y − 36 = 8(x − 4) (Exam Q7)

**Problem:** Which line is steeper?

**Solution:**
- Line 1: **y = −10x + 6** → m = **−10**
- Line 2: `y − 36 = 8(x − 4)` → `y = 8x − 32 + 36 = **8x + 4**` → m = **8**
- |−10| = 10 and |8| = 8 → **y = −10x + 6 is steeper**

**Answer:** **y = −10x + 6** (|m| = 10 > 8)

### Example 2 — Jeremy's steepness claim (Exam Q3)

**Problem:** Jeremy says a line with slope **−5** is steeper than a line with slope **3**. Is he correct?

**Solution:**
- Steepness uses **|m|**: |−5| = **5** > |3| = **3**
- Jeremy is **correct** — ignore the negative sign for steepness only.

**Answer:** **Yes — |−5| > |3|**

### Example 3 — y = 2x + 2 vs graph (Exam Q17)

**Problem:** Does a graph show the same line as **y = 2x + 2**?

**Solution:**
- Read graph slope (rise/run) and y-intercept at `(0, b)`
- Match **m = 2** and **b = 2**
- Check a second point on the graph satisfies y = 2x + 2

**Answer:** **Same line if graph has slope 2 and y-intercept 2**

### Example 4 — y = 4x + 5 vs table (Exam Q24)

**Problem:** Which table represents **y = 4x + 5**?

**Solution:**
- At x = 0, y = **5**
- Each +1 in x adds **4** to y
- Pick table with constant difference **4** and first row (0, 5) or equivalent

**Answer:** Table with **y-intercept 5** and slope **4**

### Example 5 — x-intercept 12, slope 3/8 vs table (Exam Q23)

**Problem:** Line has **x-intercept 12** and slope **3/8**. Which table matches?

**Solution:**
- Point **(12, 0)** on line
- `y = 3/8(x − 12)` → y-intercept: `y = 3/8(−12) = **−9/2**`
- Equation: **y = 3/8 x − 9/2**
- Check table rows satisfy this equation

**Answer:** Table consistent with **m = 3/8** and point **(12, 0)**

### Example 6 — Same y-intercept (Exam Q19)

**Problem:** Which equation has the **same y-intercept** as **y = −2x + 7** but a different slope?

**Solution:**
- Same b = **7**: forms like **y = 3x + 7** or **y = 1/2 x + 7**
- Different slope means different m, same **+7** constant

**Answer:** Any **y = mx + 7** with m ≠ −2

### Exam-style practice

---

**1. Are y = 5x − 1 and 10x − 2y = 2 the same line?**

**Solution:** `10x − 2y = 2` → **y = 5x − 1** → **yes, equivalent**

---

**2. Which is steeper: y = x + 1 or y = −3x + 1?**

**Solution:** |−3| = 3 > |1| → **y = −3x + 1**

---

**3. Table A: (0, 4), (1, 7), (2, 10). Match equation? (Exam Q22 practice)**

**Solution:** Slope 3, b = 4 → **y = 3x + 4**

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
