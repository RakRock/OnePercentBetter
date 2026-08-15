"""Arjun Course 3 Unit 2 — Equations & Linear Relationships practice bank."""

from __future__ import annotations

UNIT2_CATEGORIES = {
    "expressions": {"name": "Expressions & Patterns", "emoji": "✏️", "color": "#3b82f6", "weight": 1},
    "solving_equations": {"name": "Solving Equations", "emoji": "⚖️", "color": "#8b5cf6", "weight": 2},
    "slope": {"name": "Slope & Rate", "emoji": "📈", "color": "#10b981", "weight": 2},
    "slope_intercept": {"name": "Slope-Intercept", "emoji": "📊", "color": "#f59e0b", "weight": 1},
    "proportional": {"name": "Proportional", "emoji": "🔗", "color": "#06b6d4", "weight": 1},
    "systems": {"name": "Systems", "emoji": "✖️", "color": "#ef4444", "weight": 2},
}

UNIT2_CATEGORY_ACTIVITY = {
    "expressions": "activity_9_writing_expressions",
    "solving_equations": "activity_10_solving_equations",
    "slope": "activity_11_exploring_slope",
    "slope_intercept": "activity_12_slope_intercept_form",
    "proportional": "activity_13_proportional_relationships",
    "systems": "activity_14_graphing_systems",
}

UNIT2_REVISION_TIPS = {
    "expressions": "Find constant difference or ratio; substitute n into your expression.",
    "solving_equations": "Undo operations in reverse order; check for no solution or infinitely many.",
    "slope": "Slope = change in y ÷ change in x.",
    "slope_intercept": "y = mx + b: m is rate, b is starting value.",
    "proportional": "Proportional means through (0,0) with constant y/x ratio.",
    "systems": "Solution is where lines intersect; parallel lines → no solution.",
}

