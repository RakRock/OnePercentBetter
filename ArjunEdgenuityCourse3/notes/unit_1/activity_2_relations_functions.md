# Activity 2: Relations & Functions

[KEY]
A **function** is a relation where each **input** (x) has exactly **one output** (y).  
If one x-value appears with **two different y-values**, it is **not** a function.
[/KEY]

## Quick Review Notes

### Main Idea
A **relation** is any collection of input-output pairs — like a list of who is paired with what. A **function** is a special kind of relation where every input gets exactly **one** output, no exceptions. This matters because functions are predictable: if you know the input, you know the output. Machines, formulas, and graphs that are functions won't give you two different answers for the same question.

### Key Vocabulary
- **Relation:** Any set of (input, output) pairs
- **Function:** Each input has exactly one output
- **Vertical line test:** If a vertical line hits a graph more than once, it is not a function
- **Domain:** All input values
- **Range:** All output values

[DIAGRAM:vertical_line_test]

[DIAGRAM:mapping_diagram]

[DIAGRAM:function_equations]

### Example 1 — Table with duplicate inputs (Exam Q2)

**What is this about:** A party venue charges different prices for weekend and weekday packages, and you need to decide if "package number → price" is a function.

**Problem:** Fun Zone party packages: each package number has a **weekend** price and a **weekday** price. Is (package number, price) a function?

**How to think about it:** A function means one input, one output. Package 1 is a single input — but it has **two different prices** depending on the day. That's like asking "What is the price of Package 1?" and getting two different answers.

**Solution (step by step):**
1. Identify the input: **package number**.
2. Check Package 1: it has price **$160** (weekend) **and** **$110** (weekday).
3. Same input (Package 1), two different outputs → **not a function**.

**Answer:** **Not a function** — each package number has two different prices.

**Why this works:** Functions require exactly one output per input; duplicate inputs with different outputs break that rule.

### Example 2 — Remove a point to make a function (Exam Q4)

**What is this about:** You have a set of coordinate points and need to remove one so that each x-value appears only once.

**Problem:** Points include `(−2, 1)` and `(−2, −3)`. Which point should be removed so the set is a function?

**How to think about it:** Both points share x = −2 but have different y-values. To make this a function, you can only keep **one** of them — remove whichever duplicate you don't need.

**Solution (step by step):**
1. Find the repeated x-value: **x = −2** appears twice.
2. The two outputs are y = 1 and y = −3 — that's two outputs for one input.
3. Remove one point, e.g. **(−2, 1)**, so x = −2 has only one y-value left.

**Answer:** Remove **(−2, 1)** (or the other duplicate).

**Why this works:** Once each x appears exactly once, every input maps to a single output — the definition of a function.

### Example 3 — Which equation is a function of x? (Exam Q7)

**What is this about:** You need to pick the equation where each x-value gives exactly one y-value.

**Problem:** Which equation defines **y as a function of x**?

**How to think about it:** "y as a function of x" means: plug in any x, get **one** y. Vertical lines and circles fail this test. Look for equations where y is determined uniquely by x.

**Solution (step by step):**
1. `x = y² + 9` — solving for y gives ±√(x−9), so one x can give **two y values** → not a function of x in the usual form.
2. **`x² = y`** → rewrite as **`y = x²`** — each x gives exactly **one** y ✓
3. `x = 5` — this is a vertical line; x is always 5 regardless of y → not a function of x.
4. `x² = y² + 16` — one x can pair with two y values → not a function.

**Answer:** **`x² = y`** (equivalently `y = x²`)

**Why this works:** `y = x²` passes the vertical line test — every vertical line crosses the parabola at most once.

### Exam-style practice

---

**1. Which table is a function?**

| x | y |
|---|---|
| −3 | −1 |
| −2 | 5 |
| 4 | 0 |
| 7 | −1 |

**Problem:** Is this table a function?

**How to think about it:** Scan the x-column. If any x-value repeats with a **different** y, it's not a function. Repeating y-values with different x-values is fine.

**Solution (step by step):**
1. List all x-values: −3, −2, 4, 7.
2. Each x appears **exactly once**.
3. Every input has one output → **function**.

**Answer:** **Yes, it is a function.**

---

**2. Trap: pattern vs function**

A table shows weekend prices are always $50 more than weekday prices. Does that make it a function?

**Problem:** Does a consistent price pattern make the relation a function?

**How to think about it:** A nice pattern doesn't fix duplicate inputs. If Package 1 still has two prices ($160 and $110), the same input still has two outputs — no matter how regular the pattern looks.

**Solution (step by step):**
1. Check inputs, not patterns: does any package number appear twice?
2. Yes — each package has both a weekend and weekday price.
3. Same input, two outputs → **not a function**, even with a consistent $50 difference.

**Answer:** **No.** A consistent pattern does not fix duplicate inputs. Each package still has two prices.

### Common Mistakes
- **Confusing pattern with function:** A rule like "weekend is always $50 more" sounds organized, but if one input (package number) has two outputs (two prices), it's still **not** a function.
- **Thinking "every input has an output" is enough:** Having a price for every package is not the same as having **one** price per package.
- **Mixing up x and y in equations:** "y as a function of x" means y depends on x — vertical lines like `x = 5` fail because x doesn't determine a unique y.

### Mini Summary
- **One x → one y** = function. Same x with different y values = **not** a function.
- Use the **vertical line test** on graphs: if a vertical line hits twice, it's not a function.
- Parents/teachers: ask "If I give you this input, is there only one possible answer?" — that's the function test in plain language.
