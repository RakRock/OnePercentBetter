# Activity 9: Writing Expressions

[KEY]
**nth term = first term + difference × (n − 1)**  
When a pattern grows by the same amount each step, write an **expression** with `n` (the step number) instead of drawing every figure.
[/KEY]

## Quick Review Notes

### Main Idea
You can describe number patterns with **pictures, tables, words, and algebra**. When a pattern grows by the same amount each step, that amount is the **constant difference**. An **expression** lets you find any term in the pattern without drawing every figure.

### Key Vocabulary
- **Expression:** A math phrase with numbers, variables, and operations (not an equation).
- **Variable:** A letter that stands for a number (often `n` for the step number).
- **Constant difference:** The same amount added (or subtracted) each time in a pattern.
- **nth term:** The value at step `n` in a pattern.
- **Evaluate:** Replace the variable with a number and calculate.

### Important Formulas / Rules

**Remember — constant difference pattern:**

`nth term = first term + difference × (n − 1)`

[DIAGRAM:constant_difference]

**Special patterns:**

| Pattern type | nth term |
|--------------|----------|
| Square numbers | `n²` |
| Rectangular numbers | `n(n + 1)` |
| Triangular numbers | `n(n + 1) / 2` |

[DIAGRAM:square_numbers]

[DIAGRAM:rectangular_numbers]

[DIAGRAM:triangular_numbers]

### Visual Explanation

**Constant difference** — the number of tiles goes up by the same amount every figure (see diagram above).

**Square numbers** — arrange tiles in a square: `n` rows and `n` columns → **`n²`** tiles.

**Rectangular numbers** — a rectangle with `n` rows and `(n + 1)` columns → **`n(n + 1)`** tiles.

**Triangular numbers** — stack rows of 1, 2, 3, … up to `n` → **`n(n + 1) / 2`** dots.

**From a table to an expression** — find the first value and how much the table increases each step:

[DIAGRAM:table_to_expression]

### Example 1

**Problem:** A pattern starts with 4 tiles and adds 5 tiles each figure. Write an expression for the number of tiles at figure `n`. How many tiles in figure 6?

[DIAGRAM:example_1]

**Solution:**
- First term = 4, difference = 5  
- Expression: `4 + 5(n − 1)`  
- Figure 6: `4 + 5(6 − 1) = 4 + 25 = 29` tiles  

**Answer:** Expression `4 + 5(n − 1)`; figure 6 has **29** tiles.

### Example 2

**Problem:** Triangular numbers: 1, 3, 6, 10, 15… How many dots in the 8th triangle?

**Solution:**
- Use `n(n + 1) / 2` with `n = 8`  
- `8(8 + 1) / 2 = 8 × 9 / 2 = 36`  

**Answer:** **36** dots.

### Textbook practice (from the PDF)

*Problems below come from SpringBoard Unit 2, Activity 9 (Lesson 9-2 Practice & Activity 9 Practice).*

---

**1. Lesson 9-2 Practice #17 — What is the sixth square number?**

**Solution:**
1. Square numbers follow `n²` (Figure `n` has `n × n` pebbles).  
2. Sixth square number means `n = 6`.  
3. `6² = 36`.  

**Answer:** **36**

---

**2. Lesson 9-2 Practice #18 — Show that 45 is a triangular number**

**Solution:**
1. Triangular numbers: `T(n) = n(n + 1) / 2`.  
2. Set `n(n + 1) / 2 = 45` → `n(n + 1) = 90`.  
3. Try `n = 9`: `9 × 10 = 90` ✓  
4. So Figure 9 in the triangular pattern has 45 pebbles.  

**Answer:** **45 is the 9th triangular number** because `9(10)/2 = 45`.

---

**3. Activity 9 Practice #2 — Perimeter of the nth figure (Item 1 pattern)**

*Item 1: each figure is a row of unit squares along one side; perimeters are 4, 6, 8, …*

**Problem:** Write an expression for the perimeter of the `n`th figure and find the **50th** perimeter.

**Solution:**
1. Table: Figure 1 → 4, Figure 2 → 6, Figure 3 → 8 (constant difference **2**).  
2. `perimeter = 4 + 2(n − 1) = 2n + 2`.  
3. For `n = 50`: `2(50) + 2 = 102`.  
4. Check `n = 1`: `2(2) + 2 = 4` ✓  

**Answer:** **Expression: `2n + 2`; 50th figure perimeter = 102** units

---

**4. Activity 9 Practice #3f — Pebbles in the 51st figure**

*Item 3: pebble pattern with constant difference (from your class work / table).*

**Problem:** Use your expression from Item 3e to find the number of pebbles in the **51st** figure.

**Solution:**
1. If the pattern has first term `a₁` and constant difference `d`, then  
   `pebbles = a₁ + d(n − 1)`.  
2. *Example from a common pebble table:* Figure 1 has 4 pebbles, difference 3 → `4 + 3(n − 1) = 3n + 1`.  
3. `n = 51`: `3(51) + 1 = 154`.  
4. **Use the expression from your own Item 3e** if your first term or difference differs.  

**Answer:** **Substitute `n = 51` into your Item 3e expression** (example above: **154**).

---

**5. Activity 9 Practice #5 — Area of the 35th figure (Item 4)**

*Item 4 unit-square areas: 1, 5, 9, 13, … (difference 4).*

**Problem:** Write an expression for the area of the `n`th figure and find the **35th** area.

**Solution:**
1. Constant difference 4 → `area = 1 + 4(n − 1) = 4n − 3`.  
2. Check: `n = 1` → `1`; `n = 2` → `5` ✓  
3. `n = 35`: `4(35) − 3 = 140 − 3 = 137`.  

**Answer:** **Expression: `4n − 3`; 35th area = 137** square units

---

**6. Lesson 9-2 Practice #16 — Critique Nate’s reasoning about 56**

**Problem:** Nate says 56 is a rectangular number because a **4 by 14** rectangle can be formed. What is his error?

**Solution:**
1. **Rectangular numbers** in this unit are `n(n + 1)` (two **consecutive** integers).  
2. `56 = 7 × 8 = 7(7 + 1)`, so **56 is** a rectangular number — but as the **7th** rectangular number, not from 4×14.  
3. A 4×14 rectangle uses **non-consecutive** factors, which is **not** the pebble “rectangular number” pattern.  

**Answer:** Nate is wrong to use **any** rectangle. Rectangular numbers must be **`n(n + 1)`**; 56 works because **`7 × 8`**, not **`4 × 14`**.

### Common Mistakes
- Treating an **expression** like an **equation** (expressions have no “=”).
- Using `n` instead of **`n − 1`** for the number of jumps from the first term.
- Forgetting to **substitute** the value of `n` when evaluating.
- Mixing up square (`n²`) and rectangular (`n(n+1)`) patterns.

### Mini Summary
- Patterns with a fixed step size → `first + difference(n − 1)`.
- Square: `n²`; rectangular: `n(n+1)`; triangular: `n(n+1)/2`.
- **Evaluate** by plugging in a number for `n`.
- Tables and pictures help you find the first term and the difference.
