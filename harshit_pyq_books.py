"""Parse Class 10 PYQ compilations into unit-scoped practice seeds."""

from __future__ import annotations

import hashlib
import re
from typing import Any

import harshit_class10_pyq_catalog as cat

_CTRL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
_WS = re.compile(r"\s+")
_Q_DOT = re.compile(r"^(\d{1,3})\.\s*(.*)$")
_Q_PAREN = re.compile(r"^(\d{1,3})\)\s*(.*)$")
_THUS = re.compile(r"\(([a-dA-D])\)\s*is correct", re.I)
_ANS_LINE = re.compile(r"^A*\s*Ans\s*:?\s*(.*)$", re.I)
_MARKS_BRACKET = re.compile(r"\[(\d+)\s*marks?\]", re.I)
_SCI_MARKS = re.compile(
    r"^(?:\d+\.\s*)?(ONE|TWO|THREE|FIVE)\s+MARKS?\s+QUESTIONS\s*$",
    re.I,
)
_MARKS_WORD = {"one": 1, "two": 2, "three": 3, "five": 5}
_BOARD_TAG = re.compile(r"\[(?:Board|CBSE)[^\]]*\]", re.I)
_CITATION = re.compile(r"^\[[^\]]+\]$")

# Book chapter numbers in "Science Objective pyq" (their numbering, not NCERT).
_SCIENCE_BY_NUMBER: dict[int, tuple[str, int, str]] = {
    1: ("chemistry", 1, "Chemical Reactions and Equations"),
    2: ("chemistry", 2, "Acids, Bases and Salts"),
    3: ("chemistry", 3, "Metals and Non-metals"),
    4: ("chemistry", 4, "Carbon and its Compounds"),
    6: ("biology", 1, "Life Processes"),
    7: ("biology", 2, "Control and Coordination"),
    8: ("biology", 3, "How do Organisms Reproduce?"),
    9: ("biology", 4, "Heredity"),
    10: ("physics", 1, "Light – Reflection and Refraction"),
    11: ("physics", 2, "The Human Eye and the Colourful World"),
    12: ("physics", 3, "Electricity"),
    13: ("physics", 4, "Magnetic Effects of Electric Current"),
}

_SCIENCE_TITLE_RULES: list[tuple[re.Pattern[str], tuple[str, int, str]]] = [
    (re.compile(r"chemical reaction", re.I), _SCIENCE_BY_NUMBER[1]),
    (re.compile(r"acid", re.I), _SCIENCE_BY_NUMBER[2]),
    (re.compile(r"metal", re.I), _SCIENCE_BY_NUMBER[3]),
    (re.compile(r"carbon", re.I), _SCIENCE_BY_NUMBER[4]),
    (re.compile(r"life process", re.I), _SCIENCE_BY_NUMBER[6]),
    (re.compile(r"control and coordination", re.I), _SCIENCE_BY_NUMBER[7]),
    (re.compile(r"reproduc", re.I), _SCIENCE_BY_NUMBER[8]),
    (re.compile(r"hered", re.I), _SCIENCE_BY_NUMBER[9]),
    (re.compile(r"human eye|colou?rful", re.I), _SCIENCE_BY_NUMBER[11]),
    (re.compile(r"\blight\b", re.I), _SCIENCE_BY_NUMBER[10]),
    (re.compile(r"magnet", re.I), _SCIENCE_BY_NUMBER[13]),
    (re.compile(r"electricity", re.I), _SCIENCE_BY_NUMBER[12]),
]


def norm_key(text: str) -> str:
    t = _WS.sub(" ", text.strip().lower())
    t = re.sub(r"[^\w\s]", "", t)
    return t[:240]


def _clean(text: str) -> str:
    text = _CTRL.sub("", text)
    text = text.replace("\u00a0", " ")
    return _WS.sub(" ", text).strip()


def _letters(text: str) -> int:
    return sum(1 for c in text if c.isalpha())


def _readable(text: str, *, min_letters: int) -> bool:
    letters = _letters(text)
    if letters < min_letters:
        return False
    return letters / max(len(text), 1) >= 0.28


def _make_id(prefix: str, kind: str, text: str) -> str:
    digest = hashlib.sha1(norm_key(text).encode()).hexdigest()[:10]
    return f"{prefix}_{kind}_{digest}"


def _empty_math() -> dict[int, dict[str, list]]:
    out: dict[int, dict[str, list]] = {}
    for unit_id, _title in cat.load_unit_titles():
        out[unit_id] = {"mcq": [], "assertion_reason": [], "vsa": [], "sa": [], "la": []}
    return out


