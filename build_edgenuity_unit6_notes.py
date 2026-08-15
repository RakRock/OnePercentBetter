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
A system of equations is really asking: "Where do these two lines meet?" Each equation draws a line on the graph, and the **solution** is the **ordered pair (x, y)** at the crossing point — the one point that makes **both** equations true at the same time. This matters because graphing lets you **see** the answer when algebra feels tricky, and checking your work is as simple as plugging the point into both equations.

### Key Vocabulary
- **System of equations:** two or more equations with the same variables
- **Solution (ordered pair):** (x, y) that satisfies every equation in the system
- **Intersection point:** where two lines cross on a graph
- **Consistent system:** at least one solution (one point, or infinitely many on the same line)

[DIAGRAM:system_intersection]

[DIAGRAM:graph_table_system]

### Example 1 — y = ½x − 3 and y = −x (Exam focus)

**What is this about:** Graphing two lines in slope-intercept form and reading where they cross.

**Problem:** Graph **y = ½x − 3** and **y = −x**. What is the solution?

**How to think about it:** Line 1 starts at **−3** on the y-axis and rises slowly (slope ½). Line 2 goes through the origin with slope **−1** (downhill). Find the point on both lines.

**Solution (step by step):**
1. **y = ½x − 3:** slope **½**, y-intercept **−3** — plot (0, −3), then up 1 right 2.
2. **y = −x:** slope **−1**, through (0, 0) — down 1 right 1.
3. Lines cross at **(2, −2)**.
4. Check: ½(2) − 3 = −2 ✓ and −(2) = −2 ✓.

**Answer:** **(2, −2)**

**Why this works:** The intersection is the only point that satisfies both equations — that's the definition of a system's solution.

### Example 2 — Table for y = −x plus graph y = ½x − 3

**What is this about:** Using a table for one line and graphing the second to find the solution.

**Problem:** A table shows **y = −x** with points (0, 0), (1, −1), (2, −2). Line 2 is **y = ½x − 3**. Find the solution.

**How to think about it:** Plot the table points for **y = −x**, draw **y = ½x − 3** from (0, −3) with slope ½, and look for the shared point.

**Solution (step by step):**
1. Plot table points: (0, 0), (1, −1), (2, −2) for **y = −x**.
2. Graph **y = ½x − 3** using slope ½ from (0, −3).
3. Both lines pass through **(2, −2)**.

**Answer:** **(2, −2)**

**Why this works:** A table gives accurate points for one line; graphing the other reveals the intersection.

### Example 3 — Read intersection from graph

**What is this about:** Reading a solution directly from a graph without solving algebraically.

**Problem:** A graph shows two lines crossing at (−1, 4). What is the solution of the system?

**How to think about it:** The crossing point **is** the answer — write it as an ordered pair **(x, y)**.

**Solution (step by step):**
1. Find where the lines meet on the graph.
2. Read coordinates: **x = −1**, **y = 4**.
3. Solution: **(−1, 4)**.

**Answer:** **(−1, 4)**

**Why this works:** Graphically, the solution is always the intersection coordinates.

### Example 4 — Which point is NOT on both lines?

**What is this about:** Testing whether a point satisfies **both** equations in a system.

**Problem:** System: **y = 2x + 1** and **y = −x + 7**. Is **(2, 5)** a solution?

**How to think about it:** Plug **x = 2** into **both** equations and see if you get **y = 5** each time.

**Solution (step by step):**
1. Line 1: **2(2) + 1 = 5** ✓
2. Line 2: **−(2) + 7 = 5** ✓
3. Both work → (2, 5) is on **both** lines.

**Answer:** **(2, 5) is a solution**

**Why this works:** A solution must satisfy every equation — one check isn't enough.

### Example 5 — Graph by intercepts

**What is this about:** Graphing lines using x- and y-intercepts instead of slope.

**Problem:** Graph **2x + y = 6** and **x − y = 2**.

**How to think about it:** Plug **x = 0** and **y = 0** to find where each line hits the axes, then connect the dots.

**Solution (step by step):**
1. **2x + y = 6:** (0, 6) and (3, 0)
2. **x − y = 2:** (0, −2) and (2, 0)
3. Lines intersect at **(8/3, 2/3)** (or read from the graph).

**Answer:** Solve algebraically or read **(8/3, 2/3)** from the graph

**Why this works:** Intercepts give two quick points per line — enough to draw each one accurately.

### Example 6 — Adam fertilizer system (preview)

**What is this about:** A real-world system graphed to find how much seed and fertilizer to use.

**Problem:** **y = ¼x** and **x + y = 10** — find the solution by graphing.

**How to think about it:** **y = ¼x** starts at the origin with gentle slope ¼. **x + y = 10** becomes **y = −x + 10**, a line sloping down from height 10.

**Solution (step by step):**
1. Graph **y = ¼x** through origin, slope ¼.
2. Graph **y = −x + 10** from (0, 10), slope −1.
3. Intersection: **(8, 2)** — check: ¼(8) = 2 ✓ and 8 + 2 = 10 ✓.

**Answer:** **(8, 2)**

