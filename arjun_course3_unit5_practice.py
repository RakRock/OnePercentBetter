"""Arjun Course 3 Unit 5 — Probability & Statistics practice bank."""

from __future__ import annotations

UNIT5_CATEGORIES = {
    "scatter_association": {"name": "Scatter & Association", "emoji": "📈", "color": "#3b82f6", "weight": 2},
    "bivariate_data": {"name": "Bivariate Data", "emoji": "📊", "color": "#8b5cf6", "weight": 1},
    "mad": {"name": "Mean Absolute Deviation", "emoji": "📏", "color": "#10b981", "weight": 1},
    "two_way_tables": {"name": "Two-Way Tables", "emoji": "📋", "color": "#f59e0b", "weight": 2},
}

UNIT5_CATEGORY_ACTIVITY = {
    "scatter_association": "activity_32_analyzing_data",
    "bivariate_data": "activity_33_bivariate_data",
    "mad": "activity_34_median_median_line",
    "two_way_tables": "activity_35_two_way_tables_association",
}

UNIT5_REVISION_TIPS = {
    "scatter_association": "Positive: both increase; negative: one up, other down.",
    "bivariate_data": "Two variables measured on each individual.",
    "mad": "Average distance from the mean — measures spread.",
    "two_way_tables": "Use row totals for conditional percentages.",
}

