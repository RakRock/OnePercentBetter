"""Arjun Course 3 Unit 3 — Geometry practice bank."""

from __future__ import annotations

UNIT3_CATEGORIES = {
    "angles": {"name": "Angle Relationships", "emoji": "📐", "color": "#3b82f6", "weight": 2},
    "transformations": {"name": "Transformations", "emoji": "🔄", "color": "#8b5cf6", "weight": 1},
    "similarity": {"name": "Similar Triangles", "emoji": "△", "color": "#10b981", "weight": 1},
    "pythagorean": {"name": "Pythagorean Theorem", "emoji": "📏", "color": "#f59e0b", "weight": 2},
    "surface_area": {"name": "Surface Area", "emoji": "📦", "color": "#06b6d4", "weight": 1},
    "volume": {"name": "Volume", "emoji": "🧊", "color": "#ef4444", "weight": 1},
}

UNIT3_CATEGORY_ACTIVITY = {
    "angles": "activity_16_angle_pair_relationships",
    "transformations": "activity_18_introduction_transformations",
    "similarity": "activity_20_similar_triangles",
    "pythagorean": "activity_22_pythagorean_theorem",
    "surface_area": "activity_25_surface_area",
    "volume": "activity_26_volumes_of_solids",
}

UNIT3_REVISION_TIPS = {
    "angles": "Complementary = 90°; supplementary = 180°; triangle sum = 180°.",
    "transformations": "Translation: add to x/y; reflect x-axis: negate y.",
    "similarity": "AA similarity; scale factor multiplies side lengths.",
    "pythagorean": "a² + b² = c² for right triangles; c is hypotenuse.",
    "surface_area": "Prism SA = 2(lw + lh + wh); cube SA = 6s².",
    "volume": "Prism V = Bh; pyramid V = ⅓Bh.",
}

