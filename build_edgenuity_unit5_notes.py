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
Algebra tiles turn equations into something you can **see and move**, like a real balance scale. Each tile stands for a piece of the equation — x-tiles are the variable, unit tiles are plain numbers. This matters because when you can **picture** what "subtract x from both sides" means, the algebra steps stop feeling like random rules and start making sense. If both sides stay balanced, whatever you do to the tiles is exactly what you should do in algebra.

### Key Vocabulary
- **x-tile:** one variable unit (rectangle labeled x)
- **−x-tile:** opposite of one x (often red/orange)
- **Unit tile:** constant +1 (small square); yellow/green may show +1 or −1 by color
- **Balance model:** both sides must stay equal
- **Zero pair:** x and −x (or +1 and −1) cancel

[DIAGRAM:algebra_tiles_balance]

[DIAGRAM:completing_tile_model]

### Example 1 — 2x = x + 3 (Practice Q1)

**What is this about:** A tile model shows **2x** on the left and **x + 3** on the right. You need to pick the move that finds **x**.

**Problem:** A tile model shows **2x** on the left and **x + 3** on the right. Which action finds the solution?

**How to think about it:** Both sides have x-tiles, but the right side also has 3 extra unit tiles. If you remove the same number of x-tiles from **each** side, the scale stays balanced and the x-tiles on the right disappear — leaving x alone with the unit tiles.

**Solution (step by step):**
1. Start with **2x** on the left and **x + 3** on the right.
2. Remove **1 x-tile from each side** (a zero pair on the left keeps balance).
3. Left side: **x**. Right side: **3 unit tiles**.
4. Match to algebra: subtract x from both sides → **x = 3**.

**Answer:** **Remove 1 x-tile from each side**

**Why this works:** Removing the same tile from both sides is the tile version of subtracting x from both sides — you isolate x without breaking the balance.

### Example 2 — Complete 3x + 2 = −x + 6 (Practice Q4) ⚠️ Focus

**What is this about:** Juanita is building a tile model for **3x + 2 = −x + 6**. The right side is incomplete.

**Problem:** Juanita models **3x + 2 = −x + 6**. Left side has 3 x-tiles and 2 unit tiles; right side has 1 **−x** tile. How does she complete the model?

**How to think about it:** The equation says the right side equals **−x + 6**. Juanita already placed the **−x** tile. What's missing? The **+6** — six positive unit tiles.

**Solution (step by step):**
1. Read the right side of the equation: **−x + 6**.
2. Juanita already has **1 −x tile** on the right.
3. She still needs **+6**, which means **6 positive (yellow) unit tiles**.
4. Add **6 yellow unit tiles** on the right side of the equal sign.

**Answer:** **Put 6 yellow unit tiles on the right side of the equal sign**

**Why this works:** Every term in the equation needs a tile. **−x** is already shown; **+6** must appear as six +1 unit tiles.

### Example 3 — Solve 3x + 2 = −x + 6

**What is this about:** Solving the same equation using tiles or algebra once the model is complete.

**Problem:** Solve using tiles or algebra.

**How to think about it:** Get all x-tiles on one side and all unit tiles on the other. Adding x to both sides removes the **−x** from the right.

**Solution (step by step):**
1. Add **x** to both sides: **4x + 2 = 6**.
2. Subtract **2** from both sides: **4x = 4**.
3. Divide both sides by **4**: **x = 1**.

**Answer:** **x = 1**

**Why this works:** Each algebra step mirrors a balanced tile move — move variables together, then constants, then divide to find one x.

### Example 4 — What do −x tiles mean? (Test Q22)

**What is this about:** Reading a tile model and translating it into algebra.

**Problem:** A model has three red tiles labeled **−x** on the right. What do they represent?

**How to think about it:** Each red **−x** tile is one "negative x." Three tiles means you add three of them: **−x + (−x) + (−x) = −3x**.

**Solution (step by step):**
1. One red tile = **−1x**.
2. Three red tiles = **−1x + (−1x) + (−1x)**.
3. Combine: **−3x**.

**Answer:** **−3x**

**Why this works:** Tile labels tell you the term; counting tiles tells you the coefficient.

### Example 5 — Like terms in tile model (Test Q24)

**What is this about:** Finding which tiles can be grouped because they represent the same kind of term.

**Problem:** Model: **2x + 3 = 3x**. Which tiles are like terms?

**How to think about it:** "Like terms" means same type — all x-tiles match other x-tiles; unit tiles match unit tiles. You don't mix x-tiles with +1 squares.

**Solution (step by step):**
1. Left side: **2 x-tiles** and **3 unit tiles**.
2. Right side: **3 x-tiles**.
3. The **x-tiles from both sides** are like terms (2 on left, 3 on right).
4. Unit tiles (+1) are **not** like x-tiles.

**Answer:** **The x-tiles from both sides** (2 x-tiles and 3 x-tiles)

**Why this works:** Like terms share the same variable part — that's why x-tiles can be compared and moved together.

### Example 6 — Unit tile meaning (Test Q25)