**Why this works:** The intersection gives the one mix of seeds (x) and fertilizer (y) that fits both rules.

### Exam-style practice

---

**1. Lines cross at (3, 1). Solution?**

**Problem:** Two lines on a graph intersect at **(3, 1)**. What is the solution of the system?

**Solution (step by step):**
1. The intersection point is the solution.
2. Write as ordered pair **(x, y)**.

**Answer:** **(3, 1)**

---

**2. y = x + 2 and y = −2x + 5. Graph and find intersection.**

**Problem:** Find where **y = x + 2** and **y = −2x + 5** meet.

**Solution (step by step):**
1. Set equations equal: **x + 2 = −2x + 5**
2. Add 2x: **3x + 2 = 5**
3. **3x = 3** → **x = 1**
4. **y = 1 + 2 = 3**

**Answer:** **(1, 3)**

---

**3. Table gives (0, −3), (2, −2), (4, −1) on one line; second line y = −x. Solution?**

**Problem:** A table lists points on one line; the second equation is **y = −x**. Find the system solution.

**Solution (step by step):**
1. Check which table point also satisfies **y = −x**.
2. At **(2, −2)**: −(2) = −2 ✓ — on both lines.

**Answer:** **(2, −2)**

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
**y = mx + b** is the easiest form for graphing because it tells you exactly where to start (**b**, the y-intercept) and which way to go (**m**, the slope). When a system isn't in this form yet, convert it first — especially standard form like **5x − 2y = 10**. This matters because most graphing questions (including the exam focus on **5x − 2y = 10**) expect you to read slope and intercept quickly.

### Key Vocabulary
- **Slope (m):** rise over run; change in y / change in x
- **y-intercept (b):** where the line crosses the y-axis (x = 0)
- **Standard form:** Ax + By = C
- **Equivalent form:** same line, different equation (e.g., 5x − 2y = 10 and y = ⁵⁄₂x − 5)

[DIAGRAM:convert_to_slope_intercept]

[DIAGRAM:slope_intercept_form]

### Example 1 — 5x − 2y = 10 → y = ⁵⁄₂x − 5 (Exam focus)

**What is this about:** Converting standard form to slope-intercept form.

**Problem:** Write **5x − 2y = 10** in slope-intercept form.

**How to think about it:** Get **y alone** — subtract 5x, then divide **every term** by −2.

**Solution (step by step):**
1. Start: **5x − 2y = 10**
2. Subtract 5x: **−2y = −5x + 10**
3. Divide by −2: **y = (5/2)x − 5**

**Answer:** **y = ⁵⁄₂x − 5** (slope **⁵⁄₂**, y-intercept **−5**)

**Why this works:** Isolating y reveals m and b directly from the equation.

### Example 2 — Identify slope-intercept form

**What is this about:** Recognizing which equation already has y alone on the left.

**Problem:** Which equation is already in **y = mx + b**?

**How to think about it:** Look for **y =** with no other y-terms and no x, y mixed on the left.

**Solution (step by step):**
1. **A.** 3x + 2y = 8 → standard form (y not alone)
2. **B.** y = −3x + 5 → **y alone**, slope −3, intercept 5 ✓
3. **C.** x = 4 → vertical line (not y = mx + b)
4. **D.** 2x − y = 7 → standard form

**Answer:** **y = −3x + 5**

**Why this works:** Slope-intercept form always looks like **y = mx + b** with y on the left side only.

### Example 3 — Convert x + y = 10

**What is this about:** Simple rearrangement to slope-intercept form.

**Problem:** Rewrite **x + y = 10** as y = mx + b.

**How to think about it:** Subtract x from both sides — done!

**Solution (step by step):**
1. **x + y = 10**
2. Subtract x: **y = −x + 10**
3. Slope **−1**, y-intercept **10**

**Answer:** **y = −x + 10**

**Why this works:** Moving x to the other side immediately gives slope-intercept form.

### Example 4 — Graph y = ¼x and y = −x + 10 (Adam system)

**What is this about:** Identifying slopes and intercepts in a real-world system.

**Problem:** Adam uses **y = ¼x** pounds of fertilizer per **x** pounds of seeds, and **x + y = 10** total pounds. Write both in slope-intercept form and identify slopes.

**How to think about it:** First equation is already done; rewrite **x + y = 10** as **y = −x + 10**.

**Solution (step by step):**
1. Equation 1: **y = ¼x** → m = ¼, b = 0
2. Equation 2: **y = −x + 10** → m = −1, b = 10
3. Lines cross at **(8, 2)**

**Answer:** **y = ¼x** and **y = −x + 10**; solution **(8, 2)**

**Why this works:** Slope-intercept form makes both lines easy to graph and compare.

### Example 5 — Compare slopes: parallel check

**What is this about:** Using slope and intercept to decide if lines are the same or just parallel.

**Problem:** Are **y = −3x + 5** and **y = −3x − 6** the same line?

**How to think about it:** Same slope but **different** y-intercepts → parallel, not identical.

