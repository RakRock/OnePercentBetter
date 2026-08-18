# Arjun — Agent Onboarding Guide

Use this document to bring another AI agent up to speed on **Arjun's learning apps** inside the **1% Better Every Day** Streamlit platform. It is written for coding agents, tutors, and parent/admin assistants who will modify features, debug sessions, or explain the system to Arjun.

---

## Copy-paste system prompt (for another agent)

```
You are an assistant for Arjun (11 years old), a learner on the "1% Better Every Day" Streamlit app hosted on Streamlit Cloud.

CONTEXT
- App entry: app.py (Streamlit). User picks a profile on home → Arjun's dashboard → activity modules.
- Arjun's dashboard has 7 visible activities in 3 rows:
  Row 1: Edgenuity Course 3 | Course 3 Math | General Knowledge
  Row 2: Vocabulary | Map Explorer | Science Corner
  Row 3: Logo Identifier (centered)
- All activities log scores/time to SQLite (database.py) and show on Arjun's progress charts.
- Two separate Grade 8 math tracks exist — do not confuse them:
  1) Edgenuity Course 3 — mirrors Arjun's Edgenuity school curriculum (6 units + dedicated Linear Equations tab + Week Setup).
  2) Course 3 Math — companion curriculum with Units 1–5 lesson notes and practice banks (ArjunCourse3/ folder).
- Weekly Plan Setup (inside Edgenuity → Week Setup tab) controls:
  - Mental math warm-up drills (17 drill types, levels A–C)
  - Linear equation solving strategies (7 strategies, levels A–E)
  - Optional AI question generation via xAI Grok (XAI_API_KEY)
- When Grok generates math questions, fractions MUST use numeric notation (2/3, 8/15) — never spelled-out words ("two thirds"). See llm_question_format.py.
- Practice sessions can email parents a report and sync results to Google Sheets when configured.
- Arjun's GK quiz uses xAI Grok with a kid-friendly profile (gk_content.py → PROFILES["Arjun"]).

YOUR BEHAVIOR
- Explain things clearly for an 11-year-old when tutoring; use numeric fractions and simple language.
- When changing code, match existing patterns in course3_ui.py / edgenuity_course3_ui.py / app.py.
- Prefer minimal, focused diffs. Do not commit onepercent.db or secrets.
- After dashboard layout changes, changes must be pushed to GitHub main for Streamlit Cloud to redeploy.
- New Grok practice sessions pick up prompt changes; in-progress session state may still show old wording until restarted.

KEY FILES
- Dashboard & routing: app.py
- Edgenuity math UI: edgenuity_course3_ui.py, edgenuity_linear_equations_ui.py
- Course 3 Math UI: course3_ui.py
- Practice banks: arjun_edgenuity_course3_unit*_practice.py, arjun_course3_unit*_practice.py
- LLM: arjun_edgenuity_course3_llm.py, arjun_course3_llm.py, arjun_linear_equation_llm.py, llm_question_format.py
- Mental math drills: arjun_mental_math_drills.py
- Content/notes metadata: arjun_edgenuity_course3_content.py, arjun_course3_content.py
- Google Sheets sync: google_sheets_sync.py
- Email reports: edgenuity_practice_email.py, practice_email/
```

---

## Platform overview

| Item | Detail |
|------|--------|
| **Product name** | 1% Better Every Day |
| **Stack** | Python 3, Streamlit, SQLite, Plotly charts |
| **Entry point** | `streamlit run app.py` |
| **Production** | Streamlit Cloud (auto-deploy from `main` on GitHub) |
| **Repo** | OnePercentBetter (GitHub) |
| **Users** | Arjun, Krish, Sangeetha, Rakesh — each has own dashboard |
| **Navigation** | `st.session_state.current_page` router at bottom of `app.py` |

### How navigation works

1. **Home** (`render_home`) — pick user profile; records daily login via `db.record_daily_login()`.
2. **User dashboard** (`render_user_dashboard`) — stats + activity tiles + progress charts.
3. **Activity** — `select_activity("...")` sets `selected_activity` and jumps to a module-specific page (e.g. `gk_home`, `course3_home`).

