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
A scatterplot turns a two-column table into a picture — each row becomes one dot on a graph. Before you plot, decide which variable goes on the x-axis (the one you think causes or comes first) and which goes on the y-axis (the result you measure). Once the dots are on the graph, look at the overall direction: do they climb up, slide down, or scatter randomly? That direction tells you whether the two variables are related and how.

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

**What is this about:** Turn a table row into the correct scatterplot point — x first, then y.

**Problem:** A table shows touchdown passes for games 1–5:

| Game | 1 | 2 | 3 | 4 | 5 |
|------|---|---|---|---|---|
| Touchdown passes | 3 | 1 | 3 | 2 | 3 |

Which point belongs on the scatterplot?

**How to think about it:** Game number is what you track over time — that is the independent variable (x). Touchdown passes depend on what happened in each game — that is the dependent variable (y). Always write points as (x, y), never (y, x).

**Solution (step by step):**
1. Label axes: **x** = game number, **y** = touchdown passes.
2. For game 5: x = 5, y = 3 → point **(5, 3)**.
3. Double-check other games: game 3 → (3, 1), not (1, 3).

**Answer:** **(5, 3)**

**Why this works:** Scatterplot coordinates always follow (independent, dependent) = (x, y) order.

### Example 2 — Negative correlation (Test Q4)

**What is this about:** Recognize a downward trend on a scatterplot.

**Problem:** A scatterplot shows points falling from upper-left to lower-right. What correlation is shown?

**How to think about it:** Trace the cloud of dots from left to right on the graph. If they move downward as you go right, y decreases when x increases — that is a negative relationship.

**Solution (step by step):**
1. Look left to right across the graph.
2. Notice y-values get smaller as x-values get larger.
3. That pattern is **negative correlation**.

**Answer:** **Negative correlation**

**Why this works:** Negative correlation means the two variables move in opposite directions.

### Example 3 — Positive correlation (Test Q23)

**What is this about:** Recognize an upward trend on a scatterplot.

**Problem:** Points trend upward from left to right on a scatterplot.

**How to think about it:** Imagine drawing a line through the middle of the dots — if it tilts up like a hill, both variables grow together. More x tends to mean more y.

**Solution (step by step):**
1. Scan the dots from left to right.
2. See that higher x-values pair with higher y-values.
3. That upward cloud means **positive correlation**.

**Answer:** **Positive correlation**

**Why this works:** Positive correlation means as one variable increases, the other tends to increase too.

### Example 4 — No correlation (Test Q22)

**What is this about:** Tell when there is no clear relationship between two variables.

**Problem:** Points are scattered with no upward or downward trend.

**How to think about it:** If the dots look like a random splatter with no direction — not climbing, not falling — the variables probably do not affect each other in a predictable way.

**Solution (step by step):**
1. Look for an overall direction in the cloud.
2. No consistent up or down pattern appears.
3. Conclude **no correlation**.

**Answer:** **No correlation in the data set**

**Why this works:** Without a trend, knowing x does not help you predict y.

### Example 5 — Independent vs dependent (Test Q14)

**What is this about:** Choose which variable belongs on each axis.

**Problem:** Which is correct when graphing home runs over several seasons?

**How to think about it:** Ask: "Which variable do I set or measure first?" Season number is the timeline (x). Home runs are what you count as a result (y). The cause-or-first variable goes on the x-axis.

**Solution (step by step):**
1. **Season** comes first in time → independent → **x-axis**.
2. **Home runs** are measured each season → dependent → **y-axis**.
3. Same idea: umbrellas sold depend on rain — rain would be x, umbrellas y.

**Answer:** **Season is the independent variable**

**Why this works:** The independent variable is the input; the dependent variable is the output you observe.

### Example 6 — Mackenzie study hours (Test Q7)

**What is this about:** Describe a real-world positive relationship from a scatterplot.

**Problem:** A scatterplot shows hours studying (x) vs test score (y). What is the relationship?

**How to think about it:** More study hours should mean higher scores — dots should rise left to right. Even if several students share the same study hours (same x, different y), the overall trend can still be positive.

