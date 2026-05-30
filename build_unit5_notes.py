#!/usr/bin/env python3
"""Writes Unit 5 activity markdown notes. Run: python build_unit5_notes.py"""

from pathlib import Path

NOTES = Path(__file__).parent / "ArjunCourse3" / "notes" / "unit_5"
NOTES.mkdir(parents=True, exist_ok=True)

ACTIVITIES = {
    "activity_32_analyzing_data.md": '''# Activity 32: Analyzing Data

[KEY]
A **scatter plot** shows the relationship between two **numerical** variables.  
Describe **association** by **direction** (positive/negative), **form** (linear/non-linear), and **strength** (strong/moderate/weak).
[/KEY]

## Quick Review Notes

### Main Idea
Bivariate numerical data are pairs (x, y). A scatter plot helps you see whether one variable tends to increase or decrease as the other changes, and whether the pattern is linear.

### Key Vocabulary
- **Bivariate data:** Two variables measured for each subject.
- **Scatter plot:** Graph of (x, y) points.
- **Association:** Relationship between two variables.
- **Positive association:** As x increases, y tends to increase.
- **Negative association:** As x increases, y tends to decrease.
- **Linear association:** Points roughly follow a straight-line pattern.
- **Linear model:** `y = mx + b` approximates the relationship.

### What to describe

| Feature | Questions |
|---------|-----------|
| Direction | Positive, negative, or none? |
| Form | Linear or non-linear? |
| Strength | Strong, moderate, or weak? |

[DIAGRAM:scatter_association]

[DIAGRAM:association_types]

### Example 1 — TV and test score

**Problem:** More hours of TV per week vs lower test scores.

**Solution:** Points trend downward → **negative association**; roughly **linear**, **moderate** strength.

**Answer:** **Negative**, **linear**, **moderate**

### Example 2 — Homework and test score

**Problem:** Higher percent homework completed vs higher test score.

**Solution:** **Positive association** — as homework % increases, test score tends to increase.

**Answer:** **Positive association**

### Textbook practice (from the PDF)

*Activity 32 Practice, Lessons 32-1 and 32-2.*

---

**1. Activity 32 Practice #1**

**Problem:** Scatter plot: Hours of TV (x) vs Percent Homework Completed (y).

**Solution:** Plot each student pair; expect **negative** trend (more TV → less homework done).

**Answer:** **Negative association** (more TV, lower homework %)

---

**2. Activity 32 Practice #2**

**Problem:** Homework % (x) vs Test Score (y).

**Solution:** Higher homework % with higher scores → **positive association**

**Answer:** **Positive association**

---

**3. Activity 32 Practice #3**

**Problem:** TV hours (x) vs Test Score (y).

**Solution:** More TV, lower scores → **negative association**

**Answer:** **Negative association**

---

**4. Activity 32 Practice #5**

**Problem:** Which of Items 1 and 2 has positive association?

**Solution:** Item 2 (homework vs test score) → **Item 2**

**Answer:** **Scatter plot from Item 2** (homework vs test score)

---

**5. Activity 32 Practice #9–10 — helmets**

**Problem:** Price (x) vs Quality Rating (y). Linear? Higher price → higher quality?

**Solution:** Check scatter pattern; if upward trend → **positive**; more expensive helmets **tend** toward higher ratings if linear positive.

**Answer:** Describe from plot: often **positive**, **linear** or **moderate linear**

---

**6. Activity 32 Practice #15a**

**Problem:** Time studying vs test score — relationship?

**Solution:** More study → higher score → **positive association** expected.

**Answer:** **Positive association** (relationship expected)

### Common Mistakes
- Saying **causation** from association only (correlation ≠ cause).
- Confusing **positive** and **negative** direction.
- Calling a curved pattern **linear**.

### Mini Summary
- Scatter plot → describe **direction, form, strength**.
- **Positive:** both increase together; **negative:** one up, other down.
''',

    "activity_33_bivariate_data.md": '''# Activity 33: Bivariate Data

[KEY]
**Bivariate data** list two variables for each subject (e.g., rubber bands and jump length).  
A **trend line** models linear association; use **`y = mx + b`** to **predict**. **MAD** measures average distance from the mean.
[/KEY]

## Quick Review Notes

### Main Idea
Collect pairs of measurements, plot them, fit a trend line by eye or with tools, and interpret slope and intercept in context. Mean absolute deviation (MAD) summarizes spread.

### Key Vocabulary
- **Bivariate data:** Two variables per observation.
- **Trend line:** Line showing general linear pattern in a scatter plot.
- **Mean absolute deviation (MAD):** Average of `|value − mean|`.
- **Prediction:** Substitute x into trend-line equation.

### MAD formula

`MAD = (|x₁ − mean| + |x₂ − mean| + …) / n`

[DIAGRAM:bivariate_scatter]

[DIAGRAM:trend_line]

### Example 1 — Which data sets are bivariate?

**Problem:** Heights of 20 third graders vs prices and sizes of 40 houses.

**Solution:** First is **one variable** only; second is **bivariate** (price and size).

**Answer:** **Data Set 2** is bivariate

### Example 2 — Trend line interpretation

**Problem:** `y = 492 + 15x` where x = age, y = meters walked in 6 minutes.

**Solution:** Slope **15** = meters per year of age; at x = 12: `y = 492 + 180 = 672` meters.

**Answer:** Slope **15 m/year**; at age 12 predict **672 meters**

### Textbook practice (from the PDF)

*Activity 33 Practice, Lessons 33-1 through 33-3.*

---

**1. Activity 33 Practice #1**

**Problem:** Which data sets are bivariate?

**Solution:** Set 1 (heights only) — no; Set 2 (heights & weights) — yes; Set 3 (reading & age) — yes.

**Answer:** **Sets 2 and 3** (and Set 1 from lesson: prices & sizes)

---

**2. Activity 33 Practice #2**

**Problem:** Bear heights and weights — positive or negative?

**Solution:** Taller bears tend to weigh more → **positive**

**Answer:** **Positive association**

---

**3. Activity 33 Practice #3 — frying time**

**Problem:** `y = 12 − 0.2x`, x = frying time (min), y = fat (g). Interpret slope.

**Solution:** Slope **−0.2** = fat decreases by **0.2 g per minute** of frying.

**Answer:** **−0.2 g fat per minute**

---

**4. Activity 33 Practice #8 — two trend lines**

**Problem:** Which line fits age vs cell calls better?

**Solution:** Choose line that passes through **middle** of points with balanced residuals → **Line that matches downward trend**

**Answer:** **The line that follows the negative trend** (fewer calls as age increases)

---

**5. Activity 33 Practice #11 — TV and test scores**

**Problem:** Graph trend line; write equation.

**Solution:** Draw line through scatter of TV vs score; negative slope ≈ −1 or so; example **`y = 100 − x`** (adjust to your line).

**Answer:** Equation from **your** trend line (negative slope expected)

---

**6. Activity 33 Practice #15 — MAD**

**Problem:** MAD for 22, 34, 21, 12, 40, 37, 27, 19, 23, 25.

**Solution:** Mean = 26; deviations: 4, 8, 5, 14, 14, 11, 1, 7, 3, 1 → sum = 68; MAD = **6.8**

**Answer:** **MAD = 6.8**

### Common Mistakes
- Using trend line to predict **far outside** the data range (extrapolation).
- Forgetting **absolute value** in MAD.
- Single-variable data labeled as bivariate.

### Mini Summary
- **Bivariate** = two variables per row.
- **Trend line** for linear patterns; interpret **slope in context**.
''',

    "activity_34_median_median_line.md": '''# Activity 34: Median-Median Line

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
''',

    "activity_35_two_way_tables_association.md": '''# Activity 35: Two-Way Tables and Association

[KEY]
A **two-way table** summarizes two **categorical** variables. Use **row percentages** (or column percentages) and **segmented bar graphs** to compare groups and judge **association**.
[/KEY]

## Quick Review Notes

### Main Idea
When both variables are categories (grade level, sport, gender), counts go in a table. Percentages within rows show how responses differ across groups.

### Key Vocabulary
- **Categorical variable:** Labels or categories (not numbers for measurement).
- **Two-way table:** Rows = one variable, columns = another.
- **Row percentage:** `(cell count / row total) × 100%`
- **Segmented bar graph:** Stacked bars showing 100% per category.
- **Association:** Distribution of one variable **changes** across levels of the other.

### Row percentage

`Row % = (cell / row total) × 100`

[DIAGRAM:two_way_table]

[DIAGRAM:segmented_bar]

### Example 1 — Defensive players and Burger Bungalow

**Problem:** Offense 23 pizza, 21 burger; Defense 35 pizza, 9 burger. % of defensive players prefer Burger Bungalow?

**Solution:** Defense total = 35 + 9 = 44; burger = 9 → `9/44 ≈ 20.5%`

**Answer:** **20.5%** (choice d)

### Example 2 — Seat belts

**Problem:** Males always wear seat belt: 330 of 500.

**Solution:** `330/500 = 66%`

**Answer:** **66%**

### Textbook practice (from the PDF)

*Activity 35 Practice, Lessons 35-1 and 35-2.*

---

**1. Activity 35 Practice #1**

**Problem:** % defensive players prefer Burger Bungalow?

**Solution:** `9/(35+9) = 9/44 ≈ 20.5%`

**Answer:** **20.5%** (d)

---

**2. Activity 35 Practice #2**

**Problem:** % males who always wear seat belts.

**Solution:** `330/500 = 66%`

**Answer:** **66%**

---

**3. Activity 35 Practice #5**

**Problem:** Does seat belt use differ by gender?

**Solution:** Compare row %: males 66% always vs females 325/500 = **65%** — similar; slight differences in sometimes/never.

**Answer:** **Similar** overall; small differences in categories

---

**4. Activity 35 Practice #6**

**Problem:** Association between gender and seat belt use?

**Solution:** If row distributions are **very similar**, weak association; if **different**, association present.

**Answer:** **Weak or no strong association** if percentages nearly match; **association** if row profiles differ clearly

---

**5. Lesson 35-1 #11 — after-school activities**

**Problem:** Row % for 6th grade: 160 participate, 90 do not (total 250).

**Solution:** Participate `160/250 = 64%`; Do not `90/250 = 36%`

**Answer:** **64%** participate, **36%** do not (6th grade)

---

**6. Activity 35 Practice #9 — soccer injuries**

**Problem:** % soccer players injured? % football injured?

**Solution:** Soccer `8/40 = 20%`; Football `12/50 = 24%` (check table totals from practice)

**Answer:** Soccer **20%**; Football **24%** (from given counts)

### Common Mistakes
- Using **table total** instead of **row total** for row percentages.
- Saying association when percentages are **almost the same**.
- Confusing **row** vs **column** percentages.

### Mini Summary
- Two-way table → **row %** → **segmented bar graph** → compare patterns for **association**.
''',
}

