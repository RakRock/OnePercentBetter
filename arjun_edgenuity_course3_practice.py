"""
Edgenuity Course 3 — daily practice question banks and generators (Units 1–2).
"""

from __future__ import annotations

import random
from pathlib import Path

from arjun_edgenuity_course3_unit2_practice import (
    UNIT2_CATEGORIES,
    UNIT2_CATEGORY_ACTIVITY,
    UNIT2_QUESTION_BANK,
    UNIT2_REVISION_TIPS,
)

ROOT = Path(__file__).resolve().parent
PRACTICE_IMG_BY_UNIT = {
    1: ROOT / "ArjunEdgenuityCourse3" / "images" / "unit_1" / "practice",
    2: ROOT / "ArjunEdgenuityCourse3" / "images" / "unit_2" / "practice",
}
PRACTICE_IMG = PRACTICE_IMG_BY_UNIT[1]

CATEGORIES = {
    "coordinate_plane": {
        "name": "Coordinate Plane",
        "emoji": "📍",
        "color": "#3b82f6",
        "weight": 1,
    },
    "function_definition": {
        "name": "Functions",
        "emoji": "🔀",
        "color": "#8b5cf6",
        "weight": 2,
    },
    "graph_behavior": {
        "name": "Graph Behavior",
        "emoji": "📈",
        "color": "#10b981",
        "weight": 1,
    },
    "linear_equations": {
        "name": "Linear Equations",
        "emoji": "📊",
        "color": "#f59e0b",
        "weight": 1,
    },
    "word_problems": {
        "name": "Word Problems",
        "emoji": "🌍",
        "color": "#ef4444",
        "weight": 2,
    },
    "table_completion": {
        "name": "Tables",
        "emoji": "📋",
        "color": "#06b6d4",
        "weight": 1,
    },
}

# Maps practice categories to Unit 1 lesson activities for revision links.
CATEGORY_ACTIVITY: dict[str, str] = {
    "coordinate_plane": "activity_1_coordinate_plane",
    "function_definition": "activity_2_relations_functions",
    "graph_behavior": "activity_3_graph_behavior",
    "linear_equations": "activity_4_linear_equations",
    "table_completion": "activity_5_completing_tables",
    "word_problems": "activity_6_word_problems",
}

REVISION_TIPS: dict[str, str] = {
    "coordinate_plane": "Read coordinates from the graph — x first (left/right), then y (up/down).",
    "function_definition": "Use the vertical line test: each x-value must have only one y-value.",
    "graph_behavior": "Describe each segment as increasing, decreasing, or constant before picking an answer.",
    "linear_equations": "Find the unit rate (change in y ÷ change in x), then check for a starting fee.",
    "table_completion": "Plug values into the equation step by step, or extend the pattern in the table.",
    "word_problems": "Write an equation for each plan, then compare costs or solve for the unknown.",
}

STRENGTH_THRESHOLD_PCT = 80