UNIT5_QUESTION_BANK: list[dict] = [
    {
        "id": "u5_sc1", "category": "scatter_association",
        "question": (
            "Students who watch more TV hours tend to have lower test scores. "
            "What type of association is this?"
        ),
        "options": ["Positive", "Negative", "None", "Cannot tell"], "answer": 1,
        "explanation": "As TV hours go up, scores go down → negative association.",
    },
    {
        "id": "u5_sc2", "category": "scatter_association",
        "question": (
            "Students who complete a higher percent of homework tend to score higher on tests. "
            "What type of association is this?"
        ),
        "options": ["Positive", "Negative", "No association", "Nonlinear only"], "answer": 0,
        "explanation": "Both variables increase together → positive association.",
    },
    {
        "id": "u5_sc3", "category": "scatter_association",
        "question": (
            "Students who watch more TV tend to complete less homework. "
            "What type of association is this?"
        ),
        "options": ["Positive", "Negative", "None", "Linear only"], "answer": 1,
        "explanation": "TV up, homework down → negative association.",
    },
    {
        "id": "u5_sc4", "category": "scatter_association",
        "question": (
            "You compare helmet price to safety quality rating. "
            "Which association is most reasonable?"
        ),
        "options": ["Negative linear", "Positive linear", "No pattern", "Negative nonlinear"], "answer": 1,
        "explanation": "Higher price often goes with higher quality rating → positive.",
    },
    {
        "id": "u5_sc5", "category": "scatter_association",
        "question": (
            "You plot time spent studying against test score. "
            "What association would you most expect?"
        ),
        "options": ["Positive", "Negative", "Zero slope only", "No variables"], "answer": 0,
        "explanation": "More study time usually means higher scores → positive.",
    },
    {
        "id": "u5_bi1", "category": "bivariate_data",
        "question": "Which data set is bivariate (two variables measured on each case)?",
        "options": [
            "Heights of 20 students only",
            "House prices AND sizes for 40 houses",
            "Test scores only",
            "Shoe sizes only",
        ],
        "answer": 1,
        "explanation": "Each house has both a price and a size → two variables.",
    },
    {
        "id": "u5_bi2", "category": "bivariate_data",
        "question": (
            "You plot bear height against bear weight. "
            "What association would you expect?"
        ),
        "options": ["Positive", "Negative", "None", "Always negative"], "answer": 0,
        "explanation": "Taller bears usually weigh more → positive association.",
    },
    {
        "id": "u5_bi3", "category": "bivariate_data",
        "question": (
            "A line of fit is y = 492 + 15x, where x is age in years and y is meters walked. "
            "What does the slope 15 mean?"
        ),
        "options": ["Start at 492 m", "15 m more per year of age", "15 years per meter", "492 years"],
        "answer": 1,
        "explanation": "Slope is change in y per 1 unit of x → 15 more meters per year.",
    },
    {
        "id": "u5_bi4", "category": "bivariate_data",
        "question": (
            "A line is y = 12 − 0.2x, where x is frying time in minutes and y is fat in grams. "
            "What does the slope −0.2 mean?"
        ),
        "options": ["−0.2 g fat per minute", "12 g total", "0.2 g gain per minute", "−12"],
        "answer": 0,
        "explanation": "Fat decreases by 0.2 grams for each extra minute.",
    },
    {
        "id": "u5_bi5", "category": "bivariate_data",
        "question": "Use y = 492 + 15x. Predict meters walked when age x = 12.",
        "options": ["507 m", "672 m", "492 m", "180 m"], "answer": 1,
        "explanation": "492 + 15(12) = 492 + 180 = 672 meters.",
    },
    {
        "id": "u5_mad1", "category": "mad",
        "question": (
            "Data set: 22, 34, 21, 12, 40, 37, 27, 19, 23, 25. The mean is about 26. "
            "What is the mean absolute deviation (MAD)?"
        ),
        "options": ["6.8", "26", "8.4", "4.2"], "answer": 0,
        "explanation": "MAD is the average distance from the mean → about 6.8.",
    },
    {
        "id": "u5_mad2", "category": "mad",
        "question": "The mean absolute deviation (MAD) tells you:",
        "options": ["Center of data", "Typical distance from mean", "Maximum value", "Slope of trend line"],
        "answer": 1,
        "explanation": "MAD measures how spread out values are from the mean.",
    },
    {
        "id": "u5_tw1", "category": "two_way_tables",
        "question": (
            "On the defense team, 35 players prefer Pizza Palace and 9 prefer Burger Bungalow. "
            "What percent of defense players prefer Burger Bungalow?"
        ),
        "options": ["9%", "20.5%", "35%", "44%"], "answer": 1,
        "explanation": "9 ÷ (35 + 9) ≈ 20.5%.",
    },
    {
        "id": "u5_tw2", "category": "two_way_tables",
        "question": (
            "In a survey, 330 out of 500 males say they always wear a seat belt. "
            "What percent is that?"
        ),
        "options": ["33%", "66%", "50%", "75%"], "answer": 1,
        "explanation": "330/500 = 0.66 = 66%.",
    },
    {
        "id": "u5_tw3", "category": "two_way_tables",
        "question": (
            "In 6th grade, 160 students participate in a club and 90 do not (250 total). "
            "What percent participate?"
        ),
        "options": ["36%", "64%", "160%", "90%"], "answer": 1,
        "explanation": "160/250 = 0.64 = 64%.",
    },
    {
        "id": "u5_tw4", "category": "two_way_tables",
        "question": (
            "Soccer has a 20% injury rate and football has a 24% injury rate. "
            "Which sport has the higher injury rate?"
        ),
        "options": ["Soccer", "Football", "Same", "Need totals"], "answer": 1,
        "explanation": "24% > 20% → football has the higher rate.",
    },
    {
        "id": "u5_tw5", "category": "two_way_tables",
        "question": "Row percentages in a two-way table help you:",
        "options": ["Find mean", "Compare groups within one category", "Calculate volume", "Solve for x"],
        "answer": 1,
        "explanation": "Row % shows how responses split within one row group.",
    },
    {
        "id": "u5_ex1", "category": "scatter_association",
        "question": (
            "Your scatter plot shows TV hours up to 20 per week. "
            "Predicting a test score at 60 TV hours per week is called:"
        ),
        "options": ["Interpolation", "Extrapolation — unreliable", "Exact", "Always valid"], "answer": 1,
        "explanation": "60 hours is outside the data range → extrapolation, often unreliable.",
    },
]
