"""Error pattern analysis from incorrect answers."""

from __future__ import annotations

import re
from collections import defaultdict

from practice_quality.mastery import _skill_label, _strategy_name, _strategy_id


def _picked_and_correct(q: dict, ans: dict) -> tuple[str, str]:
    if "picked" in ans:
        return str(ans.get("picked", "?")), str(ans.get("correct_val", "?"))
    opts = q.get("options") or []
    choice = ans.get("choice")
    picked = opts[choice] if isinstance(choice, int) and 0 <= choice < len(opts) else "?"
    correct_idx = q.get("answer")
    correct = opts[correct_idx] if isinstance(correct_idx, int) and 0 <= correct_idx < len(opts) else "?"
    return str(picked), str(correct)


def _parse_num(text: str) -> float | None:
    s = str(text).strip().replace("−", "-")
    if re.fullmatch(r"-?\d+/\d+", s):
        a, b = s.split("/", 1)
        return int(a) / int(b) if int(b) else None
    if re.fullmatch(r"-?\d+", s):
        return float(int(s))
    return None


def _detect_mistake_type(q: dict, picked: str, correct: str) -> str:
    sid = _strategy_id(q) or 0
    lvl = str(q.get("level", ""))
    skill = _skill_label(q).lower()
    eq = str(q.get("equation", q.get("question", ""))).lower()

    pn, cn = _parse_num(picked), _parse_num(correct)
    if pn is not None and cn is not None:
        if pn == -cn or (pn != 0 and cn != 0 and abs(pn + cn) < 1e-6):
            return "sign_error"
        if abs(abs(pn) - abs(cn)) < 1e-6 and pn != cn:
            return "sign_error"
        if sid in (4,) or "distribut" in skill or "negative" in skill:
            if "(-" in eq or "-(" in eq or re.search(r"-\d+\(", eq):
                return "negative_distribution"
        if sid in (5, 3) or "fraction" in skill:
            return "fraction_operation"
        if sid == 2:
            return "inverse_operations"
        if abs(pn) < abs(cn) and cn != 0:
            return "incomplete_isolation"

    pl, cl = picked.lower(), correct.lower()
    if "distribut" in pl or "expand" in pl or "distribut" in skill:
        return "incorrect_distribution"
    if "combine" in pl or "like term" in pl:
        return "combining_unlike_terms"
    if sid == 4 and lvl in ("B", "C"):
        return "negative_distribution"
    if sid == 5 or "fraction" in skill:
        return "fraction_operation"
    if sid == 3:
        return "combining_unlike_terms"
    if sid == 2:
        return "inverse_operations"
    return "arithmetic_mistake"


_PATTERN_LABELS = {
    "sign_error": "Sign mistakes (e.g. treating − × − as −)",
    "negative_distribution": "Negative distribution / distributing the negative incorrectly",
    "incomplete_isolation": "Incomplete isolation of the variable (stopped too early)",
    "incorrect_distribution": "Incorrect use of the distributive property",
    "fraction_operation": "Fractional coefficient or LCD mistakes",
    "combining_unlike_terms": "Combining unlike terms or moving terms incorrectly",
    "inverse_operations": "Inverse operation order or choice",
    "coefficient_confusion": "Coefficient confusion when scaling both sides",
    "arithmetic_mistake": "Arithmetic slip in an otherwise correct method",
}


_PATTERN_NARRATIVES = {
    "negative_distribution": (
        "When distributing a negative, each term inside the parentheses must change sign."
    ),
    "incomplete_isolation": (
        "After isolating the variable term, divide or multiply to get the variable alone "
        "(e.g. from 1/4 x = 6, multiply both sides by 4 to get x = 24)."
    ),
    "sign_error": "Watch for sign changes when removing parentheses or moving terms across the equals sign.",
    "fraction_operation": "Clear fractions with the LCD or multiply both sides by the denominator before isolating.",
    "incorrect_distribution": "Multiply the outside factor by every term inside the parentheses.",
    "combining_unlike_terms": "Only combine terms with the same variable and power.",
    "inverse_operations": "Undo operations in reverse order — undo addition/subtraction before multiplication/division.",
    "coefficient_confusion": "Apply the same operation to both sides when clearing a coefficient.",
    "arithmetic_mistake": "Recheck basic arithmetic on each step.",
}


def analyze_errors(questions: list[dict], answers: list[dict]) -> dict:
    wrong_by_skill: dict[str, list[dict]] = defaultdict(list)
    pattern_counts: dict[str, int] = defaultdict(int)
    examples: dict[str, list[dict]] = defaultdict(list)

    for idx, (q, ans) in enumerate(zip(questions, answers)):
        if q.get("is_warmup") or ans.get("correct"):
            continue
        picked, correct = _picked_and_correct(q, ans)
        skill = _skill_label(q)
        pattern = _detect_mistake_type(q, picked, correct)
        pattern_counts[pattern] += 1
        wrong_by_skill[skill].append(
            {"index": idx, "question": q, "picked": picked, "correct": correct, "pattern": pattern}
        )
        if len(examples[pattern]) < 2:
            eq = q.get("equation") or q.get("question", "")
            examples[pattern].append(
                {"question": str(eq), "picked": picked, "correct": correct, "skill": skill}
            )

    patterns = []
    for key, count in sorted(pattern_counts.items(), key=lambda x: (-x[1], x[0])):
        if count < 1:
            continue
        patterns.append(
            {
                "pattern": key,
                "label": _PATTERN_LABELS.get(key, key.replace("_", " ").title()),
                "count": count,
                "narrative": _PATTERN_NARRATIVES.get(key, ""),
                "examples": examples.get(key, []),
            }
        )

    weak_skills = []
    for skill, items in wrong_by_skill.items():
        weak_skills.append({"skill": skill, "wrong_count": len(items), "items": items})
    weak_skills.sort(key=lambda x: (-x["wrong_count"], x["skill"]))

    return {
        "patterns": patterns,
        "weak_skills": weak_skills,
        "total_wrong": sum(pattern_counts.values()),
    }
