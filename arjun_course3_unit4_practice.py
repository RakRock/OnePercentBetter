"""Arjun Course 3 Unit 4 — Functions practice bank."""

from __future__ import annotations

UNIT4_CATEGORIES = {
    "function_basics": {"name": "Functions", "emoji": "🔀", "color": "#3b82f6", "weight": 2},
    "comparing_functions": {"name": "Comparing Functions", "emoji": "⚖️", "color": "#8b5cf6", "weight": 1},
    "constructing": {"name": "Constructing Functions", "emoji": "🏗️", "color": "#10b981", "weight": 1},
    "linear_functions": {"name": "Linear Functions", "emoji": "📈", "color": "#f59e0b", "weight": 2},
    "linear_nonlinear": {"name": "Linear vs Nonlinear", "emoji": "📊", "color": "#ef4444", "weight": 1},
}

UNIT4_CATEGORY_ACTIVITY = {
    "function_basics": "activity_27_introduction_to_functions",
    "comparing_functions": "activity_28_comparing_functions",
    "constructing": "activity_29_constructing_functions",
    "linear_functions": "activity_30_linear_functions",
    "linear_nonlinear": "activity_31_linear_nonlinear_functions",
}

UNIT4_REVISION_TIPS = {
    "function_basics": "Each input must have exactly one output.",
    "comparing_functions": "Slope = rate; y-intercept = starting value.",
    "constructing": "Find initial value + constant rate from tables.",
    "linear_functions": "Linear data has constant rate of change.",
    "linear_nonlinear": "Straight-line pattern vs curve or changing rate.",
}

