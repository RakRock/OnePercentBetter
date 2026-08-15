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
The coordinate plane is like a map with two number lines that cross at the **origin** `(0, 0)`. Every location is written as an **ordered pair (x, y)** — x tells you how far left or right to go, and y tells you how far up or down. This matters because graphs, maps, and games all use the same system to describe exact positions. Once you know the signs of x and y, you can instantly tell which **quadrant** a point is in.

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

**What is this about:** You have a point marked on the graph and need to read its exact address as an ordered pair.

**Problem:** What are the coordinates of point P shown at (−4, 3)?

**How to think about it:** Always read **x first** (left/right), then **y** (up/down). Negative x means left of the origin; positive y means above the origin. Think of it like giving directions: "Go 4 left, then 3 up."

**Solution (step by step):**
1. Start at the origin `(0, 0)`.
2. Move **4 units left** because x = −4 (negative means left).
3. From there, move **3 units up** because y = 3 (positive means up).
4. You arrive at point P.

**Answer:** **(−4, 3)**

**Why this works:** Ordered pairs always list horizontal movement (x) before vertical movement (y), so everyone describes the same point the same way.

### Example 2 — Which quadrant?

**What is this about:** You know the coordinates of a point and need to figure out which section of the plane it sits in.

**Problem:** In which quadrant is `(−3, 5)`?

**How to think about it:** Look at the signs: x = −3 is negative (left side), y = 5 is positive (top). Quadrants are numbered counterclockwise starting from the top-right. Negative x + positive y lands you in the top-left region.

**Solution (step by step):**
1. Check x: −3 is **negative** → the point is on the **left** side of the y-axis.
2. Check y: 5 is **positive** → the point is **above** the x-axis.
3. Top-left = **Quadrant II**.

**Answer:** **Quadrant II**

**Why this works:** Each quadrant has a unique sign pattern for x and y, so checking signs is the fastest way to identify where a point lives.

### Example 3 — Point on an axis

**What is this about:** Some points sit exactly on an axis instead of inside a quadrant — you need to spot which coordinate is zero.

**Problem:** Which point is on the **x-axis**?

**How to think about it:** The x-axis is the horizontal line where you never go up or down. That means the y-coordinate must be **0**. Any point with y = 0 sits on the x-axis, no matter what x is.

**Solution (step by step):**
1. Remember: on the x-axis, **y = 0**.
2. Check each option for y = 0.
3. `(1, 0)` has y = 0 ✓ — it sits on the x-axis.

**Answer:** **(1, 0)**

**Why this works:** Points on an axis always have one coordinate equal to zero, because you haven't moved in that direction at all.

### Exam-style practice

---

**1. Point in quadrant IV**

**Problem:** Which point is in quadrant IV?

**How to think about it:** Quadrant IV is the bottom-right corner. You need a point where x is positive (right) and y is negative (down).

**Solution (step by step):**
1. Quadrant IV requires **x > 0** and **y < 0**.
2. Check `(2, −4)`: x = 2 is positive ✓, y = −4 is negative ✓.
3. This point is in Quadrant IV.

**Answer:** **(2, −4)**

---

**2. Signs check**

| Point | Quadrant |
|-------|----------|
| `(3, 2)` | I |
| `(−3, 5)` | II |
| `(−2, −4)` | III |
| `(2, −4)` | IV |

**Problem:** Match each point to its quadrant using sign patterns.

**How to think about it:** Both positive = top-right (I). Negative x, positive y = top-left (II). Both negative = bottom-left (III). Positive x, negative y = bottom-right (IV).

**Solution (step by step):**
1. `(3, 2)`: both positive → **Quadrant I**.
2. `(−3, 5)`: negative x, positive y → **Quadrant II**.
3. `(−2, −4)`: both negative → **Quadrant III**.
4. `(2, −4)`: positive x, negative y → **Quadrant IV**.

**Answer:** See table above — I, II, III, IV respectively.

