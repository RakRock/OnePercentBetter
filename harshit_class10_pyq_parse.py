"""Parse extracted PYQ plain text into board_paper_seeds-shaped items."""

from __future__ import annotations

import hashlib
import re
import uuid
from typing import Any

OPTION_LINE = re.compile(r"^\s*\(([A-Da-d])\)\s*(.+)$")
Q_START = re.compile(r"^\s*(\d+)\.\s*(.*)$")
MARKS_INLINE = re.compile(r"\((\d+)\s*Marks?\)", re.I)
CBSE_TAG = re.compile(r"\(CBSE[^)]+\)", re.I)
YEAR_TAG = re.compile(r"\(20\d{2}\)")
AR_ASSERTION = re.compile(r"Assertion\s*\(A\)\s*[:：]?\s*(.+)", re.I | re.DOTALL)
AR_REASON = re.compile(r"Reason\s*\(R\)\s*[:：]?\s*(.+)", re.I | re.DOTALL)
ANS_MCQ = re.compile(r"^\s*(\d+)\.\s*\(([A-Da-d])\)\s*:?\s*(.*)$")
ANS_WRITTEN = re.compile(r"^\s*(\d+)\.\s+(.+)$")
INLINE_ANS = re.compile(r"^\s*Answer\.\s*\(([A-Da-d])\)\s*(.*)$", re.I)

WRITTEN_VERBS = re.compile(
    r"\b(prove|show|find|calculate|solve|determine|verify|evaluate|draw|construct|"
    r"factor|factorise|factorize|simplify|write|obtain|check|compute|divide|"
    r"express|form|graph|shade|state|explain|describe)\b",
    re.I,
)
SOLUTION_FRAGMENT = re.compile(
    r"^\s*(hence|therefore|thus|so)\b.*\b(wrong|contradiction|assumption)\b",
    re.I,
)

SKIP_LINE_PREFIXES = (
    "previous years",
    "directions:",
    "two statements are given",
    "select the correct",
)

GARBAGE_STEM_PATTERNS = (
    re.compile(r"^\s*or\s*$", re.I),
    re.compile(r"^\s*\([ivx]+\)\s*$", re.I),
    re.compile(r"^\s*answer\.?", re.I),
    re.compile(r"^\s*hence,?\s*$", re.I),
    re.compile(r"^\s*therefore,?\s*$", re.I),
    re.compile(r"^\s*solution\s*:?\s*$", re.I),
)


def _norm_key(text: str) -> str:
    t = re.sub(r"\s+", " ", text.strip().lower())
    t = re.sub(r"[^\w\s]", "", t)
    return t[:240]


def _make_id(unit_id: int, kind: str, text: str) -> str:
    digest = hashlib.sha1(_norm_key(text).encode()).hexdigest()[:10]
    return f"pyq_u{unit_id:02d}_{kind}_{digest}"


def _marks_from_text(text: str) -> int | None:
    m = MARKS_INLINE.search(text)
    if m:
        return int(m.group(1))
    if re.search(r"\(1\s*Mark\)", text, re.I):
        return 1
    return None