**Solution (step by step):**
1. Trace the cloud left to right — it rises.
2. That means **positive relationship**.
3. More study hours → **higher** test scores on average (not lower).
4. Multiple scores at x = 2 does **not** cancel the trend.

**Answer:** **As study hours increase, test scores increase**

**Why this works:** Correlation describes the overall trend, not every individual dot.

### Exam-style practice

---

**1. Table: hours exercised (x) vs resting heart rate (y). Point for 4 hours, 72 bpm?**

**Problem:** Plot the point for 4 hours of exercise and 72 bpm resting heart rate.

**How to think about it:** Hours exercised is x (what you choose); heart rate is y (what you measure). Write (x, y).

**Solution (step by step):**
1. x = 4 (hours exercised).
2. y = 72 (resting heart rate in bpm).
3. Plot **(4, 72)** — x first, then y.

**Answer:** **(4, 72)**

---

**2. Points form a flat horizontal band. Correlation?**

**Problem:** A scatterplot shows dots in a flat horizontal band. What correlation is this?

**How to think about it:** A horizontal band means y stays about the same no matter what x is — no upward or downward movement.

**Solution (step by step):**
1. Move left to right — y does not consistently rise or fall.
2. The variables do not change together.
3. This is **no correlation**.

**Answer:** **No correlation** (y does not change with x)

---

**3. Which variable goes on the x-axis for "age vs height"? (Test Q14 style)**

**Problem:** For a graph of age vs height, which variable is x?

**How to think about it:** Age is the independent variable — time passes and age grows. Height is measured as a result of growing.

**Solution (step by step):**
1. **Age** is the input / timeline → **x-axis**.
2. **Height** depends on age → **y-axis**.
3. Label axes with names and units.

**Answer:** **Age** on x; **height** on y

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
Once you know the direction of a scatterplot (positive, negative, or none), describe it more fully with three words: direction, form, and strength. Linear means the dots follow a straight-band pattern; nonlinear means they curve. Strong means dots hug the pattern tightly; weak means they spread out. Wyatt's horizontal-line example is important: a perfectly straight horizontal row shows **no** relationship, even though it is a straight line.

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

**What is this about:** A straight line does not always mean two variables are related.

**Problem:** Wyatt says if scatterplot points form a straight line, the variables are related. Which graph proves this is **not always** true?

**How to think about it:** Imagine GPA stays at 3.0 whether you have 1 sibling or 4. The dots form a flat horizontal line — straight, but siblings do not change GPA at all.

**Solution (step by step):**
1. Picture a **horizontal line** of points (same GPA for every sibling count).
2. The line is straight, but GPA does not change when siblings change.
3. That proves **no relationship** — Wyatt's claim is false.

**Answer:** **Horizontal line at GPA = 3** (no relationship)

**Why this works:** A horizontal pattern means y stays constant as x changes — that is the opposite of a relationship.

### Example 2 — Weak linear positive (Practice Q11 & Q14)

**What is this about:** Describe direction, form, and strength together.

**Problem:** A scatterplot shows an upward trend but points are spread out. Choose three: strong/weak, linear/nonlinear, positive/negative.

**How to think about it:** Upward = positive. Roughly straight path = linear. Wide spread around the trend = weak, not strong.

**Solution (step by step):**
1. Upward trend → **positive correlation**.
2. Straight-ish path → **linear** form.
3. Wide spread → **weak association** (not strong).

**Answer:** **Positive, linear, weak**

**Why this works:** Strength measures how tightly dots follow the pattern, not just whether a pattern exists.

### Example 3 — Cluster in a table (Practice Q9)

**What is this about:** Spot a cluster from table values and describe the trend.

**Problem:** A table of (x, y) values has x from 1.6 to 4.8 and y from 38 to 45, all in a tight band. As x increases, y increases.

**How to think about it:** When all values sit in a narrow range, the points group together on the graph — that is a cluster. Rising y with rising x means positive trend.

**Solution (step by step):**
1. Values grouped in a narrow range → **cluster**.
2. y rises as x rises → **positive** trend.
3. Describe both features in your answer.

