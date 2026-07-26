# Activity 4: Interpolation & Extrapolation

[KEY]
**Interpolation:** predict **inside** the x-range of your data — more reliable.  
**Extrapolation:** predict **outside** the x-range — less reliable.  
Substitute x into the trend-line equation **y = mx + b** (or read from the graph).
[/KEY]

## Quick Review Notes

### Main Idea
Find the smallest and largest x-values in the data set. Any prediction between them is interpolation; below or above is extrapolation. Use the trend-line equation when given; otherwise read from the drawn line. Always interpret answers with units in context.

### Key Vocabulary
- **Interpolation:** estimate within the data's x-range
- **Extrapolation:** estimate beyond the data's x-range
- **Trend-line equation:** model for predictions (e.g., y = 1.04x − 7.15)
- **Best estimate:** round reasonably to match answer choices

[DIAGRAM:interpolation_extrapolation]

[DIAGRAM:prediction_from_equation]

### Example 1 — Naomi's apples (Practice Q7)

**Problem:** Apple weights are plotted for about **5 to 15 apples** with a trend through the origin. For which count is weight an **extrapolation**?

**Solution:**
- Data x-range ≈ **5 to 15**
- **18 apples** is **outside** (greater than 15) → extrapolation
- 6, 12, 15 are **inside** the range → interpolation

**Answer:** **18 apples**

### Example 2 — Hot chocolate sales (Test Q20)

**Problem:** Cups sold vs temperature; data from about **42°F to 58°F**. Which temperature gives an **interpolation**?

**Solution:**
- **49°F** lies **inside** 42–58 → interpolation
- 21°F, 35°F, 63°F are **outside** → extrapolation

**Answer:** **49°F**

### Example 3 — Candle height after 1 hour (Test Q21)

**Problem:** Candle height vs hours burned; trend from **(0, 10)** to **(5, 0)**. Best estimate after **1 hour**?

**Solution:**
```
Slope = (0 − 10) ÷ (5 − 0) = −2
y = −2x + 10
At x = 1: y = −2 + 10 = 8 cm
```
1 hour is **inside** 0–5 → interpolation

**Answer:** **8 cm**

### Example 4 — Travel distance (Practice Q13)

**Problem:** Trend line **y = 1.04x − 7.15** (x = minutes, y = miles). How far in **48 minutes**?

**Solution:**
```
y = 1.04(48) − 7.15 = 49.92 − 7.15 = 42.77 ≈ 42 miles
```
48 is between data times 15–60 → interpolation

**Answer:** **42 miles**

### Example 5 — Jill vs Jaxon calories (Test Q11)

**Problem:** **y = 9.56x + 495.35** models daily calories y from weight x (pounds). Jill eats **1850** cal/day; Jaxon weighs **120** lb. Compare.

**Solution:**
- Jaxon: `y = 9.56(120) + 495.35 ≈ 1643` cal
- Jill's weight: `1850 = 9.56x + 495.35` → `x ≈ 141.7` lb
- Jill weighs **about 20 lb more** than Jaxon (141.7 − 120 ≈ 22)

**Answer:** **Jill weighs about 20 pounds more than Jaxon**

### Example 6 — Angelique's cord & beads (Test Q21)

**Problem:** Trend line **y = 2.52x + 1.61** (x = cord inches, y = beads). Estimate beads for **32 inches** when data stop near 26 in.

**Solution:**
```
y = 2.52(32) + 1.61 ≈ 82.25 → about 82 beads
```
32 in. is **beyond** the graphed data → extrapolation

**Answer:** **82 beads (extrapolation)**

### Exam-style practice

---

**1. Data from x = 10 to x = 50. Predict at x = 30.**

**Solution:** **Interpolation** (30 is between 10 and 50).

---

**2. Same data. Predict at x = 60.**

**Solution:** **Extrapolation** (60 > 50).

---

**3. y = −3x + 40. Find y when x = 8.**

**Solution:** **y = −24 + 40 = 16**

### Common Mistakes
- Picking an **interior** x-value for extrapolation (Naomi trap: 15 is **not** extrapolation when data go to 15).
- Forgetting **units** (miles, °F, cm, beads).
- Using a **data point** instead of the **trend line** when the question says "based on the trend line."

### Mini Summary
- **Inside** data x-range → **interpolation**; **outside** → **extrapolation**.
- Plug x into **y = mx + b**; round to match choices.
- Extrapolation is **possible** but **less reliable** than interpolation.
