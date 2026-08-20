"""Render Harshit Math question text with proper exponents, roots, and fractions."""

from __future__ import annotations

import html
import re

import streamlit as st

_VERBS = (
    "Evaluate",
    "Simplify",
    "Compute",
    "Multiply",
    "Expand",
    "Factor",
    "Classify",
    "Rationalize",
    "Look at the diagram.",
)


def normalize_math_text(text: str) -> str:
    return str(text).replace("−", "-").replace("–", "-").strip()


_LATEX_SNIPPET_RE = re.compile(
    r"\\(?:displaystyle|text|sqrt|frac)\b|\$[^$]+\$"
)

_PROSE_QUESTION_RE = re.compile(
    r"^(What|Which|How|Where|When|Why|According|On the|A |The |Between |Estimate |Start )",
    re.I,
)

_SUP_STYLE = "font-size:0.72em;vertical-align:super;line-height:0;"

_POWER_RE = re.compile(
    r"(\d+)\^\(([^)]+)\)|(\d+)\^\{(-?\d+)\}|(\d+)\^(-?\d+)"
)

_COMPOUND_POWER_RE = re.compile(
    r"\((\d+)\^(\d+)\)\^\((-?\d+)\)|\((\d+)\^(\d+)\)\^(-?\d+)"
)

_COMMON_FRAC_UNICODE = {
    "1/2": "½",
    "1/3": "⅓",
    "1/4": "¼",
    "1/5": "⅕",
    "2/3": "⅔",
    "3/4": "¾",
    "2/5": "⅖",
    "3/5": "⅗",
    "4/5": "⅘",
    "1/6": "⅙",
    "5/6": "⅚",
    "1/8": "⅛",
    "3/8": "⅜",
    "5/8": "⅝",
    "7/8": "⅞",
}

_EXP_UNICODE_CHARS = str.maketrans(
    "0123456789/-+",
    "⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁄⁺",
)


def _read_braced_content(s: str, open_brace_idx: int) -> tuple[str, int] | None:
    """Return (inner, index_after_closing_brace) when s[open_brace_idx] is '{'."""
    if open_brace_idx >= len(s) or s[open_brace_idx] != "{":
        return None
    depth = 1
    pos = open_brace_idx + 1
    start = pos
    while pos < len(s) and depth:
        ch = s[pos]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        pos += 1
    if depth != 0:
        return None
    return s[start : pos - 1], pos


def _strip_latex_command(s: str, command: str) -> str:
    """Replace \\command{...} with inner text (balanced braces)."""
    token = f"\\{command}{{"
    while token in s:
        idx = s.index(token)
        inner, end = _read_braced_content(s, idx + len(command) + 1) or ("", idx + len(token))
        if not inner and end == idx + len(token):
            break
        s = s[:idx] + inner + s[end:]
    return s


def _strip_latex_fracs(s: str) -> str:
    while r"\frac{" in s:
        idx = s.index(r"\frac{")
        num = _read_braced_content(s, idx + 5)
        if not num:
            break
        num_text, after_num = num
        if after_num >= len(s) or s[after_num] != "{":
            break
        den = _read_braced_content(s, after_num)
        if not den:
            break
        den_text, after_den = den
        s = s[:idx] + f"{num_text}/{den_text}" + s[after_den:]
    return s


