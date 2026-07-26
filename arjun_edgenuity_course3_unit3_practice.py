"""Edgenuity Course 3 Unit 3 — Writing Equations for Linear Relationships."""

from __future__ import annotations

UNIT3_CATEGORIES = {
    "slope_intercept_read": {
        "name": "Slope & Y-Intercept",
        "emoji": "📊",
        "color": "#3b82f6",
        "weight": 2,
    },
    "two_point_equations": {
        "name": "Two-Point Equations",
        "emoji": "✏️",
        "color": "#8b5cf6",
        "weight": 2,
    },
    "point_slope_form": {
        "name": "Point-Slope Form",
        "emoji": "📐",
        "color": "#10b981",
        "weight": 1,
    },
    "standard_form": {
        "name": "Standard Form",
        "emoji": "🔄",
        "color": "#f59e0b",
        "weight": 1,
    },
    "context_meaning": {
        "name": "Context & Meaning",
        "emoji": "🌍",
        "color": "#ef4444",
        "weight": 2,
    },
    "compare_functions": {
        "name": "Compare Functions",
        "emoji": "⚖️",
        "color": "#06b6d4",
        "weight": 2,
    },
}

UNIT3_CATEGORY_ACTIVITY = {
    "slope_intercept_read": "activity_1_slope_intercept_read",
    "two_point_equations": "activity_2_two_point_equations",
    "point_slope_form": "activity_3_point_slope_form",
    "standard_form": "activity_4_standard_form",
    "context_meaning": "activity_5_context_meaning",
    "compare_functions": "activity_6_compare_functions",
}

UNIT3_REVISION_TIPS = {
    "slope_intercept_read": "Slope = (y₂ − y₁) ÷ (x₂ − x₁). Y-intercept is y when x = 0.",
    "two_point_equations": "Find slope first, then substitute one point into y = mx + b to find b.",
    "point_slope_form": "Use y − y₁ = m(x − x₁), then distribute and solve for y.",
    "standard_form": "Isolate y: divide every term by the coefficient of y. Watch signs when dividing negatives.",
    "context_meaning": "Slope = rate per unit; y-intercept = starting amount (when x = 0).",
    "compare_functions": "Convert both to y = mx + b before comparing steepness (|m|) and y-intercept.",
}