**Answer:** **There is a cluster, and as x increases, y increases**

**Why this works:** Clusters are separate groupings of points; trend describes the direction within or between groups.

### Example 4 — Cluster scatterplot (Test Q8)

**What is this about:** Identify a cluster visually on a scatterplot.

**Problem:** Which scatterplot displays a **cluster**?

**How to think about it:** A cluster is not just a straight trend — it is a **group** of points bunched together, often with empty space between groups.

**Solution (step by step):**
1. Look for **two separate groups** of points (e.g., lower-left bunch and upper-right bunch).
2. A single straight cloud is a trend, not necessarily a cluster.
3. Pick the graph with **distinct groupings**.

**Answer:** **Graph with two distinct groupings of points**

**Why this works:** Clusters show subgroups in the data, not just overall direction.

### Example 5 — Study hours linear positive (Test Q13)

**What is this about:** Interpret a constant rate of change in a real context.

**Problem:** For every 30 minutes studied, grade increases 8 points. Which statements are true? (Choose three.)

**How to think about it:** More study → better grades = positive. A fixed rate per half hour = linear. But trend lines describe tendencies — not every student will gain exactly 16 points per hour.

**Solution (step by step):**
1. More study → better grades → **positive correlation**.
2. Constant rate → **linear association**.
3. "Every student earns exactly 16 more points per hour" is **too exact** — trends describe **tendencies**, not guarantees.
4. True statement: students who study more **tend to** earn better grades.

**Answer:** **Positive correlation, linear association, students who study more tend to earn better grades**

**Why this works:** Association describes general patterns, not rules that apply to every individual.

### Example 6 — No trend line needed (Test Q12)

**What is this about:** Know when a trend line does not make sense.

**Problem:** Which scatterplot has **no clear relationship** and would **not** have a trend line?

**How to think about it:** If dots are scattered like random stars with no direction, drawing a line would be misleading — there is no pattern to model.

**Solution (step by step):**
1. Look for random scatter with no up or down direction.
2. No pattern → **no relationship**.
3. Do **not** draw a trend line when there is nothing to follow.

**Answer:** **Random scatter with no upward or downward trend**

**Why this works:** Trend lines only help when data show a consistent linear pattern.

### Exam-style practice

---

**1. Points tightly packed along a rising line. Strong or weak?**

**Problem:** Dots are tightly packed along a rising line. Is the association strong or weak?

**How to think about it:** Tight packing means dots stay close to the pattern — that is strong, not weak.

**Solution (step by step):**
1. Rising line → positive direction.
2. Dots hug the line closely → **strong** association.
3. Straight path → linear form.

**Answer:** **Strong** linear positive association

---

**2. Points follow a U-shaped curve. Linear or nonlinear?**

**Problem:** Scatterplot points follow a U-shaped curve. Linear or nonlinear?

**How to think about it:** Linear means a straight-band pattern. A U-shape bends — that is curved, so nonlinear.

**Solution (step by step):**
1. Trace the pattern — it curves like a U.
2. Curved patterns are **nonlinear**.
3. A straight line would not fit well.

**Answer:** **Nonlinear**

---

**3. GPA stays at 4.0 for 1, 2, 3, or 4 siblings. Relationship?**

**Problem:** GPA is 4.0 whether a student has 1, 2, 3, or 4 siblings. Is there a relationship?

**How to think about it:** This is Wyatt's trap — a flat horizontal row. Siblings change but GPA does not.

**Solution (step by step):**
1. Plot the points — they form a horizontal line at GPA = 4.0.
2. y does not change when x changes.
3. **No relationship**.

**Answer:** **No relationship** (horizontal pattern)

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
When scatterplot dots follow a roughly straight path, you can draw a trend line (also called a line of best fit or regression line) through the middle of the cloud. The line will not hit every dot — it shows the overall pattern. Once you have two points on that line, you can find slope and write an equation to make predictions. Always use points **on the trend line**, not necessarily the original data points.