def _normalize_compound_powers(s: str) -> str:
    """(3^2)^(-1) and (3^2)^-1 stay readable; fix broken LaTeX glue like '}3^3'."""
    s = re.sub(r"\((\d+)\^(\d+)\)\^\((-?\d+)\)", r"(\1^\2)^(\3)", s)
    s = re.sub(r"\((\d+)\^(\d+)\)\^(-?\d+)", r"(\1^\2)^(\3)", s)
    s = re.sub(r"\}\s*(\d+\^)", r" × \1", s)
    s = re.sub(r"([*])\s*", r" × ", s)
    s = re.sub(r"\s*×\s*×\s*", " × ", s)
    s = re.sub(r"[{}]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def _normalize_paren_powers(s: str) -> str:
    """(9)^{}\\frac{1}{2} or (9)^(1/2) → 9^(1/2)."""
    s = re.sub(
        r"\((\d+)\)\s*\^\{\s*\\frac\{([^}]+)\}\{([^}]+)\}\s*\}",
        r"\1^(\2/\3)",
        s,
    )
    s = re.sub(
        r"\((\d+)\)\s*\^\{\s*\}\s*(\d+/\d+)",
        r"\1^(\2)",
        s,
    )
    s = re.sub(r"\((\d+)\)\s*\^\(([^)]+)\)", r"\1^(\2)", s)
    s = re.sub(r"\((\d+)\)\^\{(\d+/\d+)(?=[\s?]|$)", r"\1^(\2)", s)
    s = re.sub(r"\((\d+)\)\^(\d+/\d+)(?=[\s?]|$)", r"\1^(\2)", s)
    return s


def sanitize_grok_math_text(text: str) -> str:
    """Convert Grok LaTeX-ish output to plain notation our renderer understands."""
    s = normalize_math_text(text)
    s = re.sub(r"\\displaystyle\s*", "", s)
    s = re.sub(r"\\times", "×", s)
    s = _strip_latex_command(s, "text")
    s = _strip_latex_fracs(s)
    s = re.sub(
        r"\((\d+)\)\s*\^\{\s*\}\s*(\d+/\d+)",
        r"(\1)^(\2)",
        s,
    )
    s = _strip_latex_command(s, "sqrt")
    s = re.sub(r"\\sqrt(\d+)", r"√\1", s)
    s = _strip_latex_fracs(s)
    s = re.sub(r"\^\{\s*\}", "^", s)
    s = re.sub(r"\^\{(-?\d+)\}", r"^\1", s)
    s = re.sub(r"\^\{([^}]+)\}", r"^(\1)", s)
    s = _normalize_paren_powers(s)
    s = _normalize_compound_powers(s)
    s = re.sub(r"\$([^$]*)\$", r"\1", s)
    s = re.sub(r"\\[a-zA-Z]+\s*", " ", s)
    s = _normalize_compound_powers(s)
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"^Simplify\s*\(", "Simplify: (", s, flags=re.I)
    s = re.sub(r"^Evaluate\s*\(", "Evaluate: (", s, flags=re.I)
    s = re.sub(r"^Compute\s*\(", "Compute: (", s, flags=re.I)
    return s


def contains_raw_latex(text: str) -> bool:
    return bool(_LATEX_SNIPPET_RE.search(str(text)))


_MATH_TOKEN_RE = re.compile(
    r"(\(\d+\^\d+\)\^\(-?\d+\)|\(\d+\^\d+\)\^-?\d+|"
    r"\(\s*√\d+\s*\)\^\d+|\d+\^\([^)]+\)|\d+\^\{?-?\d+\}?|\d+/\d+|√\d+|[xy]\^(-?\d+))"
)


def _latex_escape_text(text: str) -> str:
    escaped = (
        text.replace("\\", r"\\")
        .replace("{", r"\{")
        .replace("}", r"\}")
        .replace("_", r"\_")
        .replace("%", r"\%")
        .replace("&", r"\&")
    )
    return escaped


def _is_pure_math_expression(text: str) -> bool:
    """True when the string is mostly symbols (safe for math-mode LaTeX)."""
    s = normalize_math_text(text)
    s = _MATH_TOKEN_RE.sub("", s)
    s = re.sub(r"[=\?\.\…\s\d+\-*(),]", "", s)
    return not re.search(r"[a-zA-Z]", s)


def text_to_latex_mixed(text: str) -> str:
    """Preserve word spaces in prose; render roots/fractions/exponents as math."""
    s = normalize_math_text(text)
    parts = _MATH_TOKEN_RE.split(s)
    out: list[str] = []
    for part in parts:
        if not part:
            continue
        if _MATH_TOKEN_RE.fullmatch(part):
            out.append(text_to_latex(part))
        else:
            out.append(r"\text{" + _latex_escape_text(part) + "}")
    return "".join(out)