**What is this about:** Identifying what constant the unit tiles represent.

**Problem:** Model: **3x + 4 = −2x**. What do the four unit tiles represent?

**How to think about it:** Small squares labeled **1** each stand for **+1**. Four of them together mean **+4**.

**Solution (step by step):**
1. Each unit tile = **+1**.
2. Four unit tiles = **1 + 1 + 1 + 1 = 4**.

**Answer:** **4**

**Why this works:** Unit tiles model constants (numbers without variables). Four +1 tiles always mean **+4**.

### Exam-style practice

---

**1. 2x + 3 = 3x. First tile move?**

**Problem:** A balance model shows **2x + 3** on the left and **3x** on the right. What is the first tile move to solve?

**Solution (step by step):**
1. Both sides have x-tiles — gather them on one side.
2. Remove **2 x-tiles from each side** (or remove 3 from the right).
3. Left: **3 unit tiles**. Right: **x**.

**Answer:** **Remove 2 x-tiles from each side**

---

**2. Left: x + 5, Right: 8. What to do?**

**Problem:** The left pan has **x + 5** (one x-tile and five unit tiles). The right pan has **8 unit tiles**. Find x.

**Solution (step by step):**
1. Remove **5 unit tiles from each side** to isolate x.
2. Left: **x**. Right: **3 unit tiles**.

**Answer:** **x = 3**

---

**3. Balance shows 4x = 12. Value of x?**

**Problem:** Four x-tiles on the left balance twelve unit tiles on the right. What is x?

**Solution (step by step):**
1. **4x = 12** means four x's equal twelve ones.
2. Divide both sides by 4: each x equals **3** unit tiles.

**Answer:** **x = 3**

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
When you solve an equation, every step must keep it **true** — like keeping a scale level. The **properties of equality** tell you which moves are allowed: add or subtract the same thing on both sides, divide both sides by the same nonzero number, or distribute before you combine terms. This matters because picking the **right property first** saves time and prevents mistakes — you wouldn't divide when you should add, or skip distributing when parentheses are in the way.

### Key Vocabulary
- **Addition property of equality:** if a = b, then a + c = b + c
- **Subtraction property of equality:** if a = b, then a − c = b − c
- **Division property of equality:** if a = b and c ≠ 0, then a/c = b/c
- **Distributive property:** multiply the factor outside parentheses across each term inside

[DIAGRAM:properties_equality]

[DIAGRAM:distributive_model]

### Example 1 — Best property for f − 23 = 45 (Practice Q16)

**What is this about:** Choosing the best property when the variable has a number **subtracted** from it.

**Problem:** Which equation is **best** solved using the **addition** property?

**How to think about it:** Addition property means **add the same number to both sides**. Look for a variable with something subtracted — like **f − 23** — where adding 23 will cancel the −23.

**Solution (step by step):**
1. **f − 23 = 45** → add **23** to both sides → **f = 68**. ✓ Uses addition.
2. **f ÷ 23 = 45** → needs **division**, not addition.
3. **23f = 45** → needs **division** to isolate f.

**Answer:** **f − 23 = 45**

**Why this works:** When a constant is subtracted from the variable, adding that constant to both sides is the natural first move.

### Example 2 — Division property: 7q = 49 (Practice Q19)

**What is this about:** Recognizing when the variable is **multiplied** by a number.

**Problem:** Which property should Remus use to solve **7q = 49**?

**How to think about it:** q is stuck being **multiplied by 7**. The opposite of multiply is **divide** — divide both sides by 7 to get q alone.

**Solution (step by step):**
1. **7q = 49** — q is multiplied by 7.
2. Divide **both sides by 7**: **q = 7**.

**Answer:** **Division property of equality**

**Why this works:** Division undoes multiplication — it's the property that isolates a multiplied variable.

### Example 3 — First step: 4(x − 6) = 5 (Test Q1)

**What is this about:** Identifying the property used when parentheses are expanded.

**Problem:** Which property is used in the **first** step?

```
4(x − 6) = 5
4x − 24 = 5
```

**How to think about it:** The 4 outside the parentheses was multiplied into **each** term inside: **4·x** and **4·(−6)**. That's the **distributive property**.

**Solution (step by step):**
1. Start: **4(x − 6) = 5**.
2. Multiply 4 by x → **4x**. Multiply 4 by −6 → **−24**.
3. Result: **4x − 24 = 5** — this step is **distribution**.

**Answer:** **Distributive property**

**Why this works:** a(b + c) = ab + ac — the factor outside goes to every term inside before you solve.

### Example 4 — Graphic model 8(3x + 40) (Test Q23)

**What is this about:** Reading a diagram that shows arrows from **8** to both terms inside the parentheses.

**Problem:** Arrows from **8** to **3x** and **40** in **8(3x + 40) = 10**. Which property?

**How to think about it:** Arrows mean "multiply 8 by each term" → **8·3x** and **8·40**. That's distribution in picture form.

**Solution (step by step):**
1. The diagram shows **8** connecting to **3x** and **40**.
2. That means **8(3x + 40) = 8·3x + 8·40**.
3. This is the **distributive property of multiplication**.

