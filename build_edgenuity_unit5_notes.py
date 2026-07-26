#!/usr/bin/env python3
"""One-time builder: writes Edgenuity Unit 5 activity markdown notes. Run: python build_edgenuity_unit5_notes.py"""

from pathlib import Path

NOTES = Path(__file__).parent / "ArjunEdgenuityCourse3" / "notes" / "unit_5"
NOTES.mkdir(parents=True, exist_ok=True)

ACTIVITIES = {
    "activity_1_algebra_tiles.md": '''# Activity 1: Algebra Tile Models

[KEY]
**Algebra tiles** model equations on a balance: **x-tiles** (long rectangles), **−x-tiles** (red/opposite color), **unit tiles** (+1 and −1 squares).  
Keep the scale balanced — whatever you add or remove from one side, do the same to the other.  
Goal: isolate **x** on one side and constants on the other.
[/KEY]

## Quick Review Notes

### Main Idea
Each tile stands for a term. Two x-tiles on the left mean **2x**; three unit tiles mean **+3**. To solve, move tiles so all x-tiles are on one side and all unit tiles on the other — matching the algebra steps (subtract x, add constants, etc.).

### Key Vocabulary
- **x-tile:** one variable unit (rectangle labeled x)
- **−x-tile:** opposite of one x (often red/orange)
- **Unit tile:** constant +1 (small square); yellow/green may show +1 or −1 by color
- **Balance model:** both sides must stay equal
- **Zero pair:** x and −x (or +1 and −1) cancel

[DIAGRAM:algebra_tiles_balance]

[DIAGRAM:completing_tile_model]

### Example 1 — 2x = x + 3 (Practice Q1)

**Problem:** A tile model shows **2x** on the left and **x + 3** on the right. Which action finds the solution?

**Solution:**
- Remove **1 x-tile from each side** → left: x, right: 3 unit tiles
- Algebra: subtract x from both sides → **x = 3**

**Answer:** **Remove 1 x-tile from each side**

### Example 2 — Complete 3x + 2 = −x + 6 (Practice Q4) ⚠️ Focus

**Problem:** Juanita models **3x + 2 = −x + 6**. Left side has 3 x-tiles and 2 unit tiles; right side has 1 **−x** tile. How does she complete the model?

**Solution:**
- Right side still needs **+6** (six positive unit tiles)
- The **−x** tile is already shown; add **6 yellow unit tiles** on the right

**Answer:** **Put 6 yellow unit tiles on the right side of the equal sign**

### Example 3 — Solve 3x + 2 = −x + 6

**Problem:** Solve using tiles or algebra.

**Solution:**
```
Add x to both sides:  4x + 2 = 6
Subtract 2:           4x = 4
Divide by 4:          x = 1
```

**Answer:** **x = 1**

### Example 4 — What do −x tiles mean? (Test Q22)

**Problem:** A model has three red tiles labeled **−x** on the right. What do they represent?

**Solution:**
- Each red tile is one **−x** → three tiles = **−3x**

**Answer:** **−3x**

### Example 5 — Like terms in tile model (Test Q24)

**Problem:** Model: **2x + 3 = 3x**. Which tiles are like terms?

**Solution:**
- **x-tiles** match **x-tiles** (2 on left, 3 on right)
- Unit tiles (+1) are not like x-tiles

**Answer:** **The x-tiles from both sides** (2 x-tiles and 3 x-tiles)

### Example 6 — Unit tile meaning (Test Q25)

**Problem:** Model: **3x + 4 = −2x**. What do the four unit tiles represent?

**Solution:**
- Small squares labeled **1** each → total **+4**

**Answer:** **4**

### Exam-style practice

---

**1. 2x + 3 = 3x. First tile move?**

**Solution:** Remove **2 x-tiles from each side** (or 3 from right) to gather x on one side.

---

**2. Left: x + 5, Right: 8. What to do?**

**Solution:** Remove **5 unit tiles from each side** → **x = 3**.

---

**3. Balance shows 4x = 12. Value of x?**

**Solution:** **x = 3** (four x-tiles equal twelve unit tiles).

### Common Mistakes
- Adding tiles to **only one side** — breaks the balance.
- Confusing **−x tiles** with **−1 unit tiles** (Test Q22 trap).
- Removing unit tiles before **pairing x-tiles** when variables are on both sides.

### Mini Summary
- **x-tile = x**, **unit tile = 1**, **−x-tile = −x**.
- Same move on **both sides** → same step in algebra.
- **2x = x + 3** → remove one x-tile each side → **x = 3**.
''',

    "activity_2_properties_equality.md": '''# Activity 2: Properties of Equality

[KEY]
**Addition/subtraction property:** add or subtract the same value on both sides.  
**Division property:** divide both sides by the same **nonzero** number to isolate x.  
**Distributive property:** a(b + c) = ab + ac — use this **before** combining like terms when parentheses appear.
[/KEY]

## Quick Review Notes

### Main Idea
Each step of solving keeps the equation true. Pick the property that moves you toward “x alone.” Addition fixes constants; division clears coefficients; distribution breaks apart parentheses like **4(x − 6)** or **8(3x + 40)**.

### Key Vocabulary
- **Addition property of equality:** if a = b, then a + c = b + c
- **Subtraction property of equality:** if a = b, then a − c = b − c
- **Division property of equality:** if a = b and c ≠ 0, then a/c = b/c
- **Distributive property:** multiply the factor outside parentheses across each term inside

[DIAGRAM:properties_equality]

[DIAGRAM:distributive_model]

### Example 1 — Best property for f − 23 = 45 (Practice Q16)

**Problem:** Which equation is **best** solved using the **addition** property?

**Solution:**
- **f − 23 = 45** → add **23** to both sides to isolate f
- f ÷ 23 = 45 needs **division**; 23f = 45 needs **division**

**Answer:** **f − 23 = 45**

### Example 2 — Division property: 7q = 49 (Practice Q19)

**Problem:** Which property should Remus use to solve **7q = 49**?

**Solution:**
- Variable is **multiplied** by 7 → **divide both sides by 7**
- q = 7

**Answer:** **Division property of equality**

### Example 3 — First step: 4(x − 6) = 5 (Test Q1)

**Problem:** Which property is used in the **first** step?

```
4(x − 6) = 5
4x − 24 = 5
```

**Solution:**
- Multiply **4** by **x** and **−6** → **distributive property**

**Answer:** **Distributive property**

### Example 4 — Graphic model 8(3x + 40) (Test Q23)

**Problem:** Arrows from **8** to **3x** and **40** in **8(3x + 40) = 10**. Which property?

**Solution:**
- Shows **8 · 3x** and **8 · 40** → **distributive property of multiplication**

**Answer:** **Distributive property of multiplication**

### Example 5 — Next step: 12 = −2x (Test Q12)

**Problem:** Carlton has **−4x + 12 = −6x** → **12 = −2x**. What is the **next** step?

**Solution:**
- x is **multiplied by −2** → **divide both sides by −2**
- x = −6

**Answer:** **Divide each side of the equation by −2**

### Example 6 — Distribute 5(x + 8) (Test Q16)

**Problem:** Rewrite **5(x + 8)** using the distributive property.

**Solution:**
```
5(x + 8) = 5·x + 5·8 = 5x + 40
```

**Answer:** **5x + 40**

### Example 7 — 4(x − 6) = 5 full solve (Practice Q — multistep)

**Problem:** Solve **4(x − 6) = 5**.

**Solution:**
```
4x − 24 = 5      (distribute)
4x = 29          (add 24)
x = 29/4         (divide by 4)
```

**Answer:** **x = 29/4**

### Exam-style practice

---

**1. x + 17 = 42. Best first property?**

**Solution:** **Subtraction** (subtract 17 from both sides).

---

**2. 6m = 54. Best property?**

**Solution:** **Division** → m = 9.

---

**3. 3(x + 4) = 18. First step?**

**Solution:** **Distribute 3** → 3x + 12 = 18.

### Common Mistakes
- Using **addition** when the variable is **multiplied** (7q trap).
- Dividing **only one term** instead of the **whole side**.
- Forgetting to distribute to **every term** inside parentheses.

### Mini Summary
- **f − 23 = 45** → add 23; **7q = 49** → divide by 7.
- **4(x − 6) = 5** starts with **distribute**.
- **8(3x + 40)** models the **distributive property**.
''',

    "activity_3_simplify_expressions.md": '''# Activity 3: Simplify Expressions

[KEY]
**Distribute** first: a(b + c) = ab + ac — watch **negative** signs: −(x − 3) = **−x + 3**.  
**Combine like terms:** same variable part (7b, 4b, −1b → 10b).  
With fractions, distribute to **each** term: ½(8x + 4) = 4x + 2.
[/KEY]

## Quick Review Notes

### Main Idea
Simplify before solving when expressions have parentheses or several terms. Distributing a negative flips **every** sign inside. Like terms share the same variable part (same letter and exponent).

### Key Vocabulary
- **Like terms:** same variable(s) and exponent(s); coefficients may differ
- **Coefficient:** numerical factor on a variable term
- **Constant:** term with no variable
- **Distribute negatives:** −1(x − 3) = −x + 3, not −x − 3

[DIAGRAM:distribute_negatives]

[DIAGRAM:combine_like_terms]

### Example 1 — Kadesha's error (Practice Q3) ⚠️ Focus

**Problem:** Simplify **−(x − 3) − 2(x − 1)**. Kadesha wrote Step 2 as **−x − 3 − 2x − 2**. Where is the first error?

**Solution:**
- **−(x − 3) = −x + 3** (not −x − 3)
- **−2(x − 1) = −2x + 2** (not −2x − 2)
- Correct Step 2: **−x + 3 − 2x + 2** → **−3x + 5**

**Answer:** **First error in Step 2 — should be −x + 3 − 2x + 2**

### Example 2 — 6(x − 4) (Test Q6)

**Problem:** Which expression is equivalent to **6(x − 4)**?

**Solution:**
```
6(x − 4) = 6x − 24
```

**Answer:** **6x − 24**

### Example 3 — 7b + 4b − 1b (Test Q8)

**Problem:** Simplify **7b + 4b − 1b**.

**Solution:**
```
(7 + 4 − 1)b = 10b
```

**Answer:** **10b**

### Example 4 — ½(8x + 4) + ⅓(9 − 3x) (Practice Q8)

**Problem:** Simplify **½(8x + 4) + ⅓(9 − 3x)**.

**Solution:**
```
½(8x + 4) = 4x + 2
⅓(9 − 3x) = 3 − x
Total: 4x + 2 + 3 − x = 3x + 5
```

**Answer:** **3x + 5**

### Example 5 — 9p − 3p + 2 (Test Q19)

**Problem:** Simplify **9p − 3p + 2**.

**Solution:**
```
6p + 2
```

**Answer:** **6p + 2**

### Example 6 — Like terms in −a²b + 6ab − 8 + 5a²b − 6a − b (Test Q17)

**Problem:** Which are like terms?

**Solution:**
- **−a²b** and **5a²b** share **a²b**
- 6ab and −6a are **not** like a²b terms

**Answer:** **−a²b and 5a²b**

### Example 7 — Constant in −x² − 6y + 13x + 7 (Test Q11)

**Problem:** Which number is a **constant**?

**Solution:**
- **7** has no variable

**Answer:** **7**

### Exam-style practice

---

**1. −2(x + 5)**

**Solution:** **−2x − 10**

---

**2. 4x + 9x − 2x**

**Solution:** **11x**

---

**3. ⅔x + ⅓x + 2 (Test Q18 first step)**

**Solution:** **Combine like terms** → x + 2 = 5.

### Common Mistakes
- **Kadesha trap:** −(x − 3) → −x − 3 instead of **−x + 3**.
- Distributing to **only the first term**: 6(x − 4) ≠ 6x − 4.
- Combining **unlike** terms (x with x², or x with constants).

### Mini Summary
- **Negative distribute:** flip **both** signs inside parentheses.
- **7b + 4b − 1b = 10b**; **6(x − 4) = 6x − 24**.
- **½(8x + 4) + ⅓(9 − 3x) = 3x + 5**.
''',

    "activity_4_number_of_solutions.md": '''# Activity 4: Number of Solutions

[KEY]
After simplifying, if you get **x = number** → **one solution**.  
If **false** statement (e.g., −24 = 7) → **no solution**.  
If **true** identity (e.g., 6x − 8 = 6x − 8) → **infinitely many solutions**.
[/KEY]

## Quick Review Notes

### Main Idea
Simplify both sides fully. If all x-terms cancel and constants differ, there is **no** value of x that works. If all x-terms cancel and constants match, **every** x works. If one x remains, solve for a single answer.

### Key Vocabulary
- **One solution:** exactly one value of x makes the equation true
- **No solution:** simplified equation is false (contradiction)
- **Infinitely many solutions:** both sides are identical (identity)

[DIAGRAM:one_solution]

[DIAGRAM:no_solution_case]

### Example 1 — Aanya's four equations (Practice Q2) ⚠️ Focus

**Problem:** Which has **exactly one** solution?

**Solution:**
- **A.** 6x − 8 = 4(x − 2) + 2x → 6x − 8 = 6x − 8 → **infinitely many**
- **B.** 3(x − 1) + 2x = 3(x − 1) + 2 → 5x − 3 = 5x − 1 → **−3 = −1** → **one solution** ✓
- **C.** 7x + 2 − x = 6(x + 2) → 6x + 2 = 6x + 12 → **2 = 12** → **no solution**
- **D.** 4(x + 3) + x = 5(x + 1) + 7 → 5x + 12 = 5x + 12 → **infinitely many**

**Answer:** **B: 3(x − 1) + 2x = 3(x − 1) + 2**

### Example 2 — Kamal's work (Practice Q22)

**Problem:**
```
3(x − 8) = x + 2x + 7
3x − 24 = 3x + 7
−24 = 7
```
What is the solution?

**Solution:**
- **−24 = 7** is **false** → **no solution**

**Answer:** **No solution**

### Example 3 — One solution: 9x − 10 = 3x + 2 (Test Q20)

**Problem:** Solve **9x − 10 = 3x + 2**.

**Solution:**
```
6x = 12 → x = 2
```

**Answer:** **One solution: x = 2**

### Example 4 — Maria: one solution vs none (Test Q4)

**Problem:** **3(x + 6) = 5(x − 4)** → **3x + 18 = 5x − 20**. Solution?

**Solution:**
```
38 = 2x → x = 19
```
One numeric solution.

**Answer:** **x = 19 (one solution)**

### Example 5 — Recognize identity (Practice Q2 — equation A)

**Problem:** Is **6x − 8 = 4(x − 2) + 2x** one, none, or infinite?

**Solution:**
- Both sides simplify to **6x − 8** → **infinitely many solutions**

**Answer:** **Infinitely many solutions**

### Example 6 — 6x + 2 = 9x − 1 (Test Q7)

**Problem:** Solve **6x + 2 = 9x − 1**.

**Solution:**
```
3 = 3x → x = 1
```
One solution.

**Answer:** **One solution: x = 1**

### Exam-style practice

---

**1. 2x + 5 = 2x + 9**

**Solution:** **No solution** (5 ≠ 9).

---

**2. 4(x + 1) = 4x + 4**

**Solution:** **Infinitely many solutions**.

---

**3. 5x − 3 = 2x + 6**

**Solution:** **One solution:** x = 3.

### Common Mistakes
- Picking an equation that is an **identity** (Aanya A or D trap).
- Thinking **−24 = 7** means x = −24 or x = 7 (Kamal trap).
- Stopping before **fully** simplifying both sides.

### Mini Summary
- **False** (constants differ, no x) → **no solution**.
- **True identity** → **infinitely many**.
- **One x** left → **one solution** — solve it.
''',

    "activity_5_multistep_solving.md": '''# Activity 5: Multi-Step Solving

[KEY]
Typical flow: **(1) Distribute** → **(2) Combine like terms** → **(3) Move variable terms to one side** → **(4) Move constants** → **(5) Divide** by the coefficient of x.  
When x is on **both sides**, collect x terms on one side and constants on the other.
[/KEY]

## Quick Review Notes

### Main Idea
Use the most efficient first step: if parentheses appear, **distribute** first. Then combine like terms on each side. Variables on both sides? Add or subtract x-terms to one side. Fractions and decimals follow the same order.

### Key Vocabulary
- **Multi-step equation:** needs more than one inverse operation
- **Variables on both sides:** x terms appear left and right
- **Efficient first step:** distribute before moving isolated constants inside parentheses

[DIAGRAM:multistep_flow]

[DIAGRAM:variables_both_sides]

### Example 1 — First step: 4x + 3(x + 2) = 5(2x − 3) (Practice Q17)

**Problem:** Reasonable **first** step?

**Solution:**
- **Distribute 3** to (x + 2) and **5** to (2x − 3)
- Do **not** combine 4x and x before distributing

**Answer:** **Distribute the 3 to x + 2, and the 5 to (2x − 3)**

### Example 2 — Maria's equation (Test Q4)

**Problem:** **3(x + 6) = 5(x − 4)**. Find x.

**Solution:**
```
3x + 18 = 5x − 20
38 = 2x
x = 19
```

**Answer:** **x = 19**

### Example 3 — 3x − 10 = 2x + 5 (Practice Q18)

**Problem:** Three times a number minus ten equals twice the number plus five. Find x.

**Solution:**
```
3x − 10 = 2x + 5
x = 15
```

**Answer:** **x = 15**

### Example 4 — Leonardo's fraction error (Practice Q15) ⚠️ Focus

**Problem:** Leonardo solves **4(x − ⅕) = 2⅔**. In Step 3 he writes **4/5 = 16/15** when adding fractions. Where is the error?

**Solution:**
- Step 2: **4x = 8/3 + 4/5** is correct
- Step 3: **4/5 = 12/15**, not **16/15** (common denominator 15)

**Answer:** **Error in Step 3** — 4/5 should be 12/15

### Example 5 — Carey combines terms (Test Q2)

**Problem:** **4(2x − 1) + 5 = 3 + 2(x + 1)** → **8x − 4 + 5 = 3 + 2x + 2**. Which terms should Carey combine?

**Solution:**
- Constants on left: **−4 + 5**
- Constants on right: **3 + 2**
- Do **not** combine 8x with 2x until constants are simplified (or combine x terms separately)

**Answer:** **−4 + 5 and 3 + 2**

### Example 6 — 7(x − 3) = 28 (Test Q13)

**Problem:** Follow the steps for **7(x − 3) = 28**.

**Solution:**
```
7x − 21 = 28    (distribute)
7x = 49         (add 21)
x = 7           (divide by 7)
```

**Answer:** **x = 7**

### Example 7 — 0.45(x + 1.6) + 5x = 18 (Practice Q20)

**Problem:** Find x (nearest hundredth).

**Solution:**
```
0.45x + 0.72 + 5x = 18
5.45x = 17.28
x ≈ 3.17
```

**Answer:** **x ≈ 3.17**

### Example 8 — Decimal both sides (Practice Q9)

**Problem:** Steps for **−1.3 + 4.6x = 0.3 + 4x**?

**Solution:**
- **Add 1.3** to both sides
- **Subtract 4x** from both sides
- **Divide** by the coefficient of x

**Answer:** **Add 1.3, subtract 4x, then divide by coefficient of x**

### Example 9 — 3.7x − 18 = −4.3x − 34 (Test Q9)

**Problem:** Most efficient **first** step?

**Solution:**
- Add **4.3x** to both sides to collect x terms

**Answer:** **Add 4.3x to both sides**

### Example 10 — 2(x + 6) = 3(x − 4) + 5 (Test Q15)

**Problem:** Reasonable first step?

**Solution:**
- **Distribute 2** to (x + 6) and **3** to (x − 4)

**Answer:** **Distribute 2 to (x + 6) and 3 to (x − 4)**

### Exam-style practice

---

**1. 4(2x − 1) + 5 = 3 + 2(x + 1). After distributing, combine constants.**

**Solution:** Left: **1**; Right: **5** → 8x + 1 = 2x + 5.

---

**2. Ronin: 4(x + 2) = 96 (Practice Q12). Find x.**

**Solution:** x + 2 = 24 → **x = 22**.

---

**3. Antwan: 3(⅓x + 1) + 4 = −1 − 4(x + 3) (Practice Q11). Constants after steps?**

**Solution:** **−20 or 20** (depending on side after moving terms).

### Common Mistakes
- Combining **4x + 3(x + 2)** before distributing (Practice Q17 trap).
- **Leonardo trap:** wrong common denominator when adding fractions.
- Combining **8x + 2x** before finishing constant arithmetic (Carey trap).

### Mini Summary
- Order: **distribute → combine → move x → move constants → divide**.
- **3x − 10 = 2x + 5** → **x = 15**; **Maria** → **x = 19**.
- **7(x − 3) = 28** → **x = 7**.
''',

    "activity_6_standard_form_word_problems.md": '''# Activity 6: Standard Form & Word Problems

[KEY]
**Standard form:** Ax + By = C. To **solve for y**, isolate y (often add/subtract the x-term, then **divide** by y's coefficient).  
**Word problems:** define the variable, write each part, set **equal** totals or perimeters, then solve.
[/KEY]

## Quick Review Notes

### Main Idea
In applications, translate words to algebra first. Standard-form equations may need rearranging before you can read slope or solve for one variable. Perimeter problems multiply side length by number of sides (square: 4x, triangle: 3(x + 1)).

### Key Vocabulary
- **Standard form:** Ax + By = C (A, B, C integers; A ≥ 0 often)
- **Solve for y:** rewrite with y alone on one side
- **Equivalent equation:** same solution set; different form
- **Perimeter:** sum of all side lengths

[DIAGRAM:solve_for_y]

[DIAGRAM:word_problem_setup]

### Example 1 — 9y − 12x = 36, solve for y (Practice Q6)

**Problem:** First step when solving for **y**?

**Solution:**
- y is on the left with **−12x** → **add 12x** to both sides
- Then divide by **9**

**Answer:** **Add 12x to both sides of the equation**

### Example 2 — Leah: 3x + 4y = 8 (Test Q3)

**Problem:** Leah has **4y = 8 − 3x**. What is her **next** step to solve for y?

**Solution:**
- **Divide both sides by 4**

**Answer:** **Divide both sides of the equation by 4**

### Example 3 — Tonya x = 150 − 6y (Practice Q5)

**Problem:** Which is equivalent to **x = 150 − 6y**?

**Solution:**
- Add **6y** to both sides → **x + 6y = 150**

**Answer:** **x + 6y = 150**

### Example 4 — Hockey tournament (Practice Q7)

**Problem:** Fins score **x** goals. Seals score **3 less than twice** Fins. Rays score **2 more** than Fins. Total **11** goals. Find each team.

**Solution:**
```
x + (2x − 3) + (x + 2) = 11
4x − 1 = 11 → x = 3
Fins: 3, Seals: 3, Rays: 5
```

**Answer:** **x + (2x − 3) + (x + 2) = 11**; Fins 3, Seals 3, Rays 5

### Example 5 — Square vs triangle perimeter (Test Q5)

**Problem:** Square side **x**, equilateral triangle side **x + 1**. Perimeters equal. Find equation for x.

**Solution:**
- Square: **4x**; Triangle: **3(x + 1)**
```
4x = 3(x + 1)
```

**Answer:** **4x = 3(x + 1)**

### Example 6 — Micah and Aria ages (Practice Q13)

**Problem:** Sum of ages is **29**. Aria is **5 years older than twice** Micah's age. Micah = x.

**Solution:**
```
x + (2x + 5) = 29
```

**Answer:** **x + (2x + 5) = 29**

### Example 7 — Rug rental (Test Q10)

**Problem:** **$23** per day plus **$45** checkout fee. Total **$137**. Find days d.

**Solution:**
```
23d + 45 = 137
23d = 92 → d = 4
```

**Answer:** **23d + 45 = 137**; **4 days**

### Example 8 — Solve for x: 5x − 10y = 30 (Test Q14) ⚠️ Focus

**Problem:** First step when solving for **x**?

**Solution:**
- Add **10y** to both sides (move y-term)
- **Not** subtract 5x (x is what we want to keep on the left)

**Answer:** **Add 10y to both sides**

### Example 9 — Ronin's square (Practice Q12)

**Problem:** Square side **(x + 2)** in., perimeter **96** in. **4(x + 2) = 96**. Find x.

**Solution:**
```
x + 2 = 24 → x = 22
```

**Answer:** **x = 22**

### Exam-style practice

---

**1. 2x + 5y = 20. Solve for y.**

**Solution:** **y = (20 − 2x)/5** or **y = 4 − (2/5)x**.

---

**2. Three partners: ¼ + ⅖ + x = 1 (Practice Q10). Third share?**

**Solution:** **x = 7/20**

---

**3. Tristanne: 23d + 45 = 137. Days?**

**Solution:** **d = 4**

### Common Mistakes
- **Subtracting 5x** when solving for x in 5x − 10y = 30 (Test Q14 trap).
- Hockey: using **x + 3** instead of **2x − 3** for Seals.
- Forgetting **4 sides** on a square or **3 sides** on a triangle.

### Mini Summary
- **9y − 12x = 36** → add **12x**, then divide by **9**.
- **Tonya:** x + 6y = 150; **hockey:** x + (2x − 3) + (x + 2) = 11.
- **4x = 3(x + 1)** for equal perimeters.
''',

    "unit_5_linear_equations_lesson_notes.md": '''# Unit 5: Linear Equations — Overview

| Activity | Topic | Key idea |
|----------|-------|----------|
| **1** | Algebra Tile Models | Balance 2x = x + 3; complete 3x + 2 = −x + 6; tile meanings (Test Q22–25) |
| **2** | Properties of Equality | f − 23 = 45; 4(x − 6) = 5 distribute; 8(3x + 40) graphic (Test Q1, Q23) |
| **3** | Simplify Expressions | Kadesha negatives Q3; 6(x − 4); 7b + 4b − 1b; ½(8x+4)+⅓(9−3x) Q8 |
| **4** | Number of Solutions | Aanya Q2; Kamal no solution Q22; 9x − 10 = 3x + 2 (Test Q20) |
| **5** | Multi-Step Solving | 4x + 3(x+2) = 5(2x−3); Maria x = 19; 3x−10 = 2x+5; Leonardo Q15; Carey Q2; 7(x−3) = 28 |
| **6** | Standard Form & Word Problems | 9y − 12x = 36; Leah 3x+4y = 8; hockey Q7; 4x = 3(x+1); Tonya x + 6y = 150 |

**Exam focus areas (47-page exam — 22 practice + 25 test questions):** Algebra tiles 2x = x + 3 (Practice Q1), Juanita 3x + 2 = −x + 6 (Q4), Kadesha distribute negatives (Q3), Aanya one solution (Q2), Kamal no solution (Q22), properties f − 23 = 45 (Q16), 4(x − 6) = 5 (Test Q1), 8(3x + 40) (Test Q23), simplify 6(x − 4) (Test Q6), 7b + 4b − 1b (Test Q8), fraction simplify (Practice Q8), multistep 4x + 3(x + 2) (Practice Q17), Maria (Test Q4), 3x − 10 = 2x + 5 (Practice Q18), Leonardo fraction error (Q15), Carey combine (Test Q2), 7(x − 3) = 28 (Test Q13), solve for y 9y − 12x = 36 (Practice Q6), Leah (Test Q3), hockey (Practice Q7), perimeter 4x = 3(x + 1) (Test Q5), Tonya (Practice Q5).

**Weak areas to review:** Kadesha sign errors when distributing negatives (Practice Q3), Aanya one vs infinite solutions (Q2), Leonardo LCD in fractions (Q15), Carey which terms to combine (Test Q2), solving for x vs y in standard form (Test Q14 trap), hockey/age word-problem setup (Practice Q7, Q13).

Open each activity for full notes, diagrams, and worked exam-style problems. Use **Daily Practice** for quiz sets with tile models and multi-step equations.
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
