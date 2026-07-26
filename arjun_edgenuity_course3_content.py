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


def _pdf_path(unit_id: int) -> Path:
    if unit_id == 1:
        exam = COURSE_DIR / "course_3_unit_1_exam.pdf"
        if exam.is_file():
            return exam
    if unit_id == 2:
        exam = COURSE_DIR / "course_3_unit_2_exam.pdf"
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
    _build_unit(3, "Unit 3", "Solving linear equations"),
    _build_unit(4, "Unit 4", "Systems of linear equations"),
    _build_unit(5, "Unit 5", "Bivariate data & scatter plots"),
    _build_unit(6, "Unit 6", "Transformations & congruence"),
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
