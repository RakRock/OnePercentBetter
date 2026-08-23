#!/usr/bin/env python3
"""One-time builder: writes Edgenuity Unit 2 activity markdown notes. Run: python build_edgenuity_unit2_notes.py"""

from pathlib import Path

NOTES = Path(__file__).resolve().parents[2] / "ArjunEdgenuityCourse3" / "notes" / "unit_2"
NOTES.mkdir(parents=True, exist_ok=True)

ACTIVITIES = {
    "activity_1_slope_rate.md": '''# Activity 1: Slope & Rate of Change

[KEY]
**Slope** = rate of change = **rise ÷ run** = `(y₂ − y₁) ÷ (x₂ − x₁)`.  
In word problems, slope is the **constant rate** (miles per minute, gallons per second, dollars per hour).
[/KEY]

## Quick Review Notes

### Main Idea
**Slope** tells you how steep a line is and how fast one quantity changes compared to another. On a graph, it's **rise ÷ run** — how much y changes divided by how much x changes. In real life, slope is the **rate**: miles per minute, gallons per second, or dollars per hour. Understanding slope helps you compare who's faster, who's saving more, or which plan costs more per unit — skills you'll use in science, sports, and everyday money decisions.

### Key Vocabulary
- **Slope (m):** change in y ÷ change in x
- **Rate of change:** slope in a real-world context
- **Positive slope:** y increases as x increases
- **Negative slope:** y decreases as x increases
- **Direct variation:** proportional; slope = k and line passes through `(0, 0)`

[DIAGRAM:slope_rise_run]

[DIAGRAM:wilson_watering]

### Example 1 — Wilson's watering can (Exam Q1)

**What is this about:** Wilson's watering can leaks water over time. The graph shows how much water is left at different times — you read the starting amount and the leak rate.

**Problem:** Wilson's full watering can loses water over time. The graph shows `(0, 2.5)` and `(4, 1.7)`. Which statement is correct?

**How to think about it:** The point at time 0 tells you how much water Wilson **started with** (the y-intercept). The slope tells you how fast water is **leaving** — negative because the amount is going down.

**Solution (step by step):**
1. At time 0, the graph shows **2.5 gallons** — that's the initial amount in the can.
2. Find the rate (slope): (1.7 − 2.5) ÷ (4 − 0) = −0.8 ÷ 4 = **−0.2 gallons per second**.
3. The negative slope means water is **leaving** the can at 0.2 gal/sec.
4. The question asks about the original amount → **2.5 gallons**.

**Answer:** **The amount of water originally in Wilson's can was 2.5 gallons.**

**Why this works:** The y-value at x = 0 always gives the starting (initial) amount before any change happens.

### Example 2 — Baseball distance vs swing speed (Exam Q6)

**What is this about:** A baseball's travel distance is directly proportional to how fast the bat swings — double the speed, double the distance.

**Problem:** Distance (feet) varies **directly** with swing speed (mph). The graph is proportional through the origin. At 50 mph the ball travels 250 feet. What is the relationship?

**How to think about it:** Direct variation means distance = k × speed for some constant k. Find k by dividing distance by speed at any point.

**Solution (step by step):**
1. Use the known point: 250 feet at 50 mph.
2. Find k: 250 ÷ 50 = **5**.
3. The relationship is **distance = 5 × speed** — every mph of swing speed adds 5 feet of distance.

**Answer:** **The distance is 5 times the swing speed.**

**Why this works:** In direct variation, y/x is always the same constant — here, 5 feet per mph.

### Example 3 — Slope from a table (Exam Q38)

**What is this about:** You have two points in a table and need to pick the correct expression for slope.

**Problem:** A table has `(0, 5)` and `(4, 9)`. Which expression gives the slope?

**How to think about it:** Slope = (change in y) ÷ (change in x). Label the points (x₁, y₁) and (x₂, y₂), then plug into the formula.

**Solution (step by step):**
1. Point 1: (0, 5). Point 2: (4, 9).
2. Slope = (9 − 5) ÷ (4 − 0) = 4 ÷ 4 = **1**.
3. The correct expression is **(9 − 5) ÷ (4 − 0)**.

**Answer:** **(9 − 5) ÷ (4 − 0)**

**Why this works:** Rise ÷ run — subtract y-values for rise, subtract x-values for run.

### Example 4 — Andrew vs Karleigh treadmill (Exam Q7)

**What is this about:** Two people ran on treadmills at different speeds. You compare how far each would go in 60 minutes.

**Problem:**

| Andrew | | Karleigh | |
|--------|---|----------|---|
| Minutes | Miles | Minutes | Miles |
| 18 | 1.5 | 30 | 3 |
| 24 | 2 | 40 | 4 |

Who ran farther in **60 minutes**?

**How to think about it:** Find each person's speed (slope = miles ÷ minutes), then multiply by 60 to project how far they'd go in an hour. Higher speed wins.

**Solution (step by step):**
1. Andrew's rate: (2 − 1.5) ÷ (24 − 18) = 0.5 ÷ 6 = **1/12 mile per minute**.
2. Andrew in 60 min: 60 × 1/12 = **5 miles**.
3. Karleigh's rate: (4 − 3) ÷ (40 − 30) = 1 ÷ 10 = **1/10 mile per minute**.
4. Karleigh in 60 min: 60 × 1/10 = **6 miles**.
5. 6 > 5 → **Karleigh ran farther**.

**Answer:** **Karleigh ran a greater distance** (1/10 mi/min vs 1/12 mi/min).

**Why this works:** Comparing slopes (rates) tells you who is faster; multiplying by time gives total distance.

### Example 5 — Table with slope 2 (Exam Q4)

**What is this about:** Four tables are given and you need to find the one where y increases by 2 for every 1 step in x.

**Problem:** Which table describes a line with slope **2**?

**How to think about it:** Pick any two rows from each table and compute (y₂ − y₁) ÷ (x₂ − x₁). The table where this always equals 2 is the answer.

**Solution (step by step):**
1. Try Table 3: points (−4, 4) and (−2, 8).
2. Slope = (8 − 4) ÷ (−2 − (−4)) = 4 ÷ 2 = **2** ✓
3. Table 3 has slope 2.

**Answer:** **Table 3**

**Why this works:** Slope is the same between any two points on a line — checking one pair is enough if the table is linear.

### Exam-style practice

---

**1. Ladder against a wall (Exam Q37)**

**Problem:** Bottom of ladder is 4 ft from wall; top is 20 ft high. Slope (rise/run)?

**How to think about it:** Rise = vertical height (20 ft). Run = horizontal distance (4 ft). Slope = rise ÷ run.

**Solution (step by step):**
1. Rise = **20 ft** (height on the wall).
2. Run = **4 ft** (distance from wall).
3. Slope = 20 ÷ 4 = **5**.

**Answer:** **5**

---

**2. Constant y in a table (Exam Q35)**

| x | −8 | −4 | 0 | 4 | 8 |
|---|---|---|---|---|---|
| y | 8 | 8 | 8 | 8 | 8 |

**Problem:** What is the slope of this table?

**How to think about it:** y never changes — it's always 8 no matter what x is. That means a flat horizontal line, and horizontal lines have slope zero.

**Solution (step by step):**
1. Check any two rows: y stays at 8 while x changes.
2. Change in y = 8 − 8 = **0**.
3. Slope = 0 ÷ (any run) = **0**.

**Answer:** **Slope is zero**

### Common Mistakes
- **Confusing initial value with rate:** 2.5 gallons is how much Wilson **started with**; 0.2 gal/sec is how fast water **leaves** — don't mix them up.
- **Mixing up rise and run:** Always **(y₂ − y₁) ÷ (x₂ − x₁)** — y on top, x on bottom.
- **Forgetting units:** Wilson's rate is **0.2 gal/sec**, not 2.5 — attach the correct units to slope in word problems.

### Mini Summary
- Slope = **rise ÷ run** = rate of change.
- Compare who is faster by comparing slopes.
- Direct variation: line through **(0, 0)** with constant ratio y/x.
- Parents/teachers: draw a small triangle on the graph (rise and run) to make the division visual before computing.
''',

    "activity_2_y_intercept.md": '''# Activity 2: Y-Intercept & Initial Value

[KEY]
The **y-intercept** is where the line crosses the y-axis (**x = 0**). In word problems it is the **initial value** — the starting amount before any change happens.
[/KEY]

## Quick Review Notes

### Main Idea
The **y-intercept** is the point where a line crosses the y-axis — it's the value of y when x = 0. In real-world problems, it represents the **starting amount**: money in a jar before tips come in, distance already traveled at time zero, or water in a can before it starts leaking. Finding the y-intercept helps you write complete equations and answer "how much did we start with?" questions, which show up often on exams.

### Key Vocabulary
- **Y-intercept:** value of y when x = 0; point `(0, b)`
- **Initial value:** starting output in a real-world model
- **Output for initial value:** the y-value at the start (time 0, before pumping, at opening)

[DIAGRAM:y_intercept_line]

[DIAGRAM:initial_value_table]

### Example 1 — Maricella's line (Exam Q3)

**What is this about:** Maricella draws a line through two points and extends it backward to find where it crosses the y-axis.

**Problem:** Maricella plots `(4, 9)` and `(6, 4)` and extends the segment. Where is the y-intercept?

**How to think about it:** Find the slope first, then walk backward from a known point until x = 0. When you move left in x, reverse the slope's direction on y.

**Solution (step by step):**
1. Slope = (4 − 9) ÷ (6 − 4) = −5 ÷ 2 = **−5/2**.
2. From (4, 9): to reach x = 0, go **4 units left** (run = −4).
3. Change in y = slope × run = (−5/2) × (−4) = **+10**.
4. New y = 9 + 10 = **19** → y-intercept at **(0, 19)**.

**Answer:** **(0, 19)**

**Why this works:** Extending a line backward using slope always lands you on the y-axis at x = 0.

### Example 2 — Tip jar at dry cleaners (Exam Q33)

**What is this about:** A tip jar fills up steadily each hour after the dry cleaners opens. You work backward to find how much was in the jar at opening time.

**Problem:** Hours since opening vs money in tip jar:

| Hours | 4 | 5 | 6 | 7 | 8 |
|-------|---|---|---|---|---|
| $ | 15.50 | 18.25 | 21.00 | 23.75 | 26.50 |

How much was in the jar when the cleaners **opened** (hour 0)?

**How to think about it:** Find how much money is added each hour (the rate), then subtract that amount for each hour you go backward to reach hour 0.

**Solution (step by step):**
1. Rate = 18.25 − 15.50 = **$2.75 per hour**.
2. At hour 4, the jar has $15.50.
3. Backtrack 4 hours: 15.50 − 4(2.75) = 15.50 − 11.00 = **$4.50**.

**Answer:** **$4.50**

**Why this works:** The y-intercept (hour 0) is the starting amount before the hourly rate kicks in.

### Example 3 — Marco pumping gas (Exam Q36)

**What is this about:** Marco pumps gas into his car. The table tracks seconds spent pumping vs gallons added — you find the amount at the very start.

**Problem:** Table shows gallons in Marco's car vs seconds spent pumping. What is the **output for the initial value**?

**How to think about it:** The "initial value" is what you have at time zero — before pumping starts. At 0 seconds, no gas has been pumped yet.

**Solution (step by step):**
1. Initial value means **x = 0** (0 seconds of pumping).
2. At 0 seconds, **0 gallons** have been added in this session.
3. The output at the start is **0 gallons**.

**Answer:** **0 gallons**

**Why this works:** Before any pumping happens, the amount added is zero — that's the initial output for this particular model.

### Example 4 — Nate's road trip (Exam Q12) ⚠️ Focus

**What is this about:** Nate records time and distance on a road trip. He knows his speed and needs a strategy to find how far he had already traveled at the start.

**Problem:** Nate records time and distance. The function is linear with rate **50 miles per hour**. How can he find the **initial value** (starting distance)?

**How to think about it:** If Nate is 50 miles farther for every hour, then going backward one hour means subtracting 50 miles. Repeat until you reach time 0.

**Solution (step by step):**
1. Pick any row in the table (time, distance).
2. The rate is **50 miles per hour**.
3. Work backward: subtract 50 from the distance for each hour you go back.
4. Repeat until time = 0 — that distance is the initial value.

**Answer:** **By repeatedly subtracting 50.**

**Why this works:** Undoing the rate step by step rewinds the trip to its starting point.

### Example 5 — Y-intercept from a graph (Exam Q22)

**What is this about:** You look at a graph and read where the line crosses the y-axis.

**Problem:** A line crosses the y-axis at `(0, 4)`.

**How to think about it:** The y-intercept is always the point where the line hits the vertical y-axis — that's where x = 0. Just read the coordinates.

**Solution (step by step):**
1. Find where the line crosses the **y-axis** (the vertical line at x = 0).
2. Read the coordinates at that crossing point.
3. The line crosses at **(0, 4)**.

**Answer:** **(0, 4)**

**Why this works:** The y-intercept is always the point (0, b) where the line meets the y-axis.

### Example 6 — Student graphs with y-intercept −4 (Exam Q24)

**What is this about:** Four students each draw a line on a graph. You find the one that crosses the y-axis at −4.

**Problem:** Four students graph lines. Which graph crosses the y-axis at **−4**?

**How to think about it:** Look at each graph where x = 0. The line that passes through the point (0, −4) — four units below the origin — is the answer.

**Solution (step by step):**
1. Check each student's graph at **x = 0**.
2. Find the graph whose line passes through **y = −4**.
3. That graph belongs to **Ellis**.

**Answer:** **Ellis**

**Why this works:** The y-intercept is read directly from where the line crosses the y-axis at x = 0.

### Exam-style practice

---

**1. Graph y-intercept and slope (Exam Q5)**

**Problem:** A line has y-intercept **3** and rises 1 unit for every 2 units right. What are the slope and y-intercept?

**How to think about it:** Y-intercept is given directly. "Rises 1 for every 2 right" means slope = rise ÷ run = 1/2.

**Solution (step by step):**
1. Y-intercept = **3** → point (0, 3).
2. Rise = 1, run = 2 → slope = 1 ÷ 2 = **1/2**.
3. Equation would be y = (1/2)x + 3.

**Answer:** **y-intercept is 3; slope is 1/2**

---

**2. Line on grid (Exam Q39)**

**Problem:** Graph shows slope **m = 2** and crosses y-axis at `(0, 4)`. State both values.

**How to think about it:** Read the y-intercept where the line crosses the y-axis. Confirm slope by checking rise ÷ run between any two points.

**Solution (step by step):**
1. Line crosses y-axis at **(0, 4)** → y-intercept = 4.
2. Slope is given as **m = 2**.
3. Equation: y = 2x + 4.

**Answer:** **m = 2, y-intercept (0, 4)**

### Common Mistakes
- **Using x-intercept instead of y-intercept:** (4, 0) is where the line crosses the x-axis — the y-intercept is at x = 0, not y = 0.
- **Adding the rate when working backward:** To find the starting amount, **subtract** the rate for each step back (like the tip jar), don't add.
- **Confusing initial gallons in tank with gallons pumped:** Marco's initial output is 0 gallons **pumped**, not the total gas already in his tank before arriving.

### Mini Summary
- Y-intercept = **starting value** at x = 0.
- From a table: find rate, then step **backward** to x = 0.
- In `y = mx + b`, **b** is the y-intercept.
- Parents/teachers: use the tip-jar example — "If you earn $2.75 per hour and have $15.50 after 4 hours, how much did you start with?"
''',

    "activity_3_direct_variation.md": '''# Activity 3: Direct Variation & Proportional Relationships

[KEY]
**Direct variation** (proportional): `y = kx` — graph passes through **(0, 0)** and `y/x` is always the same constant.  
If the y-intercept is **not 0**, it is linear but **not** proportional.
[/KEY]

## Quick Review Notes

### Main Idea
A **proportional relationship** means two quantities grow and shrink together at a fixed ratio — double the input, double the output. The graph always passes through the origin `(0, 0)`, and the equation looks like **y = kx** with no added constant. This is different from a general linear equation like y = 10x + 20, which has a starting fee. Knowing the difference helps on exams and in real life — like telling apart "pay per hour only" from "base pay plus hourly rate."

### Key Vocabulary
- **Direct variation:** y varies directly with x; `y = kx`
- **Constant of variation:** k = y/x
- **Proportional relationship:** passes through origin; ratios y/x are equal
- **Not proportional:** y = mx + b with **b ≠ 0**

[DIAGRAM:direct_vs_not]

[DIAGRAM:proportional_graph]

### Example 1 — Why Li is incorrect (Exam Q2)

**What is this about:** Li claims a graph shows direct variation, but the line doesn't pass through the origin. You explain why that's wrong.

**Problem:** Li says a graph shows direct variation, but at x = 0 the y-value is **1**. Why is Li wrong?

**How to think about it:** Direct variation requires the graph to go through **(0, 0)** — when x is zero, y must also be zero. If y = 1 at x = 0, there's a starting value that breaks proportionality.

**Solution (step by step):**
1. Direct variation means **y = kx** — no added constant.
2. At x = 0: y = k(0) = **0**, not 1.
3. Li's graph has y = 1 when x = 0 → it does **not** pass through the origin.

**Answer:** **When the x-value is 0, the y-value is 1.**

**Why this works:** Proportional relationships must pass through (0, 0) — any other y-intercept means a starting fee or offset.

### Example 2 — Which table is direct variation? (Exam Q32)

**What is this about:** You pick the table where y/x is always the same number and the relationship would pass through the origin.

**Problem:** Pick the table where y/x is constant and the line would pass through the origin.

**How to think about it:** Divide y by x for each row. If every answer is the same (like always 3), the relationship is y = kx — direct variation.

**Solution (step by step):**
1. Check Table B: x = 4, 6, 8, 10 → y = 12, 18, 24, 30.
2. Compute ratios: 12/4 = 3, 18/6 = 3, 24/8 = 3, 30/10 = 3 ✓
3. All ratios equal **3** → **y = 3x**, which passes through (0, 0).

**Answer:** **Table B**

**Why this works:** Equal y/x ratios across all rows confirm a constant multiplier with no offset.

### Example 3 — Which graph is proportional? (Exam Q31)

**What is this about:** You choose the graph or equation that represents a proportional (direct variation) relationship.

**Problem:** Which representation shows a proportional relationship?

**How to think about it:** Look for a straight line through **(0, 0)** or an equation like **y = 2x** with no "+ constant." If there's a +2 or any added number, it's not proportional.

**Solution (step by step):**
1. Proportional graphs pass through the **origin**.
2. Proportional equations have form **y = kx** only.
3. Reject **y = 2x + 2** — the +2 means the line starts at (0, 2), not (0, 0).

**Answer:** The graph/table with **y = kx** only (through the origin).

**Why this works:** No added constant means zero input gives zero output — the hallmark of proportionality.

### Example 4 — Caleb's earnings (Exam Q30) ⚠️ Focus

**What is this about:** Caleb's weekly earnings depend on hours worked, but he also gets a flat base pay. You decide if this is direct variation.

**Problem:**

| Hours | 12 | 15 | 18 | 21 |
|-------|----|----|----|----|
| Earnings ($) | 140 | 170 | 200 | 230 |

Does this represent direct variation?

**How to think about it:** Check if earnings ÷ hours is always the same. If the ratios differ, there's probably a fixed base pay added on top of hourly wages.

**Solution (step by step):**
1. Check ratios: 140/12 ≈ 11.67, 170/15 ≈ 11.33 — **not equal**.
2. Find the pattern: earnings increase by **$30 per 3 hours** = $10/hour, plus a base.
3. Test: 10(12) + 20 = 140 ✓ → **earnings = 10 × hours + 20**.
4. The **+$20 base** breaks proportionality.

**Answer:** **The ratios of earnings to hours are not the same each week, so the earnings do not vary directly with the hours.**

**Why this works:** The $20 base pay means earnings aren't purely a multiple of hours — it's linear but not proportional.

### Example 5 — Baseball (direct variation context) (Exam Q6)

**What is this about:** Baseball distance varies directly with swing speed — a classic proportional relationship through the origin.

**Problem:** Distance varies directly with swing speed; graph through origin.

**How to think about it:** Find k = distance ÷ speed from any point on the graph. That constant k is the multiplier in y = kx.

**Solution (step by step):**
1. Direct variation: distance = k × speed.
2. From the graph, pick a point (e.g., 50 mph → 250 feet).
3. k = 250 ÷ 50 = **5**.
4. Relationship: **distance = 5 × speed**.

**Answer:** **Distance is 5 times the swing speed.**

**Why this works:** Constant ratio distance/speed confirms direct variation through the origin.

### Exam-style practice

---

**1. Is y = 4x + 7 proportional?**

**Problem:** Does y = 4x + 7 represent a proportional relationship?

**How to think about it:** Plug in x = 0. If y ≠ 0, the line doesn't pass through the origin and it's not proportional.

**Solution (step by step):**
1. At x = 0: y = 4(0) + 7 = **7**.
2. y = 7 ≠ 0 → the line crosses the y-axis at (0, 7).
3. Not proportional — there's an added constant.

**Answer:** **No** — when x = 0, y = 7 ≠ 0.

---

**2. Table check**

| x | 2 | 4 | 6 |
|---|---|---|---|
| y | 5 | 10 | 15 |

**Problem:** Is this table proportional?

**How to think about it:** Check if y/x is the same for every row. If yes, the relationship is y = kx.

**Solution (step by step):**
1. 5/2 = 2.5, 10/4 = 2.5, 15/6 = 2.5 — all equal ✓
2. Constant ratio → **y = 2.5x**.
3. Extended to x = 0: y = 0 → passes through origin → **proportional**.

**Answer:** **Yes — y = 2.5x (proportional)**

### Common Mistakes
- **Thinking constant rate alone means direct variation:** A line can have a steady slope but still have a nonzero y-intercept (like Caleb's $20 base) — that's linear, not proportional.
- **Caleb trap:** **y = 10x + 20** is linear but **not** proportional because of the added $20.
- **Saying "proportional" when the graph misses the origin:** Always verify the line passes through **(0, 0)**.

### Mini Summary
- Direct variation: **y = kx**, through **(0, 0)**, equal ratios y/x.
- **y = mx + b** with b ≠ 0 → linear, not proportional.
- Always check the origin and ratio equality.
- Parents/teachers: ask "If I work zero hours, do I earn zero dollars?" — if not, it's not proportional.
''',

    "activity_4_special_lines.md": '''# Activity 4: Special Lines — Zero & Undefined Slope

[KEY]
**Horizontal line:** y = k → **slope 0** (y does not change).  
**Vertical line:** x = k → **undefined slope** (x does not change; not a function of x).
[/KEY]

## Quick Review Notes

### Main Idea
Not all lines slant up or down — some are perfectly flat and some go straight up and down. A **horizontal** line has **slope zero** because y never changes. A **vertical** line has **undefined slope** because x never changes and you can't divide by zero. These special lines show up on almost every exam, so knowing the difference between "slope 0" and "undefined slope" is essential.

### Key Vocabulary
- **Zero slope:** horizontal line; y = constant
- **Undefined slope:** vertical line; x = constant
- **Positive slope:** rises left to right
- **Negative slope:** falls left to right

[DIAGRAM:horizontal_vertical]

[DIAGRAM:zero_undefined_slope]

### Example 1 — Sanjay's claim (Exam Q9)

**What is this about:** Sanjay says a line with slope zero never touches the x-axis. You find a counterexample that proves him wrong.

**Problem:** Sanjay says a line with **slope zero** never touches the x-axis. Which line proves him wrong?

**How to think about it:** Slope zero means a horizontal line. The x-axis itself is the line **y = 0** — it's horizontal with slope 0 and it **is** the x-axis.

**Solution (step by step):**
1. Slope zero → horizontal line (y = some constant).
2. **y = 0** is a horizontal line at height zero.
3. That line **is** the x-axis — so it "touches" (actually lies on) the x-axis everywhere.

**Answer:** **y = 0**

**Why this works:** y = 0 is the x-axis itself — the ultimate counterexample to Sanjay's claim.

### Example 2 — Line through (9, 30) and (18, 30) (Exam Q10)

**What is this about:** Two points share the same y-value but different x-values — the line between them is horizontal.

**Problem:** What is true about this line?

**How to think about it:** When y stays the same (30) while x changes (9 to 18), the line is flat. Flat lines have slope zero because rise = 0.

**Solution (step by step):**
1. Both points have y = **30** — y doesn't change.
2. x changes from 9 to 18, but y stays constant → **horizontal line**.
3. Slope = (30 − 30) ÷ (18 − 9) = 0 ÷ 9 = **0**.

**Answer:** **It has a slope of zero because the change in the y-values is 0.**

**Why this works:** Zero rise means zero slope — the line is perfectly flat.

### Example 3 — Which equation has slope zero? (Exam Q14)

**What is this about:** You pick the equation of a horizontal line from several options.

**Problem:** Pick the horizontal line.

**How to think about it:** Horizontal lines have the form **y = constant**. Vertical lines look like x = constant. Slanted lines have both x and y in the equation.

**Solution (step by step):**
1. **y = 2** → y is always 2, no matter what x → horizontal ✓
2. `y = −½x + ½` → x has a coefficient → slanted, not horizontal.
3. `x = −5` → vertical line, not horizontal.

**Answer:** **y = 2** (constant y)

**Why this works:** y = k means y never changes — that's the definition of a horizontal line with slope 0.

### Example 4 — Undefined slope (Exam Q28)

**What is this about:** You identify the equation of a vertical line, which has undefined slope.

**Problem:** Which equation represents a line with **undefined** slope?

**How to think about it:** Vertical lines have the form **x = constant**. Their slope is undefined because run = 0 and you can't divide by zero.

**Solution (step by step):**
1. Undefined slope → **vertical line** → x = constant.
2. **x = 0** is a vertical line through the origin.
3. Reject `y = 0` — that's horizontal (slope 0), not undefined.

**Answer:** **x = 0**

**Why this works:** x = k means x never changes — vertical line, undefined slope.

### Example 5 — Which graph line is vertical? (Exam Q29)

**What is this about:** On a graph with several lines, you identify the one that runs straight up and down.

**Problem:** On a graph with lines P, Q, R, S — which has undefined slope?

**How to think about it:** A vertical line has the same x-coordinate at every point. It runs up-down, not left-right.

**Solution (step by step):**
1. Look for the line that goes **straight up and down**.
2. That line has the same x-value everywhere → vertical.
3. Vertical lines have **undefined slope**.

**Answer:** The **vertical** line on the graph.

**Why this works:** Undefined slope always means vertical — no horizontal movement means run = 0.

### Example 6 — True statements about slope (Exam Q34)

**What is this about:** You evaluate several statements about slope and pick the correct one.

**Problem:** Which statement is correct?

**How to think about it:** Remember: vertical = undefined (not zero), horizontal = zero (not undefined), rising left-to-right = positive slope.

**Solution (step by step):**
1. Vertical line → **undefined** slope, not zero ✗
2. Horizontal → slope **0**, not "no slope" ✗
3. Rising left to right → y increases as x increases → **positive slope** ✓

**Answer:** **A line that rises from left to right has a positive slope.**

**Why this works:** Direction of the line determines the sign (or undefined status) of the slope.

### Exam-style practice

---

**1. Slope of y = −3**

**Problem:** What is the slope of the line y = −3?

**How to think about it:** y = −3 means y is always −3 regardless of x — that's a horizontal line.

**Solution (step by step):**
1. y = −3 → y never changes → horizontal line.
2. Horizontal lines have **slope 0**.

**Answer:** **0** (horizontal)

---

**2. Slope of x = 7**

**Problem:** What is the slope of the line x = 7?

**How to think about it:** x = 7 means x is always 7 regardless of y — that's a vertical line.

**Solution (step by step):**
1. x = 7 → x never changes → vertical line.
2. Vertical lines have **undefined slope** (can't divide by zero run).

**Answer:** **Undefined** (vertical)

### Common Mistakes
- **Saying vertical lines have slope 0:** Vertical lines have **undefined** slope — the run is zero, so rise ÷ run is impossible.
- **Saying horizontal lines have "no slope":** Their slope is **0**, not undefined — y does change, it just changes by zero.
- **Confusing y = 0 with x = 0:** y = 0 is horizontal (slope 0); x = 0 is vertical (undefined slope).

### Mini Summary
- **Horizontal** y = k → slope **0**.
- **Vertical** x = k → slope **undefined**.
- Sanjay is wrong: **y = 0** is the x-axis itself — a horizontal line with slope 0.
- Parents/teachers: use a pencil — hold it flat for horizontal (slope 0), stand it upright for vertical (undefined).
''',

    "activity_5_writing_equations.md": '''# Activity 5: Writing Equations of Lines

[KEY]
**Slope-intercept:** `y = mx + b`  
**Point-slope:** `y − y₁ = m(x − x₁)`  
Use slope from two points or a graph, then solve for **b** with any point.
[/KEY]

## Quick Review Notes

### Main Idea
Once you know a line's **slope** and at least **one point**, you can write its equation — and then use that equation to find any missing coordinate. Two main forms are **point-slope** (great when you have a point and slope) and **slope-intercept** (great when you need y = mx + b). This skill connects graphs, tables, and algebra, and it's tested heavily on Edgenuity exams.

### Key Vocabulary
- **Slope-intercept form:** y = mx + b
- **Point-slope form:** y − y₁ = m(x − x₁)
- **Standard form:** Ax + By = C (common in word problems)

[DIAGRAM:equation_from_graph]

[DIAGRAM:point_on_line]

### Example 1 — Slope −3/4 through (−5, 4) (Exam Q13) ⚠️ Focus

**What is this about:** You write the equation of a line when you know its slope and one point it passes through — with a fractional slope that requires careful sign work.

**Problem:** Line has slope **−3/4** and passes through **(−5, 4)**. Find the equation.

**How to think about it:** Start with point-slope form, then simplify to slope-intercept. Watch the signs carefully when x = −5 (so x + 5 appears inside the parentheses).

**Solution (step by step):**
1. Write point-slope: y − 4 = −3/4(x − (−5)) = −3/4(x + 5).
2. Distribute: y − 4 = −3/4 x − 15/4.
3. Add 4 ( = 16/4): y = −3/4 x − 15/4 + 16/4 = **−3/4 x + 1/4**.
4. Check at x = −5: y = 15/4 + 1/4 = 16/4 = 4 ✓

**Answer:** **y = −3/4 x + 1/4** (use point-slope; watch distractors like y = −3/4 x − 2)

**Why this works:** Point-slope form builds the equation directly from slope and one known point.

### Example 2 — Find a on the line (Exam Q15)

**What is this about:** You find the equation from two points, then use it to find a missing x-coordinate when y is known.

**Problem:** Line through **(2, −2)** and **(−6, 2)**. Point **(a, −4)** is on the line. Find **a**.

**How to think about it:** Two points give you slope. Write the equation, plug in y = −4, and solve for x (which is a).

**Solution (step by step):**
1. Slope = (2 − (−2)) ÷ (−6 − 2) = 4 ÷ (−8) = **−1/2**.
2. Point-slope from (2, −2): y − (−2) = −1/2(x − 2) → y + 2 = −1/2(x − 2).
3. Plug in y = −4: −4 + 2 = −1/2(x − 2) → −2 = −1/2(x − 2).
4. Multiply both sides by −2: 4 = x − 2 → **x = 6** → **a = 6**.

**Answer:** **a = 6**

**Why this works:** Any point on the line must satisfy the line's equation — substitute and solve.

### Example 3 — Y-intercept from standard form (Exam Q25)

**What is this about:** An equation is given in standard form and you find the y-intercept by setting x = 0.

**Problem:** What is the y-intercept of **x − 4y = −6**?

**How to think about it:** Y-intercept is where x = 0. Plug x = 0 into the equation and solve for y.

**Solution (step by step):**
1. Set x = 0: 0 − 4y = −6.
2. Solve: −4y = −6 → y = 6/4 = **3/2**.
3. Y-intercept = point **(0, 3/2)**.

**Answer:** **3/2** (or (0, 3/2))

**Why this works:** The y-intercept is always found by setting x = 0 in any form of the equation.

### Example 4 — Slope from graph points (Exam Q27)

**What is this about:** You calculate slope from two points that are clearly marked on a graph.

**Problem:** Line passes through **(0, 2)** and **(−4, 0)** on a graph. Slope?

**How to think about it:** Use (y₂ − y₁) ÷ (x₂ − x₁). Order doesn't matter as long as you're consistent.

**Solution (step by step):**
1. Point 1: (0, 2). Point 2: (−4, 0).
2. Slope = (0 − 2) ÷ (−4 − 0) = −2 ÷ (−4) = **1/2**.

**Answer:** Use **(0 − 2) ÷ (−4 − 0)** or equivalent → **1/2**

**Why this works:** Rise ÷ run between any two points on a line always gives the same slope.

### Example 5 — Ava's slope expression (Exam Q34)

**What is this about:** Ava computes slope as (3 − 1) ÷ (4 − (−2)) and you find the matching table.

**Problem:** Ava uses `(3 − 1) ÷ (4 − (−2))` for slope. Which table fits?

**How to think about it:** Compute Ava's slope first, then find the table where y changes by that amount per step in x.

**Solution (step by step):**
1. Ava's slope = (3 − 1) ÷ (4 − (−2)) = 2 ÷ 6 = **1/3**.
2. Look for a table where y increases by 1 for every 3 increase in x.
3. That table has constant rate **1/3**.

**Answer:** The table whose rows match slope **1/3**.

**Why this works:** Slope must be the same between every pair of points in a linear table.

### Exam-style practice

---

**1. Write y = mx + b through (0, −2) and (4, 2)**

**Problem:** Find the equation of the line through (0, −2) and (4, 2).

**How to think about it:** (0, −2) gives you the y-intercept directly. Use the other point to find slope.

**Solution (step by step):**
1. Y-intercept: (0, −2) → **b = −2**.
2. Slope = (2 − (−2)) ÷ (4 − 0) = 4 ÷ 4 = **1**.
3. Equation: **y = x − 2**.

**Answer:** **y = x − 2**

---

**2. Horizontal through (9, 30)**

**Problem:** Write the equation of a horizontal line through (9, 30).

**How to think about it:** Horizontal means y stays the same everywhere. The y-value of the given point is 30.

**Solution (step by step):**
1. Horizontal line → y = constant.
2. The point has y = 30.
3. Equation: **y = 30**.

**Answer:** **y = 30**

### Common Mistakes
- **Plugging x into b and y into m:** To find b, use **b = y − mx** with a known point.
- **Sign errors with −3/4 and negative x-coordinates:** x − (−5) becomes x + 5 — watch the double negative.
- **Using x = −5 as an answer:** x = k is a vertical line, not an equation with a numeric slope.

### Mini Summary
- Two points → slope → point-slope → **y = mx + b**.
- To find a missing x or y, **substitute** into your equation.
- Standard form: set **x = 0** for y-intercept, **y = 0** for x-intercept.
- Parents/teachers: after writing the equation, pick a point and verify together by substitution.
''',

    "activity_6_linear_modeling.md": '''# Activity 6: Linear Modeling & Word Problems

[KEY]
Translate words into **Ax + By = C** or **y = mx + b**. Define variables clearly, use coefficients as unit prices/rates, and solve for the quantity asked.
[/KEY]

## Quick Review Notes

### Main Idea
Real situations — food sales, phone bills, tip jars — become linear equations once you define your variables and match coefficients to prices or rates. The hardest part is usually **translation**: figuring out what x and y stand for and which number is the price, rate, or total. Once the equation is set up, solving is straightforward. This activity ties together everything from Unit 2.

### Key Vocabulary
- **Standard form model:** Ax + By = C (A, B = rates; C = total)
- **Revenue:** (price) × (quantity) summed
- **Hourly rate:** slope on a bill-vs-hours graph
- **Initial fee + per-unit cost:** y = mx + b

[DIAGRAM:shake_shack_model]

[DIAGRAM:brenda_phone_bill]

### Example 1 — Shake Shack shakes (Exam Q8)

**What is this about:** A restaurant sells two sizes of shakes at different prices. You write an equation for total Sunday revenue.

**Problem:** Small shake **$3**, large shake **$5**. Sunday revenue **$479**.  
x = number of **small** shakes, y = number of **large** shakes. Write the equation.

**How to think about it:** Total revenue = (price of small)(number of small) + (price of large)(number of large). Match each price to the correct variable.

**Solution (step by step):**
1. x = small shakes at **$3** each → contributes **3x** dollars.
2. y = large shakes at **$5** each → contributes **5y** dollars.
3. Total revenue = $479 → **3x + 5y = 479**.

**Answer:** **3x + 5y = 479**

**Why this works:** Each coefficient is the unit price for its variable — multiply price × quantity and add for total.

### Example 2 — Pretzels and popcorn (Exam Q11)

**What is this about:** You're given an equation and must match it to the correct real-world story about snack prices.

**Problem:** Which story matches **2.75x + 3.25y = 215**?

**How to think about it:** Coefficients are prices: x-items cost $2.75, y-items cost $3.25. Total is $215. The higher price ($3.25) belongs to the more expensive item (pretzels, which cost 75¢ more).

**Solution (step by step):**
1. x items cost **$2.75** each; y items cost **$3.25** each.
2. Total sales = **$215**.
3. Pretzels cost 75¢ more than popcorn → popcorn = $2.75 (x), pretzels = $3.25 (y).

**Answer:** **Pretzels cost 75 cents more than popcorn bags. x = popcorn bags, y = pretzels. Total $215.**

**Why this works:** Matching coefficients to the correct items and prices makes the story fit the equation.

### Example 3 — Brenda's cell phone bill (Exam Q20)

**What is this about:** Brenda's phone bill depends on hours used. You read the hourly rate from a graph.

**Problem:** Graph shows Brenda's monthly bill vs hours used. What is her **hourly rate**?

**How to think about it:** The hourly rate is the **slope** — change in dollars per change in hours. Pick two clear points on the line and compute rise ÷ run.

**Solution (step by step):**
1. Pick two points on the graph, e.g., (0, base) and (h, bill).
2. Slope = (change in bill) ÷ (change in hours).
3. That slope is the **hourly rate** (e.g., **$12 per hour** if the bill rises $12 for each 1 hour).

**Answer:** Read the **slope** from the graph (e.g. **$12 per hour** if the line rises $12 for each 1 hour).

**Why this works:** On a cost-vs-hours graph, slope always represents the per-hour charge.

### Example 4 — Caleb's pay (linear but not proportional) (Exam Q30)

**What is this about:** Caleb earns hourly pay plus a base amount. You determine whether this is direct variation.

**Problem:** Earnings = **10 × hours + 20**. Is this direct variation?

**How to think about it:** Direct variation has no added constant. The +20 is a flat base pay that breaks proportionality.

**Solution (step by step):**
1. Equation: earnings = 10h + 20.
2. The **+20** means even at 0 hours, earnings would be $20 — not zero.
3. This is **y = mx + b** with b = 20 ≠ 0 → linear but **not proportional**.

**Answer:** **Not direct variation** because of the added $20.

**Why this works:** Any added constant (base pay, starting fee) means the relationship isn't purely proportional.

### Example 5 — Tip jar rate (Exam Q33)

**What is this about:** Tips grow at a steady hourly rate. You find the starting amount in the jar at opening.

**Problem:** Tips grow **$2.75 per hour** after opening. At hour 4 there is **$15.50**. Starting amount?

**How to think about it:** Work backward from hour 4 to hour 0 by subtracting $2.75 for each hour.

**Solution (step by step):**
1. Rate = **$2.75 per hour**.
2. At hour 4: **$15.50** in the jar.
3. Backtrack 4 hours: 15.50 − 4(2.75) = 15.50 − 11.00 = **$4.50**.

**Answer:** **$4.50** in the jar at opening.

**Why this works:** Subtracting the hourly rate for each hour backward reveals the initial amount at time zero.

### Exam-style practice

---

**1. T-shirts $8, hats $12, total sales $200**

**Problem:** Write an equation for total sales of t-shirts and hats.

**How to think about it:** Define variables, then multiply each price by its quantity and set the sum equal to the total.

**Solution (step by step):**
1. Let x = t-shirts ($8 each), y = hats ($12 each).
2. Revenue from shirts: **8x**. Revenue from hats: **12y**.
3. Total = $200 → **8x + 12y = 200**.

**Answer:** **8x + 12y = 200**

---

**2. Plan: $25 monthly fee + $0.15 per text**

**Problem:** Write an equation for total cost with a monthly fee plus per-text charge.

**How to think about it:** Monthly fee is the y-intercept (starting cost). Per-text charge is the slope (rate).

**Solution (step by step):**
1. Let x = number of texts, y = total cost.
2. Starting fee = **$25** (y-intercept).
3. Per-text rate = **$0.15** (slope).
4. Equation: **y = 0.15x + 25**.

**Answer:** **y = 0.15x + 25** (x texts, y total cost)

### Common Mistakes
- **Shake Shack trap:** Swapping **3 and 5** or writing **5x + 3y** when x is defined as **small** shakes ($3).
- **Pretzels/popcorn:** Matching **2.75 to pretzels** when it's the **lower** price (popcorn).
- **Brenda:** Reading the **y-intercept** (base fee) when the question asks for **hourly rate** (slope).

### Mini Summary
- Define variables first; match coefficients to prices/rates.
- Total revenue → **(price₁)(qty₁) + (price₂)(qty₂) = total**.
- Graph models: **slope = rate**, **y-intercept = starting fee**.
- Parents/teachers: have your student write "x = ___, y = ___" and label each coefficient with its meaning before building the equation.
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
