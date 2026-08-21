"""Extract NCERT exercise items from chapter PDFs and build MCQ banks (no LLM)."""

from __future__ import annotations

import re
import uuid
from pathlib import Path

import harshit_chapter_pdf as hcp
import harshit_chapter_questions as hcq
import harshit_math_prereqs as hmp
import harshit_prereq_topics as hpt

# NCERT exercise section → (prereq_id, topic_id, default levels)
EXERCISE_TOPIC_MAP: dict[int, dict[str, tuple[int, int, list[str]]]] = {
    1: {
        "1.1": (1, 1, ["A", "B"]),
        "1.2": (1, 5, ["A", "B"]),
        "1.3": (1, 5, ["B", "C"]),
        "1.4": (1, 3, ["A", "B"]),
        "1.5": (1, 4, ["A", "B"]),
        "1.6": (1, 2, ["B", "C"]),
    },
    2: {
        "2.1": (2, 1, ["A", "B"]),
        "2.2": (2, 2, ["A", "B"]),
        "2.3": (2, 3, ["A", "B"]),
        "2.4": (2, 2, ["B", "C"]),
        "2.5": (2, 3, ["B", "C"]),
    },
    4: {"4.1": (2, 4, ["A", "B"]), "4.2": (2, 4, ["B", "C"]), "4.3": (2, 4, ["C", "D"])},
    3: {"3.1": (3, 1, ["A", "B"]), "3.2": (3, 1, ["B", "C"]), "3.3": (3, 2, ["A", "B"])},
    13: {
        "13.1": (5, 2, ["A", "B"]),
        "13.2": (5, 2, ["B", "C"]),
        "13.3": (5, 2, ["C", "D"]),
        "13.4": (5, 3, ["A", "B"]),
        "13.5": (5, 3, ["B", "C"]),
        "13.6": (5, 3, ["C", "D"]),
        "13.7": (5, 3, ["D", "E"]),
        "13.8": (5, 3, ["C", "E"]),
        "13.9": (5, 3, ["D", "E"]),
    },
    14: {
        "14.1": (6, 1, ["A", "B"]),
        "14.2": (6, 1, ["B", "C"]),
        "14.3": (6, 1, ["C", "D"]),
        "14.4": (6, 2, ["A", "B"]),
        "14.5": (6, 2, ["B", "C"]),
    },
    15: {
        "15.1": (6, 3, ["A", "B"]),
        "15.2": (6, 3, ["B", "C"]),
    },
}


def _topic_for_exercise(chapter_num: int, section: str, prompt: str) -> tuple[int, int, str]:
    ex_num = re.search(r"EXERCISE\s+([\d.]+)", section, re.I)
    ex_key = ex_num.group(1) if ex_num else ""
    mapping = EXERCISE_TOPIC_MAP.get(chapter_num, {})
    if ex_key in mapping:
        pid, tid, levels = mapping[ex_key]
        return pid, tid, levels[0]
    hints = CHAPTER_TOPIC_HINTS.get(chapter_num, [(1, 1, ())])
    for pid, tid, kws in hints:
        if any(k in prompt.lower() for k in kws):
            return pid, tid, "B" if "find" in prompt.lower() else "A"
    pid, tid, _ = hints[0]
    return pid, tid, "A"


def _levels_for_exercise(chapter_num: int, section: str) -> list[str]:
    ex_num = re.search(r"EXERCISE\s+([\d.]+)", section, re.I)
    ex_key = ex_num.group(1) if ex_num else ""
    mapping = EXERCISE_TOPIC_MAP.get(chapter_num, {})
    if ex_key in mapping:
        return mapping[ex_key][2]
    return ["A", "B"]


CHAPTER_TOPIC_HINTS: dict[int, list[tuple[int, int, tuple[str, ...]]]] = {
    1: [
        (1, 1, ("number line", "integer", "whole number", "natural number", "distance")),
        (1, 2, ("rational", "fraction", "between")),
        (1, 3, ("exponent", "power", "laws")),
        (1, 4, ("rationalize", "denominator", "sqrt", "√")),
        (1, 5, ("irrational", "real number", "decimal expansion", "terminate", "recurring")),
    ],
    2: [
        (2, 1, ("add", "subtract", "polynomial", "like terms")),
        (2, 2, ("multiply", "product", "expand")),
        (2, 3, ("factor", "factorisation", "identity")),
    ],
    4: [(2, 4, ("linear", "two variable", "x", "y", "equation"))],
    3: [(3, 1, ("coordinate", "quadrant", "plot", "point")), (3, 2, ("line", "equation", "graph"))],
    5: [(4, 1, ("euclid", "axiom", "postulate", "geometry"))],
    6: [(4, 1, ("angle", "line", "parallel", "transversal"))],
    7: [(4, 2, ("triangle", "congruence", "sas", "asa"))],
    8: [(4, 3, ("quadrilateral", "parallelogram", "rectangle"))],
    10: [(4, 4, ("circle", "chord", "arc", "diameter"))],
    12: [(5, 1, ("heron", "area", "triangle", "semiperimeter"))],
    13: [
        (5, 2, ("surface area", "lateral", "cuboid", "cube", "cylinder", "cone", "sphere")),
        (5, 3, ("volume", "capacity", "litre", "hemisphere")),
    ],
    14: [
        (6, 1, ("mean", "median", "mode", "frequency", "data")),
        (6, 2, ("histogram", "bar graph", "frequency polygon", "graph")),
    ],
    15: [(6, 3, ("probability", "coin", "die", "dice", "event", "outcome"))],
}