def text_to_latex(text: str) -> str:
    """Plain math notation → LaTeX (exponents, roots, fractions)."""
    if not _is_pure_math_expression(text):
        return text_to_latex_mixed(text)
    s = normalize_math_text(text)
    s = re.sub(r"\((\d+)\^(\d+)\)\^\((-?\d+)\)", r"(\1^{\2})^{\3}", s)
    s = re.sub(r"\((\d+)\^(\d+)\)\^(-?\d+)", r"(\1^{\2})^{\3}", s)
    s = re.sub(r"(\d+)/√(\d+)", r"\\frac{\1}{\\sqrt{\2}}", s)
    s = re.sub(r"\(\s*√(\d+)\s*\)\^(\d+)", r"(\\sqrt{\1})^{\2}", s)
    s = re.sub(r"√(\d+)", r"\\sqrt{\1}", s)
    s = re.sub(r"(\d+)\^\(([^)]+)\)", _latex_paren_exp, s)
    s = re.sub(r"(\d+)\^\{(-?\d+)\}", r"\1^{\2}", s)
    s = re.sub(r"(\d+)\^(-?\d+)", r"\1^{\2}", s)
    s = re.sub(r"([xy])\^(-?\d+)", r"\1^{\2}", s)

    def _frac(m: re.Match) -> str:
        sign = m.group(1) or ""
        return f"{sign}\\frac{{{m.group(2)}}}{{{m.group(3)}}}"

    s = re.sub(r"(-)?(\d+)/(\d+)", _frac, s)
    return s


def has_math_markup(text: str) -> bool:
    s = normalize_math_text(text)
    return bool(re.search(r"\^|√|\d+/\d+", s))


def _split_verb_prompt(text: str) -> tuple[str | None, str]:
    normalized = normalize_math_text(text)
    extended = re.match(r"^(Simplify using [^:]+):", normalized, re.I)
    if extended:
        return extended.group(1), normalized[extended.end() :].strip()
    for verb in _VERBS:
        prefix = f"{verb}:"
        if normalized.lower().startswith(prefix.lower()):
            return verb, normalized[len(prefix) :].strip()
        if normalized.lower().startswith(verb.lower()) and verb.endswith("."):
            rest = normalized[len(verb) :].strip()
            return verb, rest
    return None, normalized


def _is_wordy_math_question(text: str) -> bool:
    """Sentence-style prompts render more reliably as HTML than st.latex."""
    s = normalize_math_text(text)
    if _is_prose_question(s):
        return True
    if not has_math_markup(s):
        return False
    words = re.findall(r"[a-zA-Z]{2,}", s)
    return len(words) >= 2


def _latex_body(body: str) -> str:
    if _is_pure_math_expression(body):
        return text_to_latex(body)
    return text_to_latex_mixed(body)


def _is_prose_question(text: str) -> bool:
    s = normalize_math_text(text)
    return "?" in s and bool(_PROSE_QUESTION_RE.match(s))


def format_question_display(text: str) -> str:
    """Readable question line for word problems with HTML superscripts."""
    s = _normalize_compound_powers(_normalize_paren_powers(sanitize_grok_math_text(text)))
    return _format_powers_html(s)


def _html_sup(exp: str) -> str:
    return f'<sup style="{_SUP_STYLE}">{html.escape(exp)}</sup>'


def _format_powers_html(s: str) -> str:
    """Turn (3^2)^(-1), 8^(1/3), and 5^-2 into HTML with superscripts."""
    matches: list[tuple[int, int, str]] = []
    compound_spans: list[tuple[int, int]] = []
    for m in _COMPOUND_POWER_RE.finditer(s):
        if m.group(1) is not None:
            base, inner, outer = m.group(1), m.group(2), m.group(3)
        else:
            base, inner, outer = m.group(4), m.group(5), m.group(6)
        outer_disp = html.escape(_exp_unicode(outer))
        repl = f"({html.escape(base)}{_html_sup(inner)}){_html_sup(outer_disp)}"
        matches.append((m.start(), m.end(), repl))
        compound_spans.append((m.start(), m.end()))
    for m in _POWER_RE.finditer(s):
        if any(cs < m.end() and m.start() < ce for cs, ce in compound_spans):
            continue
        if m.group(1) is not None:
            base, exp = m.group(1), m.group(2)
            exp_html = html.escape(_COMMON_FRAC_UNICODE.get(exp, exp))
        elif m.group(3) is not None:
            base, exp = m.group(3), m.group(4)
            exp_html = html.escape(_exp_unicode(exp))
        else:
            base, exp = m.group(5), m.group(6)
            exp_html = html.escape(_exp_unicode(exp))
        matches.append((m.start(), m.end(), f"{html.escape(base)}{_html_sup(exp_html)}"))
    matches.sort(key=lambda t: t[0])
    out: list[str] = []
    last = 0
    for start, end, repl in matches:
        if start < last:
            continue
        out.append(html.escape(s[last:start]))
        out.append(repl)
        last = end
    out.append(html.escape(s[last:]))
    return "".join(out)