### Key Vocabulary
- **Trend line / regression line:** same idea — best-fit line for linear data
- **Line of best fit:** minimizes distance from points; used for predictions
- **Slope (m):** change in y per 1 unit of x on the trend line
- **Y-intercept (b):** y-value when x = 0 on the trend line

[DIAGRAM:trend_line_slope]

[DIAGRAM:slope_from_graph]

### Example 1 — Slope from trend line (Practice Q10)

**What is this about:** Write the slope formula using two points on the trend line.

**Problem:** A trend line passes through **(4, 35)** and **(16, 134)**. Which expression gives the slope?

**How to think about it:** Slope is always change in y divided by change in x. Use the y-values in the numerator and x-values in the denominator — never flip them.

**Solution (step by step):**
1. Change in y: `134 − 35 = 99`.
2. Change in x: `16 − 4 = 12`.
3. Slope: `m = 99 ÷ 12 = 8.25` → expression **(134 − 35) ÷ (16 − 4)**.

**Answer:** **(134 − 35) ÷ (16 − 4)**

**Why this works:** Rise over run works the same on trend lines as on any line.

### Example 2 — Slope of negative trend line (Test Q5)

**What is this about:** Compute a negative slope from two trend-line points.

**Problem:** Trend line through **(2, 79)** and **(12, 24)**. Find the slope expression.

**How to think about it:** y drops from 79 to 24 as x grows — expect a negative slope. Subtract carefully: `24 − 79 = −55`.

**Solution (step by step):**
1. Change in y: `24 − 79 = −55`.
2. Change in x: `12 − 2 = 10`.
3. Slope: `m = −55 ÷ 10 = −5.5` → **(24 − 79) ÷ (12 − 2)**.

**Answer:** **(24 − 79) ÷ (12 − 2)**

**Why this works:** A downward trend line always has negative slope.

### Example 3 — Plant height equation (Test Q6)

**What is this about:** Build a full equation from two trend-line points in context.

**Problem:** Trend line through **(5, 3)** and **(12, 7)** (days vs height in inches). Write the equation.

**How to think about it:** Find slope first, then plug one point to solve for b. Fractions are okay — the plant grows 4/7 inch per day.

**Solution (step by step):**
1. Slope: `m = (7 − 3) ÷ (12 − 5) = 4/7`.
2. Use (5, 3): `3 = (4/7)(5) + b` → `3 = 20/7 + b`.
3. Solve: `b = 3 − 20/7 = 21/7 − 20/7 = 1/7`.

**Answer:** **y = (4/7)x + 1/7**

**Why this works:** Two points on the line determine both slope and y-intercept.

### Example 4 — Purpose of trend lines (Practice Q6)

**What is this about:** Understand why we use trend lines in real life.

**Problem:** Which statement about trend lines is true?

**How to think about it:** Trend lines summarize a pattern — they estimate what typically happens, not what happens for every single data point.

**Solution (step by step):**
1. Trend lines do **not** pass through every point — they balance above and below.
2. They help you **predict** values for new x-values.
3. Pick the answer about making **real-world predictions**.

**Answer:** **A trend line can be used to make predictions in real-world situations**

**Why this works:** Models are tools for estimation, not exact copies of every data point.

### Example 5 — Choose the correct trend line (Practice Q3)

**What is this about:** Match a trend line's direction to the scatterplot cloud.

**Problem:** Points rise left to right. Which trend line fits?

**How to think about it:** A rising cloud needs a line that tilts **up** — positive slope. The line should cut through the middle, not sit above or below all dots.

**Solution (step by step):**
1. Cloud rises → need **positive slope**.
2. Line should pass **through the center** of the cluster.
3. Reject lines with wrong direction or that miss the middle.

**Answer:** **Positive-slope line through the center of the cluster**

**Why this works:** The best trend line balances points above and below while matching direction.

### Example 6 — Loren's error finding b (Test Q12) ⚠️ Focus

**What is this about:** Avoid swapping x and y when solving for the y-intercept.

**Problem:** Loren finds slope **19/9** through **(1, 130)** and **(10, 149)** but solves `10 = (19/9)(149) + b`. What went wrong?