**Solution (step by step):**
1. Both have slope **−3**
2. y-intercepts: **5** vs **−6** — different
3. Same slope + different intercept → **parallel** (different lines)

**Answer:** **No** — parallel lines (same slope, different intercepts)

**Why this works:** Parallel lines never meet; identical lines share both m and b.

### Example 6 — 2x + 3y = 12

**What is this about:** Converting when y's coefficient isn't 1.

**Problem:** Solve **2x + 3y = 12** for y.

**How to think about it:** Subtract 2x, then divide **all** terms by 3.

**Solution (step by step):**
1. **2x + 3y = 12**
2. **3y = −2x + 12**
3. **y = (−2/3)x + 4**

**Answer:** **y = −⅔x + 4**

**Why this works:** Dividing every term by 3 keeps the equation equivalent.

### Example 7 — Which line has y-intercept −3?

**What is this about:** Reading **b** from slope-intercept form.

**Problem:** Pick the equation with **b = −3**.

**How to think about it:** In **y = mx + b**, the constant at the end is b.

**Solution (step by step):**
1. **y = ½x − 3** → b = **−3** ✓
2. **y = ½x + 3** → b = 3 (wrong sign)

**Answer:** **y = ½x − 3**

**Why this works:** The last number in y = mx + b is always the y-intercept.

### Exam-style practice

---

**1. 4x − y = 8 → slope-intercept?**

**Problem:** Write **4x − y = 8** in slope-intercept form.

**Solution (step by step):**
1. Subtract 4x: **−y = −4x + 8**
2. Multiply by −1: **y = 4x − 8**

**Answer:** **y = 4x − 8**

---

**2. Slope of y = ⁵⁄₂x − 5?**

**Problem:** What is the slope of **y = ⁵⁄₂x − 5**?

**Solution (step by step):**
1. In **y = mx + b**, m is the number on x.
2. **m = ⁵⁄₂**

**Answer:** **m = ⁵⁄₂**

---

**3. y = −2x − 8 vs y = −(2x + 8). Same line?**

**Problem:** Are **y = −2x − 8** and **y = −(2x + 8)** the same line?

**Solution (step by step):**
1. Distribute: **y = −(2x + 8) = −2x − 8**
2. Both equations identical → same line.

**Answer:** **Same line** → **infinitely many solutions**

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
Word problems with systems always give you **two facts** about the same two unknowns — your job is to turn each fact into an equation. Define your variables clearly first (like "s = smaller number"), then write two equations that are **independent** (different facts, not the same fact twice). This matters because a single equation can't pin down two unknowns — you need two equations, just like you need two clues to solve a mystery with two suspects.

### Key Vocabulary
- **Two-number problems:** sum, difference, multiples
- **Mixture / cost:** quantity equation + value equation
- **Comparison:** "twice as many," "$4 per rental," fixed fees

[DIAGRAM:word_to_equations]

[DIAGRAM:real_world_system]

### Example 1 — Two numbers (Exam focus)

**What is this about:** Translating "four times smaller plus three times larger" and a comparison sentence into a system.

**Problem:** Four times the smaller number plus three times the larger number is **31**. The larger minus **7** equals **twice** the smaller. Find the numbers.

**How to think about it:** Name the numbers **s** (smaller) and **L** (larger). First sentence → **4s + 3L = 31**. Second → **L − 7 = 2s**.

**Solution (step by step):**
1. Let **s** = smaller, **L** = larger.
2. Equation 1: **4s + 3L = 31**
3. Equation 2: **L − 7 = 2s** → **L = 2s + 7**
4. Substitute: **4s + 3(2s + 7) = 31** → **4s + 6s + 21 = 31** → **10s = 10** → **s = 1**
5. **L = 2(1) + 7 = 9**

**Answer:** **Smaller = 1, Larger = 9**; system: **4s + 3L = 31** and **L − 7 = 2s**

**Why this works:** Two sentences → two equations → one unique pair of numbers.

### Example 2 — Kedwin movies (Exam focus)

**What is this about:** Comparing two pricing plans to find when they cost the same (break-even point).

**Problem:** Kedwin can watch movies online for a **$10** flat fee (one payment, any number of movies), or rent movies at a store for **$4 per 5 movies** (no flat fee). After how many movies **m** is the total cost the same?

**How to think about it:** Define **m** = number of movies and **C** = total cost in dollars. Online is always **$10**. The store charges **$4 for every 5 movies**, so each movie costs **4/5** of a dollar.

**Solution (step by step):**
1. Define variables: **m** = number of movies, **C** = total cost ($).
2. **Online plan:** **C = 10** (flat $10 no matter how many movies).
3. **Store plan:** **C = (4/5)m** ($0.80 per movie, since $4 ÷ 5 = $0.80).
4. Set costs equal (break-even): **10 = (4/5)m**
5. Multiply both sides by 5: **50 = 4m**
6. Divide by 4: **m = 12.5**

**Answer:** System: **C = 10** and **C = (4/5)m**; break-even at **m = 12.5 movies** (cost is **$10** for both plans)

**Why this works:** Break-even means both plans cost the same — set the two cost formulas equal and solve for m.

