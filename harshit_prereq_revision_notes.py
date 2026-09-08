"""Consolidated 2–3 page revision lesson notes — one guide per PreReq (1–6)."""

from __future__ import annotations

from typing import Any

# prereq_id -> single revision guide (print / app Notes tab)
PREREQ_REVISION_GUIDES: dict[int, dict[str, Any]] = {
    1: {
        "title": "Number Systems & Foundations",
        "subtitle": "PreReq 1 · NCERT Class 9 Chapter 1 · Revision sheet",
        "sections": [
            {
                "id": "numberline",
                "title": "1. Number line & integers",
                "diagrams": [],
                "body": """
**Big idea:** Every integer sits at a fixed distance from **0**. Right = positive, left = negative.

| Concept | Rule |
|---------|------|
| **Absolute value** | Distance from zero: `|−7| = 7`, `|4| = 4` |
| **Compare** | Larger number is farther right on the line |
| **Subtract a negative** | `a − (−b) = a + b` (e.g. `−5 − (−3) = −2`) |

**Rationals on the line:** `p/q` lies between integers when you write it as a mixed number (`5/2 = 2½`).

**Try:** Which is farther from 0: `−3` or `2`? → **−3** (`|−3| = 3`).
""",
            },
            {
                "id": "rationals",
                "title": "2. Rational numbers — operations",
                "diagrams": [],
                "body": """
A **rational** number can be written as `p/q` where `p, q` are integers and `q ≠ 0`.

| Operation | Method |
|-----------|--------|
| **Add / subtract** | Find **LCD**, rewrite with common denominator, combine numerators |
| **Multiply** | Multiply numerators × numerators, denominators × denominators; simplify |
| **Divide** | Multiply by the **reciprocal**: `a/b ÷ c/d = a/b × d/c` |

**Decimals:** terminating decimals are rational (`0.375 = 375/1000 = 3/8`).

**Try:** `1/3 + 1/4` → LCD 12 → `4/12 + 3/12 =` **7/12**.
""",
            },
            {
                "id": "exponents",
                "title": "3. Laws of exponents",
                "diagrams": [],
                "body": """
For real `a, b` (with usual restrictions when bases match):

| Law | Formula |
|-----|---------|
| Product | `aᵐ × aⁿ = aᵐ⁺ⁿ` |
| Quotient | `aᵐ ÷ aⁿ = aᵐ⁻ⁿ` |
| Power of power | `(aᵐ)ⁿ = aᵐⁿ` |
| Zero exponent | `a⁰ = 1` (a ≠ 0) |
| Negative exponent | `a⁻ⁿ = 1/aⁿ` |
| Fractional | `a^(1/n) = ⁿ√a` |

**Roots:** `√a` means the non-negative number whose square is `a`. `√(ab) = √a × √b` when both defined.

**Try:** `2³ × 2⁻¹ =` **2² = 4**.
""",
            },
            {
                "id": "surds",
                "title": "4. Rationalizing & irrationals",
                "diagrams": [],
                "body": """
**Rationalize** = remove surd from the **denominator**.

| Denominator | Multiply top & bottom by |
|-------------|--------------------------|
| `√b` | `√b` |
| `a + √b` | conjugate `a − √b` |
| `a − √b` | conjugate `a + √b` |

**Irrational:** cannot be `p/q`. Examples: `√2`, `√5`, `π`, non-repeating non-terminating decimals.

**Locate √2:** `1² < 2 < 2²` so √2 is between **1 and 2** (≈ 1.414).

**Try:** Rationalize `1/√2` → multiply by `√2/√2` → **√2/2**.
""",
            },
            {
                "id": "checklist",
                "title": "5. Revision checklist",
                "diagrams": [],
                "body": """
Before Class 10 Real Numbers, Harshit should be able to:

- [ ] Plot and compare integers and simple fractions on a number line  
- [ ] Add, subtract, multiply, divide rationals (LCD / reciprocal)  
- [ ] Apply exponent laws including negative and fractional exponents  
- [ ] Rationalize monomial and binomial denominators  
- [ ] Classify numbers as rational or irrational; locate √n roughly  

**Class 10 next:** prime factorisation, HCF/LCM, proofs that √p is irrational.
""",
            },
        ],
    },
    2: {
        "title": "Algebraic Operations & Equations",
        "subtitle": "PreReq 2 · NCERT Class 9 Ch 2 & Ch 4 · Revision sheet",
        "sections": [
            {
                "id": "poly_ops",
                "title": "1. Polynomials — add, subtract, multiply",
                "diagrams": [],
                "body": """
A **polynomial** in `x` has non-negative integer powers only (e.g. `3x² − 5x + 2`).

| Skill | How |
|-------|-----|
| **Like terms** | Same variable **and** same power → combine coefficients |
| **Add / subtract** | Line up like terms; watch signs when subtracting in brackets |
| **× monomial** | Distribute: `2x(3x² − x) = 6x³ − 2x²` |
| **× binomial** | Distribute each term: `(x + 3)(2x − 1) = 2x² + 5x − 3` |

**Special products (memorise):**

- `(a + b)² = a² + 2ab + b²`  
- `(a − b)² = a² − 2ab + b²`  
- `(a + b)(a − b) = a² − b²`
""",
            },
            {
                "id": "factor",
                "title": "2. Factorization",
                "diagrams": [],
                "body": """
Reverse of multiplying — write as a **product** of simpler factors.

| Type | Method |
|------|--------|
| **Common factor** | `6x² + 9x = 3x(2x + 3)` |
| **Grouping** | `ax + ay + bx + by = a(x + y) + b(x + y) = (a + b)(x + y)` |
| **Identities** | Recognise `a² ± 2ab + b²` or `a² − b²` |
| **Trinomial** | Split middle term or use identities |

**Try:** `x² − 9 =` **(x + 3)(x − 3)**.
""",
            },
            {
                "id": "linear",
                "title": "3. Linear equations in two variables",
                "diagrams": [],
                "body": """
Standard form: **`ax + by + c = 0`** (a, b not both zero).

| Idea | Detail |
|------|--------|
| **Solution** | An ordered pair `(x, y)` that makes the equation **true** |
| **Infinitely many** | Each line has infinitely many points on it |
| **Substitution** | If `y` is known, plug in and solve for `x` (and vice versa) |
| **Table** | Pick values for `x`, find matching `y` — build `(x, y)` pairs |

**Example:** `2x + y = 7`. When `x = 1`, `y = 5` → `(1, 5)` is a solution.

**Try:** `x + 2y = 8`, find `y` when `x = 4` → `4 + 2y = 8` → **y = 2**.
""",
            },
            {
                "id": "graph_word",
                "title": "4. Graphing & word problems",
                "diagrams": [],
                "body": """
**Graph:** plot solutions — they lie on a **straight line**.

| Check | Method |
|-------|--------|
| Point on line? | Substitute `(x, y)` into equation — both sides equal? |
| Read from graph | At given `x`, read `y` from the line |
| Intercepts | `x`-intercept: set `y = 0`; `y`-intercept: set `x = 0` |

**Word problems:** translate story → `ax + by + c = 0`, then substitute or tabulate.

**Try:** Does `(2, 3)` satisfy `x + y = 5`? → `2 + 3 = 5` → **Yes**.
""",
            },
            {
                "id": "checklist",
                "title": "5. Revision checklist",
                "diagrams": [],
                "body": """
- [ ] Simplify polynomials by combining like terms  
- [ ] Multiply binomials; use `(a ± b)²` and `a² − b²`  
- [ ] Factor using common factor, grouping, and identities  
- [ ] Find missing variable in `ax + by = c`  
- [ ] Build a solution table and verify a point on the line  

**Class 10 next:** factor theorem, **pair** of linear equations (elimination/substitution), quadratics.
""",
            },
        ],
    },
    3: {
        "title": "Coordinate Graphing",
        "subtitle": "PreReq 3 · NCERT Class 9 Chapter 3 · Revision sheet",
        "sections": [
            {
                "id": "plane",
                "title": "1. Cartesian plane",
                "diagrams": [],
                "body": """
Two perpendicular number lines: **x-axis** (horizontal), **y-axis** (vertical). They meet at the **origin** `(0, 0)`.

| Quadrant | x | y | Example |
|----------|---|---|---------|
| **I** | + | + | `(3, 2)` |
| **II** | − | + | `(−2, 4)` |
| **III** | − | − | `(−1, −3)` |
| **IV** | + | − | `(5, −1)` |

**Ordered pair** `(x, y)` — **x first**, then y.

**Distance from axes:** from `(4, −3)` to x-axis is `|−3| = 3`; to y-axis is `|4| = 4`.
""",
            },
            {
                "id": "plot",
                "title": "2. Plotting & reading points",
                "diagrams": [],
                "body": """
**To plot `(a, b)`:** move `a` along x (right if +, left if −), then `b` along y (up if +, down if −).

**To read:** count horizontal from origin → x; vertical → y.

**Midpoint (intuition):** halfway between `(x₁, y₁)` and `(x₂, y₂)` is roughly average of coordinates — exact formula comes in Class 10.

**Try:** Plot `(−2, 3)` — **2 left, 3 up**. Which quadrant? → **II**.
""",
            },
            {
                "id": "lines",
                "title": "3. Equations of lines",
                "diagrams": [],
                "body": """
| Form | Graph | Notes |
|------|-------|-------|
| **`y = mx`** | Line through origin | slope `m` |
| **`y = mx + c`** | Straight line | `c` = y-intercept |
| **`y = k`** | Horizontal | slope 0 |
| **`x = k`** | Vertical | undefined slope |

**Slope** `m` = rise ÷ run = change in y ÷ change in x.

From `(x₁, y₁)` to `(x₂, y₂)`: `m = (y₂ − y₁) / (x₂ − x₁)`.

**Try:** `y = 2x + 1` has y-intercept **1** and slope **2** (up 2 for every 1 right).
""",
            },
            {
                "id": "checklist",
                "title": "4. Revision checklist",
                "diagrams": [],
                "body": """
- [ ] Name the quadrant of a given point  
- [ ] Plot and read coordinates accurately  
- [ ] Recognise `y = mx + c`, horizontal, and vertical lines  
- [ ] Compute slope from two points  

**Class 10 next:** distance formula, section formula, area of triangle from coordinates.
""",
            },
        ],
    },
    4: {
        "title": "Core Euclidean Geometry",
        "subtitle": "PreReq 4 · NCERT Class 9 Ch 5, 6, 7, 8 & 10 · Revision sheet",
        "sections": [
            {
                "id": "angles",
                "title": "1. Lines & angles",
                "diagrams": [{"type": "parallel_transversal", "angle": 65}],
                "body": """
| Term | Meaning |
|------|---------|
| **Complementary** | Sum **90°** |
| **Supplementary** / linear pair | Sum **180°** |
| **Vertically opposite** | Equal when two lines cross |

**Parallel lines + transversal** (`l ∥ m`):

- **Corresponding** & **alternate interior** → **equal**  
- **Co-interior** (same side) → **add to 180°**
""",
            },
            {
                "id": "triangles",
                "title": "2. Triangles",
                "diagrams": [{"type": "triangle", "angle_a": 50, "angle_b": 60}],
                "body": """
- **Angle sum:** `∠A + ∠B + ∠C = 180°`  
- **Exterior angle** = sum of **two remote interior** angles  
- **Congruence:** SSS, SAS, ASA, RHS (not AAA)  
- **Isosceles:** equal sides ↔ equal base angles  
- **Triangle inequality:** `a + b > c` for every side pair; longest side opposite largest angle
""",
            },
            {
                "id": "quads",
                "title": "3. Quadrilaterals",
                "diagrams": [{"type": "parallelogram", "show_diagonals": True}],
                "body": """
**Angle sum = 360°.**

| Shape | Key facts |
|-------|-----------|
| **Parallelogram** | Opposite sides & angles equal; diagonals **bisect** |
| **Rectangle** | All 90°; diagonals **equal** |
| **Rhombus** | All sides equal; diagonals **perpendicular** |
| **Square** | Rectangle + rhombus |
| **Trapezium** | **One** pair of parallel sides |
| **Kite** | Two pairs of **adjacent** equal sides |

**Mid-point theorem:** segment joining midpoints of two sides of a triangle is **parallel** to the third side and **half** its length.
""",
            },
            {
                "id": "circles",
                "title": "4. Circles",
                "diagrams": [{"type": "circle", "variant": "basic"}],
                "body": """
- `diameter = 2r`; diameter = longest chord  
- **Equal chords** → equal angles at centre (SSS proof)  
- Perpendicular from centre **bisects** chord  
- Angle at **centre** = **2 ×** angle at rim (same arc)  
- **Semicircle** → angle in semicircle = **90°**  
- **Cyclic quadrilateral:** opposite angles sum **180°**  
- `C = 2πr`; **sector** = pizza slice; **segment** = chord + arc
""",
            },
            {
                "id": "checklist",
                "title": "5. Revision checklist",
                "diagrams": [],
                "body": """
- [ ] Angle chase with parallels and vertically opposite angles  
- [ ] Use 180° sum and exterior-angle theorem  
- [ ] Pick congruence rule (SSS / SAS / ASA / RHS)  
- [ ] Parallelogram & special quad properties  
- [ ] Circle: centre vs rim, cyclic quad, chord facts  

**Class 10 next:** similar triangles, BPT, tangent ⊥ radius.
""",
            },
        ],
    },
    5: {
        "title": "Mensuration",
        "subtitle": "PreReq 5 · NCERT Class 9 Ch 12 & 13 · Revision sheet",
        "sections": [
            {
                "id": "heron",
                "title": "1. Heron's formula (triangle area)",
                "diagrams": [],
                "body": """
When you know **all three sides** `a, b, c`:

1. Semi-perimeter: `s = (a + b + c) / 2`  
2. Area: **`A = √(s(s − a)(s − b)(s − c))`**

Always check triangle inequality first: each pair of sides must sum to more than the third.

**Try:** sides 3, 4, 5 → `s = 6` → `A = √(6·3·2·1) = √36 =` **6 sq units** (right triangle check).
""",
            },
            {
                "id": "surface",
                "title": "2. Surface area",
                "diagrams": [],
                "body": """
| Solid | Lateral / curved | Total surface area (TSA) |
|-------|------------------|---------------------------|
| **Cube** (side `a`) | — | `6a²` |
| **Cuboid** `l × b × h` | — | `2(lb + bh + hl)` |
| **Cylinder** radius `r`, height `h` | `2πrh` | `2πr(r + h)` |
| **Cone** slant `l` | `πrl` | `πr(r + l)` |
| **Sphere** | — | `4πr²` |

**Units:** cm², m² — keep consistent.

**Try:** Cube side 4 cm → TSA = `6 × 16 =` **96 cm²**.
""",
            },
            {
                "id": "volume",
                "title": "3. Volume & capacity",
                "diagrams": [],
                "body": """
| Solid | Volume |
|-------|--------|
| **Cube** | `a³` |
| **Cuboid** | `l × b × h` |
| **Cylinder** | `πr²h` |
| **Cone** | `⅓ πr²h` |
| **Sphere** | `⁴⁄₃ πr³` |
| **Hemisphere** | `⅔ πr³` |

**Capacity:** `1 m³ = 1000 L`; `1 cm³ = 1 mL`.

**Combined solids:** add volumes (or subtract hollow parts); do not mix up **surface** vs **volume** formulas.

**Try:** Cylinder `r = 7`, `h = 10`, `π ≈ 22/7` → `V = 22/7 × 49 × 10 =` **1540 cm³**.
""",
            },
            {
                "id": "checklist",
                "title": "4. Revision checklist",
                "diagrams": [],
                "body": """
- [ ] Heron: compute `s` then area; include units  
- [ ] Pick lateral vs TSA for cylinders and cones  
- [ ] Volume formulas for prism, cylinder, cone, sphere  
- [ ] Convert between cm³ and litres when asked  

**Class 10 next:** sectors & segments, combination solids, frustum.
""",
            },
        ],
    },
    6: {
        "title": "Data & Probability",
        "subtitle": "PreReq 6 · NCERT Class 9 Ch 14 & 15 · Revision sheet",
        "sections": [
            {
                "id": "central",
                "title": "1. Mean, median, mode",
                "diagrams": [],
                "body": """
**Ungrouped data** (list of values):

| Measure | How |
|---------|-----|
| **Mean** | Sum of values ÷ count: `x̄ = Σx / n` |
| **Median** | Middle value when **sorted**; even count → average of two middles |
| **Mode** | Value that appears **most often** (can be more than one mode) |

**Choosing a measure:** mean is pulled by extremes; median is better for skewed data; mode for “most popular” category.

**Try:** Data `3, 5, 5, 8` → mean **5.25**, median **5**, mode **5**.
""",
            },
            {
                "id": "graphs",
                "title": "2. Graphical representation",
                "diagrams": [],
                "body": """
| Graph | Use |
|-------|-----|
| **Bar graph** | Discrete categories; bars can have gaps |
| **Histogram** | Continuous class intervals; **no gap** between bars |
| **Frequency polygon** | Line graph joining midpoints of histogram tops |

Read the **scale** on each axis before answering.

**Try:** Histogram bar height = frequency for that **class interval**, not a single number unless width is 1.
""",
            },
            {
                "id": "probability",
                "title": "3. Probability",
                "diagrams": [],
                "body": """
**Classical probability** (equally likely outcomes):

`P(E) = (number of favourable outcomes) / (total outcomes)`

| Rule | Formula |
|------|---------|
| **Range** | `0 ≤ P(E) ≤ 1` |
| **Certain event** | `P = 1` |
| **Impossible event** | `P = 0` |
| **Complement** | `P(not E) = 1 − P(E)` |

**Experimental** probability ≈ (times event happened) ÷ (total trials) — approaches theoretical with many trials.

**Try:** Fair die, P(even) = 3/6 = **1/2**. P(not even) = **1/2**.
""",
            },
            {
                "id": "checklist",
                "title": "4. Revision checklist",
                "diagrams": [],
                "body": """
- [ ] Compute mean, median, mode for a small data set  
- [ ] Distinguish bar graph vs histogram  
- [ ] Write probability as a fraction in lowest terms  
- [ ] Use complement: `P(not E) = 1 − P(E)`  

**Class 10 next:** grouped mean/median/mode formulas; classical probability with dice and cards.
""",
            },
        ],
    },
}


def get_revision_guide(prereq_id: int) -> dict[str, Any] | None:
    return PREREQ_REVISION_GUIDES.get(prereq_id)


def has_revision_notes(prereq_id: int) -> bool:
    return prereq_id in PREREQ_REVISION_GUIDES


def all_prereq_ids_with_revision() -> list[int]:
    return sorted(PREREQ_REVISION_GUIDES)
