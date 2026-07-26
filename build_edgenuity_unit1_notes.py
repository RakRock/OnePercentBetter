#!/usr/bin/env python3
"""One-time builder: writes Edgenuity Unit 1 activity markdown notes. Run: python build_edgenuity_unit1_notes.py"""

from pathlib import Path

NOTES = Path(__file__).parent / "ArjunEdgenuityCourse3" / "notes" / "unit_1"
NOTES.mkdir(parents=True, exist_ok=True)

ACTIVITIES = {
    "activity_1_coordinate_plane.md": '''# Activity 1: Coordinate Plane & Ordered Pairs

[KEY]
An **ordered pair** `(x, y)` gives a point on the coordinate plane: **x** is horizontal (left/right), **y** is vertical (up/down).  
Quadrants are numbered I (top-right), II (top-left), III (bottom-left), IV (bottom-right).
[/KEY]

## Quick Review Notes

### Main Idea
The coordinate plane has an **x-axis** (horizontal) and **y-axis** (vertical). They cross at the **origin** `(0, 0)`. Every point is written **(x, y)** — always x first.

### Key Vocabulary
- **Origin:** `(0, 0)`
- **Quadrant I:** x > 0, y > 0
- **Quadrant II:** x < 0, y > 0
- **Quadrant III:** x < 0, y < 0
- **Quadrant IV:** x > 0, y < 0
- **On the x-axis:** y = 0
- **On the y-axis:** x = 0

[DIAGRAM:quadrants]

[DIAGRAM:read_point]

### Example 1 — Read coordinates

**Problem:** What are the coordinates of point P shown at (−4, 3)?

**Solution:** Move **4 left** (x = −4), then **3 up** (y = 3).

**Answer:** **(−4, 3)**

### Example 2 — Which quadrant?

**Problem:** In which quadrant is `(−3, 5)`?

**Solution:** x is negative, y is positive → **Quadrant II**.

**Answer:** **Quadrant II**

### Example 3 — Point on an axis

**Problem:** Which point is on the **x-axis**?

**Solution:** On the x-axis, **y = 0**. Check `(1, 0)` ✓.

**Answer:** **(1, 0)**

### Exam-style practice

---

**1. Point in quadrant IV**

**Problem:** Which point is in quadrant IV?

**Solution:** Quadrant IV needs x > 0 and y < 0 → **(2, −4)**.

**Answer:** **(2, −4)**

---

**2. Signs check**

| Point | Quadrant |
|-------|----------|
| `(3, 2)` | I |
| `(−3, 5)` | II |
| `(−2, −4)` | III |
| `(2, −4)` | IV |

### Common Mistakes
- Reversing x and y: `(−4, 3)` is **not** the same as `(3, −4)`.
- Forgetting that points **on an axis** are not inside any quadrant.

### Mini Summary
- Read **(x, y)** — horizontal first, vertical second.
- Use sign patterns to identify quadrants quickly.
''',

    "activity_2_relations_functions.md": '''# Activity 2: Relations & Functions

[KEY]
A **function** is a relation where each **input** (x) has exactly **one output** (y).  
If one x-value appears with **two different y-values**, it is **not** a function.
[/KEY]

## Quick Review Notes

### Main Idea
A **relation** is any set of input-output pairs. It is a **function** only when every input maps to **exactly one** output. Check tables, graphs, and equations.

### Key Vocabulary
- **Relation:** Any set of (input, output) pairs
- **Function:** Each input has exactly one output
- **Vertical line test:** If a vertical line hits a graph more than once, it is not a function
- **Domain:** All input values
- **Range:** All output values

[DIAGRAM:vertical_line_test]

[DIAGRAM:mapping_diagram]

[DIAGRAM:function_equations]

### Example 1 — Table with duplicate inputs (Exam Q2)

**Problem:** Fun Zone party packages: each package number has a **weekend** price and a **weekday** price. Is (package number, price) a function?

**Solution:** Package 1 has prices $160 **and** $110 — same input, two outputs → **not a function**.

**Answer:** **Not a function** — each package number has two different prices.

### Example 2 — Remove a point to make a function (Exam Q4)

**Problem:** Points include `(−2, 1)` and `(−2, −3)`. Which point should be removed so the set is a function?

**Solution:** x = −2 appears twice. Remove one of them, e.g. **(−2, 1)**.

**Answer:** Remove **(−2, 1)** (or the other duplicate).

### Example 3 — Which equation is a function of x? (Exam Q7)

**Problem:** Which equation defines **y as a function of x**?

**Solution:**
- `x = y² + 9` — one x can come from two y values → not a function of x in the usual y-form
- **`x² = y`** → `y = x²` — each x gives one y ✓
- `x = 5` — vertical line, not a function of x
- `x² = y² + 16` — not a function

**Answer:** **`x² = y`** (equivalently `y = x²`)

### Exam-style practice

---

**1. Which table is a function?**

| x | y |
|---|---|
| −3 | −1 |
| −2 | 5 |
| 4 | 0 |
| 7 | −1 |

**Solution:** Every x appears once → **function**.

---

**2. Trap: pattern vs function**

A table shows weekend prices are always $50 more than weekday prices. Does that make it a function?

**Solution:** **No.** A consistent pattern does not fix duplicate inputs. Each package still has two prices.

### Common Mistakes
- Thinking a **rule** or pattern makes something a function when inputs repeat.
- Confusing "there is a price for every package" with "each input has one output."

### Mini Summary
- **One x → one y** = function.
- Same x with different y values = **not** a function.
- Use the **vertical line test** on graphs.
''',

    "activity_3_graph_behavior.md": '''# Activity 3: Graph Behavior

[KEY]
On a graph, **increasing** means y goes up as x moves right; **decreasing** means y goes down; **constant** means y stays flat.  
In distance-time graphs, a **horizontal** segment means **no change in distance** (stopped).
[/KEY]

## Quick Review Notes

### Main Idea
Describe graphs by how y changes as x increases: **increasing**, **decreasing**, or **constant**. Real-world stories (bike rides, trips) map to these behaviors.

[DIAGRAM:segment_graph]

[DIAGRAM:parabola_behavior]

[DIAGRAM:distance_time]

### Example 1 — Multi-segment graph (Exam Q1)

**Problem:** Between points A and C, the graph rises, then stays flat. How does the graph change?

**Solution:** A → B: **increasing**. B → C: **constant**.

**Answer:** **The graph increases, then remains constant.**

### Example 2 — Parabola (Exam Q5)

**Problem:** A parabola opening upward — best description?

**Solution:** Left of the vertex it **decreases**; right of the vertex it **increases**.

**Answer:** **Decreasing, then increasing**

### Example 3 — Mary's bike ride (Exam Q9)

**Problem:** Mary rides, **stops at a traffic light**, walks up a hill, then rides at constant speed. Which part shows **no change in distance**?

**Solution:** While waiting at the light, time passes but distance does not increase → **horizontal** segment.

**Answer:** **Mary stopped and waited for the traffic light.**

### Example 4 — Increasing curve (Exam Q24)

**Problem:** Between A and B on an upward curve, how does the graph change?

**Solution:** y increases as x increases.

**Answer:** **The graph increases.**

### Exam-style practice

---

**1. Segment from C to D dropping steeply**

**Answer:** **Decreasing**

---

**2. Distance-time: flat line for 5 minutes**

**Answer:** **Constant** (not moving)

### Common Mistakes
- Saying "increasing then decreasing" for a parabola that only shows the right side.
- Confusing **steep** with **increasing** — steep describes rate, not direction alone.

### Mini Summary
- Left to right: up = increasing, flat = constant, down = decreasing.
- Distance-time: flat = stopped.
''',

    "activity_4_linear_equations.md": '''# Activity 4: Linear Equations from Tables

[KEY]
A **linear relationship** has a constant rate of change. From a table, find **y = mx + b** (or **y = mx** when b = 0).  
**Unit rate** = change in y ÷ change in x.
[/KEY]

## Quick Review Notes

### Main Idea
Tables show input-output pairs. When y changes by a fixed amount for each step in x, the relationship is linear. Write an equation and use it to predict values.

[DIAGRAM:unit_rate]

[DIAGRAM:perimeter_equation]

[DIAGRAM:jaxon_change]

### Example 1 — Unit rate (Exam Q15)

**Problem:** Tickets sold → profit: 2→$18, 4→$36, 6→$54. Profit per ticket?

**Solution:** 18 ÷ 2 = **$9** per ticket. Equation: **profit = 9 × tickets**.

**Answer:** **$9 per ticket** — `y = 9x`

### Example 2 — Perimeter of a square (Exam Q19)

**Problem:** Side x → perimeter y: 4.5→18, 8.5→34, etc. Which equation?

**Solution:** y ÷ x = 4 always → **y = 4x**.

**Answer:** **y = 4x**

### Example 3 — Jaxon's change (Exam Q25)

**Problem:** Graph shows change y when item costs x. Points: (0,10), (1,9), … (9,1). Equation?

**Solution:** Start at 10, lose $1 per dollar spent → **y = 10 − x**.

**Answer:** **y = 10 − x**

### Example 4 — Hourly pay (Exam Q23)

**Problem:** Carey earns $9.75 per hour. Amount for 3 hours?

**Solution:** 9.75 × 3 = **$29.25**.

**Answer:** **$29.25**

### Exam-style practice

---

**1. Proportional table**

| x | 0 | 2 | 5 |
|---|---|---|---|
| y | 0 | 6 | 15 |

**Equation:** **y = 3x**

### Common Mistakes
- Using **y − x** when the rate is **y ÷ x**.
- Picking **y = x + 10** when the pattern is multiply, not add.

### Mini Summary
- Find constant rate: `(y₂ − y₁) ÷ (x₂ − x₁)`.
- Perimeter of square: **P = 4s**.
- Change from $10: **change = 10 − cost**.
''',

    "activity_5_completing_tables.md": '''# Activity 5: Completing & Using Tables

[KEY]
Given an equation, **substitute** each input to find outputs. Given a table, find the **missing value** or match the table to a **graph**.
[/KEY]

## Quick Review Notes

### Main Idea
Functions connect equations, tables, and graphs. Evaluate formulas, fill missing cells, and verify that plotted points lie on the same line.

[DIAGRAM:table_to_graph]

[DIAGRAM:evaluate_equation]

[DIAGRAM:gas_tank]

### Example 1 — Evaluate r = 3c + 5 (Exam Q22)

**Problem:** c = 6→23, 8→29, 12→?, 18→59. Find missing value.

**Solution:** r = 3(12) + 5 = 36 + 5 = **41**.

**Answer:** **41**

### Example 2 — Match table to graph (Exam Q17)

**Problem:** Graph passes through (−3, −2), (−1, 0), (1, 2). Which table?

**Solution:** x values −3, −1, 1 with y values −2, 0, 2 → equation **y = x + 1**.

**Answer:** Table with **(−3, −2), (−1, 0), (1, 2)**

### Example 3 — Gas tank (Exam Q8)

**Problem:** Distance 0→12 gal, 20→11, 60→9, 100→7, ?→0 gal. What question can be answered?

**Solution:** Linear decrease: 1 gallon per 20 miles. At 0 gallons, distance = **240 miles**. Question: **How far can the car travel on a full tank?**

**Answer:** **Distance on a full tank (240 miles)**

### Exam-style practice

---

**1. y = 2x + 1, find y when x = 7**

**Solution:** y = 2(7) + 1 = **15**

---

**2. Table with slope 1**

| x | −2 | 0 | 2 |
|---|---|---|---|
| y | −3 | −1 | 1 |

**Equation:** **y = x − 1**

### Common Mistakes
- Arithmetic slips when substituting negative numbers.
- Matching a table with the **same numbers** but wrong x-y pairing.

### Mini Summary
- Substitute carefully: **PEMDAS**.
- Check that every row satisfies the equation.
''',

    "activity_6_word_problems.md": '''# Activity 6: Real-World Word Problems

[KEY]
Translate stories into **equations**, compare two plans, solve **inequalities** for "at least" problems, and work **backward** (find input when output is known).
[/KEY]

## Quick Review Notes

### Main Idea
Real problems use linear functions. Set up two models, compare at a given input, solve for when a goal is met, or reverse the equation to find the input.

[DIAGRAM:movie_rentals]

[DIAGRAM:bank_deposits]

[DIAGRAM:inverse_lookup]

### Example 1 — Movie rentals (Exam Q6)

**Problem:** Movies Plus: $10 fee + $2 per movie. Movies For Less: $3 per movie, no fee. Cost for 15 movies each?

**Solution:**
- Plus: 10 + 2(15) = **$40**
- For Less: 3(15) = **$45**
- For Less costs **$5 more**.

**Answer:** **Movies For Less costs $5 more**

### Example 2 — Bank account (Exam Q20)

**Problem:** Li has $125, deposits $45 per month. At least $360 in how many months?

**Solution:** 125 + 45m ≥ 360 → 45m ≥ 235 → m ≥ 5.22… → need **6** full months.

**Check:** 125 + 45(6) = 395 ≥ 360 ✓

**Answer:** **6 months**

### Example 3 — Sarah's craft demo (Exam Q21) ⚠️ Focus

**Problem:** People → cost: 5→$15, 8→$18, 10→$20, 15→$25. Total cost $60 — how many people?

**Solution:** Pattern: **cost = people + 10** (check: 5+10=15 ✓).  
60 = x + 10 → **x = 50**.

**Answer:** **50 people** (not 30!)

### Exam-style practice

---

**1. Two phone plans**

Plan A: $20 + $0.10/min. Plan B: $0.25/min. Break-even?

**Solution:** 20 + 0.10m = 0.25m → 20 = 0.15m → m ≈ 133 min.

---

**2. Inverse: y = 4x + 7, find x when y = 31**

**Solution:** 31 = 4x + 7 → 4x = 24 → **x = 6**

### Common Mistakes
- **Q21 trap:** Guessing 30 by adding wrong offset — always find the equation first.
- Rounding **down** on "at least" problems (need 6 months, not 5).

### Mini Summary
- Write both models, then compare or solve.
- For inverse problems: **isolate x** after finding the rule.
''',

    "unit_1_input_output_relationships_lesson_notes.md": '''# Unit 1: Input-Output Relationships — Overview

| Activity | Topic | Key idea |
|----------|-------|----------|
| **1** | Coordinate Plane | Ordered pairs, quadrants, axes |
| **2** | Relations & Functions | One input → one output; vertical line test |
| **3** | Graph Behavior | Increasing / decreasing / constant; distance-time |
| **4** | Linear Equations | Unit rate, y = mx + b, real graphs |
| **5** | Completing Tables | Substitute, match table ↔ graph |
| **6** | Word Problems | Compare plans, inequalities, inverse lookup |

**Exam focus areas:** Function-or-not tables (Q2), inverse lookup (Q21).

Open each activity for full notes, diagrams, and worked exam-style problems. Use **Daily Practice** for 15-question quiz sets with graphs.
''',
}


def main():
    for filename, content in ACTIVITIES.items():
        path = NOTES / filename
        path.write_text(content.strip() + "\n", encoding="utf-8")
        print(f"  wrote {path.name}")
    print("Done.")


if __name__ == "__main__":
    main()