### Example 3 — Adam fertilizer (Exam focus)

**What is this about:** A mixture problem with a ratio and a total weight.

**Problem:** Adam uses **¼** as much fertilizer **y** (lb) as seeds **x** (lb): **y = ¼x**. Total mix is **10** lb: **x + y = 10**. How many pounds of each?

**How to think about it:** One equation gives the ratio; the other gives the total. Substitute the ratio into the total.

**Solution (step by step):**
1. **y = ¼x**
2. **x + y = 10**
3. Substitute: **x + ¼x = 10** → **(5/4)x = 10**
4. **x = 8**, **y = ¼(8) = 2**

**Answer:** **8 lb seeds, 2 lb fertilizer**; solution **(8, 2)**

**Why this works:** Substituting eliminates one variable — classic two-equation system solve.

### Example 4 — Aisha apples and oranges (Exam focus)

**What is this about:** A count equation plus a money equation.

**Problem:** Aisha buys **x** apples and **y** oranges. Total fruit: **15**. Apples **$0.50**, oranges **$0.65**; total cost **$9**.

**How to think about it:** One equation for **how many** pieces, one for **how much money**.

**Solution (step by step):**
1. Count: **x + y = 15**
2. Cost: **0.5x + 0.65y = 9**
3. From first: **x = 15 − y**
4. Substitute: **0.5(15 − y) + 0.65y = 9** → **7.5 + 0.15y = 9** → **0.15y = 1.5** → **y = 10**
5. **x = 15 − 10 = 5**

**Answer:** **5 apples, 10 oranges**; system: **x + y = 15** and **0.5x + 0.65y = 9**

**Why this works:** Quantity and cost are two different facts → two equations → one answer.

### Example 5 — Babysitting rates

**What is this about:** Finding when two hourly rates (one with a flat fee) cost the same.

**Problem:** Maria charges **$8/hr** plus **$5** travel. Jake charges **$10/hr** flat. After how many hours **h** is the cost equal?

**How to think about it:** Maria's cost grows as **8h + 5**; Jake's as **10h**. Set them equal.

**Solution (step by step):**
1. Maria: **C = 8h + 5**
2. Jake: **C = 10h**
3. **8h + 5 = 10h**
4. **5 = 2h** → **h = 2.5**

**Answer:** **2.5 hours**; system **y = 8x + 5** and **y = 10x**

**Why this works:** Equal costs at break-even — same idea as Kedwin's movie plans.

### Example 6 — Write the system only

**What is this about:** Practice translating words to equations without solving yet.

**Problem:** The sum of two numbers is **20**. One number is **3 more** than twice the other.

**How to think about it:** Let **x** and **y** be the numbers. Sum → **x + y = 20**. "3 more than twice the other" → **y = 2x + 3**.

**Solution (step by step):**
1. Let x = first number, y = second number.
2. **x + y = 20**
3. **y = 2x + 3**

**Answer:** **x + y = 20** and **y = 2x + 3**

**Why this works:** Two distinct facts from the story become two equations — setup is the critical first step.

### Exam-style practice

---

**1. Tickets: $5 adult, $3 child; 12 people, $48 total.**

**Problem:** Write a system for 12 people paying $48 with $5 adult tickets (a) and $3 child tickets (c).

**Solution (step by step):**
1. Total people: **a + c = 12**
2. Total money: **5a + 3c = 48**

**Answer:** **a + c = 12** and **5a + 3c = 48**

---

**2. Two numbers: sum 50, difference 6.**

**Problem:** Two numbers add to 50 and differ by 6. Write the system.

**Solution (step by step):**
1. Sum: **x + y = 50**
2. Difference (x bigger): **x − y = 6**

**Answer:** **x + y = 50** and **x − y = 6**

---

**3. y = ¼x and x + y = 10. Find x.**

**Problem:** Solve the system **y = ¼x** and **x + y = 10** for x.

**Solution (step by step):**
1. Substitute: **x + ¼x = 10**
2. **(5/4)x = 10**
3. **x = 8**

**Answer:** **x = 8**

### Common Mistakes
- Writing **one** equation with **two** unknowns and stopping.
- Swapping coefficients in "four times smaller + three times larger" (use **4s + 3L**, not 3s + 4L).
- Mixing **cents** and **dollars** in cost problems (Aisha: keep 0.5 and 0.65 in dollars).

### Mini Summary
- Two facts → **two equations**.
- **4s + 3L = 31** and **L − 7 = 2s** → smaller **1**, larger **9**.
- **Adam:** **y = ¼x**, **x + y = 10** → **(8, 2)**.
- **Aisha:** **x + y = 15**, **0.5x + 0.65y = 9** → **5 apples, 10 oranges**.
- **Kedwin:** **C = 10** and **C = (4/5)m** → break-even at **m = 12.5 movies**.
''',

    "activity_4_number_of_solutions.md": '''# Activity 4: Number of Solutions in a System

[KEY]
**One solution:** lines intersect at **one point** (different slopes).  
**No solution:** **parallel** lines — same slope, **different** y-intercepts.  
**Infinitely many:** **same line** — equations are equivalent (same slope **and** same intercept).
[/KEY]