**How to think about it:** In y = mx + b, y goes on the left and x on the right. Loren put x = 149 (a y-value!) into the x-slot.

**Solution (step by step):**
1. Correct substitution uses a point on the line: (10, 149) means x = 10, y = 149.
2. Loren swapped them: she used 149 as x and 10 as y.
3. Correct setup: **149 = (19/9)(10) + b**.

**Answer:** **She should have solved 149 = (19/9)(10) + b for b**

**Why this works:** Always match x-coordinates with x and y-coordinates with y in the equation.

### Example 7 — Amani checks slope sign (Practice Q1)

**What is this about:** Use the line's direction to check whether slope should be positive or negative.

**Problem:** Amani finds slope on a trend line that tilts **down** left to right. How can she check?

**How to think about it:** Downward tilt means y decreases as x increases — slope must be negative. The y-intercept's sign does not tell you slope's sign.

**Solution (step by step):**
1. Trace the line left to right — it goes down.
2. Downward tilt → **negative slope**.
3. If her calculated slope is positive, she made an error.

**Answer:** **Expect negative slope because the line tilts down left to right**

**Why this works:** Visual direction is a quick check before you trust your arithmetic.

### Example 8 — Trend line terminology (Test Q17)

**What is this about:** Know that different names refer to the same thing.

**Problem:** Which statement about trend lines is true?

**How to think about it:** "Trend line," "line of best fit," and "regression line" all describe the same kind of modeling line in this course.

**Solution (step by step):**
1. Review vocabulary: trend line = regression line.
2. They both model linear patterns in scatterplots.
3. Pick the answer stating they are **equivalent**.

**Answer:** **A regression line and trend line are equivalent terms**

**Why this works:** Different textbooks use different names for the same statistical tool.

### Exam-style practice

---

**1. Trend line through (4, 21) and (8, 35). Slope? (Test Q25)**

**Problem:** Find the slope of a trend line through **(4, 21)** and **(8, 35)**.

**How to think about it:** Subtract y-values for rise, x-values for run, then divide.

**Solution (step by step):**
1. Rise: `35 − 21 = 14`.
2. Run: `8 − 4 = 4`.
3. Slope: `14 ÷ 4 = 3.5`.

**Answer:** **Slope = 3.5** (expression: **(35 − 21) ÷ (8 − 4)**)

---

**2. Negative slope scatterplot — which table? (Test Q16)**

**Problem:** A scatterplot shows a negative trend. Which table matches?

**How to think about it:** Negative slope means y decreases as x increases — scan tables for that pattern.

**Solution (step by step):**
1. Look at each table row by row.
2. Find where x goes up and y goes down consistently.
3. Pick that table.

**Answer:** The table where **y decreases as x increases**

---

**3. Sit-ups scatterplot: 8 points plotted, none overlap. How many table rows? (Practice Q12)**

**Problem:** A scatterplot shows 8 non-overlapping points from a table. How many rows?

**How to think about it:** Each table row gives one point. No overlapping dots means 8 distinct rows.

**Solution (step by step):**
1. One row → one point on the scatterplot.
2. Eight distinct points → eight rows.
3. No overlap confirms one-to-one match.

**Answer:** **8**

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
''',

    "activity_5_two_way_tables.md": '''# Activity 5: Two-Way Tables

[KEY]
A **two-way table** organizes **two categorical variables** (rows vs columns).  
Use **row totals**, **column totals**, and the **grand total** to find missing cells:  
`cell = row total − known cell` or `cell = column total − known cell`.
[/KEY]

## Quick Review Notes

### Main Idea
Two-way tables organize survey or count data by two categories at once — like gender and favorite juice, or grade level and pet type. Each cell shows how many people fit both categories. When a cell is missing, subtract the known cell from its row total or column total. Never guess — the totals must add up perfectly. This skill helps you read real surveys and complete partial tables on exams.

### Key Vocabulary
- **Two-way table:** counts for two categories at once
- **Row variable / column variable:** the two categorical labels
- **Marginal total:** row sum or column sum
- **Grand total:** total number of subjects

[DIAGRAM:two_way_table]