QUESTION_BANK: list[dict] = [
    # ── Coordinate plane (8) ──
    {
        "id": "cp1", "category": "coordinate_plane",
        "question": "Use the graph. What are the coordinates of point P?",
        "options": ["(3, −4)", "(−4, 3)", "(4, −3)", "(−3, 4)"],
        "answer": 1,
        "explanation": "4 left means x = −4; 3 up means y = 3 → (−4, 3).",
        "image": "practice_coord_read_p",
    },
    {
        "id": "cp2", "category": "coordinate_plane",
        "question": "Use the graph. In which quadrant is the point shown?",
        "options": ["Quadrant I", "Quadrant II", "Quadrant III", "Quadrant IV"],
        "answer": 1,
        "explanation": "x is negative, y is positive → Quadrant II.",
        "image": "practice_coord_q2_ii",
    },
    {
        "id": "cp3", "category": "coordinate_plane",
        "question": "Which point is located on the x-axis?",
        "options": ["(−5, 1)", "(0, −5)", "(2, 2)", "(1, 0)"],
        "answer": 3,
        "explanation": "On the x-axis, y = 0, so (1, 0) works.",
    },
    {
        "id": "cp4", "category": "coordinate_plane",
        "question": "Use the graph. In which quadrant is the point shown?",
        "options": ["Quadrant I", "Quadrant II", "Quadrant III", "Quadrant IV"],
        "answer": 3,
        "explanation": "Quadrant IV: x > 0 and y < 0.",
        "image": "practice_coord_q4",
    },
    {
        "id": "cp5", "category": "coordinate_plane",
        "question": "Which point is in quadrant III?",
        "options": ["(3, 2)", "(−3, 5)", "(−2, −4)", "(2, −4)"],
        "answer": 2,
        "explanation": "Both coordinates negative → Quadrant III.",
    },
    {
        "id": "cp6", "category": "coordinate_plane",
        "question": "Which point lies on the y-axis?",
        "options": ["(5, 0)", "(0, −5)", "(5, 5)", "(−5, −5)"],
        "answer": 1,
        "explanation": "On the y-axis, x = 0 → (0, −5).",
    },
    {
        "id": "cp7", "category": "coordinate_plane",
        "question": "What is the x-coordinate of the point (7, −2)?",
        "options": ["−2", "7", "5", "9"],
        "answer": 1,
        "explanation": "In (x, y), the x-coordinate is 7.",
    },
    {
        "id": "cp8", "category": "coordinate_plane",
        "question": "The origin has coordinates:",
        "options": ["(1, 1)", "(0, 1)", "(1, 0)", "(0, 0)"],
        "answer": 3,
        "explanation": "The origin is where the axes cross: (0, 0).",
    },
    # ── Function definition (10) ──
    {
        "id": "fn1", "category": "function_definition",
        "question": "Fun Zone offers weekend and weekday prices for each package number. Is (package number, price) a function?",
        "options": [
            "Yes — every package has a price",
            "No — each package number has two different prices",
            "Yes — weekend is always $50 more",
            "No — two packages cost $180",
        ],
        "answer": 1,
        "explanation": "Same package number (input) maps to two prices (outputs) → not a function.",
    },
    {
        "id": "fn2", "category": "function_definition",
        "question": "Removing which point makes the relation a function? Points include (−2, 1) and (−2, −3).",
        "options": ["(−4, 3)", "(0, 4)", "(1, 1)", "(−2, 1)"],
        "answer": 3,
        "explanation": "Remove one of the duplicate x = −2 points.",
        "image": "practice_vlt_remove",
    },
    {
        "id": "fn3", "category": "function_definition",
        "question": "Which equation is a function of x?",
        "options": ["x = y² + 9", "x² = y", "x = 5", "x² = y² + 16"],
        "answer": 1,
        "explanation": "x² = y means y = x² — each x gives one y.",
    },
    {
        "id": "fn4", "category": "function_definition",
        "question": "Which table represents a function of x?",
        "options": [
            "x: −1,2,2,3  y: 7,−9,8,−4",
            "x: −8,−8,1,1  y: −9,2,−9,2",
            "x: −3,−2,4,7  y: −1,5,0,−1",
            "x: −5,−5,−5,−5  y: 1,7,−9,2",
        ],
        "answer": 2,
        "explanation": "Only the third table has each x once.",
        "image": "practice_function_scatter",
    },
    {
        "id": "fn5", "category": "function_definition",
        "question": "A relation has inputs 1→5 and 1→8. Is it a function?",
        "options": ["Yes", "No", "Only on weekends", "Cannot tell"],
        "answer": 1,
        "explanation": "Input 1 has two outputs → not a function.",
    },
    {
        "id": "fn6", "category": "function_definition",
        "question": "The vertical line x = 3 crosses a graph at two points. Is the graph a function of x?",
        "options": ["Yes", "No", "Only if y > 0", "Only if x > 0"],
        "answer": 1,
        "explanation": "Vertical line test fails → not a function.",
    },
    {
        "id": "fn7", "category": "function_definition",
        "question": "Which set of ordered pairs is a function?",
        "options": [
            "{(2,3), (2,5), (4,1)}",
            "{(0,1), (3,4), (−1,2)}",
            "{(5,2), (5,7), (5,9)}",
            "{(1,2), (1,3), (2,2)}",
        ],
        "answer": 1,
        "explanation": "Each x appears once in the second set.",
    },
    {
        "id": "fn8", "category": "function_definition",
        "question": "A table shows the same rule for weekday and weekend prices. Is (day type, price) a function of package number alone?",
        "options": [
            "Yes — the rule is consistent",
            "No — you need both package AND day type as input",
            "Yes — prices always increase",
            "No — because prices differ",
        ],
        "answer": 1,
        "explanation": "For a function of package number only, each package must have ONE price.",
    },
    {
        "id": "fn9", "category": "function_definition",
        "question": "Which graph passes the vertical line test?",
        "options": [
            "A circle",
            "A vertical line x = 2",
            "A parabola y = x²",
            "Sideways parabola x = y²",
        ],
        "answer": 2,
        "explanation": "y = x² gives one y for each x.",
    },
    {
        "id": "fn10", "category": "function_definition",
        "question": "If each student ID maps to exactly one grade, is (student ID, grade) a function?",
        "options": ["Yes", "No", "Only for seniors", "Only if grades differ"],
        "answer": 0,
        "explanation": "One input (ID) → one output (grade) → function.",
    },
    # ── Graph behavior (8) ──
    {
        "id": "gb1", "category": "graph_behavior",
        "question": "Between A and C, a graph rises then stays flat. How does it change?",
        "options": [
            "Decreases, then constant",
            "Increases, then constant",
            "Increases, then decreases",
            "Decreases, then increases",
        ],
        "answer": 1,
        "explanation": "Rising = increasing; flat = constant.",
        "image": "practice_segment_graph",
    },
    {
        "id": "gb2", "category": "graph_behavior",
        "question": "Which best describes a parabola opening upward?",
        "options": [
            "Increasing everywhere",
            "Decreasing everywhere",
            "Decreasing, then increasing",
            "Increasing, then decreasing",
        ],
        "answer": 2,
        "explanation": "Left of vertex decreases; right of vertex increases.",
        "image": "practice_parabola",
    },
    {
        "id": "gb3", "category": "graph_behavior",
        "question": "On a distance-time graph, a horizontal segment means:",
        "options": ["Speeding up", "Slowing down", "Not moving", "Returning home"],
        "answer": 2,
        "explanation": "Distance not changing → stopped.",
        "image": "practice_distance_time",
    },
    {
        "id": "gb4", "category": "graph_behavior",
        "question": "Mary waits at a traffic light. On her distance-time graph this looks like:",
        "options": ["Steep rise", "Horizontal line", "Steep drop", "Curved rise"],
        "answer": 1,
        "explanation": "Time passes but distance stays the same → horizontal.",
        "image": "practice_distance_time",
    },
    {
        "id": "gb5", "category": "graph_behavior",
        "question": "From point A to B on an upward curve, the graph:",
        "options": ["Decreases", "Increases", "Stays constant", "Increases then decreases"],
        "answer": 1,
        "explanation": "Moving right and up → increasing.",
        "image": "practice_increasing_curve",
    },
    {
        "id": "gb6", "category": "graph_behavior",
        "question": "A graph drops from B to C. This segment is:",
        "options": ["Increasing", "Decreasing", "Constant", "Undefined"],
        "answer": 1,
        "explanation": "y goes down as x increases → decreasing.",
        "image": "practice_segment_cd",
    },
    {
        "id": "gb7", "category": "graph_behavior",
        "question": "Riding a bike at constant speed on a distance-time graph looks like:",
        "options": ["Horizontal", "Straight sloped line", "Parabola", "Vertical line"],
        "answer": 1,
        "explanation": "Steady speed → straight line with positive slope.",
    },
    {
        "id": "gb8", "category": "graph_behavior",
        "question": "Between C and D the graph is flat. The output is:",
        "options": ["Increasing", "Decreasing", "Constant", "Changing rapidly"],
        "answer": 2,
        "explanation": "Flat segment → constant.",
        "image": "practice_segment_bc",
    },
    # ── Linear equations (10) ──
    {
        "id": "le1", "category": "linear_equations",
        "question": (
            "A school club sells tickets for a talent show fundraiser. "
            "The graph shows how many tickets were sold and the total profit. "
            "How much profit does the club earn for each ticket sold?"
        ),
        "options": ["$8 per ticket", "$16 per ticket", "$9 per ticket", "$18 per ticket"],
        "answer": 2,
        "explanation": "Profit rises $18 for 2 tickets → $9 profit per ticket.",
        "image": "practice_tickets_graph",
    },
    {
        "id": "le2", "category": "linear_equations",
        "question": (
            "Maya builds square garden beds. The graph shows each bed's side length "
            "and perimeter. Which equation describes the relationship?"
        ),
        "options": ["perimeter = side ÷ 4", "perimeter = side − 13.5", "perimeter = side + 13.5", "perimeter = 4 × side"],
        "answer": 3,
        "explanation": "Perimeter = 4 × side length → y = 4x.",
        "image": "practice_perimeter_graph",
    },
    {
        "id": "le3", "category": "linear_equations",
        "question": (
            "Jaxon pays for items using a $10 bill. The graph shows the item cost "
            "and the change he gets back. Which equation matches the graph?"
        ),
        "options": ["change = 10 + cost", "change = −cost − 10", "change = cost − 10", "change = 10 − cost"],
        "answer": 3,
        "explanation": "He starts with $10 change and loses $1 for each $1 spent → change = 10 − cost.",
        "image": "practice_jaxon_graph",
    },
    {
        "id": "le4", "category": "linear_equations",
        "question": (
            "Carey earns $9.75 per hour at a weekend job. The graph shows hours worked "
            "and total pay. How much will Carey earn for 3 hours?"
        ),
        "options": ["$12.75", "$29.25", "$19.50", "$9.75"],
        "answer": 1,
        "explanation": "9.75 × 3 = $29.25.",
        "image": "practice_carey_graph",
    },
    {
        "id": "le5", "category": "linear_equations",
        "question": (
            "A water station gives 3 bottles to each runner who finishes a charity 5K "
            "(no bonus bottles at the start). Which equation relates runners (r) to bottles (b)?"
        ),
        "options": ["b = 2r", "b = 3r", "b = r + 6", "b = 6r"],
        "answer": 1,
        "explanation": "3 bottles per runner with no starting amount → b = 3r.",
    },
    {
        "id": "le6", "category": "linear_equations",
        "question": (
            "A babysitter charges a $5 booking fee plus $2 for each hour. "
            "The graph shows hours worked vs total pay. Which equation matches?"
        ),
        "options": ["pay = 2 × hours", "pay = 2 × hours + 5", "pay = 5 × hours + 2", "pay = hours + 7"],
        "answer": 1,
        "explanation": "$5 flat fee plus $2/hour → pay = 2h + 5.",
        "image": "practice_slope_line",
    },
    {
        "id": "le7", "category": "linear_equations",
        "question": (
            "A store tracks a loyalty reward that grows by $1 for every $1 spent above a baseline. "
            "The graph shows the relationship. Which data table matches the line?"
        ),
        "options": [
            "Inputs −2, 0, 2 → outputs −3, −1, 1",
            "Inputs −2, 0, 2 → outputs −3, 1, 1",
            "Inputs −3, −1, 1 → outputs −2, 0, 2",
            "Inputs −3, 0, 1 → outputs −2, 0, 2",
        ],
        "answer": 2,
        "explanation": "Each output is 1 more than its input: −3+1=−2, −1+1=0, 1+1=2.",
        "image": "practice_table_line",
    },
    {
        "id": "le8", "category": "linear_equations",
        "question": (
            "Jordan gets paid $12 per hour mowing lawns. How much does Jordan earn for 5 hours?"
        ),
        "options": ["$17", "$48", "$60", "$72"],
        "answer": 2,
        "explanation": "12 × 5 = $60.",
    },
    {
        "id": "le9", "category": "linear_equations",
        "question": (
            "Which real-world situation is best modeled by perimeter = 4 × side length?"
        ),
        "options": [
            "Area of a square garden from its side",
            "Perimeter of a square garden from its side",
            "Cost with a $4 service fee",
            "Temperature dropping each hour",
        ],
        "answer": 1,
        "explanation": "Perimeter = 4 × side length for any square.",
    },
    {
        "id": "le10", "category": "linear_equations",
        "question": (
            "You pay with a $10 bill and receive $1 less change for each extra dollar the item costs. "
            "Which equation models change (c) vs item cost (x)?"
        ),
        "options": ["c = 10 + x", "c = 10 − x", "c = x − 10", "c = −10x"],
        "answer": 1,
        "explanation": "Start with $10 change; lose $1 per $1 of cost → c = 10 − x.",
        "image": "practice_jaxon_graph",
    },
    # ── Table completion (8) ──
    {
        "id": "tc1", "category": "table_completion",
        "question": (
            "A craft store sells ribbon by the yard. The total cost is $5 for setup plus "
            "$3 for each yard (r = 3c + 5). How much does 12 yards cost?"
        ),
        "options": ["$35", "$41", "$44", "$12"],
        "answer": 1,
        "explanation": "3(12) + 5 = $41.",
    },
    {
        "id": "tc2", "category": "table_completion",
        "question": (
            "A tutor charges a $1 scheduling fee plus $2 for each hour of tutoring. "
            "How much does a 7-hour session cost?"
        ),
        "options": ["$14", "$15", "$16", "$8"],
        "answer": 1,
        "explanation": "2(7) + 1 = $15.",
    },
    {
        "id": "tc3", "category": "table_completion",
        "question": (
            "On a road trip, a car starts with 12 gallons of gas. After 20 miles, "
            "11 gallons remain. At what rate is the car using gas?"
        ),
        "options": ["1 gallon per 10 miles", "1 gallon per 20 miles", "2 gallons per 20 miles", "12 gallons total"],
        "answer": 1,
        "explanation": "The car uses 1 gallon every 20 miles.",
        "image": "practice_gas_tank_graph",
    },
    {
        "id": "tc4", "category": "table_completion",
        "question": (
            "The temperature drops 6°F each hour starting from 2°F at midnight. "
            "What is the temperature after 5 hours?"
        ),
        "options": ["−28°F", "32°F", "−30°F", "28°F"],
        "answer": 0,
        "explanation": "−6(5) + 2 = −28°F.",
    },
    {
        "id": "tc5", "category": "table_completion",
        "question": (
            "A bake sale earns $7 with no items sold, then $2 for each item sold. "
            "When 0 items are sold, profit is $7; when 3 items are sold, profit is $13. "
            "What is the profit when 1 item is sold?"
        ),
        "options": ["$9", "$10", "$11", "$8"],
        "answer": 0,
        "explanation": "Profit = 2 × items + 7 → 2(1) + 7 = $9.",
    },
    {
        "id": "tc6", "category": "table_completion",
        "question": (
            "Using the ribbon rule (total = 3 × yards + $5): 6 yards costs $23 and "
            "8 yards costs $29. How much does 0 yards cost (setup fee only)?"
        ),
        "options": ["$0", "$5", "$8", "$3"],
        "answer": 1,
        "explanation": "3(0) + 5 = $5 setup fee.",
    },
    {
        "id": "tc7", "category": "table_completion",
        "question": (
            "A car with a 12-gallon tank uses 1 gallon every 20 miles. "
            "After 100 miles, 7 gallons remain. How far can the car go on a full tank?"
        ),
        "options": ["200 miles", "220 miles", "240 miles", "120 miles"],
        "answer": 2,
        "explanation": "12 gallons × 20 miles per gallon = 240 miles.",
        "image": "practice_gas_tank_graph",
    },
    {
        "id": "tc8", "category": "table_completion",
        "question": (
            "A concession stand sells snacks for $5 each (no entry fee). "
            "How much is spent on 4 snacks?"
        ),
        "options": ["$9", "$20", "$25", "$1"],
        "answer": 1,
        "explanation": "5 × 4 = $20.",
    },
    # ── Word problems (8) ──
    {
        "id": "wp1", "category": "word_problems",
        "question": (
            "Two movie rental stores are compared. Movies Plus charges a $10 membership fee "
            "plus $2 per movie. Movies For Less has no membership fee and charges $3 per movie. "
            "If you rent 15 movies in a month, which store costs more?"
        ),
        "options": [
            "Both stores cost the same",
            "Movies Plus costs $6 more",
            "Movies For Less costs $5 more",
            "Movies Plus costs $5 more",
        ],
        "answer": 2,
        "explanation": "Movies Plus: $10 + 2(15) = $40. Movies For Less: 3(15) = $45 → For Less costs $5 more.",
        "image": "practice_movie_compare",
    },
    {
        "id": "wp2", "category": "word_problems",
        "question": (
            "Li has $125 in a savings account and deposits $45 each month. "
            "What is the fewest whole months needed to have at least $360?"
        ),
        "options": ["5 months", "6 months", "8 months", "9 months"],
        "answer": 1,
        "explanation": "125 + 45(6) = $395, which meets the $360 goal.",
        "image": "practice_bank_graph",
    },
    {
        "id": "wp3", "category": "word_problems",
        "question": (
            "Sarah runs a craft demo. The cost is $10 plus $1 per person. "
            "For 5 people the cost is $15; for 8 people it is $18. "
            "How many people attended if the total cost was $60?"
        ),
        "options": ["50 people", "70 people", "30 people", "20 people"],
        "answer": 0,
        "explanation": "Cost = people + 10 → 60 = people + 10 → 50 people.",
    },
    {
        "id": "wp4", "category": "word_problems",
        "question": (
            "Two phone plans are offered. Plan A costs $20 per month plus $0.10 per minute of talk time. "
            "Plan B has no monthly fee and costs $0.25 per minute. "
            "After how many minutes of talk time will both plans cost the same amount?"
        ),
        "options": ["100 minutes", "120 minutes", "133 minutes", "200 minutes"],
        "answer": 2,
        "explanation": "Set costs equal: 20 + 0.10m = 0.25m → 20 = 0.15m → m ≈ 133 minutes.",
    },
    {
        "id": "wp5", "category": "word_problems",
        "question": (
            "A streaming service charges a $7 monthly fee plus $4 per extra profile. "
            "If the total bill is $31, how many extra profiles were added?"
        ),
        "options": ["4 profiles", "5 profiles", "6 profiles", "7 profiles"],
        "answer": 2,
        "explanation": "31 = 4 × profiles + 7 → 4 × profiles = 24 → 6 profiles.",
    },
    {
        "id": "wp6", "category": "word_problems",
        "question": (
            "An amusement park charges an $8 entry fee plus $3 per ride. "
            "How much does it cost for 10 rides?"
        ),
        "options": ["$30", "$38", "$80", "$11"],
        "answer": 1,
        "explanation": "8 + 3(10) = $38.",
    },
    {
        "id": "wp7", "category": "word_problems",
        "question": (
            "A phone repair shop charges $12 for diagnostics plus $2 per hour of labor. "
            "How many hours of labor if the total bill is $36?"
        ),
        "options": ["10 hours", "12 hours", "14 hours", "24 hours"],
        "answer": 1,
        "explanation": "36 = 12 + 2 × hours → 2 × hours = 24 → 12 hours.",
    },
    {
        "id": "wp8", "category": "word_problems",
        "question": (
            "Sarah's craft demo costs $10 plus $1 per person (cost = people + 10). "
            "What is the cost for 40 people?"
        ),
        "options": ["$40", "$50", "$30", "$45"],
        "answer": 1,
        "explanation": "40 + 10 = $50.",
    },
    # ── Two-plan comparison (6) ──
    {
        "id": "tp1", "category": "word_problems",
        "question": (
            "Movies Plus charges a $10 membership fee plus $2 per movie rented. "
            "Movies For Less has no membership fee and charges $3 per movie. "
            "How many movies must you rent before both stores cost the same amount?"
        ),
        "options": ["5 movies", "10 movies", "15 movies", "20 movies"],
        "answer": 1,
        "explanation": "Set costs equal: 10 + 2m = 3m → 10 = m → 10 movies.",
    },
    {
        "id": "tp2", "category": "word_problems",
        "question": (
            "Movies Plus charges a $10 membership fee plus $2 per movie. "
            "Movies For Less charges $3 per movie with no membership fee. "
            "If you rent zero movies, how much more does Movies Plus cost?"
        ),
        "options": ["$0 more", "$10 more", "$3 more", "$13 more"],
        "answer": 1,
        "explanation": "With 0 movies: Movies Plus costs $10; Movies For Less costs $0 → Plus costs $10 more.",
    },
    {
        "id": "tp3", "category": "word_problems",
        "question": (
            "Movies Plus charges $10 plus $2 per movie. Movies For Less charges $3 per movie. "
            "If you rent 4 movies, how much more does Movies Plus cost than Movies For Less?"
        ),
        "options": [
            "Movies Plus costs $6 more",
            "Movies For Less costs $6 more",
            "Both cost the same",
            "Movies Plus costs $4 more",
        ],
        "answer": 0,
        "explanation": "Movies Plus: $10 + 2(4) = $18. Movies For Less: 3(4) = $12. Difference: $6.",
    },
    {
        "id": "tp4", "category": "word_problems",
        "question": (
            "Movies Plus charges a $10 membership fee plus $2 per movie. "
            "Movies For Less charges $3 per movie with no fee. "
            "Which store is cheaper if you rent 20 movies in a month?"
        ),
        "options": ["Movies Plus", "Movies For Less", "Both cost the same", "Cannot tell"],
        "answer": 0,
        "explanation": "Movies Plus: $10 + 2(20) = $50. Movies For Less: 3(20) = $60 → Movies Plus is cheaper.",
    },
    {
        "id": "tp5", "category": "word_problems",
        "question": (
            "Mia is comparing two cell phone plans. Plan A charges a $30 monthly fee "
            "plus $0.05 per text message. Plan B has no monthly fee and charges $0.20 per text. "
            "If Mia sends 200 texts in a month, will both plans cost the same amount?"
        ),
        "options": [
            "Yes — both plans cost $40",
            "No — the plans cost different amounts",
            "No — Plan A is cheaper",
            "No — Plan B is cheaper",
        ],
        "answer": 0,
        "explanation": "Plan A: $30 + 0.05(200) = $40. Plan B: 0.20(200) = $40 → same cost.",
    },
    {
        "id": "tp6", "category": "word_problems",
        "question": (
            "Gym A charges a flat $50 monthly membership. Gym B has no monthly fee "
            "but charges $10 per visit. Which gym is cheaper if you go 3 times in a month?"
        ),
        "options": ["Gym A", "Gym B", "Both cost the same", "Need more information"],
        "answer": 1,
        "explanation": "Gym A: $50. Gym B: 3 × $10 = $30 → Gym B is cheaper.",
    },
    # ── Graph / diagram questions (exam-style) ──
    {
        "id": "gq1", "category": "coordinate_plane",
        "question": "Use the graph. What are the coordinates of point P?",
        "options": ["(−3, 4)", "(−4, 3)", "(4, −3)", "(3, −4)"],
        "answer": 1,
        "explanation": "P is 4 left (x = −4) and 3 up (y = 3).",
        "image": "practice_coord_read_p",
    },
    {
        "id": "gq2", "category": "coordinate_plane",
        "question": "Use the graph. In which quadrant is the point shown?",
        "options": ["Quadrant I", "Quadrant II", "Quadrant III", "Quadrant IV"],
        "answer": 1,
        "explanation": "The point (−3, 5) has x < 0 and y > 0 → Quadrant II.",
        "image": "practice_coord_q2_ii",
    },
    {
        "id": "gq3", "category": "coordinate_plane",
        "question": "Use the graph. In which quadrant is the point shown?",
        "options": ["Quadrant I", "Quadrant II", "Quadrant III", "Quadrant IV"],
        "answer": 3,
        "explanation": "The point (2, −4) has x > 0 and y < 0 → Quadrant IV.",
        "image": "practice_coord_q4",
    },
    {
        "id": "gq4", "category": "coordinate_plane",
        "question": "Use the graph. Which labeled point is on the x-axis?",
        "options": ["Point A", "Point B", "Point C", "Point D"],
        "answer": 3,
        "explanation": "Point D at (1, 0) has y = 0, so it lies on the x-axis.",
        "image": "practice_coord_xaxis",
    },
    {
        "id": "gq5", "category": "function_definition",
        "question": "Use the graph. Removing which point makes the relation a function of x?",
        "options": ["(−4, 3)", "(0, 4)", "(1, 1)", "(−2, 1)"],
        "answer": 3,
        "explanation": "x = −2 appears twice. Remove (−2, 1) or (−2, −3) to fix it.",
        "image": "practice_vlt_remove",
    },
    {
        "id": "gq6", "category": "function_definition",
        "question": "Use the graph. Is this relation a function of x?",
        "options": [
            "Yes — each x appears once",
            "No — a vertical line hits twice",
            "Yes — all y values differ",
            "Cannot tell from the graph",
        ],
        "answer": 0,
        "explanation": "Each x-value has exactly one y-value → function.",
        "image": "practice_vlt_scatter",
    },
    {
        "id": "gq7", "category": "function_definition",
        "question": "Use the graph. Does this set of points pass the vertical line test?",
        "options": ["Yes", "No — x = −2 has two outputs", "Only for x > 0", "Only for x < 0"],
        "answer": 1,
        "explanation": "A vertical line at x = −2 crosses two points → not a function.",
        "image": "practice_vlt_fail",
    },
    {
        "id": "gq8", "category": "graph_behavior",
        "question": "Use the graph. How does the graph change between A and C?",
        "options": [
            "Decreases, then constant",
            "Increases, then constant",
            "Increases, then decreases",
            "Constant, then increases",
        ],
        "answer": 1,
        "explanation": "A → B rises (increasing); B → C is flat (constant).",
        "image": "practice_segment_graph",
    },
    {
        "id": "gq9", "category": "graph_behavior",
        "question": "Use the graph. How does the graph change from B to C?",
        "options": ["Increasing", "Decreasing", "Constant", "Increasing then decreasing"],
        "answer": 2,
        "explanation": "From B to C the graph is horizontal → constant.",
        "image": "practice_segment_bc",
    },
    {
        "id": "gq10", "category": "graph_behavior",
        "question": "Use the graph. How does the graph change from C to D?",
        "options": ["Increasing", "Decreasing", "Constant", "Increasing then decreasing"],
        "answer": 1,
        "explanation": "From C to D the graph falls → decreasing.",
        "image": "practice_segment_cd",
    },
    {
        "id": "gq11", "category": "graph_behavior",
        "question": "Use the graph. Which best describes this parabola?",
        "options": [
            "Increasing everywhere",
            "Decreasing everywhere",
            "Decreasing, then increasing",
            "Increasing, then decreasing",
        ],
        "answer": 2,
        "explanation": "Left of the vertex it decreases; right of the vertex it increases.",
        "image": "practice_parabola",
    },
    {
        "id": "gq12", "category": "graph_behavior",
        "question": "Use the distance-time graph. Which part shows no change in distance?",
        "options": [
            "The first rising segment",
            "The flat segment (stopped)",
            "The last rising segment",
            "The entire graph",
        ],
        "answer": 1,
        "explanation": "A horizontal segment means distance is not changing — stopped.",
        "image": "practice_distance_time",
    },
    {
        "id": "gq13", "category": "graph_behavior",
        "question": "Use the graph. From point A to B, the graph:",
        "options": ["Decreases", "Increases", "Stays constant", "Increases then decreases"],
        "answer": 1,
        "explanation": "Moving from A to B along the curve, y increases.",
        "image": "practice_increasing_curve",
    },
    {
        "id": "gq14", "category": "linear_equations",
        "question": (
            "Jaxon pays with a $10 bill. The graph shows item cost vs change received. "
            "Which equation represents the line?"
        ),
        "options": ["change = 10 + cost", "change = −cost − 10", "change = cost − 10", "change = 10 − cost"],
        "answer": 3,
        "explanation": "Change starts at $10 and drops $1 for each $1 spent → change = 10 − cost.",
        "image": "practice_jaxon_graph",
    },
    {
        "id": "gq15", "category": "linear_equations",
        "question": (
            "A store loyalty reward increases by $1 for each $1 spent above a baseline. "
            "The graph shows input vs output values. Which table matches the plotted points?"
        ),
        "options": [
            "Inputs −2, 0, 2 → outputs −3, −1, 1",
            "Inputs −3, −1, 1 → outputs −2, 0, 2",
            "Inputs −3, 0, 1 → outputs −2, 0, 2",
            "Inputs −2, −1, 2 → outputs −3, 0, 1",
        ],
        "answer": 1,
        "explanation": "Each output is 1 more than its input: −3+1=−2, −1+1=0, 1+1=2.",
        "image": "practice_table_line",
    },
    {
        "id": "gq16", "category": "linear_equations",
        "question": (
            "A school club sells talent show tickets. The graph shows tickets sold vs total profit. "
            "How much profit does the club earn per ticket?"
        ),
        "options": ["$8 per ticket", "$16 per ticket", "$9 per ticket", "$18 per ticket"],
        "answer": 2,
        "explanation": "Profit rises $36 for 4 tickets → $9 profit per ticket.",
        "image": "practice_tickets_graph",
    },
    {
        "id": "gq17", "category": "linear_equations",
        "question": (
            "Maya builds square garden beds. The graph shows side length vs perimeter. "
            "Which equation fits the data?"
        ),
        "options": ["perimeter = side ÷ 4", "perimeter = 4 × side", "perimeter = side + 4", "perimeter = 2 × side"],
        "answer": 1,
        "explanation": "Perimeter = 4 × side length for a square.",
        "image": "practice_perimeter_graph",
    },
    {
        "id": "gq18", "category": "linear_equations",
        "question": (
            "A part-time job pays a $5 starting bonus plus $2 per hour. "
            "The graph shows hours worked vs total pay. Which equation matches?"
        ),
        "options": ["pay = 2 × hours", "pay = 2 × hours + 5", "pay = 5 × hours + 2", "pay = hours + 7"],
        "answer": 1,
        "explanation": "$5 bonus plus $2/hour → pay = 2 × hours + 5.",
        "image": "practice_slope_line",
    },
    {
        "id": "gq19", "category": "word_problems",
        "question": "Use the graph. For 15 movies, which rental plan costs more?",
        "options": [
            "Same cost",
            "Movies Plus costs $5 more",
            "Movies For Less costs $5 more",
            "Movies Plus costs $10 more",
        ],
        "answer": 2,
        "explanation": "At x = 15: Plus = $40, For Less = $45.",
        "image": "practice_movie_compare",
    },
    {
        "id": "gq20", "category": "table_completion",
        "question": "Use the graph. How many miles can the car travel on a full tank?",
        "options": ["120 miles", "200 miles", "240 miles", "100 miles"],
        "answer": 2,
        "explanation": "12 gallons × 20 miles/gallon = 240 miles.",
        "image": "practice_gas_tank_graph",
    },
    {
        "id": "gq21", "category": "word_problems",
        "question": "Use the graph. Li starts with $125 and deposits $45/month. Minimum months to reach $360?",
        "options": ["5", "6", "7", "8"],
        "answer": 1,
        "explanation": "125 + 45(6) = 395 ≥ 360.",
        "image": "practice_bank_graph",
    },
    {
        "id": "gq22", "category": "function_definition",
        "question": "Use the graph. Which statement is true?",
        "options": [
            "It is a function — each x has one y",
            "Not a function — duplicate x at −2",
            "Function because points are spread out",
            "Not a function — too few points",
        ],
        "answer": 0,
        "explanation": "Every x-value appears once in the green scatter → function.",
        "image": "practice_function_scatter",
    },
]

