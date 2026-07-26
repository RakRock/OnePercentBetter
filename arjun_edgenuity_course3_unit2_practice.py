"""Edgenuity Course 3 Unit 2 — Linear Functions practice bank."""

from __future__ import annotations

UNIT2_CATEGORIES = {
    "slope_rate": {
        "name": "Slope & Rate",
        "emoji": "📈",
        "color": "#3b82f6",
        "weight": 2,
    },
    "y_intercept": {
        "name": "Y-Intercept",
        "emoji": "📍",
        "color": "#8b5cf6",
        "weight": 1,
    },
    "direct_variation": {
        "name": "Direct Variation",
        "emoji": "🔗",
        "color": "#10b981",
        "weight": 2,
    },
    "special_lines": {
        "name": "Special Lines",
        "emoji": "➖",
        "color": "#f59e0b",
        "weight": 2,
    },
    "writing_equations": {
        "name": "Writing Equations",
        "emoji": "✏️",
        "color": "#06b6d4",
        "weight": 1,
    },
    "linear_modeling": {
        "name": "Linear Modeling",
        "emoji": "🌍",
        "color": "#ef4444",
        "weight": 2,
    },
}

UNIT2_CATEGORY_ACTIVITY = {
    "slope_rate": "activity_1_slope_rate",
    "y_intercept": "activity_2_y_intercept",
    "direct_variation": "activity_3_direct_variation",
    "special_lines": "activity_4_special_lines",
    "writing_equations": "activity_5_writing_equations",
    "linear_modeling": "activity_6_linear_modeling",
}

UNIT2_REVISION_TIPS = {
    "slope_rate": "Slope = change in y ÷ change in x. Rate of change is the slope in context.",
    "y_intercept": "The y-intercept is where the graph crosses the y-axis (x = 0) — the starting amount.",
    "direct_variation": "Direct variation passes through (0, 0) with a constant ratio y/x.",
    "special_lines": "Horizontal → slope 0. Vertical → undefined slope.",
    "writing_equations": "Use y = mx + b or point-slope form, then substitute known points.",
    "linear_modeling": "Define variables, write price × quantity equations, then solve.",
}