### Common Mistakes
- **Reversing x and y:** `(−4, 3)` means 4 left and 3 up — it is **not** the same as `(3, −4)`, which would be 3 right and 4 down. Always write x first!
- **Forgetting axis points:** Points like `(1, 0)` or `(0, 5)` sit **on an axis**, not inside any quadrant. If either coordinate is zero, the point is on a boundary line.
- **Mixing up left/right with up/down:** x controls horizontal movement only; y controls vertical movement only. Don't swap them when reading a graph.

### Mini Summary
- Read every point as **(x, y)** — horizontal first, vertical second.
- Use sign patterns to identify quadrants quickly: (+,+), (−,+), (−,−), (+,−).
- Points on an axis have one coordinate equal to zero and belong to **no quadrant**.
- Parents/teachers: have your student practice by naming a point aloud ("3 left, 2 down") before writing the ordered pair.
''',

    "activity_2_relations_functions.md": '''# Activity 2: Relations & Functions

[KEY]
A **function** is a relation where each **input** (x) has exactly **one output** (y).  
If one x-value appears with **two different y-values**, it is **not** a function.
[/KEY]

## Quick Review Notes

### Main Idea
A **relation** is any collection of input-output pairs — like a list of who is paired with what. A **function** is a special kind of relation where every input gets exactly **one** output, no exceptions. This matters because functions are predictable: if you know the input, you know the output. Machines, formulas, and graphs that are functions won't give you two different answers for the same question.

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

**What is this about:** A party venue charges different prices for weekend and weekday packages, and you need to decide if "package number → price" is a function.

**Problem:** Fun Zone party packages: each package number has a **weekend** price and a **weekday** price. Is (package number, price) a function?

**How to think about it:** A function means one input, one output. Package 1 is a single input — but it has **two different prices** depending on the day. That's like asking "What is the price of Package 1?" and getting two different answers.

**Solution (step by step):**
1. Identify the input: **package number**.
2. Check Package 1: it has price **$160** (weekend) **and** **$110** (weekday).
3. Same input (Package 1), two different outputs → **not a function**.

**Answer:** **Not a function** — each package number has two different prices.

**Why this works:** Functions require exactly one output per input; duplicate inputs with different outputs break that rule.

### Example 2 — Remove a point to make a function (Exam Q4)

**What is this about:** You have a set of coordinate points and need to remove one so that each x-value appears only once.

**Problem:** Points include `(−2, 1)` and `(−2, −3)`. Which point should be removed so the set is a function?

**How to think about it:** Both points share x = −2 but have different y-values. To make this a function, you can only keep **one** of them — remove whichever duplicate you don't need.

**Solution (step by step):**
1. Find the repeated x-value: **x = −2** appears twice.
2. The two outputs are y = 1 and y = −3 — that's two outputs for one input.
3. Remove one point, e.g. **(−2, 1)**, so x = −2 has only one y-value left.

**Answer:** Remove **(−2, 1)** (or the other duplicate).

**Why this works:** Once each x appears exactly once, every input maps to a single output — the definition of a function.

### Example 3 — Which equation is a function of x? (Exam Q7)

**What is this about:** You need to pick the equation where each x-value gives exactly one y-value.

**Problem:** Which equation defines **y as a function of x**?

**How to think about it:** "y as a function of x" means: plug in any x, get **one** y. Vertical lines and circles fail this test. Look for equations where y is determined uniquely by x.

**Solution (step by step):**
1. `x = y² + 9` — solving for y gives ±√(x−9), so one x can give **two y values** → not a function of x in the usual form.
2. **`x² = y`** → rewrite as **`y = x²`** — each x gives exactly **one** y ✓
3. `x = 5` — this is a vertical line; x is always 5 regardless of y → not a function of x.
4. `x² = y² + 16` — one x can pair with two y values → not a function.

**Answer:** **`x² = y`** (equivalently `y = x²`)

**Why this works:** `y = x²` passes the vertical line test — every vertical line crosses the parabola at most once.

### Exam-style practice

---

**1. Which table is a function?**

| x | y |
|---|---|
| −3 | −1 |
| −2 | 5 |
| 4 | 0 |
| 7 | −1 |

**Problem:** Is this table a function?