GRAPH_MIN_PER_SESSION = 9
GRAPH_MIN_BY_UNIT = {1: 9, 2: 9}
RECENT_SESSIONS_TO_AVOID = 2

QUESTION_BANK_BY_UNIT: dict[int, list[dict]] = {}
CATEGORIES_BY_UNIT: dict[int, dict] = {}
CATEGORY_ACTIVITY_BY_UNIT: dict[int, dict[str, str]] = {}
REVISION_TIPS_BY_UNIT: dict[int, dict[str, str]] = {}

QUESTION_BANK_BY_UNIT[1] = QUESTION_BANK
CATEGORIES_BY_UNIT[1] = CATEGORIES
CATEGORY_ACTIVITY_BY_UNIT[1] = CATEGORY_ACTIVITY
REVISION_TIPS_BY_UNIT[1] = REVISION_TIPS

QUESTION_BANK_BY_UNIT[2] = UNIT2_QUESTION_BANK
CATEGORIES_BY_UNIT[2] = UNIT2_CATEGORIES
CATEGORY_ACTIVITY_BY_UNIT[2] = UNIT2_CATEGORY_ACTIVITY
REVISION_TIPS_BY_UNIT[2] = UNIT2_REVISION_TIPS


def _gen_quadrant_question() -> dict:
    x, y = random.choice([(3, 2), (-3, 5), (-2, -4), (2, -4), (-1, 6), (4, -3)])
    quads = {1: "Quadrant I", 2: "Quadrant II", 3: "Quadrant III", 4: "Quadrant IV"}
    qnum = 1 if x > 0 and y > 0 else 2 if x < 0 and y > 0 else 3 if x < 0 and y < 0 else 4
    wrong = [quads[k] for k in quads if k != qnum]
    random.shuffle(wrong)
    opts = wrong[:3] + [quads[qnum]]
    random.shuffle(opts)
    return {
        "id": f"gen_cp_{x}_{y}",
        "category": "coordinate_plane",
        "question": f"In which quadrant is ({x}, {y})?",
        "options": opts,
        "answer": opts.index(quads[qnum]),
        "explanation": f"x={'+' if x > 0 else '-'}, y={'+' if y > 0 else '-'} → {quads[qnum]}.",
    }