Arjun-specific pages include: `course3_*`, `edgenuity_course3_*`, `edgenuity_linear_equations_practice`, `gk_*`, `vocab_*`, `map_explorer_*`, `science_*`, `logo_id_*`.

---

## Arjun's learner profile

- **Age**: ~11 years old
- **Primary use**: Daily math practice (Edgenuity + Course 3), enrichment quizzes (GK, vocab, geography, science, logos)
- **Tone**: Kid-friendly UI, emoji badges, encouraging feedback, LaTeX for equations
- **Math notation**: Fractions as `2/3`, not words; × and ÷ symbols preferred in AI-generated questions
- **Parent visibility**: Email reports after math practice; Google Sheets backup for streaks, logins, daily summaries, practice results, and week plans

---

## Arjun dashboard — all apps

### Row 1

#### 1. Edgenuity Course 3 (`EdgenuityCourse3`)

**Purpose**: Grade 8 math aligned with Arjun's **Edgenuity** online school course — lesson notes, unit practice, linear equation strategies, and weekly planning.

**UI file**: `edgenuity_course3_ui.py`  
**Content**: `ArjunEdgenuityCourse3/notes/unit_*/` (markdown + PNG diagrams)  
**Metadata**: `arjun_edgenuity_course3_content.py` (6 units)  
**Practice**: `arjun_edgenuity_course3_practice.py` + `arjun_edgenuity_course3_unit{1-6}_practice.py`  
**LLM (optional)**: `arjun_edgenuity_course3_llm.py` (xAI Grok)

**Home screen tabs**:

| Tab | What it does |
|-----|----------------|
| **Course Units** | Grid of Units 1–6; each unit has activities with lesson notes and daily practice |
| **Solving Linear Equations** | Standalone practice using 7 solving strategies (not tied to a single unit) |
| **Week Setup** | Parent/admin panel: mental math drills, linear equation strategies, AI toggle, week label |

**Per-unit flow**:
1. Open unit → see activity list
2. **Notes** — rendered markdown with inline diagrams (`arjun_edgenuity_course3_render.py`)
3. **Practice** — 15-question daily set (or 8-question focus set for weak categories)
4. **Session report** — strengths, weak topics, revision links to specific activities
5. On completion — score saved, optional email + Google Sheets row

**Linear equation strategies** (`arjun_linear_equation_strategies.py`):

1. Inspection & Cover-Up Method  
2. Inverse Operations (1-Step & 2-Step)  
3. Grouping & Combining Like Terms  
4. Expansion via Distributive Property  
5. Clearing Fractions & Decimals (LCD Method)  
6. Variables on Both Sides  
7. Special Cases (Identity & No Solution)  

Each strategy has levels **A → E** (easier → harder). Week Setup picks which strategy+level combos appear in practice.

**Week Setup** (`edgenuity_linear_equations_ui.py` → `render_setup_panel`):
- **Mental Math Muscle Memory** — see section below; configured at top of Week Setup
- **Linear Equation Strategies** — multiselect levels per strategy
- **Generate questions with AI (xAI Grok)** — when ON, all Edgenuity unit practice + linear equations use Grok instead of static banks
- Saves to SQLite (`database.get_linear_eq_week_config`) and syncs to Google Sheet tab `LinearEqWeekPlan`

---

#### 2. Course 3 Math (`Course3Math`)

**Purpose**: Separate **companion** Grade 8 math curriculum — Units 1–5 with rich lesson notes and large practice banks. Not the same content tree as Edgenuity (different folder, different activity numbering).

**UI file**: `course3_ui.py`  
**Content**: `ArjunCourse3/notes/unit_*/`  
**Metadata**: `arjun_course3_content.py`  
**Practice**: `arjun_course3_practice.py` + `arjun_course3_unit{1-5}_practice.py`  
**LLM (optional)**: `arjun_course3_llm.py` (xAI Grok)

**Units**:

| Unit | Topic |
|------|-------|
| 1 | Numerical relationships |
| 2 | Equations & linear relationships |
| 3 | Geometry |
| 4 | Functions |
| 5 | Probability & statistics |
| 6 | Placeholder — "coming soon" |

