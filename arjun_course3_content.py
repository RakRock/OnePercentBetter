"""Arjun Course 3 Math — lesson notes metadata and paths."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent
COURSE3_DIR = ROOT / "ArjunCourse3"
NOTES_DIR = COURSE3_DIR / "notes"
IMAGES_DIR = COURSE3_DIR / "images"

def _diagrams(activity: int, items: list[tuple[str, str, str]]) -> list[dict]:
    return [{"key": k, "file": f, "caption": c} for k, f, c in items]


UNIT_1_ACTIVITIES = [
    {
        "number": 1,
        "slug": "activity_1_investigating_patterns",
        "title": "Investigating Patterns",
        "file": "activity_1_investigating_patterns.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(1, [
            ("sequence_pattern", "activity_1_sequence_pattern.png", "Arithmetic sequence with constant difference"),
            ("fibonacci", "activity_1_fibonacci.png", "Fibonacci: each term is sum of previous two"),
        ]),
    },
    {
        "number": 2,
        "slug": "activity_2_operations_with_fractions",
        "title": "Operations with Fractions",
        "file": "activity_2_operations_with_fractions.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(2, [
            ("add_fractions", "activity_2_add_fractions.png", "Add fractions using a common denominator"),
            ("multiply_fractions", "activity_2_multiply_fractions.png", "Multiply numerators and denominators"),
        ]),
    },
    {
        "number": 3,
        "slug": "activity_3_powers_and_roots",
        "title": "Powers and Roots",
        "file": "activity_3_powers_and_roots.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(3, [
            ("square_area", "activity_3_square_area.png", "Square area = side squared"),
            ("cube_volume", "activity_3_cube_volume.png", "Cube volume = edge cubed"),
        ]),
    },
    {
        "number": 4,
        "slug": "activity_4_rational_numbers",
        "title": "Rational Numbers",
        "file": "activity_4_rational_numbers.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(4, [
            ("frac_decimal_percent", "activity_4_frac_decimal_percent.png", "Fraction, decimal, and percent"),
            ("repeating_decimal", "activity_4_repeating_decimal.png", "Repeating decimals are rational"),
        ]),
    },
    {
        "number": 5,
        "slug": "activity_5_rational_irrational_numbers",
        "title": "Rational and Irrational Numbers",
        "file": "activity_5_rational_irrational_numbers.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(5, [
            ("sqrt_number_line", "activity_5_sqrt_number_line.png", "Estimate square roots on a number line"),
            ("rational_irrational", "activity_5_rational_irrational.png", "Rational vs irrational numbers"),
        ]),
    },
    {
        "number": 6,
        "slug": "activity_6_properties_of_exponents",
        "title": "Properties of Exponents",
        "file": "activity_6_properties_of_exponents.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(6, [
            ("product_rule", "activity_6_product_rule.png", "Multiply: add exponents (same base)"),
            ("negative_exponent", "activity_6_negative_exponent.png", "Negative exponent = reciprocal"),
        ]),
    },
    {
        "number": 7,
        "slug": "activity_7_scientific_notation",
        "title": "Scientific Notation",
        "file": "activity_7_scientific_notation.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(7, [
            ("sci_notation_form", "activity_7_sci_notation_form.png", "Write large numbers as a × 10^n"),
            ("standard_form", "activity_7_standard_form.png", "Convert scientific notation to standard form"),
        ]),
    },
    {
        "number": 8,
        "slug": "activity_8_operations_scientific_notation",
        "title": "Operations with Scientific Notation",
        "file": "activity_8_operations_scientific_notation.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(8, [
            ("multiply_sci", "activity_8_multiply_sci.png", "Multiply: coefficients ×, exponents add"),
            ("add_sci", "activity_8_add_sci.png", "Add: same power of 10, then add coefficients"),
        ]),
    },
]


UNIT_2_ACTIVITIES = [
    {
        "number": 9,
        "slug": "activity_9_writing_expressions",
        "title": "Writing Expressions",
        "file": "activity_9_writing_expressions.md",
        "diagrams": [
            {
                "key": "constant_difference",
                "file": "activity_9_constant_difference.png",
                "caption": "Constant difference — +3 tiles each figure",
            },
            {
                "key": "square_numbers",
                "file": "activity_9_square_numbers.png",
                "caption": "Square numbers — n × n grid (n²)",
            },
            {
                "key": "rectangular_numbers",
                "file": "activity_9_rectangular_numbers.png",
                "caption": "Rectangular numbers — n × (n+1)",
            },
            {
                "key": "triangular_numbers",
                "file": "activity_9_triangular_numbers.png",
                "caption": "Triangular numbers — rows 1, 2, 3…",
            },
            {
                "key": "table_to_expression",
                "file": "activity_9_table_to_expression.png",
                "caption": "Read the table → write 4 + 5(n−1)",
            },
            {
                "key": "example_1",
                "file": "activity_9_example_1.png",
                "caption": "Example 1 — 4 tiles, +5 per figure; figure 6 has 29 tiles",
            },
        ],
        "inline_diagrams": True,
    },
    {
        "number": 10,
        "slug": "activity_10_solving_equations",
        "title": "Solving Equations",
        "file": "activity_10_solving_equations.md",
        "inline_diagrams": True,
        "diagrams": [
            {"key": "balance_scale", "file": "activity_10_balance_scale.png", "caption": "Balance both sides of the equation"},
            {"key": "solve_steps", "file": "activity_10_solve_steps.png", "caption": "Steps to solve 3x + 4 = 16"},
            {"key": "solution_types", "file": "activity_10_solution_types.png", "caption": "One solution, no solution, or infinitely many"},
        ],
    },
    {
        "number": 11,
        "slug": "activity_11_exploring_slope",
        "title": "Exploring Slope",
        "file": "activity_11_exploring_slope.md",
        "inline_diagrams": True,
        "diagrams": [
            {"key": "change_in_y_x", "file": "activity_11_change_in_y_x.png", "caption": "Slope = change in y / change in x"},
            {"key": "rate_context", "file": "activity_11_rate_context.png", "caption": "Slope as speed (miles per hour)"},
        ],
    },
    {
        "number": 12,
        "slug": "activity_12_slope_intercept_form",
        "title": "Slope-Intercept Form",
        "file": "activity_12_slope_intercept_form.md",
        "inline_diagrams": True,
        "diagrams": [
            {"key": "y_mx_b", "file": "activity_12_y_mx_b.png", "caption": "y = mx + b on a graph"},
            {"key": "graph_example", "file": "activity_12_graph_example.png", "caption": "Graph y = ½x − 2 using b and slope"},
        ],
    },
    {
        "number": 13,
        "slug": "activity_13_proportional_relationships",
        "title": "Proportional Relationships",
        "file": "activity_13_proportional_relationships.md",
        "inline_diagrams": True,
        "diagrams": [
            {"key": "proportional_vs_not", "file": "activity_13_proportional_vs_not.png", "caption": "Through (0,0) vs not through origin"},
            {"key": "table_constant", "file": "activity_13_table_constant.png", "caption": "Same y/x ratio → proportional"},
        ],
    },
    {
        "number": 14,
        "slug": "activity_14_graphing_systems",
        "title": "Graphing Systems of Linear Equations",
        "file": "activity_14_graphing_systems.md",
        "inline_diagrams": True,
        "diagrams": [
            {"key": "intersection", "file": "activity_14_intersection.png", "caption": "Solution where lines cross"},
            {"key": "parallel", "file": "activity_14_parallel.png", "caption": "Parallel lines → no solution"},
            {"key": "three_cases", "file": "activity_14_three_cases.png", "caption": "One, none, or infinitely many solutions"},
        ],
    },
    {
        "number": 15,
        "slug": "activity_15_solving_systems_algebraically",
        "title": "Solving Systems Algebraically",
        "file": "activity_15_solving_systems_algebraically.md",
        "inline_diagrams": True,
        "diagrams": [
            {"key": "substitution", "file": "activity_15_substitution.png", "caption": "Substitution steps and graph of the solution point"},
            {"key": "elimination", "file": "activity_15_elimination.png", "caption": "Elimination by subtracting equations; multiply first when needed"},
            {"key": "tickets_example", "file": "activity_15_tickets_example.png", "caption": "Ticket problem: set up equations, solve, and check"},
        ],
    },
]


UNIT_3_ACTIVITIES = [
    {
        "number": 16,
        "slug": "activity_16_angle_pair_relationships",
        "title": "Angle-Pair Relationships",
        "file": "activity_16_angle_pair_relationships.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(16, [
            ("complementary", "activity_16_complementary.png", "Complementary angles sum to 90°"),
            ("transversal", "activity_16_transversal.png", "Parallel lines and a transversal"),
        ]),
    },
    {
        "number": 17,
        "slug": "activity_17_angles_triangles_quadrilaterals",
        "title": "Angles of Triangles and Quadrilaterals",
        "file": "activity_17_angles_triangles_quadrilaterals.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(17, [
            ("triangle_sum", "activity_17_triangle_sum.png", "Triangle angle sum = 180°"),
            ("quadrilateral", "activity_17_quadrilateral.png", "Quadrilateral angle sum = 360°"),
        ]),
    },
    {
        "number": 18,
        "slug": "activity_18_introduction_transformations",
        "title": "Introduction to Transformations",
        "file": "activity_18_introduction_transformations.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(18, [
            ("transformations", "activity_18_transformations.png", "Translation, reflection, rotation"),
            ("coordinate", "activity_18_coordinate.png", "Translation on the coordinate plane"),
        ]),
    },
    {
        "number": 19,
        "slug": "activity_19_rigid_transformations_compositions",
        "title": "Rigid Transformations and Compositions",
        "file": "activity_19_rigid_transformations_compositions.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(19, [
            ("rigid", "activity_19_rigid.png", "Rigid transformations preserve size and shape"),
            ("rotation", "activity_19_rotation.png", "Rotation about the origin"),
        ]),
    },
    {
        "number": 20,
        "slug": "activity_20_similar_triangles",
        "title": "Similar Triangles",
        "file": "activity_20_similar_triangles.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(20, [
            ("similar", "activity_20_similar.png", "Similar triangles — proportional sides"),
            ("aa", "activity_20_aa.png", "AA similarity criterion"),
        ]),
    },
    {
        "number": 21,
        "slug": "activity_21_dilations",
        "title": "Dilations",
        "file": "activity_21_dilations.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(21, [
            ("dilation", "activity_21_dilation.png", "Dilation enlarges or shrinks from a center"),
            ("scale_factor", "activity_21_scale_factor.png", "Scale factor k"),
        ]),
    },
    {
        "number": 22,
        "slug": "activity_22_pythagorean_theorem",
        "title": "The Pythagorean Theorem",
        "file": "activity_22_pythagorean_theorem.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(22, [
            ("pythagorean", "activity_22_pythagorean.png", "a² + b² = c² in a right triangle"),
            ("solve_triangle", "activity_22_solve_triangle.png", "Find the hypotenuse"),
        ]),
    },
    {
        "number": 23,
        "slug": "activity_23_applying_pythagorean_theorem",
        "title": "Applying the Pythagorean Theorem",
        "file": "activity_23_applying_pythagorean_theorem.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(23, [
            ("ladder", "activity_23_ladder.png", "Ladder problem"),
            ("diagonal", "activity_23_diagonal.png", "Diagonal of a square"),
        ]),
    },
    {
        "number": 24,
        "slug": "activity_24_converse_pythagorean_theorem",
        "title": "Converse of the Pythagorean Theorem",
        "file": "activity_24_converse_pythagorean_theorem.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(24, [
            ("converse", "activity_24_converse.png", "Converse: a² + b² = c² → right triangle"),
            ("test_triangle", "activity_24_test_triangle.png", "Test if sides form a right triangle"),
        ]),
    },
    {
        "number": 25,
        "slug": "activity_25_surface_area",
        "title": "Surface Area",
        "file": "activity_25_surface_area.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(25, [
            ("prism_net", "activity_25_prism_net.png", "Surface area from a net"),
            ("surface_area", "activity_25_surface_area.png", "Rectangular prism SA = 2(lw + lh + wh)"),
        ]),
    },
    {
        "number": 26,
        "slug": "activity_26_volumes_of_solids",
        "title": "Volumes of Solids",
        "file": "activity_26_volumes_of_solids.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(26, [
            ("volume_prism", "activity_26_volume_prism.png", "Volume V = l × w × h"),
            ("volume_solids", "activity_26_volume_solids.png", "Volume formulas for common solids"),
        ]),
    },
]


UNIT_4_ACTIVITIES = [
    {
        "number": 27,
        "slug": "activity_27_introduction_to_functions",
        "title": "Introduction to Functions",
        "file": "activity_27_introduction_to_functions.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(27, [
            ("function_mapping", "activity_27_function_mapping.png", "Each input maps to exactly one output"),
            ("domain_range", "activity_27_domain_range.png", "Domain and range"),
        ]),
    },
    {
        "number": 28,
        "slug": "activity_28_comparing_functions",
        "title": "Comparing Functions",
        "file": "activity_28_comparing_functions.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(28, [
            ("comparing_graphs", "activity_28_comparing_graphs.png", "Compare linear models"),
            ("rate_of_change", "activity_28_rate_of_change.png", "Rate of change = slope"),
        ]),
    },
    {
        "number": 29,
        "slug": "activity_29_constructing_functions",
        "title": "Constructing Functions",
        "file": "activity_29_constructing_functions.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(29, [
            ("plant_growth", "activity_29_plant_growth.png", "Linear growth from a pattern"),
            ("pattern_perimeter", "activity_29_pattern_perimeter.png", "Pattern to table to equation"),
        ]),
    },
    {
        "number": 30,
        "slug": "activity_30_linear_functions",
        "title": "Linear Functions",
        "file": "activity_30_linear_functions.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(30, [
            ("linear_graph", "activity_30_linear_graph.png", "Linear vs non-linear graphs"),
            ("rate_of_change", "activity_30_rate_of_change.png", "Constant rate of change"),
        ]),
    },
    {
        "number": 31,
        "slug": "activity_31_linear_nonlinear_functions",
        "title": "Linear and Non-Linear Functions",
        "file": "activity_31_linear_nonlinear_functions.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(31, [
            ("scatter_plot", "activity_31_scatter_plot.png", "Scatter plot with linear trend"),
            ("linear_vs_nonlinear", "activity_31_linear_vs_nonlinear.png", "Linear vs non-linear data"),
        ]),
    },
]


UNIT_5_ACTIVITIES = [
    {
        "number": 32,
        "slug": "activity_32_analyzing_data",
        "title": "Analyzing Data",
        "file": "activity_32_analyzing_data.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(32, [
            ("scatter_association", "activity_32_scatter_association.png", "Scatter plot: TV hours vs test score"),
            ("association_types", "activity_32_association_types.png", "Positive vs negative association"),
        ]),
    },
    {
        "number": 33,
        "slug": "activity_33_bivariate_data",
        "title": "Bivariate Data",
        "file": "activity_33_bivariate_data.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(33, [
            ("bivariate_scatter", "activity_33_bivariate_scatter.png", "Bivariate data on a scatter plot"),
            ("trend_line", "activity_33_trend_line.png", "Trend line for prediction"),
        ]),
    },
    {
        "number": 34,
        "slug": "activity_34_median_median_line",
        "title": "Median-Median Line",
        "file": "activity_34_median_median_line.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(34, [
            ("median_median", "activity_34_median_median_line.png", "Median-median line on a scatter plot"),
            ("three_groups", "activity_34_three_groups.png", "Steps for the median-median line"),
        ]),
    },
    {
        "number": 35,
        "slug": "activity_35_two_way_tables_association",
        "title": "Two-Way Tables and Association",
        "file": "activity_35_two_way_tables_association.md",
        "inline_diagrams": True,
        "diagrams": _diagrams(35, [
            ("two_way_table", "activity_35_two_way_table.png", "Two-way table for categorical data"),
            ("segmented_bar", "activity_35_segmented_bar.png", "Segmented bar graph with row percentages"),
        ]),
    },
]


def _pdf_path(unit_id: int) -> Path:
    return COURSE3_DIR / f"course_3_unit_{unit_id}.pdf"


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
        "Numerical relationships",
        activities=UNIT_1_ACTIVITIES,
        combined_notes_name="unit_1_numerical_relationships_lesson_notes.md",
    ),
    _build_unit(
        2,
        "Unit 2",
        "Equations & linear relationships",
        activities=UNIT_2_ACTIVITIES,
        combined_notes_name="unit_2_equations_lesson_notes.md",
    ),
    _build_unit(
        3,
        "Unit 3",
        "Geometry",
        activities=UNIT_3_ACTIVITIES,
        combined_notes_name="unit_3_geometry_lesson_notes.md",
    ),
    _build_unit(
        4,
        "Unit 4",
        "Functions",
        activities=UNIT_4_ACTIVITIES,
        combined_notes_name="unit_4_functions_lesson_notes.md",
    ),
    _build_unit(
        5,
        "Unit 5",
        "Probability & statistics",
        activities=UNIT_5_ACTIVITIES,
        combined_notes_name="unit_5_statistics_lesson_notes.md",
    ),
    _build_unit(6, "Unit 6", "Lesson notes coming soon"),
]

# Back-compat alias
UNIT_2 = next(u for u in UNITS if u["id"] == 2)


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


def load_activity_markdown(unit: dict, activity: dict) -> str:
    path = unit_notes_dir(unit["id"]) / activity["file"]
    if not path.is_file():
        return f"*Notes file not found: {path.name}*"
    return path.read_text(encoding="utf-8")


def diagram_path(unit: dict, activity: dict) -> str | None:
    name = activity.get("diagram")
    if not name:
        return None
    img = unit_images_dir(unit["id"]) / name
    return str(img) if img.is_file() else None


def activity_diagrams(unit: dict, activity: dict) -> list[tuple[str, str]]:
    out: list[tuple[str, str]] = []
    img_dir = unit_images_dir(unit["id"])
    for item in activity.get("diagrams") or []:
        path = img_dir / item["file"]
        if path.is_file():
            out.append((str(path), item.get("caption", "")))
    if out:
        return out
    single = diagram_path(unit, activity)
    if single:
        out.append((single, "Lesson diagram"))
    return out