def _gen_function_table_question() -> dict:
    is_function = random.choice([True, False])
    if is_function:
        xs = random.sample(range(-5, 6), 4)
        pairs = [(x, random.randint(-9, 9)) for x in xs]
    else:
        x_dup = random.randint(-3, 3)
        pairs = [(x_dup, random.randint(-9, 9)), (x_dup, random.randint(-9, 9) + random.choice([-3, 3, 5]))]
        xs = random.sample([n for n in range(-5, 6) if n != x_dup], 2)
        pairs += [(x, random.randint(-9, 9)) for x in xs]
    table_str = ", ".join(f"({x},{y})" for x, y in pairs)
    correct = "Yes — each x appears once" if is_function else "No — an x-value repeats with different y"
    wrong = [
        "Yes — outputs are all different",
        "No — too many points",
        "Yes — because y values differ",
        "No — not enough data",
    ]
    opts = [correct] + [w for w in wrong if w != correct][:3]
    random.shuffle(opts)
    return {
        "id": f"gen_fn_{hash(table_str) % 10000}",
        "category": "function_definition",
        "question": f"Is this relation a function of x? {table_str}",
        "options": opts,
        "answer": opts.index(correct),
        "explanation": correct,
    }


def _gen_linear_table_question() -> dict:
    m = random.choice([2, 3, 4, 5, 9, 12])
    b = random.choice([0, 1, 5, 10])
    x = random.randint(2, 12)
    y = m * x + b
    wrong = [str(y + d) for d in random.sample([-5, -3, -2, 2, 3, 5, 7], 3)]
    opts = wrong + [str(y)]
    random.shuffle(opts)
    if b == 0:
        if random.choice([True, False]):
            question = f"Jordan earns ${m} per hour mowing lawns. How much for {x} hours?"
        else:
            question = f"Concession snacks cost ${m} each (no entry fee). How much for {x} snacks?"
    else:
        question = f"A tutor charges a ${b} fee plus ${m} per hour. How much for a {x}-hour session?"
    dollar_opts = [f"${o}" if not str(o).startswith("−") else f"−${str(o)[1:]}" for o in opts]
    return {
        "id": f"gen_le_{m}_{b}_{x}",
        "category": "linear_equations",
        "question": question,
        "options": dollar_opts,
        "answer": opts.index(str(y)),
        "explanation": f"{m}({x}) + {b} = ${y}.",
    }