def _format_powers_plain(s: str) -> str:
    """Compact exponent notation for button labels (Unicode only)."""
    s = _format_compound_powers_plain(s)

    def _repl(m: re.Match) -> str:
        if m.group(1) is not None:
            base, exp = m.group(1), m.group(2)
            glyph = _COMMON_FRAC_UNICODE.get(exp)
            if glyph:
                return f"{base}^{glyph}"
            return base + exp.translate(_EXP_UNICODE_CHARS)
        if m.group(3) is not None:
            return m.group(3) + _exp_unicode(m.group(4))
        return m.group(5) + _exp_unicode(m.group(6))

    return _POWER_RE.sub(_repl, s)


def _format_compound_powers_plain(s: str) -> str:
    def repl(m: re.Match) -> str:
        if m.group(1) is not None:
            base, inner, outer = m.group(1), m.group(2), m.group(3)
        else:
            base, inner, outer = m.group(4), m.group(5), m.group(6)
        return f"({base}{_exp_unicode(inner)}){_exp_unicode(outer)}"

    return _COMPOUND_POWER_RE.sub(repl, s)


def _latex_paren_exp(m: re.Match) -> str:
    inner = m.group(2)
    if re.fullmatch(r"-?\d+/\d+", inner):
        num, den = inner.split("/", 1)
        return f"{m.group(1)}^{{\\frac{{{num}}}{{{den}}}}}"
    return f"{m.group(1)}^{{{inner}}}"


def render_question(text: str) -> None:
    """Kid-friendly: short instruction line + large math (LaTeX) when needed."""
    text = sanitize_grok_math_text(text)
    if _is_wordy_math_question(text) or contains_raw_latex(text):
        verb, body = _split_verb_prompt(text)
        if verb and verb.lower().startswith("simplify using"):
            st.markdown(
                f'<p style="font-size:1.05rem;color:#4b5563;text-align:center;margin:0 0 0.35rem 0;">{html.escape(verb)}</p>',
                unsafe_allow_html=True,
            )
            display = _format_powers_html(_normalize_compound_powers(body))
        else:
            display = format_question_display(text)
        st.markdown(
            f"""
        <div class="gk-question-box">
            <div class="gk-question-text" style="margin-top:0.4rem;font-size:1.3rem;">{display}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )
        return

    verb, body = _split_verb_prompt(text)
    if verb and has_math_markup(body):
        label = verb.rstrip(".")
        st.markdown(
            f'<p style="font-size:1.05rem;color:#4b5563;text-align:center;margin:0 0 0.35rem 0;">{label}</p>',
            unsafe_allow_html=True,
        )
        st.latex(r"\displaystyle " + _latex_body(body))
        return

    if has_math_markup(text):
        st.latex(r"\displaystyle " + text_to_latex_mixed(text))
        return

    st.markdown(
        f"""
    <div class="gk-question-box">
        <div class="gk-question-text" style="margin-top:0.4rem;font-size:1.3rem;">{html.escape(text)}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def format_option_label(text: str) -> str:
    """Button-safe label with Unicode superscripts and common fraction glyphs."""
    s = sanitize_grok_math_text(text)
    s = _normalize_paren_powers(s)
    s = _normalize_compound_powers(s)
    s = _format_powers_plain(s)
    return s or "—"


def _exp_unicode(exp: str) -> str:
    digits = {"0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"}
    if exp.startswith("-") and exp[1:].isdigit():
        return "⁻" + "".join(digits.get(c, c) for c in exp[1:])
    if exp.isdigit():
        return "".join(digits.get(c, c) for c in exp)
    return f"^{exp}"
