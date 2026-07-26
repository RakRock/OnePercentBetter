"""Edgenuity Course 3 Unit 6 — Systems of Linear Equations practice bank."""

from __future__ import annotations

UNIT6_CATEGORIES = {
    "graph_solutions": {
        "name": "Graphing & Solutions",
        "emoji": "📊",
        "color": "#3b82f6",
        "weight": 2,
    },
    "slope_intercept": {
        "name": "Slope-Intercept Form",
        "emoji": "📐",
        "color": "#8b5cf6",
        "weight": 1,
    },
    "word_problems": {
        "name": "Word Problems",
        "emoji": "🌍",
        "color": "#10b981",
        "weight": 2,
    },
    "number_of_solutions": {
        "name": "Number of Solutions",
        "emoji": "🔢",
        "color": "#f59e0b",
        "weight": 2,
    },
    "identify_graph": {
        "name": "Identify from Graph",
        "emoji": "🔍",
        "color": "#ef4444",
        "weight": 2,
    },
    "checking_solutions": {
        "name": "Checking Solutions",
        "emoji": "✅",
        "color": "#06b6d4",
        "weight": 2,
    },
}

UNIT6_CATEGORY_ACTIVITY = {
    "graph_solutions": "activity_1_graphing_solutions",
    "slope_intercept": "activity_2_slope_intercept",
    "word_problems": "activity_3_word_problems",
    "number_of_solutions": "activity_4_number_of_solutions",
    "identify_graph": "activity_5_identify_from_graph",
    "checking_solutions": "activity_6_checking_solutions",
}

UNIT6_REVISION_TIPS = {
    "graph_solutions": "The solution is the intersection point (x, y) where both equations are true.",
    "slope_intercept": "Solve for y: y = mx + b. Divide every term by the coefficient of y.",
    "word_problems": "Define variables, write one equation per sentence, then graph or solve.",
    "number_of_solutions": "Same slope + different intercept → parallel (0). Same line → infinite. Different slopes → one.",
    "identify_graph": "Match slope and intercept of each line to the equations in the system.",
    "checking_solutions": "Substitute x and y into BOTH equations. Both must be true for a system solution.",
}

