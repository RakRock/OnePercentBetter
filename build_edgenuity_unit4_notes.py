#!/usr/bin/env python3
"""One-time builder: writes Edgenuity Unit 4 activity markdown notes. Run: python build_edgenuity_unit4_notes.py"""

from pathlib import Path

NOTES = Path(__file__).parent / "ArjunEdgenuityCourse3" / "notes" / "unit_4"
NOTES.mkdir(parents=True, exist_ok=True)

ACTIVITIES = {
    "activity_1_scatterplots_correlation.md": '''# Activity 1: Scatterplots & Correlation

[KEY]
A **scatterplot** graphs bivariate data as points **(x, y)**.  
**Independent variable (x):** the input you choose or control. **Dependent variable (y):** the output that may depend on x.  
**Correlation:** **positive** (both increase), **negative** (one up, other down), or **none** (no clear pattern).
[/KEY]

## Quick Review Notes

### Main Idea
Each row of a two-column table becomes one point: first column → x, second column → y. Before plotting, decide which variable is independent (x-axis) and which is dependent (y-axis). Then describe the overall direction of the cloud of points.

### Key Vocabulary
- **Bivariate data:** two variables measured for each subject
- **Scatterplot:** graph of ordered pairs (x, y)
- **Independent variable:** x; often time, age, or the cause you study
- **Dependent variable:** y; often the result you measure
- **Positive correlation:** as x increases, y tends to increase
- **Negative correlation:** as x increases, y tends to decrease
- **No correlation:** points scattered with no direction

[DIAGRAM:scatterplot_basics]

[DIAGRAM:correlation_types]

### Example 1 — QB touchdown passes (Test Q25)

**Problem:** A table shows touchdown passes for games 1–5:

| Game | 1 | 2 | 3 | 4 | 5 |
|------|---|---|---|---|---|
| Touchdown passes | 3 | 1 | 3 | 2 | 3 |

Which point belongs on the scatterplot?

**Solution:**
- **x** = game number (independent), **y** = touchdown passes (dependent)
- Game 5 → **(5, 3)**
- Check others: game 3 → (3, 1), not (3, 1) reversed

**Answer:** **(5, 3)**

### Example 2 — Negative correlation (Test Q4)

**Problem:** A scatterplot shows points falling from upper-left to lower-right. What correlation is shown?

**Solution:**
- As x increases, y decreases → **negative correlation**

**Answer:** **Negative correlation**

### Example 3 — Positive correlation (Test Q23)

**Problem:** Points trend upward from left to right on a scatterplot.

**Solution:**
- Both variables increase together → **positive correlation**

**Answer:** **Positive correlation**

### Example 4 — No correlation (Test Q22)

**Problem:** Points are scattered with no upward or downward trend.

**Solution:**
- No consistent direction → **no correlation**

**Answer:** **No correlation in the data set**

### Example 5 — Independent vs dependent (Test Q14)

**Problem:** Which is correct when graphing home runs over several seasons?

**Solution:**
- **Season** is the independent variable (x)
- **Home runs** is the dependent variable (y)
- Umbrellas sold depend on rain → umbrellas are **dependent**, not independent

**Answer:** **Season is the independent variable**

### Example 6 — Mackenzie study hours (Test Q7)

**Problem:** A scatterplot shows hours studying (x) vs test score (y). What is the relationship?

**Solution:**
- Points rise left to right → **positive relationship**
- More study hours → **higher** test scores (not lower)
- Multiple scores at x = 2 does **not** mean no relationship

**Answer:** **As study hours increase, test scores increase**

### Exam-style practice

---

**1. Table: hours exercised (x) vs resting heart rate (y). Point for 4 hours, 72 bpm?**

**Solution:** **(4, 72)** — x first, then y.

---

**2. Points form a flat horizontal band. Correlation?**

**Solution:** **No correlation** (y does not change with x).

---

**3. Which variable goes on the x-axis for "age vs height"? (Test Q14 style)**

**Solution:** **Age** (independent) on x; **height** (dependent) on y.

### Common Mistakes
- Swapping **x and y** when plotting from a table — always **(x, y)** order.
- Calling any straight line a "relationship" — a **horizontal** line means **no** correlation (see Wyatt, Activity 2).
- Confusing **positive** and **negative** — trace the cloud left to right.

### Mini Summary
- Table row → point **(x, y)**; label axes with variable names and units.
- **Positive:** ↗ trend; **Negative:** ↘ trend; **None:** scattered blob.
- **Independent = x**, **dependent = y**.
''',

    "activity_2_association_strength.md": '''# Activity 2: Association Strength & Form

[KEY]
Describe association by **direction** (positive/negative/none), **form** (linear vs nonlinear), and **strength** (strong vs weak).  
A **cluster** is a group of points close together. A **horizontal** trend means **no relationship** — even though points form a line.
[/KEY]

## Quick Review Notes

### Main Idea
Strength tells how tightly points hug a pattern. Weak association: points follow a direction but spread out. Strong association: points stay close to a line or curve. Linear means a straight-line pattern; nonlinear means curved. Wyatt's horizontal scatterplot proves that "straight line" does not always mean two variables are related.

### Key Vocabulary
- **Linear association:** points roughly follow a straight line
- **Nonlinear association:** curved pattern (parabola, exponential, etc.)
- **Strong association:** points close to the pattern
- **Weak association:** points spread out but still show direction
- **Cluster:** a group of nearby points separated from others
- **No relationship:** horizontal cloud or random scatter

[DIAGRAM:strong_vs_weak]

[DIAGRAM:linear_vs_nonlinear]

### Example 1 — Wyatt's siblings vs GPA (Practice Q2) ⚠️ Focus

**Problem:** Wyatt says if scatterplot points form a straight line, the variables are related. Which graph proves this is **not always** true?

**Solution:**
- A **horizontal line** of points (same GPA for every sibling count) is straight but shows **no relationship**
- Siblings change; GPA stays at 3 → GPA does **not** depend on siblings

**Answer:** **Horizontal line at GPA = 3** (no relationship)

### Example 2 — Weak linear positive (Practice Q11 & Q14)

**Problem:** A scatterplot shows an upward trend but points are spread out. Choose three: strong/weak, linear/nonlinear, positive/negative.

**Solution:**
- Upward trend → **positive correlation**
- Straight-ish path → **linear**
- Wide spread → **weak association** (not strong)

**Answer:** **Positive, linear, weak**

### Example 3 — Cluster in a table (Practice Q9)

**Problem:** A table of (x, y) values has x from 1.6 to 4.8 and y from 38 to 45, all in a tight band. As x increases, y increases.

**Solution:**
- Values grouped in a range → **cluster**
- y rises with x → **positive** trend

**Answer:** **There is a cluster, and as x increases, y increases**

### Example 4 — Cluster scatterplot (Test Q8)

**Problem:** Which scatterplot displays a **cluster**?

**Solution:**
- Look for **two separate groups** of points (e.g., lower-left cluster and upper-right cluster)
- Not the same as a single straight-line trend

**Answer:** **Graph with two distinct groupings of points**

### Example 5 — Study hours linear positive (Test Q13)

**Problem:** For every 30 minutes studied, grade increases 8 points. Which statements are true? (Choose three.)

**Solution:**
- More study → better grades → **positive correlation**
- Constant rate → **linear association**
- "Every student earns exactly 16 more points per hour" is **too exact** — trend lines describe **tendencies**, not guarantees

**Answer:** **Positive correlation, linear association, students who study more tend to earn better grades**

### Example 6 — No trend line needed (Test Q12)

**Problem:** Which scatterplot has **no clear relationship** and would **not** have a trend line?

**Solution:**
- Points scattered randomly with no direction → **no relationship**
- Do not draw a trend line when there is no pattern

**Answer:** **Random scatter with no upward or downward trend**

### Exam-style practice

---

**1. Points tightly packed along a rising line. Strong or weak?**

**Solution:** **Strong** linear positive association.

---

**2. Points follow a U-shaped curve. Linear or nonlinear?**

**Solution:** **Nonlinear**.

---

**3. GPA stays at 4.0 for 1, 2, 3, or 4 siblings. Relationship?**

**Solution:** **No relationship** (horizontal pattern).

### Common Mistakes
- Picking **strong** when points are widely spread (Practice Q11 trap).
- Thinking a **horizontal line** proves a relationship — it proves Wyatt's claim is **false**.
- Saying **nonlinear** when points clearly follow a straight band.

### Mini Summary
- Describe: **direction + form + strength**.
- **Horizontal line = no relationship**, even if it's straight.
- **Cluster** = grouped points; **weak** = spread out, **strong** = tight.
''',

    "activity_3_trend_lines_slope.md": '''# Activity 3: Trend Lines & Slope

[KEY]
A **trend line** (line of best fit) models a **linear** pattern; it does **not** pass through every point.  
**Slope** from two points on the line: `m = (y₂ − y₁) ÷ (x₂ − x₁)`.  
Use the line to write **y = mx + b** and to make predictions.
[/KEY]

## Quick Review Notes

### Main Idea
Draw or choose a trend line that balances points above and below. Read or compute slope from two clear points on the **line** (not necessarily data points). Trend lines and regression lines mean the same thing. The slope tells the rate of change; the y-intercept is the starting value when x = 0.

### Key Vocabulary
- **Trend line / regression line:** same idea — best-fit line for linear data
- **Line of best fit:** minimizes distance from points; used for predictions
- **Slope (m):** change in y per 1 unit of x on the trend line
- **Y-intercept (b):** y-value when x = 0 on the trend line

[DIAGRAM:trend_line_slope]

[DIAGRAM:slope_from_graph]

### Example 1 — Slope from trend line (Practice Q10)

**Problem:** A trend line passes through **(4, 35)** and **(16, 134)**. Which expression gives the slope?

**Solution:**
```
m = (134 − 35) ÷ (16 − 4) = 99 ÷ 12 = 8.25
```

**Answer:** **(134 − 35) ÷ (16 − 4)**

### Example 2 — Slope of negative trend line (Test Q5)

**Problem:** Trend line through **(2, 79)** and **(12, 24)**. Find the slope expression.

**Solution:**
```
m = (24 − 79) ÷ (12 − 2) = −55 ÷ 10 = −5.5
```

**Answer:** **(24 − 79) ÷ (12 − 2)**

### Example 3 — Plant height equation (Test Q6)

**Problem:** Trend line through **(5, 3)** and **(12, 7)** (days vs height in inches). Write the equation.

**Solution:**
```
m = (7 − 3) ÷ (12 − 5) = 4/7
3 = (4/7)(5) + b → b = 3 − 20/7 = 1/7
```

**Answer:** **y = (4/7)x + 1/7**

### Example 4 — Purpose of trend lines (Practice Q6)

**Problem:** Which statement about trend lines is true?

**Solution:**
- Trend lines **estimate** patterns — they do not hit every point
- They are used to **make predictions** in real situations

**Answer:** **A trend line can be used to make predictions in real-world situations**

### Example 5 — Choose the correct trend line (Practice Q3)

**Problem:** Points rise left to right. Which trend line fits?

**Solution:**
- Match **positive slope** — line tilts **up** left to right
- Line should pass **through the middle** of the cloud, not above/below all points

**Answer:** **Positive-slope line through the center of the cluster**

### Example 6 — Loren's error finding b (Test Q12) ⚠️ Focus

**Problem:** Loren finds slope **19/9** through **(1, 130)** and **(10, 149)** but solves `10 = (19/9)(149) + b`. What went wrong?

**Solution:**
- She swapped **x and y** when substituting
- Correct: **149 = (19/9)(10) + b**

**Answer:** **She should have solved 149 = (19/9)(10) + b for b**

### Example 7 — Amani checks slope sign (Practice Q1)

**Problem:** Amani finds slope on a trend line that tilts **down** left to right. How can she check?

**Solution:**
- Downward tilt → **negative slope**
- y-intercept sign does **not** determine slope sign

**Answer:** **Expect negative slope because the line tilts down left to right**

### Example 8 — Trend line terminology (Test Q17)

**Problem:** Which statement about trend lines is true?

**Solution:**
- **Regression line** and **trend line** are **equivalent** terms

**Answer:** **A regression line and trend line are equivalent terms**

### Exam-style practice

---

**1. Trend line through (4, 21) and (8, 35). Slope? (Test Q25)**

**Solution:** **(35 − 21) ÷ (8 − 4) = 14/4 = 3.5**

---

**2. Negative slope scatterplot — which table? (Test Q16)**

**Solution:** Pick table where **y decreases as x increases**.

---

**3. Sit-ups scatterplot: 8 points plotted, none overlap. How many table rows? (Practice Q12)**

**Solution:** **8** — one row per point.

### Common Mistakes
- Using **(x₂ − x₁) ÷ (y₂ − y₁)** — slope is **Δy ÷ Δx**.
- Substituting **x into y's place** when solving for b (Loren trap).
- Picking a trend line with the **wrong direction** (negative line for positive data).

### Mini Summary
- Slope from two points on the **line:** **(y₂ − y₁) ÷ (x₂ − x₁)**.
- **Plant height:** m = 4/7, b = 1/7 → **y = (4/7)x + 1/7**.
- Trend lines **predict**; they are **not** exact data values.
''',

    "activity_4_predictions.md": '''# Activity 4: Interpolation & Extrapolation

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
''',

    "activity_5_two_way_tables.md": '''# Activity 5: Two-Way Tables

[KEY]
A **two-way table** organizes **two categorical variables** (rows vs columns).  
Use **row totals**, **column totals**, and the **grand total** to find missing cells:  
`cell = row total − known cell` or `cell = column total − known cell`.
[/KEY]

## Quick Review Notes

### Main Idea
Two-way tables count how many subjects fall into each combination (e.g., girls who prefer orange juice). Marginal totals appear in the right column and bottom row. The grand total is all subjects. Missing values come from subtraction — never guess.

### Key Vocabulary
- **Two-way table:** counts for two categories at once
- **Row variable / column variable:** the two categorical labels
- **Marginal total:** row sum or column sum
- **Grand total:** total number of subjects

[DIAGRAM:two_way_table]

[DIAGRAM:table_variables]

### Example 1 — Proma's favorite juices (Practice Q4)

**Problem:** Partial table:

| | Grapefruit | Orange | Total |
|---|------------|--------|-------|
| Girls | 7 | ? | 16 |
| Boys | 3 | ? | 14 |
| Total | 10 | ? | ? |

Who prefers orange juice?

**Solution:**
- Girls orange: **16 − 7 = 9**
- Boys orange: **14 − 3 = 11**

**Answer:** **girls: 9; boys: 11**

### Example 2 — Esther's pets (Practice Q5)

**Problem:**

| | Cats | Dogs | Total |
|---|------|------|-------|
| 7th Grade | ? | ? | ? |
| 8th Grade | 26 | 35 | 61 |
| Total | 54 | 48 | ? |

7th-grade classmates with pets?

**Solution:**
- 7th cats: **54 − 26 = 28**
- 7th dogs: **48 − 35 = 13**

**Answer:** **cats: 28; dogs: 13**

### Example 3 — Study groups (Test Q10)

**Problem:**

| | Group 1 | Group 2 | Total |
|---|---------|---------|-------|
| 3rd Period | 18 | 14 | 32 |
| 4th Period | 15 | 17 | 32 |
| Total | 33 | 31 | 64 |

What are the two variables?

**Solution:**
- One variable: **period number** (3rd vs 4th)
- Other variable: **study group number** (1 vs 2)

**Answer:** **period number and study group number**

### Example 4 — Favorite fruits (Test Q15)

**Problem:**

| | Apples | Bananas | Total |
|---|--------|---------|-------|
| Class A | 13 | 20 | 33 |
| Class B | ? | 16 | 34 |
| Total | 31 | 37 | ? |

How many in Class B prefer apples?

**Solution:**
- Class B apples: **31 − 13 = 18** (or **34 − 16 = 18**)

**Answer:** **18**

### Example 5 — Subash's teams (Test Q18)

**Problem:**

| | Team A | Team B | Total |
|---|--------|--------|-------|
| Boys | 15 | 18 | 33 |
| Girls | 17 | ? | 31 |
| Total | 32 | 32 | ? |

How many girls on Team B?

**Solution:**
- Girls Team B: **31 − 17 = 14** (or **32 − 18 = 14**)

**Answer:** **14**

### Example 6 — Grand total check

**Problem:** Proma's table — what is the grand total?

**Solution:**
```
Girls + Boys = 16 + 14 = 30
Grapefruit + Orange = 10 + 20 = 30
```

**Answer:** **30 friends**

### Exam-style practice

---

**1. Row total 25, one cell 9. Other cell in row?**

**Solution:** **25 − 9 = 16**

---

**2. Column total 40, known cell 15. Missing cell below?**

**Solution:** **40 − 15 = 25** (if only one other cell in column).

---

**3. Which is NOT a two-way table variable pair?**

**Solution:** **One numerical + one categorical** alone — two-way tables need **two categorical** variables.

### Common Mistakes
- Adding wrong direction — use **row total − known cell** for the partner in the same row.
- Swapping **girls/boys** counts between juice types (Proma trap).
- Confusing **Team A total** with **girls total**.

### Mini Summary
- Missing cell = **total − known part** (same row or same column).
- Name both **categorical variables** when asked.
- Grand total should match from **any** full row or column sum.
''',

    "activity_6_outliers_interpretation.md": '''# Activity 6: Outliers & Interpretation

[KEY]
An **outlier** is a point far from the overall pattern.  
Including an outlier can **overstate** or **understate** the relationship.  
**No correlation:** points scattered with no trend (reading vs chores).  
**Plotting errors:** swapped coordinates **(x, y)** — check each point against the table.
[/KEY]

## Quick Review Notes

### Main Idea
Outliers pull trend lines and summaries toward them. A low outlier in a negative trend can make the relationship look **stronger/more negative** than it is (understate typical values). A high outlier in a positive trend can **overstate** performance. Random scatter means no correlation — do not force a trend line.

### Key Vocabulary
- **Outlier:** point unusually far from the cloud
- **Overstated:** description makes results look **better/higher** than typical
- **Understated:** description makes results look **lower/weaker** than typical
- **No correlation:** no meaningful pattern between variables
- **Plotting error:** wrong (x, y) order or swapped coordinates

[DIAGRAM:outlier_effect]

[DIAGRAM:no_correlation_scatter]

### Example 1 — Roommates & rent (Practice Q8)

**Problem:** Rent vs roommates shows lower rent with more roommates, except **(2, 100)** when others at 2 roommates are ~250–350.

**Solution:**
- **(2, 100)** is an **outlier** — unusually **low** rent
- Including it pulls the trend **down**, making typical rent look **cheaper** than it is → **understated**

**Answer:** **Including (2, 100) could cause the description to be understated**

### Example 2 — Ticket sales outlier (Test Q24)

**Problem:** Hours worked vs tickets sold — positive trend. Which point **overstates** the data?

**Solution:**
- **(1, 60)** — at only 1 hour, 60 tickets is far **above** the pattern (others near 10 at 1 hour)
- Makes sales-per-hour look **better** than typical → **overstated**

**Answer:** **(1, 60)**

### Example 3 — Reading vs chores (Test Q19)

**Problem:** Scatterplot of weekly reading hours vs chore hours — wide random scatter.

**Solution:**
- No upward or downward pattern
- Reading hours do **not** predict chore hours

**Answer:** **In general, reading hours do not affect chore hours**

### Example 4 — Victoria's teacher plot (Test Q3) ⚠️ Focus

**Problem:** Table lists Teacher 3: age **50**, height **60 in.** Plot shows a point at **(60, 50)**.

**Solution:**
- Coordinates were **swapped** — should be **(50, 60)**
- Age belongs on x, height on y (height depends on age in her study)

**Answer:** **She mixed up the x- and y-coordinates of the point for teacher 3**

### Example 5 — No correlation vs negative (Test Q19 vs Q4)

**Problem:** How is "no correlation" different from "negative correlation"?

**Solution:**
- **Negative:** clear ↘ trend — as x up, y **tends** down
- **None:** no direction — knowing x tells you **little** about y

**Answer:** **Negative has a trend; none has random scatter**

### Example 6 — Should outliers always be removed? (Practice Q8)

**Problem:** Should **(2, 100)** rent always be deleted?

**Solution:**
- It may be a **real** cheap apartment — not necessarily an error
- But recognize it **affects** the trend and summary
- Exam focus: how it changes **interpretation**, not automatic deletion

**Answer:** **It affects interpretation; understates typical rent if included**

### Exam-style practice

---

**1. Most points show y ≈ 2x. One point at (5, 50) when others near (5, 10). Effect?**

**Solution:** **Overstates** y at x = 5; outlier pulls line up.

---

**2. Table says (3, 8) but plot shows (8, 3). Error?**

**Solution:** **Swapped x and y coordinates**.

---

**3. Cloud of points with no direction. Trend line?**

**Solution:** **No** — no clear relationship (reading/chores style).

### Common Mistakes
- Confusing **understated** vs **overstated** — low outlier in a "more roommates → less rent" graph **understates** rent.
- Thinking **multiple y-values at one x** means no relationship (Mackenzie Q7 trap — still can be positive).
- Plotting **(y, x)** instead of **(x, y)** (Victoria trap).

### Mini Summary
- **Outlier** → check if interpretation is **overstated** or **understated**.
- **No correlation** → random scatter; **no trend line**.
- Verify every point: **x from first column, y from second**.
''',

    "unit_4_bivariate_data_lesson_notes.md": '''# Unit 4: Patterns in Bivariate Data — Overview

| Activity | Topic | Key idea |
|----------|-------|----------|
| **1** | Scatterplots & Correlation | Plot (x, y); positive/negative/none; QB TDs Q25, Mackenzie Q7 |
| **2** | Association Strength | Linear/nonlinear, strong/weak, clusters; Wyatt horizontal Q2 |
| **3** | Trend Lines & Slope | Slope from two points; plant height Q6; Loren error Q12 |
| **4** | Predictions | Interpolation vs extrapolation; Naomi Q7, hot chocolate Q20, travel Q13 |
| **5** | Two-Way Tables | Complete tables; Proma, Esther, study groups, fruits, Subash |
| **6** | Outliers & Interpretation | Rent Q8, tickets Q24, reading/chores Q19, Victoria Q3 |

**Exam focus areas (39-page exam — 14 practice + 25 test questions):** Table to scatterplot point (Test Q25), correlation direction (Q4, Q23, Q22), Wyatt horizontal line (Practice Q2), weak vs strong linear (Practice Q11, Q14), trend-line slope (Practice Q10, Test Q5, Q25), plant equation (Test Q6), interpolation/extrapolation (Practice Q7, Test Q20, Q21), two-way tables (Practice Q4–5, Test Q10, Q15, Q18), outliers (Practice Q8, Test Q24), no correlation (Test Q19, Q12), plotting errors (Test Q3).

**Weak areas to review:** Weak vs strong association (Practice Q11), understated vs overstated outliers (Practice Q8), swapped coordinates (Victoria Q3, Loren Q12), extrapolation vs interpolation (Naomi Q7), two-way table subtraction (Proma/Esther).

Open each activity for full notes, diagrams, and worked exam-style problems. Use **Daily Practice** for quiz sets with scatterplots and tables.
''',
}


def main() -> list[Path]:
    created: list[Path] = []
    for filename, content in ACTIVITIES.items():
        path = NOTES / filename
        path.write_text(content.strip() + "\n", encoding="utf-8")
        created.append(path)
        print(f"  wrote {path.name}")
    print("Done.")
    return created


if __name__ == "__main__":
    main()
