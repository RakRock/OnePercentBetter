#!/usr/bin/env python3
"""Writes Unit 3 activity markdown notes. Run: python build_unit3_notes.py"""

from pathlib import Path

NOTES = Path(__file__).parent / "ArjunCourse3" / "notes" / "unit_3"
NOTES.mkdir(parents=True, exist_ok=True)

ACTIVITIES = {
    "activity_16_angle_pair_relationships.md": '''# Activity 16: Angle-Pair Relationships

[KEY]
**Complementary** angles sum to **90°**; **supplementary** angles sum to **180°**.  
When a **transversal** crosses **parallel lines**, matching angle pairs are **congruent** (corresponding, alternate interior, alternate exterior).
[/KEY]

## Quick Review Notes

### Main Idea
Angles that share a vertex or a line can be related by their measures. Parallel lines cut by a transversal create predictable equal-angle pairs you can use to find missing measures.

### Key Vocabulary
- **Complementary angles:** Two angles whose measures add to 90°.
- **Supplementary angles:** Two angles whose measures add to 180°.
- **Adjacent angles:** Share a vertex and a side.
- **Linear pair:** Adjacent supplementary angles on a straight line (sum 180°).
- **Transversal:** A line that intersects two or more other lines.
- **Corresponding angles:** Same position at each intersection (congruent if lines are parallel).
- **Alternate interior / exterior:** Opposite sides of the transversal, between or outside the parallels (congruent if parallel).

### Important Formulas / Rules

| Relationship | Equation |
|--------------|----------|
| Complementary | `m∠A + m∠B = 90°` |
| Supplementary | `m∠A + m∠B = 180°` |
| Linear pair | `m∠1 + m∠2 = 180°` |
| Parallel + transversal | Corresponding, alternate interior, alternate exterior angles are **equal** |

[DIAGRAM:complementary]

[DIAGRAM:transversal]

### Example 1 — Complementary

**Problem:** One angle measures 38°. Find its complement.

**Solution:** `90° − 38° = 52°`

**Answer:** **52°**

### Example 2 — Parallel lines

**Problem:** Two parallel lines are cut by a transversal. One angle is 115°. Find a corresponding angle and an alternate interior angle.

**Solution:** Corresponding angle = **115°**. Alternate interior to 115° on the other side of the transversal = **115°** (or use 180° − 115° = 65° for the interior partner on the same side).

**Answer:** **115°** (corresponding); alternate interior pair includes **115°** and **65°**

### Textbook practice (from the PDF)

*SpringBoard Unit 3, Activity 16 (Lessons 16-1, 16-2, Activity 16 Practice).*

---

**1. Complementary angles**

**Problem:** Angles measure `(2x + 10)°` and `(3x − 5)°` and are complementary. Find `x` and each angle.

**Solution:**
1. `(2x + 10) + (3x − 5) = 90` → `5x + 5 = 90` → `5x = 85` → `x = 17`
2. Angles: `2(17) + 10 = 44°`, `3(17) − 5 = 46°` (check: 44 + 46 = 90)

**Answer:** **x = 17**; **44°** and **46°**

---

**2. Supplementary angles**

**Problem:** One angle is twice another; together they are supplementary. Find both angles.

**Solution:**
1. Let smaller = `a`, larger = `2a` → `a + 2a = 180` → `3a = 180` → `a = 60`
2. Angles: **60°** and **120°**

**Answer:** **60°** and **120°**

---

**3. Linear pair**

**Problem:** Two angles form a linear pair. One is `(4x + 12)°`, the other `(2x + 6)°`. Find `x` and each angle.

**Solution:** `(4x + 12) + (2x + 6) = 180` → `6x + 18 = 180` → `6x = 162` → `x = 27`  
Angles: **120°** and **60°**

**Answer:** **x = 27**; **120°**, **60°**

---

**4. Parallel lines — find an angle**

**Problem:** Parallel lines cut by a transversal; one angle is **72°**. Find the measure of its alternate interior angle.

**Solution:** Alternate interior to 72° on parallel lines is **congruent** → **72°**

**Answer:** **72°**

---

**5. Vertical angles**

**Problem:** Two lines intersect. One angle is **(5x − 7)°**, its vertical angle is **(3x + 31)°`. Find `x` and the angle measure.

**Solution:** Vertical angles are equal: `5x − 7 = 3x + 31` → `2x = 38` → `x = 19` → angle **88°**

**Answer:** **x = 19**; **88°**

---

**6. Multi-step parallel lines**

**Problem:** `m∠1 = 110°` (corresponding to an interior angle in a parallel-line diagram). Find `m∠2` if ∠2 is alternate interior to the 70° angle on the same transversal.

**Solution:** If one interior angle is 70°, its alternate interior partner is **70°**. Use 180° − 110° = 70° for co-interior on one side.

**Answer:** **70°** (when ∠2 is alternate interior to 70°)

### Common Mistakes
- Mixing **90°** (complementary) with **180°** (supplementary).
- Assuming any two angles on a diagram are supplementary without a straight line.
- For parallel lines, confusing **corresponding** with **alternate interior**.

### Mini Summary
- Complementary → **90°**; supplementary / linear pair → **180°**.
- Parallel lines + transversal → use **congruent** angle pairs to find missing measures.
''',

    "activity_17_angles_triangles_quadrilaterals.md": '''# Activity 17: Angles of Triangles and Quadrilaterals

[KEY]
The three interior angles of any triangle sum to **180°**.  
The four interior angles of any quadrilateral sum to **360°**. Use these facts to write equations and find missing angle measures.
[/KEY]

## Quick Review Notes

### Main Idea
In a triangle, if you know two angles you can find the third. In a quadrilateral, if you know three angles you can find the fourth. Exterior angles of a triangle relate to the non-adjacent interior angles.

### Key Vocabulary
- **Interior angle:** Inside the polygon.
- **Exterior angle:** Formed by extending one side; equals sum of two remote interior angles in a triangle.
- **Acute / obtuse / right triangle:** All acute, one obtuse, or one 90° angle.
- **Equilateral triangle:** All angles 60°.

### Important Formulas / Rules

| Shape | Angle sum |
|-------|-----------|
| Triangle | `m∠A + m∠B + m∠C = 180°` |
| Quadrilateral | `m∠A + m∠B + m∠C + m∠D = 360°` |
| Exterior angle of △ | `m∠ext = m∠1 + m∠2` (remote interior angles) |

[DIAGRAM:triangle_sum]

[DIAGRAM:quadrilateral]

### Example 1 — Third angle of a triangle

**Problem:** Two angles of a triangle measure **32°** and **70°**. Find the third.

**Solution:** `180 − 32 − 70 = 78°`

**Answer:** **78°**

### Example 2 — Solve for x

**Problem:** Angles in a triangle are `x°`, `(2x + 4)°`, and `(2x − 9)°`.

**Solution:** `x + 2x + 4 + 2x − 9 = 180` → `5x − 5 = 180` → `5x = 185` → `x = 37`  
Angles: **37°**, **78°**, **65°**

**Answer:** **x = 37**; angles **37°, 78°, 65°**

### Textbook practice (from the PDF)

*Activity 17 Practice, Lesson 17-1.*

---

**1. Activity 17 Practice #1**

**Problem:** Two angles of a triangle measure **32°** and **70°**. Find the third angle.

**Solution:** `180 − 32 − 70 = 78°`

**Answer:** **78°**

---

**2. Activity 17 Practice #6**

**Problem:** Two angles are **38°** and **47°**. Find the third.

**Solution:** `180 − 38 − 47 = 95°`

**Answer:** **95°** (choice B)

---

**3. Activity 17 Practice #12**

**Problem:** Right triangle; one acute angle is **22°**. Find the other acute angle.

**Solution:** `90 − 22 = 68°`

**Answer:** **68°**

---

**4. Activity 17 Practice #11**

**Problem:** Angles `x°`, `(2x + 4)°`, `(2x − 9)°`.

**Solution:** `5x − 5 = 180` → `x = 37`; angles **37°, 78°, 65°**

**Answer:** **x = 37**; **37°, 78°, 65°**

---

**5. Activity 17 Practice #10 — error check**

**Problem:** Player picked **100°** and **82°** for two angles of a triangle. Why is that impossible?

**Solution:** `100 + 82 = 182 > 180` — three interior angles cannot sum to more than 180°.

**Answer:** **Impossible** — two angles already exceed 180°

---

**6. Activity 17 Practice #7**

**Problem:** In △DEF, `m∠D = (3x − 6)°`, `m∠E = (3x − 6)°`, `m∠F = (2x)°`. Find `m∠F`.

**Solution:** `(3x − 6) + (3x − 6) + 2x = 180` → `8x − 12 = 180` → `8x = 192` → `x = 24` → `m∠F = 48°`

**Answer:** **48°** (choice C)

### Common Mistakes
- Forgetting the third angle must make the **sum 180°**, not 360°.
- In a right triangle, using 180° instead of **90°** for the two acute angles.
- Adding exterior angles into the 180° triangle sum.

### Mini Summary
- Triangle: **180°** total; quadrilateral: **360°** total.
- Set up `angle₁ + angle₂ + angle₃ = 180` and solve for variables.
''',

    "activity_18_introduction_transformations.md": '''# Activity 18: Introduction to Transformations

[KEY]
A **transformation** moves or flips a figure in the plane. **Translation** slides, **reflection** flips across a line, **rotation** turns about a point. The original is the **preimage**; the result is the **image**.
[/KEY]

## Quick Review Notes

### Main Idea
Transformations describe how figures move on the coordinate plane or in a diagram. You name the preimage and image and describe the motion in words or with coordinates.

### Key Vocabulary
- **Preimage:** Original figure before the transformation.
- **Image:** Figure after the transformation (often labeled with prime marks: A′).
- **Translation:** Slide every point the same direction and distance.
- **Reflection:** Flip across a line of reflection (mirror line).
- **Rotation:** Turn about a center point by a given angle and direction (clockwise / counterclockwise).

### Important Rules

| Transformation | What stays the same | What changes |
|----------------|---------------------|--------------|
| Translation | Size, shape, orientation | Position |
| Reflection | Size, shape | Orientation (left/right) |
| Rotation | Size, shape | Position and orientation (unless 360°) |

**Coordinate translation:** `(x, y) → (x + a, y + b)` moves right `a`, up `b`.

[DIAGRAM:transformations]

[DIAGRAM:coordinate]

### Example 1 — Translation

**Problem:** Translate point `(3, 2)` right 4 units and down 1 unit.

**Solution:** `(3 + 4, 2 − 1) = (7, 1)`

**Answer:** **(7, 1)**

### Example 2 — Reflection across x-axis

**Problem:** Reflect `(−2, 5)` across the x-axis.

**Solution:** Change sign of y: **(−2, −5)**

**Answer:** **(−2, −5)**

### Textbook practice (from the PDF)

*Activity 18, Lessons 18-1 through 18-4.*

---

**1. Translation on grid**

**Problem:** Move triangle 3 units left and 2 units up. Vertex A is at `(5, 1)`. Where is A′?

**Solution:** `(5 − 3, 1 + 2) = (2, 3)`

**Answer:** **(2, 3)**

---

**2. Reflection across y-axis**

**Problem:** Reflect `(4, −3)` across the y-axis.

**Solution:** Negate x: **(−4, −3)**

**Answer:** **(−4, −3)**

---

**3. Rotation 90° counterclockwise about origin**

**Problem:** Rotate `(3, 1)` 90° CCW about the origin.

**Solution:** Rule: `(x, y) → (−y, x)` → **(−1, 3)**

**Answer:** **(−1, 3)**

---

**4. Describe a transformation**

**Problem:** Preimage at `(1, 2)`, image at `(5, 2)`. What transformation?

**Solution:** Same y, x increased by 4 → **translation 4 units right**

**Answer:** **Translation right 4 units**

---

**5. Reflection across x-axis**

**Problem:** Vertices `(2, 4)`, `(0, 1)`, `(3, 0)` reflected over x-axis. Give one vertex of the image.

**Solution:** `(2, 4) → (2, −4)`

**Answer:** Example image vertex **(2, −4)**

---

**6. Rotation 180° about origin**

**Problem:** Rotate `(−2, 3)` 180° about the origin.

**Solution:** `(x, y) → (−x, −y)` → **(2, −3)**

**Answer:** **(2, −3)**

### Common Mistakes
- Confusing **(x, y) → (−y, x)** (90° CCW) with **(y, −x)** (90° CW).
- Reflecting across the wrong axis (x vs y).
- Forgetting prime notation for **image** points.

### Mini Summary
- Translation: add to coordinates; reflection: flip one coordinate; rotation: use rotation rules about the origin.
''',

    "activity_19_rigid_transformations_compositions.md": '''# Activity 19: Rigid Transformations and Compositions

[KEY]
**Rigid transformations** (translations, reflections, rotations) keep **size and shape** — images are **congruent** to the preimage. A **composition** applies two or more transformations in order.
[/KEY]

## Quick Review Notes

### Main Idea
Rigid motions are also called **isometries**. Distance, angle measures, and area do not change. You can perform one transformation after another; order can matter.

### Key Vocabulary
- **Rigid transformation / isometry:** Preserves distance and angle measure.
- **Congruent figures:** Same size and shape; one is the image of the other under a rigid motion.
- **Composition:** Two or more transformations performed in sequence.
- **Coordinate rules (origin):**
  - 90° CCW: `(x, y) → (−y, x)`
  - 180°: `(x, y) → (−x, −y)`
  - 90° CW: `(x, y) → (y, −x)`

[DIAGRAM:rigid]

[DIAGRAM:rotation]

### Example 1 — Congruence

**Problem:** △ABC is rotated to △A′B′C′. Are the triangles congruent?

**Solution:** Rotation is rigid → corresponding sides and angles match → **yes, congruent**.

**Answer:** **Yes — congruent**

### Example 2 — 90° rotation

**Problem:** Rotate `(2, −1)` 90° counterclockwise about the origin.

**Solution:** `(−(−1), 2) = (1, 2)`

**Answer:** **(1, 2)**

### Textbook practice (from the PDF)

*Activity 19 Practice, Lesson 19-1.*

---

**1. Activity 19 Practice #5a — areas**

**Problem:** Compare areas of images in Items 1–4 to the original under rigid transformations.

**Solution:** Rigid transformations preserve area → **all areas equal**

**Answer:** **Same area** as original

---

**2. Activity 19 Practice #5b — sides**

**Problem:** What can you say about corresponding sides?

**Solution:** Congruent figures → **corresponding sides equal in length**

**Answer:** **Equal lengths**

---

**3. Activity 19 Practice #5d — congruent?**

**Problem:** Are images congruent to the original?

**Solution:** Rigid motions produce **congruent** images with same side lengths and angle measures.

**Answer:** **Yes — congruent**

---

**4. Rotate (3, 1) 90° CCW**

**Problem:** Find image coordinates.

**Solution:** **(−1, 3)**

**Answer:** **(−1, 3)**

---

**5. Reflect then translate**

**Problem:** Reflect `(4, 2)` over x-axis, then translate 3 units left.

**Solution:** Reflect → `(4, −2)`; translate → `(1, −2)`

**Answer:** **(1, −2)**

---

**6. 180° rotation of (−3, 2)**

**Problem:** Rotate 180° about the origin.

**Solution:** **(3, −2)**

**Answer:** **(3, −2)**

### Common Mistakes
- Thinking dilations are rigid (they change size).
- Applying the **second** transformation to the **preimage** instead of the first image.
- Wrong rotation rule sign.

### Mini Summary
- Rigid = **congruent** image; area and side lengths unchanged.
- Compose by applying steps **in order** to the current figure.
''',

    "activity_20_similar_triangles.md": '''# Activity 20: Similar Triangles

[KEY]
**Similar** figures have the same shape but not necessarily the same size — angles are congruent and sides are **proportional**. **AA** (two pairs of congruent angles) is enough to prove triangles similar.
[/KEY]

## Quick Review Notes

### Main Idea
If two triangles have the same angle measures, they are similar. You can write a similarity statement matching vertices in order and set up ratios of corresponding sides.

### Key Vocabulary
- **Similar (≈):** Same shape; proportional sides, congruent angles.
- **Scale factor:** Ratio of corresponding side lengths (image ÷ preimage).
- **AA Similarity:** Two pairs of congruent angles → triangles similar.
- **SSS / SAS similarity:** All sides proportional, or two sides proportional with included angle equal.

[DIAGRAM:similar]

[DIAGRAM:aa]

### Important Rules

If △ABC ∼ △DEF, then `AB/DE = BC/EF = AC/DF`.

### Example 1 — AA

**Problem:** Two angles in one triangle are 50° and 60°; two in another are 50° and 60°. Similar?

**Solution:** AA → **yes**, third angles both 70°.

**Answer:** **Similar (AA)**

### Example 2 — Side lengths

**Problem:** △ABC has sides 6, 8, 10. Which triangle could be similar? (A) 3, 4, 5 (B) 6, 8, 9

**Solution:** Ratios 6:8:10 = 3:4:5 → **(A)**; (B) fails 10:9 ratio.

**Answer:** **(A) 3, 4, 5**

### Textbook practice (from the PDF)

*Activity 20 Practice, Lesson 20-1.*

---

**1. Activity 20 Practice #1 — are they similar?**

**Problem:** Angles 88°, 49°, 43° in one triangle; 49°, 43° in another with proportional sides 12:6, 9:6, etc.

**Solution:** Shared angles 49° and 43° → third angles match → **similar** by AA. Write `△BCD ∼ △HIJ` (match order to corresponding angles).

**Answer:** **Similar** — AA

---

**2. Activity 20 Practice #2 — △JOE ∼ △AMY**

**Problem:** Given 20° and 80° at some vertices, find `m∠J`, `m∠O`, `m∠Y`, `m∠M`.

**Solution:** Match corresponding vertices from similarity statement; use **180°** sum and equal corresponding angles.

**Answer:** Use correspondence from diagram (e.g. if J↔A, copy known angles)

---

**3. Activity 20 Practice #3**

**Problem:** △ABC sides 15, 20, 25 cm. Which could be similar?

**Solution:** Scale 1:2 → **30, 40, 50** mm or cm; check **6 m, 8 m, 10 m** (choice B) — ratio 3:4:5 matches 15:20:25.

**Answer:** **(B) 6 m, 8 m, 10 m**

---

**4. Find missing side**

**Problem:** △ABC ∼ △DEF, AB = 8, DE = 12, BC = 6. Find EF.

**Solution:** Scale factor `12/8 = 1.5` → `EF = 6 × 1.5 = 9`

**Answer:** **EF = 9**

---

**5. AA with algebra**

**Problem:** Angles `(2x)°`, `(3x + 10)°`, and `(x + 30)°` in a triangle. Find x.

**Solution:** `2x + 3x + 10 + x + 30 = 180` → `6x + 40 = 180` → `x = 70/3` (verify each angle positive and < 180)

**Answer:** Solve with **sum = 180°**

---

**6. Proportional perimeters**

**Problem:** Similar triangles with scale factor 2:3. Smaller perimeter 18. Larger perimeter?

**Solution:** Perimeters scale like sides → `18 × (3/2) = 27`

**Answer:** **27**

### Common Mistakes
- Matching wrong vertices in similarity statements.
- Adding lengths instead of using **ratios**.
- Assuming similar without checking angles or side ratios.

### Mini Summary
- **AA** is the most common proof of similarity.
- Set up **corresponding side ratios** equal to each other.
''',

    "activity_21_dilations.md": '''# Activity 21: Dilations

[KEY]
A **dilation** changes size but not shape — the image is **similar** to the preimage. **Scale factor k** tells how much to enlarge (`k > 1`) or shrink (`0 < k < 1`). Center of dilation is the fixed point.
[/KEY]

## Quick Review Notes

### Main Idea
Every point moves along a ray from the center through the preimage point. Distance to the center is multiplied by `k`. On the coordinate plane with center at the origin: `(x, y) → (kx, ky)`.

### Key Vocabulary
- **Dilation:** Transformation with scale factor k about a center.
- **Center of dilation:** Fixed point (only point that may not move).
- **Enlargement:** k > 1; **reduction:** 0 < k < 1.

[DIAGRAM:dilation]

[DIAGRAM:scale_factor]

### Example 1 — Scale factor 2

**Problem:** Preimage segment length 5 cm. Image under dilation k = 2?

**Solution:** `5 × 2 = 10` cm

**Answer:** **10 cm**

### Example 2 — Coordinate dilation

**Problem:** Dilate `(4, 6)` about origin with k = 1/2.

**Solution:** `(2, 3)`

**Answer:** **(2, 3)**

### Textbook practice (from the PDF)

*Activity 21, Lesson 21-1.*

---

**1. Lesson 21-1 #3a — factor 2**

**Problem:** Dilate △PQR by factor 2 from center P.

**Solution:** Each vertex on ray from P through Q (or R) lands at **twice** the distance from P.

**Answer:** Side lengths **doubled**

---

**2. Lesson 21-1 #3b — factor 1/2**

**Problem:** Dilate by 1/2.

**Solution:** Distances from center are **halved**.

**Answer:** Half the original size

---

**3. Origin dilation k = 3**

**Problem:** Image of `(2, −1)`?

**Solution:** **(6, −3)**

**Answer:** **(6, −3)**

---

**4. Find scale factor**

**Problem:** Preimage length 8, image length 12. Find k.

**Solution:** `k = 12/8 = 1.5`

**Answer:** **k = 1.5**

---

**5. Area and scale factor**

**Problem:** k = 2. How does area change?

**Solution:** Area scales by `k²` → `2² = 4` times larger

**Answer:** **4 times** the area

---

**6. Reduction on coordinate plane**

**Problem:** Rectangle from (0,0) to (8, 4) dilated by k = 0.5 about origin.

**Solution:** Corner **(8, 4) → (4, 2)**

**Answer:** Image corner **(4, 2)**

### Common Mistakes
- Using **k** for area change instead of **k²**.
- Dilating from the wrong **center**.
- Confusing dilation (similar) with translation (rigid).

### Mini Summary
- Multiply distances from center by **k**; coordinates at origin: `(kx, ky)`.
- **k > 1** enlarge; **0 < k < 1** reduce.
''',

    "activity_22_pythagorean_theorem.md": '''# Activity 22: The Pythagorean Theorem

[KEY]
In a **right triangle**, `a² + b² = c²` where **c** is the **hypotenuse** (longest side, opposite the right angle). Use it to find a missing leg or the hypotenuse.
[/KEY]

## Quick Review Notes

### Main Idea
The Pythagorean Theorem links the three sides of a right triangle. Identify the right angle first; the side across from it is c.

### Key Vocabulary
- **Right triangle:** One 90° angle.
- **Legs:** Sides that form the right angle (a and b).
- **Hypotenuse:** Longest side, opposite the right angle (c).

### Formula

`a² + b² = c²`  →  `c = √(a² + b²)`  or  `a = √(c² − b²)`

[DIAGRAM:pythagorean]

[DIAGRAM:solve_triangle]

### Example 1 — Hypotenuse

**Problem:** Legs 5 and 12. Find c.

**Solution:** `c² = 25 + 144 = 169` → `c = 13`

**Answer:** **13**

### Example 2 — Missing leg

**Problem:** Leg 9, hypotenuse 15. Find other leg.

**Solution:** `b² = 225 − 81 = 144` → `b = 12`

**Answer:** **12**

### Textbook practice (from the PDF)

*Activity 22 Practice.*

---

**1. Find hypotenuse**

**Problem:** Legs 7 and 24.

**Solution:** `49 + 576 = 625` → **25**

**Answer:** **25**

---

**2. Find leg**

**Problem:** Leg 8, hypotenuse 17.

**Solution:** `289 − 64 = 225` → leg **15**

**Answer:** **15**

---

**3. Word problem**

**Problem:** Ladder 10 ft reaches 6 ft up a wall. How far is the base from the wall?

**Solution:** `b² = 100 − 36 = 64` → **8 ft**

**Answer:** **8 feet**

---

**4. Is it a right triangle?**

**Problem:** Sides 9, 12, 15.

**Solution:** `81 + 144 = 225 = 15²` → **yes**

**Answer:** **Right triangle**

---

**5. Diagonal of rectangle**

**Problem:** Rectangle 9 ft by 12 ft. Diagonal length?

**Solution:** `81 + 144 = 225` → **15 ft**

**Answer:** **15 feet**

---

**6. Find leg (decimal)**

**Problem:** Leg 5, hypotenuse 13.

**Solution:** `169 − 25 = 144` → **12**

**Answer:** **12**

### Common Mistakes
- Putting the **hypotenuse** as a leg in the formula.
- Forgetting to **take the square root** at the end.
- Adding legs when you should **subtract** (finding a leg).

### Mini Summary
- Right triangle only: **`a² + b² = c²`** with c opposite the right angle.
''',

    "activity_23_applying_pythagorean_theorem.md": '''# Activity 23: Applying the Pythagorean Theorem

[KEY]
Use `a² + b² = c²` in real situations: ladders, distances on a grid, diagonals of rectangles, and **3D** problems (find a leg in a right triangle, then use it in another).
[/KEY]

## Quick Review Notes

### Main Idea
Draw or imagine a right triangle in the situation. Label legs and hypotenuse, substitute, and solve. For distance between two points, horizontal and vertical changes are the legs.

### Key Vocabulary
- **Distance formula:** From `(x₁, y₁)` to `(x₂, y₂)`: `d = √((x₂ − x₁)² + (y₂ − y₁)²)` — comes from the Pythagorean Theorem.
- **Space diagonal:** Diagonal through a rectangular prism; often use two right triangles.

[DIAGRAM:ladder]

[DIAGRAM:diagonal]

### Example 1 — Ladder

**Problem:** Ladder 25 ft, base 15 ft from wall. How high on the wall?

**Solution:** `h² = 625 − 225 = 400` → **20 ft**

**Answer:** **20 feet**

### Example 2 — Distance on grid

**Problem:** From (1, 2) to (4, 6).

**Solution:** Δx = 3, Δy = 4 → `d = √(9 + 16) = 5`

**Answer:** **5 units**

### Textbook practice (from the PDF)

*Activity 23 Practice.*

---

**1. Ladder problem**

**Problem:** Wall height 20 ft, base 15 ft from wall. Ladder length?

**Solution:** `400 + 225 = 625` → **25 ft**

**Answer:** **25 feet**

---

**2. Two-dimensional distance**

**Problem:** Town A at (0, 0), town B at (9, 12). Distance?

**Solution:** `√(81 + 144) = 15`

**Answer:** **15 units**

---

**3. Square diagonal**

**Problem:** Square side 10 m. Diagonal?

**Solution:** `100 + 100 = 200` → `√200 = 10√2 ≈ 14.1 m`

**Answer:** **10√2 m** (≈ **14.1 m**)

---

**4. Rectangle diagonal**

**Problem:** Room 12 ft by 16 ft. Diagonal of floor?

**Solution:** `144 + 256 = 400` → **20 ft**

**Answer:** **20 feet**

---

**5. 3D — box diagonal**

**Problem:** Box 3 × 4 × 5. Space diagonal?

**Solution:** Floor diagonal `√(9+16)=5`; then `√(25+25)=√50=5√2`

**Answer:** **5√2** (≈ **7.07**)

---

**6. Path on coordinate plane**

**Problem:** Ship at (2, 5) sails to (10, 11). Direct distance?

**Solution:** Δx = 8, Δy = 6 → **10**

**Answer:** **10 units**

### Common Mistakes
- Not drawing the **right triangle** in context.
- Using **subtraction** in the wrong order when solving for a leg.
- Forgetting units in the final answer.

### Mini Summary
- Sketch the right triangle; use **horizontal and vertical** as legs when needed.
''',

    "activity_24_converse_pythagorean_theorem.md": '''# Activity 24: Converse of the Pythagorean Theorem

[KEY]
If `a² + b² = c²` for the three sides of a triangle (with **c** the longest side), then the triangle is a **right triangle**. **Pythagorean triples** are whole-number solutions like 3-4-5 and 5-12-13.
[/KEY]

## Quick Review Notes

### Main Idea
The converse lets you **test** whether a triangle is right without measuring angles. Check the longest side squared against the sum of squares of the other two.

### Key Vocabulary
- **Converse:** If `a² + b² = c²`, then the angle opposite c is 90°.
- **Pythagorean triple:** Three whole numbers that satisfy `a² + b² = c²`.
- **Common triples:** 3-4-5, 5-12-13, 8-15-17, 7-24-25.

[DIAGRAM:converse]

[DIAGRAM:test_triangle]

### Example 1 — Is it right?

**Problem:** Sides 5, 12, 13.

**Solution:** `25 + 144 = 169 = 13²` → **right triangle**

**Answer:** **Yes**

### Example 2 — Not right

**Problem:** Sides 5, 4, 6 (longest 6).

**Solution:** `25 + 16 = 41 ≠ 36` → **not** a right triangle

**Answer:** **No**

### Textbook practice (from the PDF)

*Activity 24, Lesson 24-1 and 24-2.*

---

**1. Test 8, 15, 17**

**Solution:** `64 + 225 = 289 = 17²` → **right**

**Answer:** **Right triangle**

---

**2. Test 6, 7, 8**

**Solution:** `36 + 49 = 85 ≠ 64` → **not right**

**Answer:** **Not a right triangle**

---

**3. Pythagorean triple 3-4-5 × 2**

**Problem:** Multiply 3-4-5 by 2. Still a triple?

**Solution:** 6-8-10 → `36 + 64 = 100` → **yes**

**Answer:** **Yes — 6, 8, 10**

---

**4. Find missing side to test**

**Problem:** Which set is a triple? (A) 9, 10, 12 (B) 9, 12, 15

**Solution:** (B) `81 + 144 = 225 = 15²`

**Answer:** **(B)**

---

**5. Converse application**

**Problem:** A triangle has sides 10, 24, 26. Right?

**Solution:** `100 + 576 = 676 = 26²` → **yes**

**Answer:** **Right triangle**

---

**6. Generate triple from 5-12-13 × 3**

**Problem:** Multiply by 3.

**Solution:** **15, 36, 39** — still satisfies `a² + b² = c²`

**Answer:** **15, 36, 39**

### Common Mistakes
- Squaring the **wrong** side (must use longest as c).
- Saying “close enough” — need **exact** equality for the converse.
- Confusing **theorem** (right → equation) with **converse** (equation → right).

### Mini Summary
- Longest side c: if `a² + b² = c²`, triangle is **right**.
''',

    "activity_25_surface_area.md": '''# Activity 25: Surface Area

[KEY]
**Surface area (SA)** is the total area of all **faces** of a 3D figure. For a **rectangular prism**, `SA = 2(lw + lh + wh)`. Unfold the solid into a **net** to see each face.
[/KEY]

## Quick Review Notes

### Main Idea
Add the areas of every face (or use a formula). Draw a net when the solid is unfamiliar. Units are **square** (cm², ft²).

### Key Vocabulary
- **Face:** Flat surface of a prism or pyramid.
- **Net:** Flat pattern that folds into a 3D figure.
- **Lateral faces:** Sides (not top/bottom for prisms).

### Formulas

| Solid | Surface area |
|-------|----------------|
| Rectangular prism | `SA = 2(lw + lh + wh)` |
| Cube (side s) | `SA = 6s²` |
| Cylinder | `SA = 2πr² + 2πrh` (two circles + rectangle) |
| Square pyramid | `SA = base area + ½ × perimeter × slant height` |

[DIAGRAM:prism_net]

[DIAGRAM:surface_area]

### Example 1 — Rectangular prism

**Problem:** l = 5 in, w = 4 in, h = 3 in. Find SA.

**Solution:** `SA = 2(20 + 15 + 12) = 2(47) = 94` in²

**Answer:** **94 in²**

### Example 2 — Cube

**Problem:** Side 6 cm.

**Solution:** `6 × 6² = 6 × 36 = 216` cm²

**Answer:** **216 cm²**

### Textbook practice (from the PDF)

*Activity 25 Practice.*

---

**1. Prism SA**

**Problem:** 5 in × 8 in × 6 in.

**Solution:** `2(40 + 30 + 48) = 236` in²

**Answer:** **236 in²**

---

**2. Cube**

**Problem:** Side 7.1 mm.

**Solution:** `6 × (7.1)² ≈ 6 × 50.41 ≈ 302.5` mm²

**Answer:** **≈ 302.5 mm²** (or exact `6 × 7.1²`)

---

**3. Find missing dimension**

**Problem:** SA = 94 ft², l = 5, w = 4. Find h.

**Solution:** `94 = 2(20 + 5h + 4h)` → `47 = 20 + 9h` → `h = 3`

**Answer:** **3 ft**

---

**4. Cube from SA**

**Problem:** SA of cube is 150 cm². Find side.

**Solution:** `6s² = 150` → `s² = 25` → `s = 5`

**Answer:** **5 cm**

---

**5. Cylinder (concept)**

**Problem:** r = 3 cm, h = 10 cm. SA ≈ ? (use π ≈ 3.14)

**Solution:** `2π(9) + 2π(3)(10) = 18π + 60π = 78π ≈ 244.9` cm²

**Answer:** **≈ 245 cm²**

---

**6. Net reasoning**

**Problem:** Prism net has three pairs of rectangles 2×3, 2×4, 3×4. SA?

**Solution:** `2(6 + 8 + 12) = 52`

**Answer:** **52 square units**

### Common Mistakes
- Using **volume** formula instead of surface area.
- Forgetting to **double** all three face pairs in `2(lw + lh + wh)`.
- Leaving answer in **linear** units instead of square units.

### Mini Summary
- Count every **face**; prism formula **2(lw + lh + wh)**.
''',

    "activity_26_volumes_of_solids.md": '''# Activity 26: Volumes of Solids

[KEY]
**Volume** is space inside a 3D figure (cubic units). Prism and cylinder: **V = Bh** (area of base × height). Pyramid and cone: **V = (1/3)Bh**. Sphere: **V = (4/3)πr³**.
[/KEY]

## Quick Review Notes

### Main Idea
Multiply base area by height for prisms and cylinders. Pyramids and cones use one-third of that. Label answers in **cubic** units (cm³, ft³).

### Key Vocabulary
- **Base (B):** Area of the bottom face (or cross-section).
- **Height (h):** Perpendicular distance between bases (not always slant height).
- **Cube:** Special prism with `V = s³`.

### Formulas

| Solid | Volume |
|-------|--------|
| Rectangular prism | `V = lwh` |
| Cube | `V = s³` |
| Cylinder | `V = πr²h` |
| Square pyramid | `V = (1/3)s²h` |
| Cone | `V = (1/3)πr²h` |
| Sphere | `V = (4/3)πr³` |

[DIAGRAM:volume_prism]

[DIAGRAM:volume_solids]

### Example 1 — Rectangular prism

**Problem:** 5 in × 8 in × 6 in.

**Solution:** `5 × 8 × 6 = 240` in³

**Answer:** **240 in³**

### Example 2 — Square pyramid

**Problem:** Base edge 12 cm, height 20 cm.

**Solution:** `V = (1/3)(12²)(20) = (1/3)(144)(20) = 960` cm³

**Answer:** **960 cm³**

### Textbook practice (from the PDF)

*Activity 26 Practice, Lesson 26-1.*

---

**1. Activity 26 Practice #1**

**Problem:** Prism 5 in × 8 in × 6 in.

**Solution:** `240` in³

**Answer:** **240 cubic inches**

---

**2. Activity 26 Practice #2**

**Problem:** Cube side 7.1 mm.

**Solution:** `7.1³ ≈ 357.9` mm³

**Answer:** **≈ 358 mm³**

---

**3. Activity 26 Practice #3**

**Problem:** Square pyramid base edge 12 cm, height 20 cm.

**Solution:** `(1/3)(144)(20) = 960` cm³

**Answer:** **960 cm³**

---

**4. Activity 26 Practice #5**

**Problem:** V = 80 ft³, l = 8 ft, h = 4 ft. Find width.

**Solution:** `80 = 8 × w × 4` → `w = 80/32 = 2.5`

**Answer:** **2.5 feet**

---

**5. Cube planter**

**Problem:** Cube edge 1.5 ft. Volume?

**Solution:** `1.5³ = 3.375` ft³

**Answer:** **3.375 ft³**

---

**6. Cylinder**

**Problem:** r = 4 cm, h = 10 cm (π ≈ 3.14).

**Solution:** `π(16)(10) ≈ 502.4` cm³

**Answer:** **≈ 502 cm³**

### Common Mistakes
- Using **slant height** instead of perpendicular height for pyramids/cones.
- Forgetting **(1/3)** for pyramids and cones.
- Reporting **square** units instead of **cubic** units.

### Mini Summary
- Prism/cylinder: **V = Bh**; pyramid/cone: **V = (1/3)Bh**.
''',
}

