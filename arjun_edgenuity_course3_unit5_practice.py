"""Edgenuity Course 3 Unit 5 — Linear Equations practice bank."""

from __future__ import annotations

UNIT5_CATEGORIES = {
    "algebra_tiles": {
        "name": "Algebra Tiles",
        "emoji": "🧱",
        "color": "#3b82f6",
        "weight": 2,
    },
    "properties_equality": {
        "name": "Properties of Equality",
        "emoji": "⚖️",
        "color": "#8b5cf6",
        "weight": 1,
    },
    "simplify_expressions": {
        "name": "Simplify Expressions",
        "emoji": "✂️",
        "color": "#10b981",
        "weight": 2,
    },
    "number_of_solutions": {
        "name": "Number of Solutions",
        "emoji": "🔢",
        "color": "#f59e0b",
        "weight": 2,
    },
    "multistep_solving": {
        "name": "Multi-Step Solving",
        "emoji": "📝",
        "color": "#ef4444",
        "weight": 2,
    },
    "word_problems": {
        "name": "Word Problems & Standard Form",
        "emoji": "🌍",
        "color": "#06b6d4",
        "weight": 2,
    },
}

UNIT5_CATEGORY_ACTIVITY = {
    "algebra_tiles": "activity_1_algebra_tiles",
    "properties_equality": "activity_2_properties_equality",
    "simplify_expressions": "activity_3_simplify_expressions",
    "number_of_solutions": "activity_4_number_of_solutions",
    "multistep_solving": "activity_5_multistep_solving",
    "word_problems": "activity_6_standard_form_word_problems",
}

UNIT5_REVISION_TIPS = {
    "algebra_tiles": "Remove the same tiles from both sides to keep the equation balanced.",
    "properties_equality": "Do the same operation to both sides. Distribute before combining like terms.",
    "simplify_expressions": "Watch negative signs when distributing: −(x − 3) = −x + 3.",
    "number_of_solutions": "If variables cancel and you get a false statement → no solution; true → infinite.",
    "multistep_solving": "Distribute → combine like terms → move variables to one side → isolate x.",
    "word_problems": "Define the variable, write each quantity in terms of x, then set up the equation.",
}

