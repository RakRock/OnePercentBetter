# Activity 15: Solving Systems of Linear Equations Algebraically

[KEY]
**Substitution** — replace one variable with an expression from the other equation, then solve.  
**Elimination** — add or subtract equations so one variable cancels; always write the answer as **(x, y)** and **check both** equations.
[/KEY]

## Quick Review Notes

### Main Idea
A **system** is two linear equations with the **same variables** (usually `x` and `y`). You already know how to solve by **graphing** (Activity 14): the solution is where the lines meet. **Algebraic methods** find that same `(x, y)` without drawing a graph — faster and more exact.

Two main methods:
1. **Substitution** — plug one equation into the other.  
2. **Elimination** — combine equations so one variable disappears.

### Key Vocabulary
- **System of linear equations:** Two (or more) equations using the same variables.
- **Solution of a system:** Ordered pair `(x, y)` that makes **every** equation true.
- **Substitution:** Replace one variable with an expression from another equation.
- **Elimination:** Add or subtract equations to cancel a variable.
- **Equivalent equation:** Same solutions as the original (you can multiply an entire equation by a number).
- **Back-substitute:** Plug a value you found into an equation to get the other variable.

### Important Formulas / Rules

**Remember — when to use which:**

| Method | Good when… |
|--------|------------|
| **Substitution** | One variable is already isolated (`y = …` or `x = …`) |
| **Elimination** | Coefficients of one variable are the **same** or **opposites** |
| **Either** | Word problems — define variables, write two equations, then choose |

**General solving steps (both methods):**
1. Write both equations clearly.  
2. Solve for one variable (or eliminate one variable).  
3. Find the **second** variable.  
4. Write the answer as **`(x, y)`**.  
5. **Check** in **both** original equations.

[DIAGRAM:substitution]

### Substitution — step by step

1. If needed, solve one equation for a variable (e.g. `y = 4x − 3`).  
2. **Substitute** that expression into the **other** equation.  
3. Solve the equation with **one** variable.  
4. **Back-substitute** to find the other variable.  
5. Check `(x, y)` in **both** originals.

### Elimination — step by step

1. Line up like terms (x with x, y with y).  
2. If needed, **multiply** one or both equations so a variable will cancel.  
3. **Add** (opposite coefficients) or **subtract** (same coefficients) the equations.  
4. Solve for the remaining variable.  
5. **Back-substitute** and check.

[DIAGRAM:elimination]

### Visual Explanation

Algebraic methods find the **same intersection point** you would see on a graph. Substitution builds one equation in one variable; elimination cancels a variable by combining equations.

### Example 1 — Substitution (full walkthrough)

**Problem:** Solve the system: `y = 4x − 3` and `2x + y = 13`.

**Solution:**
1. Equation 1 already has `y` isolated: `y = 4x − 3`.  
2. Substitute into equation 2: `2x + (4x − 3) = 13`.  
3. Combine like terms: `6x − 3 = 13`.  
4. Add 3: `6x = 16` → `x = 16/6 = 8/3`.  
5. Back-substitute: `y = 4(8/3) − 3 = 32/3 − 9/3 = 23/3`.  
6. **Check equation 1:** `23/3 = 4(8/3) − 3` ✓  
7. **Check equation 2:** `2(8/3) + 23/3 = 16/3 + 23/3 = 39/3 = 13` ✓  

**Answer:** **`(8/3, 23/3)`** — about **(2.67, 7.67)**

### Example 2 — Substitution (solve for x first)

**Problem:** Solve: `x + y = 7` and `3x − y = 5`.

**Solution:**
1. From equation 1: `x = 7 − y`.  
2. Substitute into equation 2: `3(7 − y) − y = 5`.  
3. `21 − 3y − y = 5` → `21 − 4y = 5` → `−4y = −16` → `y = 4`.  
4. `x = 7 − 4 = 3`.  
5. Check: `3 + 4 = 7` ✓ and `3(3) − 4 = 5` ✓  

**Answer:** **`(3, 4)`**

### Example 3 — Elimination (subtract)

**Problem:** Solve: `3x + 2y = 16` and `3x − y = 4`.

**Solution:**
1. `x` coefficients match (both 3). **Subtract** equation 2 from equation 1:  
   `(3x + 2y) − (3x − y) = 16 − 4`  
2. `3x + 2y − 3x + y = 12` → `3y = 12` → `y = 4`.  
3. Plug into `3x − y = 4`: `3x − 4 = 4` → `3x = 8` → `x = 8/3`.  
4. Check both equations ✓  

**Answer:** **`(8/3, 4)`**

### Example 4 — Elimination (multiply first)

**Problem:** Solve: `2x + 3y = 12` and `4x − 2y = 10`.

**Solution:**
1. Multiply equation 1 by **2** so `x` coefficients match: `4x + 6y = 24`.  
2. Equation 2 stays: `4x − 2y = 10`.  
3. **Subtract** equation 2 from the new equation 1:  
   `(4x + 6y) − (4x − 2y) = 24 − 10` → `8y = 14` → `y = 7/4`.  
4. Use `2x + 3y = 12`: `2x + 3(7/4) = 12` → `2x = 27/4` → `x = 27/8`.  
5. Check in both originals ✓  

**Answer:** **`(27/8, 7/4)`**

**Tip:** Before eliminating, decide whether to cancel **x** or **y** — pick the one that needs fewer multiplies.

### Example 5 — Real world (ticket problem)