def _gen_inverse_question() -> dict:
    b = random.choice([5, 10, 12])
    x_ans = random.choice([20, 30, 40, 50])
    y = x_ans + b
    wrong = [str(x_ans + d) for d in random.sample([-20, -10, 10, 20], 3)]
    opts = wrong + [str(x_ans)]
    random.shuffle(opts)
    return {
        "id": f"gen_inv_{y}_{b}",
        "category": "word_problems",
        "question": (
            f"Sarah's craft demo costs ${b} plus $1 per person. "
            f"If the total cost is ${y}, how many people attended?"
        ),
        "options": [f"{o} people" for o in opts],
        "answer": opts.index(str(x_ans)),
        "explanation": f"{y} = people + {b} → {x_ans} people.",
    }


GENERATORS = [
    _gen_quadrant_question,
    _gen_function_table_question,
    _gen_linear_table_question,
    _gen_inverse_question,
]


def get_categories(unit_id: int = 1) -> dict:
    return CATEGORIES_BY_UNIT.get(unit_id, CATEGORIES)


def _unit_practice(unit_id: int) -> dict:
    return {
        "bank": QUESTION_BANK_BY_UNIT.get(unit_id, QUESTION_BANK),
        "categories": CATEGORIES_BY_UNIT.get(unit_id, CATEGORIES),
        "category_activity": CATEGORY_ACTIVITY_BY_UNIT.get(unit_id, CATEGORY_ACTIVITY),
        "revision_tips": REVISION_TIPS_BY_UNIT.get(unit_id, REVISION_TIPS),
        "graph_min": GRAPH_MIN_BY_UNIT.get(unit_id, GRAPH_MIN_PER_SESSION),
        "generators": GENERATORS if unit_id == 1 else [],
    }