**How to think about it:** Scan the x-column. If any x-value repeats with a **different** y, it's not a function. Repeating y-values with different x-values is fine.

**Solution (step by step):**
1. List all x-values: −3, −2, 4, 7.
2. Each x appears **exactly once**.
3. Every input has one output → **function**.

**Answer:** **Yes, it is a function.**

---

**2. Trap: pattern vs function**

A table shows weekend prices are always $50 more than weekday prices. Does that make it a function?

**Problem:** Does a consistent price pattern make the relation a function?

**How to think about it:** A nice pattern doesn't fix duplicate inputs. If Package 1 still has two prices ($160 and $110), the same input still has two outputs — no matter how regular the pattern looks.

**Solution (step by step):**
1. Check inputs, not patterns: does any package number appear twice?
2. Yes — each package has both a weekend and weekday price.
3. Same input, two outputs → **not a function**, even with a consistent $50 difference.

**Answer:** **No.** A consistent pattern does not fix duplicate inputs. Each package still has two prices.

### Common Mistakes
- **Confusing pattern with function:** A rule like "weekend is always $50 more" sounds organized, but if one input (package number) has two outputs (two prices), it's still **not** a function.
- **Thinking "every input has an output" is enough:** Having a price for every package is not the same as having **one** price per package.
- **Mixing up x and y in equations:** "y as a function of x" means y depends on x — vertical lines like `x = 5` fail because x doesn't determine a unique y.

### Mini Summary
- **One x → one y** = function. Same x with different y values = **not** a function.
- Use the **vertical line test** on graphs: if a vertical line hits twice, it's not a function.
- Parents/teachers: ask "If I give you this input, is there only one possible answer?" — that's the function test in plain language.
''',

    "activity_3_graph_behavior.md": '''# Activity 3: Graph Behavior

[KEY]
On a graph, **increasing** means y goes up as x moves right; **decreasing** means y goes down; **constant** means y stays flat.  
In distance-time graphs, a **horizontal** segment means **no change in distance** (stopped).
[/KEY]

## Quick Review Notes

### Main Idea
When you read a graph from left to right, you can describe what happens to y in three simple words: **increasing** (going up), **decreasing** (going down), or **constant** (staying flat). This helps you tell stories about real life — like bike rides, road trips, or savings accounts — just by looking at the shape of a line. Distance-time graphs are especially useful: a flat line means someone **stopped moving**, even though time keeps ticking.

[DIAGRAM:segment_graph]

[DIAGRAM:parabola_behavior]

[DIAGRAM:distance_time]

### Example 1 — Multi-segment graph (Exam Q1)

**What is this about:** A graph has different sections — part of it rises, then part of it goes flat. You describe each section separately.

**Problem:** Between points A and C, the graph rises, then stays flat. How does the graph change?

**How to think about it:** Break the trip into pieces. From A to B, the line goes up (y increases). From B to C, the line is flat (y stays the same). Describe each piece in order.

**Solution (step by step):**
1. Look at segment A → B: the line **goes up** as x increases → **increasing**.
2. Look at segment B → C: the line is **flat** → **constant**.
3. Combine: the graph increases, then remains constant.

**Answer:** **The graph increases, then remains constant.**

**Why this works:** Graph behavior is always described left to right, one segment at a time.

### Example 2 — Parabola (Exam Q5)

**What is this about:** A U-shaped parabola opening upward has a lowest point (vertex). The graph falls on one side and rises on the other.

**Problem:** A parabola opening upward — best description?

**How to think about it:** Picture a bowl. On the left side, you slide down into the bowl (decreasing). On the right side, you climb back up (increasing). The vertex is the turning point.

**Solution (step by step):**
1. Left of the vertex: as x increases, y **decreases** → **decreasing**.
2. Right of the vertex: as x increases, y **increases** → **increasing**.
3. Full description: decreasing, then increasing.

**Answer:** **Decreasing, then increasing**

**Why this works:** A parabola opening upward always falls to its minimum, then rises — that's the classic "decreasing then increasing" shape.

### Example 3 — Mary's bike ride (Exam Q9)