UNIT6_QUESTION_BANK: list[dict] = [
    # ── Graphing & solutions (8) ──
    {
        "id": "u6_gs1", "category": "graph_solutions",
        "question": (
            "A graph shows y = ½x − 3. A table gives (−1, 1), (0, 0), (2, −2), (3, −3) for the second equation. "
            "What is the solution to the system?"
        ),
        "options": ["(1, −1)", "(−2, −4)", "(4, −4)", "(2, −2)"],
        "answer": 3,
        "explanation": "Second equation is y = −x. Solve ½x − 3 = −x → x = 2, y = −2.",
        "image": "practice_u6_graph_table",
    },
    {
        "id": "u6_gs2", "category": "graph_solutions",
        "question": "What is the solution to the graphed system (intersection at (−5, 1))?",
        "options": ["(−4, 3)", "(−5, 1)", "(3, −4)", "(1, −5)"],
        "answer": 1,
        "explanation": "The solution is the intersection point (−5, 1).",
        "image": "practice_u6_intersection",
    },
    {
        "id": "u6_gs3", "category": "graph_solutions",
        "question": "The system y = −½x + 4 and y = 2x − 1 is graphed. What is the solution?",
        "options": ["(4, −1)", "(−1, 4)", "(2, 3)", "(3, 2)"],
        "answer": 2,
        "explanation": "Lines cross at (2, 3).",
    },
    {
        "id": "u6_gs4", "category": "graph_solutions",
        "question": "The system y = 2x + 5 and y = −3x − 15 is graphed. What is the solution?",
        "options": ["(−3, −4)", "(−4, −3)", "(5, −5)", "(−5, 5)"],
        "answer": 1,
        "explanation": "Solve 2x + 5 = −3x − 15 → x = −4, y = −3.",
        "image": "practice_u6_system_neg",
    },
    {
        "id": "u6_gs5", "category": "graph_solutions",
        "question": "y = ¾x − 4 and y = −x + 3 are graphed. What is the solution?",
        "options": ["(−1, 4)", "(4, −1)", "(1, 4)", "(4, 1)"],
        "answer": 1,
        "explanation": "Intersection at (4, −1).",
    },
    {
        "id": "u6_gs6", "category": "graph_solutions",
        "question": (
            "Adam mixes fertilizer: y = ¼x and x + y = 10 (x = water cups, y = concentrate cups). "
            "What is the solution?"
        ),
        "options": ["(4, 6)", "(0, 2.5)", "(5, 5)", "(8, 2)"],
        "answer": 3,
        "explanation": "Substitute y = x/4 into x + y = 10 → x = 8, y = 2.",
        "image": "practice_u6_fertilizer",
    },
    {
        "id": "u6_gs7", "category": "graph_solutions",
        "question": "A number equals 3 times a smaller number; smaller + 4 equals the larger. Graph shows lines crossing at (2, 6). Which system matches?",
        "options": [
            "y = ⅓x and y = x + 4",
            "y = 3x and y = x + 4",
            "y = 3x and y = x − 4",
            "y = ⅓x and y = x − 4",
        ],
        "answer": 1,
        "explanation": "Larger y = 3x; y = x + 4. Intersection (2, 6).",
        "image": "practice_u6_word_graph",
    },
    {
        "id": "u6_gs8", "category": "graph_solutions",
        "question": "The equation y = ½x + 4 is graphed. Which equation intersects it at (4, 6)?",
        "options": ["y = 4", "y = 6x", "y = 6", "y = 4x"],
        "answer": 2,
        "explanation": "At x = 4, y = 6 is a horizontal line through (4, 6).",
    },
    # ── Slope-intercept form (7) ──
    {
        "id": "u6_si1", "category": "slope_intercept",
        "question": "5x − 2y = 10 written in slope-intercept form is —",
        "options": ["y = 5/2 x + 10", "y = −5x − 5", "y = −5/2 x + 10", "y = 5/2 x − 5"],
        "answer": 3,
        "explanation": "−2y = −5x + 10 → y = 5/2 x − 5.",
    },
    {
        "id": "u6_si2", "category": "slope_intercept",
        "question": "Which equation is in slope-intercept form?",
        "options": ["3y = 8x − 5", "y = 3x − 2", "x = ½y + 8", "2x + 5y = 12"],
        "answer": 1,
        "explanation": "y = mx + b form has y isolated on the left.",
    },
    {
        "id": "u6_si3", "category": "slope_intercept",
        "question": "2x − 3y = 12 in slope-intercept form is —",
        "options": ["y = −3/2 x + 4", "y = 2/3 x − 4", "y = 3/2 x − 4", "y = −2/3 x + 4"],
        "answer": 1,
        "explanation": "−3y = −2x + 12 → y = 2/3 x − 4.",
    },
    {
        "id": "u6_si4", "category": "slope_intercept",
        "question": "10(x + 3/5) = 2y solved for y gives —",
        "options": ["y = 5x + 3", "y = ½x + 6", "y = ⅕x + 3/25", "y = 5x + 3/10"],
        "answer": 0,
        "explanation": "2y = 10x + 6 → y = 5x + 3.",
    },
    {
        "id": "u6_si5", "category": "slope_intercept",
        "question": "Which is the first equation 5x − 2y = 10 in slope-intercept form?",
        "options": ["y = −5/2 x + 5", "y = 5/2 x − 5", "y = 5x − 2", "y = −2x + 5"],
        "answer": 1,
        "explanation": "Divide by −2: y = 5/2 x − 5.",
    },
    {
        "id": "u6_si6", "category": "slope_intercept",
        "question": "4x − 5y = 5 solved for y gives —",
        "options": ["y = 4/5 x − 1", "y = −4/5 x + 1", "y = 4/5 x + 1", "y = 5/4 x − 1"],
        "answer": 0,
        "explanation": "−5y = −4x + 5 → y = 4/5 x − 1.",
    },
    {
        "id": "u6_si7", "category": "slope_intercept",
        "question": "To graph 2x − 3y = 12, the best slope-intercept form is —",
        "options": ["y = 2/3 x − 4", "y = −2/3 x + 4", "x = 3/2 y + 6", "y = 3/2 x − 4"],
        "answer": 0,
        "explanation": "y = 2/3 x − 4 has slope 2/3 and intercept −4.",
    },
    # ── Word problems (8) ──
    {
        "id": "u6_wp1", "category": "word_problems",
        "question": (
            "4 times a smaller number plus 3 times a larger is 31. "
            "Larger minus 7 equals twice the smaller (x = smaller, y = larger). Which system?"
        ),
        "options": [
            "y = −4/3 x + 31, y = −2x + 7",
            "y = −4/3 x + 31/3, y = 2x + 7",
            "y = −4/3 x + 31, y = 2x + 7",
            "y = −4/3 x + 31/3, y = −2x + 7",
        ],
        "answer": 1,
        "explanation": "4x + 3y = 31 and y − 7 = 2x → y = 2x + 7.",
    },
    {
        "id": "u6_wp2", "category": "word_problems",
        "question": (
            "Aisha bought 15 apples and oranges for $9.00. Oranges $0.50, apples $0.65. "
            "x = oranges, y = apples. Which system?"
        ),
        "options": [
            "x = y, 0.5x + 0.65y = 15",
            "x + y = 15, 0.5x + 0.65y = 9",
            "x = y, 0.5x + 0.65y = 9",
            "x + y = 9, 0.5x + 0.65y = 15",
        ],
        "answer": 1,
        "explanation": "Count: x + y = 15. Cost: 0.5x + 0.65y = 9.",
    },
    {
        "id": "u6_wp3", "category": "word_problems",
        "question": "Anthony bought 6 fruit bars and 3 chocolate-nut bars for $4.12: 6x + 3y = 4.12. What is x?",
        "options": [
            "Number of fruit bars",
            "Cost of a fruit bar",
            "Number of chocolate-nut bars",
            "Cost of a chocolate-nut bar",
        ],
        "answer": 1,
        "explanation": "x represents the cost of one fruit bar.",
    },
    {
        "id": "u6_wp4", "category": "word_problems",
        "question": "Audra wrote 0.10x + 0.25y = 5.30 for dimes and quarters. What is x?",
        "options": ["Value of a quarter", "Value of a dime", "Number of quarters", "Number of dimes"],
        "answer": 3,
        "explanation": "x = number of dimes (worth $0.10 each).",
    },
    {
        "id": "u6_wp5", "category": "word_problems",
        "question": (
            "Twice a larger number plus a smaller is 5; 5 times smaller minus larger is 3. "
            "Which system (x = smaller, y = larger)?"
        ),
        "options": [
            "2x + y = 5, x − 5y = 3",
            "2y + x = 5, 5x − y = 3",
            "2x + y = 5, 5y − x = 3",
            "2y + x = 5, y − 5x = 3",
        ],
        "answer": 1,
        "explanation": "2y + x = 5 and 5x − y = 3.",
    },
    {
        "id": "u6_wp6", "category": "word_problems",
        "question": (
            "Sum of twice a number and a larger number is 145; difference is 55 (x smaller, y larger). "
            "Which three equations could apply?"
        ),
        "options": [
            "x − y = 55 only",
            "y − x = 55, y = x + 55, and 2x + y = 145",
            "2(x + y) = 145 only",
            "x + y = 145 only",
        ],
        "answer": 1,
        "explanation": "2x + y = 145, y − x = 55, and y = x + 55 all describe the situation.",
    },
    {
        "id": "u6_wp7", "category": "word_problems",
        "question": (
            "Kedwin: unlimited online movies $10/month vs renting 5 movies for $4. "
            "How many movies per month makes online cheaper?"
        ),
        "options": ["10.40", "12.5", "10", "13"],
        "answer": 3,
        "explanation": "Rental cost = 0.8x. Online wins when 0.8x > 10 → x > 12.5, so 13+.",
        "image": "practice_u6_movie",
    },
    {
        "id": "u6_wp8", "category": "word_problems",
        "question": "First number = half of second + 3; first = quarter of second + 5. Which system (x = second)?",
        "options": [
            "y = 2x + 3, y = 4x + 5",
            "y = 3x + 2, y = 5x + 4",
            "y = ½x + 3, y = ¼x + 5",
            "y = 3x + ½, y = 5x + ¼",
        ],
        "answer": 2,
        "explanation": "y = ½x + 3 and y = ¼x + 5; intersection at (8, 7).",
    },
    # ── Number of solutions (8) ──
    {
        "id": "u6_ns1", "category": "number_of_solutions",
        "question": "y = −3x + 5 and y = −3x − 6 are graphed. How many solutions?",
        "options": ["0", "1", "2", "Infinitely many"],
        "answer": 0,
        "explanation": "Same slope, different intercepts → parallel → no solution.",
        "image": "practice_u6_parallel",
    },
    {
        "id": "u6_ns2", "category": "number_of_solutions",
        "question": "Which equation paired with y = −2x − 8 gives infinitely many solutions?",
        "options": ["y = −(2x + 8)", "y = −(−2x + 8)", "y = −2(x − 4)", "y = −2(x − 8)"],
        "answer": 0,
        "explanation": "y = −(2x + 8) = −2x − 8, the same line.",
    },
    {
        "id": "u6_ns3", "category": "number_of_solutions",
        "question": "y = 2(x + 4) and y = 2x + 8. How many solutions?",
        "options": ["No solution", "Infinitely many", "One unique", "Two"],
        "answer": 1,
        "explanation": "Both simplify to y = 2x + 8 → same line.",
    },
    {
        "id": "u6_ns4", "category": "number_of_solutions",
        "question": "y = −2(x + 3) and y = −2x + 3. Trang says no solution. Is he correct?",
        "options": [
            "No — same slope, different intercepts",
            "Yes — same slope and intercept",
            "No — same slope and intercept",
            "Yes — same slope, different intercepts",
        ],
        "answer": 3,
        "explanation": "Slopes both −2; intercepts −6 vs +3 → parallel → no solution.",
    },
    {
        "id": "u6_ns5", "category": "number_of_solutions",
        "question": "y = −3(x + 2) and y = −3x − 6. Why is only one line graphed?",
        "options": [
            "Same slope and intercept → infinitely many solutions",
            "Same slope, different intercepts → no solution",
            "Different slopes → one solution",
            "Different slopes → no solution",
        ],
        "answer": 0,
        "explanation": "Both are y = −3x − 6 → coincident lines.",
    },
    {
        "id": "u6_ns6", "category": "number_of_solutions",
        "question": "y = 3x + 5 and y = 3x + 8. How many solutions?",
        "options": ["No solution", "One unique", "Infinitely many", "Two"],
        "answer": 0,
        "explanation": "Parallel lines never meet.",
    },
    {
        "id": "u6_ns7", "category": "number_of_solutions",
        "question": "y = −5x + 1 and y = −5x + 10 never meet. Why are they parallel?",
        "options": [
            "Different slopes, same intercept",
            "Different slopes and intercepts",
            "Same slope, different intercepts",
            "Same slope and intercept",
        ],
        "answer": 2,
        "explanation": "Equal slopes (−5) and different y-intercepts → parallel.",
    },
    {
        "id": "u6_ns8", "category": "number_of_solutions",
        "question": "Two lines with different slopes on a graph will —",
        "options": [
            "Intersect exactly once",
            "Never intersect",
            "Always overlap",
            "Intersect twice",
        ],
        "answer": 0,
        "explanation": "Different slopes → one intersection point.",
    },
    # ── Identify from graph (7) ──
    {
        "id": "u6_ig1", "category": "identify_graph",
        "question": "Four lines are graphed. Which system has solution ≈ (−0.3, 1.4)?",
        "options": [
            "2x − y = −2 and 3x + 2y = 5",
            "4x − y = 2 and 22x + 10y = 7",
            "3x + 2y = 5 and 4x − y = 2",
            "2x − y = −2 and 22x + 10y = 7",
        ],
        "answer": 3,
        "explanation": "The red and purple lines cross near (−0.3, 1.4).",
        "image": "practice_u6_four_lines",
    },
    {
        "id": "u6_ig2", "category": "identify_graph",
        "question": "Which system has solution ≈ (−2.7, −1.2)?",
        "options": [
            "4x − 5y = 5 and 3x + 10y = 20",
            "4x − 5y = −5 and 3x + 10y = −20",
            "4x − 5y = −5 and 3x + 10y = 20",
            "4x − 5y = 5 and 3x + 10y = −20",
        ],
        "answer": 1,
        "explanation": "Match the intersection in the third quadrant.",
    },
    {
        "id": "u6_ig3", "category": "identify_graph",
        "question": "What system is shown on the graph (one line slope −2, y-int −4; other slope ½, y-int −2)?",
        "options": [
            "x − 2y = −4 and 2x + y = 4",
            "x − 2y = −2 and 2x + y = −4",
            "x − 2y = 2 and 2x + y = 4",
            "x − 2y = 4 and 2x + y = −4",
        ],
        "answer": 3,
        "explanation": "x − 2y = 4 and 2x + y = −4 match the graphed lines.",
    },
    {
        "id": "u6_ig4", "category": "identify_graph",
        "question": "Which graph shows 4x + y = 3 and 2x − 3y = 3?",
        "options": [
            "Two lines crossing in quadrant IV near (0.9, −0.4)",
            "Two parallel lines",
            "A single line only",
            "Two lines crossing at (3, 0)",
        ],
        "answer": 0,
        "explanation": "The system intersects once in quadrant IV.",
    },
    {
        "id": "u6_ig5", "category": "identify_graph",
        "question": "Lines with different slopes that extend toward each other have —",
        "options": [
            "One solution because they will eventually intersect",
            "One solution because they never intersect",
            "No solution because they never intersect",
            "No solution because they intersect",
        ],
        "answer": 0,
        "explanation": "Different slopes → lines cross at exactly one point.",
    },
    {
        "id": "u6_ig6", "category": "identify_graph",
        "question": "Which ordered pair is a solution to −4x + y = 8 and x − 5y = 17?",
        "options": ["(−3, 4)", "(−3, −4)", "(−4, 3)", "(−4, −3)"],
        "answer": 1,
        "explanation": "Check: −4(−3) + (−4) = 8 and −3 − 5(−4) = 17.",
    },
    {
        "id": "u6_ig7", "category": "identify_graph",
        "question": "Which system matches a graph with lines y = 3x and y = x + 4?",
        "options": [
            "y = 3x, y = x − 4",
            "y = 3x, y = x + 4",
            "y = x/3, y = x + 4",
            "y = 3x, y = 4x + 1",
        ],
        "answer": 1,
        "explanation": "Steeper line through origin (y = 3x) and y = x + 4.",
        "image": "practice_u6_word_graph",
    },
    # ── Checking solutions (7) ──
    {
        "id": "u6_cs1", "category": "checking_solutions",
        "question": "Dimitri checks (2, −2) in 7x + 9y = −4 and 5x − 2y = 6. Where is his error?",
        "options": [
            "Checked first equation when he should check second first",
            "Error substituting into 5x − 2y = 6 (wrote 10 − 4 instead of 10 + 4)",
            "Error in 7x + 9y = −4",
            "Mixed up x and y coordinates",
        ],
        "answer": 1,
        "explanation": "5(2) − 2(−2) = 10 + 4 = 14, not 6. (2, −2) is not a solution.",
    },
    {
        "id": "u6_cs2", "category": "checking_solutions",
        "question": "Betty says (−3, 5) is a solution to 6x + 5y = 7 and x + 4y = 17. Which is true?",
        "options": [
            "Satisfies x + 4y = 17 only",
            "Satisfies 6x + 5y = 7 only",
            "Satisfies both equations",
            "Satisfies neither",
        ],
        "answer": 2,
        "explanation": "Both equations are true when x = −3, y = 5.",
    },
    {
        "id": "u6_cs3", "category": "checking_solutions",
        "question": "Is (1, 2) a solution to 2x + 3y = 8 and 3x + y = −2?",
        "options": [
            "Yes — satisfies both",
            "No — fails 3x + y = −2",
            "No — fails both",
            "Yes — satisfies 2x + 3y = 8 only",
        ],
        "answer": 1,
        "explanation": "3(1) + 2 = 5 ≠ −2, so (1, 2) is not a solution.",
    },
    {
        "id": "u6_cs4", "category": "checking_solutions",
        "question": "To verify (−3, 5) is a solution, you must —",
        "options": [
            "Substitute into both equations",
            "Substitute into one equation only",
            "Graph one line only",
            "Add the two equations",
        ],
        "answer": 0,
        "explanation": "Both equations must be true at the same (x, y).",
    },
    {
        "id": "u6_cs5", "category": "checking_solutions",
        "question": "Check (2, −2) in x − 2y = 6. Is it true?",
        "options": ["Yes: 2 − 2(−2) = 6", "No: 2 − 2(−2) = −2", "Yes: 2 + 2 = 6", "No: 2 + (−2) = 0"],
        "answer": 0,
        "explanation": "2 + 4 = 6 ✓",
    },
    {
        "id": "u6_cs6", "category": "checking_solutions",
        "question": "(2, −2) satisfies 7x + 9y = −4. Does it satisfy 5x − 2y = 6?",
        "options": ["Yes", "No — gives 14, not 6", "Cannot tell", "Yes — gives 6"],
        "answer": 1,
        "explanation": "5(2) − 2(−2) = 14 ≠ 6.",
    },
    {
        "id": "u6_cs7", "category": "checking_solutions",
        "question": "A point is a system solution when —",
        "options": [
            "It makes both equations true",
            "It makes one equation true",
            "It is on the x-axis",
            "It has integer coordinates",
        ],
        "answer": 0,
        "explanation": "System solution = intersection = both equations satisfied.",
    },
]