## Quick Review Notes

### Main Idea
A system can have **one** solution (lines cross once), **zero** solutions (parallel lines that never meet), or **infinitely many** (both equations describe the **same** line). Compare **slopes** and **y-intercepts** after rewriting as **y = mx + b**. This matters because exam questions love the parallel trap (**y = −3x + 5** and **y = −3x − 6**) and the "same line" trap (**y = −(2x + 8)**).

### Key Vocabulary
- **Parallel lines:** equal slopes, no intersection (in a plane)
- **Coincident lines:** same line — every point on the line is a solution
- **Inconsistent system:** no solution (parallel)
- **Dependent system:** infinitely many solutions (same line)

[DIAGRAM:parallel_lines]

[DIAGRAM:infinite_solutions]

### Example 1 — Parallel: y = −3x + 5 and y = −3x − 6 (Exam focus)

**What is this about:** Recognizing parallel lines from matching slopes and different intercepts.

**Problem:** How many solutions does the system **y = −3x + 5** and **y = −3x − 6** have?

**How to think about it:** Same slope **−3** means same steepness. Different b values (**5** vs **−6**) means different lines that never cross.

**Solution (step by step):**
1. Line 1: slope **−3**, y-intercept **5**
2. Line 2: slope **−3**, y-intercept **−6**
3. Same slope, different intercepts → **parallel**
4. Parallel lines never intersect → **zero solutions**

**Answer:** **Zero solutions (no solution)**

**Why this works:** No intersection means no (x, y) satisfies both equations.

### Example 2 — Infinite: y = −2x − 8 and y = −(2x + 8) (Exam focus)

**What is this about:** Showing two equations look different but describe the same line.

**Problem:** How many solutions for **y = −2x − 8** and **y = −(2x + 8)**?

**How to think about it:** Distribute the minus sign — you might get the **same** equation twice.

**Solution (step by step):**
1. **y = −(2x + 8) = −2x − 8**
2. Second equation matches the first exactly
3. Same line → every point on the line is a solution

**Answer:** **Infinitely many solutions**

**Why this works:** Equivalent equations graph as one line — infinite shared points.

### Example 3 — One solution

**What is this about:** Different slopes guarantee exactly one crossing point.

**Problem:** **y = ½x − 3** and **y = −x** — how many solutions?

**How to think about it:** Slopes **½** and **−1** are different → lines must cross once.

**Solution (step by step):**
1. Slopes: **½** and **−1** — different ✓
2. Lines cross at **(2, −2)**
3. Exactly one intersection → one solution

**Answer:** **Exactly one solution: (2, −2)**

**Why this works:** Different slopes → one meeting point → one ordered pair solution.

### Example 4 — Standard form parallel check

**What is this about:** Converting standard form to compare slopes and intercepts.

**Problem:** Are **2x + 4y = 8** and **x + 2y = 5** the same line?

**How to think about it:** Rewrite both as y = mx + b and compare m and b.

**Solution (step by step):**
1. First: **4y = −2x + 8** → **y = −½x + 2**
2. Second: **2y = −x + 5** → **y = −½x + 2.5**
3. Same slope **−½**, different intercepts → parallel, not identical

**Answer:** **No solution** (not the same line)

**Why this works:** Same slope + different intercept = parallel = zero solutions.

### Example 5 — Coincident from standard form

**What is this about:** Spotting when one equation is a multiple of the other.

**Problem:** **3x − y = 4** and **−6x + 2y = −8** — number of solutions?

**How to think about it:** Divide the second equation by **−2** and see if it matches the first.

**Solution (step by step):**
1. Second equation ÷ (−2): **3x − y = 4**
2. Identical to the first equation
3. Same line → infinitely many solutions

**Answer:** **Infinitely many solutions**

**Why this works:** Scalar multiples of the same equation represent the same line.

### Example 6 — Graph interpretation

**What is this about:** Reading "no solution" from a graph where lines never meet.

**Problem:** A graph shows two lines that never meet. What can you conclude?

**How to think about it:** Lines that don't cross on a flat plane are parallel.

**Solution (step by step):**
1. No intersection visible on the graph.
2. Lines are **parallel**.
3. Parallel system → **no solution**.

**Answer:** **Zero solutions**

**Why this works:** Graphically, parallel lines confirm an inconsistent system.

### Example 7 — Which system has no solution?

**What is this about:** Picking the parallel pair from a list.

**Problem:** Pick the system with **no** solution.

**How to think about it:** Look for the same slope with different intercepts.

**Solution (step by step):**
1. **A.** y = 2x + 1 and y = 2x − 3 → slope 2, b = 1 vs −3 → **no solution** ✓
2. **B.** y = x and y = −x → different slopes → one solution
3. **C.** y = 3x and y = 3x → same line → infinite

**Answer:** **y = 2x + 1 and y = 2x − 3**

**Why this works:** Same m, different b is the signature of a parallel (no-solution) system.

### Exam-style practice

---

**1. y = 4x + 1 and y = 4x + 1**