[DIAGRAM:table_variables]

### Example 1 — Proma's favorite juices (Practice Q4)

**What is this about:** Fill in missing cells using row totals.

**Problem:** Partial table:

| | Grapefruit | Orange | Total |
|---|------------|--------|-------|
| Girls | 7 | ? | 16 |
| Boys | 3 | ? | 14 |
| Total | 10 | ? | ? |

Who prefers orange juice?

**How to think about it:** Each row total tells you how many girls (or boys) there are. Subtract the known juice count from the row total to find the other juice count for that row.

**Solution (step by step):**
1. Girls orange: **16 − 7 = 9**.
2. Boys orange: **14 − 3 = 11**.
3. Orange total: 9 + 11 = 20; grand total: 16 + 14 = 30.

**Answer:** **girls: 9; boys: 11**

**Why this works:** Row total = sum of the two cells in that row.

### Example 2 — Esther's pets (Practice Q5)

**What is this about:** Use column totals and row totals to find missing 7th-grade counts.

**Problem:**

| | Cats | Dogs | Total |
|---|------|------|-------|
| 7th Grade | ? | ? | ? |
| 8th Grade | 26 | 35 | 61 |
| Total | 54 | 48 | ? |

7th-grade classmates with pets?

**How to think about it:** Column totals give the full cat and dog counts. Subtract 8th-grade numbers to get 7th-grade numbers.

**Solution (step by step):**
1. 7th cats: **54 − 26 = 28**.
2. 7th dogs: **48 − 35 = 13**.
3. 7th total: 28 + 13 = 41.

**Answer:** **cats: 28; dogs: 13**

**Why this works:** Column total minus one row's cell gives the other row's cell in the same column.

### Example 3 — Study groups (Test Q10)

**What is this about:** Name the two categorical variables in a two-way table.

**Problem:**

| | Group 1 | Group 2 | Total |
|---|---------|---------|-------|
| 3rd Period | 18 | 14 | 32 |
| 4th Period | 15 | 17 | 32 |
| Total | 33 | 31 | 64 |

What are the two variables?

**How to think about it:** Rows and columns each represent one category. Here, rows split by period and columns split by study group.

**Solution (step by step):**
1. Row labels: **3rd Period** vs **4th Period** → variable is **period number**.
2. Column labels: **Group 1** vs **Group 2** → variable is **study group number**.
3. Both are categorical (labels, not measurements).

**Answer:** **period number and study group number**

**Why this works:** Two-way tables always have exactly two categorical variables — one for rows, one for columns.

### Example 4 — Favorite fruits (Test Q15)

**What is this about:** Find a missing cell using a column total.

**Problem:**

| | Apples | Bananas | Total |
|---|--------|---------|-------|
| Class A | 13 | 20 | 33 |
| Class B | ? | 16 | 34 |
| Total | 31 | 37 | ? |

How many in Class B prefer apples?

**How to think about it:** You can subtract along a row OR along a column. Class B total minus bananas = apples, OR apple column total minus Class A apples = Class B apples.

**Solution (step by step):**
1. Column method: **31 − 13 = 18**.
2. Row check: **34 − 16 = 18** ✓

**Answer:** **18**

**Why this works:** Two different subtraction paths should give the same missing cell — use that to check your work.

### Example 5 — Subash's teams (Test Q18)

**What is this about:** Find a missing cell in the girls row.

**Problem:**

| | Team A | Team B | Total |
|---|--------|--------|-------|
| Boys | 15 | 18 | 33 |
| Girls | 17 | ? | 31 |
| Total | 32 | 32 | ? |

How many girls on Team B?

**How to think about it:** Girls total is 31, and 17 are on Team A. The rest must be on Team B.

**Solution (step by step):**
1. Row method: **31 − 17 = 14**.
2. Column check: **32 − 18 = 14** ✓

**Answer:** **14**

**Why this works:** Row total minus known cell equals the missing cell in the same row.

### Example 6 — Grand total check

**What is this about:** Verify your table using the grand total.

**Problem:** Proma's table — what is the grand total?

