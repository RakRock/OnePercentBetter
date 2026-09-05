"""Parent-led lesson notes for Harshit Class 9 PreReqs."""

from __future__ import annotations

from typing import Any

# prereq_id -> topic_id -> guide
TOPIC_GUIDES: dict[int, dict[int, dict[str, Any]]] = {
    4: {
        1: {
            "title": "Lines & Angles",
            "subtitle": "PreReq 4 · Topic 1 · NCERT Class 9 Chapters 5 & 6",
            "sections": [
                {
                    "id": "euclid",
                    "title": "1. One line through two points",
                    "diagrams": [{"type": "two_points_line"}],
                    "body": """
**Euclid’s rule (Class 9, Ch 5):**  
If you pick **two different points**, there is **exactly one line** that goes through both.

Think of two dots on paper. You can lay a ruler on them in **only one** way.

> **Axiom:** Through two distinct points **P** and **Q**, there passes **one and only one** line.

**What that proves (Theorem 5.1):**  
Two **different** lines cannot share **two** points.  
If they shared P and Q, they would be the **same** line.

**On a line segment:**  
If C sits **between** A and B, then

`AC + CB = AB`

If C is the **midpoint**, then `AC = CB`, so each piece is **half** of AB:

`AC = ½ AB`

**Try together**

1. How many lines pass through P and Q? → **One**  
2. Can two distinct lines meet at two different points? → **No**  
3. C is between A and B, and `AC = CB`. If `AB = 10 cm`, what is `AC`? → **5 cm**
""",
                },
                {
                    "id": "comp_supp",
                    "title": "2. Complementary & supplementary",
                    "diagrams": [{"type": "angle_arc", "degrees": 35}, {"type": "linear_pair"}],
                    "body": """
An **angle** is two rays from one **vertex**. We write `∠ABC` — the vertex letter is in the **middle**.

| Name | What it means | Memory hook |
|------|----------------|-------------|
| **Complementary** | Two angles add to **90°** | Corner of a square |
| **Supplementary** | Two angles add to **180°** | A straight line |

They do **not** have to touch. “Complementary” only means their **measures** add to 90°.

**Linear pair:** two angles that sit **next to each other on a straight line**.  
They are always supplementary: `a + b = 180°`.

**Try together**

1. Complement of **35°** → `90 − 35 =` **55°**  
2. Supplement of **110°** → `180 − 110 =` **70°**  
3. A linear pair: one angle is **x°**, the other is **(3x)°**.  
   `x + 3x = 180` → `4x = 180` → `x = 45`. Angles: **45°** and **135°**.

**Watch-outs**

- Complement of an **obtuse** angle does not exist (it would be negative).  
- Supplement of **180°** is **0°** — we do not use that in school problems.
""",
                },
                {
                    "id": "vertical",
                    "title": "3. Vertically opposite angles",
                    "diagrams": [{"type": "intersecting_lines", "angle_a": 50, "angle_b": 130}],
                    "body": """
When **two lines cross**, they make an **X** and **four** angles.

**Vertically opposite** = the pair that faces each other across the X (not next-door neighbours).

> **Theorem:** Vertically opposite angles are **equal**.

The two angles **next** to each other form a **linear pair**, so they add to **180°**.

**Picture in your head**

- Opposite pair: both **50°**  
- The other opposite pair: both **130°**  
- Check: `50 + 130 = 180` (neighbours on a straight line)

**Why it works (short proof)**  
Call the four angles around the point 1, 2, 3, 4 going around.  
Angle 1 + angle 2 = 180° (linear pair).  
Angle 2 + angle 3 = 180° (linear pair).  
So angle 1 = angle 3. Those are vertically opposite.

**Try together**

Two lines intersect. One angle is **70°**.

- Vertically opposite to it → **70°**  
- Each adjacent angle → `180 − 70 =` **110°**
""",
                },
                {
                    "id": "parallel",
                    "title": "4. Parallel lines + transversal",
                    "diagrams": [{"type": "parallel_transversal", "angle": 65}],
                    "body": """
**Parallel lines** (`l ∥ m`) never meet, even if you draw them longer.

A **transversal** (`t`) is a line that **cuts across** two (or more) other lines.  
That makes **eight** angles — four at each crossing.

When the two lines are **parallel**, these pairs are reliable:

| Pair | Where to look | If `l ∥ m` |
|------|----------------|-------------|
| **Corresponding** | Same “corner” at each crossing (both top-left, etc.) | **Equal** |
| **Alternate interior** | Inside the parallels, **opposite** sides of `t` | **Equal** |
| **Alternate exterior** | Outside the parallels, **opposite** sides of `t` | **Equal** |
| **Co-interior** (same-side interior) | Inside the parallels, **same** side of `t` | **Add to 180°** |

**Worked example**  
`l ∥ m`, cut by transversal `t`. One interior angle is **65°**.

- Corresponding angle → **65°**  
- Alternate interior → **65°**  
- Co-interior (same side) → `180 − 65 =` **115°**

**The converse (useful later)**  
If a transversal makes **corresponding angles equal**, the two lines are **parallel**.  
Same idea for alternate interior (equal) and co-interior (supplementary).

**Try together**

`l ∥ m`. A corresponding angle to 118° is? → **118°**  
A co-interior partner of 118° is? → **62°**
""",
                },
                {
                    "id": "checklist",
                    "title": "5. Ready for practice?",
                    "diagrams": [],
                    "body": """
Sit with Harshit and tick these out loud:

- [ ] Two points → **one** line; two distinct lines meet in **at most one** point  
- [ ] Complement → **90°**; supplement / linear pair → **180°**  
- [ ] Crossing lines → **vertically opposite are equal**; neighbours add to **180°**  
- [ ] Parallel + transversal → corresponding & alternate **equal**; co-interior **180°**

Then open **Practice** and start **Lines & Angles** at Level A.

**Class 10 later:** these same pairs show up in **similar triangles** and **circle tangents**.
""",
                },
            ],
        },
        2: {
            "title": "Triangles",
            "subtitle": "PreReq 4 · Topic 2 · NCERT Class 9 Chapter 7",
            "sections": [
                {
                    "id": "angle_sum",
                    "title": "1. Angle sum is 180°",
                    "diagrams": [{"type": "triangle", "angle_a": 50, "angle_b": 60}],
                    "body": """
A **triangle** has three sides and three angles. We write `△ABC`.

> **Angle-sum property:** `∠A + ∠B + ∠C = 180°`

If you know **two** angles, the third is `180°` minus their sum.

**Try together**

1. Angles `50°` and `60°`. Third angle → `180 − 50 − 60 =` **70°**  
2. A **right** triangle has one `90°`. The other two add to **90°** (they are complementary).  
3. Can a triangle have two right angles? → **No** (`90 + 90` already uses up 180°).

**Types by angles**

- **Acute:** all three angles &lt; 90°  
- **Right:** one angle = 90°  
- **Obtuse:** one angle &gt; 90°
""",
                },
                {
                    "id": "exterior",
                    "title": "2. Exterior angle",
                    "diagrams": [{"type": "triangle", "angle_a": 40, "angle_b": 70, "exterior": True}],
                    "body": """
Extend one side of the triangle. The new angle sitting **outside**, next to an interior angle, is an **exterior angle**.

That exterior angle and its **adjacent interior** angle form a **linear pair**, so they add to **180°**.

> **Exterior-angle theorem:**  
> An exterior angle = the **sum of the two remote (far) interior angles**.

“Remote” means the two interiors that are **not** next to that exterior.

**Why it works**  
Interior next to the exterior is `180° −` exterior.  
The three interiors add to 180°, so the two far ones must equal the exterior.

**Try together**

Remote interiors are `40°` and `70°`. Exterior → `40 + 70 =` **110°**  
Check: adjacent interior would be `180 − 110 = 70°`, and `40 + 70 + 70 = 180`.
""",
                },
                {
                    "id": "congruence",
                    "title": "3. Congruence (SSS, SAS, ASA, RHS)",
                    "diagrams": [{"type": "congruent_triangles"}],
                    "body": """
**Congruent** (`≅`) means same **size** and same **shape**. One triangle can sit exactly on the other.

We do **not** need all six measurements. These **rules** are enough:

| Rule | What you must match | Memory |
|------|---------------------|--------|
| **SSS** | Three sides | Side–side–side |
| **SAS** | Two sides and the **included** angle (the angle **between** those sides) | Side–angle–side |
| **ASA** | Two angles and the **included** side | Angle–side–angle |
| **AAS** | Two angles and a **non-included** side (also works, because the third angle is fixed) | |
| **RHS** | Right angle, **hypotenuse**, and one other side | Only for **right** triangles |

**AAA is not a congruence rule.** Same three angles means the triangles are **similar** (same shape), but one can be bigger.

**Watch-out — included angle**  
SAS needs the angle **between** the two sides. An angle that is not between them is **not** SAS.

**Try together**

1. All three sides equal → **SSS** → congruent  
2. Only three angles equal → **not** congruent (similar only)  
3. Right triangle: hypotenuse and one leg match → **RHS**
""",
                },
                {
                    "id": "isosceles",
                    "title": "4. Isosceles & equilateral",
                    "diagrams": [{"type": "isosceles_triangle"}],
                    "body": """
| Kind | Sides | Angles |
|------|-------|--------|
| **Scalene** | All different | All different |
| **Isosceles** | Two sides equal | The two **base** angles (opposite the equal sides) are equal |
| **Equilateral** | All three equal | All angles **60°** |

> **Isosceles theorem:** equal sides → equal angles opposite them.  
> **Converse:** equal angles → the sides opposite them are equal.

The **vertex** angle is the one between the two equal sides.  
The other two are **base** angles.

**Try together**

1. Equilateral: each angle is **60°**.  
2. Isosceles, each base angle `40°`. Vertex → `180 − 40 − 40 =` **100°**.  
3. Isosceles, vertex `80°`. Each base → `(180 − 80) / 2 =` **50°**.
""",
                },
                {
                    "id": "inequality",
                    "title": "5. Inequalities in a triangle",
                    "diagrams": [{"type": "triangle", "angle_a": 30, "angle_b": 50}],
                    "body": """
Two rules keep a triangle “able to close”:

> **1. Triangle inequality:** the sum of **any two** sides must be **greater** than the third.  
> `a + b > c`, `a + c > b`, `b + c > a`

> **2. Bigger side faces bigger angle.**  
> The longest side is opposite the largest angle.

**Try together**

1. Sides 5, 7, 10. Is `5 + 7 > 10`? `12 > 10` → **yes**. `5 + 10 > 7` and `7 + 10 > 5` also yes. It **can** be a triangle.  
2. Sides 5, 7, 13. `5 + 7 = 12`, which is **not** greater than 13. → **No triangle**.  
3. In a triangle, the largest angle is at C. The longest side is **AB** (the side opposite C).

**Right triangle extra:** the **hypotenuse** (opposite 90°) is always the **longest** side.
""",
                },
                {
                    "id": "checklist",
                    "title": "6. Ready for practice?",
                    "diagrams": [],
                    "body": """
Tick these out loud:

- [ ] Three angles add to **180°**  
- [ ] Exterior = **sum of the two far interiors**  
- [ ] Congruence: **SSS, SAS, ASA, RHS** — not AAA  
- [ ] Isosceles: equal sides ↔ equal base angles; equilateral → **60°, 60°, 60°**  
- [ ] Two sides must **beat** the third; big side faces big angle

Then open **Practice** and start **Triangles** at Level A.

**Class 10 later:** congruence becomes **similarity** (same shape, maybe different size) and **BPT**.
""",
                },
            ],
        },
        3: {
            "title": "Quadrilaterals",
            "subtitle": "PreReq 4 · Topic 3 · NCERT Class 9 Chapter 8",
            "sections": [
                {
                    "id": "family",
                    "title": "1. What is a quadrilateral?",
                    "diagrams": [{"type": "parallelogram"}],
                    "body": """
A **quadrilateral** is a four-sided closed shape. We write `ABCD` in order around the shape (not jumping across).

> **Angle sum:** the four interior angles add to **360°**.

A diagonal splits a quadrilateral into **two triangles**. Each triangle is 180°, so `180 + 180 = 360`.

**The family (NCERT names)**

| Shape | Parallel sides | Extra “always” |
|-------|----------------|----------------|
| **Parallelogram** | **Two pairs** | See next section |
| **Rectangle** | Two pairs | All angles **90°** |
| **Rhombus** | Two pairs | All **sides equal** |
| **Square** | Two pairs | Rectangle **and** rhombus |
| **Trapezium** | **Exactly one pair** | The parallel sides are the **bases** |
| **Kite** | Usually none | Two pairs of **adjacent** equal sides |

A square is a special rectangle **and** a special rhombus. A rectangle is a special parallelogram.
""",
                },
                {
                    "id": "parallelogram",
                    "title": "2. Parallelogram properties",
                    "diagrams": [{"type": "parallelogram", "show_diagonals": True}],
                    "body": """
In parallelogram `ABCD`, `AB ∥ CD` and `AD ∥ BC`.

**Always true**

- Opposite **sides** are equal: `AB = CD`, `AD = BC`  
- Opposite **angles** are equal: `∠A = ∠C`, `∠B = ∠D`  
- Adjacent angles are **supplementary**: `∠A + ∠B = 180°`  
- Diagonals **bisect each other** (they cut each other in half — the crossing is the midpoint of both)

**Not always true** (unless it is a special parallelogram)

- All sides equal → that is a **rhombus** (or square)  
- All angles 90° → **rectangle** (or square)  
- Diagonals equal → **rectangle** (or square)  
- Diagonals perpendicular → **rhombus** (or square)

**Try together**

1. One angle of a parallelogram is `70°`. Adjacent → **110°**. Opposite → **70°**.  
2. Diagonals meet at O. If `AC = 10 cm`, then `AO =` **5 cm**.
""",
                },
                {
                    "id": "special",
                    "title": "3. Rectangle, rhombus, square",
                    "diagrams": [
                        {"type": "rectangle", "show_diagonals": True},
                        {"type": "rhombus", "show_diagonals": True},
                    ],
                    "body": """
Start from a parallelogram, then add one extra fact.

**Rectangle**

- All angles **90°**  
- Diagonals are **equal** (`AC = BD`) and still bisect each other  
- Sides: opposite sides equal (not all four, unless it is a square)

**Rhombus**

- All **four sides equal**  
- Diagonals **bisect each other at 90°** (they are perpendicular)  
- Diagonals also **bisect the vertex angles**  
- Angles: opposite equal, adjacent supplementary (still a parallelogram)

**Square**

- All sides equal **and** all angles 90°  
- Diagonals equal, perpendicular, and bisect each other

**Try together**

1. “All angles 90°, sides not all equal” → **rectangle** (not square).  
2. “All sides equal, angles not all 90°” → **rhombus**.  
3. Diagonals of a rhombus are **perpendicular**. Diagonals of a rectangle are **equal**.
""",
                },
                {
                    "id": "trap_kite",
                    "title": "4. Trapezium & kite",
                    "diagrams": [{"type": "trapezium"}, {"type": "kite"}],
                    "body": """
**Trapezium (NCERT):** **exactly one** pair of parallel sides.

- The parallel sides are the **bases**  
- Angles on the same **leg** (between the two bases) add to **180°** (they are co-interior on the parallels)

**Kite:** two pairs of **adjacent** equal sides — like `AB = AD` and `CB = CD`.

- Diagonals are **perpendicular**  
- One diagonal is an **axis of symmetry** and **bisects** the other diagonal  
- One pair of opposite angles (between the unequal sides) is equal

**Try together**

1. Two pairs of parallel sides → **parallelogram**, not a trapezium.  
2. A kite is **not** usually a parallelogram (unless it is a rhombus).
""",
                },
                {
                    "id": "midpoint",
                    "title": "5. Mid-point theorem",
                    "diagrams": [{"type": "triangle", "midpoints": True}],
                    "body": """
This theorem lives in the **triangle** chapter but is practised with quads.

> **Mid-point theorem:**  
> Join the midpoints of **two sides** of a triangle.  
> That segment is **parallel** to the third side and **half** as long.

In `△ABC`, if E and F are midpoints of AB and AC, then

`EF ∥ BC` and `EF = ½ BC`

**Converse:** a line through the midpoint of one side, **parallel** to a second side, hits the third side at its **midpoint**.

**Why it shows up with quads**  
Joining the midpoints of **all four** sides of any quadrilateral makes a **parallelogram** (Varignon). You do not need that name — just see “midpoints → parallel and half.”

**Try together**

`BC = 12 cm`, E and F midpoints of the other two sides. `EF =` **6 cm**, and `EF ∥ BC`.
""",
                },
                {
                    "id": "checklist",
                    "title": "6. Ready for practice?",
                    "diagrams": [],
                    "body": """
Tick these out loud:

- [ ] Four angles add to **360°**  
- [ ] Parallelogram: opposite sides/angles equal; adjacent **180°**; diagonals **bisect**  
- [ ] Rectangle → equal diagonals; rhombus → perpendicular diagonals; square → both  
- [ ] Trapezium → **one** pair of parallels; kite → adjacent equal sides  
- [ ] Mid-point theorem → parallel to the third side and **half** as long

Then open **Practice** and start **Quadrilaterals** at Level A.

**Class 10 later:** these properties help with **coordinate geometry** (proving a quad is a parallelogram) and **areas**.
""",
                },
            ],
        },
        4: {
            "title": "Circles",
            "subtitle": "PreReq 4 · Topic 4 · NCERT Class 9 Chapter 10",
            "sections": [
                {
                    "id": "parts",
                    "title": "1. Parts of a circle",
                    "diagrams": [{"type": "circle", "variant": "basic"}, {"type": "circle", "variant": "chord"}],
                    "body": """
A **circle** is every point at the **same distance** from a fixed point — the **centre** `O`.

That distance is the **radius** `r`. Every radius of the same circle is equal.

| Word | What it is |
|------|-------------|
| **Radius** | Segment from the centre to a point **on** the circle (`OA`) |
| **Diameter** | A chord that **passes through the centre**. Longest chord. `d = 2r` |
| **Chord** | Segment joining **two** points on the circle (`AB`) |
| **Arc** | A piece of the **rim** between two points |
| **Circumference** | The full rim. `C = 2πr` |

**Always true**

- `diameter = 2 × radius`  
- The diameter is the **longest** chord  
- All radii of one circle are **equal**

NCERT also says the circle splits the paper into **three** parts: **inside** (interior), the **circle itself**, and **outside** (exterior).

**Try together**

1. Radius `7 cm` → diameter **14 cm**.  
2. Diameter `10 cm` → radius **5 cm**.  
3. Longest chord of a circle? → **diameter**.
""",
                },
                {
                    "id": "equal_chords",
                    "title": "2. Equal chords at the centre",
                    "diagrams": [{"type": "circle", "variant": "equal_chords"}],
                    "body": """
Draw two chords `AB` and `CD` that are the **same length**. Join each end to the centre.

> **Theorem:** Equal chords **subtend equal angles** at the centre.  
> `AB = CD` → `∠AOB = ∠COD`

**Converse:** equal angles at the centre → the chords are equal.  
`∠AOB = ∠COD` → `AB = CD`

**Why (one sentence):** triangles `AOB` and `COD` are **SSS** congruent — two radii and the equal chord — so the centre angles match.

**Try together**

1. `AB = CD` and `∠AOB = 70°` → `∠COD =` **70°**.  
2. `∠AOB = ∠COD` → the chords `AB` and `CD` are **equal**.  
3. Proof rule for those two triangles? → **SSS**.
""",
                },
                {
                    "id": "perp_chord",
                    "title": "3. Perpendicular from the centre",
                    "diagrams": [{"type": "circle", "variant": "perp_chord"}],
                    "body": """
Drop a perpendicular from `O` onto chord `AB`. Call the foot `M`.

> **Theorem:** The perpendicular from the centre to a chord **bisects** the chord.  
> `OM ⊥ AB` → `AM = MB`

**Converse:** the line from the centre to the **midpoint** of a chord is **perpendicular** to the chord.

**Also useful:** equal chords are the **same distance** from the centre. A longer chord sits **closer** to the centre (the diameter is closest of all — distance 0).

**Try together**

1. Chord `AB = 10 cm`, `OM ⊥ AB`. Then `AM =` **5 cm**.  
2. Two equal chords: their distances from `O` are **equal**.
""",
                },
                {
                    "id": "centre_vs_rim",
                    "title": "4. Angle at the centre vs the rim",
                    "diagrams": [
                        {"type": "circle", "variant": "center_angle", "angle": 80},
                        {"type": "circle", "variant": "semicircle"},
                    ],
                    "body": """
The same chord (or arc) `AB` can be “seen” from the centre or from a point `P` on the remaining rim.

> **Theorem:** The angle at the **centre** is **twice** the angle at the circumference.  
> `∠AOB = 2 × ∠APB`  
> (`P` is on the **major** arc when `∠AOB` is the minor-arc angle.)

So if the centre angle is `80°`, the rim angle is **40°**.

**Same segment:** angles that sit on the **same arc** `AB` (same side of the chord) are **equal**.

**Special case — semicircle**

If `AB` is a **diameter** and `P` is on the circle, then `∠AOB = 180°`, so

`∠APB = 90°`

> **Angle in a semicircle is a right angle.**

**Try together**

1. Centre angle `100°` → rim angle **50°**.  
2. Rim angle `35°` (same arc) → centre angle **70°**.  
3. `AB` is a diameter, `P` on the circle → `∠APB =` **90°**.
""",
                },
                {
                    "id": "cyclic",
                    "title": "5. Cyclic quadrilateral",
                    "diagrams": [{"type": "circle", "variant": "cyclic"}],
                    "body": """
A quadrilateral is **cyclic** if all **four vertices** lie on **one** circle.

> **Theorem:** Opposite angles of a cyclic quadrilateral add to **180°**.  
> `∠A + ∠C = 180°` and `∠B + ∠D = 180°`

**Converse:** if opposite angles of a quadrilateral add to 180°, it can be drawn in a circle (it is cyclic).

This is **not** true for a random quadrilateral — only when it sits on a circle.

**Try together**

1. Cyclic `ABCD` with `∠A = 70°` → `∠C =` **110°**.  
2. `∠B = 95°` → `∠D =` **85°**.  
3. “All four corners on a circle” → **cyclic** quadrilateral.
""",
                },
                {
                    "id": "arc_sector",
                    "title": "6. Arc, sector, segment",
                    "diagrams": [{"type": "circle", "variant": "sector"}],
                    "body": """
Two points on a circle cut the rim into a **minor** arc (shorter) and a **major** arc (longer). A **semicircle** is an arc of **180°**.

| Region | Bounded by | Picture |
|--------|------------|---------|
| **Sector** | Two **radii** and an arc | A pizza slice |
| **Segment** | A **chord** and its arc | The crust left after a straight cut |

When the arc is a semicircle, the two segments are the same — each is a **semicircular region**.

**Length of the rim**

`circumference = 2πr`  
(In practice we often use `π ≈ 3.14`.)

**Try together**

1. Region between a chord and an arc → **segment**.  
2. Pizza slice from the centre → **sector**.  
3. Radius `5`, `π ≈ 3.14` → circumference `2 × 3.14 × 5 =` **31.4**.
""",
                },
                {
                    "id": "checklist",
                    "title": "7. Ready for practice?",
                    "diagrams": [],
                    "body": """
Tick these out loud:

- [ ] `diameter = 2 × radius`; diameter is the **longest** chord  
- [ ] Equal chords → **equal angles** at the centre (and converse)  
- [ ] Perpendicular from the centre **bisects** the chord  
- [ ] Angle at the centre is **twice** the angle at the rim; semicircle → **90°**  
- [ ] Cyclic quad: opposite angles add to **180°**  
- [ ] Sector = two radii + arc; segment = chord + arc; `C = 2πr`

Then open **Practice** and start **Circles** at Level A.

**Class 10 later:** **tangents** (a tangent is perpendicular to the radius at the point of contact) and **areas** of sectors and segments.
""",
                },
            ],
        },
    }
}


def get_topic_guide(prereq_id: int, topic_id: int) -> dict[str, Any] | None:
    return TOPIC_GUIDES.get(prereq_id, {}).get(topic_id)


def topics_with_notes(prereq_id: int) -> list[int]:
    return sorted(TOPIC_GUIDES.get(prereq_id, {}))


def prereq_has_notes(prereq_id: int) -> bool:
    return bool(TOPIC_GUIDES.get(prereq_id))