**Problem:** How many solutions does **y = 4x + 1** and **y = 4x + 1** have?

**Solution (step by step):**
1. Both equations identical → same line.
2. Every point on the line satisfies both.

**Answer:** **Infinitely many solutions**

---

**2. y = −x + 10 and y = 2x + 1**

**Problem:** How many solutions for **y = −x + 10** and **y = 2x + 1**?

**Solution (step by step):**
1. Slopes **−1** and **2** — different.
2. Different slopes → lines cross exactly once.

**Answer:** **Exactly one solution**

---

**3. y = −3x + 5 and y = −3x − 6**

**Problem:** How many solutions for **y = −3x + 5** and **y = −3x − 6**?

**Solution (step by step):**
1. Same slope **−3**, intercepts **5** and **−6**.
2. Parallel lines → never intersect.

**Answer:** **No solution (zero solutions)**

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
When a graph shows lines (sometimes **four** at once!), you match equations by checking each line's **slope** and **y-intercept**, then verify the target point lies on **both** chosen lines. This matters on exams where you must pick the correct pair from several lines — plug the solution point into candidate equations to eliminate wrong choices fast.

### Key Vocabulary
- **Solution point test:** plug (x, y) into both equations
- **Line identification:** slope from rise/run; y-intercept where x = 0
- **System matching:** pair of equations whose graphs intersect at the given point

[DIAGRAM:four_lines_graph]

[DIAGRAM:match_system_graph]

### Example 1 — Four lines on one graph (Exam focus)

**What is this about:** Choosing the correct pair of lines from four when the solution is **(2, −2)**.

**Problem:** A graph shows four lines labeled W, X, Y, Z. Which **system** has solution **(2, −2)**?

**How to think about it:** Test **(2, −2)** in each candidate pair. You need **both** equations to work.

**Solution (step by step):**
1. Test **(2, −2)** on **y = ½x − 3**: ½(2) − 3 = −2 ✓
2. Test on **y = −x**: −(2) = −2 ✓
3. Both pass through **(2, −2)** → this is the correct system.
4. Slopes **½** and **−1** match the graph.

**Answer:** System **y = ½x − 3** and **y = −x**

**Why this works:** The solution point must satisfy both equations in the system — test, don't guess by color.

### Example 2 — Match graph to y = ⁵⁄₂x − 5

**What is this about:** Connecting an equation to its graph using slope and intercept.

**Problem:** Which graph shows **5x − 2y = 10**?

**How to think about it:** Convert to **y = ⁵⁄₂x − 5** — y-intercept **−5**, steep positive slope.

**Solution (step by step):**
1. Rewrite: **y = ⁵⁄₂x − 5**
2. y-intercept: **(0, −5)**
3. Slope: rise **5**, run **2** (steep uphill)
4. Pick the graph through (0, −5) with that slope.

**Answer:** Line through **(0, −5)** with steep positive slope **⁵⁄₂**

**Why this works:** m and b tell you exactly how the line should look on the graph.

### Example 3 — Which system has solution (8, 2)?

**What is this about:** Matching Adam's fertilizer system to a solution point.

**Problem:** Find the system with solution **(8, 2)**.

**How to think about it:** Plug **(8, 2)** into both equations of each candidate system.

**Solution (step by step):**
1. **y = ¼x:** ¼(8) = 2 ✓
2. **x + y = 10:** 8 + 2 = 10 ✓
3. Both work → Adam's system.

**Answer:** **y = ¼x** and **x + y = 10** (Adam fertilizer)

**Why this works:** A solution point must make both equations true simultaneously.

### Example 4 — Point (−3, 5) on both lines

**What is this about:** Verifying Betty's claimed solution.

**Problem:** Betty claims **(−3, 5)** satisfies her system. Equations: **y = −2x − 1** and **y = x + 8**. Is she correct?

**How to think about it:** Substitute **x = −3, y = 5** into each equation.

**Solution (step by step):**
1. **y = −2x − 1:** −2(−3) − 1 = 6 − 1 = **5** ✓
2. **y = x + 8:** −3 + 8 = **5** ✓
3. Both true → Betty is correct.

**Answer:** **Yes** — **(−3, 5)** is the solution

**Why this works:** Substitution confirms whether a point lies on each line.

### Example 5 — Pick the wrong line

**What is this about:** Checking that a point lies on a given line.

**Problem:** Solution should be **(1, 9)**. One equation is **y = 2x + 7**. Does (1, 9) work?

**How to think about it:** Plug **x = 1** into **y = 2x + 7**.

**Solution (step by step):**
1. **2(1) + 7 = 9** ✓
2. (1, 9) is on **y = 2x + 7**
3. Need a second line through (1, 9) to complete the system.

**Answer:** **(1, 9)** lies on **y = 2x + 7**; match with another line through the same point

**Why this works:** One equation confirms the point is on one line; the system needs two lines through that point.

### Example 6 — Parallel lines on graph

**What is this about:** Reading "no solution" from parallel lines on a graph.

**Problem:** Two lines on the graph have the same slope but different y-intercepts. How many solutions?