**How to think about it:** Add all row totals or all column totals — both should match.

**Solution (step by step):**
1. Row totals: **16 + 14 = 30**.
2. Column totals: **10 + 20 = 30**.
3. Both paths agree → grand total is **30**.

**Answer:** **30 friends**

**Why this works:** Grand total is a built-in check — if row and column sums disagree, a cell is wrong.

### Exam-style practice

---

**1. Row total 25, one cell 9. Other cell in row?**

**Problem:** A row totals 25 and one cell is 9. Find the other cell.

**How to think about it:** Row total = cell 1 + cell 2. Subtract to find the missing piece.

**Solution (step by step):**
1. Set up: 9 + ? = 25.
2. Subtract: **25 − 9 = 16**.

**Answer:** **16**

---

**2. Column total 40, known cell 15. Missing cell below?**

**Problem:** A column totals 40 with one cell of 15. Find the other cell (assuming two cells in the column).

**How to think about it:** Same idea as rows, but subtract vertically in the column.

**Solution (step by step):**
1. Set up: 15 + ? = 40.
2. Subtract: **40 − 15 = 25**.

**Answer:** **25**

---

**3. Which is NOT a two-way table variable pair?**

**Problem:** Which pair would NOT work as two variables in a two-way table?

**How to think about it:** Two-way tables need **two categorical** variables (labels like boy/girl, apple/banana). One number + one label does not fit.

**Solution (step by step):**
1. Valid pairs: gender + juice, period + group, class + fruit.
2. Invalid: **height (numerical) + favorite color (categorical)** alone — height is not categorical.
3. Two-way tables count categories, not measurements.

**Answer:** **One numerical + one categorical** alone — two-way tables need **two categorical** variables

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
An outlier is a dot that sits far away from the main cloud of points. Outliers can be real (a genuinely unusual case) or errors (swapped coordinates). Either way, they pull trend lines and change how you describe the data. A low outlier in a "more x → less y" graph makes results look better than typical (understated). A high outlier in a positive trend makes results look better than typical (overstated). Random scatter with no trend means no correlation — do not force a line.

### Key Vocabulary
- **Outlier:** point unusually far from the cloud
- **Overstated:** description makes results look **better/higher** than typical
- **Understated:** description makes results look **lower/weaker** than typical
- **No correlation:** no meaningful pattern between variables
- **Plotting error:** wrong (x, y) order or swapped coordinates

[DIAGRAM:outlier_effect]

[DIAGRAM:no_correlation_scatter]

### Example 1 — Roommates & rent (Practice Q8)

**What is this about:** See how a low outlier affects interpretation of a negative trend.

**Problem:** Rent vs roommates shows lower rent with more roommates, except **(2, 100)** when others at 2 roommates are ~250–350.

**How to think about it:** (2, 100) is way below the other rents at 2 roommates. Including it pulls the trend line down, making typical rent look cheaper than it really is.

**Solution (step by step):**
1. Identify **(2, 100)** as an **outlier** — unusually **low** rent.
2. Including it pulls the trend **downward**.
3. The description makes rent seem **lower/cheaper** than typical → **understated**.

**Answer:** **Including (2, 100) could cause the description to be understated**

**Why this works:** A low outlier in a decreasing trend drags the line down below where most points sit.

### Example 2 — Ticket sales outlier (Test Q24)

**What is this about:** Spot an outlier that makes performance look better than it is.

**Problem:** Hours worked vs tickets sold — positive trend. Which point **overstates** the data?

**How to think about it:** Overstated means the data look better than typical. Find the point far **above** the pattern — it makes sales per hour seem higher than most workers achieve.

**Solution (step by step):**
1. Scan for a point much higher than neighbors at the same x.
2. **(1, 60)** — at only 1 hour, 60 tickets is far above others near 10 at 1 hour.
3. Including it makes sales look **better** than typical → **overstated**.

**Answer:** **(1, 60)**

**Why this works:** A high outlier in a positive trend pulls the line up, exaggerating success.

### Example 3 — Reading vs chores (Test Q19)

**What is this about:** Recognize when there is no correlation at all.