COMBINED = '''# Unit 3: Geometry — Lesson Notes Cheat Sheet

## Angle relationships (Activities 16–17)
- Complementary: **90°** | Supplementary / linear pair: **180°**
- Triangle interior angles: **180°** | Quadrilateral: **360°**
- Parallel lines + transversal → corresponding & alternate angles **congruent**

## Transformations (Activities 18–21)
- **Rigid:** translation, reflection, rotation → **congruent** image (same size)
- **Dilation:** scale factor **k** → similar image; `(x,y) → (kx, ky)` about origin
- **AA** → similar triangles; side ratios equal

## Pythagorean Theorem (Activities 22–24)
- Right triangle: **`a² + b² = c²`** (c = hypotenuse)
- **Converse:** if `a² + b² = c²` with c longest → **right triangle**
- Triples: 3-4-5, 5-12-13, 8-15-17

## Surface area & volume (Activities 25–26)
- Rectangular prism: **SA = 2(lw + lh + wh)** | **V = lwh**
- Pyramid / cone: **V = (1/3)Bh** | Sphere: **V = (4/3)πr³**

## Embedded assessments (from textbook)
- After Activity 17: Angle measures
- After Activity 19: Rigid transformations
- After Activity 21: Similarity and dilations
- After Activity 24: Pythagorean Theorem
- After Activity 26: Surface area and volume
'''


def main():
    for name, body in ACTIVITIES.items():
        path = NOTES / name
        path.write_text(body.strip() + "\n", encoding="utf-8")
        print(f"wrote {path}")
    combined_path = NOTES / "unit_3_geometry_lesson_notes.md"
    combined_path.write_text(COMBINED.strip() + "\n", encoding="utf-8")
    print(f"wrote {combined_path}")


if __name__ == "__main__":
    main()