**How to think about it:** Same slope + different intercept = parallel = never meet.

**Solution (step by step):**
1. Same slope → lines go the same direction.
2. Different intercepts → offset, never cross.
3. **Zero solutions**.

**Answer:** **Zero solutions**

**Why this works:** Parallel lines on a graph always represent an inconsistent system.

### Example 7 — Aisha system from context

**What is this about:** Finding where Aisha's count and cost lines cross.

**Problem:** Graph shows **x + y = 15** (y = −x + 15) and **0.5x + 0.65y = 9**. Where do they cross?

**How to think about it:** Solve or read the intersection — it's the fruit counts.

**Solution (step by step):**
1. System: **x + y = 15** and **0.5x + 0.65y = 9**
2. Solve: **x = 5**, **y = 10**
3. Intersection: **(5, 10)**

**Answer:** **(5, 10)** or **(x, y) = (5, 10)**

**Why this works:** The intersection gives both the graph solution and the word-problem answer.

### Exam-style practice

---

**1. Lines cross at (4, 3). Which ordered pair is the solution?**

**Problem:** Two lines intersect at **(4, 3)** on a graph. What is the solution?

**Solution (step by step):**
1. Intersection coordinates are the solution.
2. Write **(x, y) = (4, 3)**.

**Answer:** **(4, 3)**

---

**2. Point (2, −2) — which pair of slopes could form the system?**

**Problem:** A system's solution is **(2, −2)**. Which slopes could the two lines have?

**Solution (step by step):**
1. Verify (2, −2) on **y = ½x − 3**: ½(2) − 3 = −2 ✓
2. Verify on **y = −x**: −2 = −2 ✓
3. Slopes are **½** and **−1**.

**Answer:** **m = ½** and **m = −1** (system **y = ½x − 3** and **y = −x**)

---

**3. Four lines; only two pass through (−3, 5). That pair is the system.**

**Problem:** Four lines on a graph — find the two that both pass through **(−3, 5)**.

**Solution (step by step):**
1. Test (−3, 5) on each line's equation.
2. **y = −2x − 1** and **y = x + 8** both give y = 5 when x = −3.

