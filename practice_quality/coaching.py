"""Parent coaching concepts — group mistake patterns into 3–4 teachable ideas with examples."""

from __future__ import annotations

# Pattern keys from error_analysis → consolidated parent-facing concepts.
_COACHING_CONCEPTS: list[dict] = [
    {
        "key": "finish_isolation",
        "title": "Finish isolating the variable",
        "idea": (
            "After the x-term is alone on one side, undo the coefficient — multiply or divide "
            "both sides so x is by itself."
        ),
        "rule": "Isolate the x-term first, then clear the number in front of x.",
        "patterns": {"incomplete_isolation", "coefficient_confusion"},
        "default_example": "1/4 x = 6",
        "default_walkthrough": (
            "We have x times 1/4, not plain x. Multiply both sides by 4: x = 24. "
            "Check: 1/4 of 24 is 6."
        ),
    },
    {
        "key": "signs",
        "title": "Signs and negatives",
        "idea": (
            "A minus in front of parentheses flips every sign inside. "
            "Remember − × − = + when distributing or moving terms."
        ),
        "rule": "When a negative distributes, change the sign of each term inside the parentheses.",
        "patterns": {"sign_error", "negative_distribution", "incorrect_distribution"},
        "default_example": "8 − 3(2x − 5) = 11",
        "default_walkthrough": (
            "Distribute −3: 8 − 6x + 15 = 11 → −6x + 23 = 11 → −6x = −12 → x = 2. "
            "Check by plugging x = 2 back in."
        ),
    },
    {
        "key": "fractions",
        "title": "Fractions and LCD",
        "idea": (
            "Clear fractions early — multiply every term on both sides by the LCD "
            "(lowest common denominator), then solve."
        ),
        "rule": "Find the LCD, multiply the whole equation, then solve like usual.",
        "patterns": {"fraction_operation"},
        "default_example": "x/4 + 2 = 3/4",
        "default_walkthrough": (
            "LCD is 4. Multiply everything by 4: x + 8 = 3 → x = −5. Check in the original equation."
        ),
    },
    {
        "key": "inverse_ops",
        "title": "Inverse operations in order",
        "idea": (
            "Undo what was done to x in reverse order — move x-terms together, "
            "move constants together, then divide."
        ),
        "rule": "Addition/subtraction first, then multiplication/division.",
        "patterns": {"inverse_operations", "combining_unlike_terms", "arithmetic_mistake"},
        "default_example": "−4x + 10 = −9x − 15",
        "default_walkthrough": (
            "Add 9x: 5x + 10 = −15. Subtract 10: 5x = −25. Divide by 5: x = −5. Check by substitution."
        ),
    },
]


def _example_from_patterns(patterns: list[dict], pattern_keys: set[str]) -> tuple[str, str] | None:
    """Pick a real missed question from this session when available."""
    for p in patterns:
        if p.get("pattern") not in pattern_keys:
            continue
        for ex in p.get("examples") or []:
            q = str(ex.get("question", "")).strip()
            if q:
                picked = ex.get("picked", "?")
                correct = ex.get("correct", "?")
                walk = (
                    f"They answered {picked}; the correct value is {correct}. "
                    f"Walk through step-by-step and watch for: {p.get('label', 'this pattern')}."
                )
                return q, walk
    return None


def build_coaching_concepts(errors: dict, *, student_name: str = "Student") -> list[dict]:
    """
    Return 3–4 parent-facing concepts with example problems to review together.
    Only includes concepts that match mistakes from this session.
    """
    patterns = errors.get("patterns") or []
    if not patterns:
        return []

    pattern_counts = {p.get("pattern"): int(p.get("count", 0)) for p in patterns}
    first_name = student_name.split()[0] if student_name.strip() else "your child"
    out: list[dict] = []

    for concept in _COACHING_CONCEPTS:
        matched = [p for p in patterns if p.get("pattern") in concept["patterns"]]
        if not matched:
            continue
        mistake_count = sum(int(p.get("count", 0)) for p in matched)
        labels = [p.get("label", "") for p in matched if p.get("label")]

        example_q, walkthrough = _example_from_patterns(patterns, concept["patterns"]) or (
            concept["default_example"],
            concept["default_walkthrough"],
        )

        out.append(
            {
                "title": concept["title"],
                "idea": concept["idea"],
                "rule": concept["rule"],
                "example": example_q,
                "walkthrough": walkthrough,
                "mistake_count": mistake_count,
                "from_session": bool(_example_from_patterns(patterns, concept["patterns"])),
                "patterns": labels,
            }
        )

    if out:
        out[0]["intro"] = (
            f"Based on {first_name}'s missed questions, review these {len(out)} ideas together "
            f"(about 15–20 minutes). Use the example, then ask them to explain each step aloud."
        )
    return out