COMBINED = '''# Unit 5: Probability & Statistics — Lesson Notes Cheat Sheet

## Scatter plots & association (Activity 32)
- **Bivariate numerical data:** two variables per subject
- Describe: **direction** (+/−), **form** (linear/non-linear), **strength**
- **Positive:** x up → y up; **Negative:** x up → y down

## Bivariate data & trend lines (Activity 33)
- **Trend line:** `y = mx + b` for predictions
- **MAD:** average of |value − mean|
- Slope = change in y per unit x (in context)

## Median-median line (Activity 34)
- Three x-groups → median points L, M, G → line of fit
- Avoid **extrapolation** far outside data

## Two-way tables (Activity 35)
- Two **categorical** variables
- **Row %** = cell / row total
- **Segmented bar graph** compares distributions
- **Association:** row percentages differ meaningfully

## Embedded assessments
- After Activity 33: Scatter plots, associations, trends
- After Activity 35: Median-median line and two-way tables
'''


def main():
    for name, body in ACTIVITIES.items():
        path = NOTES / name
        path.write_text(body.strip() + "\n", encoding="utf-8")
        print(f"wrote {path}")
    combined_path = NOTES / "unit_5_statistics_lesson_notes.md"
    combined_path.write_text(COMBINED.strip() + "\n", encoding="utf-8")
    print(f"wrote {combined_path}")


if __name__ == "__main__":
    main()
