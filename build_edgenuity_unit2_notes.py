#!/usr/bin/env python3
"""One-time builder: writes Edgenuity Unit 2 activity markdown notes. Run: python build_edgenuity_unit2_notes.py"""

from pathlib import Path

NOTES = Path(__file__).parent / "ArjunEdgenuityCourse3" / "notes" / "unit_2"
NOTES.mkdir(parents=True, exist_ok=True)

ACTIVITIES = {
    "activity_1_slope_rate.md": '''# Activity 1: Slope & Rate of Change

[KEY]
**Slope** = rate of change = **rise ÷ run** = `(y₂ − y₁) ÷ (x₂ − x₁)`.  
In word problems, slope is the **constant rate** (miles per minute, gallons per second, dollars per hour).
[/KEY]

## Quick Review Notes

### Main Idea
Slope tells how fast y changes as x increases. Find it from two points, a graph, or a table. Compare slopes to see who goes faster or which line is steeper.

### Key Vocabulary
- **Slope (m):** change in y ÷ change in x
- **Rate of change:** slope in a real-world context
- **Positive slope:** y increases as x increases
- **Negative slope:** y decreases as x increases
- **Direct variation:** proportional; slope = k and line passes through `(0, 0)`

[DIAGRAM:slope_rise_run]

[DIAGRAM:wilson_watering]

### Example 1 — Wilson's watering can (Exam Q1)

**Problem:** Wilson's full watering can loses water over time. The graph shows `(0, 2.5)` and `(4, 1.7)`. Which statement is correct?

**Solution:**
- **Initial amount (y-intercept):** at time 0, **2.5 gallons** in the can.
- **Rate:** `(1.7 − 2.5) ÷ (4 − 0) = −0.8 ÷ 4 = **−0.2 gallons per second** (water leaving).

**Answer:** **The amount of water originally in Wilson's can was 2.5 gallons.**

### Example 2 — Baseball distance vs swing speed (Exam Q6)

**Problem:** Distance (feet) varies **directly** with swing speed (mph). The graph is proportional through the origin. At 50 mph the ball travels 250 feet. What is the relationship?

**Solution:** `250 ÷ 50 = 5` → **distance = 5 × speed**.

**Answer:** **The distance is 5 times the swing speed.**

### Example 3 — Slope from a table (Exam Q38)

**Problem:** A table has `(0, 5)` and `(4, 9)`. Which expression gives the slope?

**Solution:** `(9 − 5) ÷ (4 − 0) = **4/4 = 1**` → use `(9 − 5) ÷ (4 − 0)`.

**Answer:** **(9 − 5) ÷ (4 − 0)**

### Example 4 — Andrew vs Karleigh treadmill (Exam Q7)

**Problem:**

| Andrew | | Karleigh | |
|--------|---|----------|---|
| Minutes | Miles | Minutes | Miles |
| 18 | 1.5 | 30 | 3 |
| 24 | 2 | 40 | 4 |

Who ran farther in **60 minutes**?

**Solution:**
- Andrew: `(2 − 1.5) ÷ (24 − 18) = **1/12**` mile per minute → 60 × 1/12 = **5 miles**
- Karleigh: `(4 − 3) ÷ (40 − 30) = **1/10**` mile per minute → 60 × 1/10 = **6 miles**

**Answer:** **Karleigh ran a greater distance** (1/10 mi/min vs 1/12 mi/min).

### Example 5 — Table with slope 2 (Exam Q4)

**Problem:** Which table describes a line with slope **2**?

**Solution:** Pick two rows; slope = `(y₂ − y₁) ÷ (x₂ − x₁)`.  
Table 3: `(−4, 4)` to `(−2, 8)` → `(8 − 4) ÷ (−2 − (−4)) = 4/2 = **2**`.

**Answer:** **Table 3**

### Exam-style practice

---

**1. Ladder against a wall (Exam Q37)**

Bottom of ladder is 4 ft from wall; top is 20 ft high. Slope (rise/run)?

**Solution:** `20 ÷ 4 = **5**`.

---

**2. Constant y in a table (Exam Q35)**

| x | −8 | −4 | 0 | 4 | 8 |
|---|---|---|---|---|---|
| y | 8 | 8 | 8 | 8 | 8 |

**Solution:** y never changes → **slope is zero**.

### Common Mistakes
- Confusing **initial value** (y-intercept) with **rate** (slope).
- Mixing up **run** and **rise** — always `(y₂ − y₁) ÷ (x₂ − x₁)`.
- Forgetting units: Wilson's rate is **0.2 gal/sec**, not 2.5.

### Mini Summary
- Slope = **rise ÷ run** = rate of change.
- Compare rates by comparing slopes.
- Direct variation: line through **(0, 0)** with constant ratio y/x.
''',

    "activity_2_y_intercept.md": '''# Activity 2: Y-Intercept & Initial Value

[KEY]
The **y-intercept** is where the line crosses the y-axis (**x = 0**). In word problems it is the **initial value** — the starting amount before any change happens.
[/KEY]

## Quick Review Notes

### Main Idea
Every line in slope-intercept form `y = mx + b` has y-intercept **b**. Read it from a graph at `(0, b)`, from an equation when x = 0, or by working **backward** from a table using the rate.

### Key Vocabulary
- **Y-intercept:** value of y when x = 0; point `(0, b)`
- **Initial value:** starting output in a real-world model
- **Output for initial value:** the y-value at the start (time 0, before pumping, at opening)

[DIAGRAM:y_intercept_line]

[DIAGRAM:initial_value_table]

### Example 1 — Maricella's line (Exam Q3)

**Problem:** Maricella plots `(4, 9)` and `(6, 4)` and extends the segment. Where is the y-intercept?

**Solution:** Slope = `(4 − 9) ÷ (6 − 4) = −5/2`. From `(4, 9)`: down 5 in y for every 2 in x.  
At x = 0: start at `(0, **6**)`.

**Answer:** **(0, 6)**

### Example 2 — Tip jar at dry cleaners (Exam Q33)

**Problem:** Hours since opening vs money in tip jar:

| Hours | 4 | 5 | 6 | 7 | 8 |
|-------|---|---|---|---|---|
| $ | 15.50 | 18.25 | 21.00 | 23.75 | 26.50 |

How much was in the jar when the cleaners **opened** (hour 0)?

**Solution:** Rate = `18.25 − 15.50 = **2.75**` per hour.  
Backtrack 4 hours: `15.50 − 4(2.75) = 15.50 − 11.00 = **4.50**`.

**Answer:** **$4.50**

### Example 3 — Marco pumping gas (Exam Q36)

**Problem:** Table shows gallons in Marco's car vs seconds spent pumping. What is the **output for the initial value**?

**Solution:** Before pumping starts (0 seconds), the tank has **0 gallons** added in this session — the initial output is **0 gallons** at the pump start.

**Answer:** **0 gallons**

### Example 4 — Nate's road trip (Exam Q12) ⚠️ Focus

**Problem:** Nate records time and distance. The function is linear with rate **50 miles per hour**. How can he find the **initial value** (starting distance)?

**Solution:** Pick any row, then **repeatedly subtract 50** for each hour worked backward to time 0.

**Answer:** **By repeatedly subtracting 50.**

### Example 5 — Y-intercept from a graph (Exam Q22)

**Problem:** A line crosses the y-axis at `(0, 4)`.

**Solution:** Read the point where the line hits the y-axis.

**Answer:** **(0, 4)**

### Example 6 — Student graphs with y-intercept −4 (Exam Q24)

**Problem:** Four students graph lines. Which graph crosses the y-axis at **−4**?

**Solution:** Find the graph whose line passes through `(0, −4)`.

**Answer:** **Ellis**

### Exam-style practice

---

**1. Graph y-intercept and slope (Exam Q5)**

A line has y-intercept **3** and rises 1 unit for every 2 units right.

**Answer:** **y-intercept is 3; slope is 1/2**

---

**2. Line on grid (Exam Q39)**

Graph shows slope **m = 2** and crosses y-axis at `(0, 4)`.

**Answer:** **m = 2, y-intercept (0, 4)**

### Common Mistakes
- Using **x-intercept** `(4, 0)` when the question asks for **y-intercept**.
- Adding the rate instead of **subtracting** when working backward (Nate's trip).
- Confusing **initial gallons in tank** with **gallons pumped** (Marco).

### Mini Summary
- Y-intercept = **starting value** at x = 0.
- From a table: find rate, then step **backward** to x = 0.
- In `y = mx + b`, **b** is the y-intercept.
''',

    "activity_3_direct_variation.md": '''# Activity 3: Direct Variation & Proportional Relationships

[KEY]
**Direct variation** (proportional): `y = kx` — graph passes through **(0, 0)** and `y/x` is always the same constant.  
If the y-intercept is **not 0**, it is linear but **not** proportional.
[/KEY]

## Quick Review Notes

### Main Idea
Proportional relationships have no starting fee: double the input, double the output. Check `(0, 0)` on the graph and equal ratios in tables. A line with a y-intercept breaks direct variation.

### Key Vocabulary
- **Direct variation:** y varies directly with x; `y = kx`
- **Constant of variation:** k = y/x
- **Proportional relationship:** passes through origin; ratios y/x are equal
- **Not proportional:** y = mx + b with **b ≠ 0**

[DIAGRAM:direct_vs_not]

[DIAGRAM:proportional_graph]

### Example 1 — Why Li is incorrect (Exam Q2)

**Problem:** Li says a graph shows direct variation, but at x = 0 the y-value is **1**. Why is Li wrong?

**Solution:** Direct variation requires the graph to pass through **(0, 0)**. Here y = 1 when x = 0.

**Answer:** **When the x-value is 0, the y-value is 1.**

### Example 2 — Which table is direct variation? (Exam Q32)

**Problem:** Pick the table where y/x is constant and the line would pass through the origin.

**Solution:** Table B: x = 4, 6, 8, 10 → y = 12, 18, 24, 30.  
Check: `12/4 = 18/6 = 24/8 = 30/10 = **3**` → **y = 3x**.

**Answer:** **Table B**

### Example 3 — Which graph is proportional? (Exam Q31)

**Problem:** Which representation shows a proportional relationship?

**Solution:** A **straight line through (0, 0)** or an equation like **y = 2x** (no + constant).  
Reject **y = 2x + 2** — the +2 means not through the origin.

**Answer:** The graph/table with **y = kx** only (through the origin).

### Example 4 — Caleb's earnings (Exam Q30) ⚠️ Focus

**Problem:**

| Hours | 12 | 15 | 18 | 21 |
|-------|----|----|----|----|
| Earnings ($) | 140 | 170 | 200 | 230 |

Does this represent direct variation?

**Solution:** Check `140/12 ≈ 11.67`, `170/15 ≈ 11.33` — ratios differ.  
Pattern: **earnings = 10 × hours + 20** (base pay $20). The +20 breaks proportionality.

**Answer:** **The ratios of earnings to hours are not the same each week, so the earnings do not vary directly with the hours.**

### Example 5 — Baseball (direct variation context) (Exam Q6)

**Problem:** Distance varies directly with swing speed; graph through origin.

**Solution:** Find k = distance ÷ speed from any point. `k = 5` → **distance = 5 × speed**.

**Answer:** **Distance is 5 times the swing speed.**

### Exam-style practice

---

**1. Is y = 4x + 7 proportional?**

**Solution:** No — when x = 0, y = 7 ≠ 0.

---

**2. Table check**

| x | 2 | 4 | 6 |
|---|---|---|---|
| y | 5 | 10 | 15 |

**Solution:** y/x = 2.5 always, but at x = 0 y would be 0 only if extended from origin — table alone shows constant ratio **y = 2.5x** (proportional).

### Common Mistakes
- Thinking a **constant rate of change** alone means direct variation (need **b = 0**).
- Caleb trap: **y = 10x + 20** is linear but **not** proportional because of the $20 base.
- Saying "proportional" when the graph misses the origin.

### Mini Summary
- Direct variation: **y = kx**, through **(0, 0)**, equal ratios y/x.
- **y = mx + b** with b ≠ 0 → linear, not proportional.
- Always check the origin and ratio equality.
''',

    "activity_4_special_lines.md": '''# Activity 4: Special Lines — Zero & Undefined Slope

[KEY]
**Horizontal line:** y = k → **slope 0** (y does not change).  
**Vertical line:** x = k → **undefined slope** (x does not change; not a function of x).
[/KEY]

## Quick Review Notes

### Main Idea
Some lines are special. A flat horizontal line has slope zero. A vertical line has no defined slope. Know the difference for equations, graphs, and true/false statements.

### Key Vocabulary
- **Zero slope:** horizontal line; y = constant
- **Undefined slope:** vertical line; x = constant
- **Positive slope:** rises left to right
- **Negative slope:** falls left to right

[DIAGRAM:horizontal_vertical]

[DIAGRAM:zero_undefined_slope]

### Example 1 — Sanjay's claim (Exam Q9)

**Problem:** Sanjay says a line with **slope zero** never touches the x-axis. Which line proves him wrong?

**Solution:** **y = 0** is the x-axis itself — horizontal, slope 0, and it **lies on** the x-axis.

**Answer:** **y = 0**

### Example 2 — Line through (9, 30) and (18, 30) (Exam Q10)

**Problem:** What is true about this line?

**Solution:** y stays **30** while x changes → **horizontal** → **slope = 0** because change in y is 0.

**Answer:** **It has a slope of zero because the change in the y-values is 0.**

### Example 3 — Which equation has slope zero? (Exam Q14)

**Problem:** Pick the horizontal line.

**Solution:** **y = 2** (or any y = constant). Reject `y = −½x + ½` (nonzero slope) and `x = −5` (vertical).

**Answer:** **y = 2** (constant y)

### Example 4 — Undefined slope (Exam Q28)

**Problem:** Which equation represents a line with **undefined** slope?

**Solution:** Vertical lines: **x = 0**, **x = 1**, etc. Not `y = 0` (that is slope 0).

**Answer:** **x = 0**

### Example 5 — Which graph line is vertical? (Exam Q29)

**Problem:** On a graph with lines P, Q, R, S — which has undefined slope?

**Solution:** The **vertical** line (runs up-down, same x everywhere).

**Answer:** The **vertical** line on the graph.

### Example 6 — True statements about slope (Exam Q34)

**Problem:** Which statement is correct?

**Solution:**
- Vertical line → **undefined** slope, not zero.
- Horizontal → slope **0**, not "no slope."
- Rising left to right → **positive** slope ✓

**Answer:** **A line that rises from left to right has a positive slope.**

### Exam-style practice

---

**1. Slope of y = −3**

**Answer:** **0** (horizontal)

---

**2. Slope of x = 7**

**Answer:** **Undefined** (vertical)

### Common Mistakes
- Saying vertical lines have **slope 0** — they have **no slope** (undefined).
- Saying horizontal lines have **no slope** — their slope is **0**.
- Confusing **y = 0** (horizontal, slope 0) with **x = 0** (vertical, undefined).

### Mini Summary
- **Horizontal** y = k → slope **0**.
- **Vertical** x = k → slope **undefined**.
- Sanjay is wrong: **y = 0** touches the x-axis everywhere.
''',

    "activity_5_writing_equations.md": '''# Activity 5: Writing Equations of Lines

[KEY]
**Slope-intercept:** `y = mx + b`  
**Point-slope:** `y − y₁ = m(x − x₁)`  
Use slope from two points or a graph, then solve for **b** with any point.
[/KEY]

## Quick Review Notes

### Main Idea
Build equations from slope and a point, from two points, or from a graph. Convert to slope-intercept when needed and use the equation to find missing coordinates.

### Key Vocabulary
- **Slope-intercept form:** y = mx + b
- **Point-slope form:** y − y₁ = m(x − x₁)
- **Standard form:** Ax + By = C (common in word problems)

[DIAGRAM:equation_from_graph]

[DIAGRAM:point_on_line]

### Example 1 — Slope −3/4 through (−5, 4) (Exam Q13) ⚠️ Focus

**Problem:** Line has slope **−3/4** and passes through **(−5, 4)**. Find the equation.

**Solution:**
```
y − 4 = −3/4(x + 5)
y = −3/4 x − 15/4 + 16/4
y = −3/4 x + 1/4
```
Check: at x = −5 → y = 15/4 + 1/4 = 4 ✓

**Answer:** **y = −3/4 x + 1/4** (use point-slope; watch distractors like y = −3/4 x − 2)

### Example 2 — Find a on the line (Exam Q15)

**Problem:** Line through **(2, −2)** and **(−6, 2)**. Point **(a, −4)** is on the line. Find **a**.

**Solution:**
- Slope: `(2 − (−2)) ÷ (−6 − 2) = 4 ÷ (−8) = **−1/2**`
- Using (2, −2): `y + 2 = −1/2(x − 2)`
- At y = −4: `−2 = −1/2(x − 2)` → `x − 2 = 4` → **a = 6**

**Answer:** **a = 6**

### Example 3 — Y-intercept from standard form (Exam Q25)

**Problem:** What is the y-intercept of **x − 4y = −6**?

**Solution:** Set x = 0: `−4y = −6` → `y = **3/2**` → point **(0, 3/2)**.

**Answer:** **3/2** (or (0, 3/2))

### Example 4 — Slope from graph points (Exam Q27)

**Problem:** Line passes through **(0, 2)** and **(−4, 0)** on a graph. Slope?

**Solution:** `(0 − 2) ÷ (−4 − 0) = −2 ÷ (−4) = **1/2**`.

**Answer:** Use **(0 − 2) ÷ (−4 − 0)** or equivalent.

### Example 5 — Ava's slope expression (Exam Q34)

**Problem:** Ava uses `(3 − 1) ÷ (4 − (−2))` for slope. Which table fits?

**Solution:** Slope = `2/6 = 1/3`. Pick the table with constant rate **1/3** (y increases 1 when x increases 3).

**Answer:** The table whose rows match slope **1/3**.

### Exam-style practice

---

**1. Write y = mx + b through (0, −2) and (4, 2)**

**Solution:** m = 1, b = −2 → **y = x − 2**

---

**2. Horizontal through (9, 30)**

**Answer:** **y = 30**

### Common Mistakes
- Plugging x into **b** and y into **m** when solving for b — use `b = y − mx`.
- Sign errors with **−3/4** and negative x-coordinates.
- Using **x = −5** when asked for an equation with a numeric **slope** (that is vertical).

### Mini Summary
- Two points → slope → point-slope → **y = mx + b**.
- To find a missing x or y, **substitute** into your equation.
- Standard form: set **x = 0** for y-intercept, **y = 0** for x-intercept.
''',

    "activity_6_linear_modeling.md": '''# Activity 6: Linear Modeling & Word Problems

[KEY]
Translate words into **Ax + By = C** or **y = mx + b**. Define variables clearly, use coefficients as unit prices/rates, and solve for the quantity asked.
[/KEY]

## Quick Review Notes

### Main Idea
Real situations (food sales, phone bills, revenue) become linear equations. Match each variable to a quantity, each coefficient to a price or rate, and the constant to a total.

### Key Vocabulary
- **Standard form model:** Ax + By = C (A, B = rates; C = total)
- **Revenue:** (price) × (quantity) summed
- **Hourly rate:** slope on a bill-vs-hours graph
- **Initial fee + per-unit cost:** y = mx + b

[DIAGRAM:shake_shack_model]

[DIAGRAM:brenda_phone_bill]

### Example 1 — Shake Shack shakes (Exam Q8)

**Problem:** Small shake **$3**, large shake **$5**. Sunday revenue **$479**.  
x = number of **small** shakes, y = number of **large** shakes. Write the equation.

**Solution:** `3x + 5y = 479`

**Answer:** **3x + 5y = 479**

### Example 2 — Pretzels and popcorn (Exam Q11)

**Problem:** Which story matches **2.75x + 3.25y = 215**?

**Solution:** x items at **$2.75**, y items at **$3.25**, total **$215**.  
Pretzels cost **75¢ more** than popcorn → popcorn **$2.75**, pretzels **$3.25**.

**Answer:** **Pretzels cost 75 cents more than popcorn bags. x = popcorn bags, y = pretzels. Total $215.**

### Example 3 — Brenda's cell phone bill (Exam Q20)

**Problem:** Graph shows Brenda's monthly bill vs hours used. What is her **hourly rate**?

**Solution:** Find slope (rise ÷ run) between two clear points on the line — change in **dollars** per **hour**.

**Answer:** Read the **slope** from the graph (e.g. **$12 per hour** if the line rises $12 for each 1 hour).

### Example 4 — Caleb's pay (linear but not proportional) (Exam Q30)

**Problem:** Earnings = **10 × hours + 20**. Is this direct variation?

**Solution:** The **$20 base** makes it **y = mx + b** with b ≠ 0 — linear model, not proportional.

**Answer:** **Not direct variation** because of the added $20.

### Example 5 — Tip jar rate (Exam Q33)

**Problem:** Tips grow **$2.75 per hour** after opening. At hour 4 there is **$15.50**. Starting amount?

**Solution:** `15.50 − 4(2.75) = **$4.50**` at hour 0.

**Answer:** **$4.50** in the jar at opening.

### Exam-style practice

---

**1. T-shirts $8, hats $12, total sales $200**

**Equation:** **8x + 12y = 200**

---

**2. Plan: $25 monthly fee + $0.15 per text**

**Equation:** **y = 0.15x + 25** (x texts, y total cost)

### Common Mistakes
- Shake Shack trap: swapping **3 and 5** or using **5x + 3y** when x is defined as **small**.
- Pretzels/popcorn: matching **2.75 to pretzels** when it is the **lower** price (popcorn).
- Brenda: reading the **y-intercept** (base fee) when the question asks for **hourly rate** (slope).

### Mini Summary
- Define variables first; match coefficients to prices/rates.
- Total revenue → **(price₁)(qty₁) + (price₂)(qty₂) = total**.
- Graph models: **slope = rate**, **y-intercept = starting fee**.
''',

    "unit_2_linear_functions_lesson_notes.md": '''# Unit 2: Linear Functions — Overview

| Activity | Topic | Key idea |
|----------|-------|----------|
| **1** | Slope & Rate of Change | Rise ÷ run; Wilson watering can; Andrew vs Karleigh |
| **2** | Y-Intercept & Initial Value | Starting value at x = 0; tip jar; Marco gas; Nate trip |
| **3** | Direct Variation | y = kx through origin; Li's error; Caleb earnings |
| **4** | Special Lines | Horizontal (slope 0) vs vertical (undefined); Sanjay |
| **5** | Writing Equations | Point-slope, slope-intercept; find point on line |
| **6** | Linear Modeling | Shake Shack, pretzels/popcorn, Brenda phone bill |

**Exam focus areas (39-question practice test):** Direct variation vs linear with intercept (Q2, Q30), undefined vs zero slope (Q9–Q10, Q28–Q34), writing equations from points (Q13, Q15), initial value backward from tables (Q12, Q33).

**Weak areas to review:** Point-slope with fractional slope (Q13), Caleb proportional trap (Q30), Sanjay horizontal-line reasoning (Q9), standard-form word problems (Q8, Q11).

Open each activity for full notes, diagrams, and worked exam-style problems. Use **Daily Practice** for quiz sets with graphs.
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