UNIT2_QUESTION_BANK: list[dict] = [
    {
        "id": "u2_ex1", "category": "expressions",
        "question": "A square number is a number you get when you multiply a whole number by itself. What is the 6th square number?",
        "options": ["30", "36", "42", "49"], "answer": 1,
        "explanation": "The 6th square number is 6 × 6 = 36.",
    },
    {
        "id": "u2_ex2", "category": "expressions",
        "question": (
            "A dot pattern has perimeters 4, 6, 8, … for figures 1, 2, 3, … "
            "Each new figure adds 2 to the perimeter. Which expression gives the perimeter of figure n?"
        ),
        "options": ["2n", "2n + 2", "4n", "n + 4"], "answer": 1,
        "explanation": "Figure 1 has perimeter 4, and each step adds 2 → 2n + 2.",
    },
    {
        "id": "u2_ex3", "category": "expressions",
        "question": (
            "An area pattern follows 1, 5, 9, 13, … (add 4 each time). "
            "Using the rule 4n − 3, what is the area of figure 35?"
        ),
        "options": ["137", "141", "135", "139"], "answer": 0,
        "explanation": "4(35) − 3 = 140 − 3 = 137.",
    },
    {
        "id": "u2_ex4", "category": "expressions",
        "question": (
            "Triangular numbers are built from rows of dots: 1, 3, 6, 10, … "
            "The formula is n(n + 1)/2. What is the 8th triangular number?"
        ),
        "options": ["28", "36", "45", "32"], "answer": 1,
        "explanation": "8(9)/2 = 72/2 = 36.",
    },
    {
        "id": "u2_ex5", "category": "expressions",
        "question": (
            "A tile pattern uses the rule 4 + 5(n − 1) tiles for figure n. "
            "How many tiles are in figure 6?"
        ),
        "options": ["24", "29", "34", "25"], "answer": 1,
        "explanation": "4 + 5(6 − 1) = 4 + 25 = 29.",
    },
    {
        "id": "u2_eq1", "category": "solving_equations",
        "question": "Solve for x: 3x + 4 = 16.",
        "options": ["x = 3", "x = 4", "x = 5", "x = 6"], "answer": 1,
        "explanation": "Subtract 4: 3x = 12. Divide by 3: x = 4.",
    },
    {
        "id": "u2_eq2", "category": "solving_equations",
        "question": "Solve for x: 5x + 2 = 2x + 11.",
        "options": ["x = 3", "x = 4", "x = 9", "x = 13"], "answer": 0,
        "explanation": "Subtract 2x: 3x + 2 = 11. Subtract 2: 3x = 9 → x = 3.",
    },
    {
        "id": "u2_eq3", "category": "solving_equations",
        "question": "Solve for x: 2x + 1 = 2x + 5.",
        "options": ["x = 2", "x = 0", "No solution", "Infinitely many"], "answer": 2,
        "explanation": "Subtract 2x from both sides: 1 = 5, which is never true → no solution.",
    },
    {
        "id": "u2_eq4", "category": "solving_equations",
        "question": "Solve for x: 2(x + 3) = 2x + 6.",
        "options": ["x = 0", "No solution", "Infinitely many solutions", "x = 3"], "answer": 2,
        "explanation": "Expand: 2x + 6 = 2x + 6. Both sides match for every x → infinitely many solutions.",
    },
    {
        "id": "u2_eq5", "category": "solving_equations",
        "question": "Solve for x: −3x + 11 = 26.",
        "options": ["x = 5", "x = −5", "x = 15", "x = −15"], "answer": 1,
        "explanation": "Subtract 11: −3x = 15. Divide by −3: x = −5.",
    },
    {
        "id": "u2_eq6", "category": "solving_equations",
        "question": (
            "A triangle has area A = ½bh. If the area is 126 square feet and the base b is 12 feet, "
            "what is the height h?"
        ),
        "options": ["10 ft", "21 ft", "42 ft", "18 ft"], "answer": 1,
        "explanation": "126 = ½(12)h = 6h → h = 21 ft.",
    },
    {
        "id": "u2_sl1", "category": "slope",
        "question": "What is the slope of the line that passes through the points (2, 3) and (6, 11)?",
        "options": ["1", "2", "4", "8"], "answer": 1,
        "explanation": "Slope = (11 − 3)/(6 − 2) = 8/4 = 2.",
    },
    {
        "id": "u2_sl2", "category": "slope",
        "question": "A car travels 30 miles in 2 hours at a constant speed. What is the rate in miles per hour?",
        "options": ["10", "15", "20", "60"], "answer": 1,
        "explanation": "30 ÷ 2 = 15 miles per hour.",
    },
    {
        "id": "u2_sl3", "category": "slope",
        "question": (
            "A table shows x-values 0, 3, 6 and matching y-values 1, 7, 13. "
            "What is the slope (rate of change) of this linear relationship?"
        ),
        "options": ["1", "2", "3", "6"], "answer": 1,
        "explanation": "From (0,1) to (3,7): change in y is 6, change in x is 3 → slope = 2.",
    },
    {
        "id": "u2_sl4", "category": "slope",
        "question": (
            "A train travels 84 miles in 4 hours at a constant rate. "
            "How far will it travel in 7 hours at the same rate?"
        ),
        "options": ["126 mi", "147 mi", "168 mi", "21 mi"], "answer": 1,
        "explanation": "Rate = 84/4 = 21 mi/hr. In 7 hours: 21 × 7 = 147 miles.",
    },
    {
        "id": "u2_sl5", "category": "slope",
        "question": (
            "A car gets 64 miles on 2 gallons of gas at a constant rate. "
            "How many miles can it drive on 12 gallons?"
        ),
        "options": ["320", "384", "768", "128"], "answer": 1,
        "explanation": "32 miles per gallon × 12 gallons = 384 miles.",
    },
    {
        "id": "u2_si1", "category": "slope_intercept",
        "question": "In the equation y = −3x + 7, what are the slope m and the y-intercept b?",
        "options": ["m=3, b=7", "m=−3, b=7", "m=−3, b=−7", "m=7, b=−3"], "answer": 1,
        "explanation": "In y = mx + b, m = −3 and b = 7.",
    },
    {
        "id": "u2_si2", "category": "slope_intercept",
        "question": (
            "A town had 1,000 bells in 2003 and adds 2,000 bells each year after that. "
            "Let t be years since 2003 and N the total bells. Which equation models this?"
        ),
        "options": ["N = 1000t", "N = 2000t + 1000", "N = 2000t", "N = t + 2000"], "answer": 1,
        "explanation": "Start at 1,000 and increase by 2,000 per year → N = 2000t + 1000.",
    },
    {
        "id": "u2_si3", "category": "slope_intercept",
        "question": (
            "A bottle leaks according to y = −3x + 24, where y is milliliters left and x is seconds. "
            "What does the slope −3 mean?"
        ),
        "options": ["Starts with 24 mL", "Loses 3 mL per second", "Gains 3 mL per second", "24 mL total leak"],
        "answer": 1,
        "explanation": "The slope is the rate of change: the bottle loses 3 mL each second.",
    },
    {
        "id": "u2_si4", "category": "slope_intercept",
        "question": (
            "A line with slope −2 passes through (3, 5) and also through (−2, p). What is p?"
        ),
        "options": ["10", "15", "5", "−5"], "answer": 1,
        "explanation": "Moving 5 left in x (from 3 to −2) adds 10 to y → 5 + 10 = 15.",
    },
    {
        "id": "u2_si5", "category": "slope_intercept",
        "question": (
            "A gym charges $15 per day plus a one-time $8 sign-up fee. "
            "Write an equation for total cost y after x days."
        ),
        "options": ["y = 15x", "y = 15x + 8", "y = 8x + 15", "y = 23x"], "answer": 1,
        "explanation": "$15 per day plus flat $8 → y = 15x + 8.",
    },
    {
        "id": "u2_pr1", "category": "proportional",
        "question": (
            "A table shows x: 2, 4, 6 and y: 7, 14, 21. "
            "Is this a proportional relationship (y/x always the same)?"
        ),
        "options": ["Yes, k=3.5", "No", "Yes, k=7", "Yes, k=2"], "answer": 0,
        "explanation": "7/2 = 14/4 = 21/6 = 3.5 → yes, constant of proportionality k = 3.5.",
    },
    {
        "id": "u2_pr2", "category": "proportional",
        "question": "Is the equation y = 4x + 1 a proportional relationship?",
        "options": ["Yes", "No — not through origin", "Yes, k=4", "Only for x>0"], "answer": 1,
        "explanation": "Proportional graphs pass through (0, 0). The +1 means this line does not.",
    },
    {
        "id": "u2_pr3", "category": "proportional",
        "question": (
            "A car drives 330 miles in 5.5 hours at a constant speed. "
            "How many hours will it take to drive 720 miles at the same speed?"
        ),
        "options": ["10 hr", "12 hr", "14 hr", "11 hr"], "answer": 1,
        "explanation": "Speed = 330/5.5 = 60 mi/hr. Time = 720/60 = 12 hours.",
    },
    {
        "id": "u2_pr4", "category": "proportional",
        "question": (
            "A fair charges $5 entry plus $0.75 per ride. "
            "Is the total cost proportional to the number of rides?"
        ),
        "options": ["Yes", "No — flat fee", "Yes, k=0.75", "Only after 5 rides"], "answer": 1,
        "explanation": "The $5 entry fee is not per ride, so total cost is not proportional to rides alone.",
    },
    {
        "id": "u2_pr5", "category": "proportional",
        "question": (
            "You type at a constant rate of 25 words per minute, starting from 0 words. "
            "Which equation gives total words w after t minutes?"
        ),
        "options": ["w = 25 + t", "w = 25t", "w = t/25", "w = 25/t"], "answer": 1,
        "explanation": "Through the origin at 25 words per minute → w = 25t.",
    },
    {
        "id": "u2_sy1", "category": "systems",
        "question": "Where do the lines y = x + 1 and y = −x + 5 intersect?",
        "options": ["(2, 3)", "(3, 2)", "(1, 5)", "(5, 1)"], "answer": 0,
        "explanation": "Set equal: x + 1 = −x + 5 → 2x = 4 → x = 2, y = 3.",
    },
    {
        "id": "u2_sy2", "category": "systems",
        "question": "How many solutions does the system y = 3x + 2 and y = 3x − 1 have?",
        "options": ["One", "None (parallel)", "Infinitely many", "Two"], "answer": 1,
        "explanation": "Same slope (3) but different y-intercepts → parallel lines, no intersection.",
    },
    {
        "id": "u2_sy3", "category": "systems",
        "question": "Where do the lines y = −2x + 4 and y = ½x − 1 intersect?",
        "options": ["(2, 0)", "(0, 2)", "(4, 0)", "(1, 2)"], "answer": 0,
        "explanation": "−2x + 4 = ½x − 1 → 5 = 2.5x → x = 2, y = 0.",
    },
    {
        "id": "u2_sy4", "category": "systems",
        "question": (
            "Job J pays J = 5W + 5 and job B pays B = 4W + 12, where W is hours worked. "
            "After how many hours W do both jobs pay the same amount?"
        ),
        "options": ["5", "7", "10", "12"], "answer": 1,
        "explanation": "5W + 5 = 4W + 12 → W = 7.",
    },
    {
        "id": "u2_sy5", "category": "systems",
        "question": "Solve the system: x + y = 7 and 3x − y = 5.",
        "options": ["(3, 4)", "(4, 3)", "(2, 5)", "(5, 2)"], "answer": 0,
        "explanation": "Add equations: 4x = 12 → x = 3, then y = 4.",
    },
    {
        "id": "u2_sy6", "category": "systems",
        "question": (
            "You buy 10 tickets total: child tickets cost $8 and adult tickets cost $12. "
            "The total cost is $100. How many child tickets did you buy?"
        ),
        "options": ["4", "5", "6", "8"], "answer": 1,
        "explanation": "5 child ($40) + 5 adult ($60) = $100.",
    },
]