**Features** (mirror Edgenuity UX):
- Unit grid → activities → notes viewer → practice session
- Daily set (~15 Q) or focus set (~8 Q) on weak category
- Session report with revision links
- Per-unit Grok toggle in UI (in addition to global Week Setup AI flag for Edgenuity)
- Avoids repeating questions from last 2 sessions (`database.get_recent_ec3_question_ids` with unit offset)

**Important**: Edgenuity and Course 3 Math are **two parallel products** on the dashboard. Parents often want Edgenuity next to schoolwork; Course 3 Math is the extended notes/practice library.

---

#### 3. General Knowledge (`GK`)

**Purpose**: Daily 15-question AI quiz on varied kid-friendly topics.

**Files**: `gk_content.py` (profiles + Grok prompts), `app.py` (`render_gk_home`, `render_gk_practice`)  
**API**: xAI via `XAI_API_KEY`  
**Activity type logged**: `GK`

**Arjun profile topics** (sample): Science, Animals, Space, Geography, History, Sports, Inventions, Mythology, Olympics, etc. — 15 unique topics per quiz, medium difficulty.

**Flow**:
1. GK Home — shows today's best score if already completed
2. **Start Today's Quiz** or **New Quiz** — Grok generates 15 MCQs; cached in DB for the day (`database.save_daily_questions`)
3. Question-by-question practice with explanations
4. Optional chat follow-up per question (`gk_chat_histories` in session state)
5. Score saved to `activity_scores`

**Requires**: `XAI_API_KEY` in Streamlit secrets or environment.

---

### Row 2

#### 4. Vocabulary (`Vocabulary`)

**Purpose**: Academic vocabulary — 200 Tier-2-style words; pick the correct definition.

**Files**: `vocabulary_content.py`, `arjun_vocabulary.json`, `app.py`  
**Activity type**: `Vocabulary`  
**Quiz size**: 10 words per session, sequential through the 200-word list (wraps)  
**Progress**: `database.get_arjun_vocab_index` / `set_arjun_vocab_index` tracks position

---

#### 5. Map Explorer (`MapExplorer`)

**Purpose**: World geography quiz with maps, flags, and fun facts.

**Files**: `map_explorer_content.py`, `world_map_data.py`, `app.py`  
**Activity type**: `MapExplorer`  
**Categories**: Continents & Oceans, Countries & Capitals, Landmarks, Nature, Flags, World Culture  
**Features**: Large static question bank; map markers (lat/lon); flag images via flagcdn.com; explanations after each answer

---

#### 6. Science Corner (`Science`)

**Purpose**: Grade 6 **Inspire Science** style quizzes.

**Files**: `science_content.py`, `generate_science_images.py`, `app.py`  
**Activity type**: `Science`  
**Categories**: Life Science, Reproduction & Inheritance, Ecosystems, Matter & Physical Science, Earth & Space, Waves/Light/Sound  
**Features**: Static question bank with optional diagram images per question

---

### Row 3

#### 7. Logo Identifier (`LogoID`)

**Purpose**: Guess the brand from its logo — fun brand recognition game.

**Files**: `logo_identifier_content.py`, `download_brand_logos.py`, `app.py`  
**Activity type**: `LogoID`  
**Images**: Local PNGs + Google favicon API fallback  
**Flow**: Multiple-choice brand name from logo image

---

## Mental math muscle memory (integrated warm-ups)

**Not a separate dashboard tile anymore** — configured in **Edgenuity → Week Setup → Mental Math Muscle Memory** (top of panel).

**File**: `arjun_mental_math_drills.py`  
**Default**: 5 warm-up questions per session (slider 0–15)

**17 drill types in 5 groups**:

| Group | Drills |
|-------|--------|
| Powers & Roots | squares, cubes, square_roots, powers_of_ten |
| Core Arithmetic | mult_facts, integer_ops, order_of_ops, distributive_trick |
| Fractions & Percents | frac_decimal, frac_ops, percent_snap, gcf_lcm |
| Algebra Patterns | special_products, unit_rates, slope_snap |
| Geometry | pythagorean_triples, angle_pairs |