**Answer:** **Distributive property of multiplication**

**Why this works:** Visual models of distribution show one factor splitting to every term inside parentheses.

### Example 5 — Next step: 12 = −2x (Test Q12)

**What is this about:** Picking the next move after x-terms are already on one side.

**Problem:** Carlton has **−4x + 12 = −6x** → **12 = −2x**. What is the **next** step?

**How to think about it:** Now x is **multiplied by −2**. To get x alone, **divide both sides by −2**.

**Solution (step by step):**
1. Current equation: **12 = −2x**.
2. x has coefficient **−2** (multiplied by −2).
3. Divide **each side by −2**: **x = −6**.

**Answer:** **Divide each side of the equation by −2**

**Why this works:** After moving terms, division clears the coefficient — the last step to isolate x.

### Example 6 — Distribute 5(x + 8) (Test Q16)

**What is this about:** Rewriting an expression using the distributive property.

**Problem:** Rewrite **5(x + 8)** using the distributive property.

**How to think about it:** Send the 5 to **both** x and 8: **5·x + 5·8**.

**Solution (step by step):**
1. **5(x + 8) = 5·x + 5·8**
2. **5·8 = 40**
3. Result: **5x + 40**

**Answer:** **5x + 40**

**Why this works:** Distribution replaces one factored form with an equivalent expanded form — needed before combining like terms.

### Example 7 — 4(x − 6) = 5 full solve (Practice Q — multistep)

**What is this about:** Full solve using distribute → add/subtract → divide.

**Problem:** Solve **4(x − 6) = 5**.

**How to think about it:** Parentheses first (distribute), then undo subtraction, then undo multiplication.

**Solution (step by step):**
1. Distribute: **4x − 24 = 5**.
2. Add 24 to both sides: **4x = 29**.
3. Divide by 4: **x = 29/4**.

**Answer:** **x = 29/4**

**Why this works:** Multi-step solving chains the properties in order — each step gets you closer to "x alone."

### Exam-style practice

---

**1. x + 17 = 42. Best first property?**

**Problem:** Solve **x + 17 = 42**. Which property is best for the first step?

**Solution (step by step):**
1. 17 is **added** to x.
2. Subtract 17 from **both sides** (subtraction property).

**Answer:** **Subtraction property of equality** (subtract 17 from both sides)

---

**2. 6m = 54. Best property?**

**Problem:** Solve **6m = 54**. Which property isolates m?

**Solution (step by step):**
1. m is multiplied by 6.
2. Divide both sides by 6: **m = 9**.

**Answer:** **Division property of equality** → **m = 9**

---

**3. 3(x + 4) = 18. First step?**

**Problem:** Solve **3(x + 4) = 18**. What should you do first?

**Solution (step by step):**
1. Parentheses mean **distribute 3** first.
2. **3x + 12 = 18**.

**Answer:** **Distribute 3** → **3x + 12 = 18**

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
Before you solve a tricky equation, you often need to **clean it up** — that's simplifying. Distribute to remove parentheses, then combine like terms (terms with the same variable). This matters because a messy expression hides what you're really solving; simplifying first makes the next steps obvious. Watch **negative signs** especially — they flip every sign inside the parentheses, and that's where most students slip (like Kadesha in Practice Q3).

### Key Vocabulary
- **Like terms:** same variable(s) and exponent(s); coefficients may differ
- **Coefficient:** numerical factor on a variable term
- **Constant:** term with no variable
- **Distribute negatives:** −1(x − 3) = −x + 3, not −x − 3

[DIAGRAM:distribute_negatives]

[DIAGRAM:combine_like_terms]

### Example 1 — Kadesha's error (Practice Q3) ⚠️ Focus

**What is this about:** Spotting the first sign error when distributing negatives.

**Problem:** Simplify **−(x − 3) − 2(x − 1)**. Kadesha wrote Step 2 as **−x − 3 − 2x − 2**. Where is the first error?

**How to think about it:** A minus in front of parentheses means multiply by **−1** and flip **both** inside signs. Also, **−2(x − 1) = −2x + 2**, not −2x − 2.

