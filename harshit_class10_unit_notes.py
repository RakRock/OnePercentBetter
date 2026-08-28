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
}


# Bump a unit's version when its guide content changes so returning users land on the guide tab.
GUIDE_VERSIONS: dict[int, int] = {2: 1, 3: 1}


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
