"""Edgenuity Course 3 Unit 4 — Patterns in Bivariate Data practice bank."""

from __future__ import annotations

UNIT4_CATEGORIES = {
    "scatter_correlation": {
        "name": "Scatterplots & Correlation",
        "emoji": "📈",
        "color": "#3b82f6",
        "weight": 2,
    },
    "association_type": {
        "name": "Association Type",
        "emoji": "🔗",
        "color": "#8b5cf6",
        "weight": 2,
    },
    "trend_lines": {
        "name": "Trend Lines & Slope",
        "emoji": "📐",
        "color": "#10b981",
        "weight": 2,
    },
    "predictions": {
        "name": "Interpolation & Extrapolation",
        "emoji": "🎯",
        "color": "#f59e0b",
        "weight": 2,
    },
    "two_way_tables": {
        "name": "Two-Way Tables",
        "emoji": "📋",
        "color": "#ef4444",
        "weight": 1,
    },
    "outliers_interpretation": {
        "name": "Outliers & Interpretation",
        "emoji": "🔍",
        "color": "#06b6d4",
        "weight": 2,
    },
}

UNIT4_CATEGORY_ACTIVITY = {
    "scatter_correlation": "activity_1_scatterplots_correlation",
    "association_type": "activity_2_association_strength",
    "trend_lines": "activity_3_trend_lines_slope",
    "predictions": "activity_4_predictions",
    "two_way_tables": "activity_5_two_way_tables",
    "outliers_interpretation": "activity_6_outliers_interpretation",
}

UNIT4_REVISION_TIPS = {
    "scatter_correlation": "Positive: up left-to-right. Negative: down. No pattern: scattered with no direction.",
    "association_type": "Linear = points follow a line. Strong = tight cluster. Weak = spread out.",
    "trend_lines": "Slope = (y₂ − y₁)/(x₂ − x₁) using two points ON the trend line.",
    "predictions": "Interpolation = inside data range. Extrapolation = outside the data range.",
    "two_way_tables": "Row total − known cell = missing cell. Variables are the two categories.",
    "outliers_interpretation": "Outliers can pull a trend line. Check if they overstate or understate the relationship.",
}