UNIT3_QUESTION_BANK: list[dict] = [
    {
        "id": "u3_ang1", "category": "angles",
        "question": "Two angles are complementary if they add to 90°. What is the complement of 38°?",
        "options": ["52°", "142°", "38°", "90°"], "answer": 0,
        "explanation": "90° − 38° = 52°.",
    },
    {
        "id": "u3_ang2", "category": "angles",
        "question": "In a triangle, two angles measure 32° and 70°. What is the third angle?",
        "options": ["68°", "78°", "88°", "102°"], "answer": 1,
        "explanation": "Triangle angles sum to 180°: 180 − 32 − 70 = 78°.",
    },
    {
        "id": "u3_ang3", "category": "angles",
        "question": (
            "Two supplementary angles add to 180°. One angle is twice the other. "
            "What is the measure of the smaller angle?"
        ),
        "options": ["60°", "90°", "120°", "30°"], "answer": 0,
        "explanation": "x + 2x = 180 → x = 60° (the smaller angle).",
    },
    {
        "id": "u3_ang4", "category": "angles",
        "question": (
            "Vertical angles are equal. If one vertical angle is (5x − 7)° and the other is (3x + 31)°, "
            "what is x?"
        ),
        "options": ["17", "19", "21", "15"], "answer": 1,
        "explanation": "5x − 7 = 3x + 31 → 2x = 38 → x = 19.",
    },
    {
        "id": "u3_ang5", "category": "angles",
        "question": "In a right triangle, one acute angle is 22°. What is the other acute angle?",
        "options": ["68°", "78°", "58°", "112°"], "answer": 0,
        "explanation": "The two acute angles sum to 90°: 90 − 22 = 68°.",
    },
    {
        "id": "u3_ang6", "category": "angles",
        "question": "Can a triangle have angles measuring 100° and 82°?",
        "options": ["Yes", "No — sum exceeds 180°", "Only if isosceles", "Only if equilateral"], "answer": 1,
        "explanation": "100 + 82 = 182°, which is more than 180°, so no triangle is possible.",
    },
    {
        "id": "u3_tr1", "category": "transformations",
        "question": "Translate the point (3, 2) right 4 units and down 1 unit. What is the new point?",
        "options": ["(7, 1)", "(7, 3)", "(−1, 1)", "(4, −1)"], "answer": 0,
        "explanation": "Add 4 to x and subtract 1 from y: (3 + 4, 2 − 1) = (7, 1).",
    },
    {
        "id": "u3_tr2", "category": "transformations",
        "question": "Reflect the point (−2, 5) across the x-axis. What is the image?",
        "options": ["(2, 5)", "(−2, −5)", "(2, −5)", "(−5, −2)"], "answer": 1,
        "explanation": "Reflecting across the x-axis negates the y-coordinate.",
    },
    {
        "id": "u3_tr3", "category": "transformations",
        "question": "Reflect the point (4, −3) across the y-axis. What is the image?",
        "options": ["(4, 3)", "(−4, −3)", "(−4, 3)", "(3, −4)"], "answer": 1,
        "explanation": "Reflecting across the y-axis negates the x-coordinate.",
    },
    {
        "id": "u3_tr4", "category": "transformations",
        "question": "Rotate the point (3, 1) 90° counterclockwise about the origin. What is the image?",
        "options": ["(1, 3)", "(−1, 3)", "(−3, −1)", "(1, −3)"], "answer": 1,
        "explanation": "A 90° CCW rotation maps (x, y) to (−y, x) → (−1, 3).",
    },
    {
        "id": "u3_tr5", "category": "transformations",
        "question": "Rotate the point (−2, 3) 180° about the origin. What is the image?",
        "options": ["(2, −3)", "(−2, −3)", "(3, −2)", "(2, 3)"], "answer": 0,
        "explanation": "A 180° rotation maps (x, y) to (−x, −y) → (2, −3).",
    },
    {
        "id": "u3_sim1", "category": "similarity",
        "question": (
            "Two triangles each have angles of 50° and 60°. "
            "Are the triangles similar by the AA (angle-angle) rule?"
        ),
        "options": ["Yes (AA)", "No", "Only if sides match", "Only if congruent"], "answer": 0,
        "explanation": "Both triangles must have a third angle of 70°, so AA proves similarity.",
    },
    {
        "id": "u3_sim2", "category": "similarity",
        "question": "A triangle has sides 6, 8, and 10. Which set of side lengths could form a similar triangle?",
        "options": ["3, 4, 5", "6, 8, 9", "12, 16, 20", "Both A and C"], "answer": 3,
        "explanation": "6-8-10 and 3-4-5 have ratio 2:1; 12-16-20 is also a scale-2 version.",
    },
    {
        "id": "u3_sim3", "category": "similarity",
        "question": (
            "Triangle ABC is similar to triangle DEF. AB = 8, DE = 12, and BC = 6. What is EF?"
        ),
        "options": ["8", "9", "10", "12"], "answer": 1,
        "explanation": "Scale factor DE/AB = 12/8 = 1.5 → EF = 6 × 1.5 = 9.",
    },
    {
        "id": "u3_sim4", "category": "similarity",
        "question": (
            "Two similar figures have a side-length ratio of 2 : 3. "
            "The smaller figure has perimeter 18. What is the perimeter of the larger figure?"
        ),
        "options": ["24", "27", "36", "12"], "answer": 1,
        "explanation": "18 × (3/2) = 27.",
    },
    {
        "id": "u3_pyt1", "category": "pythagorean",
        "question": "A right triangle has legs 5 and 12. What is the length of the hypotenuse?",
        "options": ["13", "17", "15", "11"], "answer": 0,
        "explanation": "5² + 12² = 25 + 144 = 169 = 13².",
    },
    {
        "id": "u3_pyt2", "category": "pythagorean",
        "question": "A right triangle has one leg 9 and hypotenuse 15. What is the other leg?",
        "options": ["10", "12", "6", "8"], "answer": 1,
        "explanation": "15² − 9² = 225 − 81 = 144 → leg = 12.",
    },
    {
        "id": "u3_pyt3", "category": "pythagorean",
        "question": (
            "A 10-foot ladder leans against a wall with its base 6 feet from the wall. "
            "How high up the wall does the ladder reach?"
        ),
        "options": ["6 ft", "8 ft", "4 ft", "10 ft"], "answer": 1,
        "explanation": "10² − 6² = 100 − 36 = 64 → height = 8 ft.",
    },
    {
        "id": "u3_pyt4", "category": "pythagorean",
        "question": "Do side lengths 9, 12, and 15 form a right triangle?",
        "options": ["Yes", "No", "Only if acute", "Cannot tell"], "answer": 0,
        "explanation": "9² + 12² = 81 + 144 = 225 = 15² → yes, it is a right triangle.",
    },
    {
        "id": "u3_pyt5", "category": "pythagorean",
        "question": "A rectangle is 9 feet by 12 feet. How long is the diagonal?",
        "options": ["15 ft", "21 ft", "13 ft", "18 ft"], "answer": 0,
        "explanation": "Use the 9-12-15 Pythagorean triple → diagonal = 15 ft.",
    },
    {
        "id": "u3_pyt6", "category": "pythagorean",
        "question": "What is the distance between the points (1, 2) and (4, 6)?",
        "options": ["5", "7", "4", "6"], "answer": 0,
        "explanation": "Horizontal change 3, vertical change 4 → 3-4-5 triangle, distance = 5.",
    },
    {
        "id": "u3_pyt7", "category": "pythagorean",
        "question": (
            "A 25-foot ladder has its base 15 feet from a wall. "
            "How high on the wall does the top of the ladder reach?"
        ),
        "options": ["20 ft", "18 ft", "22 ft", "10 ft"], "answer": 0,
        "explanation": "25² − 15² = 625 − 225 = 400 → height = 20 ft.",
    },
    {
        "id": "u3_sa1", "category": "surface_area",
        "question": "Find the surface area of a rectangular prism with length 5 in, width 4 in, and height 3 in.",
        "options": ["94 in²", "60 in²", "74 in²", "120 in²"], "answer": 0,
        "explanation": "SA = 2(lw + lh + wh) = 2(20 + 15 + 12) = 94 in².",
    },
    {
        "id": "u3_sa2", "category": "surface_area",
        "question": "Find the surface area of a cube with side length 6 cm.",
        "options": ["36 cm²", "216 cm²", "144 cm²", "72 cm²"], "answer": 1,
        "explanation": "SA = 6s² = 6 × 36 = 216 cm².",
    },
    {
        "id": "u3_sa3", "category": "surface_area",
        "question": (
            "A rectangular prism has length 5 ft, width 4 ft, and surface area 94 ft². "
            "What is its height?"
        ),
        "options": ["2 ft", "3 ft", "4 ft", "5 ft"], "answer": 1,
        "explanation": "94 = 2(20 + 5h + 4h) → 47 = 20 + 9h → h = 3 ft.",
    },
    {
        "id": "u3_vol1", "category": "volume",
        "question": "Find the volume of a rectangular prism with length 5 in, width 8 in, and height 6 in.",
        "options": ["240 in³", "120 in³", "480 in³", "19 in³"], "answer": 0,
        "explanation": "V = lwh = 5 × 8 × 6 = 240 in³.",
    },
    {
        "id": "u3_vol2", "category": "volume",
        "question": (
            "A square pyramid has a square base with side 12 cm and height 20 cm. What is its volume?"
        ),
        "options": ["480 cm³", "960 cm³", "1440 cm³", "720 cm³"], "answer": 1,
        "explanation": "Base area = 144. V = ⅓ × 144 × 20 = 960 cm³.",
    },
    {
        "id": "u3_vol3", "category": "volume",
        "question": "Find the volume of a cube with edge length 1.5 ft.",
        "options": ["3.375 ft³", "6.75 ft³", "2.25 ft³", "4.5 ft³"], "answer": 0,
        "explanation": "V = s³ = 1.5³ = 3.375 ft³.",
    },
    {
        "id": "u3_vol4", "category": "volume",
        "question": (
            "A rectangular prism has volume 80 ft³, length 8 ft, and height 4 ft. What is its width?"
        ),
        "options": ["2.5 ft", "3 ft", "2 ft", "4 ft"], "answer": 0,
        "explanation": "80 = 8 × 4 × w → w = 80/32 = 2.5 ft.",
    },
]