**What is this about:** Mary's distance-from-home graph tells a story about her bike ride, including a stop at a traffic light.

**Problem:** Mary rides, **stops at a traffic light**, walks up a hill, then rides at constant speed. Which part shows **no change in distance**?

**How to think about it:** On a distance-time graph, distance is on the y-axis and time on the x-axis. If distance doesn't change, the graph goes **flat** (horizontal) — even though time is still passing.

**Solution (step by step):**
1. While Mary **rides**, distance increases → slanted upward line.
2. While she **waits at the light**, time passes but she doesn't move → distance stays the same → **horizontal** segment.
3. The flat part = stopped and waiting.

**Answer:** **Mary stopped and waited for the traffic light.**

**Why this works:** A horizontal segment on a distance-time graph means zero change in distance — the person is stationary.

### Example 4 — Increasing curve (Exam Q24)

**What is this about:** A smooth upward curve between two points always goes up as you move right.

**Problem:** Between A and B on an upward curve, how does the graph change?

**How to think about it:** Trace the curve from A to B left to right. If y keeps getting higher, the graph is increasing — even if the curve is curved instead of straight.

**Solution (step by step):**
1. Start at point A and move right toward B.
2. At every step, y is **higher** than before.
3. The graph is **increasing** throughout this interval.

**Answer:** **The graph increases.**

**Why this works:** "Increasing" only cares about direction (up or down), not whether the line is straight or curved.

### Exam-style practice

---

**1. Segment from C to D dropping steeply**

**Problem:** A graph segment from C to D goes sharply downward. How does the graph change?

**How to think about it:** Moving left to right, if y goes down, the graph is decreasing. "Steep" describes how fast, but the direction is still down.

**Solution (step by step):**
1. Trace from C to D, moving right.
2. y-values get **smaller** → the line goes down.
3. Direction = **decreasing**.

**Answer:** **Decreasing**

---

**2. Distance-time: flat line for 5 minutes**

**Problem:** A distance-time graph is flat (horizontal) for 5 minutes. What does that mean?