UNIT4_QUESTION_BANK: list[dict] = [
    # ── Scatterplots & correlation (8) ──
    {
        "id": "u4_sc1", "category": "scatter_correlation",
        "question": (
            "A quarterback's touchdown passes in games 1–5 were 3, 1, 3, 2, 3. "
            "Which point belongs on a scatterplot with game number on the x-axis?"
        ),
        "options": ["(2, 4)", "(3, 1)", "(1, 2)", "(5, 3)"],
        "answer": 3,
        "explanation": "Game 5 → 3 touchdowns → point (5, 3).",
    },
    {
        "id": "u4_sc2", "category": "scatter_correlation",
        "question": "Use the scatterplot. Which describes the correlation?",
        "options": [
            "Negative correlation",
            "Positive correlation",
            "No correlation",
            "Cannot tell without more points",
        ],
        "answer": 0,
        "explanation": "Points trend downward left to right → negative correlation.",
        "image": "practice_u4_trend_negative",
    },
    {
        "id": "u4_sc3", "category": "scatter_correlation",
        "question": "Use the scatterplot. Which describes the correlation?",
        "options": [
            "Positive correlation",
            "Negative correlation",
            "No correlation",
            "Perfect linear correlation",
        ],
        "answer": 0,
        "explanation": "Points trend upward → positive correlation.",
        "image": "practice_u4_study_hours",
    },
    {
        "id": "u4_sc4", "category": "scatter_correlation",
        "question": "Which is a correct way to construct a scatterplot?",
        "options": [
            "For home runs over seasons, season is the independent variable (x-axis)",
            "For umbrellas sold vs rain, umbrellas sold is the independent variable",
            "For voters by age, age is the dependent variable",
            "For bus riders by day of week, day is the dependent variable",
        ],
        "answer": 0,
        "explanation": "The input (season) goes on x; the output (home runs) on y.",
    },
    {
        "id": "u4_sc5", "category": "scatter_correlation",
        "question": (
            "A table has x: 1.6, 1.9, 2.3, 3.4, 3.8, 4.2, 4.3, 4.6, 4.8 and "
            "y: 39, 38, 42, 40, 41, 44, 42, 45, 44. Which statement is true?"
        ),
        "options": [
            "There is a cluster, and as x increases, y increases",
            "There is a cluster, and as x decreases, y increases",
            "No cluster, and as x increases, y increases",
            "No cluster, and as x decreases, y increases",
        ],
        "answer": 0,
        "explanation": "Values cluster between x ≈ 1.6 and 4.8; y generally rises as x rises.",
    },
    {
        "id": "u4_sc6", "category": "scatter_correlation",
        "question": "Use the scatterplot. Which describes the correlation?",
        "options": [
            "No correlation",
            "Negative correlation",
            "Positive correlation",
            "Strong negative only",
        ],
        "answer": 0,
        "explanation": "Points are scattered with no clear direction → no correlation.",
    },
    {
        "id": "u4_sc7", "category": "scatter_correlation",
        "question": "Use the scatterplot. Which describes the correlation?",
        "options": [
            "Positive correlation",
            "Negative correlation",
            "No correlation",
            "More points needed",
        ],
        "answer": 0,
        "explanation": "Clear upward trend → positive correlation.",
    },
    {
        "id": "u4_sc8", "category": "scatter_correlation",
        "question": (
            "Hours reading vs hours on chores: points are scattered with no pattern. "
            "Which statement is true?"
        ),
        "options": [
            "Reading hours do not affect chore hours in general",
            "As reading increases, chores increase",
            "Chore hours equal reading hours",
            "As reading increases, chores decrease",
        ],
        "answer": 0,
        "explanation": "No correlation means one variable does not predict the other.",
    },
    # ── Association type (7) ──
    {
        "id": "u4_at1", "category": "association_type",
        "question": (
            "Wyatt says a straight line of points always means two variables are related. "
            "Which scatterplot proves that is NOT always true?"
        ),
        "options": [
            "Points at (1,3), (2,3), (3,3), (4,3) — a horizontal line",
            "Points sloping up from (1,1) to (4,4)",
            "Points sloping down from (1,4) to (4,1)",
            "Points in a curved U-shape",
        ],
        "answer": 0,
        "explanation": "Horizontal line: straight but GPA does not change with siblings → no relationship.",
        "image": "practice_u4_wyatt_horizontal",
    },
    {
        "id": "u4_at2", "category": "association_type",
        "question": "Use the scatterplot. What type of association is shown?",
        "options": ["Linear, weak", "Linear, strong", "Nonlinear, strong", "Nonlinear, weak"],
        "answer": 0,
        "explanation": "Points follow a general line but are spread out → linear, weak.",
    },
    {
        "id": "u4_at3", "category": "association_type",
        "question": "Which scatterplot would have a trend line with a negative slope?",
        "options": [
            "Points decreasing as x increases (e.g., y drops from 4.5 to 3.5 as x goes 1 to 3.5)",
            "Points horizontal at y = 3",
            "Points increasing as x increases",
            "Random scatter with no direction",
        ],
        "answer": 0,
        "explanation": "Negative slope: y decreases as x increases.",
        "image": "practice_u4_negative_slope_pick",
    },
    {
        "id": "u4_at4", "category": "association_type",
        "question": "Which scatterplot would NOT have a useful trend line?",
        "options": [
            "Points scattered randomly with no direction",
            "Points in a clear upward line",
            "Points in a clear downward line",
            "Points clustered along a straight band",
        ],
        "answer": 0,
        "explanation": "No clear relationship → no meaningful trend line.",
    },
    {
        "id": "u4_at5", "category": "association_type",
        "question": "Use the scatterplot. Which trend line best fits the data?",
        "options": [
            "A line with positive slope through the middle of the upward cluster",
            "A horizontal line through y = 2",
            "A line with negative slope",
            "A line through the origin only",
        ],
        "answer": 0,
        "explanation": "Data clusters with positive trend → positive-slope line through the cluster.",
        "image": "practice_u4_trend_fit",
    },
    {
        "id": "u4_at6", "category": "association_type",
        "question": (
            "On average, every 30 minutes studied raises a test grade by 8 points. "
            "Which statement about the data set is true?"
        ),
        "options": [
            "The data would show a linear, positive association",
            "The data would show a negative correlation",
            "Every student gains exactly 16 points per hour — no exceptions",
            "The data would show a nonlinear association",
        ],
        "answer": 0,
        "explanation": "Constant rate of change → linear; both variables increase together → positive.",
    },
    {
        "id": "u4_at7", "category": "association_type",
        "question": "Which scatterplot displays an example of a cluster?",
        "options": [
            "Points grouped tightly in one region of the graph",
            "Points spread evenly across the entire graph",
            "A single point far from all others",
            "Points forming a perfect horizontal line",
        ],
        "answer": 0,
        "explanation": "A cluster is a group of points close together in one area.",
    },
    # ── Trend lines & slope (8) ──
    {
        "id": "u4_tl1", "category": "trend_lines",
        "question": (
            "Amani checks her slope on a scatterplot. The trend line tilts down left to right. "
            "What should she expect about the slope sign?"
        ),
        "options": [
            "Negative slope",
            "Positive slope",
            "Zero slope",
            "Undefined slope",
        ],
        "answer": 0,
        "explanation": "Line tilting down → negative slope.",
        "image": "practice_u4_trend_negative",
    },
    {
        "id": "u4_tl2", "category": "trend_lines",
        "question": "Which statement is true about trend lines?",
        "options": [
            "A trend line can be used to make predictions in real-world situations",
            "A trend line must pass through the largest data point",
            "A trend line shows exact collected data points only",
            "A trend line must pass through the smallest data point",
        ],
        "answer": 0,
        "explanation": "Trend lines model the overall pattern and support predictions.",
    },
    {
        "id": "u4_tl3", "category": "trend_lines",
        "question": (
            "Use the graph. Which expression finds the slope of the line of best fit "
            "through (4, 35) and (16, 134)?"
        ),
        "options": [
            "(134 − 35)/(16 − 4)",
            "(4 − 16)/(35 − 134)",
            "(4 − 16)/(134 − 35)",
            "(134 − 16)/(35 − 4)",
        ],
        "answer": 0,
        "explanation": "Slope = rise/run = (134 − 35)/(16 − 4).",
        "image": "practice_u4_slope_line",
    },
    {
        "id": "u4_tl4", "category": "trend_lines",
        "question": (
            "Trend line passes through (2, 79) and (12, 24). "
            "Which expression gives the slope?"
        ),
        "options": [
            "(24 − 79)/(12 − 2)",
            "(24 − 79)/(12 + 2)",
            "(24 + 79)/(12 + 2)",
            "(24 − 79)/(2 − 12)",
        ],
        "answer": 0,
        "explanation": "Use (y₂ − y₁)/(x₂ − x₁) = (24 − 79)/(12 − 2).",
    },
    {
        "id": "u4_tl5", "category": "trend_lines",
        "question": (
            "Plant height trend line passes through (5, 3) and (12, 7). "
            "What is the equation of the trend line?"
        ),
        "options": [
            "y = (4/7)x + 1/7",
            "y = (1/7)x + 16/7",
            "y = (4/7)x − 1/7",
            "y = (1/7)x + 4/7",
        ],
        "answer": 0,
        "explanation": "Slope = (7−3)/(12−5) = 4/7. y = (4/7)(5) + b = 3 → b = 1/7.",
    },
    {
        "id": "u4_tl6", "category": "trend_lines",
        "question": "A regression line and a trend line are —",
        "options": [
            "Equivalent terms for the line of best fit",
            "Opposite terms",
            "Only for largest points",
            "Only for smallest points",
        ],
        "answer": 0,
        "explanation": "Regression line and trend line both describe the line of best fit.",
    },
    {
        "id": "u4_tl7", "category": "trend_lines",
        "question": (
            "Loren solved 10 = (19/9)(149) + b to find b for a trend line through (1,130) and (10,149). "
            "What error did she make?"
        ),
        "options": [
            "She should have solved 149 = (19/9)(10) + b",
            "She should have solved 130 = (9/19)(1) + b",
            "She mixed up slope and y-intercept",
            "She used the wrong slope entirely",
        ],
        "answer": 0,
        "explanation": "Use a point ON the line: y = mx + b with (10, 149), not x = 10 as y-value.",
    },
    {
        "id": "u4_tl8", "category": "trend_lines",
        "question": (
            "Trend line through (4, 21) and (8, 35). Which expression gives the slope?"
        ),
        "options": [
            "(35 − 21)/(8 − 4)",
            "(21 − 35)/(8 − 4)",
            "(8 − 4)/(21 − 35)",
            "(8 − 4)/(35 − 21)",
        ],
        "answer": 0,
        "explanation": "Slope = (35 − 21)/(8 − 4) = 14/4 = 3.5.",
    },
    # ── Predictions (8) ──
    {
        "id": "u4_pr1", "category": "predictions",
        "question": (
            "Naomi's apple weight scatterplot has data from about 5 to 15 apples. "
            "For which number of apples is predicting weight an extrapolation?"
        ),
        "options": ["18 apples", "6 apples", "12 apples", "15 apples"],
        "answer": 0,
        "explanation": "18 is outside the data range → extrapolation.",
        "image": "practice_u4_naomi_apples",
    },
    {
        "id": "u4_pr2", "category": "predictions",
        "question": (
            "Hot chocolate sales vs temperature: data from about 42°F to 58°F. "
            "For which temperature is a cups-sold prediction an interpolation?"
        ),
        "options": ["49°F", "63°F", "21°F", "35°F"],
        "answer": 0,
        "explanation": "49°F is inside the data cluster → interpolation.",
        "image": "practice_u4_hot_chocolate",
    },
    {
        "id": "u4_pr3", "category": "predictions",
        "question": (
            "Candle height vs hours burned: trend line from 10 cm at 0 hr toward 0 cm at 5 hr. "
            "Best estimate for height after 1 hour?"
        ),
        "options": ["8 cm", "4 cm", "9 cm", "5 cm"],
        "answer": 0,
        "explanation": "Linear decrease ~2 cm/hr from 10 cm → about 8 cm at 1 hour.",
        "image": "practice_u4_candle_height",
    },
    {
        "id": "u4_pr4", "category": "predictions",
        "question": (
            "Travel model: y = 1.04x − 7.15 (x = minutes, y = miles). "
            "How many miles for 48 minutes?"
        ),
        "options": ["About 42 miles", "About 54 miles", "About 32 miles", "48 miles"],
        "answer": 0,
        "explanation": "y = 1.04(48) − 7.15 ≈ 49.92 − 7.15 ≈ 42.8 → about 42 miles.",
        "image": "practice_u4_travel_line",
    },
    {
        "id": "u4_pr5", "category": "predictions",
        "question": (
            "Beaded jewelry: y = 2.52x + 1.61 (x = cord inches, y = beads). "
            "Best estimate for beads on a 32-inch cord?"
        ),
        "options": ["About 82 beads", "About 68 beads", "About 132 beads", "About 12 beads"],
        "answer": 0,
        "explanation": "y = 2.52(32) + 1.61 ≈ 80.64 + 1.61 ≈ 82.",
    },
    {
        "id": "u4_pr6", "category": "predictions",
        "question": (
            "Calories model: y = 9.56x + 495.35 (x = weight in lb, y = calories). "
            "Jill eats 1850 cal/day. Jaxon weighs 120 lb. Which comparison is accurate?"
        ),
        "options": [
            "Jill weighs about 20 pounds more than Jaxon",
            "Jill consumes 20 more calories than Jaxon",
            "Jaxon weighs 20 pounds more than Jill",
            "Jaxon consumes 20 more calories than Jill",
        ],
        "answer": 0,
        "explanation": "Solve 1850 = 9.56x + 495.35 → x ≈ 142 lb for Jill vs Jaxon's 120 lb.",
    },
    {
        "id": "u4_pr7", "category": "predictions",
        "question": "Data points from x = 3 to x = 15. Predicting at x = 6 is —",
        "options": ["Interpolation", "Extrapolation", "An outlier", "Impossible"],
        "answer": 0,
        "explanation": "6 is inside the range 3–15 → interpolation.",
    },
    {
        "id": "u4_pr8", "category": "predictions",
        "question": "Data points from x = 3 to x = 15. Predicting at x = 20 is —",
        "options": ["Extrapolation", "Interpolation", "A cluster", "The y-intercept"],
        "answer": 0,
        "explanation": "20 is outside the data range → extrapolation.",
    },
    # ── Two-way tables (7) ──
    {
        "id": "u4_tw1", "category": "two_way_tables",
        "question": (
            "Favorite juices: Girls total 16 (7 grapefruit). Boys total 14 (3 grapefruit). "
            "How many girls prefer orange juice?"
        ),
        "options": ["9 girls", "11 girls", "23 girls", "7 girls"],
        "answer": 0,
        "explanation": "16 − 7 = 9 girls prefer orange juice.",
    },
    {
        "id": "u4_tw2", "category": "two_way_tables",
        "question": (
            "Pets table: 8th grade has 26 cats, 35 dogs (61 total). "
            "Totals: 54 cats, 48 dogs. How many 7th graders have cats?"
        ),
        "options": ["28 cats", "13 cats", "83 cats", "26 cats"],
        "answer": 0,
        "explanation": "7th grade cats = 54 − 26 = 28.",
    },
    {
        "id": "u4_tw3", "category": "two_way_tables",
        "question": (
            "Study groups: 3rd period 18 in Group 1, 14 in Group 2. "
            "4th period 15 in Group 1, 17 in Group 2. What are the variables?"
        ),
        "options": [
            "Period number and study group number",
            "Study group and period 3 only",
            "Group 1 and total students",
            "Period and total only",
        ],
        "answer": 0,
        "explanation": "Two categorical variables: which period and which study group.",
    },
    {
        "id": "u4_tw4", "category": "two_way_tables",
        "question": (
            "Favorite fruits: Class A 13 apples, 20 bananas (33 total). "
            "Total apples 31. How many students in Class B prefer apples?"
        ),
        "options": ["18 students", "16 students", "13 students", "20 students"],
        "answer": 0,
        "explanation": "Class B apples = 31 − 13 = 18.",
    },
    {
        "id": "u4_tw5", "category": "two_way_tables",
        "question": (
            "Teams table: Boys 15 on Team A, 18 on Team B (33 total). "
            "Girls total 31, Team A girls 17. How many girls on Team B?"
        ),
        "options": ["14 girls", "18 girls", "15 girls", "17 girls"],
        "answer": 0,
        "explanation": "Team B girls = 31 − 17 = 14 (or 32 − 18 = 14).",
    },
    {
        "id": "u4_tw6", "category": "two_way_tables",
        "question": (
            "Juice table: Boys total 14, 3 prefer grapefruit. "
            "How many boys prefer orange juice?"
        ),
        "options": ["11 boys", "9 boys", "3 boys", "14 boys"],
        "answer": 0,
        "explanation": "14 − 3 = 11 boys prefer orange juice.",
    },
    {
        "id": "u4_tw7", "category": "two_way_tables",
        "question": "In a two-way table, the two variables are always —",
        "options": [
            "Two different categorical attributes",
            "One numeric and one categorical",
            "Always row totals and column totals",
            "Independent and dependent numerical variables",
        ],
        "answer": 0,
        "explanation": "Two-way tables cross-tabulate two categorical variables.",
    },
    # ── Outliers & interpretation (7) ──
    {
        "id": "u4_oi1", "category": "outliers_interpretation",
        "question": (
            "Rent vs roommates scatterplot has an outlier at (2, 100) while others are $200–350. "
            "Including this point could cause the relationship to be —"
        ),
        "options": [
            "Understated (slope less steep than it should be)",
            "Overstated (slope steeper than it should be)",
            "Unchanged",
            "Proven to have no relationship",
        ],
        "answer": 0,
        "explanation": "Low outlier pulls the line down → understates the negative trend.",
        "image": "practice_u4_roommates_rent",
    },
    {
        "id": "u4_oi2", "category": "outliers_interpretation",
        "question": (
            "Ticket sales: most points follow hours vs tickets trend, but (1, 60) is far above others near (1, 10). "
            "Which value would overstate the relationship?"
        ),
        "options": ["(1, 60)", "(10, 80)", "(1, 10)", "(9, 85)"],
        "answer": 0,
        "explanation": "(1, 60) is an outlier that pulls the trend line up → overstates the relationship.",
        "image": "practice_u4_ticket_outlier",
    },
    {
        "id": "u4_oi3", "category": "outliers_interpretation",
        "question": (
            "Teacher age vs height: Teacher 3 is (50, 60) but plotted at (60, 50). "
            "What error was made?"
        ),
        "options": [
            "Mixed up x- and y-coordinates for teacher 3",
            "Plotted (36, 62) when it should not appear",
            "Swapped independent and dependent variables entirely",
            "Labeled x-axis 'Age' incorrectly",
        ],
        "answer": 0,
        "explanation": "Age should be x and height y — (50, 60) was swapped to (60, 50).",
    },
    {
        "id": "u4_oi4", "category": "outliers_interpretation",
        "question": (
            "Mackenzie: as study hours increase, test scores increase. "
            "Two students studied 2 hours with different scores. Which is correct?"
        ),
        "options": [
            "There is still a relationship — same x can have different y values",
            "No relationship because x = 2 appears twice",
            "No relationship because points are not on a perfect line",
            "The data must be nonlinear",
        ],
        "answer": 0,
        "explanation": "Real data varies; overall trend still shows positive relationship.",
        "image": "practice_u4_study_hours",
    },
    {
        "id": "u4_oi5", "category": "outliers_interpretation",
        "question": (
            "Sit-ups vs time scatterplot: 8 distinct points plotted, none overlapping. "
            "How many data points were in the table?"
        ),
        "options": ["8", "7", "6", "5"],
        "answer": 0,
        "explanation": "Each non-overlapping dot = one data point → 8.",
    },
    {
        "id": "u4_oi6", "category": "outliers_interpretation",
        "question": (
            "Which linear function has the same y-intercept as a graph with y-intercept 10?"
        ),
        "options": [
            "Table with slope 6: (−6, −26) to (4, 34) → y = 6x + 10",
            "Table with y-intercept −5",
            "Table with y-intercept −10",
            "Table with y-intercept 5",
        ],
        "answer": 0,
        "explanation": "Extend table A: at x = 0, y = 10 matches the graph's y-intercept.",
        "image": "practice_u4_trend_fit",
    },
    {
        "id": "u4_oi7", "category": "outliers_interpretation",
        "question": (
            "A scatterplot shows points widely scattered with no direction. "
            "Which statement about chores vs reading is true?"
        ),
        "options": [
            "No general effect of reading on chore time",
            "Strong positive correlation",
            "Strong negative correlation",
            "Perfect linear relationship",
        ],
        "answer": 0,
        "explanation": "Random scatter → no correlation / no predictable relationship.",
    },
]
