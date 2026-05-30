#!/usr/bin/env python3
"""Writes Unit 4 activity markdown notes. Run: python build_unit4_notes.py"""

from pathlib import Path

NOTES = Path(__file__).parent / "ArjunCourse3" / "notes" / "unit_4"
NOTES.mkdir(parents=True, exist_ok=True)

ACTIVITIES = {
    "activity_27_introduction_to_functions.md": '''# Activity 27: Introduction to Functions

[KEY]
A **function** is a relation where each **input** (x) has exactly **one output** (y).  
**Domain** = all allowed inputs; **range** = all possible outputs. Evaluate with substitution: plug in x, compute y.
[/KEY]

## Quick Review Notes

### Main Idea
A relation is a set of ordered pairs. It is a **function** only if no input value is paired with two different outputs. You can check tables, mappings, and graphs.

### Key Vocabulary
- **Relation:** Any set of ordered pairs (x, y).
- **Function:** Each x-value maps to exactly one y-value.
- **Domain:** All possible input values (x).
- **Range:** All possible output values (y).
- **Ordered pair:** Written (x, y); x is input, y is output.
- **Discrete data:** Separate, counted values (often whole numbers).
- **Continuous data:** Values that can be any number in an interval.

### Important Rules

| Check | Function? |
|-------|-----------|
| Table: same x with two different y | **Not** a function |
| Mapping: one arrow from each x | **Function** |
| Equation: one y for each x | Usually a function |

**Evaluate:** For `y = 2x + 4` and `x = 3`, substitute: `y = 2(3) + 4 = 10`.

[DIAGRAM:function_mapping]

[DIAGRAM:domain_range]

### Example 1 — Evaluate

**Problem:** `y = 2x + 4` for `x = 3`.

**Solution:** `y = 2(3) + 4 = 10`

**Answer:** **10**

### Example 2 — Is it a function?

**Problem:** `{(-2, 2), (-3, 4), (-2, 6)}`

**Solution:** x = −2 appears with y = 2 and y = 6 → **not a function**

**Answer:** **Not a function**

### Textbook practice (from the PDF)

*Activity 27 Practice, Lessons 27-1 through 27-3.*

---

**1. Activity 27 Practice #1**

**Problem:** `y = 2x + 4` for x = 3, 4, and 0.25.

**Solution:**
- x = 3: `y = 10`
- x = 4: `y = 12`
- x = 0.25: `y = 2(0.25) + 4 = 4.5`

**Answer:** **10, 12, 4.5**

---

**2. Activity 27 Practice #2**

**Problem:** `y = −6x + 2` for x = 5, −1/2, and −7.

**Solution:**
- x = 5: `y = −28`
- x = −1/2: `y = 5`
- x = −7: `y = 44`

**Answer:** **−28, 5, 44**

---

**3. Activity 27 Practice #3**

**Problem:** `y = 7 + (x − 9)` for x = 8, −1, 10.

**Solution:** Simplify: `y = x − 2` → **6, −3, 8**

**Answer:** **6, −3, 8**

---

**4. Activity 27 Practice #6**

**Problem:** Is `{(-2, 2), (-3, 4), (-4, 5), (-2, 6), (-3, 7)}` a function?

**Solution:** −2 has two outputs; −3 has two outputs → **not a function**

**Answer:** **Not a function**

---

**5. Activity 27 Practice #9**

**Problem:** Table x: 5,6,7,8 and y: 3,4,5,6 — function?

**Solution:** Each x has exactly one y → **yes**

**Answer:** **Yes — it is a function**

---

**6. Activity 27 Practice #12 — domain and range**

**Problem:** `{(-1, 7), (-2, 4), (-2, −3), (6, −3)}`

**Solution:** Domain: **{−1, −2, 6}**; Range: **{7, 4, −3}** (not a function because −2 has two y-values)

**Answer:** Domain **{−1, −2, 6}**; Range **{7, 4, −3}**; **not a function**

### Common Mistakes
- Confusing **domain** (x) with **range** (y).
- Thinking every relation is a function.
- Order of operations errors when **evaluating**.

### Mini Summary
- Function: **one output per input**.
- **Domain** = inputs; **range** = outputs.
''',

    "activity_28_comparing_functions.md": '''# Activity 28: Comparing Functions

[KEY]
Compare functions as **tables, graphs, and equations**. **Slope** is the **rate of change** (how fast y changes per unit of x). **y = mx + b**: m = rate, b = starting value.
[/KEY]

## Quick Review Notes

### Main Idea
Real situations (walkways, pay, motion) can be modeled with linear equations. Match the story to the graph and equation by finding slope and intercept.

### Key Vocabulary
- **Rate of change:** Slope; change in y per change in x.
- **Directly proportional:** Through origin; equation `y = kx` (b = 0).
- **Linear function:** Graph is a straight line; `y = mx + b`.

### Important Rules

`slope = (y₂ − y₁) / (x₂ − x₁)` = rate of change

| Form | Meaning |
|------|---------|
| `y = 4x` | slope 4, starts at 0 |
| `y = 4x + 1` | slope 4, starts at 1 |
| `y = 2x + 2` | slope 2, starts at 2 |

[DIAGRAM:comparing_graphs]

[DIAGRAM:rate_of_change]

### Example 1 — Kaneesha's pay

**Problem:** $75 per week plus $8 per hour. Rate of change and base pay?

**Solution:** Rate = **$8/hour**; base = **$75**; equation **`y = 8x + 75`**

**Answer:** Slope **8**; intercept **75**

### Example 2 — Speed

**Problem:** `y = −5x − 1` describes position vs time. Speed?

**Solution:** Slope = **−5** units per minute (moving backward/down)

**Answer:** Speed **5** (rate of change **−5**)

### Textbook practice (from the PDF)

*Activity 28 Practice.*

---

**1. Activity 28 Practice #5–6 — pay**

**Problem:** $75/week + $8/hour. Rate and equation?

**Solution:** Rate **$8/hr**; **`y = 8x + 75`** (choice B)

**Answer:** Rate **8**; equation **`y = 8x + 75`**

---

**2. Activity 28 Practice #1 — separate tiles**

**Problem:** Square tiles, no edges touching. Perimeter vs number of tiles?

**Solution:** Each tile adds 4 to perimeter → **`y = 4x`**

**Answer:** **`y = 4x`**

---

**3. Activity 28 Practice #3 — touching tiles**

**Problem:** Tiles share edges; perimeter not counting shared sides.

**Solution:** Pattern gives **`y = 2x + 2`**

**Answer:** **`y = 2x + 2`**

---

**4. Activity 28 Practice #4a**

**Problem:** `y = −5x − 1` — speed and starting position?

**Solution:** Slope **−5** = speed; y-intercept **−1** = start position

**Answer:** Speed **5** (rate −5); starts at **−1**

---

**5. Activity 28 Practice #7 — directly proportional**

**Problem:** Which functions in Item 4 are directly proportional?

**Solution:** Only **`y = kx`** forms (b = 0) — e.g. `y = 4x`, not `y = 4x + 1`

**Answer:** Equations with **no** constant term (through origin)

---

**6. Activity 28 Practice #8**

**Problem:** 0.5 miles per minute from start. Which function?

**Solution:** **`y = 0.5x`** (distance = rate × time)

**Answer:** **`y = 0.5x`** (linear through origin)

### Common Mistakes
- Mixing up **slope** and **y-intercept** in word problems.
- Using **`y = 8x − 75`** instead of **`+ 75`** for base pay added.
- Matching wrong equation to tile pattern.

### Mini Summary
- **Slope** = rate of change; **b** = starting amount.
- Compare graphs by **steepness** (m) and **where they cross the y-axis** (b).
''',

    "activity_29_constructing_functions.md": '''# Activity 29: Constructing Functions

[KEY]
Build a function from a pattern: make a **table**, sketch a **graph**, write **`y = mx + b`**.  
Constant growth → **linear**; compare plants with different **starting heights** and **rates**.
[/KEY]

## Quick Review Notes

### Main Idea
When something grows by the same amount each step, the relationship is linear. Use the first value and the rate to write `y = mx + b` or `y = b + mx`.

### Key Vocabulary
- **Initial value:** Starting amount (y-intercept when x = 0).
- **Constant rate:** Same change per unit (slope).
- **Directly proportional:** Starts at 0; `y = kx`.

### Pattern → Equation

| Situation | Equation |
|-----------|----------|
| Plant: 0 mm at day 0, +12 mm/day | `h = 12d` |
| Plant: 20 mm at day 0, +6 mm/day | `h = 20 + 6d` |
| Square train perimeter | `P = 4n` |

[DIAGRAM:plant_growth]

[DIAGRAM:pattern_perimeter]

### Example 1 — Plant A

**Problem:** Grows 12 mm per day from 0 mm.

**Solution:** Table: 0→0, 1→12, …; **`h = 12d`**; day 80: `12(80) = 960` mm

**Answer:** **`h = 12d`**; day 80: **960 mm**

### Example 2 — Plant B

**Problem:** Starts 20 mm, grows 6 mm/day.

**Solution:** **`h = 20 + 6d`**; day 80: `20 + 480 = 500` mm

**Answer:** **`h = 20 + 6d`**; day 80: **500 mm**

### Textbook practice (from the PDF)

*Activity 29 Practice.*

---

**1. Activity 29 Practice #1–4 — 12 mm/day plant**

**Problem:** Table for 8 days; function; height on day 80.

**Solution:** Heights 0, 12, 24, …, 84; **`h = 12d`**; day 80: **960 mm**

**Answer:** **`h = 12d`**; **960 mm** on day 80

---

**2. Activity 29 Practice #5–8 — 20 mm start, 6 mm/day**

**Problem:** Table, graph, function, day 80.

**Solution:** 20, 26, 32, …; **`h = 20 + 6d`**; day 80: **500 mm**

**Answer:** **`h = 20 + 6d`**; **500 mm**

---

**3. Activity 29 Practice #9**

**Problem:** Which function is directly proportional?

**Solution:** **`h = 12d`** starts at 0; **`h = 20 + 6d`** does not → only **12d** is directly proportional

**Answer:** **`h = 12d`** (through origin)

---

**4. Activity 29 Practice #10 — square train**

**Problem:** Perimeter of square pattern blocks, side 1 unit.

**Solution:** 1 square → P=4; 2 → 8; pattern **`P = 4n`**

**Answer:** **`P = 4n`**

---

**5. Activity 29 Practice #11 — triangles**

**Problem:** Triangle train perimeter pattern.

**Solution:** Find table values; often linear with slope **2** or similar from pattern — write **`P = 2n + 2`** or book-specific rule from your sketch.

**Answer:** Linear equation from table (check pattern in textbook)

---

**6. Activity 29 Practice #12 — hexagons**

**Problem:** Hexagon train perimeter.

**Solution:** Complete table from pattern blocks; write linear **`P = mn + b`** from rate between figures

**Answer:** Equation from your table (linear)

### Common Mistakes
- Using **x** for days in one problem and **n** for figures in another — label variables clearly.
- Forgetting **starting value** in `y = mx + b`.
- Plotting **discrete** points without connecting only when appropriate.

### Mini Summary
- **Construct:** table → graph → **`y = mx + b`**.
- **Directly proportional** only when the graph passes through **(0, 0)**.
''',

    "activity_30_linear_functions.md": '''# Activity 30: Linear Functions

[KEY]
A **linear function** has a **constant rate of change** — its graph is a **straight line**.  
Identify linear data in tables by equal **slopes** between points; non-linear data curves or has changing rates.
[/KEY]

## Quick Review Notes

### Main Idea
Linear relationships change by the same amount for each equal step in x. The rate of change (slope) is the same everywhere on the line.

### Key Vocabulary
- **Linear function:** Constant rate of change; graph is a line.
- **Non-linear:** Rate of change is not constant (curve, quadratic, etc.).
- **Rate of change / slope:** `(Δy) / (Δx)`.

### Important Rules

| Source | Rate of change |
|--------|----------------|
| `y = 8.3x − 1` | **8.3** |
| `y = 5 − 0.5x` | **−0.5** |
| Table | `(y₂ − y₁) / (x₂ − x₁)` same for all pairs |

[DIAGRAM:linear_graph]

[DIAGRAM:rate_of_change]

### Example 1 — Table

**Problem:** (0,0), (3,90), (6,180), (9,270). Linear?

**Solution:** Slope `(90−0)/(3−0) = 30` each step → **linear**, rate **30**

**Answer:** **Linear**; rate of change **30**

### Example 2 — Non-linear table

**Problem:** x: 0,10,20,30 and y: 45,40,35,30 then 40,35…

**Solution:** Slopes not constant → **not linear**

**Answer:** **Not linear**

### Textbook practice (from the PDF)

*Activity 30 Practice.*

---

**1. Activity 30 Practice #6**

**Problem:** {(5, −3), (7, −1), (9, 1), (11, 3)} — linear?

**Solution:** Slope `(−1−(−3))/(7−5) = 1` and `(1−(−1))/(9−7) = 1` → **linear**

**Answer:** **Linear**

---

**2. Activity 30 Practice #8a**

**Problem:** Rate of change in `y = 8.3x − 1`.

**Solution:** Coefficient of x → **8.3**

**Answer:** **8.3**

---

**3. Activity 30 Practice #8b**

**Problem:** Rate of change in `y = 5 − 0.5x`.

**Solution:** Rewrite: `y = −0.5x + 5` → **−0.5**

**Answer:** **−0.5**

---

**4. Activity 30 Practice #9**

**Problem:** Table x: 0,3,6,9,12 and y: 0,90,180,270,360.

**Solution:** `(90−0)/3 = 30` always → rate **30**

**Answer:** Rate of change **30**

---

**5. Activity 30 Practice #10**

**Problem:** Rate of change for a linear equation must be…

**Solution:** Definition of linear → **constant** (choice A)

**Answer:** **A — constant**

---

**6. Activity 30 Practice #7 — which table is linear?**

**Problem:** Compare tables A and B from practice.

**Solution:** Check if `(y₂−y₁)/(x₂−x₁)` is the same between consecutive rows; linear table has **equal** differences in y per equal step in x.

**Answer:** The table with **constant** slope (compute each)

### Common Mistakes
- Plotting non-linear points and calling them linear because they "look almost straight."
- Using **different** x-intervals when computing slope.
- Confusing **positive** slope with "must be linear."

### Mini Summary
- Linear = **constant** rate of change = **straight** graph.
- From `y = mx + b`, **m** is the rate of change.
''',

    "activity_31_linear_nonlinear_functions.md": '''# Activity 31: Linear and Non-Linear Functions

[KEY]
**Scatter plots** show data pairs; a **trend line** models linear patterns.  
**Linear** data has roughly constant rate of change; **non-linear** curves or changes speed. Use **`y = mx + b`** or a trend line to **predict**.
[/KEY]

## Quick Review Notes

### Main Idea
Real measurements rarely lie exactly on a line. Scatter plots help you see whether a linear model fits. Trend lines support predictions; functions give exact values when the model is exact.

### Key Vocabulary
- **Scatter plot:** Graph of (x, y) data points only (not connected unless modeling).
- **Trend line:** Line drawn through the "middle" of linear-looking data.
- **Linear data:** Points roughly along a line; constant rate.
- **Non-linear data:** Curved pattern or changing steepness.

### Important Rules

**Water tank:** 2.25 gal/min → `w = 2.25t` (linear, through origin)

**Predict:** Substitute into your function or read from trend line.

[DIAGRAM:scatter_plot]

[DIAGRAM:linear_vs_nonlinear]

### Example 1 — Hose filling tank

**Problem:** 2.25 gallons per minute. Water after 6 minutes? After 8?

**Solution:** Table: 2.25, 4.5, 6.75, 9, 11.25, 13.5; **`w = 2.25t`**; t=8: **18 gallons**

**Answer:** **`w = 2.25t`**; **18 gallons** at 8 min

### Example 2 — Dog food (non-linear)

**Problem:** Food level rises quickly then levels off in the table.

**Solution:** Not constant rate → **non-linear**; trend line only **approximates** part of the data

**Answer:** **Non-linear**

### Textbook practice (from the PDF)

*Activity 31 Practice.*

---

**1. Activity 31 Practice #1**

**Problem:** Hose 2.25 gal/min — table for minutes 1–6.

**Solution:** 2.25, 4.5, 6.75, 9, 11.25, 13.5 gallons

**Answer:** **2.25, 4.5, 6.75, 9, 11.25, 13.5**

---

**2. Activity 31 Practice #2**

**Problem:** Scatter plot; linear? trend line; predict 8 minutes.

**Solution:** Constant rate → **linear**; trend matches **`w = 2.25t`**; 8 min ≈ **18 gal**

**Answer:** **Linear**; about **18 gallons** at 8 min

---

**3. Activity 31 Practice #3**

**Problem:** Write function for water; check 8 minutes vs trend line.

**Solution:** Let w = gallons, t = minutes: **`w = 2.25t`**; t=8 → **18** (matches trend)

**Answer:** **`w = 2.25t`**; **18 gallons**

---

**4. Activity 31 Practice #4**

**Problem:** Dog food level table — linear?

**Solution:** Level increases fast then slows — rate not constant → **non-linear**

**Answer:** **Not linear**

---

**5. Activity 31 Practice #6a**

**Problem:** How do you tell if data is linear or non-linear?

**Solution:** Check if rate of change `(Δy/Δx)` is **constant**; or if scatter plot is roughly a **straight line**

**Answer:** **Constant rate** or **straight-line pattern**

---

**6. Activity 31 Practice #6b**

**Problem:** Example of linear data and non-linear equation.

**Solution:** Linear: distance = 50t; Non-linear equation: **`y = x²`** or **`y = 2^x`**

**Answer:** Linear data example: **distance vs time at constant speed**; Non-linear: **`y = x²`**

### Common Mistakes
- Connecting scatter points with segments when you should only draw a **trend line** for linear fit.
- Using a linear model for clearly **curved** data without saying it is approximate.
- Forgetting **units** on axes (minutes, gallons).

### Mini Summary
- **Scatter plot** + **trend line** for real data.
- **Linear:** constant rate; **non-linear:** not constant.
''',
}