UNIT2_QUESTION_BANK: list[dict] = [
    # ── Slope & rate (10) ──
    {
        "id": "u2_sr1", "category": "slope_rate",
        "question": (
            "Wilson waters his garden with a full watering can. The graph shows water remaining "
            "vs time. Which statement is correct?"
        ),
        "options": [
            "The can originally held 2.5 gallons.",
            "Wilson uses 2.5 gallons per second.",
            "Wilson uses 0 gallons per second.",
            "The can originally held 0 gallons.",
        ],
        "answer": 0,
        "explanation": "At time 0, the graph shows 2.5 gallons — the starting amount.",
        "image": "practice_u2_wilson_can",
    },
    {
        "id": "u2_sr2", "category": "slope_rate",
        "question": (
            "Wilson's watering can starts with 2.5 gallons and loses 0.5 gallon each second. "
            "What is the rate of change of water in the can?"
        ),
        "options": ["−0.5 gallons per second", "0.5 gallons per second", "−2.5 gallons per second", "2.5 gallons per second"],
        "answer": 0,
        "explanation": "Water decreases 0.5 gal each second → slope = −0.5.",
        "image": "practice_u2_wilson_can",
    },
    {
        "id": "u2_sr3", "category": "slope_rate",
        "question": (
            "A baseball's travel distance varies directly with swing speed. The graph shows "
            "distance (feet) vs speed (mph). Which relationship fits the graph?"
        ),
        "options": [
            "Distance is 5 times the swing speed.",
            "Distance is 10 times the swing speed.",
            "Distance is 0.1 times the swing speed.",
            "Distance is 0.2 times the swing speed.",
        ],
        "answer": 0,
        "explanation": "Through origin: about 500 ft at 100 mph → 5 ft per mph.",
        "image": "practice_u2_baseball",
    },
    {
        "id": "u2_sr4", "category": "slope_rate",
        "question": (
            "Andrew ran 1.5 miles in 18 minutes and 2 miles in 24 minutes. Karleigh ran "
            "3 miles in 30 minutes and 4 miles in 40 minutes. Who ran a greater distance in 1 hour?"
        ),
        "options": [
            "Karleigh — she runs 1/10 mile per minute vs Andrew's 1/12",
            "Andrew — he runs 1/12 mile per minute vs Karleigh's 1/10",
            "Andrew — both run the same distance",
            "Karleigh — she runs 1/12 mile per minute vs Andrew's 1/10",
        ],
        "answer": 0,
        "explanation": "Andrew: 1.5/18 = 1/12 mi/min. Karleigh: 3/30 = 1/10 mi/min → Karleigh runs farther in 60 min.",
    },
    {
        "id": "u2_sr5", "category": "slope_rate",
        "question": "Which table describes a linear function with slope 2?",
        "options": [
            "x: 2, 6, 8  →  y: 4, 12, 16",
            "x: 0, 2, 6  →  y: 0, 4, 12",
            "x: −4, −2, 2  →  y: 1, −1, −2",
            "x: 4, 7  →  y: 8, 4",
        ],
        "answer": 1,
        "explanation": "Check: (4−0)/(2−0)=2, (12−4)/(6−2)=2.",
    },
    {
        "id": "u2_sr6", "category": "slope_rate",
        "question": (
            "Ava uses (y₂ − y₁)/(x₂ − x₁) to find slope. Which table might represent her line?"
        ),
        "options": [
            "x: 1, 2, 4, 2  →  y: 4, 3, 4, 3",
            "x: 3, 4, 4, 3  →  y: 3, 4, 4, 3",
            "x: −1, −2, 2, 1  →  y: −2, −4, 4, 2",
            "x: 1, 2, 4, 2  →  y: 1, 2, 4, 2",
        ],
        "answer": 2,
        "explanation": "Consistent slope: (−4−(−2))/(−2−(−1)) = 2, (4−2)/(2−1) = 2.",
    },
    {
        "id": "u2_sr7", "category": "slope_rate",
        "question": (
            "A ladder leans against a wall. The graph shows ladder height vs feet from the wall. "
            "What is the slope of the graph?"
        ),
        "options": ["−5", "−4", "−20", "−24"],
        "answer": 0,
        "explanation": "Height drops 20 ft as base moves 4 ft → slope = −20/4 = −5.",
        "image": "practice_u2_ladder",
    },
    {
        "id": "u2_sr8", "category": "slope_rate",
        "question": "Which expression finds the slope of the linear function graphed?",
        "options": ["(2 − 0)/(0 − 2)", "(0 − 2)/(2 − 0)", "(−4 − 0)/(0 − 4)", "(−5 − 5)/(0 − 5)"],
        "answer": 1,
        "explanation": "Slope = (change in y)/(change in x) = (0 − 2)/(2 − 0) = −1.",
        "image": "practice_u2_slope_table",
    },
    {
        "id": "u2_sr9", "category": "slope_rate",
        "question": "Which statement about slope is correct?",
        "options": [
            "A line rising left to right has positive slope.",
            "A horizontal line has no slope.",
            "A line falling left to right has positive slope.",
            "A vertical line has slope zero.",
        ],
        "answer": 0,
        "explanation": "Upward left-to-right → positive slope.",
    },
    {
        "id": "u2_sr10", "category": "slope_rate",
        "question": (
            "The table shows y = 8 for every x-value. What describes the slope?"
        ),
        "options": ["No slope", "Positive slope", "Negative slope", "Zero slope"],
        "answer": 3,
        "explanation": "y never changes → horizontal line → slope = 0.",
    },
    # ── Y-intercept (8) ──
    {
        "id": "u2_yi1", "category": "y_intercept",
        "question": (
            "Maricella plots two points and extends the segment to both axes. "
            "Where is the y-intercept of the line?"
        ),
        "options": ["(0, −10)", "(0, −8)", "(0, −22)", "(0, 5)"],
        "answer": 0,
        "explanation": "The extended line crosses the y-axis at (0, −10).",
        "image": "practice_u2_maricella",
    },
    {
        "id": "u2_yi2", "category": "y_intercept",
        "question": (
            "A tip jar at a dry cleaners gains $2.75 each hour after opening. After 4 hours "
            "there is $15.50. How much was in the jar when the store opened?"
        ),
        "options": ["$4.50", "$1.25", "$1.15", "$2.15"],
        "answer": 0,
        "explanation": "Rate is $2.75 per hour. At 4 hours: $15.50 → start = 15.50 − 4(2.75) = $4.50.",
        "image": "practice_u2_tip_jar",
    },
    {
        "id": "u2_yi3", "category": "y_intercept",
        "question": (
            "Marco pumps gas at a steady rate. After 36 seconds there are 6 gallons; after "
            "48 seconds there are 8 gallons. What is the initial amount (at 0 seconds)?"
        ),
        "options": ["0 gallons", "2 gallons", "3 gallons", "6 gallons"],
        "answer": 0,
        "explanation": "Rate = 2 gal per 12 sec = 1/6 gal/sec. At 36 sec: 6 = start + 6 → start = 0.",
    },
    {
        "id": "u2_yi4", "category": "y_intercept",
        "question": (
            "Nate records distance vs time on a road trip. Distance increases 50 miles per hour. "
            "How can he find his starting distance (initial value)?"
        ),
        "options": [
            "Repeatedly subtract 50 from a distance value.",
            "Repeatedly add 50 to a time value.",
            "Repeatedly multiply by 50.",
            "Repeatedly divide time by 50.",
        ],
        "answer": 0,
        "explanation": "Work backward from any (time, distance) pair by subtracting 50 per hour.",
    },
    {
        "id": "u2_yi5", "category": "y_intercept",
        "question": "What is the y-intercept of the graph shown?",
        "options": ["(0, 4)", "(4, 0)", "(−1, 2)", "(−2, 0)"],
        "answer": 0,
        "explanation": "The line crosses the y-axis at (0, 4).",
        "image": "practice_u2_equation_graph",
    },
    {
        "id": "u2_yi6", "category": "y_intercept",
        "question": "What is the y-intercept of the linear equation x = −4, y = −6?",
        "options": ["0", "−4", "−6", "4"],
        "answer": 2,
        "explanation": "When x = 0, y = −6 → y-intercept is −6.",
    },
    {
        "id": "u2_yi7", "category": "y_intercept",
        "question": (
            "Four students graphed lines. Which student drew a line with y-intercept at −4?"
        ),
        "options": ["Ellis", "Braden", "Cameron", "Rhett"],
        "answer": 0,
        "explanation": "Ellis's line crosses the y-axis at −4.",
    },
    {
        "id": "u2_yi8", "category": "y_intercept",
        "question": (
            "Based on the graph, how do the y-intercept and slope compare?"
        ),
        "options": [
            "The y-intercept is 3, and the slope is ½.",
            "The y-intercept is ½, and the slope is 3.",
            "The y-intercept is 3, and the slope is 3.",
            "The y-intercept is ½, and the slope is ½.",
        ],
        "answer": 0,
        "explanation": "Line crosses y-axis at 3; rise 1.5 over run 3 → slope ½.",
        "image": "practice_u2_slope_table",
    },
    # ── Direct variation (8) ──
    {
        "id": "u2_dv1", "category": "direct_variation",
        "question": (
            "Li says a graph shows direct variation because it is a straight line. "
            "Why is Li incorrect?"
        ),
        "options": [
            "When x = 0, y is not 0 (line does not pass through the origin).",
            "The graph has no constant rate of change.",
            "The slope is negative.",
            "The relationship is not linear.",
        ],
        "answer": 0,
        "explanation": "Direct variation requires the line to pass through (0, 0).",
    },
    {
        "id": "u2_dv2", "category": "direct_variation",
        "question": "Which graph shows a direct variation?",
        "options": ["Graph A", "Graph B", "Graph C", "Graph D"],
        "answer": 2,
        "explanation": "Direct variation: straight line through the origin.",
        "image": "practice_u2_direct_graphs",
    },
    {
        "id": "u2_dv3", "category": "direct_variation",
        "question": "Which table represents a direct variation?",
        "options": ["Table A", "Table B", "Table C", "Table D"],
        "answer": 3,
        "explanation": "Table D: y/x is constant (3/3 = 1 for each pair).",
    },
    {
        "id": "u2_dv4", "category": "direct_variation",
        "question": (
            "Caleb earns $140 for 12 hours, $170 for 15 hours, $200 for 18 hours, and "
            "$230 for 21 hours. Does earnings vary directly with hours?"
        ),
        "options": [
            "No — earnings increase by $30 every 3 hours but ratios earnings/hours differ.",
            "Yes — he earns $10 per hour exactly.",
            "Yes — he earns $20 more than 10 times the hours.",
            "No — the earnings decrease over time.",
        ],
        "answer": 0,
        "explanation": "140/12 ≈ 11.67, 170/15 ≈ 11.33 — ratio not constant → not direct variation.",
    },
    {
        "id": "u2_dv5", "category": "direct_variation",
        "question": "Which representation shows a proportional relationship?",
        "options": ["Graph A (line through origin)", "Equation y = 2x + 2", "Graph C with y-intercept", "Table with unequal ratios"],
        "answer": 0,
        "explanation": "Proportional = direct variation = through (0, 0) with constant ratio.",
    },
    {
        "id": "u2_dv6", "category": "direct_variation",
        "question": (
            "The distance a baseball travels is proportional to swing speed. "
            "Which equation could model distance d (feet) and speed s (mph) if d = 5s?"
        ),
        "options": [
            "Yes — d/s = 5 for all points on the graph.",
            "No — there is a starting fee.",
            "No — the graph is curved.",
            "No — speed and distance are unrelated.",
        ],
        "answer": 0,
        "explanation": "d = 5s passes through origin with constant ratio 5.",
        "image": "practice_u2_baseball",
    },
    {
        "id": "u2_dv7", "category": "direct_variation",
        "question": "A line passes through (0, 0) and (4, 10). Is this direct variation?",
        "options": ["Yes — passes through the origin", "No — slope is not constant", "No — y-intercept is 10", "No — line is vertical"],
        "answer": 0,
        "explanation": "Through (0, 0) with constant slope → direct variation.",
    },
    {
        "id": "u2_dv8", "category": "direct_variation",
        "question": (
            "Which table shows y varying directly with x?"
        ),
        "options": [
            "x: 4, 6, 8  →  y: 4, 6, 8",
            "x: 4, 6, 8  →  y: 12, 18, 24",
            "x: 4, 6, 8  →  y: 7, 9, 11",
            "x: 4, 6, 8  →  y: 1, 3, 5",
        ],
        "answer": 1,
        "explanation": "y/x = 3 for every row → direct variation.",
    },
    # ── Special lines (8) ──
    {
        "id": "u2_sl1", "category": "special_lines",
        "question": (
            "Sanjay says a line with slope zero never touches the x-axis. "
            "Which graph proves he is wrong?"
        ),
        "options": ["y = 0 (horizontal on x-axis)", "x = 1 (vertical line)", "y = x", "y = −x"],
        "answer": 0,
        "explanation": "y = 0 has slope 0 and lies on the x-axis.",
    },
    {
        "id": "u2_sl2", "category": "special_lines",
        "question": (
            "A line passes through (9, 30) and (18, 30). Which statement is true?"
        ),
        "options": [
            "The slope is zero because the y-values do not change.",
            "The slope is undefined because the y-values do not change.",
            "The slope is zero because the x-values do not change.",
            "The line has no slope because x changes.",
        ],
        "answer": 0,
        "explanation": "y stays at 30 → horizontal → slope = 0.",
    },
    {
        "id": "u2_sl3", "category": "special_lines",
        "question": "Which equation represents a line with slope zero?",
        "options": ["y = 4", "y = −½x + ½", "x = −5", "y = 2x"],
        "answer": 0,
        "explanation": "y = 4 is horizontal → slope 0.",
    },
    {
        "id": "u2_sl4", "category": "special_lines",
        "question": "Which equation has an undefined slope?",
        "options": ["x = 0", "y = 0", "y = x", "y = −x"],
        "answer": 0,
        "explanation": "x = 0 is vertical → undefined slope.",
        "image": "practice_u2_vertical_line",
    },
    {
        "id": "u2_sl5", "category": "special_lines",
        "question": "Which line on the graph has slope zero?",
        "options": ["Line P", "Line Q", "Line R", "Line S"],
        "answer": 1,
        "explanation": "Line Q is horizontal → slope 0.",
        "image": "practice_u2_zero_lines",
    },
    {
        "id": "u2_sl6", "category": "special_lines",
        "question": "Which line on the graph has undefined slope?",
        "options": ["Line P", "Line Q", "Line R", "Line S"],
        "answer": 2,
        "explanation": "Line R is vertical → undefined slope.",
        "image": "practice_u2_vertical_line",
    },
    {
        "id": "u2_sl7", "category": "special_lines",
        "question": "A vertical line has which slope?",
        "options": ["Undefined", "Zero", "Positive", "Negative"],
        "answer": 0,
        "explanation": "Vertical lines have undefined slope (change in x = 0).",
    },
    {
        "id": "u2_sl8", "category": "special_lines",
        "question": "Which statement is correct?",
        "options": [
            "A horizontal line has slope zero.",
            "A vertical line has slope zero.",
            "A horizontal line has undefined slope.",
            "A rising line has negative slope.",
        ],
        "answer": 0,
        "explanation": "Horizontal → slope 0; vertical → undefined.",
    },
    # ── Writing equations (8) ──
    {
        "id": "u2_we1", "category": "writing_equations",
        "question": (
            "A line has slope −¾ and passes through (−5, 4). Which is the equation?"
        ),
        "options": ["y = −¾x − 2", "y = −¾x + 4", "y = −¾x + 1", "y = ¾x − 2"],
        "answer": 0,
        "explanation": "4 = −¾(−5) + b → 4 = 15/4 + b → b = −2.",
    },
    {
        "id": "u2_we2", "category": "writing_equations",
        "question": (
            "Which equation represents the linear function shown on the graph?"
        ),
        "options": ["y = ½x + 4", "y = 4x − 2", "y = −2x + 4", "y = 2x − 4"],
        "answer": 0,
        "explanation": "y-intercept 4, slope ½ → y = ½x + 4.",
        "image": "practice_u2_equation_graph",
    },
    {
        "id": "u2_we3", "category": "writing_equations",
        "question": (
            "A line passes through (2, −2) and (−6, 2). The point (a, −4) is on the line. "
            "What is a?"
        ),
        "options": ["6", "2", "−2", "−6"],
        "answer": 0,
        "explanation": "Slope = (2−(−2))/(−6−2) = −½. Using (2,−2): −4 = −½(a−2) → a = 6.",
    },
    {
        "id": "u2_we4", "category": "writing_equations",
        "question": "What are the slope m and y-intercept of the graphed line?",
        "options": [
            "m = 2, y-intercept (0, −4)",
            "m = ½, y-intercept (0, −4)",
            "m = 2, y-intercept (0, −2)",
            "m = −2, y-intercept (0, 4)",
        ],
        "answer": 0,
        "explanation": "Rise 2 per run 1 from (0,−4) → m = 2.",
        "image": "practice_u2_equation_graph",
    },
    {
        "id": "u2_we5", "category": "writing_equations",
        "question": "What is the x-intercept of the graph shown?",
        "options": ["(2, 0)", "(3, 0)", "(−3, 4)", "(0, 2)"],
        "answer": 0,
        "explanation": "The line crosses the x-axis at (2, 0).",
        "image": "practice_u2_equation_graph",
    },
    {
        "id": "u2_we6", "category": "writing_equations",
        "question": (
            "Which expression finds the slope from the table: x = 0, 5, 9 and y = 4, 9, 13?"
        ),
        "options": ["(13 − 9)/(9 − 5)", "(9 − 4)/(9 − 0)", "(9 − 5)/(13 − 9)", "(4 − 0)/(9 − 0)"],
        "answer": 0,
        "explanation": "Slope = (13 − 9)/(9 − 5) = 4/4 = 1.",
    },
    {
        "id": "u2_we7", "category": "writing_equations",
        "question": "Write the equation of a line with slope 2 and y-intercept −3.",
        "options": ["y = 2x − 3", "y = −3x + 2", "y = 2x + 3", "y = −2x − 3"],
        "answer": 0,
        "explanation": "y = mx + b → y = 2x − 3.",
    },
    {
        "id": "u2_we8", "category": "writing_equations",
        "question": (
            "A line has equation y = −2x + 5. What is the y-value when x = 3?"
        ),
        "options": ["−1", "1", "11", "−6"],
        "answer": 0,
        "explanation": "y = −2(3) + 5 = −1.",
    },
    # ── Linear modeling (8) ──
    {
        "id": "u2_lm1", "category": "linear_modeling",
        "question": (
            "The Shake Shack sells small shakes for $3 and large shakes for $5. "
            "On Sunday, total revenue was $479. Which equation represents x small shakes "
            "and y large shakes sold?"
        ),
        "options": ["3x + 5y = 479", "5x + 3y = 479", "4x + 4y = 479", "479x + 479y = 15"],
        "answer": 0,
        "explanation": "$3 per small + $5 per large = $479 total.",
    },
    {
        "id": "u2_lm2", "category": "linear_modeling",
        "question": (
            "A snack stand sells popcorn bags and pretzels. The equation "
            "2.75x + 3.25y = 215 models total sales. Popcorn costs $2.75 and pretzels "
            "cost $3.25. What do x and y represent?"
        ),
        "options": [
            "x = popcorn bags sold, y = pretzels sold",
            "x = pretzels sold, y = popcorn bags sold",
            "x = dollars spent on popcorn, y = dollars on pretzels",
            "x = price of popcorn, y = price of pretzels",
        ],
        "answer": 0,
        "explanation": "Coefficients match item prices → x and y are quantities sold.",
    },
    {
        "id": "u2_lm3", "category": "linear_modeling",
        "question": (
            "Brenda's cell phone bill includes a flat fee plus an hourly charge. "
            "The graph shows hours used vs total bill. What is her hourly rate?"
        ),
        "options": ["$9 per hour", "$12 per hour", "$27 per hour", "$39 per hour"],
        "answer": 0,
        "explanation": "Bill rises $9 per hour after the starting fee → $9/hour.",
        "image": "practice_u2_brenda_phone",
    },
    {
        "id": "u2_lm4", "category": "linear_modeling",
        "question": (
            "Brenda's phone bill starts at $12 with no usage and increases $9 per hour. "
            "What is the total bill for 3 hours?"
        ),
        "options": ["$39", "$27", "$21", "$15"],
        "answer": 0,
        "explanation": "12 + 9(3) = $39.",
        "image": "practice_u2_brenda_phone",
    },
    {
        "id": "u2_lm5", "category": "linear_modeling",
        "question": (
            "A tip jar holds $4.50 when the dry cleaners opens and gains $2.75 each hour. "
            "How much is in the jar after 6 hours?"
        ),
        "options": ["$21.00", "$18.25", "$23.75", "$16.50"],
        "answer": 0,
        "explanation": "4.50 + 6(2.75) = 4.50 + 16.50 = $21.00.",
        "image": "practice_u2_tip_jar",
    },
    {
        "id": "u2_lm6", "category": "linear_modeling",
        "question": (
            "Pretzels cost 50 cents less than popcorn bags. Popcorn is $2.75 and pretzels "
            "are $3.25. Total sales were $215. Which setup is correct?"
        ),
        "options": [
            "2.75 × popcorn + 3.25 × pretzels = 215",
            "3.25 × popcorn + 2.75 × pretzels = 215",
            "Popcorn + pretzels = 215 with no prices",
            "2.75 + 3.25 = 215",
        ],
        "answer": 0,
        "explanation": "Match each price to its item count; total $215.",
    },
    {
        "id": "u2_lm7", "category": "linear_modeling",
        "question": (
            "Andrew's treadmill distance increases ⅙ mile per minute. "
            "How far does he run in 30 minutes?"
        ),
        "options": ["5 miles", "3 miles", "2.5 miles", "6 miles"],
        "answer": 0,
        "explanation": "⅙ × 30 = 5 miles.",
    },
    {
        "id": "u2_lm8", "category": "linear_modeling",
        "question": (
            "Wilson's can loses 0.5 gallon per second. How much water remains after 4 seconds "
            "if he started with 2.5 gallons?"
        ),
        "options": ["0.5 gallons", "0 gallons", "2.0 gallons", "1.5 gallons"],
        "answer": 0,
        "explanation": "2.5 − 4(0.5) = 0.5 gallons left.",
        "image": "practice_u2_wilson_can",
    },
]