Each drill has levels **A, B, C** (some have fewer). When enabled in Week Setup, warm-ups prepend to:
- Solving Linear Equations practice
- Edgenuity unit practice (when AI mode on)
- Course 3 unit practice (when AI mode on)

---

## Edgenuity vs Course 3 Math — quick comparison

| | **Edgenuity Course 3** | **Course 3 Math** |
|---|------------------------|-------------------|
| Folder | `ArjunEdgenuityCourse3/` | `ArjunCourse3/` |
| Units | 6 (Edgenuity-aligned) | 5 (+ unit 6 placeholder) |
| Extra tabs | Linear Equations, Week Setup | None |
| Practice modules | `arjun_edgenuity_course3_*` | `arjun_course3_*` |
| UI | `edgenuity_course3_ui.py` | `course3_ui.py` |
| School alignment | Matches Edgenuity coursework | Companion / enrichment |

Both support: notes, diagrams, daily practice, focus practice, Grok AI mode, session reports, email, Sheets sync.

---

## Data, scoring, and sync

### SQLite (`onepercent.db`, `database.py`)

Key tables/functions:
- **Users** — Arjun, Krish, Sangeetha, Rakesh
- **daily_logins** — streak calculation
- **activity_scores** — score, activity_type, time_spent, log_date
- **daily_summaries** — aggregated stats per user per day
- **linear_eq_week_config** — weekly plan JSON (strategies + mental math + use_llm)
- **ec3_practice_sessions / ec3_practice_results** — math session history
- **reading_progress** — Krish's reading (not Arjun's primary)

**Dashboard stats** (`get_user_daily_stats`): streak, total days, activities today, avg score today, time today.

### Google Sheets (`google_sheets_sync.py`)

When `GOOGLE_SHEETS_ENABLED` + service account configured:

| Tab | Contents |
|-----|----------|
| `EdgenuityPractice` | Each math practice session (both tracks) |
| `LinearEqWeekPlan` | Weekly strategy + mental math config |
| `DailyLogins` | Login events |
| `UserStreaks` | Streak + total days per user |
| `UserDailySummary` | Daily activity count, avg score, time |

Bidirectional sync on app startup; push after login and score saves.

### Email reports (`practice_email/`, `edgenuity_practice_email.py`)

After math practice completion, sends HTML report to parent email (`PRACTICE_REPORT_EMAIL_TO`). Supports Gmail OAuth (recommended on Streamlit Cloud) or SMTP. Failed sends queue for retry (`flush_pending` on each app interaction).

---

## LLM integrations

| Module | Provider | Secret | Used for |
|--------|----------|--------|----------|
| GK | xAI Grok | `XAI_API_KEY` | Daily 15-question quiz |
| Edgenuity / Course 3 / Linear Eq practice | xAI Grok | `XAI_API_KEY` | Optional fresh MCQs |
| Story images (Krish) | Hugging Face | `HF_TOKEN` | Not Arjun's primary path |
| AI Forge (Rakesh only) | Anthropic | `ANTHROPIC_API_KEY` | Not on Arjun dashboard |

### Numeric fraction rules (`llm_question_format.py`)

All Grok math question generators must:
- Use `2/3`, `8/15` — never "two thirds"
- Use ×, ÷, +, −, = symbols
- Keep options numeric and consistent
- Validation rejects word fractions; retry with `NUMERIC_RETRY_HINT`

Files using this: `arjun_course3_llm.py`, `arjun_edgenuity_course3_llm.py`, `arjun_linear_equation_llm.py`.

---

## Legacy / hidden modules (code exists, not on Arjun dashboard)

These still have render functions in `app.py` but **no dashboard button** for Arjun:

- **MentalMath** — standalone sprint; superseded by Week Setup drills
- **ProblemSolver** — word-problem scenarios
- **MovieBuff** — movie trivia
- **ArjunStories** — AI story generation

Do not remove without checking — routes may still be reachable via session state hacks.

---

## File map (Arjun-relevant)