def practice_image_path(image_key: str | None, unit_id: int = 1) -> str | None:
    if not image_key:
        return None
    base = PRACTICE_IMG_BY_UNIT.get(unit_id, PRACTICE_IMG)
    path = base / f"{image_key}.png"
    return str(path) if path.is_file() else None


def _weighted_pool(questions: list[dict], categories: dict | None = None) -> list[dict]:
    cats = categories or CATEGORIES
    pool: list[dict] = []
    for q in questions:
        cat = cats.get(q["category"], {})
        w = cat.get("weight", 1)
        pool.extend([q] * w)
    random.shuffle(pool)
    return pool


def _question_available(
    q: dict,
    used_ids: set[str],
    used_images: set[str],
    avoid_ids: set[str],
    *,
    allow_recent: bool,
) -> bool:
    if q["id"] in used_ids:
        return False
    if not allow_recent and q["id"] in avoid_ids:
        return False
    img = q.get("image")
    if img and img in used_images:
        return False
    return True


def _pick_unique(
    pool: list[dict],
    count: int,
    used_ids: set[str],
    used_images: set[str],
    avoid_ids: set[str] | None = None,
) -> list[dict]:
    """Pick up to `count` questions; one diagram per session; prefer fresh IDs."""
    avoid_ids = avoid_ids or set()
    picked: list[dict] = []

    for allow_recent in (False, True):
        if len(picked) >= count:
            break
        for q in pool:
            if len(picked) >= count:
                break
            if not _question_available(q, used_ids, used_images, avoid_ids, allow_recent=allow_recent):
                continue
            picked.append(dict(q))
            used_ids.add(q["id"])
            img = q.get("image")
            if img:
                used_images.add(img)
    return picked