**Problem:** Child tickets cost **$8**, adult tickets cost **$12**. You buy **10** tickets for **$100**. How many of each?

[DIAGRAM:tickets_example]

**Solution:**
1. Let `c` = child tickets, `a` = adult tickets.  
2. **Quantity:** `c + a = 10`  
3. **Cost:** `8c + 12a = 100`  
4. From first equation: `c = 10 − a`.  
5. Substitute: `8(10 − a) + 12a = 100`  
6. `80 − 8a + 12a = 100` → `4a = 20` → `a = 5`  
7. `c = 10 − 5 = 5`  
8. Check cost: `5(8) + 5(12) = 40 + 60 = 100` ✓  

**Answer:** **5 child** and **5 adult** tickets.

### Example 6 — Real world (coins)

**Problem:** You have **20** coins worth **$3.20**. All are **dimes** (10¢) or **quarters** (25¢). How many of each?

**Solution:**
1. Let `d` = dimes, `q` = quarters.  
2. `d + q = 20`  
3. `10d + 25q = 320` (cents)  
4. `d = 20 − q`. Substitute: `10(20 − q) + 25q = 320`  
5. `200 + 15q = 320` → `15q = 120` → `q = 8`  
6. `d = 20 − 8 = 12`  
7. Check: `12 + 8 = 20` and `120 + 200 = 320` cents ✓  

**Answer:** **12 dimes** and **8 quarters**

### Setting up systems from words

| Story clue | Equation type |
|------------|----------------|
| Total number of items | `x + y = total` |
| Total cost or value | `(price)x + (price)y = total` |
| Comparison (“twice as many”) | `x = 2y` or similar |
| Two different totals | One equation per situation |

Always **name variables** in a sentence first: “Let `c` = …”

### Textbook practice (from the PDF)

*SpringBoard Unit 2, Activity 15 (Lesson 15-1 Practice, Activity 15 Practice, Lesson 15-2).*

---

**1. Activity 15 Practice #1a — Substitution**

**Problem:** `y = −½x + 5` and `3x − y = 2`.

**Solution:**
1. Substitute `y`: `3x − (−½x + 5) = 2`  
2. `3x + ½x − 5 = 2` → `3.5x = 7` → `x = 2`  
3. `y = −½(2) + 5 = 4`  
4. Check: `3(2) − 4 = 2` ✓  

**Answer:** **`(2, 4)`**

---

**2. Activity 15 Practice #2a — Elimination**

**Problem:** `3x + 4y = 17` and `5x − 4y = 7`.

**Solution:**
1. **Add** equations (y terms cancel): `8x = 24` → `x = 3`  
2. `3(3) + 4y = 17` → `4y = 8` → `y = 2`  
3. Check second: `5(3) − 4(2) = 15 − 8 = 7` ✓  

**Answer:** **`(3, 2)`**

---

**3. Lesson 15-1 Practice #5 — Substitution**

**Problem:** `y = −3x + 2` and `2x − 3y = 22`.

**Solution:**
1. Substitute: `2x − 3(−3x + 2) = 22`  
2. `2x + 9x − 6 = 22` → `11x = 28` → `x = 28/11`  
3. `y = −3(28/11) + 2 = −84/11 + 22/11 = −62/11`  

**Answer:** **`(28/11, −62/11)`**

---

**4. Lesson 15-1 Practice #4 — Elimination**

**Problem:** `3x + 7y = −1` and `4x − 3y = 11`.

**Solution:**
1. Multiply first by 3, second by 7: `9x + 21y = −3` and `28x − 21y = 77`  
2. Add: `37x = 74` → `x = 2`  
3. `3(2) + 7y = −1` → `7y = −7` → `y = −1`  

**Answer:** **`(2, −1)`**

---

**5. Activity 15 Practice #3 Item 3 — `4x − 7y = 10` and `3x + 2y = −7`**

**Solution:**
1. Multiply first by 2, second by 7: `8x − 14y = 20` and `21x + 14y = −49`  
2. Add: `29x = −29` → `x = −1`  
3. `4(−1) − 7y = 10` → `−7y = 14` → `y = −2`  

**Answer:** **`(−1, −2)`**

---

**6. Lesson 15-2 #7 — Adventure Shoe Company**

**Problem:** 20 athletic + 10 hiking = $750; 25 athletic + 20 hiking = $1,200. Find cost per pair.

**Solution:**
1. Let `a` = athletic, `h` = hiking: `20a + 10h = 750`, `25a + 20h = 1200`  
2. Multiply first by 2: `40a + 20h = 1500`  
3. Subtract second: `15a = 300` → `a = 20`  
4. `20(20) + 10h = 750` → `400 + 10h = 750` → `h = 35`  

**Answer:** **$20** per athletic pair, **$35** per hiking pair (choice A)

### Common Mistakes
- Finding only **one** variable and stopping.  
- Sign errors when **subtracting** whole equations (distribute the minus to **every** term).  
- Forgetting to **multiply every term** when you multiply an equation by a number.  
- Not **checking** in **both** original equations.  
- Mixing up which expression to substitute (use the **isolated** variable).  
- Writing the answer as `x = …` only — include **`y`** as **`(x, y)`**.

### Mini Summary
- **Substitution:** plug in → one variable → back-substitute → check both.  
- **Elimination:** align → multiply if needed → add/subtract → solve → check both.  
- Same answer as the **intersection** on a graph (Activity 14).  
- Word problems: **two equations**, two variables, then solve.