COMBINED = '''# Unit 4: Functions — Lesson Notes Cheat Sheet

## Introduction (Activity 27)
- **Function:** each input x has exactly **one** output y
- **Domain** = inputs; **Range** = outputs
- Evaluate by **substitution**

## Comparing & constructing (Activities 28–29)
- **`y = mx + b`**: m = **rate of change**, b = **starting value**
- **Directly proportional:** `y = kx` (through origin)
- Build from patterns: **table → graph → equation**

## Linear vs non-linear (Activities 30–31)
- **Linear:** constant rate of change, straight graph
- **Non-linear:** changing rate or curved pattern
- **Scatter plot** + **trend line** for real-world data
- Slope from table: `(y₂ − y₁) / (x₂ − x₁)`

## Embedded assessments (textbook)
- After Activity 29: Functions
- After Activity 31: Scatter plots and trend lines
'''


def main():
    for name, body in ACTIVITIES.items():
        path = NOTES / name
        path.write_text(body.strip() + "\n", encoding="utf-8")
        print(f"wrote {path}")
    combined_path = NOTES / "unit_4_functions_lesson_notes.md"
    combined_path.write_text(COMBINED.strip() + "\n", encoding="utf-8")
    print(f"wrote {combined_path}")


if __name__ == "__main__":
    main()