def _top_up(
    selected: list[dict],
    count: int,
    used_ids: set[str],
    used_images: set[str],
    avoid_ids: set[str],
    candidates: list[dict],
) -> None:
    random.shuffle(candidates)
    for allow_recent in (False, True):
        if len(selected) >= count:
            break
        for q in candidates:
            if len(selected) >= count:
                break
            if not _question_available(q, used_ids, used_images, avoid_ids, allow_recent=allow_recent):
                continue
            selected.append(dict(q))
            used_ids.add(q["id"])
            img = q.get("image")
            if img:
                used_images.add(img)


def build_daily_set(
    count: int = 15,
    unit_id: int = 1,
    exclude_ids: set[str] | None = None,
) -> list[dict]:
    cfg = _unit_practice(unit_id)
    bank = cfg["bank"]
    categories = cfg["categories"]
    generators = cfg["generators"]
    graph_min = cfg["graph_min"]
    avoid_ids = set(exclude_ids or ())

    graph_bank = [q for q in bank if q.get("image")]
    text_bank = [q for q in bank if not q.get("image")]
    graph_target = min(graph_min, count, len(graph_bank))
    text_target = count - graph_target

    used_ids: set[str] = set()
    used_images: set[str] = set()
    selected: list[dict] = []

    selected.extend(
        _pick_unique(_weighted_pool(graph_bank, categories), graph_target, used_ids, used_images, avoid_ids)
    )

    if len(selected) < graph_target:
        selected.extend(
            _pick_unique(graph_bank, graph_target - len(selected), used_ids, used_images, avoid_ids)
        )

    selected.extend(
        _pick_unique(_weighted_pool(text_bank, categories), text_target, used_ids, used_images, avoid_ids)
    )

    if len(selected) < count:
        remainder = [q for q in bank if q["id"] not in used_ids]
        _top_up(selected, count, used_ids, used_images, avoid_ids, remainder)

    attempts = 0
    while len(selected) < count and generators and attempts < 20:
        attempts += 1
        gq = random.choice(generators)()
        if gq["id"] in used_ids:
            continue
        if not attempts > 10 and gq["id"] in avoid_ids:
            continue
        selected.append(gq)
        used_ids.add(gq["id"])

    random.shuffle(selected)
    return selected[:count]


