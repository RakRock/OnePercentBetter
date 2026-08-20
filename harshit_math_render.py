"""Render Harshit Math question text with proper exponents, roots, and fractions."""

from __future__ import annotations

import html
import re


def _st():
    import streamlit as st

    return st

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

_VAR_POWER_RE = re.compile(
    r"(\d*)([a-zA-Z])\^\(([^)]+)\)|(\d*)([a-zA-Z])\^(-?\d+)"
)

# NCERT-style implicit exponents: u3 → u^3, 3x2 → 3x^2 (not plain numbers like 12).
_IMPLICIT_POLY_EXP_RE = re.compile(
    r"(?<![a-zA-Z])(\d*)([a-zA-Z])(\d+)(?![a-zA-Z0-9])"
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

_SUB_UNICODE_CHARS = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

# Coefficient subscripts: a_0, x_n (NCERT polynomial notation).
_COEFF_SUB_RE = re.compile(r"\b([a-zA-Z])_(\d+|n)\b")


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


def _normalize_implicit_poly_exponents(s: str) -> str:
    """u3 + v2 → u^3 + v^2; 3x2 → 3x^2 (NCERT polynomial notation)."""

    def repl(m: re.Match) -> str:
        coeff, var, exp = m.group(1) or "", m.group(2), m.group(3)
        return f"{coeff}{var}^{exp}"

    return _IMPLICIT_POLY_EXP_RE.sub(repl, s)


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
    s = _normalize_implicit_poly_exponents(s)
    return s


def contains_raw_latex(text: str) -> bool:
    return bool(_LATEX_SNIPPET_RE.search(str(text)))


_MATH_TOKEN_RE = re.compile(
    r"(?:\(\d+\^\d+\)\^\(-?\d+\)|\(\d+\^\d+\)\^-?\d+|"
    r"\(\s*√\d+\s*\)\^\d+|\d+\^\([^)]+\)|\d+\^\{?-?\d+\}?|"
    r"\d+/\d+|√\d+|"
    r"\d*[a-zA-Z]\^\([^)]+\)|\d*[a-zA-Z]\^-?\d+)"
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
    s = _normalize_implicit_poly_exponents(s)
    s = re.sub(r"\((\d+)\^(\d+)\)\^\((-?\d+)\)", r"(\1^{\2})^{\3}", s)
    s = re.sub(r"\((\d+)\^(\d+)\)\^(-?\d+)", r"(\1^{\2})^{\3}", s)
    s = re.sub(r"(\d+)/√(\d+)", r"\\frac{\1}{\\sqrt{\2}}", s)
    s = re.sub(r"\(\s*√(\d+)\s*\)\^(\d+)", r"(\\sqrt{\1})^{\2}", s)
    s = re.sub(r"√(\d+)", r"\\sqrt{\1}", s)
    s = re.sub(r"(\d+)\^\(([^)]+)\)", _latex_paren_exp, s)
    s = re.sub(r"(\d+)\^\{(-?\d+)\}", r"\1^{\2}", s)
    s = re.sub(r"(\d+)\^(-?\d+)", r"\1^{\2}", s)
    s = re.sub(r"(\d*)([a-zA-Z])\^\(([^)]+)\)", _latex_var_paren_exp, s)
    s = re.sub(r"(\d*)([a-zA-Z])\^(-?\d+)", r"\1\2^{\3}", s)

    def _frac(m: re.Match) -> str:
        sign = m.group(1) or ""
        return f"{sign}\\frac{{{m.group(2)}}}{{{m.group(3)}}}"

    s = re.sub(r"(-)?(\d+)/(\d+)", _frac, s)
    return s


def has_math_markup(text: str) -> bool:
    s = normalize_math_text(text)
    if re.search(r"\^|√|\d+/\d+", s):
        return True
    return bool(_IMPLICIT_POLY_EXP_RE.search(s))


def _prepare_for_display(text: str) -> str:
    return _normalize_compound_powers(_normalize_paren_powers(sanitize_grok_math_text(text)))


def _needs_latex_fraction(text: str) -> bool:
    """Stacked fractions over radicals — keep LaTeX for these."""
    s = normalize_math_text(text)
    if contains_raw_latex(s):
        return True
    return bool(re.search(r"\d+/√\d+", s))


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


def format_math_display(text: str) -> str:
    """Shared HTML formatter — exponents, implicit powers, roots (safe for Streamlit + email)."""
    return _format_powers_html(_prepare_for_display(text))


def format_math_plain(text: str) -> str:
    """Shared plain formatter — Unicode superscripts for buttons and plain-text email."""
    s = _format_powers_plain(_prepare_for_display(text))
    return s or "—"


def format_question_display(text: str) -> str:
    """Readable question line for word problems with HTML superscripts."""
    return format_math_display(text)


def _html_sup(exp: str) -> str:
    return f'<sup style="{_SUP_STYLE}">{html.escape(exp)}</sup>'


def _exp_display(exp: str, *, unicode_only: bool) -> str:
    glyph = _COMMON_FRAC_UNICODE.get(exp)
    if glyph:
        return glyph
    return _exp_unicode(exp)


def _collect_exponent_matches(s: str, *, unicode_only: bool) -> list[tuple[int, int, str]]:
    """Non-overlapping exponent spans → replacement text (HTML or Unicode)."""
    s = _normalize_implicit_poly_exponents(s)
    matches: list[tuple[int, int, str]] = []
    covered: list[tuple[int, int]] = []

    def _overlaps(start: int, end: int) -> bool:
        return any(cs < end and start < ce for cs, ce in covered)

    def _add(start: int, end: int, repl: str) -> None:
        if not _overlaps(start, end):
            matches.append((start, end, repl))
            covered.append((start, end))

    def _sup(exp: str) -> str:
        disp = _exp_display(exp, unicode_only=unicode_only)
        if unicode_only:
            return disp
        return _html_sup(disp)

    for m in _COMPOUND_POWER_RE.finditer(s):
        if m.group(1) is not None:
            base, inner, outer = m.group(1), m.group(2), m.group(3)
        else:
            base, inner, outer = m.group(4), m.group(5), m.group(6)
        inner_disp = _exp_display(inner, unicode_only=unicode_only)
        outer_disp = _exp_display(outer, unicode_only=unicode_only)
        if unicode_only:
            repl = f"({base}{inner_disp}){outer_disp}"
        else:
            repl = (
                f"({html.escape(base)}{_html_sup(inner_disp)})"
                f"{_html_sup(outer_disp)}"
            )
        _add(m.start(), m.end(), repl)

    for m in _POWER_RE.finditer(s):
        if m.group(1) is not None:
            base, exp = m.group(1), m.group(2)
        elif m.group(3) is not None:
            base, exp = m.group(3), m.group(4)
        else:
            base, exp = m.group(5), m.group(6)
        if unicode_only:
            repl = f"{base}{_sup(exp)}"
        else:
            repl = f"{html.escape(base)}{_sup(exp)}"
        _add(m.start(), m.end(), repl)

    for m in _VAR_POWER_RE.finditer(s):
        if m.group(3) is not None:
            coeff, var, exp = m.group(1) or "", m.group(2), m.group(3)
        else:
            coeff, var, exp = m.group(4) or "", m.group(5), m.group(6)
        if unicode_only:
            repl = f"{coeff}{var}{_sup(exp)}"
        else:
            repl = f"{html.escape(coeff)}{html.escape(var)}{_sup(exp)}"
        _add(m.start(), m.end(), repl)

    for m in _IMPLICIT_POLY_EXP_RE.finditer(s):
        coeff, var, exp = m.group(1) or "", m.group(2), m.group(3)
        if unicode_only:
            repl = f"{coeff}{var}{_exp_unicode(exp)}"
        else:
            repl = f"{html.escape(coeff)}{html.escape(var)}{_html_sup(_exp_unicode(exp))}"
        _add(m.start(), m.end(), repl)

    matches.sort(key=lambda t: t[0])
    return matches


def _apply_exponent_formatting(s: str, *, unicode_only: bool) -> str:
    s = _apply_subscript_formatting(s, unicode_only=True)
    matches = _collect_exponent_matches(s, unicode_only=unicode_only)
    out: list[str] = []
    last = 0
    for start, end, repl in matches:
        if start < last:
            continue
        chunk = s[last:start]
        out.append(chunk if unicode_only else html.escape(chunk))
        out.append(repl)
        last = end
    tail = s[last:]
    out.append(tail if unicode_only else html.escape(tail))
    return "".join(out)


def _format_powers_html(s: str) -> str:
    """Turn 5x^2, u3, (3^2)^(-1), and 5^-2 into HTML with superscripts."""
    return _apply_exponent_formatting(s, unicode_only=False)


def _format_powers_plain(s: str) -> str:
    """Compact exponent notation for button labels (Unicode only)."""
    return _apply_exponent_formatting(s, unicode_only=True)


def _latex_paren_exp(m: re.Match) -> str:
    inner = m.group(2)
    if re.fullmatch(r"-?\d+/\d+", inner):
        num, den = inner.split("/", 1)
        return f"{m.group(1)}^{{\\frac{{{num}}}{{{den}}}}}"
    return f"{m.group(1)}^{{{inner}}}"


def _latex_var_paren_exp(m: re.Match) -> str:
    inner = m.group(3)
    coeff, var = m.group(1), m.group(2)
    if re.fullmatch(r"-?\d+/\d+", inner):
        num, den = inner.split("/", 1)
        return f"{coeff}{var}^{{\\frac{{{num}}}{{{den}}}}}"
    return f"{coeff}{var}^{{{inner}}}"


def _render_html_question(display: str) -> None:
    _st().markdown(
        f"""
    <div class="gk-question-box">
        <div class="gk-question-text" style="margin-top:0.4rem;font-size:1.3rem;">{display}</div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_question(text: str) -> None:
    """Kid-friendly: short instruction line + large math (HTML superscripts or LaTeX fractions)."""
    st = _st()
    text = sanitize_grok_math_text(text)
    verb, body = _split_verb_prompt(text)

    if verb and _needs_latex_fraction(body):
        label = verb.rstrip(".")
        st.markdown(
            f'<p style="font-size:1.05rem;color:#4b5563;text-align:center;margin:0 0 0.35rem 0;">{html.escape(label)}</p>',
            unsafe_allow_html=True,
        )
        st.latex(r"\displaystyle " + _latex_body(body))
        return

    if verb and verb.lower().startswith("simplify using"):
        st.markdown(
            f'<p style="font-size:1.05rem;color:#4b5563;text-align:center;margin:0 0 0.35rem 0;">{html.escape(verb)}</p>',
            unsafe_allow_html=True,
        )
        _render_html_question(format_math_display(body))
        return

    if has_math_markup(text) or _is_wordy_math_question(text) or contains_raw_latex(text):
        _render_html_question(format_math_display(text))
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
    return format_math_plain(text)


def _exp_unicode(exp: str) -> str:
    digits = {"0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"}
    if exp.startswith("-") and exp[1:].isdigit():
        return "⁻" + "".join(digits.get(c, c) for c in exp[1:])
    if exp.isdigit():
        return "".join(digits.get(c, c) for c in exp)
    return f"^{exp}"


def _sub_unicode(sub: str) -> str:
    if sub == "n":
        return "ₙ"
    return sub.translate(_SUB_UNICODE_CHARS)


def _html_sub(text: str) -> str:
    return (
        f'<sub style="font-size:0.72em;vertical-align:sub;line-height:0;">'
        f"{html.escape(text)}</sub>"
    )


def _apply_subscript_formatting(s: str, *, unicode_only: bool) -> str:
    """Turn a_0, a_n into subscripts (before exponent pass treats a^0 as power)."""
    matches: list[tuple[int, int, str]] = []
    for m in _COEFF_SUB_RE.finditer(s):
        var, sub = m.group(1), m.group(2)
        glyph = _sub_unicode(sub)
        if unicode_only:
            repl = f"{var}{glyph}"
        else:
            repl = f"{html.escape(var)}{_html_sub(glyph)}"
        matches.append((m.start(), m.end(), repl))
    if not matches:
        return s
    out: list[str] = []
    last = 0
    for start, end, repl in matches:
        chunk = s[last:start]
        out.append(chunk if unicode_only else html.escape(chunk))
        out.append(repl)
        last = end
    tail = s[last:]
    out.append(tail if unicode_only else html.escape(tail))
    return "".join(out)