**Solution (step by step):**
1. **−(x − 3) = −x + 3** (NOT −x − 3 — Kadesha's first mistake).
2. **−2(x − 1) = −2x + 2** (NOT −2x − 2).
3. Correct Step 2: **−x + 3 − 2x + 2**.
4. Combine: **−3x + 5**.

**Answer:** **First error in Step 2 — should be −x + 3 − 2x + 2**

**Why this works:** Distributing a negative changes **every** sign inside — minus times minus gives plus.

### Example 2 — 6(x − 4) (Test Q6)

**What is this about:** Basic positive distribution.

**Problem:** Which expression is equivalent to **6(x − 4)**?

**How to think about it:** Multiply 6 by **x** and 6 by **−4**.

**Solution (step by step):**
1. **6 · x = 6x**
2. **6 · (−4) = −24**
3. Result: **6x − 24**

**Answer:** **6x − 24**

**Why this works:** The distributive property sends the outside factor to each term inside.

### Example 3 — 7b + 4b − 1b (Test Q8)

**What is this about:** Combining like terms by adding coefficients.

**Problem:** Simplify **7b + 4b − 1b**.

**How to think about it:** All terms are **b** terms — add the numbers in front: 7 + 4 − 1.

**Solution (step by step):**
1. Coefficients: **7 + 4 − 1 = 10**.
2. Keep the variable part: **b**.
3. Result: **10b**.

**Answer:** **10b**

**Why this works:** Like terms share the same variable — only the coefficients combine.

### Example 4 — ½(8x + 4) + ⅓(9 − 3x) (Practice Q8)

**What is this about:** Distributing fractions to every term, then combining.

**Problem:** Simplify **½(8x + 4) + ⅓(9 − 3x)**.

**How to think about it:** Distribute each fraction separately, then combine the x terms and constants.

**Solution (step by step):**
1. **½(8x + 4) = 4x + 2**
2. **⅓(9 − 3x) = 3 − x**
3. Add: **4x + 2 + 3 − x = 3x + 5**

**Answer:** **3x + 5**

**Why this works:** Fractions distribute the same way — multiply the fraction by **each** term inside.

### Example 5 — 9p − 3p + 2 (Test Q19)

**What is this about:** Combining variable terms and leaving the constant alone.

**Problem:** Simplify **9p − 3p + 2**.

**How to think about it:** **9p** and **−3p** are like terms; **2** stays as a constant.

**Solution (step by step):**
1. **9p − 3p = 6p**
2. Add constant: **6p + 2**

**Answer:** **6p + 2**

**Why this works:** Only like terms combine — constants don't mix with p terms.

### Example 6 — Like terms in −a²b + 6ab − 8 + 5a²b − 6a − b (Test Q17)

**What is this about:** Matching terms that share the **exact** variable part.

**Problem:** Which are like terms?

**How to think about it:** **a²b** is different from **ab** or **a**. Look for the same letters **and** same exponents.

**Solution (step by step):**
1. **−a²b** and **5a²b** both have **a²b** — like terms ✓
2. **6ab** has **ab** — not like **a²b**
3. **−6a** has only **a** — different again

**Answer:** **−a²b and 5a²b**

**Why this works:** Like terms must match variable **and** exponent — a²b ≠ ab.

### Example 7 — Constant in −x² − 6y + 13x + 7 (Test Q11)

**What is this about:** Finding a term with **no variable**.

**Problem:** Which number is a **constant**?

**How to think about it:** A constant is a plain number — no letters attached.

**Solution (step by step):**
1. Scan each term: −x² (has x²), −6y (has y), 13x (has x).
2. **7** has no variable — it's a constant.

**Answer:** **7**

**Why this works:** Constants stand alone; variable terms always include a letter.

### Exam-style practice

---

**1. −2(x + 5)**

**Problem:** Simplify **−2(x + 5)**.

**Solution (step by step):**
1. Distribute −2 to x: **−2x**
2. Distribute −2 to 5: **−10**
3. Result: **−2x − 10**

**Answer:** **−2x − 10**

---

**2. 4x + 9x − 2x**

**Problem:** Simplify **4x + 9x − 2x**.

**Solution (step by step):**
1. Add coefficients: **4 + 9 − 2 = 11**
2. Keep **x**: **11x**

**Answer:** **11x**

---

**3. ⅔x + ⅓x + 2 = 5 (Test Q18 first step)**

**Problem:** Solve **⅔x + ⅓x + 2 = 5**. What is a good first step?

**Solution (step by step):**
1. **⅔x + ⅓x** are like terms → **(⅔ + ⅓)x = x**
2. Equation becomes **x + 2 = 5**

**Answer:** **Combine like terms** → **x + 2 = 5**

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
Not every equation has a nice single answer for x. After you simplify fully, three things can happen: you get **one number** for x (one solution), a **false** statement like 5 = 9 (no solution), or a **true** statement that's always true (infinitely many solutions). This matters because on tests like Aanya's problem (Practice Q2), students pick an equation that looks hard but actually has **infinite** solutions — knowing the three outcomes saves you from that trap.

### Key Vocabulary
- **One solution:** exactly one value of x makes the equation true
- **No solution:** simplified equation is false (contradiction)
- **Infinitely many solutions:** both sides are identical (identity)

[DIAGRAM:one_solution]

[DIAGRAM:no_solution_case]

### Example 1 — Aanya's four equations (Practice Q2) ⚠️ Focus

**What is this about:** Comparing four equations to find which has **exactly one** solution.

**Problem:** Which has **exactly one** solution?

**How to think about it:** Simplify each equation completely. If x disappears and you get something false → no solution. If both sides match → infinite. If you can solve for one x → one solution.

**Solution (step by step):**
1. **A.** 6x − 8 = 4(x − 2) + 2x → 6x − 8 = 6x − 8 → **infinitely many**
2. **B.** 3(x − 1) + 2x = 3(x − 1) + 2 → 5x − 3 = 3x − 1 → 2x = 2 → **x = 1** → **one solution** ✓
3. **C.** 7x + 2 − x = 6(x + 2) → 6x + 2 = 6x + 12 → **2 = 12** → **no solution**
4. **D.** 4(x + 3) + x = 5(x + 1) + 7 → 5x + 12 = 5x + 12 → **infinitely many**

**Answer:** **B: 3(x − 1) + 2x = 3(x − 1) + 2**

**Why this works:** Only B simplifies to a single value of x; the others become identities or contradictions.

### Example 2 — Kamal's work (Practice Q22)

**What is this about:** Understanding that a false statement means **no solution**, not "x equals something."

**Problem:**
```
3(x − 8) = x + 2x + 7
3x − 24 = 3x + 7
−24 = 7
```
What is the solution?

**How to think about it:** When all x terms cancel and you're left with **−24 = 7**, that's never true — no x can fix it.

**Solution (step by step):**
1. Kamal simplified correctly to **−24 = 7**.
2. **−24 = 7** is **always false**.
3. No value of x makes this true.

**Answer:** **No solution**

**Why this works:** A contradiction (false statement with no x) means the equation has zero solutions.

### Example 3 — One solution: 9x − 10 = 3x + 2 (Test Q20)

**What is this about:** Standard solve ending with one value for x.

**Problem:** Solve **9x − 10 = 3x + 2**.

**How to think about it:** Move x terms together, constants together, then divide — you'll get exactly one x.

**Solution (step by step):**
1. Subtract 3x: **6x − 10 = 2**
2. Add 10: **6x = 12**
3. Divide by 6: **x = 2**

**Answer:** **One solution: x = 2**

**Why this works:** One x remains after simplifying → exactly one solution.

### Example 4 — Maria: one solution vs none (Test Q4)

**What is this about:** Distributing and solving when variables are on both sides.

**Problem:** **3(x + 6) = 5(x − 4)** → **3x + 18 = 5x − 20**. Solution?

**How to think about it:** Different coefficients on x (3 vs 5) → x won't cancel → one solution.

**Solution (step by step):**
1. **3x + 18 = 5x − 20**
2. Subtract 3x: **18 = 2x − 20**
3. Add 20: **38 = 2x**
4. **x = 19**

**Answer:** **x = 19 (one solution)**

**Why this works:** When x terms don't fully cancel, you solve for a single numeric answer.

### Example 5 — Recognize identity (Practice Q2 — equation A)

**What is this about:** Spotting when both sides simplify to the **same** expression.

**Problem:** Is **6x − 8 = 4(x − 2) + 2x** one, none, or infinite?

**How to think about it:** Distribute and combine — if both sides become identical, every x works.

**Solution (step by step):**
1. Right side: **4(x − 2) + 2x = 4x − 8 + 2x = 6x − 8**
2. Left side: **6x − 8**
3. Both sides match → **infinitely many solutions**

**Answer:** **Infinitely many solutions**

**Why this works:** An identity is true for every x — the equation doesn't restrict x at all.

### Example 6 — 6x + 2 = 9x − 1 (Test Q7)

**What is this about:** Another standard one-solution case.

**Problem:** Solve **6x + 2 = 9x − 1**.

**How to think about it:** Collect x on one side, numbers on the other.

**Solution (step by step):**
1. Subtract 6x: **2 = 3x − 1**
2. Add 1: **3 = 3x**
3. **x = 1**

**Answer:** **One solution: x = 1**

**Why this works:** One x left → one solution.

### Exam-style practice

---

**1. 2x + 5 = 2x + 9**

**Problem:** How many solutions does **2x + 5 = 2x + 9** have?

**Solution (step by step):**
1. Subtract 2x from both sides: **5 = 9**
2. **5 = 9** is false — no x fixes this.

**Answer:** **No solution**

---

**2. 4(x + 1) = 4x + 4**

**Problem:** How many solutions does **4(x + 1) = 4x + 4** have?

**Solution (step by step):**
1. Distribute: **4x + 4 = 4x + 4**
2. Both sides identical — true for every x.

**Answer:** **Infinitely many solutions**

---

**3. 5x − 3 = 2x + 6**

**Problem:** Solve **5x − 3 = 2x + 6** and state the number of solutions.

**Solution (step by step):**
1. Subtract 2x: **3x − 3 = 6**
2. Add 3: **3x = 9**
3. **x = 3** — one value.

**Answer:** **One solution: x = 3**

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
Some equations need several steps before x is alone — that's multi-step solving. Follow a reliable order: distribute parentheses first, combine like terms, move all x terms to one side, move constants to the other, then divide. This matters because doing steps out of order (like combining before distributing in Practice Q17) leads to wrong answers, and fraction/decimal equations use the **same** flow once you stay organized.

### Key Vocabulary
- **Multi-step equation:** needs more than one inverse operation
- **Variables on both sides:** x terms appear left and right
- **Efficient first step:** distribute before moving isolated constants inside parentheses

[DIAGRAM:multistep_flow]

[DIAGRAM:variables_both_sides]

### Example 1 — First step: 4x + 3(x + 2) = 5(2x − 3) (Practice Q17)

**What is this about:** Picking the smartest **first** move when parentheses are on both sides.

**Problem:** Reasonable **first** step?

**How to think about it:** You can't combine **4x** with **x** inside the parentheses until you distribute. Clear the parentheses first.

**Solution (step by step):**
1. See **3(x + 2)** and **5(2x − 3)** — parentheses block combining.
2. **Distribute 3** to (x + 2) and **5** to (2x − 3).
3. Do **not** combine 4x and x before distributing.

**Answer:** **Distribute the 3 to x + 2, and the 5 to (2x − 3)**

**Why this works:** Distribution removes parentheses so like terms can actually be combined.

### Example 2 — Maria's equation (Test Q4)

**What is this about:** Full solve after distributing.

**Problem:** **3(x + 6) = 5(x − 4)**. Find x.

**How to think about it:** Distribute, then move x terms and constants.

**Solution (step by step):**
1. Distribute: **3x + 18 = 5x − 20**
2. Subtract 3x: **18 = 2x − 20**
3. Add 20: **38 = 2x**
4. **x = 19**

**Answer:** **x = 19**

**Why this works:** Standard multi-step flow — distribute, isolate x, divide.

### Example 3 — 3x − 10 = 2x + 5 (Practice Q18)

**What is this about:** Translating words into an equation and solving.

**Problem:** Three times a number minus ten equals twice the number plus five. Find x.

**How to think about it:** "Three times a number" → **3x**; "twice the number plus five" → **2x + 5**.

**Solution (step by step):**
1. Write: **3x − 10 = 2x + 5**
2. Subtract 2x: **x − 10 = 5**
3. Add 10: **x = 15**

**Answer:** **x = 15**

**Why this works:** Moving x terms to one side leaves a simple one-step solve.

### Example 4 — Leonardo's fraction error (Practice Q15) ⚠️ Focus

**What is this about:** Finding a fraction addition mistake mid-solve.

**Problem:** Leonardo solves **4(x − ⅕) = 2⅔**. In Step 3 he writes **4/5 = 16/15** when adding fractions. Where is the error?

**How to think about it:** When adding fractions, common denominators must be correct. **4/5 = 12/15**, not 16/15.

**Solution (step by step):**
1. Step 2: **4x = 8/3 + 4/5** — correct setup.
2. Convert **4/5** to fifteenths: **4/5 = 12/15** (multiply top and bottom by 3).
3. Leonardo wrote **16/15** — that's wrong.

**Answer:** **Error in Step 3** — 4/5 should be 12/15

**Why this works:** LCD errors throw off the entire solution — always check fraction conversion.

### Example 5 — Carey combines terms (Test Q2)

**What is this about:** Knowing **which** terms to combine after distributing.

**Problem:** **4(2x − 1) + 5 = 3 + 2(x + 1)** → **8x − 4 + 5 = 3 + 2x + 2**. Which terms should Carey combine?

**How to think about it:** Combine **constants with constants** on each side before tackling x terms.

**Solution (step by step):**
1. Left constants: **−4 + 5**
2. Right constants: **3 + 2**
3. Save **8x** and **2x** for the next step (or combine x terms after constants).

**Answer:** **−4 + 5 and 3 + 2**

**Why this works:** Simplify each side fully — constants and like variable terms separately.

### Example 6 — 7(x − 3) = 28 (Test Q13)

**What is this about:** Classic distribute → add → divide pattern.

**Problem:** Follow the steps for **7(x − 3) = 28**.

**How to think about it:** Three clean steps: distribute, undo subtraction, undo multiplication.

**Solution (step by step):**
1. Distribute: **7x − 21 = 28**
2. Add 21: **7x = 49**
3. Divide by 7: **x = 7**

**Answer:** **x = 7**

**Why this works:** Each inverse operation undoes one part of the expression.

### Example 7 — 0.45(x + 1.6) + 5x = 18 (Practice Q20)

**What is this about:** Decimals follow the same steps — distribute carefully.

**Problem:** Find x (nearest hundredth).

**How to think about it:** Distribute 0.45, combine x terms, then divide.

**Solution (step by step):**
1. Distribute: **0.45x + 0.72 + 5x = 18**
2. Combine x: **5.45x + 0.72 = 18**
3. Subtract 0.72: **5.45x = 17.28**
4. Divide: **x ≈ 3.17**

**Answer:** **x ≈ 3.17**

**Why this works:** Decimals don't change the strategy — only the arithmetic care.

### Example 8 — Decimal both sides (Practice Q9)

**What is this about:** Planning steps for variables on both sides with decimals.

**Problem:** Steps for **−1.3 + 4.6x = 0.3 + 4x**?

**How to think about it:** Move constants together, x terms together, then divide.

**Solution (step by step):**
1. **Add 1.3** to both sides (clear −1.3 on left).
2. **Subtract 4x** from both sides (collect x on left).
3. **Divide** by the coefficient of x.

**Answer:** **Add 1.3, subtract 4x, then divide by coefficient of x**

**Why this works:** Same three-move pattern works for decimals and fractions.

### Example 9 — 3.7x − 18 = −4.3x − 34 (Test Q9)

**What is this about:** Efficient first step when x is on both sides.

**Problem:** Most efficient **first** step?

**How to think about it:** Get all x terms on one side — add **4.3x** to both sides.

**Solution (step by step):**
1. x appears as **3.7x** and **−4.3x**.
2. Add **4.3x** to both sides → **8x − 18 = −34**.

**Answer:** **Add 4.3x to both sides**

**Why this works:** Collecting x terms early prevents bouncing back and forth.

### Example 10 — 2(x + 6) = 3(x − 4) + 5 (Test Q15)

**What is this about:** Distribute on both sides before anything else.

**Problem:** Reasonable first step?

**How to think about it:** Parentheses on both sides → distribute first.

**Solution (step by step):**
1. Left: **2(x + 6)** needs distribution.
2. Right: **3(x − 4)** needs distribution.
3. **Distribute 2** to (x + 6) and **3** to (x − 4).

**Answer:** **Distribute 2 to (x + 6) and 3 to (x − 4)**

**Why this works:** You can't combine or move terms hidden inside parentheses.

### Exam-style practice

---

**1. 4(2x − 1) + 5 = 3 + 2(x + 1). After distributing, combine constants.**

**Problem:** After distributing both sides of **4(2x − 1) + 5 = 3 + 2(x + 1)**, what are the simplified constant terms?

**Solution (step by step):**
1. Left: **8x − 4 + 5** → constants **−4 + 5 = 1**
2. Right: **3 + 2x + 2** → constants **3 + 2 = 5**
3. Equation: **8x + 1 = 2x + 5**

**Answer:** Left constant **1**; Right constant **5**

---

**2. Ronin: 4(x + 2) = 96 (Practice Q12). Find x.**

**Problem:** Solve **4(x + 2) = 96**.

**Solution (step by step):**
1. Divide both sides by 4: **x + 2 = 24**
2. Subtract 2: **x = 22**

**Answer:** **x = 22**

---

**3. Antwan: 3(⅓x + 1) + 4 = −1 − 4(x + 3) (Practice Q11). Constants after moving terms?**

**Problem:** After distributing and moving terms in **3(⅓x + 1) + 4 = −1 − 4(x + 3)**, what constant appears on one side?

**Solution (step by step):**
1. Distribute: **x + 3 + 4 = −1 − 4x − 12**
2. Simplify: **x + 7 = −4x − 13**
3. Add 4x: **5x + 7 = −13**
4. Subtract 7: **5x = −20** → **x = −4**

**Answer:** After moving terms, **5x = −20** (constant **−20** on the right)

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
Real-world problems and standard-form equations (Ax + By = C) show up together because stories become algebra, and algebra sometimes needs rearranging before you can use it. For word problems, always **name your variable first**, then translate each sentence into math. For standard form, move terms to get the variable you want **alone** on one side. This matters on tests like the hockey tournament (Practice Q7) and solving for x vs y traps (Test Q14) — setup is half the battle.

### Key Vocabulary
- **Standard form:** Ax + By = C (A, B, C integers; A ≥ 0 often)
- **Solve for y:** rewrite with y alone on one side
- **Equivalent equation:** same solution set; different form
- **Perimeter:** sum of all side lengths

[DIAGRAM:solve_for_y]

[DIAGRAM:word_problem_setup]

### Example 1 — 9y − 12x = 36, solve for y (Practice Q6)

**What is this about:** First step when y is on the left mixed with an x-term.

**Problem:** First step when solving for **y**?

**How to think about it:** You want y alone. The **−12x** is in the way — move it to the other side by adding 12x.

**Solution (step by step):**
1. Start: **9y − 12x = 36**
2. **Add 12x** to both sides: **9y = 12x + 36**
3. Next (not asked): divide by 9 for **y = (12x + 36)/9**

**Answer:** **Add 12x to both sides of the equation**

**Why this works:** To isolate y, first remove other variables from y's side.

### Example 2 — Leah: 3x + 4y = 8 (Test Q3)

**What is this about:** Next step after x-terms are already on the other side.

**Problem:** Leah has **4y = 8 − 3x**. What is her **next** step to solve for y?

**How to think about it:** y is multiplied by 4 — divide both sides by 4.

**Solution (step by step):**
1. Current: **4y = 8 − 3x**
2. **Divide both sides by 4**: **y = 2 − (3/4)x**

**Answer:** **Divide both sides of the equation by 4**

**Why this works:** Division clears the coefficient on y.

### Example 3 — Tonya x = 150 − 6y (Practice Q5)

**What is this about:** Rewriting an equation into standard form.

**Problem:** Which is equivalent to **x = 150 − 6y**?

**How to think about it:** Standard form has x and y on the same side. Add **6y** to both sides.

**Solution (step by step):**
1. **x = 150 − 6y**
2. Add 6y: **x + 6y = 150**

**Answer:** **x + 6y = 150**

**Why this works:** Equivalent equations have the same solutions — just rearranged.

### Example 4 — Hockey tournament (Practice Q7)

**What is this about:** Writing an equation from a story with three teams' scores.

**Problem:** Fins score **x** goals. Seals score **3 less than twice** Fins. Rays score **2 more** than Fins. Total **11** goals. Find each team.

**How to think about it:** Build each team's score from x, then add them for total 11.

**Solution (step by step):**
1. Fins: **x**
2. Seals: **2x − 3** (twice Fins, minus 3)
3. Rays: **x + 2** (2 more than Fins)
4. Total: **x + (2x − 3) + (x + 2) = 11**
5. Simplify: **4x − 1 = 11** → **x = 3**
6. Fins: 3, Seals: 3, Rays: 5

**Answer:** **x + (2x − 3) + (x + 2) = 11**; Fins 3, Seals 3, Rays 5

**Why this works:** One variable (x) represents Fins; everything else follows from the story.

### Example 5 — Square vs triangle perimeter (Test Q5)

**What is this about:** Setting equal perimeters from different shapes.

**Problem:** Square side **x**, equilateral triangle side **x + 1**. Perimeters equal. Find equation for x.

**How to think about it:** Square has **4** equal sides; triangle has **3** equal sides.

**Solution (step by step):**
1. Square perimeter: **4x**
2. Triangle perimeter: **3(x + 1)**
3. Set equal: **4x = 3(x + 1)**

**Answer:** **4x = 3(x + 1)**

**Why this works:** "Same perimeter" means the two expressions are equal.

### Example 6 — Micah and Aria ages (Practice Q13)

**What is this about:** Age problems with "twice as old plus" language.

**Problem:** Sum of ages is **29**. Aria is **5 years older than twice** Micah's age. Micah = x.

**How to think about it:** Micah is x; Aria is **2x + 5**; together they make 29.

**Solution (step by step):**
1. Micah: **x**
2. Aria: **2x + 5**
3. Sum: **x + (2x + 5) = 29**

**Answer:** **x + (2x + 5) = 29**

**Why this works:** "Twice Micah plus 5" translates directly to **2x + 5**.

### Example 7 — Rug rental (Test Q10)

**What is this about:** Cost = rate × time plus fixed fee.

**Problem:** **$23** per day plus **$45** checkout fee. Total **$137**. Find days d.

**How to think about it:** Daily cost **23d** plus one-time fee **45** equals total **137**.

**Solution (step by step):**
1. **23d + 45 = 137**
2. Subtract 45: **23d = 92**
3. Divide: **d = 4**

**Answer:** **23d + 45 = 137**; **4 days**

**Why this works:** Rate × quantity + fixed fee is a classic linear model.

### Example 8 — Solve for x: 5x − 10y = 30 (Test Q14) ⚠️ Focus

**What is this about:** Avoiding the trap of subtracting x when you want to **keep** x on the left.

**Problem:** First step when solving for **x**?

**How to think about it:** x is already on the left — move the **y-term** away by adding 10y. Do **not** subtract 5x.

**Solution (step by step):**
1. **5x − 10y = 30** — solving for **x**
2. **Add 10y** to both sides: **5x = 10y + 30**
3. (Next: divide by 5)

**Answer:** **Add 10y to both sides**

**Why this works:** Move the *other* variable, not the one you're solving for.

### Example 9 — Ronin's square (Practice Q12)

**What is this about:** Perimeter equation with expression side length.

**Problem:** Square side **(x + 2)** in., perimeter **96** in. **4(x + 2) = 96**. Find x.

**How to think about it:** Four sides, each **(x + 2)**, total 96.

**Solution (step by step):**
1. **4(x + 2) = 96**
2. Divide by 4: **x + 2 = 24**
3. **x = 22**

**Answer:** **x = 22**

**Why this works:** Perimeter = 4 × side length, even when the side is an expression.

### Exam-style practice

---

**1. 2x + 5y = 20. Solve for y.**

**Problem:** Rewrite **2x + 5y = 20** with y alone on one side.

**Solution (step by step):**
1. Subtract 2x: **5y = 20 − 2x**
2. Divide by 5: **y = (20 − 2x)/5** or **y = 4 − (2/5)x**

**Answer:** **y = (20 − 2x)/5** or **y = 4 − (2/5)x**

---

**2. Three partners: ¼ + ⅖ + x = 1 (Practice Q10). Third share?**

**Problem:** Three partners split 100% of a business. First gets ¼, second gets ⅖, third gets x. Find x.

**Solution (step by step):**
1. **¼ + ⅖ + x = 1**
2. Common denominator 20: **5/20 + 8/20 + x = 1**
3. **13/20 + x = 1** → **x = 7/20**

**Answer:** **x = 7/20**

---

**3. Tristanne: 23d + 45 = 137. Days?**

**Problem:** Rental costs $23 per day plus $45 fee. Total $137. Find d.

**Solution (step by step):**
1. **23d + 45 = 137**
2. **23d = 92**
3. **d = 4**

**Answer:** **d = 4**

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