UNIT4_QUESTION_BANK: list[dict] = [
    {
        "id": "u4_fn1", "category": "function_basics",
        "question": "Use the function y = 2x + 4. What is y when x = 3?",
        "options": ["10", "12", "8", "14"], "answer": 0,
        "explanation": "2(3) + 4 = 6 + 4 = 10.",
    },
    {
        "id": "u4_fn2", "category": "function_basics",
        "question": (
            "A relation lists pairs (−2, 2), (−3, 4), and (−2, 6). "
            "Is this relation a function?"
        ),
        "options": [
            "Yes — it is a function",
            "No — the input −2 is used twice with different outputs",
            "Yes, but only for positive x-values",
            "Cannot tell",
        ], "answer": 1,
        "explanation": "Input −2 has two different outputs (2 and 6), so it is not a function.",
    },
    {
        "id": "u4_fn3", "category": "function_basics",
        "question": "Use the function y = −6x + 2. What is y when x = 5?",
        "options": ["−28", "28", "−32", "32"], "answer": 0,
        "explanation": "−6(5) + 2 = −30 + 2 = −28.",
    },
    {
        "id": "u4_fn4", "category": "function_basics",
        "question": "Use the function y = 7 + (x − 9). What is y when x = 8?",
        "options": ["6", "8", "−1", "7"], "answer": 0,
        "explanation": "y = 7 + (8 − 9) = 7 − 1 = 6.",
    },
    {
        "id": "u4_fn5", "category": "function_basics",
        "question": (
            "A table shows x-values 5, 6, 7, 8 with y-values 3, 4, 5, 6. "
            "Does this table represent a function?"
        ),
        "options": [
            "Yes — each input has exactly one output",
            "No — some inputs repeat",
            "Only if the table is linear",
            "Only if x-values increase",
        ], "answer": 0,
        "explanation": "Each x-value appears once with exactly one y-value → it is a function.",
    },
    {
        "id": "u4_cf1", "category": "comparing_functions",
        "question": (
            "You earn $75 per week plus $8 per hour worked. "
            "Which equation gives total pay y after x hours?"
        ),
        "options": ["y = 75x + 8", "y = 8x + 75", "y = 83x", "y = 75x"], "answer": 1,
        "explanation": "$8 per hour (rate) plus $75 base → y = 8x + 75.",
    },
    {
        "id": "u4_cf2", "category": "comparing_functions",
        "question": "In y = −5x − 1, what is the speed (magnitude of the rate of change)?",
        "options": ["1", "5", "−5", "6"], "answer": 1,
        "explanation": "Speed is |slope| = |−5| = 5.",
    },
    {
        "id": "u4_cf3", "category": "comparing_functions",
        "question": (
            "Square tiles are placed in a row but not touching. "
            "Which rule gives perimeter P for n separate square tiles (side 1 unit)?"
        ),
        "options": ["P = 2n + 2", "P = 4n", "P = n + 4", "P = 4n + 2"], "answer": 1,
        "explanation": "Each separate square contributes 4 units of perimeter → P = 4n.",
    },
    {
        "id": "u4_cf4", "category": "comparing_functions",
        "question": (
            "Square tiles are placed in a row so they share edges (touching). "
            "Which rule best describes the outer perimeter P for n tiles?"
        ),
        "options": ["P = 4n", "P = 2n + 2", "P = n²", "P = 2n"], "answer": 1,
        "explanation": "Shared edges reduce the outer boundary → P = 2n + 2 for a row of squares.",
    },
    {
        "id": "u4_cf5", "category": "comparing_functions",
        "question": (
            "You walk 0.5 miles per minute from the start. "
            "Which equation gives distance y in miles after x minutes?"
        ),
        "options": ["y = 0.5x", "y = x + 0.5", "y = 2x", "y = 0.5 + x"], "answer": 0,
        "explanation": "Constant rate from zero → y = 0.5x.",
    },
    {
        "id": "u4_co1", "category": "constructing",
        "question": (
            "A plant is 0 mm tall on day 0 and grows 12 mm per day. "
            "How tall is it on day 80?"
        ),
        "options": ["960 mm", "500 mm", "92 mm", "720 mm"], "answer": 0,
        "explanation": "h = 12d → 12(80) = 960 mm.",
    },
    {
        "id": "u4_co2", "category": "constructing",
        "question": (
            "A plant starts at 20 mm tall and grows 6 mm per day. "
            "How tall is it on day 80?"
        ),
        "options": ["500 mm", "480 mm", "960 mm", "520 mm"], "answer": 0,
        "explanation": "20 + 6(80) = 20 + 480 = 500 mm.",
    },
    {
        "id": "u4_co3", "category": "constructing",
        "question": "Which height equation represents a directly proportional (through-the-origin) relationship?",
        "options": ["h = 12d", "h = 20 + 6d", "h = d + 20", "h = 6d + 20"], "answer": 0,
        "explanation": "Only h = 12d has no starting offset and passes through (0, 0).",
    },
    {
        "id": "u4_co4", "category": "constructing",
        "question": (
            "A train of n unit squares in a row (each side 1 unit) has perimeter P. "
            "Which rule matches that pattern?"
        ),
        "options": ["P = 4n", "P = n + 4", "P = 2n", "P = n²"], "answer": 0,
        "explanation": "Each square adds 4 to the perimeter when squares are separate → P = 4n.",
    },
    {
        "id": "u4_lf1", "category": "linear_functions",
        "question": (
            "Points (0, 0), (3, 90), and (6, 180) lie on a line. "
            "Is the relationship linear, and what is the rate of change?"
        ),
        "options": ["Yes, rate 30", "No", "Yes, rate 90", "Yes, rate 60"], "answer": 0,
        "explanation": "y increases by 30 for each +1 in x → constant rate 30, so linear.",
    },
    {
        "id": "u4_lf2", "category": "linear_functions",
        "question": "In the linear function y = 8.3x − 1, what is the rate of change?",
        "options": ["8.3", "−1", "1", "8.3x"], "answer": 0,
        "explanation": "The coefficient of x is the slope (rate) → 8.3.",
    },
    {
        "id": "u4_lf3", "category": "linear_functions",
        "question": "In the linear function y = 5 − 0.5x, what is the rate of change?",
        "options": ["5", "−0.5", "0.5", "−5"], "answer": 1,
        "explanation": "The rate of change is the slope, −0.5.",
    },
    {
        "id": "u4_lf4", "category": "linear_functions",
        "question": "A key feature of linear functions is that the rate of change is:",
        "options": ["Constant", "Increasing", "Zero always", "Undefined"], "answer": 0,
        "explanation": "Linear functions have the same slope everywhere → constant rate of change.",
    },
    {
        "id": "u4_ln1", "category": "linear_nonlinear",
        "question": (
            "A hose fills a pool at 2.25 gallons per minute. "
            "How many gallons are in the pool after 8 minutes?"
        ),
        "options": ["18 gal", "16 gal", "2.25 gal", "20 gal"], "answer": 0,
        "explanation": "w = 2.25t → 2.25(8) = 18 gallons.",
    },
    {
        "id": "u4_ln2", "category": "linear_nonlinear",
        "question": (
            "A dog bowl is filled: the water level rises quickly at first, then levels off. "
            "Is this a linear relationship?"
        ),
        "options": [
            "Yes — the rate stays the same",
            "No — the rate of change is not constant",
            "Yes, if you only look at the first few seconds",
            "No, but only at the very end",
        ], "answer": 1,
        "explanation": "The rate of change is not constant → not linear.",
    },
    {
        "id": "u4_ln3", "category": "linear_nonlinear",
        "question": "Which equation represents a nonlinear function?",
        "options": ["y = 2x", "y = x²", "y = 0.5x", "y = −3x + 1"], "answer": 1,
        "explanation": "y = x² is quadratic and curves → nonlinear.",
    },
    {
        "id": "u4_ln4", "category": "linear_nonlinear",
        "question": "What is the best way to tell if a data set is linear?",
        "options": ["Constant rate of change", "Always curved", "More than 5 points", "Negative values"], "answer": 0,
        "explanation": "Linear data has the same change in y for equal steps in x.",
    },
]
