"""Catalog of high-frequency CBSE Class 10 Math exam question types."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExamType:
    id: str
    unit_id: int
    topic_id: int
    level: str
    title: str
    board_stem: str


# Maps each canonical board question pattern to a practice slot (unit, topic, level).
EXAM_TYPES: tuple[ExamType, ...] = (
    # Unit 1 — Real Numbers
    ExamType("u1_euclid_hcf", 1, 2, "D", "Euclid's division HCF", "Use Euclid's division algorithm to find the HCF of 135 and 225."),
    ExamType("u1_hcf_lcm_prime", 1, 2, "B", "HCF & LCM by prime factorisation", "Find the HCF and LCM of 96 and 404 using prime factorisation."),
    ExamType("u1_sqrt2_irrational", 1, 3, "D", "Prove √2 irrational", "Prove that √2 is irrational."),
    ExamType("u1_sqrt3_irrational", 1, 3, "D", "Prove √3 irrational", "Prove that √3 is irrational."),
    ExamType("u1_sqrt5_irrational", 1, 3, "D", "Prove √5 irrational", "Prove that √5 is irrational."),
    ExamType("u1_sum_irrational", 1, 4, "D", "Rational + irrational sum", "Show that 3 + 2√5 is irrational."),
    ExamType("u1_hcf_from_product_lcm", 1, 2, "C", "HCF from product & LCM", "Find the HCF of two numbers when their product and LCM are given."),
    ExamType("u1_hcf_lcm_pairs", 1, 2, "E", "Possible (a,b) from HCF & LCM", "If HCF(a,b) = 12 and LCM(a,b) = 420, find possible values of a and b."),
    ExamType("u1_euclid_first_remainder", 1, 2, "D", "Euclid — first remainder", "Using Euclid's algorithm on 135 and 225, find the first remainder."),
    ExamType("u1_prime_factor_step", 1, 2, "B", "Prime factorisation step", "Prime factorise 96 (step 1 of HCF/LCM by prime factors)."),
    ExamType("u1_prime_hcf_step", 1, 2, "B", "HCF from prime factors", "Find HCF using prime factorisation (step 2)."),
    ExamType("u1_prime_lcm_step", 1, 2, "C", "LCM from prime factors", "Find LCM using prime factorisation (step 2)."),
    ExamType("u1_hcf_lcm_pair_step", 1, 2, "E", "Pair from HCF and LCM", "If HCF(a,b) and LCM(a,b) are given, find a valid pair (stepwise)."),
    ExamType("u1_irrational_assume_step", 1, 3, "D", "Irrational proof — Step 1", "To prove √2 is irrational, what is Step 1?"),
    ExamType("u1_irrational_contradiction_step", 1, 3, "D", "Irrational proof — Step 2", "After assuming √p = p/q, what follows in the proof?"),
    # Unit 2 — Polynomials
    ExamType("u2_zeroes_verify", 2, 3, "C", "Zeroes & coefficients verify", "Find the zeroes of a quadratic polynomial and verify the relationship between zeroes and coefficients."),
    ExamType("u2_alpha_beta_sum", 2, 3, "B", "α+β and αβ", "If α and β are zeroes of (2x²−5x+3), find α+β and αβ."),
    ExamType("u2_form_from_zeroes", 2, 3, "C", "Form quadratic from zeroes", "Find a quadratic polynomial whose zeroes are 3 and −5."),
    ExamType("u2_find_k_one_zero", 2, 4, "E", "Find k from one zero", "If one zero of (2x²+kx+6) is 2, find k and the other zero."),
    ExamType("u2_equal_zeroes_k", 2, 3, "D", "Equal zeroes — find k", "Find the value of k if the zeroes of (x²−(k+3)x+k) are equal."),
    ExamType("u2_form_sum_product", 2, 3, "C", "Form polynomial sum & product", "Form a quadratic polynomial when sum and product of zeroes are given."),
    ExamType("u2_graphical_zeroes", 2, 2, "C", "Graphical zeroes", "Verify graphically the zeroes of a quadratic polynomial."),
    ExamType("u2_zeroes_x2_7x_12", 2, 4, "D", "Zeroes of x²−7x+12", "Find the zeroes of (x²−7x+12) and verify the relationships."),
    ExamType("u2_surd_zero_polynomial", 2, 3, "D", "Quadratic from surd zeroes", "Find a quadratic polynomial whose zeroes are (5 − 2√3) and (5 + 2√3)."),
    ExamType("u2_surd_zero_product", 2, 3, "D", "Product of surd zeroes", "If zeroes are conjugate surds a±b√c, find their product."),
    ExamType("u2_surd_zero_sum", 2, 3, "C", "Sum of surd zeroes", "If zeroes are conjugate surds a±b√c, find their sum."),
    ExamType("u2_cubic_factor_all_zeroes", 2, 4, "E", "Cubic zeroes from linear factor", "Obtain all zeroes of p(x) = 2x³ + x² − 5x + 2 if (x − 1) is a factor."),
    ExamType("u2_cubic_factor_quotient", 2, 4, "E", "Quadratic quotient from cubic", "Divide a cubic by (x − a) to obtain the quadratic factor."),
    ExamType("u2_cubic_verify_quadratic", 2, 4, "E", "Verify quadratic zero-coefficient relations", "Verify sum/product of zeroes for the quadratic factor obtained."),
    # Unit 3 — Pair of Linear Equations
    ExamType("u3_substitution", 3, 2, "C", "Substitution method", "Solve two linear equations by substitution method."),
    ExamType("u3_elimination", 3, 3, "C", "Elimination method", "Solve a pair of equations by elimination method."),
    ExamType("u3_cross_mult", 3, 4, "B", "Cross-multiplication", "Solve a pair of equations by cross-multiplication method."),
    ExamType("u3_unique_k", 3, 4, "C", "k for unique solution", "Find the value of k for which a pair of linear equations has a unique solution."),
    ExamType("u3_infinite_k", 3, 1, "D", "k for infinitely many", "Find k for which equations have infinitely many solutions."),
    ExamType("u3_no_solution_k", 3, 1, "C", "k for no solution", "Find k for which equations have no solution."),
    ExamType("u3_word_ages", 3, 4, "D", "Word problem — ages", "Solve a word problem based on ages."),
    ExamType("u3_word_two_digit", 3, 4, "D", "Word problem — two-digit number", "Solve a word problem based on two-digit numbers."),
    ExamType("u3_word_income", 3, 4, "E", "Word problem — income & expenditure", "Solve a problem based on income and expenditure."),
    ExamType("u3_word_speed", 3, 4, "E", "Word problem — speed & distance", "Solve a problem involving speed and distance."),
    ExamType("u3_word_cost", 3, 4, "E", "Word problem — cost of articles", "Solve a problem based on cost of two articles."),
    ExamType("u3_substitution_express", 3, 2, "B", "Substitution — express variable", "Step 1: express x from one equation."),
    ExamType("u3_substitution_y_step", 3, 2, "D", "Substitution — find y", "Step 2: find y after substitution."),
    ExamType("u3_substitution_full", 3, 2, "C", "Substitution — full solution", "Solve a pair by substitution (all steps)."),
    ExamType("u3_elimination_y_step", 3, 3, "D", "Elimination — find y", "Step 3: find y after elimination."),
    ExamType("u3_elimination_full", 3, 3, "C", "Elimination — full solution", "Solve by elimination (all steps)."),
    ExamType("u3_consistency_ratios", 3, 4, "D", "Consistency via ratios", "Compare a₁/a₂, b₁/b₂, c₁/c₂ to classify the pair."),
    ExamType("u3_word_ages_setup", 3, 4, "D", "Ages word problem — setup", "Form equations for a father-son age problem (Step 1)."),
    ExamType("u3_word_ages_solve", 3, 4, "D", "Ages word problem — solve", "Find present ages from the age word problem (Step 2)."),
    # Unit 4 — Quadratic Equations
    ExamType("u4_factorisation", 4, 2, "B", "Solve by factorisation", "Solve a quadratic equation by factorisation."),
    ExamType("u4_quadratic_formula", 4, 3, "B", "Quadratic formula", "Solve a quadratic equation using the quadratic formula."),
    ExamType("u4_solve_2x2_7x_3", 4, 3, "C", "Solve 2x²−7x+3=0", "Solve (2x²−7x+3=0)."),
    ExamType("u4_nature_roots", 4, 4, "B", "Nature of roots", "Find the nature of roots using the discriminant."),
    ExamType("u4_equal_roots_k", 4, 4, "C", "Equal roots — find k", "Find k if a quadratic equation has equal roots."),
    ExamType("u4_no_real_roots_k", 4, 4, "C", "No real roots — find k", "Find k if a quadratic equation has no real roots."),
    ExamType("u4_form_from_roots", 4, 1, "C", "Form equation from roots", "Form a quadratic equation when its roots are given."),
    ExamType("u4_consecutive_integers", 4, 1, "D", "Consecutive integers", "Solve a problem based on consecutive integers."),
    ExamType("u4_rectangle_area", 4, 1, "D", "Rectangle area", "Solve a problem based on area of a rectangle."),
    ExamType("u4_speed_time", 4, 1, "E", "Speed & time", "Solve a problem based on speed/time."),
    ExamType("u4_verify_sum_product", 4, 1, "C", "Verify sum & product of roots", "Find the roots and verify their sum and product."),
    # Unit 5 — AP
    ExamType("u5_nth_term", 5, 2, "B", "nth term of AP", "Find the nth term of an AP."),
    ExamType("u5_20th_term", 5, 2, "C", "20th term of AP", "Find the 20th term of a given AP."),
    ExamType("u5_first_term_d", 5, 2, "D", "First term & common difference", "Find the first term and common difference when two terms are given."),
    ExamType("u5_sum_n_terms", 5, 3, "B", "Sum of n terms", "Find the sum of first n terms of an AP."),
    ExamType("u5_sum_20_terms", 5, 3, "C", "Sum of first 20 terms", "Find the sum of first 20 terms of an AP."),
    ExamType("u5_which_term", 5, 2, "D", "Which term equals given number", "Find which term of an AP is a given number."),
    ExamType("u5_number_of_terms", 5, 3, "D", "Number of terms from sum", "Find the number of terms when the sum is given."),
    ExamType("u5_word_savings", 5, 4, "C", "AP word — savings", "Solve an AP word problem based on savings."),
    ExamType("u5_word_seating", 5, 4, "D", "AP word — seating", "Solve an AP problem based on seating arrangements."),
    ExamType("u5_three_numbers_ap", 5, 4, "E", "Three numbers in AP", "Find three numbers in AP whose sum and product are given."),
    # Unit 6 — Triangles
    ExamType("u6_bpt_state", 6, 2, "C", "State & apply BPT", "State and prove the Basic Proportionality Theorem."),
    ExamType("u6_bpt_side", 6, 2, "D", "BPT — unknown side", "Apply BPT to find an unknown side."),
    ExamType("u6_aa_similar", 6, 3, "B", "Similarity AA", "Prove two triangles are similar using AA criterion."),
    ExamType("u6_sss_similar", 6, 3, "C", "Similarity SSS", "Prove similarity using SSS criterion."),
    ExamType("u6_sas_similar", 6, 3, "C", "Similarity SAS", "Prove similarity using SAS criterion."),
    ExamType("u6_similar_sides", 6, 3, "D", "Unknown sides from similarity", "Find unknown sides using similarity of triangles."),
    ExamType("u6_pythagoras_similar", 6, 4, "C", "Pythagoras via similarity", "Prove the Pythagoras theorem using similarity."),
    ExamType("u6_area_ratio", 6, 4, "D", "Area ratio similar triangles", "If two similar triangles have a given ratio of sides, find their areas."),
    ExamType("u6_ratio_areas", 6, 4, "D", "Ratio of areas", "Find the ratio of areas of two similar triangles."),
    ExamType("u6_similar_proof", 6, 4, "E", "Proof using similarity", "Prove a given result using the similarity of triangles."),
    # Unit 7 — Coordinate Geometry
    ExamType("u7_distance_two_points", 7, 1, "B", "Distance between points", "Find the distance between two points."),
    ExamType("u7_distance_origin", 7, 1, "B", "Distance from origin", "Find the distance between a point and the origin."),
    ExamType("u7_midpoint", 7, 2, "B", "Midpoint", "Find the midpoint of a line segment."),
    ExamType("u7_section_formula", 7, 2, "C", "Section formula", "Find the coordinates of a point dividing a line segment in a given ratio."),
    ExamType("u7_find_ratio", 7, 2, "D", "Find division ratio", "Find the ratio in which a point divides a line segment."),
    ExamType("u7_collinear", 7, 3, "C", "Collinear points", "Show that three given points are collinear."),
    ExamType("u7_triangle_area", 7, 3, "C", "Area of triangle", "Find the area of a triangle using coordinates."),
    ExamType("u7_right_triangle", 7, 4, "D", "Right-angled triangle check", "Determine whether three points form a right-angled triangle."),
    ExamType("u7_missing_coordinate", 7, 4, "D", "Missing coordinate", "Find the missing coordinate when the distance between two points is given."),
    # Unit 8 — Trigonometry
    ExamType("u8_standard_angles", 8, 2, "A", "Standard angle values", "Find the values of standard trigonometric ratios at 0°, 30°, 45°, 60° and 90°."),
    ExamType("u8_eval_expression", 8, 2, "B", "Evaluate trig expression", "Evaluate an expression involving standard trigonometric ratios."),
    ExamType("u8_sin_to_cos_tan", 8, 1, "C", "From sin θ find cos & tan", "If sin θ is given, find cos θ and tan θ."),
    ExamType("u8_tan_to_sin_cos", 8, 1, "C", "From tan θ find sin & cos", "If tan θ is given, find sin θ and cos θ."),
    ExamType("u8_prove_identity", 8, 3, "C", "Prove trig identity", "Prove a trigonometric identity using fundamental identities."),
    ExamType("u8_sin2_cos2", 8, 3, "B", "sin²θ+cos²θ=1", "Prove an identity involving (sin²θ+cos²θ=1)."),
    ExamType("u8_one_plus_tan2", 8, 3, "C", "1+tan²θ=sec²θ", "Prove an identity involving (1+tan²θ=sec²θ)."),
    ExamType("u8_simplify", 8, 4, "B", "Simplify trig expression", "Simplify a trigonometric expression."),
    ExamType("u8_find_angle", 8, 1, "D", "Find θ from ratio", "Find θ when a trigonometric ratio is given."),
    # Unit 9 — Applications of Trigonometry
    ExamType("u9_elevation_height", 9, 2, "B", "Angle of elevation — height", "Find the height of a tower using angle of elevation."),
    ExamType("u9_elevation_distance", 9, 3, "B", "Angle of elevation — distance", "Find the distance of an object from a tower."),
    ExamType("u9_depression", 9, 1, "C", "Angle of depression", "Solve a problem involving angle of depression."),
    ExamType("u9_two_angles_height", 9, 2, "D", "Two angles — building height", "Find the height of a building when the angle of elevation changes."),
    ExamType("u9_two_position", 9, 4, "D", "Two-position observation", "Solve a two-position observation problem involving a tower."),
    ExamType("u9_ladder_wall", 9, 4, "C", "Ladder and wall", "Solve a problem involving a ladder and a wall."),
    # Unit 10 — Circles
    ExamType("u10_tangent_perp", 10, 1, "C", "Tangent ⊥ radius", "Prove that tangent at any point of a circle is perpendicular to the radius."),
    ExamType("u10_equal_tangents", 10, 2, "B", "Equal tangents from external point", "Prove that tangents drawn from an external point to a circle are equal."),
    ExamType("u10_tangent_length", 10, 3, "B", "Length of tangent", "Find the length of a tangent from an external point."),
    ExamType("u10_radius_from_tangent", 10, 3, "C", "Radius from tangent data", "Find the radius of a circle when tangent-related measurements are given."),
    ExamType("u10_tangent_proof", 10, 2, "D", "Proof with two tangents", "Prove a result using two tangents drawn from an external point."),
    ExamType("u10_tangent_numerical", 10, 4, "C", "Tangent numerical problem", "Solve a numerical problem based on tangent and radius."),
    # Unit 11 — Areas Related to Circles
    ExamType("u11_sector_area", 11, 1, "B", "Area of sector", "Find the area of a sector."),
    ExamType("u11_arc_length", 11, 2, "B", "Length of arc", "Find the length of an arc."),
    ExamType("u11_segment_area", 11, 3, "C", "Area of segment", "Find the area of a segment of a circle."),
    ExamType("u11_shaded_circle_square", 11, 4, "C", "Shaded — circle & square", "Find the area of a shaded region involving a circle and square."),
    ExamType("u11_shaded_circle_triangle", 11, 4, "D", "Shaded — circle & triangle", "Find the area of a shaded region involving a circle and triangle."),
    ExamType("u11_sector_perimeter", 11, 2, "C", "Perimeter of sector", "Find the perimeter of a sector."),
    ExamType("u11_semicircles_composite", 11, 4, "D", "Composite semicircles", "Solve a composite figure problem involving semicircles."),
    # Unit 12 — Surface Areas & Volumes
    ExamType("u12_combo_sa_volume", 12, 2, "C", "Combination TSA/CSA & volume", "Find the TSA/CSA and volume of a combination of solids."),
    ExamType("u12_cone_cylinder", 12, 2, "D", "Cone and cylinder", "Solve a problem involving a cone and cylinder."),
    ExamType("u12_joined_solids_volume", 12, 3, "C", "Volume of joined solids", "Find the volume of a solid formed by joining two or more solids."),
    ExamType("u12_melting_conversion", 12, 3, "D", "Melting/conversion problem", "Solve a conversion/melting problem involving a cylinder, cone or sphere."),
    ExamType("u12_dimensions_from_volume", 12, 4, "D", "Dimensions from volume/SA", "Find the dimensions of a solid when its volume or surface area is given."),
)

EXAM_TYPE_BY_ID: dict[str, ExamType] = {t.id: t for t in EXAM_TYPES}

EXAM_TYPES_BY_SLOT: dict[tuple[int, int, str], list[str]] = {}
for _t in EXAM_TYPES:
    key = (_t.unit_id, _t.topic_id, _t.level)
    EXAM_TYPES_BY_SLOT.setdefault(key, []).append(_t.id)


def exam_types_for_slot(unit_id: int, topic_id: int, level: str) -> list[str]:
    return list(EXAM_TYPES_BY_SLOT.get((unit_id, topic_id, level), []))


def exam_type_ids_for_unit(unit_id: int) -> list[str]:
    return [t.id for t in EXAM_TYPES if t.unit_id == unit_id]