UNIT5_QUESTION_BANK: list[dict] = [
    # ── Algebra tiles (7) ──
    {
        "id": "u5_at1", "category": "algebra_tiles",
        "question": "Use the tile model for 2x = x + 3. Which move finds the solution?",
        "options": [
            "Remove 1 x-tile from each side",
            "Add 3 unit tiles to each side",
            "Remove 3 unit tiles from the right only",
            "Split into groups without removing tiles",
        ],
        "answer": 0,
        "explanation": "Subtract x from both sides: x = 3.",
        "image": "practice_u5_tiles_2x",
    },
    {
        "id": "u5_at2", "category": "algebra_tiles",
        "question": (
            "Juanita models 3x + 2 = −x + 6 with 3 x-tiles and 2 unit tiles on the left, "
            "and −x on the right. How should she complete the model?"
        ),
        "options": [
            "Put 6 positive unit tiles on the right",
            "Put 6 x-tiles on the right",
            "Put 4 unit tiles on the left",
            "Put 4 unit tiles on the right only",
        ],
        "answer": 0,
        "explanation": "Right side needs +6 units to match −x + 6.",
        "image": "practice_u5_tiles_3x2",
    },
    {
        "id": "u5_at3", "category": "algebra_tiles",
        "question": "In a tile model, four unit tiles on one side represent —",
        "options": ["+4", "−4", "+4x", "−4x"],
        "answer": 0,
        "explanation": "Each small unit tile stands for 1.",
    },
    {
        "id": "u5_at4", "category": "algebra_tiles",
        "question": "To solve 2x = x + 5 with tiles, the best first move is —",
        "options": [
            "Remove one x-tile from each side",
            "Add 5 unit tiles to the left",
            "Remove all unit tiles",
            "Flip all tiles to negative",
        ],
        "answer": 0,
        "explanation": "Balance by removing x from both sides → x = 5.",
        "image": "practice_u5_tiles_2x",
    },
    {
        "id": "u5_at5", "category": "algebra_tiles",
        "question": "3x + 4 = x + 10. After removing one x-tile from each side, you have —",
        "options": ["2x + 4 = 10", "3x + 4 = 10", "2x = 10", "x + 4 = 10"],
        "answer": 0,
        "explanation": "Subtract x from both sides: 2x + 4 = 10.",
    },
    {
        "id": "u5_at6", "category": "algebra_tiles",
        "question": "Negative x-tiles on a model represent —",
        "options": ["−x terms", "+x terms", "Unit values of −1", "The constant term only"],
        "answer": 0,
        "explanation": "Red/orange x-tiles represent −x.",
    },
    {
        "id": "u5_at7", "category": "algebra_tiles",
        "question": "Balanced tile models show that equations must stay —",
        "options": [
            "Equal on both sides after each move",
            "Positive on both sides",
            "Free of unit tiles",
            "Written in slope-intercept form",
        ],
        "answer": 0,
        "explanation": "Whatever you do to one side, do to the other.",
    },
    # ── Properties of equality (7) ──
    {
        "id": "u5_pe1", "category": "properties_equality",
        "question": "Which equation is best solved using the addition property of equality?",
        "options": ["f − 23 = 45", "f + 23 = 45", "23f = 45", "f ÷ 23 = 45"],
        "answer": 0,
        "explanation": "Add 23 to both sides to isolate f.",
    },
    {
        "id": "u5_pe2", "category": "properties_equality",
        "question": "4(x − 6) = 5 → 4x − 24 = 5. Which property was used first?",
        "options": [
            "Distributive property",
            "Addition property of equality",
            "Division property of equality",
            "Commutative property",
        ],
        "answer": 0,
        "explanation": "Multiply 4 through (x − 6).",
        "image": "practice_u5_multistep",
    },
    {
        "id": "u5_pe3", "category": "properties_equality",
        "question": "The graphic shows 8(3x + 40) = 10 with arrows from 8 to each term. Which property?",
        "options": [
            "Distributive property of multiplication",
            "Addition property of equality",
            "Commutative property",
            "Associative property of addition",
        ],
        "answer": 0,
        "explanation": "Distribution multiplies 8 by each addend inside the parentheses.",
        "image": "practice_u5_distribute_graphic",
    },
    {
        "id": "u5_pe4", "category": "properties_equality",
        "question": "9y − 12x = 36. First step to solve for y?",
        "options": [
            "Add 12x to both sides",
            "Subtract 12x from both sides",
            "Multiply both sides by 12",
            "Divide both sides by 12",
        ],
        "answer": 0,
        "explanation": "Move −12x: 9y = 12x + 36.",
        "image": "practice_u5_solve_y",
    },
    {
        "id": "u5_pe5", "category": "properties_equality",
        "question": "Leah has 4y = 8 − 3x. Next step to solve for y?",
        "options": [
            "Divide both sides by 4",
            "Multiply both sides by 4",
            "Add 4y to both sides",
            "Subtract 8 from both sides",
        ],
        "answer": 0,
        "explanation": "y = (8 − 3x)/4.",
    },
    {
        "id": "u5_pe6", "category": "properties_equality",
        "question": "7(x − 3) = 28 → 7x − 21 = 28 → 7x = 49 → x = ?",
        "options": ["7", "9", "42", "56"],
        "answer": 0,
        "explanation": "49 ÷ 7 = 7.",
    },
    {
        "id": "u5_pe7", "category": "properties_equality",
        "question": "(2/3)x + (1/3)x + 2 = 5. Best first step?",
        "options": [
            "Combine like terms on the left",
            "Multiply both sides by 5",
            "Subtract 2/3 from each side",
            "Add 2 to each side first",
        ],
        "answer": 0,
        "explanation": "(2/3 + 1/3)x = x, so combine to get x + 2 = 5.",
    },
    # ── Simplify expressions (8) ──
    {
        "id": "u5_se1", "category": "simplify_expressions",
        "question": "Kadesha simplifies −(x − 3) − 2(x − 1). First error?",
        "options": [
            "Step 2 should be −x + 3 − 2x + 2",
            "Step 1: forgot to distribute",
            "Step 3: cannot combine terms",
            "Step 4: answer should be −x − 5",
        ],
        "answer": 0,
        "explanation": "−(x − 3) = −x + 3 and −2(x − 1) = −2x + 2.",
    },
    {
        "id": "u5_se2", "category": "simplify_expressions",
        "question": "Which is equivalent to 6(x − 4)?",
        "options": ["6x − 24", "6x − 4", "−6x + 24", "x − 24"],
        "answer": 0,
        "explanation": "6·x − 6·4 = 6x − 24.",
    },
    {
        "id": "u5_se3", "category": "simplify_expressions",
        "question": "Which is equivalent to 7b + 4b − 1b?",
        "options": ["10b", "12b", "4b", "2b"],
        "answer": 0,
        "explanation": "7 + 4 − 1 = 10 → 10b.",
    },
    {
        "id": "u5_se4", "category": "simplify_expressions",
        "question": "Simplify ½(8x + 4) + ⅓(9 − 3x).",
        "options": ["3x + 5", "7x + 1", "x + 7", "5x + 5"],
        "answer": 0,
        "explanation": "4x + 2 + 3 − x = 3x + 5.",
    },
    {
        "id": "u5_se5", "category": "simplify_expressions",
        "question": "Carey expands 4(2x − 1) + 5 = 3 + 2(x + 1) to 8x − 4 + 5 = 3 + 2x + 2. Which terms combine on the left?",
        "options": ["−4 + 5", "8x + 2x", "4 + 5", "−4 + 5 + 3 + 2"],
        "answer": 0,
        "explanation": "Combine constants −4 and +5 on the left.",
    },
    {
        "id": "u5_se6", "category": "simplify_expressions",
        "question": "−3(x + 2) equals —",
        "options": ["−3x − 6", "−3x + 6", "3x − 6", "−3x + 2"],
        "answer": 0,
        "explanation": "Distribute −3: −3x − 6.",
    },
    {
        "id": "u5_se7", "category": "simplify_expressions",
        "question": "5x + 2x − x equals —",
        "options": ["6x", "8x", "4x", "7x"],
        "answer": 0,
        "explanation": "5 + 2 − 1 = 6 → 6x.",
    },
    {
        "id": "u5_se8", "category": "simplify_expressions",
        "question": "4(x − ½) equals —",
        "options": ["4x − 2", "4x − ½", "x − 2", "4x + 2"],
        "answer": 0,
        "explanation": "4·x − 4·½ = 4x − 2.",
    },
    # ── Number of solutions (7) ──
    {
        "id": "u5_ns1", "category": "number_of_solutions",
        "question": "Which equation has exactly one solution?",
        "options": [
            "3(x − 1) + 2x = 3(x − 1) + 2",
            "6x − 8 = 4(x − 2) + 2x",
            "7x + 2 − x = 6(x + 2)",
            "4(x + 3) + x = 5(x + 1) + 7",
        ],
        "answer": 0,
        "explanation": "5x − 3 = 3x − 1 → 2x = 2 → x = 1. The others simplify to identities or contradictions.",
    },
    {
        "id": "u5_ns2", "category": "number_of_solutions",
        "question": "Kamal: 3(x − 8) = x + 2x + 7 → 3x − 24 = 3x + 7 → −24 = 7. Solution?",
        "options": ["No solution", "−24", "7", "Infinitely many solutions"],
        "answer": 0,
        "explanation": "Variables cancel leaving a false statement → no solution.",
    },
    {
        "id": "u5_ns3", "category": "number_of_solutions",
        "question": "6x − 8 = 4(x − 2) + 2x simplifies to —",
        "options": [
            "6x − 8 = 6x − 8 (infinitely many solutions)",
            "6x − 8 = 6x − 10 (one solution)",
            "x = 0 (one solution)",
            "No solution",
        ],
        "answer": 0,
        "explanation": "Both sides identical → all real numbers work.",
    },
    {
        "id": "u5_ns4", "category": "number_of_solutions",
        "question": "4(x + 3) + x = 5(x + 1) + 7 simplifies to —",
        "options": [
            "5x + 12 = 5x + 12 (infinitely many)",
            "One solution x = 0",
            "No solution",
            "One solution x = 12",
        ],
        "answer": 0,
        "explanation": "Both sides equal 5x + 12 → identity.",
    },
    {
        "id": "u5_ns5", "category": "number_of_solutions",
        "question": "7x + 2 − x = 6(x + 2) simplifies to —",
        "options": [
            "6x + 2 = 6x + 12 → no solution",
            "One solution x = 2",
            "Infinitely many",
            "One solution x = 10",
        ],
        "answer": 0,
        "explanation": "6x + 2 = 6x + 12 → 2 = 12 is false.",
    },
    {
        "id": "u5_ns6", "category": "number_of_solutions",
        "question": "If solving gives 5 = 5 after variables cancel, there are —",
        "options": [
            "Infinitely many solutions",
            "No solution",
            "Exactly one solution",
            "Zero solutions and one solution",
        ],
        "answer": 0,
        "explanation": "True statement for all x → infinite solutions.",
    },
    {
        "id": "u5_ns7", "category": "number_of_solutions",
        "question": "If solving gives 3 = 7 after variables cancel, there are —",
        "options": ["No solution", "Infinitely many", "x = 7", "x = 3"],
        "answer": 0,
        "explanation": "False statement → no value of x works.",
    },
    # ── Multi-step solving (8) ──
    {
        "id": "u5_ms1", "category": "multistep_solving",
        "question": "First step to solve 4x + 3(x + 2) = 5(2x − 3)?",
        "options": [
            "Distribute 3 and 5",
            "Combine 4x and x first without distributing",
            "Subtract 2x from both sides immediately",
            "Add 3 to both sides",
        ],
        "answer": 0,
        "explanation": "Expand both parentheses before combining like terms.",
    },
    {
        "id": "u5_ms2", "category": "multistep_solving",
        "question": "Three times a number minus ten equals twice the number plus five. Equation?",
        "options": ["3x − 10 = 2x + 5", "3x − 10 = 2x − 5", "3x + 10 = 2x + 5", "x − 10 = 2x + 5"],
        "answer": 0,
        "explanation": "3x − 10 = 2x + 5 → x = 15.",
        "image": "practice_u5_variables_both",
    },
    {
        "id": "u5_ms3", "category": "multistep_solving",
        "question": "Solve 3x − 10 = 2x + 5.",
        "options": ["15", "3", "−5", "−1"],
        "answer": 0,
        "explanation": "Subtract 2x: x − 10 = 5 → x = 15.",
    },
    {
        "id": "u5_ms4", "category": "multistep_solving",
        "question": "Maria: 3(x + 6) = 5(x − 4) → 3x + 18 = 5x − 20. Solution?",
        "options": ["19", "38", "No solution", "Infinitely many"],
        "answer": 0,
        "explanation": "18 + 20 = 2x → x = 19.",
    },
    {
        "id": "u5_ms5", "category": "multistep_solving",
        "question": "Leonardo: 4(x − 1/5) = 2⅔. Error in step 3 when adding fractions?",
        "options": [
            "Should be 40/15 + 12/15 not 40/15 + 16/15",
            "Error in step 1 distribute",
            "Error in step 2",
            "Error in step 4 divide",
        ],
        "answer": 0,
        "explanation": "4/5 = 8/15 not 16/15 when converting to fifteenths.",
    },
    {
        "id": "u5_ms6", "category": "multistep_solving",
        "question": "Solve 4(2x − 1) + 5 = 3 + 2(x + 1).",
        "options": ["2/3", "1", "2", "0"],
        "answer": 0,
        "explanation": "8x + 1 = 2x + 5 → 6x = 4 → x = 2/3.",
    },
    {
        "id": "u5_ms7", "category": "multistep_solving",
        "question": "Solve 5(x − 2) = 3x + 4.",
        "options": ["7", "5", "3", "9"],
        "answer": 0,
        "explanation": "5x − 10 = 3x + 4 → 2x = 14 → x = 7.",
    },
    {
        "id": "u5_ms8", "category": "multistep_solving",
        "question": "Solve 2(x + 4) = x + 10.",
        "options": ["2", "4", "6", "8"],
        "answer": 0,
        "explanation": "2x + 8 = x + 10 → x = 2.",
    },
    # ── Word problems & standard form (8) ──
    {
        "id": "u5_wp1", "category": "word_problems",
        "question": (
            "Hockey: Seals scored 3 less than twice the Fins' goals. "
            "Rays scored 2 more than the Fins. Total 11 goals. Fins = x. Equation?"
        ),
        "options": [
            "x + (2x − 3) + (x + 2) = 11",
            "x + (x + 3) + (x + 2) = 11",
            "x + (2x − 3) + (x − 2) = 11",
            "x + (x − 3) + (x + 2) = 11",
        ],
        "answer": 0,
        "explanation": "Fins x, Seals 2x−3, Rays x+2 → sum 11. x=3.",
        "image": "practice_u5_hockey",
    },
    {
        "id": "u5_wp2", "category": "word_problems",
        "question": (
            "Square side x and equilateral triangle side x + 1 have equal perimeter. Equation?"
        ),
        "options": ["4x = 3(x + 1)", "3x = 4(x + 1)", "x = 3(x + 1)", "x = x + 1"],
        "answer": 0,
        "explanation": "Square perimeter 4x = triangle 3(x + 1).",
        "image": "practice_u5_perimeter",
    },
    {
        "id": "u5_wp3", "category": "word_problems",
        "question": "Tonya wrote x = 150 − 6y. Equivalent equation?",
        "options": ["x + 6y = 150", "x + 150 = 6y", "2x + 3y = 75", "2x − 3y = 75"],
        "answer": 0,
        "explanation": "Add 6y to both sides.",
    },
    {
        "id": "u5_wp4", "category": "word_problems",
        "question": "Solve 4x = 3(x + 1) for x (perimeter problem).",
        "options": ["3", "1", "4", "−3"],
        "answer": 0,
        "explanation": "4x = 3x + 3 → x = 3.",
    },
    {
        "id": "u5_wp5", "category": "word_problems",
        "question": "9y − 12x = 36 solved for y gives —",
        "options": ["y = (4x + 12)/3", "y = 12x + 36", "y = −12x + 36", "y = 4x + 3"],
        "answer": 0,
        "explanation": "9y = 12x + 36 → y = (12x + 36)/9 = (4x + 12)/3.",
        "image": "practice_u5_solve_y",
    },
    {
        "id": "u5_wp6", "category": "word_problems",
        "question": "Hockey problem: x + (2x − 3) + (x + 2) = 11. How many goals did the Fins score?",
        "options": ["3", "2", "5", "4"],
        "answer": 0,
        "explanation": "4x − 1 = 11 → x = 3.",
    },
    {
        "id": "u5_wp7", "category": "word_problems",
        "question": "3x + 4y = 8. Solve for y.",
        "options": ["y = (8 − 3x)/4", "y = 8 − 3x", "y = 2 − 3x", "y = (8 + 3x)/4"],
        "answer": 0,
        "explanation": "4y = 8 − 3x → divide by 4.",
    },
    {
        "id": "u5_wp8", "category": "word_problems",
        "question": "A number increased by 8 equals triple the number minus 4. Equation?",
        "options": ["x + 8 = 3x − 4", "x + 8 = 3x + 4", "8x = 3x − 4", "x − 8 = 3x − 4"],
        "answer": 0,
        "explanation": "x + 8 = 3x − 4 → 12 = 2x → x = 6.",
    },
]
