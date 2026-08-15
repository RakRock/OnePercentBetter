# Activity 4: Interpolation & Extrapolation

[KEY]
**Interpolation:** predict **inside** the x-range of your data — more reliable.  
**Extrapolation:** predict **outside** the x-range — less reliable.  
Substitute x into the trend-line equation **y = mx + b** (or read from the graph).
[/KEY]

## Quick Review Notes

### Main Idea
After you have a trend-line equation, you can predict y for any x-value. The key question is: is that x-value inside the range of your original data or beyond it? Predictions **inside** the data range (interpolation) are more trustworthy because the model was built on nearby values. Predictions **outside** the range (extrapolation) are guesses about unknown territory — possible, but less reliable. Always include units and say whether your prediction is interpolation or extrapolation.

### Key Vocabulary
- **Interpolation:** estimate within the data's x-range
- **Extrapolation:** estimate beyond the data's x-range
- **Trend-line equation:** model for predictions (e.g., y = 1.04x − 7.15)
- **Best estimate:** round reasonably to match answer choices

[DIAGRAM:interpolation_extrapolation]

[DIAGRAM:prediction_from_equation]

### Example 1 — Naomi's apples (Practice Q7)

**What is this about:** Decide whether a prediction is inside or outside the data range.

**Problem:** Apple weights are plotted for about **5 to 15 apples** with a trend through the origin. For which count is weight an **extrapolation**?

**How to think about it:** Find the smallest and largest x-values in the data (about 5 to 15). Any x outside that interval is extrapolation.

**Solution (step by step):**
1. Data x-range ≈ **5 to 15 apples**.
2. Check each choice: 6, 12, 15 are **inside** → interpolation.
3. **18 apples** is greater than 15 → **outside** → extrapolation.

**Answer:** **18 apples**

**Why this works:** Extrapolation means you are stretching the model beyond the data you actually collected.

### Example 2 — Hot chocolate sales (Test Q20)

**What is this about:** Identify interpolation from a temperature context.

**Problem:** Cups sold vs temperature; data from about **42°F to 58°F**. Which temperature gives an **interpolation**?

**How to think about it:** Interpolation means the x-value falls between the lowest and highest data values — here, between 42°F and 58°F.

**Solution (step by step):**
1. Data range: **42°F to 58°F**.
2. **49°F** is between 42 and 58 → **interpolation**.
3. 21°F, 35°F, 63°F are outside → extrapolation.

**Answer:** **49°F**

**Why this works:** 49°F is comfortably inside the range where the model was built.

### Example 3 — Candle height after 1 hour (Test Q21)

**What is this about:** Build an equation from two points and predict within the data range.

**Problem:** Candle height vs hours burned; trend from **(0, 10)** to **(5, 0)**. Best estimate after **1 hour**?

**How to think about it:** Find slope from the two points, write y = mx + b, plug in x = 1. One hour is between 0 and 5, so this is interpolation.

**Solution (step by step):**
1. Slope: `(0 − 10) ÷ (5 − 0) = −2`.
2. Equation: **y = −2x + 10** (starts at 10 cm, burns 2 cm per hour).
3. At x = 1: `y = −2(1) + 10 = 8 cm`.
4. 1 hour is inside 0–5 → **interpolation**.

**Answer:** **8 cm**

**Why this works:** The linear model tracks steady burning between the known endpoints.

### Example 4 — Travel distance (Practice Q13)

**What is this about:** Plug into a given trend-line equation and round reasonably.

**Problem:** Trend line **y = 1.04x − 7.15** (x = minutes, y = miles). How far in **48 minutes**?

**How to think about it:** Substitute x = 48 directly. Round to match answer choices — here, about 42 miles.

**Solution (step by step):**
1. Substitute: `y = 1.04(48) − 7.15`.
2. Compute: `49.92 − 7.15 = 42.77`.
3. Round: **≈ 42 miles**.
4. 48 is between data times 15–60 → interpolation.

**Answer:** **42 miles**

**Why this works:** The equation encodes the average travel rate from the data.

### Example 5 — Jill vs Jaxon calories (Test Q11)

**What is this about:** Use the model forward and backward to compare two people.

**Problem:** **y = 9.56x + 495.35** models daily calories y from weight x (pounds). Jill eats **1850** cal/day; Jaxon weighs **120** lb. Compare.

**How to think about it:** Find Jaxon's predicted calories by plugging in x = 120. Find Jill's weight by setting y = 1850 and solving for x. Then compare.

**Solution (step by step):**
1. Jaxon: `y = 9.56(120) + 495.35 ≈ 1147 + 495 ≈ 1643` cal.
2. Jill: `1850 = 9.56x + 495.35` → `9.56x ≈ 1354.65` → `x ≈ 141.7` lb.
3. Difference: `141.7 − 120 ≈ 21.7` lb → **about 20 lb more**.

**Answer:** **Jill weighs about 20 pounds more than Jaxon**

**Why this works:** The same equation links weight and calories in both directions.

### Example 6 — Angelique's cord & beads (Test Q21)

**What is this about:** Extrapolate beyond the graphed data range.

**Problem:** Trend line **y = 2.52x + 1.61** (x = cord inches, y = beads). Estimate beads for **32 inches** when data stop near 26 in.

**How to think about it:** 32 inches is beyond the data (which stops near 26), so this is extrapolation. Plug in anyway, but know it is less certain.

**Solution (step by step):**
1. Substitute x = 32: `y = 2.52(32) + 1.61`.
2. Compute: `80.64 + 1.61 ≈ 82.25`.
3. Round: **about 82 beads**.
4. 32 in. > 26 in. data max → **extrapolation**.

**Answer:** **82 beads (extrapolation)**

**Why this works:** The model extends the observed pattern, but predictions far outside the data are less reliable.

### Exam-style practice

---

**1. Data from x = 10 to x = 50. Predict at x = 30.**

**Problem:** Data range is x = 10 to x = 50. Is predicting at x = 30 interpolation or extrapolation?

**How to think about it:** 30 is between 10 and 50 — inside the data range.

**Solution (step by step):**
1. Compare 30 to the range 10–50.
2. 10 < 30 < 50 → inside the data.
3. This is **interpolation**.

**Answer:** **Interpolation**

---

**2. Same data. Predict at x = 60.**

**Problem:** Same data (x = 10 to 50). Is x = 60 interpolation or extrapolation?

**How to think about it:** 60 is greater than 50 — beyond the largest data x-value.

**Solution (step by step):**
1. Compare 60 to the range 10–50.
2. 60 > 50 → outside the data.
3. This is **extrapolation**.

**Answer:** **Extrapolation**

---

**3. y = −3x + 40. Find y when x = 8.**

**Problem:** Use **y = −3x + 40** to find y when x = 8.

**How to think about it:** Substitute x = 8 and compute carefully with the negative.

**Solution (step by step):**
1. Substitute: `y = −3(8) + 40`.
2. Compute: `−24 + 40 = 16`.

**Answer:** **y = 16**

### Common Mistakes
- Picking an **interior** x-value for extrapolation (Naomi trap: 15 is **not** extrapolation when data go to 15).
- Forgetting **units** (miles, °F, cm, beads).
- Using a **data point** instead of the **trend line** when the question says "based on the trend line."

### Mini Summary
- **Inside** data x-range → **interpolation**; **outside** → **extrapolation**.
- Plug x into **y = mx + b**; round to match choices.
- Extrapolation is **possible** but **less reliable** than interpolation.
