"""Arjun Edgenuity Course 3 Math — lesson notes metadata and paths."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
COURSE_DIR = ROOT / "ArjunEdgenuityCourse3"
NOTES_DIR = COURSE_DIR / "notes"
IMAGES_DIR = COURSE_DIR / "images"


def _diagrams(activity: int, items: list[tuple[str, str, str]]) -> list[dict]:
    return [{"key": k, "file": f, "caption": c} for k, f, c in items]


UNIT_1_ACTIVITIES = [
    {
        "number": 1,
        "slug": "activity_1_coordinate_plane",
        "title": "Coordinate Plane & Ordered Pairs",
        "file": "activity_1_coordinate_plane.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(1, [
            ("quadrants", "activity_1_quadrants.png", "Four quadrants and sign patterns for (x, y)"),
            ("read_point", "activity_1_read_point.png", "Point P at (−4, 3) — x first, then y"),
        ]),
    },
    {
        "number": 2,
        "slug": "activity_2_relations_functions",
        "title": "Relations & Functions",
        "file": "activity_2_relations_functions.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(2, [
            ("vertical_line_test", "activity_2_vertical_line_test.png", "Vertical line test on a scatter of points"),
            ("mapping_diagram", "activity_2_mapping_diagram.png", "One input with two outputs — not a function"),
            ("function_equations", "activity_2_function_equations.png", "Which equations define y as a function of x"),
        ]),
    },
    {
        "number": 3,
        "slug": "activity_3_graph_behavior",
        "title": "Graph Behavior",
        "file": "activity_3_graph_behavior.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(3, [
            ("segment_graph", "activity_3_segment_graph.png", "Increasing, constant, then decreasing segments"),
            ("parabola_behavior", "activity_3_parabola_behavior.png", "Parabola: decreasing then increasing"),
            ("distance_time", "activity_3_distance_time.png", "Distance-time graph — flat means stopped"),
        ]),
    },
    {
        "number": 4,
        "slug": "activity_4_linear_equations",
        "title": "Linear Equations from Tables",
        "file": "activity_4_linear_equations.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(4, [
            ("unit_rate", "activity_4_unit_rate.png", "Tickets sold vs profit — constant $9 per ticket"),
            ("perimeter_equation", "activity_4_perimeter_equation.png", "Square side length x → perimeter y = 4x"),
            ("jaxon_change", "activity_4_jaxon_change.png", "Change from $10 bill: y = 10 − x"),
        ]),
    },
    {
        "number": 5,
        "slug": "activity_5_completing_tables",
        "title": "Completing & Using Tables",
        "file": "activity_5_completing_tables.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(5, [
            ("table_to_graph", "activity_5_table_to_graph.png", "Match table values to points on a line"),
            ("evaluate_equation", "activity_5_evaluate_equation.png", "Evaluate r = 3c + 5 for c = 12"),
            ("gas_tank", "activity_5_gas_tank.png", "Gas remaining vs distance traveled"),
        ]),
    },
    {
        "number": 6,
        "slug": "activity_6_word_problems",
        "title": "Real-World Word Problems",
        "file": "activity_6_word_problems.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(6, [
            ("movie_rentals", "activity_6_movie_rentals.png", "Movies Plus vs Movies For Less cost comparison"),
            ("bank_deposits", "activity_6_bank_deposits.png", "125 + 45m ≥ 360 — months until $360"),
            ("inverse_lookup", "activity_6_inverse_lookup.png", "Find input when output is known (Sarah's craft demo)"),
        ]),
    },
]


UNIT_2_ACTIVITIES = [
    {
        "number": 1,
        "slug": "activity_1_slope_rate",
        "title": "Slope & Rate of Change",
        "file": "activity_1_slope_rate.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(1, [
            ("slope_rise_run", "activity_1_slope_rise_run.png", "Slope = rise ÷ run"),
            ("wilson_watering", "activity_1_wilson_watering.png", "Wilson's watering can — water vs time"),
        ]),
    },
    {
        "number": 2,
        "slug": "activity_2_y_intercept",
        "title": "Y-Intercept & Initial Value",
        "file": "activity_2_y_intercept.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(2, [
            ("y_intercept_line", "activity_2_y_intercept_line.png", "Where the graph crosses the y-axis"),
            ("initial_value_table", "activity_2_initial_value_table.png", "Find the starting value from a table"),
        ]),
    },
    {
        "number": 3,
        "slug": "activity_3_direct_variation",
        "title": "Direct Variation & Proportionality",
        "file": "activity_3_direct_variation.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(3, [
            ("direct_vs_not", "activity_3_direct_vs_not.png", "Direct variation must pass through the origin"),
            ("proportional_graph", "activity_3_proportional_graph.png", "Proportional relationship graph"),
        ]),
    },
    {
        "number": 4,
        "slug": "activity_4_special_lines",
        "title": "Horizontal, Vertical & Special Slopes",
        "file": "activity_4_special_lines.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(4, [
            ("horizontal_vertical", "activity_4_horizontal_vertical.png", "Horizontal vs vertical lines"),
            ("zero_undefined_slope", "activity_4_zero_undefined_slope.png", "Zero slope vs undefined slope"),
        ]),
    },
    {
        "number": 5,
        "slug": "activity_5_writing_equations",
        "title": "Writing Linear Equations",
        "file": "activity_5_writing_equations.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(5, [
            ("equation_from_graph", "activity_5_equation_from_graph.png", "Read slope and y-intercept from a graph"),
            ("point_on_line", "activity_5_point_on_line.png", "Find a missing coordinate on a line"),
        ]),
    },
    {
        "number": 6,
        "slug": "activity_6_linear_modeling",
        "title": "Real-World Linear Models",
        "file": "activity_6_linear_modeling.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(6, [
            ("shake_shack_model", "activity_6_shake_shack_model.png", "Shake Shack revenue model"),
            ("brenda_phone_bill", "activity_6_brenda_phone_bill.png", "Cell phone bill vs hours used"),
        ]),
    },
]


UNIT_3_ACTIVITIES = [
    {
        "number": 1,
        "slug": "activity_1_slope_intercept_read",
        "title": "Reading Slope & Y-Intercept",
        "file": "activity_1_slope_intercept_read.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(1, [
            ("slope_intercept_line", "activity_1_slope_intercept_line.png", "Slope and y-intercept on a line"),
            ("table_to_slope", "activity_1_table_to_slope.png", "Find slope from a table"),
        ]),
    },
    {
        "number": 2,
        "slug": "activity_2_two_point_equations",
        "title": "Equations from Two Points",
        "file": "activity_2_two_point_equations.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(2, [
            ("two_points_graph", "activity_2_two_points_graph.png", "Line through two plotted points"),
            ("equation_from_points", "activity_2_equation_from_points.png", "From (0, 6) and (2, 0)"),
        ]),
    },
    {
        "number": 3,
        "slug": "activity_3_point_slope_form",
        "title": "Point-Slope Form",
        "file": "activity_3_point_slope_form.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(3, [
            ("point_slope_convert", "activity_3_point_slope_convert.png", "Convert point-slope to slope-intercept"),
            ("line_through_point", "activity_3_line_through_point.png", "Line with known slope through a point"),
        ]),
    },
    {
        "number": 4,
        "slug": "activity_4_standard_form",
        "title": "Standard Form & Conversion",
        "file": "activity_4_standard_form.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(4, [
            ("standard_to_slope", "activity_4_standard_to_slope.png", "Convert Ax + By = C to y = mx + b"),
            ("jill_error_steps", "activity_4_jill_error_steps.png", "Common sign errors when converting"),
        ]),
    },
    {
        "number": 5,
        "slug": "activity_5_context_meaning",
        "title": "Slope & Intercept in Context",
        "file": "activity_5_context_meaning.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(5, [
            ("inez_phone_card", "activity_5_inez_phone_card.png", "Inez's phone card — minutes vs days"),
            ("washing_machine_model", "activity_5_washing_machine_model.png", "Repair cost y = 45x + 35"),
        ]),
    },
    {
        "number": 6,
        "slug": "activity_6_compare_functions",
        "title": "Comparing Linear Functions",
        "file": "activity_6_compare_functions.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(6, [
            ("compare_two_lines", "activity_6_compare_two_lines.png", "Compare slopes and y-intercepts"),
            ("same_y_intercept", "activity_6_same_y_intercept.png", "Same steepness ≠ same line"),
        ]),
    },
]


UNIT_4_ACTIVITIES = [
    {
        "number": 1,
        "slug": "activity_1_scatterplots_correlation",
        "title": "Scatterplots & Correlation",
        "file": "activity_1_scatterplots_correlation.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(1, [
            ("scatterplot_basics", "activity_1_scatterplot_basics.png", "Reading a scatterplot"),
            ("correlation_types", "activity_1_correlation_types.png", "Positive, negative, and no correlation"),
        ]),
    },
    {
        "number": 2,
        "slug": "activity_2_association_strength",
        "title": "Association Strength & Type",
        "file": "activity_2_association_strength.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(2, [
            ("strong_vs_weak", "activity_2_strong_vs_weak.png", "Strong vs weak association"),
            ("linear_vs_nonlinear", "activity_2_linear_vs_nonlinear.png", "Linear vs nonlinear patterns"),
        ]),
    },
    {
        "number": 3,
        "slug": "activity_3_trend_lines_slope",
        "title": "Trend Lines & Slope",
        "file": "activity_3_trend_lines_slope.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(3, [
            ("trend_line_slope", "activity_3_trend_line_slope.png", "Trend line and slope"),
            ("slope_from_graph", "activity_3_slope_from_graph.png", "Slope from two points on the line"),
        ]),
    },
    {
        "number": 4,
        "slug": "activity_4_predictions",
        "title": "Interpolation & Extrapolation",
        "file": "activity_4_predictions.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(4, [
            ("interpolation_extrapolation", "activity_4_interpolation_extrapolation.png", "Inside vs outside the data range"),
            ("prediction_from_equation", "activity_4_prediction_from_equation.png", "Predict using a trend-line equation"),
        ]),
    },
    {
        "number": 5,
        "slug": "activity_5_two_way_tables",
        "title": "Two-Way Tables",
        "file": "activity_5_two_way_tables.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(5, [
            ("two_way_table", "activity_5_two_way_table.png", "Two-way frequency table"),
            ("table_variables", "activity_5_table_variables.png", "Identifying the two variables"),
        ]),
    },
    {
        "number": 6,
        "slug": "activity_6_outliers_interpretation",
        "title": "Outliers & Data Interpretation",
        "file": "activity_6_outliers_interpretation.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(6, [
            ("outlier_effect", "activity_6_outlier_effect.png", "How outliers affect interpretation"),
            ("no_correlation_scatter", "activity_6_no_correlation_scatter.png", "Scatter with no correlation"),
        ]),
    },
]


UNIT_5_ACTIVITIES = [
    {
        "number": 1,
        "slug": "activity_1_algebra_tiles",
        "title": "Algebra Tile Models",
        "file": "activity_1_algebra_tiles.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(1, [
            ("algebra_tiles_balance", "activity_1_algebra_tiles_balance.png", "Balance model with x-tiles and unit tiles"),
            ("completing_tile_model", "activity_1_completing_tile_model.png", "Completing a tile model for 3x + 2 = −x + 6"),
        ]),
    },
    {
        "number": 2,
        "slug": "activity_2_properties_equality",
        "title": "Properties of Equality",
        "file": "activity_2_properties_equality.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(2, [
            ("properties_equality", "activity_2_properties_equality.png", "Addition, subtraction, and division properties"),
            ("distributive_model", "activity_2_distributive_model.png", "Distributive property before solving"),
        ]),
    },
    {
        "number": 3,
        "slug": "activity_3_simplify_expressions",
        "title": "Simplifying Expressions",
        "file": "activity_3_simplify_expressions.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(3, [
            ("distribute_negatives", "activity_3_distribute_negatives.png", "Distributing negative signs correctly"),
            ("combine_like_terms", "activity_3_combine_like_terms.png", "Combining like terms on both sides"),
        ]),
    },
    {
        "number": 4,
        "slug": "activity_4_number_of_solutions",
        "title": "Number of Solutions",
        "file": "activity_4_number_of_solutions.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(4, [
            ("one_solution", "activity_4_one_solution.png", "Equation with exactly one solution"),
            ("no_solution_case", "activity_4_no_solution_case.png", "Variables cancel to a false statement"),
        ]),
    },
    {
        "number": 5,
        "slug": "activity_5_multistep_solving",
        "title": "Multi-Step Solving",
        "file": "activity_5_multistep_solving.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(5, [
            ("multistep_flow", "activity_5_multistep_flow.png", "Distribute → combine → isolate x"),
            ("variables_both_sides", "activity_5_variables_both_sides.png", "Variables on both sides of the equation"),
        ]),
    },
    {
        "number": 6,
        "slug": "activity_6_standard_form_word_problems",
        "title": "Standard Form & Word Problems",
        "file": "activity_6_standard_form_word_problems.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(6, [
            ("solve_for_y", "activity_6_solve_for_y.png", "Solve Ax + By = C for y"),
            ("word_problem_setup", "activity_6_word_problem_setup.png", "Translate a word problem into an equation"),
        ]),
    },
]


UNIT_6_ACTIVITIES = [
    {
        "number": 1,
        "slug": "activity_1_graphing_solutions",
        "title": "Graphing Systems & Solutions",
        "file": "activity_1_graphing_solutions.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(1, [
            ("system_intersection", "activity_1_system_intersection.png", "Solution at the intersection of two lines"),
            ("graph_table_system", "activity_1_graph_table_system.png", "Line plus table for the second equation"),
        ]),
    },
    {
        "number": 2,
        "slug": "activity_2_slope_intercept",
        "title": "Slope-Intercept Form",
        "file": "activity_2_slope_intercept.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(2, [
            ("convert_to_slope_intercept", "activity_2_convert_to_slope_intercept.png", "Convert 5x − 2y = 10 to y = mx + b"),
            ("slope_intercept_form", "activity_2_slope_intercept_form.png", "Recognizing slope-intercept form"),
        ]),
    },
    {
        "number": 3,
        "slug": "activity_3_word_problems",
        "title": "Systems from Word Problems",
        "file": "activity_3_word_problems.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(3, [
            ("word_to_equations", "activity_3_word_to_equations.png", "Translate words into a system"),
            ("real_world_system", "activity_3_real_world_system.png", "Real-world cost comparison graph"),
        ]),
    },
    {
        "number": 4,
        "slug": "activity_4_number_of_solutions",
        "title": "Number of Solutions",
        "file": "activity_4_number_of_solutions.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(4, [
            ("parallel_lines", "activity_4_parallel_lines.png", "Parallel lines → no solution"),
            ("infinite_solutions", "activity_4_infinite_solutions.png", "Same line → infinitely many solutions"),
        ]),
    },
    {
        "number": 5,
        "slug": "activity_5_identify_from_graph",
        "title": "Identify Systems from Graphs",
        "file": "activity_5_identify_from_graph.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(5, [
            ("four_lines_graph", "activity_5_four_lines_graph.png", "Multiple lines on one coordinate plane"),
            ("match_system_graph", "activity_5_match_system_graph.png", "Match equations to a graphed system"),
        ]),
    },
    {
        "number": 6,
        "slug": "activity_6_checking_solutions",
        "title": "Checking Solutions",
        "file": "activity_6_checking_solutions.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(6, [
            ("substitution_check", "activity_6_substitution_check.png", "Substitute an ordered pair into both equations"),
            ("verify_solution", "activity_6_verify_solution.png", "Error analysis when checking a solution"),
        ]),
    },
]


def _pdf_path(unit_id: int) -> Path:
    if unit_id == 1:
        exam = COURSE_DIR / "course_3_unit_1_exam.pdf"
        if exam.is_file():
            return exam
    if unit_id == 2:
        exam = COURSE_DIR / "course_3_unit_2_exam.pdf"
        if exam.is_file():
            return exam
    if unit_id == 3:
        exam = COURSE_DIR / "course_3_unit_3_exam.pdf"
        if exam.is_file():
            return exam
    if unit_id == 4:
        exam = COURSE_DIR / "course_3_unit_4_exam.pdf"
        if exam.is_file():
            return exam
    if unit_id == 5:
        exam = COURSE_DIR / "course_3_unit_5_exam.pdf"
        if exam.is_file():
            return exam
    if unit_id == 6:
        exam = COURSE_DIR / "course_3_unit_6_exam.pdf"
        if exam.is_file():
            return exam
    return COURSE_DIR / f"course_3_unit_{unit_id}.pdf"


def _build_unit(
    unit_id: int,
    title: str,
    subtitle: str = "",
    *,
    activities: list | None = None,
    combined_notes_name: str | None = None,
) -> dict:
    combined = None
    if combined_notes_name:
        p = NOTES_DIR / f"unit_{unit_id}" / combined_notes_name
        if p.is_file():
            combined = p
    return {
        "id": unit_id,
        "title": title,
        "subtitle": subtitle,
        "pdf": _pdf_path(unit_id),
        "combined_notes": combined,
        "activities": activities or [],
    }


UNITS = [
    _build_unit(
        1,
        "Unit 1",
        "Input-output relationships",
        activities=UNIT_1_ACTIVITIES,
        combined_notes_name="unit_1_input_output_relationships_lesson_notes.md",
    ),
    _build_unit(2, "Unit 2", "Linear functions & modeling", activities=UNIT_2_ACTIVITIES,
                combined_notes_name="unit_2_linear_functions_lesson_notes.md"),
    _build_unit(
        3,
        "Unit 3",
        "Writing equations for linear relationships",
        activities=UNIT_3_ACTIVITIES,
        combined_notes_name="unit_3_writing_linear_equations_lesson_notes.md",
    ),
    _build_unit(
        4,
        "Unit 4",
        "Patterns in bivariate data",
        activities=UNIT_4_ACTIVITIES,
        combined_notes_name="unit_4_bivariate_data_lesson_notes.md",
    ),
    _build_unit(
        5,
        "Unit 5",
        "Linear equations",
        activities=UNIT_5_ACTIVITIES,
        combined_notes_name="unit_5_linear_equations_lesson_notes.md",
    ),
    _build_unit(
        6,
        "Unit 6",
        "Systems of linear equations",
        activities=UNIT_6_ACTIVITIES,
        combined_notes_name="unit_6_systems_linear_equations_lesson_notes.md",
    ),
    _build_unit(7, "Unit 7", "Similarity & dilations"),
    _build_unit(8, "Unit 8", "Exponents & scientific notation"),
    _build_unit(9, "Unit 9", "Irrational numbers, Pythagorean theorem & volume"),
    _build_unit(10, "Unit 10", "Statistics & course review"),
]


def list_units() -> list[dict]:
    return UNITS


def get_unit(unit_id: int) -> dict | None:
    return next((u for u in UNITS if u["id"] == unit_id), None)


def unit_notes_ready(unit: dict) -> bool:
    return bool(unit.get("activities"))


def unit_notes_dir(unit_id: int) -> Path:
    return NOTES_DIR / f"unit_{unit_id}"


def unit_images_dir(unit_id: int) -> Path:
    return IMAGES_DIR / f"unit_{unit_id}"


def practice_images_dir(unit_id: int) -> Path:
    return IMAGES_DIR / f"unit_{unit_id}" / "practice"


def load_activity_markdown(unit: dict, activity: dict) -> str:
    path = unit_notes_dir(unit["id"]) / activity["file"]
    if not path.is_file():
        return f"*Notes file not found: {path.name}*"
    return path.read_text(encoding="utf-8")


def activity_diagrams(unit: dict, activity: dict) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    img_dir = unit_images_dir(unit["id"])
    for item in activity.get("diagrams") or []:
        path = img_dir / item["file"]
        if path.is_file():
            out.append((str(path), item.get("caption", "")))
    return out
