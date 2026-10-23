# VI-2 Patterns and Modeling: Using Patterns to Write and Evaluate Expressions

[KEY]
**Square numbers** `n²` and **rectangular numbers** `n(n + 1)` do **not** have a constant difference (the gap grows). **Triangular numbers** are `n(n + 1) / 2` — half of the matching rectangle, and `T_n + T_{n−1} = n²`. For **joined polygons**, count the outer perimeter: the first shape has all of its sides; each new shape adds all of its sides minus the **2** sides that become internal. Pentagon walkway: `5 + 3(n − 1)` or `3n + 2`. Octagon walkway: `8 + 6(n − 1)` or `6n + 2`.
[/KEY]

## Quick Review Notes

### Main Idea
Class packet **VI-2 / 9-2** (Course 3 Unit 6, after the 10/19 VI-1 agenda): use a picture sequence to decide whether the **count** has a constant difference. If not, name the special pattern (**square**, **rectangular**, **triangular**) and write the expression in **n**. On the back, joined pentagons and octagons **do** have a constant perimeter difference.

### Class method (same order as the worksheet)

1. Count dots in the next figures (4th, 5th, 6th).
2. Ask: is the **difference** always the same? If the gap grows, it is **not** a constant-difference pattern.
3. Describe the pattern in words, then write an expression in **n**.
4. Substitute a far figure (10th, 40th, 99th) into that expression.
5. Classify a number as square, rectangular, and/or triangular by solving `n²`, `n(n + 1)`, or `n(n + 1)/2`.
6. For joined polygons: list perimeters, table the **constant difference**, write `first + d(n − 1)`, then evaluate.

### Important Formulas / Rules

| Pattern | Figures (dots) | nth figure | Constant difference? |
|---------|----------------|------------|----------------------|
| Square | 1, 4, 9, 16, … | `n²` | No — gaps are 3, 5, 7, … |
| Rectangular | 2, 6, 12, 20, … | `n(n + 1)` | No — gaps are 4, 6, 8, … |
| Triangular | 1, 3, 6, 10, … | `n(n + 1) / 2` | No — gaps are 2, 3, 4, … |

**Joined polygons** (each new shape shares **one** full side):

| Walkway | Figure 1 | Add each time | Expression | Far figure |
|---------|----------|---------------|------------|------------|
| Regular pentagon, side 1 cm | 5 cm | +3 cm | `5 + 3(n − 1)` or `3n + 2` | 10th = 32 cm; 50th = 152 cm |
| Regular octagon, side 1 m | 8 m | +6 m | `8 + 6(n − 1)` or `6n + 2` | 40 tiles = 242 m |

Why +3 and +6? A new pentagon has 5 sides, but 2 sides hide on the shared edge → add **3**. A new octagon has 8 sides, 2 hide → add **6**.

---

## Guided example (VI-2 front, problems 1–11)

### Square numbers (problems 1–6)

**Figures:** Figure 1 is a **1×1** square (**1** dot). Figure 2 is **2×2** (**4** dots). Figure 3 is **3×3** (**9** dots).

**1. 4th, 5th, and 6th figures:** **16, 25, 36** dots (`4²`, `5²`, `6²`).

**2. Constant difference?** **No.** Consecutive differences are 3, 5, 7, 9, … (odd numbers, growing).

**3. In words:** Figure `n` is an `n` by `n` square of dots.

**4. 10th figure:** `10² = 100` dots.

**5. 40th figure:** `40² = 1600` dots.

**6. nth figure:** `n²`.

### Rectangular numbers (problems 7–9)

**Figures:** Figure 1 is **1×2** (**2** dots). Figure 2 is **2×3** (**6** dots). Figure 3 is **3×4** (**12** dots).

**7. Constant difference?** **No.** Differences are 4, 6, 8, … (even numbers, growing).

**8. Conjecture for the nth figure:** `n` rows and `n + 1` columns → **`n(n + 1)`** dots.

**9. 99th figure:** `99 × 100 = 9900` dots.

### Triangular numbers (problems 10–11)

**Figures:** Figure 1 has **1** dot. Figure 2 has rows 1 + 2 = **3** dots. Figure 3 has 1 + 2 + 3 = **6** dots.

**10. Related to the square pattern at the top:** two triangles (the nth and the previous) make an `n × n` square: `T_n + T_{n−1} = n²`. Equivalently, a triangle is **half** of the `n` by `(n + 1)` rectangle.

**11. Expression:** `n(n + 1) / 2`.

---

## Practice (VI-2 back, solution guide)

**1. Is 72 a square, rectangular, or triangular number?**

| Type | Equation | Check |
|------|----------|-------|
| Square | `n² = 72` | `8² = 64`, `9² = 81` → **no** |
| Rectangular | `n(n + 1) = 72` | `8 × 9 = 72` → **yes** |
| Triangular | `n(n + 1)/2 = 72` → `n(n + 1) = 144` | `11 × 12 = 132`, `12 × 13 = 156` → **no** |

**72 is rectangular only.**

### Pentagon walkway (problems 2–6) — each side 1 cm

Figure 1 is **one** regular pentagon. Each new pentagon shares **one** full side with the previous one.

**2. Perimeters:** Figure 1 = **5 cm**, Figure 2 = **8 cm**, Figure 3 = **11 cm**. Pattern: **add 3 cm** each time.

**3. Figures 4–6:** **14 cm, 17 cm, 20 cm**.

**4. Table and 10th figure**

| Figure Number (n) | Perimeter (cm) | Difference |
|-------------------|----------------|------------|
| 1 | 5 | — |
| 2 | 8 | 3 |
| 3 | 11 | 3 |
| 4 | 14 | 3 |
| 5 | 17 | 3 |
| 6 | 20 | 3 |
| 7 | 23 | 3 |
| 8 | 26 | 3 |
| 9 | 29 | 3 |
| 10 | 32 | 3 |

Keep adding 3 until the 10th figure: **32 cm**.

**5. Expression:** `5 + 3(n − 1)` or `3n + 2`.

**6. 50th figure:** `3(50) + 2 = 152` cm.

### Octagon walkway (problems 7–10) — each side 1 m

Figure 1 is **one** regular octagon. Each new octagon shares **one** full side (a walkway of octagonal blocks).

**7. Perimeters:** Figure 1 = **8 m**, Figure 2 = **14 m**, Figure 3 = **20 m**. Pattern: **add 6 m** each time.

**8. Figures 4–6:** **26 m, 32 m, 38 m**.

**9. Expression:** `8 + 6(n − 1)` or `6n + 2`.

**10. Walkway of 40 octagonal blocks:** `6(40) + 2 = 242` m.

---

## Common slips
- Treating square / rectangular / triangular counts as a **constant difference** (they are not).
- Using `n²` for rectangular numbers (`n(n + 1)` is one extra column).
- Forgetting to hide **2** sides when polygons join, so adding 5 or 8 instead of 3 or 6.
- Mixing **cm** (pentagons) with **m** (octagons).
- Calling 72 a square because it is “close to 64 or 81.”
