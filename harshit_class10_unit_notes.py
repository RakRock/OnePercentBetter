"""Teaching notes / unit guides for Class 10 Mathematics (parent-led intro)."""

from __future__ import annotations

from typing import Any

import harshit_class10_units as h10u

# Each unit may define ordered sections with markdown body (plain + Unicode math).
UNIT_GUIDES: dict[int, dict[str, Any]] = {
    2: {
        "title": "Polynomials — Unit Guide",
        "subtitle": "NCERT Chapter 2 · Read together before practice",
        "sections": [
            {
                "id": "overview",
                "title": "What this chapter is about",
                "body": """
**Unit 2 — Polynomials** builds on Class 9 and focuses on **zeroes** of polynomials: finding them,
understanding them on a **graph**, and linking them to the **coefficients** in the equation.

A **polynomial** is an expression in one variable (like x) where every exponent is a **whole number**
(0, 1, 2, 3, …).

**Examples:** `3x² − 5x + 2`, `x³ + 4x − 1`  
**Not polynomials:** `1/x`, `√x + 2`, `2/(x + 3)`

The central idea:

> **Zeroes** are the values of x that make `p(x) = 0`. On a graph they are **x-intercepts**.
> The numbers **a, b, c** in `ax² + bx + c` tell us about those zeroes without always drawing the graph.

This chapter prepares **Unit 4 (Quadratic Equations)**, where solving `ax² + bx + c = 0` is the same as
finding zeroes of a quadratic polynomial.
""",
            },
            {
                "id": "topics",
                "title": "Four topics in this unit",
                "body": """
### 1. Types & degree of polynomials 📐

- **Degree** = highest power of x (`5x³ − 4x + 7` → degree **3**)
- **Linear** (degree 1): `2x − 3`
- **Quadratic** (degree 2): `ax² + bx + c`, **a ≠ 0**
- **Cubic** (degree 3): `ax³ + bx² + cx + d`
- Know what **is** and **is not** a polynomial

---

### 2. Geometrical meaning of zeroes 📈

- **Zero** of `p(x)` → number k with **p(k) = 0**
- On a graph → where the curve meets the **x-axis**
- **Linear:** exactly **1** zero
- **Quadratic (parabola):** **0, 1, or 2** zeroes
  - above/below axis → no zero
  - touches axis → one repeated zero
  - cuts twice → two distinct zeroes

---

### 3. Zeroes & coefficients 🔗 *(heart of the chapter)*

For **ax² + bx + c** with zeroes **α, β**:

| | |
|--|--|
| Sum | **α + β = −b/a** |
| Product | **αβ = c/a** |

**Monic** `x² + bx + c`: sum = **−b**, product = **c**

**Skills:** factorise → find zeroes → verify sum/product; build a quadratic from given zeroes;
handle surds like `(5 − 2√3)` and `(5 + 2√3)`; expressions like **1/α + 1/β**.

---

### 4. Division algorithm ➗

- Remainder when dividing by **(x − a)** equals **p(a)**
- **(x − a)** is a factor ⟺ **p(a) = 0**
- For **cubics:** if `(x − 1)` is a factor, **divide** to get a quadratic, then factorise for all three zeroes
""",
            },
            {
                "id": "ncert",
                "title": "How NCERT organises the chapter",
                "body": """
| Section | Content |
|---------|---------|
| **2.1 Introduction** | Degree, types, value p(k), definition of a zero |
| **2.2 Geometrical meaning** | Graphs of linear & quadratic; zeroes as x-intercepts |
| **2.3 Zeroes & coefficients** | Sum/product relations; forming quadratics |
| **2.4 Summary** | Key ideas; division algorithm (from Class 9) |

**By the end of the unit** Harshit should be able to:

1. Identify degree and type of a polynomial  
2. Explain zeroes in words, by algebra, and on a graph  
3. Use **α + β** and **αβ** for quadratics  
4. Factorise quadratics (and cubics after division)  
5. Form a quadratic from given zeroes or sum/product  
6. Use division / factor theorem when one factor of a cubic is known  

**Not in this unit:** pair of linear equations (Unit 3), full quadratic-equation word problems (Unit 4).
""",
            },
            {
                "id": "formulas",
                "title": "Formula sheet — get these comfortable",
                "body": """
### Basics

| Concept | Rule |
|---------|------|
| Zero of p(x) | **p(k) = 0** |
| Value at x = k | Substitute k → **p(k)** |

---

### Quadratic **ax² + bx + c** (zeroes α, β)

| | Formula |
|--|---------|
| Sum | **α + β = −b/a** |
| Product | **αβ = c/a** |

**Monic x² + bx + c:** sum = **−b**, product = **c**

**Build monic quadratic** from sum **S** and product **P:**

`x² − Sx + P`

**From zeroes α, β:** `a(x − α)(x − β)`

---

### Useful extras

| Situation | Rule |
|-----------|------|
| **1/α + 1/β** | **(α + β) / (αβ)** |
| Zeroes **1/α, 1/β** | new sum = **(α+β)/(αβ)**, new product = **1/(αβ)** |
| Reciprocal zeroes | **αβ = 1** |
| Equal zeroes | **b² − 4ac = 0** |

---

### Identities (factorisation)

- **a² − b² = (a − b)(a + b)**
- **(x + a)(x + b) = x² + (a+b)x + ab**

Irrational pair **(p − q)** and **(p + q):** sum = **2p**, product = **p² − q**

---

### Division & factors

| Theorem | Rule |
|---------|------|
| Remainder | Divide by **(x − a)** → remainder **p(a)** |
| Factor | **(x − a)** factor ⟺ **p(a) = 0** |

---

### Cubic **ax³ + bx² + cx + d** (zeroes α, β, γ)

| | Formula |
|--|---------|
| α + β + γ | **−b/a** |
| αβ + βγ + γα | **c/a** |
| αβγ | **−d/a** |

*(Use mainly to **verify** zeroes after factorisation.)*

---

### Quick reference (one line each)

```
α+β = −b/a     αβ = c/a     x² − (sum)x + (product)
1/α + 1/β = (α+β)/(αβ)     equal zeroes ⇒ b²−4ac = 0
remainder ÷ (x−a) = p(a)     (x−a) factor ⇔ p(a) = 0
```
""",
            },
            {
                "id": "teaching",
                "title": "Suggested teaching order",
                "body": """
A comfortable order before starting **Practice** in the app:

| Step | Focus | ~Time |
|------|--------|-------|
| 1 | Degree, types, “zero = x-intercept” | 15 min |
| 2 | Sum/product formulas + factorise + verify | 25 min |
| 3 | 1/α + 1/β, surd zeroes, reciprocal zeroes | 20 min |
| 4 | One cubic example with division | 20 min |
| 5 | Quick oral check: 2–3 examples on paper | 10 min |

Then use **Week Setup** to pick topics & levels, run **Practice**, and later the **Unit Test** when ready.

**One sentence for Harshit:**

> *Polynomials is about expressions in x — finding where they equal zero, seeing that on a graph,
> and using a, b, c to get those zeroes quickly.*
""",
            },
        ],
    },
    3: {
        "title": "Pair of Linear Equations — Unit Guide",
        "subtitle": "NCERT Chapter 3 · Read together before practice",
        "sections": [
            {
                "id": "overview",
                "title": "What this chapter is about",
                "body": """
**Unit 3** is about **two unknown numbers** (usually called **x** and **y**) that must satisfy **two
rules at the same time**.

**Real-life idea:**  
Akhila goes to a fair. Rides cost ₹3 each and Hoopla costs ₹4 per game. She spends ₹20 total,
and she played Hoopla **half as many times** as she took rides. How many rides? How many Hoopla games?

You write **two equations** with the same x and y — that is a **pair of linear equations in two variables**.

**Linear equation** = equation where x and y appear only to the **first power** (no x², no xy).

**Standard form:** `a₁x + b₁y + c₁ = 0` and `a₂x + b₂y + c₂ = 0`

**The big question of the chapter:**

> Where do the two rules **agree**? That common (x, y) is the **solution** — on a graph, it is where
> the two **lines meet** (if they meet at all).

You already saw one-variable linear equations in Class 9. Now there are **two** variables, so you need
**two** equations to pin down both numbers.
""",
            },
            {
                "id": "topics",
                "title": "Four topics in this unit",
                "body": """
### 1. Graphs & what solutions mean 📊

Picture each equation as a **straight line** on a graph.

| What the lines look like | What it means |
|--------------------------|---------------|
| **Cross at one point** | **One solution** — one pair (x, y) works |
| **Parallel** (same slope, never meet) | **No solution** — impossible pair |
| **Same line** (coincident) | **Infinitely many** solutions — every point on the line works |

**Consistent** = at least one solution. **Inconsistent** = no solution.

---

### 2. Substitution method 🔄

**Idea:** From one equation, write **x = …** or **y = …**, then **plug into** the other equation.

**Example:** `x + y = 7` and `x − y = 3`  
Add the equations → `2x = 10` → **x = 5**, then **y = 2**.

Good when one equation is easy to rearrange (like `y = x/2`).

---

### 3. Elimination method ➖

**Idea:** Make the **x** or **y** coefficients match (or opposite), then **add or subtract** the
equations so one variable **disappears**.

**Example:**  
`2x + y = 6` and `2x − y = 2` → subtract → `2y = 4` → **y = 2**, then **x = 2**.

Often faster than substitution when coefficients line up nicely.

---

### 4. Word problems & cross-multiplication ✖️

**Word problems:** Turn the story into two equations — ages, money, ratios, digits, notes (₹50 vs ₹100).

**Cross-multiplication** (shortcut when you know the formula): one shot at x and y without long steps.
Useful in practice and some board questions after you understand substitution and elimination.
""",
            },
            {
                "id": "ncert",
                "title": "How NCERT organises the chapter",
                "body": """
| Section | Content |
|---------|---------|
| **3.1 Introduction** | Fair / pocket-money type stories → two equations |
| **3.2 Graphical method** | Draw lines; intersect / parallel / coincident |
| **3.3 Algebraic methods** | **3.3.1 Substitution** · **3.3.2 Elimination** |
| **3.4 Summary** | Ratio test for consistent / inconsistent / dependent |

**By the end of the unit** Harshit should be able to:

1. Say whether a pair has **0, 1, or infinitely many** solutions (graph or ratios)  
2. **Solve** a simple pair by **substitution** or **elimination**  
3. **Sketch or read** graphs to find where lines meet  
4. Set up **two equations** from a short word problem (income, age, digits, etc.)  
5. Find **k** when lines are parallel or coincident  

**Comes next:** **Unit 4 — Quadratic Equations** (one variable, degree 2). Unit 3 stays with **lines**
and **two unknowns**.
""",
            },
            {
                "id": "formulas",
                "title": "Formula sheet — get these comfortable",
                "body": """
### Standard form

Two lines:

`a₁x + b₁y + c₁ = 0`  
`a₂x + b₂y + c₂ = 0`

---

### Which case am I in? (ratio test)

Compare **a₁/a₂**, **b₁/b₂**, **c₁/c₂** (when denominators are non-zero):

| Condition | Lines | Solutions |
|-----------|-------|-----------|
| **a₁/a₂ ≠ b₁/b₂** | Intersect | **One** (unique) |
| **a₁/a₂ = b₁/b₂ ≠ c₁/c₂** | Parallel | **None** |
| **a₁/a₂ = b₁/b₂ = c₁/c₂** | Coincident | **Infinitely many** |

**Parallel lines:** same direction → often **a₁/a₂ = b₁/b₂** but **c** ratios do not match.  
**Not parallel:** **a₁/a₂ ≠ b₁/b₂** (e.g. find **k** so slopes differ).

---

### Substitution — steps

1. From one equation: **x = …** or **y = …**  
2. Substitute into the **other** equation  
3. Solve for one variable  
4. Back-substitute to get the second  

---

### Elimination — steps

1. Multiply one or both equations so one variable has the **same or opposite** coefficient  
2. **Add** (to eliminate) or **subtract**  
3. Solve for the remaining variable  
4. Plug back to find the other  

---

### Cross-multiplication (for `a₁x + b₁y + c₁ = 0` and `a₂x + b₂y + c₂ = 0`)

When lines are **not parallel** (denominator ≠ 0):

```
x     y     1
───────── = ───────── = ─────────
(b₁c₂−b₂c₁) (c₁a₂−c₂a₁) (a₁b₂−a₂b₁)
```

So:

**x = (b₁c₂ − b₂c₁) / (a₁b₂ − a₂b₁)**  
**y = (c₁a₂ − c₂a₁) / (a₁b₂ − a₂b₁)**

Memorise the pattern after you can do substitution and elimination by hand.

---

### Graph & area (board-style)

- **Intersection point** = solve the pair (algebra or graph)  
- **Triangle with x-axis:** often need **x-intercepts** of the lines + intersection point  
- **Area** = ½ × base × height (pick base on x-axis when asked)

---

### Quick reference

```
Unique solution     → lines cross once
No solution         → parallel
Infinite solutions  → same line (coincident)
Add equations       → sometimes fastest (x or y cancels)
Word problem        → define x, y in words first, then two equations
```
""",
            },
            {
                "id": "teaching",
                "title": "Suggested teaching order",
                "body": """
A comfortable order **before Practice** — use paper and a simple graph sketch:

| Step | Focus | ~Time |
|------|--------|-------|
| 1 | What x and y mean; one example story → two equations | 15 min |
| 2 | Three line pictures: cross / parallel / same line | 15 min |
| 3 | Substitution on `x+y=7`, `x−y=3` | 20 min |
| 4 | Elimination on `2x+y=6`, `2x−y=2` | 20 min |
| 5 | Ratio test: one “find k” parallel / coincident question | 15 min |
| 6 | One word problem (e.g. incomes in ratio, same savings) | 20 min |

**Tips for Harshit’s age (Class 10):**

- Always **label** what x and y stand for (“x = number of rides”).  
- After solving, **check** in **both** original equations.  
- For graphs: only **two** points needed per line to draw it (find x when y=0 and y when x=0).  
- Do not rush to cross-multiplication until substitution/elimination feel natural.

Then open **Week Setup**, pick all four topics at levels B–C, and start **Practice**.

**One sentence for Harshit:**

> *Two rules, two unknowns — find the one (x, y) that makes both true, or see from the graph
> whether the lines meet, run parallel, or are the same line.*
""",
            },
        ],
    },
    5: {
        "title": "Arithmetic Progressions — Unit Guide",
        "subtitle": "NCERT Chapter 5 · Read together before practice",
        "sections": [
            {
                "id": "overview",
                "title": "What this chapter is about",
                "body": """
**Unit 5** is about **patterns where you keep adding the same number** each time.

**Real-life idea:**  
Reena starts a job at **₹8000** per month. Every year her salary goes up by **₹500**. Her salaries for year 1, 2, 3, … are:

`8000, 8500, 9000, 9500, …`

Each new term = previous term **+ 500**. That fixed step is the **common difference** **d**.

**Arithmetic Progression (AP)** = a list of numbers where each term (after the first) is obtained by adding the **same fixed number** **d** to the term before it.

**First term** = **a** (or a₁)  
**Common difference** = **d** (can be **positive**, **negative**, or **zero**)

**General form:** `a, a + d, a + 2d, a + 3d, …`

**Not an AP:** `2, 4, 8, 16, …` (multiply by 2 each time — that is a **geometric** pattern, not arithmetic).

**The big questions of the chapter:**

> 1. Is this list an AP? What are **a** and **d**?  
> 2. What is the **nth term**?  
> 3. What is the **sum of the first n terms**?  
> 4. How do we use this in **daily-life** problems (salary, rows of plants, savings)?
""",
            },
            {
                "id": "topics",
                "title": "Four topics in this unit",
                "body": """
### 1. Patterns & definition 📈

- Spot a **constant difference** between consecutive terms  
- Find **a** (first term) and **d** (common difference)  
- Decide if a list **is** or **is not** an AP  
- **Finite AP** = has a last term · **Infinite AP** = goes on forever  

---

### 2. nth term 🔢

**Formula:** **aₙ = a + (n − 1)d**

- Find the **10th term**, **15th term**, etc.  
- Find **which term** equals a given number (solve for **n**)  
- Find **a** and **d** when two terms are given (e.g. 3rd term = 5, 7th term = 9)  
- **Term from the end:** reverse the AP or use total number of terms first  

---

### 3. Sum of first n terms ➕

**Formulas:**

- **Sₙ = n/2 [2a + (n − 1)d]**  
- **Sₙ = n/2 (a + l)** when the **last term l** is known  

Use when the question asks for **total**, **sum**, or **all terms added**.

---

### 4. Word problems 🌱

Turn the story into an AP:

| Story | Often becomes |
|-------|----------------|
| Salary + fixed raise each year | a = starting amount, d = increment |
| Rows of plants decreasing by 2 each row | a = first row, d = −2 |
| Simple interest each year | Interests form an AP |
| Numbers divisible by 3 | AP with d = 3 |

Always **define** what **n** means (which year? which row?).
""",
            },
            {
                "id": "ncert",
                "title": "How NCERT organises the chapter",
                "body": """
| Section | Content |
|---------|---------|
| **5.1 Introduction** | Patterns in nature and daily life |
| **5.2 Arithmetic Progressions** | Definition, a and d, finite vs infinite |
| **5.3 nth Term of an AP** | Formula aₙ = a + (n − 1)d |
| **5.4 Sum of First n Terms** | Sₙ formulas and applications |

**By the end of the unit** Harshit should be able to:

1. Test whether a list is an AP and find **a**, **d**  
2. Find any **nth term** and **which term** equals a given value  
3. Find **Sₙ** using the correct formula  
4. Solve **word problems** (salary, rows, savings, divisible numbers)  
5. Handle **terms from the end** of a finite AP  

**Comes next:** **Unit 6 — Triangles** (geometry). Unit 5 is pure **number patterns** and **algebra**.
""",
            },
            {
                "id": "formulas",
                "title": "Formula sheet — get these comfortable",
                "body": """
### Check if a list is an AP

Compute **a₂ − a₁**, **a₃ − a₂**, **a₄ − a₃**, …  
If **all equal** → AP with that common difference **d**.  
If **not equal** → **not** an AP.

---

### nth term

**aₙ = a + (n − 1)d**

Also written: **l = a + (n − 1)d** when **l** is the **last term**.

**Find n when a term is given:**

Set **aₙ = given value** and solve the linear equation for **n**.  
**n must be a positive integer** for the term to belong to the list.

---

### Sum of first n terms

**Sₙ = n/2 [2a + (n − 1)d]**

**Sₙ = n/2 (a + l)**  ← use when last term **l** is known

---

### Useful special cases

| Question type | Quick approach |
|---------------|----------------|
| Two-digit numbers divisible by k | AP from smallest to largest 2-digit multiple |
| 3rd term = p, 7th term = q | a + 2d = p, a + 6d = q → solve pair |
| Term from the end | Reverse AP: new a = old last term, new d = −old d |
| Simple interest | Interest each year forms AP with d = P×R/100 |

---

### Quick reference

```
AP          → constant difference d
aₙ          → a + (n−1)d
Sₙ          → n/2[2a + (n−1)d]  OR  n/2(a + l)
Not AP      → 2, 4, 8, 16 (×2 each time)
Check n     → must be a positive whole number
Word problem → write a, d, and what n stands for first
```
""",
            },
            {
                "id": "teaching",
                "title": "Suggested teaching order",
                "body": """
A comfortable order **before Practice**:

| Step | Focus | ~Time |
|------|--------|-------|
| 1 | Spot +500 / −2 patterns; define a and d | 15 min |
| 2 | “Is this an AP?” — yes/no with reason | 15 min |
| 3 | aₙ = a + (n−1)d — find 10th term | 20 min |
| 4 | Find n when term = −81 (NCERT Example 4) | 20 min |
| 5 | Sₙ formula — sum of first 10 terms | 20 min |
| 6 | One word problem (rows of plants or salary) | 20 min |

**Tips for Harshit’s age (Class 10):**

- Write **a**, **d**, and **n** at the top of every problem before substituting.  
- For “is it an AP?”, check **at least two** consecutive differences — one match is not enough.  
- When solving for **n**, reject answers that are **not positive integers**.  
- For sums, ask: “Do I know the **last term**?” → if yes, use **n/2(a + l)**.

Then open **Week Setup**, pick all four topics at levels B–C, and start **Practice**. Try the **Unit Test** when formulas feel solid.

**One sentence for Harshit:**

> *An AP adds the same number every step — find any term with a + (n−1)d, find the total with Sₙ, and always check your story makes sense.*
""",
            },
        ],
    },
    6: {
        "title": "Triangles — Unit Guide",
        "subtitle": "NCERT Chapter 6 · Read together before practice",
        "sections": [
            {
                "id": "overview",
                "title": "What this chapter is about",
                "body": """
**Unit 6** is about **similar figures** — same **shape**, not necessarily the same **size**.

**Real-life idea:**  
A photographer enlarges a 35 mm photo to 45 mm. Every line in the big photo is **45/35** times the small one. The **angles stay the same**; only lengths scale. That is **similarity**.

**Congruent** = same shape **and** same size.  
**Similar** = same shape, sides in a **fixed ratio** (scale factor).

**The big ideas of the chapter:**

> 1. When is a line **parallel** to a triangle side? → **BPT** (Basic Proportionality Theorem)  
> 2. When are two triangles **similar**? → **AAA**, **SSS**, **SAS** criteria  
> 3. How do we use similarity for **height of a tower**, **shadow problems**, and a proof of **Pythagoras**?
""",
            },
            {
                "id": "topics",
                "title": "Four topics in this unit",
                "body": """
### 1. Similar figures & scale factor 🔺

- Congruent ⇒ similar, but **not** the reverse  
- **Scale factor** = ratio of corresponding sides (e.g. 2:3)  
- Similar polygons: **equal angles** + **proportional sides**  

---

### 2. Basic Proportionality Theorem (BPT) 📏

**Theorem 6.1:** If DE ∥ BC in ΔABC, then **AD/DB = AE/EC**.

**Converse (6.2):** If **AD/DB = AE/EC**, then **DE ∥ BC**.

Use for finding a missing segment or checking parallelism.

---

### 3. Similarity criteria △

| Criterion | What you need |
|-----------|----------------|
| **AAA / AA** | Corresponding angles equal |
| **SSS** | All three pairs of sides proportional |
| **SAS** | One equal angle + sides **including** it proportional |

Pick the criterion that matches what the question gives.

---

### 4. Pythagoras & applications 📐

- **a² + b² = c²** in a right triangle (c = hypotenuse)  
- NCERT proves Pythagoras using **similar right triangles**  
- **Shadow / height** problems → similar triangles, same ratio  
- **Area ratio** of similar triangles = **(side ratio)²**
""",
            },
            {
                "id": "ncert",
                "title": "How NCERT organises the chapter",
                "body": """
| Section | Content |
|---------|---------|
| **6.1 Introduction** | Similar vs congruent; indirect measurement |
| **6.2 Similar Figures** | Scale factor; conditions for similar polygons |
| **6.3 Similarity of Triangles** | BPT (Thales) and converse |
| **6.4 Criteria for Similarity** | AAA, SSS, SAS (Theorems 6.3–6.5) |
| **6.5 Summary** | Pythagoras via similarity; RHS note |

**By the end of the unit** Harshit should be able to:

1. Tell **similar vs congruent** and find **scale factor**  
2. Use **BPT** and its **converse** to find segments or prove DE ∥ BC  
3. Prove triangles similar using **AAA, SSS, or SAS**  
4. Solve **shadow / height** and **ladder** problems  
5. Use **area ratio = (side ratio)²** for similar triangles  

**Comes next:** **Unit 7 — Coordinate Geometry**. Unit 6 is **pure geometry** with ratios and proofs.
""",
            },
            {
                "id": "formulas",
                "title": "Formula sheet — get these comfortable",
                "body": """
### BPT (DE ∥ BC)

**AD/DB = AE/EC**

Also: **AD/AB = AE/AC** when DE ∥ BC.

**Converse:** Equal ratios on two sides ⇒ line **parallel** to third side.

---

### Similarity criteria

- **AAA:** All corresponding angles equal (often only need **AA**)  
- **SSS:** AB/DE = BC/EF = CA/FD  
- **SAS:** One angle equal + **including** sides proportional  

---

### Pythagoras (right triangle)

**Hypotenuse² = leg₁² + leg₂²**

Example: legs 6 and 8 → hypotenuse = 10.

---

### Indirect measurement

```
height₁ / shadow₁ = height₂ / shadow₂
```

Same sun angle ⇒ similar triangles.

---

### Area of similar triangles

If sides are in ratio **k : 1**, then  
**ar(large) / ar(small) = k²**

---

### Quick reference

```
Similar      → same shape, sides in ratio
BPT          → parallel line ⇒ divide sides equally (in ratio)
AAA          → angles match → similar
Area ratio   → (side ratio)²
Pythagoras   → a² + b² = c² (right triangle only)
```
""",
            },
            {
                "id": "teaching",
                "title": "Suggested teaching order",
                "body": """
A comfortable order **before Practice**:

| Step | Focus | ~Time |
|------|--------|-------|
| 1 | Congruent vs similar; scale factor 2:3 | 15 min |
| 2 | BPT: DE ∥ BC → find EC (one numeric example) | 20 min |
| 3 | Converse: check if EF ∥ QR from ratios | 15 min |
| 4 | AAA: two angles equal → similar | 15 min |
| 5 | Find missing side using similarity ratio | 20 min |
| 6 | Shadow problem or Pythagoras ladder | 20 min |

**Tips for Harshit's age (Class 10):**

- Draw a **neat diagram** and mark parallel lines with arrows.  
- For BPT, write **AD/DB = AE/EC** before substituting numbers.  
- For similarity, **name corresponding vertices** in order (A ↔ D, B ↔ E, …).  
- Area questions: square the **side ratio**, not the ratio itself.

Then open **Week Setup**, pick all four topics at levels B–C, and start **Practice**. Try the **Unit Test** when BPT and one similarity criterion feel solid.

**One sentence for Harshit:**

> *Parallel lines split sides in the same ratio; equal angles or proportional sides make triangles similar — then use ratios for lengths, areas, and heights.*
""",
            },
        ],
    },
    7: {
        "title": "Coordinate Geometry — Unit Guide",
        "subtitle": "NCERT Chapter 7 · Read together before practice",
        "sections": [
            {
                "id": "overview",
                "title": "What this chapter is about",
                "body": """
**Unit 7** uses **algebra on a grid** to study geometry — distances, mid-points, and dividing lines.

**Real-life idea:**  
A town is **36 km east** and **15 km north** of another. On a map with 1 unit = 1 km, the second town is at **(36, 15)**. The straight-line distance is **not** 36 + 15 — you need the **distance formula** (Pythagoras on the grid).

**The big ideas:**

> 1. **Distance** between two points using coordinates  
> 2. **Section formula** — point dividing a segment in ratio **m : n**  
> 3. **Collinearity** and **area** checks using coordinates
""",
            },
            {
                "id": "topics",
                "title": "Four topics in this unit",
                "body": """
### 1. Distance Formula 📏

**d = √[(x₂ − x₁)² + (y₂ − y₁)²]**

On the **x-axis only**: distance = |x₂ − x₁|.

---

### 2. Section Formula ✂️

Point dividing (x₁, y₁) and (x₂, y₂) **internally** in ratio **m : n**:

**P = ((mx₂ + nx₁)/(m + n), (my₂ + ny₁)/(m + n))**

**Mid-point** = ratio **1 : 1**.

---

### 3. Collinearity & Verification 📍

Three points **collinear** if they lie on one line — check with **equal slopes** or **AB + BC = AC**.

**Area of triangle** from coordinates — area **0** means collinear.

---

### 4. Coordinate Applications 🗺️

Town problems, **perimeter** of triangles, finding unknown coordinates.
""",
            },
            {
                "id": "ncert",
                "title": "How NCERT organises the chapter",
                "body": """
| Section | Content |
|---------|---------|
| **7.1 Introduction** | Recap of Class IX coordinates |
| **7.2 Distance Formula** | Pythagoras on the coordinate plane |
| **7.3 Section Formula** | Internal division; mid-point |
| **7.4 Summary** | Key formulas |

**By the end of the unit** Harshit should be able to:

1. Find **distance** between any two points  
2. Find **mid-point** and **section point** in ratio m : n  
3. Test **collinearity** and find **area** of a triangle  
4. Solve **town / map** style problems  

**Comes next:** **Unit 8 — Introduction to Trigonometry**. Unit 7 is **algebra + geometry on a grid**.
""",
            },
            {
                "id": "formulas",
                "title": "Formula sheet — get these comfortable",
                "body": """
### Distance

**d = √[(x₂ − x₁)² + (y₂ − y₁)²]**

On x-axis: **|x₂ − x₁|** · On y-axis: **|y₂ − y₁|**

---

### Section (internal, ratio m : n)

**x = (mx₂ + nx₁)/(m + n)**  
**y = (my₂ + ny₁)/(m + n)**

**Mid-point:** ((x₁ + x₂)/2, (y₁ + y₂)/2)

---

### Area of triangle

**Area = ½ |x₁(y₂ − y₃) + x₂(y₃ − y₁) + x₃(y₁ − y₂)|**

If area = **0** → points are **collinear**.

---

### Quick reference

```
Distance     → √(Δx² + Δy²)
Mid-point    → average of coordinates
Section m:n  → weighted average toward (x₂, y₂)
Collinear    → same slope or AB + BC = AC
```
""",
            },
            {
                "id": "teaching",
                "title": "Suggested teaching order",
                "body": """
| Step | Focus | ~Time |
|------|--------|-------|
| 1 | Distance on x-axis: (4,0) to (6,0) | 10 min |
| 2 | Distance formula: (3,4) to (0,0) = 5 | 20 min |
| 3 | Mid-point of two points | 15 min |
| 4 | Section formula ratio 2:1 | 20 min |
| 5 | Collinearity check | 15 min |
| 6 | Town B 36 km east, 15 km north | 20 min |

**Tips for Harshit's age (Class 10):**

- Sketch points on rough axes before substituting.  
- **Square** the differences in the distance formula — signs disappear.  
- Mid-point is always **section 1:1**.

Then open **Week Setup**, pick topics at levels B–C, and start **Practice**.

**One sentence for Harshit:**

> *Plot the points, use √(Δx² + Δy²) for distance, and the section formula when a point splits a line in ratio m : n.*
""",
            },
        ],
    },
    8: {
        "title": "Introduction to Trigonometry — Unit Guide",
        "subtitle": "NCERT Chapter 8 · Read together before practice",
        "sections": [
            {
                "id": "overview",
                "title": "What this chapter is about",
                "body": """
**Unit 8** studies **ratios in right triangles** — how side lengths depend on acute angles.

**Real-life idea:**  
Looking up at a **minar**, you imagine a **right triangle**. The **angle of view** fixes the ratio **height / distance**. That ratio has a name: **tan θ**.

**The big ideas:**

> 1. **Six ratios**: sin, cos, tan, cosec, sec, cot  
> 2. **Standard values** at 0°, 30°, 45°, 60°, 90°  
> 3. **Identities** linking the ratios
""",
            },
            {
                "id": "topics",
                "title": "Four topics in this unit",
                "body": """
### 1. Trigonometric Ratios 📐

With respect to angle **θ** in right ΔABC (∠B = 90°):

| Ratio | Definition |
|-------|------------|
| **sin θ** | opposite / hypotenuse |
| **cos θ** | adjacent / hypotenuse |
| **tan θ** | opposite / adjacent |

**cosec = 1/sin**, **sec = 1/cos**, **cot = 1/tan**

---

### 2. Ratios of Specific Angles 🎯

Memorise the table for **0°, 30°, 45°, 60°, 90°**.

**Complementary:** sin(90° − θ) = cos θ

---

### 3. Trigonometric Identities 🆔

**sin²θ + cos²θ = 1**  
**1 + tan²θ = sec²θ**  
**1 + cot²θ = cosec²θ**

---

### 4. Mixed Trigonometry 🔀

Simplify expressions; combine **specific angles** with **identities**.
""",
            },
            {
                "id": "ncert",
                "title": "How NCERT organises the chapter",
                "body": """
| Section | Content |
|---------|---------|
| **8.1 Introduction** | Right triangles in real life |
| **8.2 Trigonometric Ratios** | Definitions; reciprocal relations |
| **8.3 Ratios of Specific Angles** | Table; 0° and 90° |
| **8.4 Trigonometric Identities** | Three main identities |
| **8.5 Summary** | |

**By the end of the unit** Harshit should be able to:

1. Write **all six ratios** from a right triangle diagram  
2. Recall **standard values** without a calculator  
3. Use **identities** to simplify expressions  
4. Prove **simple identities** in 2–3 steps  

**Comes next:** **Unit 9 — Applications of Trigonometry** (heights and distances).
""",
            },
            {
                "id": "formulas",
                "title": "Formula sheet — get these comfortable",
                "body": """
### Standard values (memorise)

| θ | sin θ | cos θ | tan θ |
|---|-------|-------|-------|
| 0° | 0 | 1 | 0 |
| 30° | 1/2 | √3/2 | 1/√3 |
| 45° | 1/√2 | 1/√2 | 1 |
| 60° | √3/2 | 1/2 | √3 |
| 90° | 1 | 0 | undefined |

---

### Identities

**sin²θ + cos²θ = 1**  
**1 + tan²θ = sec²θ**  
**1 + cot²θ = cosec²θ**

---

### Complementary angles

**sin(90° − θ) = cos θ**  
**cos(90° − θ) = sin θ**  
**tan(90° − θ) = cot θ**

---

### Quick reference

```
SOH CAH TOA  → sin, cos, tan definitions
cosec sec cot → reciprocals
1 − sin²θ     → cos²θ
Table values  → exact surds, not decimals
```
""",
            },
            {
                "id": "teaching",
                "title": "Suggested teaching order",
                "body": """
| Step | Focus | ~Time |
|------|--------|-------|
| 1 | Label opposite, adjacent, hypotenuse | 15 min |
| 2 | sin, cos, tan from a 3-4-5 triangle | 20 min |
| 3 | Table for 30°, 45°, 60° | 25 min |
| 4 | sin²θ + cos²θ = 1 | 15 min |
| 5 | Simplify (1 − sin²θ) | 15 min |
| 6 | Evaluate sin 30° + cos 60° | 10 min |

**Tips for Harshit's age (Class 10):**

- Always **mark the angle** you are using — opposite/adjacent swap for different angles.  
- Learn the **table** by heart for board exams.  
- For identities, pick **sin² + cos² = 1** first when simplifying.

**One sentence for Harshit:**

> *Label the right triangle, pick the ratio you need, and use sin²θ + cos²θ = 1 when expressions mix sin and cos.*
""",
            },
        ],
    },
    9: {
        "title": "Some Applications of Trigonometry — Unit Guide",
        "subtitle": "NCERT Chapter 9 · Read together before practice",
        "sections": [
            {
                "id": "overview",
                "title": "What this chapter is about",
                "body": """
**Unit 9** uses trigonometry for **heights and distances** — minars, towers, cliffs, boats, aeroplanes.

**Key vocabulary:**

- **Line of sight** — from eye to object  
- **Angle of elevation** — looking **up** from horizontal  
- **Angle of depression** — looking **down** from horizontal  

Draw a **right triangle** first; then pick **sin, cos, or tan**.
""",
            },
            {
                "id": "topics",
                "title": "Four topics in this unit",
                "body": """
### 1. Angle of Elevation & Depression 👁️

Elevation = above horizontal · Depression = below horizontal.

Alternate angles link elevation and depression across **parallel horizontals**.

---

### 2. Heights Using Trigonometry 🏗️

**height = horizontal distance × tan(angle)** (often)

Add **observer height** when the question gives eye level.

---

### 3. Distances Using Trigonometry 🌉

Find **width of river**, **distance of boat**, **foot of ladder** using known height and angle.

---

### 4. Applications & Word Problems 🏔️

Shadow problems, **two-angle** setups, lighthouse and aeroplane questions.
""",
            },
            {
                "id": "ncert",
                "title": "How NCERT organises the chapter",
                "body": """
| Section | Content |
|---------|---------|
| **9.1 Heights and Distances** | Line of sight; elevation & depression; worked examples |
| **9.2 Summary** | |

**By the end of the unit** Harshit should be able to:

1. Draw a **clear diagram** with horizontal and line of sight  
2. Distinguish **elevation** vs **depression**  
3. Find **heights** and **distances** using tan/sin/cos  
4. Handle **two-triangle** board problems  

**Comes next:** **Unit 10 — Circles** (tangents and proofs).
""",
            },
            {
                "id": "formulas",
                "title": "Formula sheet — get these comfortable",
                "body": """
### Typical setup (angle of elevation θ)

**tan θ = height / distance**  
**height = distance × tan θ**  
**distance = height / tan θ**

---

### With observer height h₀

Total height = **h₀ + (horizontal × tan θ)**

---

### Shadow problems

Same sun ⇒ **height / shadow** is constant (similar triangles).

---

### Quick reference

```
Elevation    → angle above horizontal
Depression   → angle below horizontal
Line of sight → eye to object
Draw ⊥       → mark height and base first
tan θ        → most common in height problems
```
""",
            },
            {
                "id": "teaching",
                "title": "Suggested teaching order",
                "body": """
| Step | Focus | ~Time |
|------|--------|-------|
| 1 | Line of sight and horizontal | 15 min |
| 2 | Elevation vs depression on one diagram | 15 min |
| 3 | Tower: distance 30 m, angle 30° | 20 min |
| 4 | Add observer height 1.5 m | 20 min |
| 5 | Depression from cliff | 20 min |
| 6 | Shadow ratio problem | 15 min |

**Tips for Harshit's age (Class 10):**

- **Diagram is half the answer** — label θ, height, distance.  
- Check whether the height is from **ground** or **eye level**.  
- For depression, the angle inside the triangle equals the depression angle (alternate angles).

**One sentence for Harshit:**

> *Draw the right triangle, mark elevation or depression, then use tan θ = opposite/adjacent with the right pair of sides.*
""",
            },
        ],
    },
    10: {
        "title": "Circles — Unit Guide",
        "subtitle": "NCERT Chapter 10 · Read together before practice",
        "sections": [
            {
                "id": "overview",
                "title": "What this chapter is about",
                "body": """
**Unit 10** is about **tangents** — lines that touch a circle at **exactly one point**.

**Three cases** for a line and a circle:

1. **No point** in common — non-intersecting  
2. **Two points** — **secant**  
3. **One point** — **tangent**

From a point **outside** the circle you can draw **exactly two** tangents; their lengths are **equal**.
""",
            },
            {
                "id": "topics",
                "title": "Four topics in this unit",
                "body": """
### 1. Tangent to a Circle ⭕

**Theorem 10.1:** Radius ⊥ tangent at point of contact.

---

### 2. Tangents from an External Point 📍

- Inside → **no** tangent  
- On circle → **one** tangent  
- Outside → **two** tangents  

**Theorem 10.2:** Tangents from external point are **equal** (PQ = PR).

---

### 3. Length of Tangent 📏

**Length = √(OP² − r²)** where O is centre, P external point, r radius.

---

### 4. Circle Applications & Proofs 🔧

Concentric circles, chord as tangent to inner circle, angle between tangents.
""",
            },
            {
                "id": "ncert",
                "title": "How NCERT organises the chapter",
                "body": """
| Section | Content |
|---------|---------|
| **10.1 Introduction** | Line vs circle: none, secant, tangent |
| **10.2 Tangent to a Circle** | Theorem 10.1 |
| **10.3 Number of Tangents from a Point** | Cases 1–3; Theorem 10.2 |
| **10.4 Summary** | |

**By the end of the unit** Harshit should be able to:

1. State **Theorem 10.1** and **10.2**  
2. Find **tangent length** using Pythagoras  
3. Count tangents from **inside / on / outside**  
4. Prove **standard circle results** (equal tangents, bisected chord)  

**Comes next:** **Unit 11 — Areas Related to Circles**.
""",
            },
            {
                "id": "formulas",
                "title": "Formula sheet — get these comfortable",
                "body": """
### Theorem 10.1

**Radius ⊥ tangent** at point of contact.

---

### Tangent length from external point P

**PT = √(OP² − r²)**

---

### Theorem 10.2

**Two tangents from external P are equal:** PQ = PR.

**OP bisects** ∠QPR.

---

### Concentric circles

Chord of **outer** circle tangent to **inner** ⇒ tangent point **bisects** the chord.

---

### Quick reference

```
Tangent      → one common point
Secant       → two common points
Inside point → 0 tangents
Outside      → 2 equal tangents
Length       → √(OP² − r²)
```
""",
            },
            {
                "id": "teaching",
                "title": "Suggested teaching order",
                "body": """
| Step | Focus | ~Time |
|------|--------|-------|
| 1 | Tangent vs secant — one vs two points | 15 min |
| 2 | Radius ⊥ tangent (Theorem 10.1) | 20 min |
| 3 | Tangent length: r = 5, OP = 13 | 20 min |
| 4 | Two tangents equal from outside | 20 min |
| 5 | Concentric circles — chord bisected | 15 min |
| 6 | NCERT Example: ∠PTQ = 2∠OPQ | 20 min |

**Tips for Harshit's age (Class 10):**

- Mark the **right angle** at the point of contact first.  
- Tangent length problems are **Pythagoras** in disguise.  
- For proofs, join **OP** and use **RHS** congruence.

**One sentence for Harshit:**

> *Radius meets tangent at 90°; from outside the circle, both tangents have the same length — √(OP² − r²).*
""",
            },
        ],
    },
}


# Bump a unit's version when its guide content changes so returning users land on the guide tab.
GUIDE_VERSIONS: dict[int, int] = {2: 1, 3: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 10: 1}


def unit_guide_available(unit_id: int) -> bool:
    return unit_id in UNIT_GUIDES


def guide_version(unit_id: int) -> int:
    return GUIDE_VERSIONS.get(unit_id, 0)


def get_unit_guide(unit_id: int) -> dict[str, Any] | None:
    return UNIT_GUIDES.get(unit_id)


def guide_section_ids(unit_id: int) -> list[str]:
    guide = get_unit_guide(unit_id)
    if not guide:
        return []
    return [str(s["id"]) for s in guide.get("sections", [])]