UNIT3_QUESTION_BANK: list[dict] = [
    # ── Slope & y-intercept read (10) ──
    {
        "id": "u3_si1", "category": "slope_intercept_read",
        "question": (
            "Use the table. What are the slope and y-intercept of the linear function?\n\n"
            "| x | −1 | −½ | 0 | ½ |\n| y | −1½ | 0 | 1½ | 3 |"
        ),
        "options": [
            "Slope 3, y-intercept 3/2",
            "Slope −3, y-intercept 3/2",
            "Slope 3, y-intercept −1/2",
            "Slope −3, y-intercept −1/2",
        ],
        "answer": 0,
        "explanation": "Slope = (3/2 − 0)/(0 − (−1/2)) = 3. At x = 0, y = 3/2.",
    },
    {
        "id": "u3_si2", "category": "slope_intercept_read",
        "question": "What are the slope and y-intercept of y = 9x − 2?",
        "options": [
            "Slope 9, y-intercept −2",
            "Slope 9, y-intercept 2",
            "Slope −2, y-intercept 9",
            "Slope 2, y-intercept 9",
        ],
        "answer": 0,
        "explanation": "In y = mx + b, m = 9 and b = −2.",
    },
    {
        "id": "u3_si3", "category": "slope_intercept_read",
        "question": (
            "Use the table. What are the slope and y-intercept?\n\n"
            "| x | −6 | −1 | 4 | 9 |\n| y | −18 | −8 | 2 | 12 |"
        ),
        "options": [
            "Slope 2, y-intercept −6",
            "Slope −2, y-intercept 12",
            "Slope 2, y-intercept 6",
            "Slope −2, y-intercept 6",
        ],
        "answer": 0,
        "explanation": "Slope = (2 − (−8))/(4 − (−1)) = 2. At x = −1, y = −8 → b = −8 − 2(−1) = −6.",
    },
    {
        "id": "u3_si4", "category": "slope_intercept_read",
        "question": "Use the graph. What are the slope and y-intercept of the line shown?",
        "options": [
            "Slope −3/4, y-intercept 3",
            "Slope −3/4, y-intercept 4",
            "Slope −4/3, y-intercept 3",
            "Slope −4/3, y-intercept 4",
        ],
        "answer": 0,
        "explanation": "Line crosses y-axis at 3 and x-axis at 4 → slope = (0−3)/(4−0) = −3/4.",
        "image": "practice_u3_slope_from_graph",
    },
    {
        "id": "u3_si5", "category": "slope_intercept_read",
        "question": "Use the graph. What are the slope and y-intercept?",
        "options": [
            "Slope 2/3, y-intercept −2",
            "Slope 2/3, y-intercept 3",
            "Slope 3/2, y-intercept −2",
            "Slope 3/2, y-intercept 3",
        ],
        "answer": 0,
        "explanation": "Y-intercept is −2. Slope = (0 − (−2))/(3 − 0) = 2/3.",
        "image": "practice_u3_graph_fractions",
    },
    {
        "id": "u3_si6", "category": "slope_intercept_read",
        "question": "Use the graph. What are the slope and y-intercept?",
        "options": [
            "Slope 4, y-intercept 12",
            "Slope 3, y-intercept 12",
            "Slope 4, y-intercept 9",
            "Slope 3, y-intercept 9",
        ],
        "answer": 0,
        "explanation": "From (−3, 0) to (−2, 4): slope = 4/1 = 4. Extend back to x = 0 → y = 12.",
        "image": "practice_u3_graph_yint12",
    },
    {
        "id": "u3_si7", "category": "slope_intercept_read",
        "question": (
            "What is the equation in slope-intercept form for the table?\n\n"
            "| x | −6 | −1 | 4 | 9 |\n| y | −18 | −8 | 2 | 12 |"
        ),
        "options": ["y = 2x − 6", "y = −2x + 6", "y = 2x + 6", "y = −2x − 6"],
        "answer": 0,
        "explanation": "Slope = 10/5 = 2. Using (−1, −8): −8 = 2(−1) + b → b = −6.",
    },
    {
        "id": "u3_si8", "category": "slope_intercept_read",
        "question": (
            "The table shows miles traveled y after x hours.\n\n"
            "| x (hr) | 2.5 | 4.0 | 5.5 | 7.0 |\n| y (mi) | 150 | 240 | 330 | 420 |\n"
            "Which equation represents the situation?"
        ),
        "options": ["y = 60x", "y = 270x", "y = 4x + 240", "y = 60x + 480"],
        "answer": 0,
        "explanation": "Rate = (240−150)/(4−2.5) = 90/1.5 = 60 mi/hr. Through origin → y = 60x.",
    },
    {
        "id": "u3_si9", "category": "slope_intercept_read",
        "question": "A line has y-intercept −7 and passes through (2, −1). What is the missing slope in y = □x − 7?",
        "options": ["3", "−3", "4", "−4"],
        "answer": 0,
        "explanation": "Slope = (−1 − (−7))/(2 − 0) = 6/2 = 3.",
    },
    {
        "id": "u3_si10", "category": "slope_intercept_read",
        "question": (
            "What are the slope and y-intercept?\n\n"
            "| x | −3 | 0 | 3 | 6 |\n| y | 18 | 12 | 6 | 0 |"
        ),
        "options": [
            "Slope −2, y-intercept 12",
            "Slope 2, y-intercept 12",
            "Slope −2, y-intercept 6",
            "Slope 2, y-intercept 6",
        ],
        "answer": 0,
        "explanation": "Slope = (6 − 12)/(3 − 0) = −2. At x = 0, y = 12.",
    },
    # ── Two-point equations (8) ──
    {
        "id": "u3_tp1", "category": "two_point_equations",
        "question": "Use the graph. Which equation passes through points B and C?",
        "options": ["y = −2x − 6", "y = 2x − 6", "y = −2x + 10", "y = 2x + 10"],
        "answer": 0,
        "explanation": "B(−2, −2) and C(−1, −4): slope = (−4−(−2))/(−1−(−2)) = −2. y = −2x − 6.",
        "image": "practice_u3_bc_points",
    },
    {
        "id": "u3_tp2", "category": "two_point_equations",
        "question": "Which equation passes through (0, 6) and (2, 0)?",
        "options": ["y = −3x + 6", "y = −3x + 2", "y = −⅓x + 6", "y = −⅓x + 2"],
        "answer": 0,
        "explanation": "Slope = (0−6)/(2−0) = −3. Y-intercept is 6.",
        "image": "practice_u3_two_points_line",
    },
    {
        "id": "u3_tp3", "category": "two_point_equations",
        "question": (
            "A line has slope −¼ and passes through (−5/4, 1). "
            "What is the equation in slope-intercept form?"
        ),
        "options": [
            "y = −¼x + 11/16",
            "y = −¼x + 21/16",
            "y = −¼x − 5/4",
            "y = −¼x − ¼",
        ],
        "answer": 0,
        "explanation": "1 = −¼(−5/4) + b → 1 = 5/16 + b → b = 11/16.",
    },
    {
        "id": "u3_tp4", "category": "two_point_equations",
        "question": "What is the equation through (2, −1) and (5, −10) in slope-intercept form?",
        "options": ["y = −3x + 5", "y = 3x − 5", "y = −3x − 5", "y = 3x + 5"],
        "answer": 0,
        "explanation": "Slope = (−10−(−1))/(5−2) = −3. −1 = −3(2) + b → b = 5.",
    },
    {
        "id": "u3_tp5", "category": "two_point_equations",
        "question": (
            "A library tracks computer hours y vs days x:\n"
            "| x | 3 | 5 | 7 |\n| y | 21 | 37 | 53 |\n"
            "What linear equation models this?"
        ),
        "options": ["y = 8x − 3", "y = 2x − 32", "y = 2x + 16", "y = 8x + 45"],
        "answer": 0,
        "explanation": "Slope = (37−21)/(5−3) = 8. 21 = 8(3) + b → b = −3.",
    },
    {
        "id": "u3_tp6", "category": "two_point_equations",
        "question": (
            "What method writes slope-intercept form from two points?"
        ),
        "options": [
            "Find slope with m = (y₂−y₁)/(x₂−x₁), then substitute a point into y = mx + b for b",
            "Find y-intercept with m = (y₂−y₁)/(x₂−x₁), then substitute for slope",
            "Find slope with m = (x₂−x₁)/(y₂−y₁), then substitute for b",
            "Average the x- and y-coordinates of both points",
        ],
        "answer": 0,
        "explanation": "Standard two-point method: slope first, then solve for b.",
    },
    {
        "id": "u3_tp7", "category": "two_point_equations",
        "question": "What is the y-intercept of a line with slope −3 that passes through (−5, 4)?",
        "options": ["−11", "7", "19", "−17"],
        "answer": 0,
        "explanation": "4 = −3(−5) + b → 4 = 15 + b → b = −11.",
    },
    {
        "id": "u3_tp8", "category": "two_point_equations",
        "question": "Which equation has slope 1 and passes through (5, 3)?",
        "options": ["y = x − 2", "y = x − 5", "y = x + 3", "y = x + 2"],
        "answer": 0,
        "explanation": "3 = 1(5) + b → b = −2.",
    },
    # ── Point-slope form (6) ──
    {
        "id": "u3_ps1", "category": "point_slope_form",
        "question": "Convert y − 5 = 6(x + 1) to slope-intercept form.",
        "options": ["y = 6x + 11", "y = 6x − 1", "y = 6x + 6", "y = 6x − 4"],
        "answer": 0,
        "explanation": "y − 5 = 6x + 6 → y = 6x + 11.",
    },
    {
        "id": "u3_ps2", "category": "point_slope_form",
        "question": "What is the point-slope form of a line with slope ½ through (−7, 2)?",
        "options": [
            "y − 2 = ½(x − (−7))",
            "y − 7 = ½(x − 2)",
            "7 − y = ½(−2 − x)",
            "2 − y = ½(7 − x)",
        ],
        "answer": 0,
        "explanation": "Point-slope: y − y₁ = m(x − x₁) with (x₁, y₁) = (−7, 2).",
    },
    {
        "id": "u3_ps3", "category": "point_slope_form",
        "question": "Which equation has slope 4 and passes through (1, 6)?",
        "options": ["y = 4x + 2", "y = 4x + 6", "y = 4x − 3", "y = 4x − 2"],
        "answer": 0,
        "explanation": "6 = 4(1) + b → b = 2.",
    },
    {
        "id": "u3_ps4", "category": "point_slope_form",
        "question": "Write point-slope form for a line with slope −3 through (−5, 4), then find the y-intercept.",
        "options": ["−11", "7", "19", "−17"],
        "answer": 0,
        "explanation": "y − 4 = −3(x + 5) → y = −3x − 11.",
    },
    {
        "id": "u3_ps5", "category": "point_slope_form",
        "question": "Line through (5, 3) with slope 1. Which equation is correct?",
        "options": ["y = x − 2", "y = x + 2", "y = x − 5", "y = x + 3"],
        "answer": 0,
        "explanation": "3 = 5 + b → b = −2.",
    },
    {
        "id": "u3_ps6", "category": "point_slope_form",
        "question": "Convert y − 36 = 8(x − 4) to slope-intercept form.",
        "options": ["y = 8x + 4", "y = 8x − 4", "y = 8x + 36", "y = 8x − 68"],
        "answer": 0,
        "explanation": "y = 8x − 32 + 36 = 8x + 4.",
    },
    # ── Standard form (5) ──
    {
        "id": "u3_st1", "category": "standard_form",
        "question": (
            "Jill converted 15x − 4y = −2 to slope-intercept form and got "
            "slope −15/4 and y-intercept 1/2. What was her mistake?"
        ),
        "options": [
            "She got the sign of the slope wrong",
            "She mixed up slope and y-intercept",
            "She got the sign of the y-intercept wrong",
            "She used reciprocals of slope and intercept",
        ],
        "answer": 0,
        "explanation": "Correct: y = (15/4)x + 1/2. Dividing −15x by −4 gives +15/4, not −15/4.",
    },
    {
        "id": "u3_st2", "category": "standard_form",
        "question": "Write 15x − 4y = −2 in slope-intercept form.",
        "options": [
            "y = (15/4)x + 1/2",
            "y = −(15/4)x + 1/2",
            "y = (15/4)x − 1/2",
            "y = −(15/4)x − 1/2",
        ],
        "answer": 0,
        "explanation": "−4y = −2 − 15x → y = (−2/(−4)) + (−15x/(−4)) = 1/2 + (15/4)x.",
    },
    {
        "id": "u3_st3", "category": "standard_form",
        "question": "Write 2x + 3y = 12 in slope-intercept form.",
        "options": ["y = −⅔x + 4", "y = ⅔x + 4", "y = −⅔x − 4", "y = 2x + 4"],
        "answer": 0,
        "explanation": "3y = −2x + 12 → y = −(2/3)x + 4.",
    },
    {
        "id": "u3_st4", "category": "standard_form",
        "question": "Write −6x + 2y = 8 in slope-intercept form.",
        "options": ["y = 3x + 4", "y = −3x + 4", "y = 3x − 4", "y = −3x − 4"],
        "answer": 0,
        "explanation": "2y = 6x + 8 → y = 3x + 4.",
    },
    {
        "id": "u3_st5", "category": "standard_form",
        "question": "When converting Ax + By = C to y = mx + b, what is the most common error?",
        "options": [
            "Getting the sign wrong when dividing by B",
            "Adding C to both sides instead of subtracting",
            "Forgetting to divide the x-term only",
            "Using x-intercept instead of y-intercept",
        ],
        "answer": 0,
        "explanation": "Sign errors when dividing by a negative coefficient of y are very common.",
    },
    # ── Context & meaning (8) ──
    {
        "id": "u3_cm1", "category": "context_meaning",
        "question": (
            "Inez's phone card graph starts at 850 minutes (day 0) and loses 50 minutes per day. "
            "What do the slope and y-intercept represent?"
        ),
        "options": [
            "Y-intercept: 850 minutes at start. Slope: 50 minutes used per day",
            "Y-intercept: 50 minutes at start. Slope: 850 minutes used per day",
            "Slope: 850 minutes added per day. Y-intercept: 50 minutes",
            "Both represent the total minutes purchased",
        ],
        "answer": 0,
        "explanation": "Starting balance = y-intercept. Daily loss = |slope| = 50 min/day.",
        "image": "practice_u3_inez_phone",
    },
    {
        "id": "u3_cm2", "category": "context_meaning",
        "question": (
            "A repair service costs y = 45x + 35 (x = hours, y = total dollars). "
            "What does the slope represent?"
        ),
        "options": [
            "Cost per hour of repair",
            "Total cost for any job",
            "Fee for the service call visit",
            "Travel time to the home",
        ],
        "answer": 0,
        "explanation": "Slope 45 = dollars per hour of repair work.",
    },
    {
        "id": "u3_cm3", "category": "context_meaning",
        "question": (
            "Same model y = 45x + 35. What does the y-intercept represent?"
        ),
        "options": [
            "The service fee for coming to look at the machine",
            "Cost per hour of repair",
            "Total cost after one hour",
            "Travel time in hours",
        ],
        "answer": 0,
        "explanation": "Y-intercept 35 = fixed fee before any hourly charges.",
    },
    {
        "id": "u3_cm4", "category": "context_meaning",
        "question": (
            "Dog food stock: y = −15x + 430 (x = days open, y = pounds left). "
            "How many pounds remain after 21 days?"
        ),
        "options": ["115", "315", "92", "336"],
        "answer": 0,
        "explanation": "y = −15(21) + 430 = −315 + 430 = 115 pounds.",
    },
    {
        "id": "u3_cm5", "category": "context_meaning",
        "question": (
            "In the dog food model y = −15x + 430, what does −15 represent?"
        ),
        "options": [
            "Pounds of dog food sold per day",
            "Starting inventory in pounds",
            "Days until stock runs out",
            "Price per pound",
        ],
        "answer": 0,
        "explanation": "Negative slope: stock decreases 15 pounds each day open.",
    },
    {
        "id": "u3_cm6", "category": "context_meaning",
        "question": (
            "Miles traveled after x hours: 150 at 2.5 hr, 240 at 4 hr. "
            "Which equation fits if the trip started at 0 miles?"
        ),
        "options": ["y = 60x", "y = 60x + 150", "y = 90x", "y = 40x"],
        "answer": 0,
        "explanation": "Rate = 60 mi/hr with no initial offset → y = 60x.",
    },
    {
        "id": "u3_cm7", "category": "context_meaning",
        "question": (
            "Phone card: slope −50, y-intercept 850. After how many days is the balance 0?"
        ),
        "options": ["17 days", "850 days", "50 days", "12 days"],
        "answer": 0,
        "explanation": "850 ÷ 50 = 17 days until minutes reach zero.",
    },
    {
        "id": "u3_cm8", "category": "context_meaning",
        "question": (
            "Computer use: y = 8x − 3 (x days, y hours). What does −3 represent?"
        ),
        "options": [
            "Hours recorded before tracking started (adjustment at day 0)",
            "Hours used per day",
            "Total hours after 3 days",
            "Cannot be determined",
        ],
        "answer": 0,
        "explanation": "Y-intercept −3 is the starting value when x = 0 in the model.",
    },
    # ── Compare functions (8) ──
    {
        "id": "u3_cf1", "category": "compare_functions",
        "question": (
            "Compare y = −10x + 6 and y − 36 = 8(x − 4) (rewrite second as y = 8x + 4). "
            "Which statement is correct?"
        ),
        "options": [
            "y = −10x + 6 has a steeper slope and greater y-intercept",
            "Second equation has steeper slope and greater y-intercept",
            "First has steeper slope; second has greater y-intercept",
            "Second has steeper slope; first has greater y-intercept",
        ],
        "answer": 0,
        "explanation": "|−10| > |8| so first is steeper. 6 > 4 so first has greater y-intercept.",
    },
    {
        "id": "u3_cf2", "category": "compare_functions",
        "question": (
            "Use the graph. Compare y = 2x + 2 to the line shown. "
            "Which statement is correct?"
        ),
        "options": [
            "The graph has a steeper slope; the equation has a greater y-intercept",
            "The graph has a steeper slope and greater y-intercept",
            "The equation has a steeper slope and greater y-intercept",
            "The equation has a steeper slope; the graph has a greater y-intercept",
        ],
        "answer": 0,
        "explanation": "Graph slope 3 > 2; equation y-intercept 2 > 1.",
        "image": "practice_u3_compare_graph",
    },
    {
        "id": "u3_cf3", "category": "compare_functions",
        "question": (
            "Jeremy says two lines with the same steepness and same y-intercept must be identical. "
            "The graph shows y = ½x − 1. Which equation proves Jeremy wrong?"
        ),
        "options": [
            "y = −½x − 1",
            "y = −½x + 1",
            "y = ½x − 1",
            "y = ½x + 1",
        ],
        "answer": 0,
        "explanation": "Same |slope| (steepness) and same y-intercept −1, but opposite direction.",
        "image": "practice_u3_jeremy_graph",
    },
    {
        "id": "u3_cf4", "category": "compare_functions",
        "question": (
            "Which table has the same y-intercept as the graph (y-intercept = 10)?\n"
            "Table A: (−6,−26), (−4,−14), (4,34), (6,46)"
        ),
        "options": [
            "Table A — equation y = 6x + 10",
            "Table with y-intercept −5",
            "Table with y-intercept −10",
            "Table with y-intercept 5",
        ],
        "answer": 0,
        "explanation": "Table A: slope 6, at x=0 → y = 10.",
        "image": "practice_u3_yint_match_graph",
    },
    {
        "id": "u3_cf5", "category": "compare_functions",
        "question": (
            "Compare y = 4x + 5 to a table with (2,16), (4,26), (6,36), (8,46). "
            "Which statement is correct?"
        ),
        "options": [
            "The table has a steeper slope and greater y-intercept",
            "The equation has a steeper slope and greater y-intercept",
            "The table has a steeper slope; equation has greater y-intercept",
            "The equation has a steeper slope; table has greater y-intercept",
        ],
        "answer": 0,
        "explanation": "Table: slope 5, y-int 6. Equation: slope 4, y-int 5.",
    },
    {
        "id": "u3_cf6", "category": "compare_functions",
        "question": (
            "A line has x-intercept 12 and slope 3/8. How does it compare to a table "
            "with slope 3/8 and different y-intercept?"
        ),
        "options": [
            "Same slope, different y-intercept",
            "Same y-intercept, different slope",
            "Same slope and same y-intercept",
            "Different slope and different y-intercept",
        ],
        "answer": 0,
        "explanation": "Matching slope 3/8 but y-intercepts differ.",
    },
    {
        "id": "u3_cf7", "category": "compare_functions",
        "question": (
            "Which table has the same slope as (−½, ⅕), (−⅕, 7/50), (⅕, 3/50), (½, 0)?"
        ),
        "options": [
            "y = −⅕x + 1/10",
            "y = −½x + 1/10",
            "y = ½x − 1/10",
            "y = ⅕x − ½",
        ],
        "answer": 0,
        "explanation": "Table slope = (0 − 3/50)/(½ − ⅕) = −1/5.",
    },
    {
        "id": "u3_cf8", "category": "compare_functions",
        "question": (
            "Line A: y = 2x + 2. Line B passes through (0, 1) and (1, 4). "
            "Which has a greater y-intercept?"
        ),
        "options": ["Line A", "Line B", "They are equal", "Cannot tell"],
        "answer": 0,
        "explanation": "Line A y-intercept 2; Line B y-intercept 1.",
    },
]
