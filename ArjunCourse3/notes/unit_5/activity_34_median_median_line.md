# Activity 34: Median-Median Line

[KEY]
The **median-median line** fits bivariate data by splitting points into **three groups** by x, finding the **median point** in each group, and drawing a line through the **first and third** medians (adjusted through the second).  
Use it to **predict** y from x when the pattern is roughly linear.
[/KEY]

## Quick Review Notes

### Main Idea
The median-median method is a resistant way to draw a line of fit without being pulled by outliers as much as a mean-based method might be.

### Steps
1. Order data by x; divide into **three equal groups** (low, middle, high x).
2. Find **median x** and **median y** in each group → points **L**, **M**, **G**.
3. Draw line through **L** and **G**; shift parallel so it passes near **M**.
4. Write **`y = mx + b`** from two points on the line.

### Key Vocabulary
- **Median-median line:** Line of fit using medians of three groups.
- **Extrapolation:** Predicting outside the data range — can be unreliable.

[DIAGRAM:median_median]

[DIAGRAM:three_groups]

### Example 1 — Predict test score

**Problem:** Median-median line for TV hours vs test score. Predict score for 25 hours TV.

**Solution:** Substitute x = 25 into your equation; expect **low** score (around 70s if negative trend).

**Answer:** Use your equation (e.g. **≈ 70–75** if slope negative)

### Textbook practice (from the PDF)

*Activity 34 Practice, Lessons 34-1 and 34-2.*

---

**1. Activity 34 Practice #1–4 — small data set**

**Problem:** x: 4, 2, 1, 8, 3, 5, 9, 13; y: 6, 14, 11, 5, 8, 2, 4, 3.

**Solution:** Scatter plot; divide into 3 groups by x; find medians; equation from line → check fit visually.

**Answer:** Scatter plot + equation from **median-median steps**

---

**3. Activity 34 Practice #8**

**Problem:** Girl 66 inches tall — predict jump distance.

**Solution:** Substitute x = 66 into median-median equation from height/jump data → about **65–67 inches** from typical lines.

**Answer:** **≈ 65–67 in** (from your line)

---

**4. Activity 34 Practice #12 — TV 25 hours**

**Problem:** Predict test score for 25 TV hours/week.

**Solution:** x = 25 on TV vs score line → **lower** score than average.

**Answer:** **≈ 68–72** (depends on your equation)

---

**5. Activity 34 Practice #13 — TV 10 hours**

**Problem:** Predict score for 10 hours TV.

**Solution:** x = 10 → **higher** score than 25-hour case.

**Answer:** **≈ 88–92** (from your line)

---

**6. Activity 34 Practice #14**

**Problem:** Why not predict for 0 or 60 TV hours?

**Solution:** **Outside data range** — extrapolation may be wrong; no data support.

**Answer:** **Extrapolation** — not reliable far outside observed values

### Common Mistakes
- Wrong **grouping** (not by x-order).
- Using **mean** instead of **median** for each group.
- Wrong **y-intercept** after finding correct slope (check Chuck's mistake in Item 15).

### Mini Summary
- Three groups → medians **L, M, G** → line → **`y = mx + b`**.
- Good for **prediction** within the data range.