**How to think about it:** Time is passing (x increases) but distance stays the same (y doesn't change). That means the person isn't moving.

**Solution (step by step):**
1. Horizontal line → y stays the same while x increases.
2. On a distance-time graph, unchanged distance = not moving.
3. The behavior is **constant** (not increasing or decreasing).

**Answer:** **Constant** (not moving)

### Common Mistakes
- **Describing only part of a parabola:** A full upward parabola goes decreasing then increasing — don't say "increasing then decreasing" unless the graph actually shows that.
- **Confusing steep with increasing:** Steep describes **how fast** y changes; increasing/decreasing describes **which direction**. A steep downward line is decreasing, not increasing.
- **Forgetting distance-time meaning:** A flat line doesn't mean "nothing happened" — time still passed, but distance didn't change (the person stopped).

### Mini Summary
- Read graphs **left to right**: up = increasing, flat = constant, down = decreasing.
- On distance-time graphs, a **flat (horizontal) segment** means the person stopped.
- Parabolas opening upward: **decreasing** on the left, **increasing** on the right.
- Parents/teachers: have your student tell the "story" of a graph out loud before labeling increasing/decreasing/constant.
''',

    "activity_4_linear_equations.md": '''# Activity 4: Linear Equations from Tables

[KEY]
A **linear relationship** has a constant rate of change. From a table, find **y = mx + b** (or **y = mx** when b = 0).  
**Unit rate** = change in y ÷ change in x.
[/KEY]

## Quick Review Notes

### Main Idea
When a table shows that y changes by the same amount every time x goes up by 1, you have a **linear relationship** — and you can write it as an equation. The **unit rate** tells you how much y changes per one step of x, like dollars per ticket or miles per hour. Equations let you predict values you haven't seen in the table yet, which is why businesses, scientists, and athletes all use them.

[DIAGRAM:unit_rate]

[DIAGRAM:perimeter_equation]

[DIAGRAM:jaxon_change]

### Example 1 — Unit rate (Exam Q15)

**What is this about:** A fundraiser sells tickets and tracks profit. You find how much profit each ticket earns.

**Problem:** Tickets sold → profit: 2→$18, 4→$36, 6→$54. Profit per ticket?

**How to think about it:** Pick any row and divide profit by tickets — the answer should be the same every time if the rate is constant. That's your unit rate (slope).

**Solution (step by step):**
1. Pick the first row: 18 ÷ 2 = **9**.
2. Check: 36 ÷ 4 = 9 ✓ and 54 ÷ 6 = 9 ✓.
3. Each ticket earns **$9** profit.
4. Equation: **profit = 9 × tickets**, or **y = 9x**.

**Answer:** **$9 per ticket** — `y = 9x`

**Why this works:** Dividing y by x gives the constant unit rate, which becomes the multiplier in the equation.

### Example 2 — Perimeter of a square (Exam Q19)

**What is this about:** A table shows side length and perimeter of squares. You find the equation connecting them.

**Problem:** Side x → perimeter y: 4.5→18, 8.5→34, etc. Which equation?

**How to think about it:** Perimeter of a square = 4 × side. Check: does y ÷ x always equal 4?

**Solution (step by step):**
1. Compute y ÷ x for the first row: 18 ÷ 4.5 = **4**.
2. Check second row: 34 ÷ 8.5 = 4 ✓.
3. The pattern is **y = 4x** — perimeter is always 4 times the side length.

**Answer:** **y = 4x**

**Why this works:** A square has 4 equal sides, so perimeter = 4 × side — a proportional linear equation.

### Example 3 — Jaxon's change (Exam Q25)

**What is this about:** Jaxon starts with $10 and spends money on an item. The graph shows how much change he has left.

**Problem:** Graph shows change y when item costs x. Points: (0,10), (1,9), … (9,1). Equation?

**How to think about it:** Jaxon starts with $10 (that's his y-intercept at x = 0). Every dollar he spends, he loses one dollar of change. So the rate is −1, or you can think "change = 10 minus cost."

**Solution (step by step):**
1. At x = 0, y = 10 → starting amount is **$10**.
2. Each time x increases by 1, y decreases by 1 → rate = **−1** (or lose $1 per dollar spent).
3. Equation: **y = 10 − x**.

**Answer:** **y = 10 − x**

**Why this works:** Starting value minus amount spent gives remaining change — a linear equation with a negative rate.

### Example 4 — Hourly pay (Exam Q23)

**What is this about:** Carey earns a fixed amount per hour and you calculate her pay for a specific number of hours.

**Problem:** Carey earns $9.75 per hour. Amount for 3 hours?

**How to think about it:** This is a unit rate problem: multiply hours by the pay rate. No starting fee, so it's proportional.

**Solution (step by step):**
1. Rate = **$9.75 per hour**.
2. Multiply: 9.75 × 3 = **29.25**.
3. Carey earns **$29.25** for 3 hours.

**Answer:** **$29.25**

**Why this works:** Pay = rate × hours is the basic linear model for hourly wages.

### Exam-style practice

---

**1. Proportional table**

| x | 0 | 2 | 5 |
|---|---|---|---|
| y | 0 | 6 | 15 |

**Problem:** Find the equation for this table.

**How to think about it:** When x = 0, y = 0 — the line passes through the origin. Find y ÷ x for any nonzero row to get the constant multiplier.

**Solution (step by step):**
1. Check: 6 ÷ 2 = 3 and 15 ÷ 5 = 3 — constant ratio.
2. y is always **3 times** x.
3. Equation: **y = 3x**.

**Answer:** **y = 3x**

### Common Mistakes
- **Using subtraction instead of division:** The rate is **y ÷ x** (or change in y ÷ change in x), not y − x.
- **Picking y = x + 10 when the pattern is multiply:** Jaxon's change loses $1 per $1 spent — that's subtracting, not adding 10 to x.
- **Forgetting to check multiple rows:** Always verify your rate with at least two pairs to make sure it's constant.

### Mini Summary
- Find the constant rate: **(y₂ − y₁) ÷ (x₂ − x₁)** or **y ÷ x** for proportional tables.
- Perimeter of a square: **P = 4s**. Change from $10: **change = 10 − cost**.
- Parents/teachers: encourage your student to say the rate in words first ("$9 per ticket") before writing the equation.
''',

    "activity_5_completing_tables.md": '''# Activity 5: Completing & Using Tables

[KEY]
Given an equation, **substitute** each input to find outputs. Given a table, find the **missing value** or match the table to a **graph**.
[/KEY]

## Quick Review Notes

### Main Idea
Equations, tables, and graphs are three ways to show the **same relationship**. You can plug numbers into an equation to fill a table, or read a table to find a missing value, or check that points from a table lie on a graph. Being able to move between these forms helps you solve problems even when the question gives you only one representation — which is exactly what exams often do.

[DIAGRAM:table_to_graph]

[DIAGRAM:evaluate_equation]

[DIAGRAM:gas_tank]

### Example 1 — Evaluate r = 3c + 5 (Exam Q22)

**What is this about:** A table shows values for the equation r = 3c + 5, but one cell is missing. You plug in to find it.

**Problem:** c = 6→23, 8→29, 12→?, 18→59. Find missing value.

**How to think about it:** Replace c with 12 in the equation and follow order of operations: multiply first, then add.

**Solution (step by step):**
1. Write the equation: **r = 3c + 5**.
2. Substitute c = 12: r = 3(12) + 5.
3. Multiply: 3 × 12 = 36.
4. Add: 36 + 5 = **41**.

**Answer:** **41**

**Why this works:** Substituting the input into the equation always gives the correct output for a function.

### Example 2 — Match table to graph (Exam Q17)

**What is this about:** A graph passes through three known points. You pick the table that lists those same (x, y) pairs.

**Problem:** Graph passes through (−3, −2), (−1, 0), (1, 2). Which table?

**How to think about it:** Each row of the correct table must match a point on the graph exactly. You can also find the equation: y goes up by 2 when x goes up by 2, so slope = 1, and y = x + 1.

**Solution (step by step):**
1. List the graph points: (−3, −2), (−1, 0), (1, 2).
2. Check: at x = −3, y = −3 + 1 = −2 ✓; at x = −1, y = 0 ✓; at x = 1, y = 2 ✓.
3. The matching table has rows **(−3, −2), (−1, 0), (1, 2)**.
4. Equation: **y = x + 1**.

**Answer:** Table with **(−3, −2), (−1, 0), (1, 2)**

**Why this works:** Every point on a line must satisfy the same equation — the table and graph must agree on every pair.

### Example 3 — Gas tank (Exam Q8)

**What is this about:** A car's gas gauge drops steadily as you drive. You figure out what real-world question the table can answer.

**Problem:** Distance 0→12 gal, 20→11, 60→9, 100→7, ?→0 gal. What question can be answered?

**How to think about it:** Gas decreases by 1 gallon every 20 miles — that's a constant rate. The last row asks: at what distance does the tank hit 0 gallons? That's how far you can drive on a full tank.

**Solution (step by step):**
1. Find the rate: from 0 to 20 miles, gas drops 12 − 11 = 1 gallon → **1 gal per 20 miles**.
2. At 0 gallons, you've used all 12 gallons: 12 × 20 = **240 miles**.
3. The missing distance is **240**, and the question is: **How far can the car travel on a full tank?**

**Answer:** **Distance on a full tank (240 miles)**

**Why this works:** Working backward from the constant rate tells you the total distance before the tank is empty.

### Exam-style practice

---

**1. y = 2x + 1, find y when x = 7**

**Problem:** Evaluate y = 2x + 1 when x = 7.

**How to think about it:** Replace x with 7, then multiply before adding (PEMDAS).

**Solution (step by step):**
1. Substitute: y = 2(7) + 1.
2. Multiply: 2 × 7 = 14.
3. Add: 14 + 1 = **15**.

**Answer:** **15**

---

**2. Table with slope 1**

| x | −2 | 0 | 2 |
|---|---|---|---|
| y | −3 | −1 | 1 |

**Problem:** Find the equation for this table.

**How to think about it:** As x goes up by 2, y goes up by 2 — slope = 1. At x = 0, y = −1, so the y-intercept is −1.

**Solution (step by step):**
1. Slope: (1 − (−1)) ÷ (2 − 0) = 2 ÷ 2 = **1**.
2. y-intercept: when x = 0, y = **−1**.
3. Equation: **y = x − 1**.

**Answer:** **y = x − 1**

### Common Mistakes
- **Arithmetic slips with negatives:** Substituting x = −3 into y = x + 1 gives −3 + 1 = −2, not −4. Work carefully with signs.
- **Matching numbers but wrong pairs:** A table might contain the right numbers but pair them incorrectly — always check that each (x, y) matches the graph point exactly.
- **Skipping PEMDAS:** In r = 3c + 5, multiply 3 × c **before** adding 5.

### Mini Summary
- Substitute carefully using **PEMDAS** — multiply/divide before add/subtract.
- Check that **every row** satisfies the equation.
- Tables, equations, and graphs are interchangeable — learn to move between them.
- Parents/teachers: pick one row and have your student show the substitution step-by-step aloud to catch sign errors early.
''',

    "activity_6_word_problems.md": '''# Activity 6: Real-World Word Problems

[KEY]
Translate stories into **equations**, compare two plans, solve **inequalities** for "at least" problems, and work **backward** (find input when output is known).
[/KEY]

## Quick Review Notes

### Main Idea
Real-world problems almost always become **linear equations** once you translate the words into math. You might compare two phone plans, figure out how many months until a savings goal, or work backward to find how many people attended an event. The key skill is turning the story into a model first — then the algebra is straightforward. This is one of the most useful math topics because it shows up in money, time, and everyday decisions.

[DIAGRAM:movie_rentals]

[DIAGRAM:bank_deposits]

[DIAGRAM:inverse_lookup]

### Example 1 — Movie rentals (Exam Q6)

**What is this about:** Two movie rental services charge differently — one has a flat fee plus per-movie cost, the other charges only per movie. You compare total costs for 15 movies.

**Problem:** Movies Plus: $10 fee + $2 per movie. Movies For Less: $3 per movie, no fee. Cost for 15 movies each?

**How to think about it:** Write a cost formula for each plan, then plug in 15 movies. Plan A has a starting fee; Plan B doesn't — but B's per-movie rate is higher.

**Solution (step by step):**
1. Movies Plus: cost = 10 + 2(movies) = 10 + 2(15) = 10 + 30 = **$40**.
2. Movies For Less: cost = 3(movies) = 3(15) = **$45**.
3. Compare: $45 − $40 = **$5 more** for Movies For Less.

**Answer:** **Movies For Less costs $5 more**

**Why this works:** Setting up two separate models and evaluating at the same input lets you compare plans fairly.

### Example 2 — Bank account (Exam Q20)

**What is this about:** Li saves money by depositing a fixed amount each month. You find how many months until she has at least $360.

**Problem:** Li has $125, deposits $45 per month. At least $360 in how many months?

**How to think about it:** "At least $360" means ≥ 360. Write an inequality, solve for m, and **round up** — you can't do a fraction of a month and still hit the goal.

**Solution (step by step):**
1. Model: 125 + 45m ≥ 360.
2. Subtract 125: 45m ≥ 235.
3. Divide: m ≥ 235 ÷ 45 ≈ 5.22.
4. Need a **whole number** of months that meets the goal → **6 months** (5 months gives only 125 + 225 = 350, which is too low).
5. Check: 125 + 45(6) = 395 ≥ 360 ✓

**Answer:** **6 months**

**Why this works:** "At least" problems require rounding **up** to the next whole unit when the answer isn't exact.

### Example 3 — Sarah's craft demo (Exam Q21) ⚠️ Focus

**What is this about:** Sarah's craft demo costs depend on the number of people. You work **backward** to find how many people attended when the total cost was $60.

**Problem:** People → cost: 5→$15, 8→$18, 10→$20, 15→$25. Total cost $60 — how many people?

**How to think about it:** First find the rule connecting people to cost. Notice that cost − people = 10 every time (15 − 5 = 10, 18 − 8 = 10, etc.). So cost = people + 10. Then solve for people when cost = 60.

**Solution (step by step):**
1. Find the pattern: 5 → $15, 8 → $18, 10 → $20, 15 → $25.
2. Check cost − people: 15 − 5 = 10, 18 − 8 = 10, 20 − 10 = 10, 25 − 15 = 10 ✓
3. Equation: **cost = people + 10** (or y = x + 10).
4. Set cost = 60: 60 = x + 10 → x = **50**.

**Answer:** **50 people** (not 30!)

**Why this works:** Finding the equation first prevents guessing — the "+10" base cost is easy to miss if you skip straight to solving.

### Exam-style practice

---

**1. Two phone plans**

Plan A: $20 + $0.10/min. Plan B: $0.25/min. Break-even?

**Problem:** At how many minutes do both plans cost the same?

**How to think about it:** Set the two cost formulas equal and solve for m. Before the break-even point, one plan is cheaper; after it, the other wins.

**Solution (step by step):**
1. Plan A: cost = 20 + 0.10m. Plan B: cost = 0.25m.
2. Set equal: 20 + 0.10m = 0.25m.
3. Subtract 0.10m: 20 = 0.15m.
4. Divide: m = 20 ÷ 0.15 ≈ **133 minutes**.

**Answer:** **About 133 minutes**

---

**2. Inverse: y = 4x + 7, find x when y = 31**

**Problem:** Given y = 31, find x.

**How to think about it:** Plug in y = 31 and solve for x — subtract 7 first, then divide by 4.

**Solution (step by step):**
1. Substitute: 31 = 4x + 7.
2. Subtract 7: 24 = 4x.
3. Divide by 4: **x = 6**.

**Answer:** **x = 6**

### Common Mistakes
- **Q21 trap — guessing 30:** Students sometimes add wrong offsets or divide incorrectly. Always find the equation from the table first, then solve.
- **Rounding down on "at least" problems:** 5.22 months means you need **6** months, not 5 — 5 months doesn't reach the goal.
- **Forgetting the starting fee:** Movies Plus has a $10 fee on top of per-movie cost — don't leave it out.

### Mini Summary
- Write both models from the story, then compare or solve.
- "At least" → inequality, and **round up** when you need whole units.
- For inverse problems: find the rule first, then **isolate x**.
- Parents/teachers: have your student underline what each number in the story represents (fee, rate, total, starting amount) before writing any equation.
''',

    "unit_1_input_output_relationships_lesson_notes.md": '''# Unit 1: Input-Output Relationships — Overview

**What you'll learn:** How to read graphs and tables, decide what is a function, describe how graphs behave, write linear equations, fill in tables, and solve real-world comparison problems — the core of Edgenuity Unit 1.

## Your learning path (do in order)

| Step | Activity | What you'll practice |
|------|----------|----------------------|
| **1** | 📍 Coordinate Plane | Ordered pairs, quadrants, points on axes |
| **2** | 🔀 Relations & Functions | One input → one output; vertical line test |
| **3** | 📈 Graph Behavior | Increasing / decreasing / constant segments |
| **4** | 📊 Linear Equations | Unit rate, y = mx + b from graphs & tables |
| **5** | 📋 Completing Tables | Substitute values; match table to graph |
| **6** | 🌍 Word Problems | Compare plans, “at least” goals, work backward |

## How to use this unit in the app

1. **Read** each activity's notes (diagrams + step-by-step examples).
2. **Quiz** that topic with the 8-question button on the Unit 1 page or at the bottom of each lesson.
3. **Full practice** — 15 mixed questions (with graphs) when you're ready for exam-style review.

## Exam hotspots

- **Function or not?** Same input with two different outputs → **not** a function (Practice Q2 style).
- **Sarah's craft demo / inverse lookup** — find the rule first, then solve (Q21 style).
- **Compare two plans** — write both cost equations, then set them equal or plug in a value.

Enable **Generate with AI** in Week Setup for a brand-new question set every time you practice.
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