def _written_bucket(marks: int) -> str:
    if marks <= 2:
        return "vsa"
    if marks <= 3:
        return "sa"
    return "la"


def _expl_line_ok(line: str) -> bool:
    cleaned = _clean(line)
    if not cleaned or _THUS.search(cleaned) or cleaned.startswith("["):
        return False
    words = [word for word in re.findall(r"[A-Za-z]{2,}", cleaned)]
    if len(words) >= 4:
        return True
    return _letters(cleaned) >= 12 and _letters(cleaned) / max(len(cleaned), 1) >= 0.5


def _option_usable(opt: str) -> bool:
    text = opt.strip()
    if not text or text[0] in ",=#^+":
        return False
    if len(text) > 18 and _letters(text) / len(text) < 0.2 and not re.fullmatch(r"[\d\s,./+\-]+", text):
        return False
    # Shredded equation fragments such as "mp nq =" are not usable choices.
    if "=" in text and not re.search(r"\d", text) and _letters(text) < 10:
        return False
    return True


def _mcq_answer_supported(item: dict[str, Any]) -> bool:
    """Chapter-wise keys are trusted only when the written answer matches the chosen option."""
    if item.get("source_paper") != "chapter_wise_pyq":
        return True
    options = item.get("options") or []
    idx = int(item.get("answer", -1))
    if idx < 0 or idx >= len(options):
        return False
    expl = norm_key(str(item.get("explanation", "")))
    opt = norm_key(str(options[idx]))
    if len(opt) < 1 or len(expl) < 1:
        return False
    return opt in expl or expl in opt


def _short_answer_usable(stem: str, model: str) -> bool:
    if re.search(r"following questions|answer the following", model, re.I) and not re.search(
        r"following", stem, re.I
    ):
        return False
    first = model.split()[0] if model.split() else ""
    if first.isalpha() and first.islower() and len(first) <= 4 and first not in {
        "a", "an", "the", "it", "in", "on", "as", "to", "if", "yes", "no", "by",
    }:
        return False
    return True


def _split_options(blob: str) -> list[str] | None:
    blob = _ANS_LINE.sub("", blob)
    parts = re.split(r"\(([a-dA-D])\)", blob)
    # parts[0] is preamble, then letter, text, letter, text...
    found: dict[str, str] = {}
    idx = 1
    while idx + 1 < len(parts):
        letter = parts[idx].lower()
        found[letter] = _clean(parts[idx + 1])
        idx += 2
    if not all(k in found for k in "abcd"):
        return None
    options = [found[k] for k in "abcd"]
    cleaned = []
    for opt in options:
        opt = re.split(r"\bAns\b", opt, maxsplit=1, flags=re.I)[0]
        opt = _clean(opt)
        if not opt or len(opt) > 140 or not re.search(r"[A-Za-z0-9]", opt):
            return None
        cleaned.append(opt)
    if len({norm_key(o) for o in cleaned}) < 3:
        return None
    return cleaned


def parse_objective_mcq_page(unit_id: int, text: str, *, source_label: str) -> list[dict[str, Any]]:
    """MCQs whose answer line says '(b) is correct'."""
    if unit_id < 1 or unit_id > 14:
        return []
    items: list[dict[str, Any]] = []
    lines = [_CTRL.sub("", ln).strip() for ln in text.splitlines()]
    current: dict[str, Any] | None = None

    def close(start_new: re.Match[str] | None) -> None:
        nonlocal current
        if current and current.get("options") and current.get("letter") is not None:
            stem = _clean(" ".join(current["stem"]))
            if (
                _readable(stem, min_letters=18)
                and not stem.lower().startswith("algorithm")
                and all(_option_usable(opt) for opt in current["options"])
            ):
                letter = int(current["letter"])
                expl = _clean(" ".join(line for line in current["expl"] if _expl_line_ok(line)))
                expl = _BOARD_TAG.sub("", expl)
                expl = _clean(expl)
                if not _readable(expl, min_letters=20):
                    expl = f"Option ({chr(65 + letter)}) is correct."
                items.append(
                    {
                        "id": _make_id(f"pyq_u{unit_id:02d}", "mcq", stem),
                        "source_paper": source_label,
                        "question": stem[:500],
                        "options": current["options"],
                        "answer": letter,
                        "explanation": expl[:700],
                    }
                )
        current = None
        if start_new:
            current = {
                "stem": [start_new.group(2)] if start_new.group(2) else [],
                "option_lines": [],
                "options": None,
                "expl": [],
                "letter": None,
                "in_ans": False,
            }

    for line in lines:
        if not line or re.fullmatch(r"(Page|Chap)\s*\d+", line, re.I):
            continue
        thus = _THUS.search(line)
        if current and thus and current.get("options"):
            current["letter"] = ord(thus.group(1).lower()) - ord("a")
            current["expl"].append(line)
            close(None)
            continue
        qmatch = _Q_DOT.match(line)
        if qmatch and (current is None or not current.get("option_lines")):
            close(qmatch)
            continue
        if current is None:
            continue
        if _ANS_LINE.match(line):
            if current["option_lines"] and not current["options"]:
                current["options"] = _split_options("\n".join(current["option_lines"]))
            current["in_ans"] = True
            rest = _ANS_LINE.match(line).group(1).strip()
            if rest:
                current["expl"].append(rest)
            continue
        if re.search(r"\([a-dA-D]\)", line) and not current["in_ans"]:
            current["option_lines"].append(line)
            continue
        if current["in_ans"]:
            current["expl"].append(line)
        elif not current["option_lines"]:
            current["stem"].append(line)
        else:
            current["option_lines"].append(line)
    close(None)
    return items