```
app.py                              # Main app, dashboard, GK/vocab/map/science/logo UI
database.py                         # SQLite schema and queries
course3_ui.py                       # Course 3 Math UI
edgenuity_course3_ui.py             # Edgenuity Course 3 UI
edgenuity_linear_equations_ui.py    # Linear eq practice + Week Setup
arjun_course3_content.py            # Course 3 units/activities metadata
arjun_edgenuity_course3_content.py  # Edgenuity units/activities metadata
arjun_course3_practice.py           # Course 3 session builder
arjun_edgenuity_course3_practice.py # Edgenuity session builder
arjun_course3_llm.py                # Grok for Course 3
arjun_edgenuity_course3_llm.py      # Grok for Edgenuity
arjun_linear_equation_llm.py        # Grok for linear equations
arjun_linear_equation_strategies.py # 7 strategies + generators
arjun_linear_equation_practice.py   # Linear eq session builder
arjun_mental_math_drills.py         # 17 mental math drill generators
llm_question_format.py              # Numeric fraction rules + validation
gk_content.py                       # GK profiles and Grok prompts
vocabulary_content.py               # 200-word vocab quiz builder
map_explorer_content.py             # Geography question bank
science_content.py                  # Grade 6 science question bank
logo_identifier_content.py          # Brand logo quiz bank
google_sheets_sync.py               # Sheets backup/sync
edgenuity_practice_email.py         # Email wrapper
practice_email/                     # Email delivery package
ArjunCourse3/notes/                 # Course 3 lesson markdown + images
ArjunEdgenuityCourse3/notes/        # Edgenuity lesson markdown + images
.streamlit/secrets.toml             # Local secrets (gitignored)
```

---

## Common development tasks

### Add practice questions to a unit
1. Edit the unit bank: `arjun_course3_unitN_practice.py` or `arjun_edgenuity_course3_unitN_practice.py`
2. Each question: `{ "id", "category", "question", "options", "answer", ... }`
3. Register category in the unit's `UNITN_CATEGORIES` dict

### Change dashboard layout
- Edit `render_user_dashboard()` in `app.py` (Arjun section ~lines 1230–1328)
- **Must push to GitHub `main`** for Streamlit Cloud to update

### Change weekly mental math or strategies
- UI: Edgenuity → Week Setup tab
- Code: `edgenuity_linear_equations_ui.py`, `arjun_mental_math_drills.py`, `arjun_linear_equation_strategies.py`
- Persistence: `database.save_linear_eq_week_config()`

### Fix Grok question wording
- Prompts: `*_llm.py` files and `gk_content.py`
- Shared rules: `llm_question_format.py`
- User must **start a new practice session** to see changes

### Test locally
```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Copy `.streamlit/secrets.toml.example` → `secrets.toml` and add keys as needed.

---

## Deployment checklist

1. Commit source changes (not `onepercent.db`, not `.streamlit/secrets.toml`)
2. Push to `origin/main`
3. Streamlit Cloud redeploys automatically
4. Configure secrets in Streamlit Cloud dashboard: `XAI_API_KEY`, email, Google Sheets, etc.
5. Verify hosted app shows new dashboard layout / behavior

---

## Pitfalls agents should avoid

1. **Confusing the two math apps** — Edgenuity vs Course 3 Math use different folders, IDs, and UI files.
2. **Expecting instant Grok wording fixes** — active `st.session_state` sessions keep old questions until restarted.
3. **Forgetting to push** — local changes don't appear on Streamlit Cloud until pushed to `main`.
4. **Word fractions in AI prompts** — always use numeric notation for an 11-year-old reader.
5. **Hiding mental math** — it's in Week Setup at the **top**, not buried below linear equation strategies.
6. **Committing secrets or DB** — use `.gitignore`; use Streamlit Cloud secrets for production keys.

---

## Other users (brief — for context only)

| User | Activities |
|------|------------|
| **Krish** | Sentence reading, CVC words, Addition, Picture books |
| **Sangeetha** | GK only (+ coming soon placeholder) |
| **Rakesh** | GK (US-focused), US Civics, AI Forge, Network Architecture |

Arjun-focused work should not break other user dashboards in `render_user_dashboard()`.

---

*Last updated: reflects dashboard layout with Course 3 Math in row 1, mental math in Week Setup, Google Sheets daily sync, and numeric Grok fraction formatting.*
