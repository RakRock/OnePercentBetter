#!/usr/bin/env python3
"""One-time builder: writes Edgenuity Unit 6 activity markdown notes. Run: python build_edgenuity_unit6_notes.py"""

from pathlib import Path

NOTES = Path(__file__).parent / "ArjunEdgenuityCourse3" / "notes" / "unit_6"
NOTES.mkdir(parents=True, exist_ok=True)

ACTIVITIES = {
    "activity_1_graphing_solutions.md": '''# Activity 1: Graphing Systems of Equations

[KEY]
A **system of linear equations** is two (or more) lines on the same graph.  
The **solution** is the **ordered pair (x, y)** where the lines **intersect** — the point that satisfies **both** equations.  
Graph each line (slope-intercept, table, or intercepts), then read the intersection.
[/KEY]

## Quick Review Notes

### Main Idea
Each equation is a line. Where they cross is the one (x, y) that makes both equations true. If a table is given for one line, plot those points and graph the second equation to find where they meet.

### Key Vocabulary
- **System of equations:** two or more equations with the same variables
- **Solution (ordered pair):** (x, y) that satisfies every equation in the system
- **Intersection point:** where two lines cross on a graph
- **Consistent system:** at least one solution (one point, or infinitely many on the same line)

[DIAGRAM:system_intersection]

[DIAGRAM:graph_table_system]

### Example 1 — y = ½x − 3 and y = −x (Exam focus)

**Problem:** Graph **y = ½x − 3** and **y = −x**. What is the solution?

**Solution:**
- Line 1: slope **½**, y-intercept **−3**
- Line 2: slope **−1**, passes through origin
- They intersect at **(2, −2)** — check: ½(2) − 3 = −2 ✓ and −(2) = −2 ✓

**Answer:** **(2, −2)**

### Example 2 — Table for y = −x plus graph y = ½x − 3

**Problem:** A table shows **y = −x** with points (0, 0), (1, −1), (2, −2). Line 2 is **y = ½x − 3**. Find the solution.

**Solution:**
- Plot table points for **y = −x**
- Graph **y = ½x − 3** using slope ½ from (0, −3)
- Both lines pass through **(2, −2)**

**Answer:** **(2, −2)**

### Example 3 — Read intersection from graph

**Problem:** A graph shows two lines crossing at (−1, 4). What is the solution of the system?

**Solution:**
- The intersection **is** the solution

**Answer:** **(−1, 4)**

### Example 4 — Which point is NOT on both lines?

**Problem:** System: **y = 2x + 1** and **y = −x + 7**. Is **(2, 5)** a solution?

**Solution:**
- Line 1: 2(2) + 1 = **5** ✓
- Line 2: −(2) + 7 = **5** ✓
- Yes — (2, 5) is on **both** lines

**Answer:** **(2, 5) is a solution**

### Example 5 — Graph by intercepts

**Problem:** Graph **2x + y = 6** and **x − y = 2**.

**Solution:**
- **2x + y = 6:** (0, 6) and (3, 0)
- **x − y = 2:** (0, −2) and (2, 0)
- Intersection: **(8/3, 2/3)** or read from graph

**Answer:** Solve algebraically or read **(8/3, 2/3)** from the graph

### Example 6 — Adam fertilizer system (preview)

**Problem:** **y = ¼x** and **x + y = 10** — find the solution by graphing.

**Solution:**
- **y = ¼x** through origin, slope ¼
- **x + y = 10** → y = −x + 10, y-intercept 10, slope −1
- Intersection: **(8, 2)** — ¼(8) = 2 ✓ and 8 + 2 = 10 ✓

**Answer:** **(8, 2)**

### Exam-style practice

---

**1. Lines cross at (3, 1). Solution?**

**Solution:** **(3, 1)**

---

**2. y = x + 2 and y = −2x + 5. Graph and find intersection.**

**Solution:** Set equal: x + 2 = −2x + 5 → 3x = 3 → **(1, 3)**

---

**3. Table gives (0, −3), (2, −2), (4, −1) on one line; second line y = −x. Solution?**

**Solution:** Point **(2, −2)** appears on both → **(2, −2)**

### Common Mistakes
- Reading the **wrong** intersection when more than two lines are on the graph.
- Using a point that lies on **only one** line (check **both** equations).
- Confusing **x** and **y** when writing the ordered pair — always **(x, y)**.

### Mini Summary
- **Solution = intersection point** of the lines.
- **y = ½x − 3** and **y = −x** → **(2, −2)**.
- Tables + graphs: plot table points, draw the other line, read where they meet.
''',

    "activity_2_slope_intercept.md": '''# Activity 2: Slope-Intercept Form

[KEY]
**Slope-intercept form:** **y = mx + b** — **m** = slope, **b** = y-intercept.  
To graph a system easily, rewrite each equation as **y = mx + b**.  
From **standard form** Ax + By = C: isolate y (move x-term, divide by B).
[/KEY]

## Quick Review Notes

### Main Idea
Systems are easier to graph when both equations are in y = mx + b. Convert standard form by solving for y. Once you have m and b, plot the y-intercept and use the slope.

### Key Vocabulary
- **Slope (m):** rise over run; change in y / change in x
- **y-intercept (b):** where the line crosses the y-axis (x = 0)
- **Standard form:** Ax + By = C
- **Equivalent form:** same line, different equation (e.g., 5x − 2y = 10 and y = ⁵⁄₂x − 5)

[DIAGRAM:convert_to_slope_intercept]

[DIAGRAM:slope_intercept_form]

### Example 1 — 5x − 2y = 10 → y = ⁵⁄₂x − 5 (Exam focus)

**Problem:** Write **5x − 2y = 10** in slope-intercept form.

**Solution:**
```
5x − 2y = 10
−2y = −5x + 10
y = (5/2)x − 5
```

**Answer:** **y = ⁵⁄₂x − 5** (slope **⁵⁄₂**, y-intercept **−5**)

### Example 2 — Identify slope-intercept form

**Problem:** Which equation is already in **y = mx + b**?

**Solution:**
- **A.** 3x + 2y = 8 → standard form
- **B.** y = −3x + 5 → **slope-intercept** ✓
- **C.** x = 4 → vertical line (not y = mx + b)
- **D.** 2x − y = 7 → standard form

**Answer:** **y = −3x + 5**

### Example 3 — Convert x + y = 10

**Problem:** Rewrite **x + y = 10** as y = mx + b.

**Solution:**
```
y = −x + 10
```
Slope **−1**, y-intercept **10**

**Answer:** **y = −x + 10**

### Example 4 — Graph y = ¼x and y = −x + 10 (Adam system)

**Problem:** Adam uses **y = ¼x** pounds of fertilizer per **x** pounds of seeds, and **x + y = 10** total pounds. Write both in slope-intercept form and identify slopes.

**Solution:**
- Equation 1: **y = ¼x** → m = ¼, b = 0
- Equation 2: **y = −x + 10** → m = −1, b = 10

**Answer:** **y = ¼x** and **y = −x + 10**; solution **(8, 2)**

### Example 5 — Compare slopes: parallel check

**Problem:** Are **y = −3x + 5** and **y = −3x − 6** the same line?

**Solution:**
- Same slope **−3**, different y-intercepts (**5** vs **−6**)
- **Parallel** — different lines

**Answer:** **No** — parallel lines (same slope, different intercepts)

### Example 6 — 2x + 3y = 12

**Problem:** Solve **2x + 3y = 12** for y.

**Solution:**
```
3y = −2x + 12
y = (−2/3)x + 4
```

**Answer:** **y = −⅔x + 4**

### Example 7 — Which line has y-intercept −3?

**Problem:** Pick the equation with **b = −3**.

**Solution:**
- **y = ½x − 3** has y-intercept **−3** ✓
- y = ½x + 3 has b = 3

**Answer:** **y = ½x − 3**

### Exam-style practice

---

**1. 4x − y = 8 → slope-intercept?**

**Solution:** **y = 4x − 8**

---

**2. Slope of y = ⁵⁄₂x − 5?**

**Solution:** **m = ⁵⁄₂**

---

**3. y = −2x − 8 vs y = −(2x + 8). Same line?**

**Solution:** y = −(2x + 8) = **−2x − 8** → **same equation** → infinitely many solutions.

### Common Mistakes
- Forgetting to **divide every term** when isolating y (5x − 2y = 10 trap).
- Sign errors: **−2y = −5x + 10** → y = **(5/2)x − 5**, not +5.
- Thinking **x + y = 10** is slope-intercept (y must be **alone** on the left).

### Mini Summary
- **5x − 2y = 10** → **y = ⁵⁄₂x − 5**.
- **y = mx + b:** m = slope, b = y-intercept.
- Convert standard form **before** graphing systems.
''',

    "activity_3_word_problems.md": '''# Activity 3: Word Problems → Systems

[KEY]
**Step 1:** Define variables (x = smaller number, x = apples, etc.).  
**Step 2:** Write **two** independent equations from the story.  
**Step 3:** Graph or solve — the answer must satisfy **both** equations.
[/KEY]

## Quick Review Notes

### Main Idea
Most system word problems give two facts about the same two unknowns. Translate each sentence into an equation. Mixture/cost problems often use “total amount” plus “total value.”

### Key Vocabulary
- **Two-number problems:** sum, difference, multiples
- **Mixture / cost:** quantity equation + value equation
- **Comparison:** “twice as many,” “$4 per rental,” fixed fees

[DIAGRAM:word_to_equations]

[DIAGRAM:real_world_system]

### Example 1 — Two numbers (Exam focus)

**Problem:** Four times the smaller number plus three times the larger number is **31**. The larger minus **7** equals **twice** the smaller. Find the numbers.

**Solution:**
Let **s** = smaller, **L** = larger.
```
4s + 3L = 31
L − 7 = 2s   →   L = 2s + 7
```
Substitute: 4s + 3(2s + 7) = 31 → 10s + 21 = 31 → s = 1, L = 9

**Answer:** **Smaller = 1, Larger = 9**; system: **4s + 3L = 31** and **L − 7 = 2s**

### Example 2 — Kedwin movies (Exam focus)

**Problem:** Kedwin can watch movies online for a **$10** flat fee, or rent **5 movies for $4** at a store (plus no flat fee for the first comparison — online $10 total vs $4 for 5 rentals). After how many movies **m** is the cost the same?

**Solution:**
```
Online:  C = 10        (flat $10 for unlimited / subscription style)
Rental:  C = (4/5)m    ($4 for 5 movies → $0.80 per movie)
```
Set equal: 10 = (4/5)m → m = 12.5 — or compare total cost formulas as given in the problem.

**Answer:** System: **y = 10** and **y = (4/5)x** (interpret variables from context); break-even depends on exact wording — **set costs equal**.

### Example 3 — Adam fertilizer (Exam focus)

**Problem:** Adam uses **¼** as much fertilizer **y** (lb) as seeds **x** (lb): **y = ¼x**. Total mix is **10** lb: **x + y = 10**. How many pounds of each?

**Solution:**
```
y = ¼x
x + y = 10
x + ¼x = 10 → (5/4)x = 10 → x = 8, y = 2
```

**Answer:** **8 lb seeds, 2 lb fertilizer**; solution **(8, 2)**

### Example 4 — Aisha apples and oranges (Exam focus)

**Problem:** Aisha buys **x** apples and **y** oranges. Total fruit: **15**. Apples **$0.50**, oranges **$0.65**; total cost **$9**.

**Solution:**
```
x + y = 15
0.5x + 0.65y = 9
```
From first: x = 15 − y. Substitute: 0.5(15 − y) + 0.65y = 9 → 0.15y = 1.5 → y = 10, x = 5

**Answer:** **5 apples, 10 oranges**; system: **x + y = 15** and **0.5x + 0.65y = 9**

### Example 5 — Babysitting rates

**Problem:** Maria charges **$8/hr** plus **$5** travel. Jake charges **$10/hr** flat. After how many hours **h** is the cost equal?

**Solution:**
```
Maria:  C = 8h + 5
Jake:   C = 10h
8h + 5 = 10h → h = 2.5
```

**Answer:** **2.5 hours**; system **y = 8x + 5** and **y = 10x**

### Example 6 — Write the system only

**Problem:** The sum of two numbers is **20**. One number is **3 more** than twice the other.

**Solution:**
Let x = first, y = second.
```
x + y = 20
y = 2x + 3
```

**Answer:** **x + y = 20** and **y = 2x + 3**

### Exam-style practice

---

**1. Tickets: $5 adult, $3 child; 12 people, $48 total.**

**Solution:** **a + c = 12** and **5a + 3c = 48**

---

**2. Two numbers: sum 50, difference 6.**

**Solution:** **x + y = 50** and **x − y = 6**

---

**3. y = ¼x and x + y = 10. Find x.**

**Solution:** **x = 8**

### Common Mistakes
- Writing **one** equation with **two** unknowns and stopping.
- Swapping coefficients in “four times smaller + three times larger” (use **4s + 3L**, not 3s + 4L).
- Mixing **cents** and **dollars** in cost problems (Aisha: keep 0.5 and 0.65 in dollars).

### Mini Summary
- Two facts → **two equations**.
- **4s + 3L = 31** and **L − 7 = 2s** → smaller **1**, larger **9**.
- **Adam:** **y = ¼x**, **x + y = 10** → **(8, 2)**.
- **Aisha:** **x + y = 15**, **0.5x + 0.65y = 9** → **5 apples, 10 oranges**.
''',

    "activity_4_number_of_solutions.md": '''# Activity 4: Number of Solutions in a System

[KEY]
**One solution:** lines intersect at **one point** (different slopes).  
**No solution:** **parallel** lines — same slope, **different** y-intercepts.  
**Infinitely many:** **same line** — equations are equivalent (same slope **and** same intercept).
[/KEY]

## Quick Review Notes

### Main Idea
Compare slopes and y-intercepts after writing both equations as y = mx + b. Different slopes → one crossing point. Same slope, different intercepts → parallel (never meet). Same slope and same intercept → one line drawn twice.

### Key Vocabulary
- **Parallel lines:** equal slopes, no intersection (in a plane)
- **Coincident lines:** same line — every point on the line is a solution
- **Inconsistent system:** no solution (parallel)
- **Dependent system:** infinitely many solutions (same line)

[DIAGRAM:parallel_lines]

[DIAGRAM:infinite_solutions]

### Example 1 — Parallel: y = −3x + 5 and y = −3x − 6 (Exam focus)

**Problem:** How many solutions does the system **y = −3x + 5** and **y = −3x − 6** have?

**Solution:**
- Both slopes **−3**
- y-intercepts **5** and **−6** — **different**
- Lines are **parallel** → **never intersect**

**Answer:** **Zero solutions (no solution)**

### Example 2 — Infinite: y = −2x − 8 and y = −(2x + 8) (Exam focus)

**Problem:** How many solutions for **y = −2x − 8** and **y = −(2x + 8)**?

**Solution:**
```
y = −(2x + 8) = −2x − 8
```
Second equation **is the same** as the first → **same line**

**Answer:** **Infinitely many solutions**

### Example 3 — One solution

**Problem:** **y = ½x − 3** and **y = −x** — how many solutions?

**Solution:**
- Slopes **½** and **−1** — **different**
- Lines cross at **(2, −2)**

**Answer:** **Exactly one solution: (2, −2)**

### Example 4 — Standard form parallel check

**Problem:** Are **2x + 4y = 8** and **x + 2y = 5** the same line?

**Solution:**
- First: y = −½x + 2
- Second: y = −½x + 2.5
- Same slope, different intercepts → **parallel**, **no solution**

**Answer:** **No solution** (not the same line)

### Example 5 — Coincident from standard form

**Problem:** **3x − y = 4** and **−6x + 2y = −8** — number of solutions?

**Solution:**
- Second equation: divide by −2 → **3x − y = 4** — identical to first

**Answer:** **Infinitely many solutions**

### Example 6 — Graph interpretation

**Problem:** A graph shows two lines that never meet. What can you conclude?

**Solution:**
- **Parallel lines** → **no solution** to the system

**Answer:** **Zero solutions**

### Example 7 — Which system has no solution?

**Problem:** Pick the system with **no** solution.

**Solution:**
- **A.** y = 2x + 1 and y = 2x − 3 → same slope 2, different b → **no solution** ✓
- **B.** y = x and y = −x → one solution
- **C.** y = 3x and y = 3x → infinite

**Answer:** **y = 2x + 1 and y = 2x − 3**

### Exam-style practice

---

**1. y = 4x + 1 and y = 4x + 1**

**Solution:** **Infinitely many** (same line).

---

**2. y = −x + 10 and y = 2x + 1**

**Solution:** Different slopes → **one solution**.

---

**3. y = −3x + 5 and y = −3x − 6**

**Solution:** **No solution** (parallel).

### Common Mistakes
- Seeing **same slope** and assuming **infinite** solutions — must also match **y-intercept**.
- Forgetting **y = −(2x + 8)** distributes to **−2x − 8** (infinite-solutions trap).
- Confusing **no solution** with **one solution** when lines look close on a small graph.

### Mini Summary
- **Different slopes** → **one** solution.
- **Same slope, different b** → **parallel** → **0** solutions (**y = −3x + 5**, **y = −3x − 6**).
- **Same line** → **∞** solutions (**y = −2x − 8** and **y = −(2x + 8)**).
''',

    "activity_5_identify_from_graph.md": '''# Activity 5: Identify Systems from Graphs

[KEY]
Match a graph to equations by checking **slope** and **y-intercept** of each line.  
Given a **solution point**, find the system where **both** lines pass through that point.  
With **four lines** on one graph, pair the correct two lines that intersect at the target point.
[/KEY]

## Quick Review Notes

### Main Idea
Work line by line: identify m and b from the graph or from slope-intercept form. To verify a solution point, substitute into both equations. When four lines appear, eliminate lines that do not go through the required point.

### Key Vocabulary
- **Solution point test:** plug (x, y) into both equations
- **Line identification:** slope from rise/run; y-intercept where x = 0
- **System matching:** pair of equations whose graphs intersect at the given point

[DIAGRAM:four_lines_graph]

[DIAGRAM:match_system_graph]

### Example 1 — Four lines on one graph (Exam focus)

**Problem:** A graph shows four lines labeled W, X, Y, Z. Which **system** has solution **(2, −2)**?

**Solution:**
- Test **(2, −2)** on each pair:
- **y = ½x − 3:** ½(2) − 3 = −2 ✓
- **y = −x:** −(2) = −2 ✓
- Lines with slopes **½** and **−1** through **(2, −2)** form the correct system

**Answer:** System **y = ½x − 3** and **y = −x**

### Example 2 — Match graph to y = ⁵⁄₂x − 5

**Problem:** Which graph shows **5x − 2y = 10**?

**Solution:**
- Rewrite: **y = ⁵⁄₂x − 5**
- y-intercept **−5**, slope **⁵⁄₂** (rise 5, run 2)

**Answer:** Line through **(0, −5)** with steep positive slope

### Example 3 — Which system has solution (8, 2)?

**Problem:** Find the system with solution **(8, 2)**.

**Solution:**
- **y = ¼x:** ¼(8) = 2 ✓
- **x + y = 10:** 8 + 2 = 10 ✓

**Answer:** **y = ¼x** and **x + y = 10** (Adam fertilizer)

### Example 4 — Point (−3, 5) on both lines

**Problem:** Betty claims **(−3, 5)** satisfies her system. Equations: **y = −2x − 1** and **y = x + 8**. Is she correct?

**Solution:**
- Line 1: −2(−3) − 1 = 6 − 1 = **5** ✓
- Line 2: −3 + 8 = **5** ✓

**Answer:** **Yes** — **(−3, 5)** is the solution

### Example 5 — Pick the wrong line

**Problem:** Solution should be **(1, 9)**. One equation is **y = 2x + 7**. Does (1, 9) work?

**Solution:**
- 2(1) + 7 = **9** ✓ — point is on this line; need second line through (1, 9) as well

**Answer:** **(1, 9)** lies on **y = 2x + 7**; match with another line through the same point

### Example 6 — Parallel lines on graph

**Problem:** Two lines on the graph have the same slope but different y-intercepts. How many solutions?

**Solution:**
- **Parallel** → **no solution**

**Answer:** **Zero solutions**

### Example 7 — Aisha system from context

**Problem:** Graph shows **x + y = 15** (y = −x + 15) and **0.5x + 0.65y = 9**. Where do they cross?

**Solution:**
- Solve: **(5, 10)** — 5 apples, 10 oranges

**Answer:** **(5, 10)** or **(x, y) = (5, 10)**

### Exam-style practice

---

**1. Lines cross at (4, 3). Which ordered pair is the solution?**

**Solution:** **(4, 3)**

---

**2. Point (2, −2) — which pair of slopes could form the system?**

**Solution:** **m = ½** and **m = −1** (y = ½x − 3 and y = −x)

---

**3. Four lines; only two pass through (−3, 5). That pair is the system.**

**Solution:** Identify those two lines (Betty: **y = −2x − 1**, **y = x + 8**)

### Common Mistakes
- Matching a line by **color** only without checking **slope and intercept**.
- Using a point that satisfies **one** equation but not the other.
- Picking two lines that intersect at a **different** point than asked.

### Mini Summary
- Read **m** and **b** from graphs or **y = mx + b**.
- **(2, −2)** → **y = ½x − 3** and **y = −x**.
- **(8, 2)** → **y = ¼x** and **x + y = 10**.
- **Betty (−3, 5)** satisfies **y = −2x − 1** and **y = x + 8**.
''',

    "activity_6_checking_solutions.md": '''# Activity 6: Checking Solutions by Substitution

[KEY]
An ordered pair **(x, y)** is a solution only if it makes **both** equations **true**.  
**Substitute** x and y into **each** equation.  
If one equation fails, the point is **not** a solution — find Dimitri-style arithmetic or sign errors.
[/KEY]

## Quick Review Notes

### Main Idea
Always verify by plugging in. For error analysis, repeat the student’s substitution step by step and locate where the arithmetic or sign first goes wrong.

### Key Vocabulary
- **Substitution check:** replace x and y with the pair’s values
- **True statement:** correct solution for that equation (e.g., 5 = 5)
- **False statement:** point is not on that line
- **Error analysis:** compare student work to correct substitution

[DIAGRAM:substitution_check]

[DIAGRAM:verify_solution]

### Example 1 — Betty (−3, 5) (Exam focus)

**Problem:** Is **(−3, 5)** a solution to **y = −2x − 1** and **y = x + 8**?

**Solution:**
```
Eq 1:  y = −2(−3) − 1 = 6 − 1 = 5  ✓
Eq 2:  y = −3 + 8 = 5               ✓
```

**Answer:** **Yes — (−3, 5) is a solution**

### Example 2 — Check (2, −2) for y = ½x − 3 and y = −x

**Problem:** Verify **(2, −2)**.

**Solution:**
```
y = ½(2) − 3 = 1 − 3 = −2  ✓
y = −(2) = −2               ✓
```

**Answer:** **(2, −2) is a solution**

### Example 3 — (8, 2) for Adam’s system

**Problem:** Check **(8, 2)** in **y = ¼x** and **x + y = 10**.

**Solution:**
```
y = ¼(8) = 2     ✓
8 + 2 = 10       ✓
```

**Answer:** **(8, 2) is a solution**

### Example 4 — (5, 10) for Aisha

**Problem:** Check **(5, 10)** in **x + y = 15** and **0.5x + 0.65y = 9**.

**Solution:**
```
5 + 10 = 15                    ✓
0.5(5) + 0.65(10) = 2.5 + 6.5 = 9  ✓
```

**Answer:** **(5, 10) is a solution** (5 apples, 10 oranges)

### Example 5 — Point is NOT a solution

**Problem:** Is **(0, −3)** a solution to **y = −x** and **y = ½x − 3**?

**Solution:**
```
y = −x:     −3 = −(0) = 0   ✗  (false)
y = ½x − 3: −3 = −3          ✓
```

**Answer:** **No** — fails **y = −x**

### Example 6 — Dimitri’s error analysis (Exam focus)

**Problem:** Dimitri checks **(2, −2)** in **y = ½x − 3**. He writes: “y = ½(2) − 3 = 2 − 3 = −2.” Is his work correct?

**Solution:**
- **½(2) = 1**, not 2
- Correct: **1 − 3 = −2** — final answer lucky right, but **middle step wrong**
- If exam asks “first error”: **½(2) should be 1, not 2**

**Answer:** **Error:** wrote **2 − 3** instead of **1 − 3** (miscomputed ½ × 2)

### Example 7 — Dimitri checks wrong point

**Problem:** Dimitri says **(3, −1)** satisfies **y = −x** and **y = ½x − 3**. Verify.

**Solution:**
```
y = −x:     −1 = −3   ✗
y = ½x − 3: −1 = 1.5 − 3 = −1.5  ✗
```

**Answer:** **(3, −1) is NOT a solution**

### Example 8 — Which point satisfies both?

**Problem:** System **y = −3x + 5** and **y = −3x − 6**. Can any point satisfy both?

**Solution:**
- Parallel lines → **no** ordered pair works

**Answer:** **No solution** — none check for both

### Exam-style practice

---

**1. Quick check: (1, 9) on y = 2x + 7?**

**Solution:** 2(1) + 7 = 9 ✓

---

**2. (4, 2) on x + y = 10?**

**Solution:** 4 + 2 = 6 ≠ 10 ✗

---

**3. Find error: “−2(−3) − 1 = −6 − 1 = −7” for y at x = −3**

**Solution:** **−2(−3) = +6**, not −6 → should be **6 − 1 = 5**

### Common Mistakes
- Checking **only one** equation (Betty-style problems require **both**).
- **Dimitri trap:** arithmetic on fractions (**½ × 2 = 1**, not 2).
- Sign errors: **−2(−3) = +6**, not −6.

### Mini Summary
- Substitute into **both** equations.
- **(−3, 5)** works for **y = −2x − 1** and **y = x + 8**.
- **(2, −2)** works for **y = ½x − 3** and **y = −x**.
- **Parallel systems** — no point passes both.
''',

    "unit_6_systems_linear_equations_lesson_notes.md": '''# Unit 6: Systems of Linear Equations — Overview

| Activity | Topic | Key idea |
|----------|-------|----------|
| **1** | Graphing Systems | Intersection = solution; y = ½x − 3 and y = −x → (2, −2); table + graph |
| **2** | Slope-Intercept Form | 5x − 2y = 10 → y = ⁵⁄₂x − 5; identify y = mx + b |
| **3** | Word Problems | Two numbers 4s + 3L = 31; Kedwin movies; Adam y = ¼x, x + y = 10; Aisha fruit cost |
| **4** | Number of Solutions | Parallel y = −3x + 5 & y = −3x − 6 → 0; infinite y = −2x − 8 & y = −(2x + 8) |
| **5** | Identify from Graph | Four lines; match system to (2, −2), (8, 2); Betty (−3, 5) |
| **6** | Checking Solutions | Substitute ordered pairs; Dimitri fraction/sign error analysis |

**Exam focus areas:** Graphing systems and reading intersection **(2, −2)** from **y = ½x − 3** with **y = −x** (table + line); converting **5x − 2y = 10** to **y = ⁵⁄₂x − 5**; two-number system **4s + 3L = 31** and **L − 7 = 2s**; parallel lines **y = −3x + 5** and **y = −3x − 6** (no solution); equivalent lines **y = −2x − 8** and **y = −(2x + 8)** (infinitely many); Kedwin movie cost comparison; Adam fertilizer **y = ¼x**, **x + y = 10** → **(8, 2)**; Aisha **x + y = 15**, **0.5x + 0.65y = 9**; verify **Betty (−3, 5)** on both equations; Dimitri substitution errors.

**Weak areas to review:** Distinguishing **parallel** (same slope, different intercept) vs **coincident** (same line); distributing **y = −(2x + 8)**; fraction substitution **½(2)**; writing **two** equations from word problems; checking **both** equations when verifying a point.

Open each activity for full notes, diagrams, and worked exam-style problems. Use **Daily Practice** for graphing systems, slope-intercept conversion, and substitution checks.
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
