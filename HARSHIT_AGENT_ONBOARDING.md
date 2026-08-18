# Harshit Sai — Agent Onboarding Guide

Use this document to onboard an AI agent to **Harshit Sai's math intervention app** inside **1% Better Every Day**. Architecture mirrors Arjun's math modules (SQLite, Google Sheets, email, Streamlit routing) with a **low-sensory, anti-gamified** pedagogy.

---

## Copy-paste system prompt

```
You are an assistant for Harshit Sai, a 10th-grade student stabilizing NCERT Class 9 mathematics before advancing to Class 10.

CONTEXT
- App: Streamlit "1% Better Every Day" → select "Harshit Sai" → Number Sense
- Curriculum: 60-day plan; ONLY Phase 1 (Days 1–10, Number Sense) is implemented
- Source: NCERT Class 9 Mathematics, Chapter 1 (Number Systems) + prerequisites
- UI: Anti-gamified — one problem per screen, muted palette, no timers, soft amber errors (never red)
- Flow: Visual manipulative FIRST → intermediate steps → final answer (never single-shot input)
- State machine: harshit_math_state.py + HarshitMath/phase1/error_state_machines.json

KEY FILES
- harshit_math_ui.py — Streamlit UI
- harshit_math_content.py — loads logic_schema.json, state machines, component specs
- harshit_math_state.py — ProblemStateMachine error-catching engine
- harshit_math_components.py — number line + fraction grid visuals
- HarshitMath/phase1/logic_schema.json — 10-day breakdown
- HarshitMath/phase1/error_state_machines.json — Day 2 & Day 9 full graphs
- HarshitMath/phase1/component_specs.json — CSS variables + component props

DATA LAYER (same as Arjun)
- database.py — harshit_math_progress, harshit_math_day_status, activity_scores
- google_sheets_sync.py — session_kind "harshit_phase1", unit offset 200
- edgenuity_practice_email.py — practice completion emails

CONSTRAINTS
- No countdown timers, streaks, or celebratory gamification
- Errors → soft amber micro-feedback tied to specific mistake patterns
- Scale Phase 1 pattern to Days 11–60 (Algebra, Geometry, Mensuration) without changing architecture
```

---

## Student profile

| Field | Value |
|-------|--------|
| Name | Harshit Sai |
| Avatar | 📐 |
| Grade | 10th (intervention targets Class 9 gaps first) |
| Primary app | Number Sense — Phase 1, Days 1–10 |

---

## Phase 1 — 10-Day Logic Schema

Full machine-readable schema: `HarshitMath/phase1/logic_schema.json`

| Day | Title | Manipulative | NCERT anchor |
|-----|-------|--------------|--------------|
| 1 | Integers on the Number Line | Number line | §1.1 foundation |
| 2 | Adding/Subtracting Integers | Number line | −5 − (−3) prerequisite |
| 3 | Rational Numbers on Number Line | Number line | Ex 1.1 / Example 1 (5/2) |
| 4 | Adding Fractions — LCD | Fraction grid | §1.1 rational addition |
| 5 | Subtracting Fractions | Fraction grid | §1.1 rational subtraction |
| 6 | Multiplying Fractions — Area Model | Fraction grid | §1.1 multiplication |
| 7 | Dividing Fractions | Fraction grid | §1.1 division |
| 8 | Decimals → p/q | Number line | §1.1 decimal rationals |
| 9 | Locating √2 | Number line | **§1.2 Example 5** |
| 10 | Rational vs Irrational | Number line | Ex 1.2 Q1 style |

Each day defines: `core_concept`, `manipulative`, `ncert_problem` with step-by-step progression.

---

## Error-Catching State Machines

Full JSON: `HarshitMath/phase1/error_state_machines.json`

### Day 2 — `d2_p1` (−5 − (−3))

```
visual_start → visual_rewrite → step_rewrite → step_move → final_answer → complete
```

Key error traps:
- **−8** → `classic_minus_trap`: "subtracting a negative is adding a positive"
- Wrong side of zero → `visual_wrong_side`
- Dropped negative in rewrite → `dropped_negative`

### Day 9 — `d9_p1 (Locate √2)

```
visual_bracket → step_square_check → visual_plot → step_classify → final_explain → complete
```

Key error traps:
- Interval [0,1] → `interval_too_low`
- Plot at 2 → `plot_at_two` (2² = 4)
- Says "rational" → `said_rational`

---

## Frontend Component Specs

Full spec: `HarshitMath/phase1/component_specs.json`

### CSS palette (muted, high-contrast)

| Variable | Value | Use |
|----------|-------|-----|
| `--hm-bg-page` | `#F7F8FA` | Page background |
| `--hm-text-equation` | `#0F172A` | Equations |
| `--hm-feedback-amber` | `#F5DEB3` | Error hints (not red) |
| `--hm-number-line-marker` | `#1E3A5F` | Draggable marker |

### InteractiveNumberLine

Props: `min`, `max`, `mode` (`single_marker` | `dual_marker` | `interval_select`), `target`, `tolerance`, `onVisualComplete`

### FractionBlockGrid

Props: `rows`, `cols`, `phase` (`shade_rows` | `shade_cols` | `overlay` | `count_overlap`), `expectedRowShade`, `expectedColShade`

---

## Class 9 PreReq buckets (6)

Catalog: `HarshitMath/prereqs/catalog.json` · Loader: `harshit_math_prereqs.py`

| # | PreReq | Class 9 Chapters | Grade 10 bridge |
|---|--------|------------------|-----------------|
| 1 | Number Systems & Foundations | Ch 1 | Real Numbers, FTA |
| 2 | Algebraic Operations & Equations | Ch 2, 4 | Polynomials, linear pairs, quadratics |
| 3 | Coordinate Graphing | Ch 3 | Distance & section formula |
| 4 | Core Euclidean Geometry | Ch 5, 6, 7, 8, 10 | Similarity, tangents, trig intro |
| 5 | Mensuration | Ch 12, 13 | Circle areas, 3D volumes |
| 6 | Data & Probability | Ch 14, 15 | Grouped statistics, probability |

Chapter files searched in:
- `HarshitMath/class9_chapters/`
- `~/Downloads/Harshit-Math/Class9-Chapter` (or `HARSHIT_CLASS9_CHAPTERS` env var)

PreReq 1 links to **Phase 1** Number Sense bootcamp for Chapter 1 interactive practice.

---

## File map

```
HarshitMath/prereqs/catalog.json   # 6 PreReq bucket definitions
HarshitMath/class9_chapters/       # Drop NCERT chapter notes/PDFs here
HarshitMath/phase1/
  logic_schema.json
  error_state_machines.json
  component_specs.json
harshit_math_prereqs.py
harshit_math_content.py
harshit_math_state.py
harshit_math_components.py
harshit_math_ui.py
database.py
app.py
```

---

## Scaling to Days 11–60

1. Add `HarshitMath/phase2/logic_schema.json` (Algebra), phase3 (Geometry), etc.
2. Add state machines per problem in `error_state_machines.json`
3. Extend `harshit_math_content.PHASE_ID` routing
4. Reuse same UI shell — one problem per screen, visual-first, state machine backend

---

*Phase 1 scaffold live in app; Days 2 and 9 have full state-machine implementations. Days 1, 3–8, 10 use schema + UI shell — extend state machines using the same JSON pattern.*