def parse_inline_written(text: str, *, source_label: str) -> dict[int, dict[str, list]]:
    """Most-repeated style: '1) question' then '[2 marks]' then the solution."""
    buckets = _empty_math()
    unit_id: int | None = None
    lines = text.splitlines()
    idx = 0
    while idx < len(lines):
        raw = lines[idx].strip()
        heading = cat.match_unit_id_for_heading(raw) if raw else None
        if heading:
            unit_id = heading
            idx += 1
            continue
        qmatch = _Q_PAREN.match(raw)
        if not qmatch or unit_id is None:
            idx += 1
            continue
        stem_parts = [qmatch.group(2)] if qmatch.group(2) else []
        marks = 3
        idx += 1
        while idx < len(lines):
            nxt = lines[idx].strip()
            if _Q_PAREN.match(nxt) or cat.match_unit_id_for_heading(nxt):
                break
            mark = _MARKS_BRACKET.search(nxt)
            if mark and _letters(" ".join(stem_parts)) >= 12:
                marks = int(mark.group(1))
                idx += 1
                break
            if nxt:
                stem_parts.append(nxt)
            idx += 1
        answer_parts: list[str] = []
        while idx < len(lines):
            nxt = lines[idx].strip()
            if _Q_PAREN.match(nxt) or (nxt and cat.match_unit_id_for_heading(nxt)):
                break
            if nxt and not re.fullmatch(r"Most Repeated Questions in Board Exams", nxt, re.I):
                answer_parts.append(nxt)
            idx += 1
        stem = _clean(" ".join(stem_parts))
        model = _clean(" ".join(answer_parts))
        if not _readable(stem, min_letters=20) or not _readable(model, min_letters=40):
            continue
        bucket = _written_bucket(marks)
        buckets[unit_id][bucket].append(
            {
                "id": _make_id(f"pyq_u{unit_id:02d}", "w", stem),
                "source_paper": source_label,
                "marks": marks,
                "question": stem[:800],
                "model_answer": model[:2000],
                "rubric": ["Correct method", "Accurate final result"],
            }
        )
    return buckets


_Q_WORD = re.compile(r"^Question\s+(\d+)\.?\s*(.*)$", re.I)
_SOLUTION = re.compile(r"^Solution\s*:?\s*(.*)$", re.I)