def _mcq_from_fill_blank(
    prereq_id: int,
    topic_id: int,
    level: str,
    stmt: str,
    chapter_num: int,
    chapter_ref: str,
) -> dict | None:
    """Convert NCERT '(exterior/ interior)' fill-in items to proper MCQs."""
    m = re.search(r"\(([^/)]+)/\s*([^)]+)\)\s*\.?\s*$", stmt)
    if not m:
        return None
    w1 = m.group(1).strip().title()
    w2 = m.group(2).strip().title()
    stem = re.sub(r"\s+", " ", stmt[: m.start()]).strip().rstrip(".")
    stem_lower = stem.lower()

    if "centre" in stem_lower and "circle" in stem_lower and "lies" in stem_lower:
        question = "Where does the centre of a circle lie?"
        correct = "Interior"
    elif "greater than" in stem_lower and "radius" in stem_lower:
        question = "A point whose distance from the centre is greater than the radius lies in the ___ of the circle."
        correct = "Exterior"
    elif "equal to" in stem_lower and "radius" in stem_lower:
        question = "A point whose distance from the centre equals the radius lies ___ the circle."
        correct = "On"
    elif "less than" in stem_lower and "radius" in stem_lower:
        question = "A point whose distance from the centre is less than the radius lies in the ___ of the circle."
        correct = "Interior"
    else:
        stem_clean = re.sub(r"\s+in\s+of\s+", " in the ", stem, flags=re.I)
        question = f"Which word best completes this statement? {stem_clean}"
        correct = w2 if w2.lower() in ("interior", "exterior", "on") else w1

    pool = [correct, w1, w2, "On the circle", "Exterior", "Interior", "Boundary"]
    options: list[str] = []
    for item in pool:
        label = item.strip().title() if item.lower() not in ("on",) else "On the circle"
        if label and label not in options:
            options.append(label)
        if len(options) >= 4:
            break
    while len(options) < 4:
        for extra in ("Circumference", "Diameter", "Sector"):
            if extra not in options:
                options.append(extra)
            if len(options) >= 4:
                break
    if correct == "On":
        correct = "On the circle"
    if correct not in options:
        options[0] = correct
    else:
        options = [correct] + [o for o in options if o != correct]
        options = options[:4]

    return hcq.normalize_question(
        {
            "question": question,
            "options": options[:4],
            "answer": 0,
            "explanation": f"See {chapter_ref} in NCERT Chapter {chapter_num}.",
            "source": "chapter_pdf",
            "chapter_num": chapter_num,
            "chapter_ref": chapter_ref,
        },
        prereq_id,
        topic_id,
        level,
    )


def _parse_exercise_items(text: str, chapter_num: int) -> list[dict]:
    """Offline extract: fill-in-blank MCQs only — no true/false (templates/xAI handle compute drills)."""
    questions: list[dict] = []
    for m in re.finditer(r"EXERCISE\s+[\d.]+\s*(.*?)(?=EXERCISE|\Z)", text, re.I | re.S):
        section = m.group(0).split("\n", 1)[0].strip()
        body = m.group(1)
        if "true or false" in body.lower() or "state whether" in body.lower():
            questions.extend(_parse_fill_blank_only(body, chapter_num, section))
    return questions


def _parse_fill_blank_only(block: str, chapter_num: int, section: str) -> list[dict]:
    out: list[dict] = []
    for m in re.finditer(r"\(([ivxlc]+)\)\s*(.+?)(?=\([ivxlc]+\)|$)", block, re.I | re.S):
        stmt = re.sub(r"\s+", " ", m.group(2)).strip(" .")
        stmt = re.split(r"\d+\.\s|Example\s|EXERCISE", stmt, maxsplit=1)[0].strip(" .")
        if not re.search(r"\([^/)]+/\s*[^)]+\)\s*\.?\s*$", stmt):
            continue
        prereq_id, topic_id, level = _topic_for_exercise(chapter_num, section, stmt)
        q = _mcq_from_fill_blank(prereq_id, topic_id, level, stmt, chapter_num, section)
        if q:
            out.append(q)
    return out


def _parse_examples(text: str, chapter_num: int) -> list[dict]:
    """Deprecated — example blocks become low-quality meta MCQs; use xAI instead."""
    return []


def extract_questions_for_chapter(chapter_num: int) -> list[dict]:
    prereq = None
    aliases = None
    for p in hmp.list_prereqs():
        for ch in p.get("class9_chapters", []):
            if ch["number"] == chapter_num:
                prereq = p
                aliases = ch.get("folder_aliases")
                break
    bundle = hcp.extract_chapter_text(chapter_num, aliases)
    if not bundle["has_text"]:
        return []

    text = bundle["text"]
    items: list[dict] = []
    items.extend(_parse_exercise_items(text, chapter_num))
    items.extend(_parse_examples(text, chapter_num))

    # Dedupe by question text
    seen: set[str] = set()
    unique: list[dict] = []
    for q in items:
        t = q.get("question", "")
        if t in seen:
            continue
        seen.add(t)
        unique.append(q)
    return unique


def build_offline_banks(chapters: list[int] | None = None) -> int:
    """Parse PDFs and write question banks. Returns total questions added."""
    if chapters is None:
        chapters = sorted({hcq.chapter_for_topic(p, t) for p in hpt.TOPICS for t in hpt.TOPICS[p] if hcq.chapter_for_topic(p, t)})

    total = 0
    for ch in chapters:
        if ch is None:
            continue
        qs = extract_questions_for_chapter(ch)
        by_slot: dict[tuple[int, int, str], list[dict]] = {}
        for q in qs:
            key = (q["prereq_id"], q["topic"], q["level"])
            by_slot.setdefault(key, []).append(q)
        for (pid, tid, lvl), bucket in by_slot.items():
            total += hcq.add_questions(pid, tid, lvl, bucket, chapter_num=ch)
    return total
