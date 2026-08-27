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
}


def unit_guide_available(unit_id: int) -> bool:
    return unit_id in UNIT_GUIDES


def get_unit_guide(unit_id: int) -> dict[str, Any] | None:
    return UNIT_GUIDES.get(unit_id)


def guide_section_ids(unit_id: int) -> list[str]:
    guide = get_unit_guide(unit_id)
    if not guide:
        return []
    return [str(s["id"]) for s in guide.get("sections", [])]