def graph_question_count(questions: list[dict]) -> int:
    return sum(1 for q in questions if q.get("image"))


def build_session_report(
    questions: list[dict],
    answers: list[dict],
    unit_id: int = 1,
) -> dict:
    """Summarize a completed practice set by topic — strengths vs areas to revise."""
    cfg = _unit_practice(unit_id)
    categories = cfg["categories"]
    category_activity = cfg["category_activity"]
    revision_tips = cfg["revision_tips"]

    by_cat: dict[str, dict] = {}
    for q, ans in zip(questions, answers):
        cat = q.get("category", "unknown")
        bucket = by_cat.setdefault(cat, {"correct": 0, "total": 0})
        bucket["total"] += 1
        if ans.get("correct"):
            bucket["correct"] += 1

    strengths: list[dict] = []
    needs_revision: list[dict] = []
    for cat, stats in by_cat.items():
        info = categories.get(cat, {})
        pct = int(100 * stats["correct"] / stats["total"]) if stats["total"] else 0
        entry = {
            "category": cat,
            "name": info.get("name", cat.replace("_", " ").title()),
            "emoji": info.get("emoji", "📐"),
            "color": info.get("color", "#6366f1"),
            "correct": stats["correct"],
            "total": stats["total"],
            "pct": pct,
            "activity_slug": category_activity.get(cat),
            "tip": revision_tips.get(cat, "Review the matching lesson notes and try again."),
        }
        if pct >= STRENGTH_THRESHOLD_PCT:
            strengths.append(entry)
        else:
            needs_revision.append(entry)

    strengths.sort(key=lambda e: (-e["pct"], e["name"]))
    needs_revision.sort(key=lambda e: (e["pct"], e["name"]))

    correct_count = sum(1 for a in answers if a.get("correct"))
    total = len(answers)
    score_pct = int(100 * correct_count / total) if total else 0

    if needs_revision:
        tip = f"{needs_revision[0]['name']}: {needs_revision[0]['tip']}"
    elif score_pct == 100:
        tip = "Perfect run — try another set tomorrow to keep skills sharp."
    else:
        tip = "Solid session. One more practice set will help lock in the harder topics."

    return {
        "correct_count": correct_count,
        "total": total,
        "score_pct": score_pct,
        "strengths": strengths,
        "needs_revision": needs_revision,
        "tip": tip,
    }


def format_report_details(report: dict) -> str:
    """One-line summary for activity_scores.details."""
    base = f"{report['correct_count']}/{report['total']} correct"
    weak = [r["name"] for r in report.get("needs_revision", [])]
    if weak:
        return f"{base} | Review: {', '.join(weak)}"
    return base