**Problem:** Scatterplot of weekly reading hours vs chore hours — wide random scatter.

**How to think about it:** If dots are scattered like stars with no direction, reading hours do not predict chore hours. Do not draw a trend line.

**Solution (step by step):**
1. Look for an up or down trend — none appears.
2. Points are randomly spread.
3. Conclude: reading hours do **not** affect chore hours.

**Answer:** **In general, reading hours do not affect chore hours**

**Why this works:** No pattern means the variables are unrelated in this data set.

### Example 4 — Victoria's teacher plot (Test Q3) ⚠️ Focus

**What is this about:** Catch a plotting error from swapped coordinates.

**Problem:** Table lists Teacher 3: age **50**, height **60 in.** Plot shows a point at **(60, 50)**.

**How to think about it:** Points must be (x, y) = (age, height). Victoria plotted (height, age) — she swapped the coordinates.

**Solution (step by step):**
1. Correct point: **(50, 60)** — age 50, height 60.
2. Plot shows **(60, 50)** — x and y are reversed.
3. Victoria **mixed up the x- and y-coordinates**.

**Answer:** **She mixed up the x- and y-coordinates of the point for teacher 3**

**Why this works:** Always verify each plotted point against the table: first column = x, second column = y.

### Example 5 — No correlation vs negative (Test Q19 vs Q4)

**What is this about:** Distinguish "no pattern" from "downward pattern."

**Problem:** How is "no correlation" different from "negative correlation"?

**How to think about it:** Negative correlation has a clear downward trend. No correlation is random — knowing x tells you almost nothing about y.

**Solution (step by step):**
1. **Negative:** clear ↘ trend — as x up, y **tends** down.
2. **None:** no direction — knowing x tells you **little** about y.
3. Negative has a pattern; none does not.

**Answer:** **Negative has a trend; none has random scatter**

**Why this works:** Both are different from positive, but only negative shows a consistent direction.

### Example 6 — Should outliers always be removed? (Practice Q8)

**What is this about:** Understand that outliers affect interpretation even if they are real.

**Problem:** Should **(2, 100)** rent always be deleted?

**How to think about it:** The cheap apartment might be real — not necessarily a typo. But including it changes how you describe typical rent.

**Solution (step by step):**
1. The outlier may be a **real** cheap apartment.
2. It still **pulls the trend line down**.
3. Exam focus: how it changes **interpretation**, not automatic deletion.

**Answer:** **It affects interpretation; understates typical rent if included**

**Why this works:** Outliers are not always errors — but they always affect summaries and trend lines.

### Exam-style practice

---

**1. Most points show y ≈ 2x. One point at (5, 50) when others near (5, 10). Effect?**

**Problem:** Most points follow y ≈ 2x, but one point at **(5, 50)** sits far above others near **(5, 10)**. What is the effect?

**How to think about it:** (5, 50) is a high outlier — it pulls the trend line upward at x = 5.

**Solution (step by step):**
1. Identify (5, 50) as far above the pattern.
2. It pulls the line **up** at that x-value.
3. The description **overstates** y → **overstated**.

**Answer:** **Overstates** y at x = 5; outlier pulls line up

---

**2. Table says (3, 8) but plot shows (8, 3). Error?**

**Problem:** The table says **(3, 8)** but the plot shows **(8, 3)**. What went wrong?

**How to think about it:** Compare table coordinates to the plotted point — x and y are reversed.

**Solution (step by step):**
1. Table: x = 3, y = 8 → should plot at (3, 8).
2. Plot shows (8, 3) — coordinates flipped.
3. Error: **swapped x and y**.

**Answer:** **Swapped x and y coordinates**

---

**3. Cloud of points with no direction. Trend line?**

**Problem:** A scatterplot shows a cloud with no direction. Should you draw a trend line?

**How to think about it:** No direction = no relationship. A trend line would mislead the reader.

**Solution (step by step):**
1. Scan for up or down trend — none found.
2. Random scatter → **no clear relationship**.
3. Do **not** draw a trend line.

**Answer:** **No** — no clear relationship (reading/chores style)

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