def parse_question_solution_blocks(text: str, *, source_label: str) -> dict[int, dict[str, list]]:
    """Chapter-wise compilations that print Question N / Solution."""
    buckets = _empty_math()
    unit_id: int | None = None
    marks = 3
    lines = text.splitlines()
    idx = 0
    while idx < len(lines):
        raw = lines[idx].strip()
        heading = cat.match_unit_id_for_heading(raw) if raw else None
        if heading:
            unit_id = heading
            idx += 1
            continue
        section = re.search(r"\[(\d+)\s*Marks?\]", raw, re.I)
        if section and "question" in raw.lower():
            marks = int(section.group(1))
            idx += 1
            continue
        qmatch = _Q_WORD.match(raw)
        if not qmatch or unit_id is None:
            idx += 1
            continue
        stem_parts = [qmatch.group(2)] if qmatch.group(2) else []
        idx += 1
        while idx < len(lines) and not _SOLUTION.match(lines[idx].strip()):
            nxt = lines[idx].strip()
            if _Q_WORD.match(nxt) or cat.match_unit_id_for_heading(nxt):
                break
            if nxt:
                stem_parts.append(nxt)
            idx += 1
        if idx >= len(lines) or not _SOLUTION.match(lines[idx].strip()):
            continue
        sol_first = _SOLUTION.match(lines[idx].strip())
        answer_parts = [sol_first.group(1)] if sol_first and sol_first.group(1) else []
        idx += 1
        while idx < len(lines):
            nxt = lines[idx].strip()
            if _Q_WORD.match(nxt) or (nxt and cat.match_unit_id_for_heading(nxt)):
                break
            if re.search(r"\[(\d+)\s*Marks?\]", nxt, re.I) and "question" in nxt.lower():
                break
            if nxt:
                answer_parts.append(nxt)
            idx += 1
        stem = _clean(" ".join(stem_parts))
        model = _clean(" ".join(answer_parts))
        if not _readable(stem, min_letters=20) or not _readable(model, min_letters=30):
            continue
        bucket = _written_bucket(marks)
        buckets[unit_id][bucket].append(
            {
                "id": _make_id(f"pyq_u{unit_id:02d}", "w", stem),
                "source_paper": source_label,
                "marks": marks,
                "question": stem[:800],
                "model_answer": model[:2000],
                "rubric": ["Correct method", "Accurate final result"],
            }
        )
    return buckets


def science_unit_for(chapter_number: int | None, title: str) -> tuple[str, int, str] | None:
    if title:
        for pattern, mapped in _SCIENCE_TITLE_RULES:
            if pattern.search(title):
                return mapped
    if chapter_number in _SCIENCE_BY_NUMBER:
        return _SCIENCE_BY_NUMBER[chapter_number]
    return None


def parse_science_short_answers(
    text: str,
    *,
    subject: str,
    unit_id: int,
    source_label: str,
    default_marks: int = 1,
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    marks = default_marks
    current: dict[str, Any] | None = None

    def flush() -> None:
        nonlocal current
        if not current:
            return
        stem = _clean(" ".join(current["stem"]))
        model = _clean(" ".join(current["answer"]))
        model = _BOARD_TAG.sub("", model)
        model = _clean(model)
        if (
            current["seen_ans"]
            and _readable(stem, min_letters=15)
            and _readable(model, min_letters=8)
            and _short_answer_usable(stem, model)
        ):
            items.append(
                {
                    "id": _make_id(f"pyq_{subject[:3]}_u{unit_id:02d}", "sa", stem),
                    "source_paper": source_label,
                    "question": stem[:700],
                    "model_answer": model[:1600],
                    "marks": int(current["marks"]),
                }
            )
        current = None

    for raw in text.splitlines():
        line = _CTRL.sub("", raw).strip()
        if not line:
            continue
        if re.fullmatch(r"(Page|Chap)\s*\d+.*", line, re.I) and len(line) < 80:
            continue
        if re.fullmatch(r"CHAPTER\s*\d+", line, re.I) or line.lower().startswith("www."):
            continue
        section = _SCI_MARKS.match(line)
        if section:
            flush()
            marks = _MARKS_WORD[section.group(1).lower()]
            continue
        if _CITATION.match(line):
            continue
        qmatch = _Q_DOT.match(line)
        ans = _ANS_LINE.match(line)
        if qmatch and (current is None or current["seen_ans"] or _letters(qmatch.group(2)) >= 8):
            if current and not current["seen_ans"] and _letters(qmatch.group(2)) < 8:
                current["stem"].append(line)
                continue
            flush()
            current = {
                "stem": [qmatch.group(2)] if qmatch.group(2) else [],
                "answer": [],
                "seen_ans": False,
                "marks": marks,
            }
            continue
        if ans and current and not current["seen_ans"]:
            current["seen_ans"] = True
            if ans.group(1):
                current["answer"].append(ans.group(1))
            continue
        if current is None:
            continue
        if current["seen_ans"]:
            current["answer"].append(line)
        else:
            current["stem"].append(line)
    flush()
    return items


def dedupe_items(items: list[dict[str, Any]], text_field: str) -> list[dict[str, Any]]:
    seen: set[str] = set()
    kept: list[dict[str, Any]] = []
    for item in items:
        key = norm_key(str(item.get(text_field, "")))
        if not key or key in seen:
            continue
        seen.add(key)
        kept.append(item)
    return kept