**Answer:** **y = −2x − 1** and **y = x + 8** (Betty's system)

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
Always **check your answer** by plugging the ordered pair into **both** equations — not just one. If even one equation comes out false, the point is wrong. Error-analysis problems (like Dimitri's) ask you to find the **first** arithmetic or sign mistake in someone's substitution work. This matters because a small fraction error (**½ × 2 = 1**, not 2) can look like the right final answer but still show broken reasoning.

### Key Vocabulary
- **Substitution check:** replace x and y with the pair's values
- **True statement:** correct solution for that equation (e.g., 5 = 5)
- **False statement:** point is not on that line
- **Error analysis:** compare student work to correct substitution

[DIAGRAM:substitution_check]

[DIAGRAM:verify_solution]

### Example 1 — Betty (−3, 5) (Exam focus)

**What is this about:** Verifying a claimed solution in both equations.

**Problem:** Is **(−3, 5)** a solution to **y = −2x − 1** and **y = x + 8**?

**How to think about it:** Replace x with **−3** and y with **5** in **each** equation separately.

**Solution (step by step):**
1. Eq 1: **y = −2(−3) − 1 = 6 − 1 = 5** ✓ (matches y = 5)
2. Eq 2: **y = −3 + 8 = 5** ✓ (matches y = 5)
3. Both true → valid solution.

**Answer:** **Yes — (−3, 5) is a solution**

**Why this works:** A system solution must satisfy every equation — two checks, both must pass.

### Example 2 — Check (2, −2) for y = ½x − 3 and y = −x

**What is this about:** Checking the classic exam intersection point.

**Problem:** Verify **(2, −2)**.

**How to think about it:** Plug **x = 2, y = −2** into both lines.

**Solution (step by step):**
1. **y = ½x − 3:** ½(2) − 3 = 1 − 3 = **−2** ✓
2. **y = −x:** −(2) = **−2** ✓

**Answer:** **(2, −2) is a solution**

**Why this works:** Matching y-values in both equations confirms the point is on both lines.

### Example 3 — (8, 2) for Adam's system

**What is this about:** Checking a word-problem answer in context.

**Problem:** Check **(8, 2)** in **y = ¼x** and **x + y = 10**.

**How to think about it:** 8 lb seeds, 2 lb fertilizer — do both rules hold?

**Solution (step by step):**
1. **y = ¼x:** ¼(8) = **2** ✓
2. **x + y = 10:** 8 + 2 = **10** ✓

**Answer:** **(8, 2) is a solution**

**Why this works:** Substitution verifies both the ratio and the total from the story.

### Example 4 — (5, 10) for Aisha

**What is this about:** Checking count and cost for Aisha's fruit purchase.

**Problem:** Check **(5, 10)** in **x + y = 15** and **0.5x + 0.65y = 9**.

**How to think about it:** 5 apples, 10 oranges — right count and right total cost?

**Solution (step by step):**
1. **x + y = 15:** 5 + 10 = **15** ✓
2. **0.5x + 0.65y = 9:** 0.5(5) + 0.65(10) = 2.5 + 6.5 = **9** ✓

**Answer:** **(5, 10) is a solution** (5 apples, 10 oranges)

**Why this works:** Both the quantity equation and the money equation must check out.

### Example 5 — Point is NOT a solution

**What is this about:** Showing that failing **one** equation is enough to reject a point.

**Problem:** Is **(0, −3)** a solution to **y = −x** and **y = ½x − 3**?

**How to think about it:** If either equation fails, stop — it's not a solution.

**Solution (step by step):**
1. **y = −x:** −3 = −(0) = **0** ✗ (false!)
2. (Second equation would work, but one failure is enough.)

**Answer:** **No** — fails **y = −x**

**Why this works:** Both equations must be true — one false statement disqualifies the point.

### Example 6 — Dimitri's error analysis (Exam focus)

**What is this about:** Finding a fraction multiplication error in substitution work.

**Problem:** Dimitri checks **(2, −2)** in **y = ½x − 3**. He writes: "y = ½(2) − 3 = 2 − 3 = −2." Is his work correct?

**How to think about it:** Check **½(2)** carefully — half of 2 is **1**, not 2.

**Solution (step by step):**
1. Dimitri wrote **½(2) = 2** — that's wrong.
2. Correct: **½(2) = 1**
3. Then **1 − 3 = −2** — final answer happens to be right, but **middle step is wrong**.

**Answer:** **Error:** wrote **2 − 3** instead of **1 − 3** (miscomputed ½ × 2)

**Why this works:** Error analysis looks at **each step**, not just the final number.

### Example 7 — Dimitri checks wrong point

**What is this about:** Showing a point fails both equations.

**Problem:** Dimitri says **(3, −1)** satisfies **y = −x** and **y = ½x − 3**. Verify.

**How to think about it:** Substitute **x = 3, y = −1** into both.

**Solution (step by step):**
1. **y = −x:** −1 = −3 ✗
2. **y = ½x − 3:** −1 = 1.5 − 3 = −1.5 ✗

**Answer:** **(3, −1) is NOT a solution**

**Why this works:** Neither equation works — Dimitri's claim is wrong on both counts.

### Example 8 — Which point satisfies both?

**What is this about:** Recognizing that parallel systems have no checking point.

**Problem:** System **y = −3x + 5** and **y = −3x − 6**. Can any point satisfy both?

**How to think about it:** Parallel lines never share a point — no (x, y) works for both.

**Solution (step by step):**
1. Same slope **−3**, different intercepts → parallel.
2. No intersection → no ordered pair satisfies both.

**Answer:** **No solution** — none check for both

**Why this works:** You can't substitute-check a solution that doesn't exist.

### Exam-style practice

---

**1. Quick check: (1, 9) on y = 2x + 7?**

**Problem:** Does **(1, 9)** satisfy **y = 2x + 7**?

**Solution (step by step):**
1. Substitute x = 1: **y = 2(1) + 7 = 9**
2. Matches y = 9 ✓

**Answer:** **Yes — (1, 9) is on the line**

---

**2. (4, 2) on x + y = 10?**

**Problem:** Does **(4, 2)** satisfy **x + y = 10**?

**Solution (step by step):**
1. **4 + 2 = 6**
2. **6 ≠ 10** ✗

**Answer:** **No — (4, 2) is not a solution**

---

**3. Find error: "−2(−3) − 1 = −6 − 1 = −7" for y at x = −3**

**Problem:** Find the error in computing **y = −2x − 1** when **x = −3**.

**Solution (step by step):**
1. **−2(−3) = +6**, not −6 (negative × negative = positive).
2. Correct: **6 − 1 = 5**, not −7.

**Answer:** **−2(−3) should be +6**, not −6 → **y = 5**

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
| **3** | Word Problems | Two numbers 4s + 3L = 31; Kedwin movies break-even m = 12.5; Adam y = ¼x, x + y = 10; Aisha fruit cost |
| **4** | Number of Solutions | Parallel y = −3x + 5 & y = −3x − 6 → 0; infinite y = −2x − 8 & y = −(2x + 8) |
| **5** | Identify from Graph | Four lines; match system to (2, −2), (8, 2); Betty (−3, 5) |
| **6** | Checking Solutions | Substitute ordered pairs; Dimitri fraction/sign error analysis |

**Exam focus areas:** Graphing systems and reading intersection **(2, −2)** from **y = ½x − 3** with **y = −x** (table + line); converting **5x − 2y = 10** to **y = ⁵⁄₂x − 5**; two-number system **4s + 3L = 31** and **L − 7 = 2s**; parallel lines **y = −3x + 5** and **y = −3x − 6** (no solution); equivalent lines **y = −2x − 8** and **y = −(2x + 8)** (infinitely many); Kedwin movie cost break-even **m = 12.5**; Adam fertilizer **y = ¼x**, **x + y = 10** → **(8, 2)**; Aisha **x + y = 15**, **0.5x + 0.65y = 9**; verify **Betty (−3, 5)** on both equations; Dimitri substitution errors.

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