def _clean_stem(text: str) -> str:
    text = CBSE_TAG.sub("", text)
    text = YEAR_TAG.sub("", text)
    text = MARKS_INLINE.sub("", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _written_bucket(marks: int) -> str:
    if marks <= 2:
        return "vsa"
    if marks <= 3:
        return "sa"
    return "la"


def _is_answer_section(line: str) -> bool:
    """Standalone answer-key headings only (not inline 'Answer. (b) ...' lines)."""
    s = line.strip().lower()
    if not s:
        return False
    return s in ("answer", "answers", "answer:")


def _letter_index(letter: str) -> int:
    return max(0, min(3, ord(letter.upper()) - ord("A")))


def _parse_ar_answer_index(text: str) -> int | None:
    text = text.strip()
    m = re.match(r"^\(?([A-Da-d])\)?", text)
    if m:
        return _letter_index(m.group(1))
    low = text.lower()
    if "both" in low and "assertion" in low and "reason" in low:
        if "not" in low and "explanation" in low:
            return 1
        if "correct explanation" in low or "explains" in low:
            return 0
    if "assertion" in low and "true" in low and "reason" in low and "false" in low:
        return 2
    if "assertion" in low and "false" in low:
        return 3
    return None


def _starts_new_question(line: str) -> bool:
    """Detect a new exam question while scanning an answer-key region."""
    m = Q_START.match(line)
    if not m:
        return False
    if ANS_MCQ.match(line):
        return False
    rest = m.group(2).strip()
    if not rest or len(rest) < 10:
        return False
    if re.match(r"^\([A-Da-d]\)\s*", rest):
        return False
    low = rest.lower()
    if low.startswith(("assume", "let ", "hence", "therefore", "thus", "solution", "we know")):
        return False
    if "assertion (a)" in low:
        return True
    if MARKS_INLINE.search(rest) or MARKS_INLINE.search(line):
        return True
    if "?" in rest:
        return True
    if rest.endswith(":") or " : " in rest:
        return True
    if WRITTEN_VERBS.search(rest):
        return True
    return False


def _split_question_answer_regions(block: str) -> list[tuple[str, list[str]]]:
    """Split into alternating ('questions'|'answers', lines) regions."""
    regions: list[tuple[str, list[str]]] = []
    mode = "questions"
    buf: list[str] = []

    def flush() -> None:
        nonlocal buf
        if buf:
            regions.append((mode, buf))
        buf = []

    for line in block.splitlines():
        stripped = line.strip()
        if _is_answer_section(line):
            flush()
            mode = "answers"
            continue
        if mode == "answers" and _starts_new_question(line):
            flush()
            mode = "questions"
            buf.append(line)
            continue
        low = stripped.lower()
        if low.startswith("previous years"):
            flush()
            mode = "questions"
            continue
        buf.append(line)
    flush()
    return regions


def _parse_answer_region(lines: list[str]) -> dict[str, dict[str, Any]]:
    """Map question number -> parsed answer payload."""
    answers: dict[str, dict[str, Any]] = {}
    current_num: str | None = None
    buf: list[str] = []

    def store(num: str, kind: str, **extra: Any) -> None:
        text = " ".join(buf).strip()
        text = re.sub(r"\s+", " ", text)
        payload: dict[str, Any] = {"kind": kind, "text": text, **extra}
        answers[num] = payload
        buf.clear()

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current_num and buf:
                buf.append("")
            continue

        inline = INLINE_ANS.match(line)
        if inline:
            letter = inline.group(1)
            rest = inline.group(2).strip()
            num = current_num or "_inline"
            answers[num] = {
                "kind": "mcq",
                "letter": _letter_index(letter),
                "text": rest,
            }
            continue

        mcq = ANS_MCQ.match(line)
        if mcq:
            if current_num and buf and current_num not in answers:
                store(current_num, "written")
            current_num = mcq.group(1)
            letter = mcq.group(2)
            rest = mcq.group(3).strip()
            answers[current_num] = {
                "kind": "mcq",
                "letter": _letter_index(letter),
                "text": rest,
            }
            buf.clear()
            continue

        wr = ANS_WRITTEN.match(line)
        if wr:
            if current_num and buf and current_num not in answers:
                store(current_num, "written")
            current_num = wr.group(1)
            first = wr.group(2).strip()
            buf = [first] if first else []
            continue

        if Q_START.match(line) and line.strip().endswith(".") and not OPTION_LINE.match(line):
            m = Q_START.match(line)
            if m and not m.group(2).strip():
                if current_num and buf and current_num not in answers:
                    store(current_num, "written")
                current_num = m.group(1)
                buf = []
                continue

        if current_num:
            buf.append(stripped)

    if current_num and buf and current_num not in answers:
        store(current_num, "written")

    return answers


def _pair_regions(regions: list[tuple[str, list[str]]]) -> list[tuple[list[str], dict[str, dict[str, Any]]]]:
    pairs: list[tuple[list[str], dict[str, dict[str, Any]]]] = []
    i = 0
    while i < len(regions):
        kind, lines = regions[i]
        if kind == "questions":
            amap: dict[str, dict[str, Any]] = {}
            j = i + 1
            while j < len(regions) and regions[j][0] == "answers":
                amap.update(_parse_answer_region(regions[j][1]))
                j += 1
            pairs.append((lines, amap))
            i = j
        else:
            i += 1
    return pairs


def _is_garbage_stem(stem: str) -> bool:
    s = stem.strip()
    if len(s) < 12:
        return True
    for pat in GARBAGE_STEM_PATTERNS:
        if pat.match(s):
            return True
    low = s.lower()
    if low.startswith("multiplying eqn") or low.startswith("adding eqn"):
        return True
    if SOLUTION_FRAGMENT.match(s):
        return True
    if s.count("=") >= 3 and "?" not in s and not WRITTEN_VERBS.search(s):
        return True
    return False


def _is_valid_written_stem(stem: str, marks: int) -> bool:
    if _is_garbage_stem(stem):
        return False
    s = stem.strip()
    if len(s) < 20:
        return False
    if "?" in s or WRITTEN_VERBS.search(s):
        return True
    if marks >= 5 and len(s) >= 45:
        return True
    if marks >= 3 and len(s) >= 55:
        return True
    return False


def _is_valid_model_answer(text: str) -> bool:
    t = re.sub(r"\s+", " ", text.strip())
    if len(t) < 30:
        return False
    if t.startswith("(Work the solution"):
        return False
    alpha = sum(1 for c in t if c.isalpha())
    return alpha >= 8


def _is_valid_mcq(stem: str, options: list[str]) -> bool:
    if _is_garbage_stem(stem):
        return False
    if len(stem) < 15:
        return False
    cleaned = [_clean_stem(o) for o in options if o.strip()]
    if len(cleaned) < 3:
        return False
    if len(set(_norm_key(o) for o in cleaned[:4])) < 3:
        return False
    return True


def _apply_answer_to_mcq(item: dict[str, Any], ans: dict[str, Any] | None) -> None:
    meta = item.setdefault("pyq_meta", {})
    if not ans or ans.get("kind") != "mcq":
        meta["needs_answer_key"] = True
        return
    letter = int(ans.get("letter", 0))
    item["answer"] = letter
    expl = ans.get("text", "").strip()
    if expl:
        item["explanation"] = expl
    meta.pop("needs_answer_key", None)
    meta["answer_paired"] = True


def _apply_answer_to_ar(item: dict[str, Any], ans: dict[str, Any] | None) -> None:
    meta = item.setdefault("pyq_meta", {})
    if not ans:
        return
    text = ans.get("text", "")
    if ans.get("kind") == "mcq":
        text = f"({chr(65 + int(ans['letter']))}) {text}"
    idx = _parse_ar_answer_index(text)
    if idx is not None:
        item["answer"] = idx
        meta["answer_paired"] = True
        if text:
            item["explanation"] = text[:500]


def _apply_answer_to_written(item: dict[str, Any], ans: dict[str, Any] | None) -> bool:
    """Return False if item should be dropped (no usable model answer)."""
    if ans and ans.get("kind") == "written":
        model = ans.get("text", "").strip()
        if _is_valid_model_answer(model):
            item["model_answer"] = model[:4000]
            item.setdefault("pyq_meta", {})["answer_paired"] = True
            return True
    if ans and ans.get("kind") == "mcq" and ans.get("text"):
        model = ans.get("text", "").strip()
        if _is_valid_model_answer(model):
            item["model_answer"] = model[:4000]
            item.setdefault("pyq_meta", {})["answer_paired"] = True
            return True
    return False


def _parse_question_region(
    unit_id: int,
    lines: list[str],
    answer_map: dict[str, dict[str, Any]],
    *,
    source_label: str,
    seen: set[str],
) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = {
        "mcq": [],
        "assertion_reason": [],
        "vsa": [],
        "sa": [],
        "la": [],
    }

    i = 0
    while i < len(lines):
        line = lines[i]
        low = line.strip().lower()
        if any(low.startswith(p) for p in SKIP_LINE_PREFIXES):
            i += 1
            continue
        if INLINE_ANS.match(line):
            i += 1
            continue

        m = Q_START.match(line)
        if not m:
            i += 1
            continue

        qnum = m.group(1)
        stem_parts = [m.group(2).strip()] if m.group(2).strip() else []
        options: list[str] = []
        j = i + 1
        while j < len(lines):
            nxt = lines[j]
            if _is_answer_section(nxt):
                break
            if INLINE_ANS.match(nxt):
                break
            om = OPTION_LINE.match(nxt)
            if om:
                options.append(om.group(2).strip())
                j += 1
                continue
            if Q_START.match(nxt) and not options:
                stem_parts.append(nxt.strip())
                j += 1
                continue
            if Q_START.match(nxt) and options:
                break
            if not nxt.strip():
                j += 1
                continue
            if options:
                break
            if Q_START.match(nxt) and not options:
                break
            if nxt.strip() and not OPTION_LINE.match(nxt):
                if MARKS_INLINE.search(nxt) or CBSE_TAG.search(nxt) or YEAR_TAG.search(nxt):
                    stem_parts.append(nxt.strip())
                    j += 1
                    continue
                if not AR_ASSERTION.search(" ".join(stem_parts)):
                    stem_parts.append(nxt.strip())
                    j += 1
                    continue
            break

        raw_stem = " ".join(stem_parts)
        marks = _marks_from_text(raw_stem) or _marks_from_text(" ".join(lines[i:j]))
        stem = _clean_stem(raw_stem)
        if _is_garbage_stem(stem):
            i = j
            continue

        key = _norm_key(stem)
        if key in seen:
            i = j
            continue
        seen.add(key)

        ans = answer_map.get(qnum)

        if "assertion (a)" in stem.lower() and "reason (r)" in stem.lower():
            a_m = AR_ASSERTION.search(stem)
            r_m = AR_REASON.search(stem)
            if a_m and r_m:
                assertion = _clean_stem(a_m.group(1))
                reason = _clean_stem(r_m.group(1))
                if len(assertion) < 12 or len(reason) < 12:
                    i = j
                    continue
                item = {
                    "id": _make_id(unit_id, "ar", stem),
                    "source_paper": source_label,
                    "assertion": assertion,
                    "reason": reason,
                    "answer": 0,
                    "explanation": "",
                    "pyq_meta": {"qnum": qnum, "parse": "ar"},
                }
                _apply_answer_to_ar(item, ans)
                out["assertion_reason"].append(item)
        elif len(options) >= 3:
            opts = options[:4]
            while len(opts) < 4:
                opts.append(f"(option {len(opts) + 1})")
            if not _is_valid_mcq(stem, opts):
                i = j
                continue
            item = {
                "id": _make_id(unit_id, "mcq", stem),
                "source_paper": source_label,
                "question": stem,
                "options": opts,
                "answer": 0,
                "explanation": "",
                "pyq_meta": {"qnum": qnum, "parse": "mcq"},
            }
            _apply_answer_to_mcq(item, ans)
            out["mcq"].append(item)
        else:
            mks = marks or 3
            if not _is_valid_written_stem(stem, mks):
                i = j
                continue
            bucket = _written_bucket(mks)
            item = {
                "id": _make_id(unit_id, "w", stem),
                "source_paper": source_label,
                "marks": mks,
                "question": stem,
                "model_answer": "",
                "rubric": ["Correct method", "Accurate final result"],
                "pyq_meta": {"qnum": qnum, "parse": "written", "marks": mks},
            }
            if not _apply_answer_to_written(item, ans):
                i = j
                continue
            out[bucket].append(item)

        i = j

    return out


def parse_chapter_block(
    unit_id: int,
    block: str,
    *,
    source_label: str,
) -> dict[str, list[dict[str, Any]]]:
    """Parse one chapter text block with answer-key pairing and quality filters."""
    combined: dict[str, list[dict[str, Any]]] = {
        "mcq": [],
        "assertion_reason": [],
        "vsa": [],
        "sa": [],
        "la": [],
    }
    seen: set[str] = set()
    regions = _split_question_answer_regions(block)
    for q_lines, amap in _pair_regions(regions):
        part = _parse_question_region(
            unit_id,
            q_lines,
            amap,
            source_label=source_label,
            seen=seen,
        )
        for bucket in combined:
            combined[bucket].extend(part.get(bucket, []))
    return combined


def strip_pyq_items(seed: dict[str, Any]) -> int:
    """Remove prior pyq_u* imports from a unit seed file."""
    removed = 0
    for bucket in ("mcq", "assertion_reason", "vsa", "sa", "la"):
        items = seed.get(bucket, [])
        kept = [q for q in items if not str(q.get("id", "")).startswith("pyq_u")]
        removed += len(items) - len(kept)
        seed[bucket] = kept
    meta = seed.setdefault("meta", {})
    sources = meta.get("sources", [])
    meta["sources"] = [s for s in sources if not str(s).startswith("PYQ:")]
    return removed


def _upgrade_existing_item(base: dict[str, list[dict[str, Any]]], bucket: str, text_key: str, item: dict[str, Any]) -> bool:
    for ex in base.get(bucket, []):
        ex_key = _norm_key(
            ex.get("question") or ex.get("assertion", "") or ex.get("reason", "")
        )
        if ex_key != text_key:
            continue
        if bucket == "mcq":
            if int(item.get("answer", 0)) != 0 and int(ex.get("answer", 0)) == 0:
                ex["answer"] = int(item["answer"])
            if item.get("explanation") and not ex.get("explanation"):
                ex["explanation"] = item["explanation"]
            return True
        if bucket == "assertion_reason":
            if int(item.get("answer", 0)) != 0 and int(ex.get("answer", 0)) == 0:
                ex["answer"] = int(item["answer"])
            if item.get("explanation") and not ex.get("explanation"):
                ex["explanation"] = item["explanation"]
            return True
        if bucket in ("vsa", "sa", "la"):
            model = str(item.get("model_answer", ""))
            if _is_valid_model_answer(model) and not _is_valid_model_answer(str(ex.get("model_answer", ""))):
                ex["model_answer"] = model
                return True
        return True
    return False


def merge_seed_buckets(
    base: dict[str, list[dict[str, Any]]],
    extra: dict[str, list[dict[str, Any]]],
    *,
    existing_ids: set[str],
    existing_keys: set[str],
) -> int:
    added = 0
    for bucket in ("mcq", "assertion_reason", "vsa", "sa", "la"):
        for item in extra.get(bucket, []):
            if bucket == "mcq" and item.get("pyq_meta", {}).get("needs_answer_key"):
                continue
            if bucket in ("vsa", "sa", "la"):
                if not _is_valid_model_answer(str(item.get("model_answer", ""))):
                    continue
            iid = str(item.get("id") or "")
            if not iid:
                item["id"] = f"pyq_{uuid.uuid4().hex[:8]}"
                iid = item["id"]
            text_key = _norm_key(
                item.get("question") or item.get("assertion", "") or item.get("reason", "")
            )
            if text_key in existing_keys:
                _upgrade_existing_item(base, bucket, text_key, item)
                continue
            if iid in existing_ids:
                continue
            item.pop("pyq_meta", None)
            base.setdefault(bucket, []).append(item)
            existing_ids.add(iid)
            existing_keys.add(text_key)
            added += 1
    return added
