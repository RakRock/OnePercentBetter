"""
1% Better Every Day - Main Application
A daily improvement tracker for kids and adults.
"""

try:
    import truststore
    truststore.inject_into_ssl()
except ImportError:
    pass

import os
import streamlit as st
import database as db
from datetime import datetime, timedelta
from collections import defaultdict
import plotly.graph_objects as go
import time
import reading_content as rc
import math_content as mc

# ── Optional imports for story generation (only when HF_TOKEN is set) ──
_HF_TOKEN = os.environ.get("HF_TOKEN")
_CAN_GENERATE = bool(_HF_TOKEN)

# ── xAI key for GK module (from secrets.toml or env var) ──
try:
    _XAI_API_KEY = st.secrets.get("XAI_API_KEY") or os.environ.get("XAI_API_KEY")
except Exception:
    _XAI_API_KEY = os.environ.get("XAI_API_KEY")
_CAN_GK = bool(_XAI_API_KEY)

# ──────────────────────────────────────────────
# App Configuration
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="1% Better Every Day",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Initialize database
db.init_db()


def _daily_time_calendar_fallback(user_id: int, days: int = 30) -> list:
    """Fill calendar days when ``database.get_daily_time_spent_calendar`` is missing (older deploys)."""
    sparse = db.get_daily_time_spent(user_id, days=days)
    by_date = {r["log_date"]: r for r in sparse}
    end = datetime.now().date()
    start = end - timedelta(days=days - 1)
    out = []
    d = start
    while d <= end:
        ds = d.strftime("%Y-%m-%d")
        if ds in by_date:
            out.append(dict(by_date[ds]))
        else:
            out.append({"log_date": ds, "total_seconds": 0, "activity_count": 0})
        d += timedelta(days=1)
    return out


def _daily_score_calendar_fallback(user_id: int, days: int = 30) -> list:
    """Per-day average scores when ``database.get_daily_score_calendar`` is missing (older deploys)."""
    hist = db.get_scores_history(user_id, days=days)
    by_day: dict[str, list] = defaultdict(list)
    for h in hist:
        by_day[h["log_date"]].append(h["score"])
    end = datetime.now().date()
    start = end - timedelta(days=days - 1)
    out = []
    d = start
    while d <= end:
        ds = d.strftime("%Y-%m-%d")
        if ds in by_day:
            scores = by_day[ds]
            out.append(
                {
                    "log_date": ds,
                    "avg_score": round(sum(scores) / len(scores), 1),
                    "best_score": max(scores),
                    "activity_count": len(scores),
                }
            )
        else:
            out.append(
                {
                    "log_date": ds,
                    "avg_score": None,
                    "best_score": None,
                    "activity_count": 0,
                }
            )
        d += timedelta(days=1)
    return out


def daily_time_calendar_for_dashboard(user_id: int, days: int = 30) -> list:
    fn = getattr(db, "get_daily_time_spent_calendar", None)
    if callable(fn):
        return fn(user_id, days=days)
    return _daily_time_calendar_fallback(user_id, days=days)


def daily_score_calendar_for_dashboard(user_id: int, days: int = 30) -> list:
    fn = getattr(db, "get_daily_score_calendar", None)
    if callable(fn):
        return fn(user_id, days=days)
    return _daily_score_calendar_fallback(user_id, days=days)


# ──────────────────────────────────────────────
# Custom CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
    /* Main app styling */
    .main .block-container {
        padding-top: 2rem;
        max-width: 1100px;
    }

    /* Hero title */
    .hero-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .hero-subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #6b7280;
        margin-bottom: 2rem;
    }

    /* User card styling */
    .user-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 20px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
        border: 3px solid transparent;
        min-height: 220px;
    }
    .user-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    .user-emoji { font-size: 4rem; display: block; margin-bottom: 0.5rem; }
    .user-name { font-size: 1.5rem; font-weight: 700; color: #1f2937; }

    /* Streak badge */
    .streak-badge {
        display: inline-block;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }

    /* Score card */
    .score-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        text-align: center;
    }
    .score-number { font-size: 2.5rem; font-weight: 800; color: #667eea; }
    .score-label { font-size: 0.9rem; color: #6b7280; font-weight: 500; }

    /* Button styles */
    .stButton > button {
        border-radius: 12px;
        font-weight: 600;
        padding: 0.5rem 2rem;
    }

    /* Divider */
    .fancy-divider {
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2, #f093fb);
        border: none;
        border-radius: 2px;
        margin: 1.5rem 0;
    }

    /* ─── Book covers on reading home ─── */
    .book-cover {
        border-radius: 18px;
        padding: 1.2rem 0.8rem;
        text-align: center;
        min-height: 160px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 14px rgba(0,0,0,0.10);
        transition: transform 0.2s ease;
    }
    .book-cover:hover {
        transform: scale(1.04);
    }
    .book-emoji { font-size: 2.4rem; }
    .book-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: white;
        margin-top: 0.4rem;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
    }
    .book-pages {
        font-size: 0.8rem;
        color: rgba(255,255,255,0.85);
        margin-top: 0.2rem;
    }

    /* ─── Picture book page ─── */
    .story-page {
        background: #fffef5;
        border: 3px solid #e5e7eb;
        border-radius: 24px;
        max-width: 640px;
        margin-left: auto;
        margin-right: auto;
        padding: 2rem 1.5rem;
        text-align: center;
        margin: 0.75rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .story-page img {
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        max-width: 512px;
        margin: 0 auto;
    }
    .story-page-text {
        font-size: 1.6rem;
        font-weight: 600;
        color: #1f2937;
        line-height: 1.5;
        font-family: 'Georgia', 'Times New Roman', serif;
    }
    .story-page-number {
        font-size: 0.8rem;
        color: #9ca3af;
        margin-top: 0.5rem;
    }

    /* ─── Quiz styling ─── */
    .quiz-question {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.3rem;
    }
    .correct-answer {
        background: #d1fae5;
        border: 3px solid #10b981;
        border-radius: 16px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        font-size: 1.1rem;
    }
    .wrong-answer {
        background: #fee2e2;
        border: 3px solid #ef4444;
        border-radius: 16px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        font-size: 1.1rem;
    }

    /* ─── Math problem display ─── */
    .math-problem-box {
        background: #fffef5;
        border: 3px solid #e5e7eb;
        border-radius: 24px;
        padding: 1.5rem 1rem;
        text-align: center;
        margin: 0.75rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .math-problem-box img {
        border-radius: 8px;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));
    }
    .math-question-text {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-top: 0.5rem;
    }
    .math-option-btn button {
        font-size: 1.4rem !important;
        padding: 1rem !important;
        min-height: 70px !important;
    }
    .math-level-card {
        border-radius: 18px;
        padding: 1.5rem 1rem;
        text-align: center;
        min-height: 170px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 14px rgba(0,0,0,0.10);
        transition: transform 0.2s ease;
    }
    .math-level-card:hover {
        transform: scale(1.04);
    }

    /* ─── GK topic badge ─── */
    .gk-topic-badge {
        display: inline-block;
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
    }
    .gk-question-box {
        background: #fffef5;
        border: 3px solid #e5e7eb;
        border-radius: 24px;
        padding: 2rem 1.5rem;
        text-align: center;
        margin: 0.75rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    .gk-question-text {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1f2937;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Session State Initialization
# ──────────────────────────────────────────────
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"
if "selected_user" not in st.session_state:
    st.session_state.selected_user = None
if "selected_activity" not in st.session_state:
    st.session_state.selected_activity = None
if "reading_state" not in st.session_state:
    st.session_state.reading_state = None
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "reading_start_time" not in st.session_state:
    st.session_state.reading_start_time = None
if "story_page_idx" not in st.session_state:
    st.session_state.story_page_idx = 0
if "gen_status" not in st.session_state:
    st.session_state.gen_status = None  # None | "generating" | "done" | "error"
if "gen_error" not in st.session_state:
    st.session_state.gen_error = ""
# Math module state
if "math_level" not in st.session_state:
    st.session_state.math_level = None
if "math_problems" not in st.session_state:
    st.session_state.math_problems = []
if "math_current" not in st.session_state:
    st.session_state.math_current = 0
if "math_answers" not in st.session_state:
    st.session_state.math_answers = []
if "math_start_time" not in st.session_state:
    st.session_state.math_start_time = None
# GK module state
if "gk_questions" not in st.session_state:
    st.session_state.gk_questions = []
if "gk_current" not in st.session_state:
    st.session_state.gk_current = 0
if "gk_answers" not in st.session_state:
    st.session_state.gk_answers = []
if "gk_chat_histories" not in st.session_state:
    st.session_state.gk_chat_histories = {}
if "gk_start_time" not in st.session_state:
    st.session_state.gk_start_time = None
# Map Explorer state
if "me_questions" not in st.session_state:
    st.session_state.me_questions = []
if "me_current" not in st.session_state:
    st.session_state.me_current = 0
if "me_answers" not in st.session_state:
    st.session_state.me_answers = []
if "me_last_feedback" not in st.session_state:
    st.session_state.me_last_feedback = None
if "me_start_time" not in st.session_state:
    st.session_state.me_start_time = None
# Problem Solver state
if "ps_scenario" not in st.session_state:
    st.session_state.ps_scenario = None
if "ps_current_step" not in st.session_state:
    st.session_state.ps_current_step = 0
if "ps_answers" not in st.session_state:
    st.session_state.ps_answers = []
if "ps_last_feedback" not in st.session_state:
    st.session_state.ps_last_feedback = None
if "ps_start_time" not in st.session_state:
    st.session_state.ps_start_time = None
# Mental Math state
if "mm_questions" not in st.session_state:
    st.session_state.mm_questions = []
if "mm_current" not in st.session_state:
    st.session_state.mm_current = 0
if "mm_answers" not in st.session_state:
    st.session_state.mm_answers = []
if "mm_last_feedback" not in st.session_state:
    st.session_state.mm_last_feedback = None
if "mm_start_time" not in st.session_state:
    st.session_state.mm_start_time = None
# Logo Identifier state
if "logo_questions" not in st.session_state:
    st.session_state.logo_questions = []
if "logo_current" not in st.session_state:
    st.session_state.logo_current = 0
if "logo_answers" not in st.session_state:
    st.session_state.logo_answers = []
if "logo_last_feedback" not in st.session_state:
    st.session_state.logo_last_feedback = None
if "logo_start_time" not in st.session_state:
    st.session_state.logo_start_time = None
# Movie Buff state
if "movie_questions" not in st.session_state:
    st.session_state.movie_questions = []
if "movie_current" not in st.session_state:
    st.session_state.movie_current = 0
if "movie_answers" not in st.session_state:
    st.session_state.movie_answers = []
if "movie_last_feedback" not in st.session_state:
    st.session_state.movie_last_feedback = None
if "movie_start_time" not in st.session_state:
    st.session_state.movie_start_time = None
# Science Corner state
if "sci_questions" not in st.session_state:
    st.session_state.sci_questions = []
if "sci_current" not in st.session_state:
    st.session_state.sci_current = 0
if "sci_answers" not in st.session_state:
    st.session_state.sci_answers = []
if "sci_last_feedback" not in st.session_state:
    st.session_state.sci_last_feedback = None
if "sci_start_time" not in st.session_state:
    st.session_state.sci_start_time = None
# Cube Addition state
if "cube_problem" not in st.session_state:
    st.session_state.cube_problem = None
if "cube_phase" not in st.session_state:
    st.session_state.cube_phase = "intro"
if "cube_score" not in st.session_state:
    st.session_state.cube_score = 0
if "cube_total" not in st.session_state:
    st.session_state.cube_total = 0
if "cube_streak" not in st.session_state:
    st.session_state.cube_streak = 0


# ──────────────────────────────────────────────
# Navigation helpers
# ──────────────────────────────────────────────
def go_home():
    st.session_state.current_page = "home"
    st.session_state.selected_user = None
    st.session_state.selected_activity = None
    st.session_state.reading_state = None
    st.session_state.quiz_answers = {}
    st.session_state.quiz_submitted = False
    st.session_state.story_page_idx = 0


def select_user(name):
    st.session_state.current_page = "user_dashboard"
    st.session_state.selected_user = name
    st.session_state.selected_activity = None
    user = db.get_user(name)
    if user:
        db.record_daily_login(user["id"])


def select_activity(activity):
    st.session_state.selected_activity = activity
    if activity == "Reading":
        st.session_state.current_page = "reading_home"
    elif activity == "Math":
        st.session_state.current_page = "math_home"
    elif activity == "GK":
        st.session_state.current_page = "gk_home"
    elif activity == "ArjunStories":
        st.session_state.current_page = "arjun_stories_home"
    elif activity == "Civics":
        st.session_state.current_page = "civics_home"
    elif activity == "SightWords":
        st.session_state.current_page = "sight_words_home"
    elif activity == "MapExplorer":
        st.session_state.current_page = "map_explorer_home"
    elif activity == "ProblemSolver":
        st.session_state.current_page = "problem_solver_home"
    elif activity == "MentalMath":
        st.session_state.current_page = "mental_math_home"
    elif activity == "Science":
        st.session_state.current_page = "science_home"
    elif activity == "MovieBuff":
        st.session_state.current_page = "movie_buff_home"
    elif activity == "LogoID":
        st.session_state.current_page = "logo_id_home"
    elif activity == "CubeAddition":
        st.session_state.current_page = "cube_addition"
        st.session_state.cube_problem = None
        st.session_state.cube_phase = "intro"
        st.session_state.cube_score = 0
        st.session_state.cube_total = 0
        st.session_state.cube_streak = 0


def start_story(story_id):
    st.session_state.reading_state = story_id
    st.session_state.current_page = "reading_story"
    st.session_state.quiz_answers = {}
    st.session_state.quiz_submitted = False
    st.session_state.reading_start_time = time.time()
    st.session_state.story_page_idx = 0


def back_to_reading_home():
    st.session_state.current_page = "reading_home"
    st.session_state.reading_state = None
    st.session_state.quiz_answers = {}


def back_to_arjun_stories():
    st.session_state.current_page = "arjun_stories_home"
    st.session_state.reading_state = None
    st.session_state.quiz_answers = {}
    st.session_state.quiz_submitted = False
    st.session_state.story_page_idx = 0


def go_to_generate():
    st.session_state.current_page = "generate_story"
    st.session_state.gen_status = None
    st.session_state.gen_error = ""


def start_math_level(level_id):
    st.session_state.current_page = "math_practice"
    st.session_state.math_level = level_id
    st.session_state.math_problems = mc.generate_round(level_id, num_problems=5)
    st.session_state.math_current = 0
    st.session_state.math_answers = []
    st.session_state.math_start_time = time.time()


def back_to_math_home():
    st.session_state.current_page = "math_home"
    st.session_state.math_level = None
    st.session_state.math_problems = []
    st.session_state.math_current = 0
    st.session_state.math_answers = []


def go_to_gk_home():
    st.session_state.current_page = "gk_home"


def start_gk_quiz(questions):
    st.session_state.current_page = "gk_practice"
    st.session_state.gk_questions = questions
    st.session_state.gk_current = 0
    st.session_state.gk_answers = []
    st.session_state.gk_chat_histories = {}
    st.session_state.gk_start_time = time.time()


def back_to_gk_home():
    st.session_state.current_page = "gk_home"
    st.session_state.gk_questions = []
    st.session_state.gk_current = 0
    st.session_state.gk_answers = []
    st.session_state.gk_chat_histories = {}


def start_civics_quiz(questions):
    st.session_state.current_page = "civics_practice"
    st.session_state.civics_questions = questions
    st.session_state.civics_current = 0
    st.session_state.civics_answers = []
    st.session_state.civics_start_time = time.time()
    st.session_state.civics_last_feedback = None


def back_to_civics_home():
    st.session_state.current_page = "civics_home"
    st.session_state.civics_questions = []
    st.session_state.civics_current = 0
    st.session_state.civics_answers = []
    st.session_state.civics_last_feedback = None


def start_sight_words(level_id):
    import sight_words_content as sw
    questions = sw.generate_round(level_id)
    st.session_state.current_page = "sight_words_practice"
    st.session_state.sw_level = level_id
    st.session_state.sw_questions = questions
    st.session_state.sw_current = 0
    st.session_state.sw_start_time = time.time()


def back_to_sight_words_home():
    st.session_state.current_page = "sight_words_home"
    st.session_state.sw_questions = []
    st.session_state.sw_current = 0


def start_map_explorer(questions):
    st.session_state.current_page = "map_explorer_practice"
    st.session_state.me_questions = questions
    st.session_state.me_current = 0
    st.session_state.me_answers = []
    st.session_state.me_last_feedback = None
    st.session_state.me_start_time = time.time()


def back_to_map_explorer_home():
    st.session_state.current_page = "map_explorer_home"
    st.session_state.me_questions = []
    st.session_state.me_current = 0
    st.session_state.me_answers = []
    st.session_state.me_last_feedback = None


def start_problem_solver(scenario):
    st.session_state.current_page = "problem_solver_practice"
    st.session_state.ps_scenario = scenario
    st.session_state.ps_current_step = 0
    st.session_state.ps_answers = []
    st.session_state.ps_last_feedback = None
    st.session_state.ps_start_time = time.time()


def back_to_problem_solver_home():
    st.session_state.current_page = "problem_solver_home"
    st.session_state.ps_scenario = None
    st.session_state.ps_current_step = 0
    st.session_state.ps_answers = []
    st.session_state.ps_last_feedback = None


def start_mental_math(questions):
    st.session_state.current_page = "mental_math_practice"
    st.session_state.mm_questions = questions
    st.session_state.mm_current = 0
    st.session_state.mm_answers = []
    st.session_state.mm_last_feedback = None
    st.session_state.mm_start_time = time.time()


def back_to_mental_math_home():
    st.session_state.current_page = "mental_math_home"
    st.session_state.mm_questions = []
    st.session_state.mm_current = 0
    st.session_state.mm_answers = []
    st.session_state.mm_last_feedback = None


def start_science_quiz(questions):
    st.session_state.current_page = "science_practice"
    st.session_state.sci_questions = questions
    st.session_state.sci_current = 0
    st.session_state.sci_answers = []
    st.session_state.sci_last_feedback = None
    st.session_state.sci_start_time = time.time()


def back_to_science_home():
    st.session_state.current_page = "science_home"
    st.session_state.sci_questions = []
    st.session_state.sci_current = 0
    st.session_state.sci_answers = []
    st.session_state.sci_last_feedback = None


def start_movie_quiz(questions):
    st.session_state.current_page = "movie_buff_practice"
    st.session_state.movie_questions = questions
    st.session_state.movie_current = 0
    st.session_state.movie_answers = []
    st.session_state.movie_last_feedback = None
    st.session_state.movie_start_time = time.time()


def back_to_movie_home():
    st.session_state.current_page = "movie_buff_home"
    st.session_state.movie_questions = []
    st.session_state.movie_current = 0
    st.session_state.movie_answers = []
    st.session_state.movie_last_feedback = None


def start_logo_quiz(questions):
    st.session_state.current_page = "logo_id_practice"
    st.session_state.logo_questions = questions
    st.session_state.logo_current = 0
    st.session_state.logo_answers = []
    st.session_state.logo_last_feedback = None
    st.session_state.logo_start_time = time.time()


def back_to_logo_home():
    st.session_state.current_page = "logo_id_home"
    st.session_state.logo_questions = []
    st.session_state.logo_current = 0
    st.session_state.logo_answers = []
    st.session_state.logo_last_feedback = None


# ──────────────────────────────────────────────
# PAGE: Home (User Selection)
# ──────────────────────────────────────────────
def render_home():
    st.markdown('<h1 class="hero-title">1% Better Every Day</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Small daily improvements lead to extraordinary results over time</p>', unsafe_allow_html=True)
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    st.markdown("### 👋 Who's practicing today?")
    st.markdown("")

    users = [
        ("Arjun", "🦁", "#ff6b6b", "The fearless learner"),
        ("Krish", "🚀", "#667eea", "Reaching for the stars"),
        ("Sangeetha", "🌸", "#f093fb", "Blooming with knowledge"),
        ("Rakesh", "⚡", "#ffd93d", "Lightning-fast thinker"),
    ]

    cols = st.columns(4, gap="large")
    for i, (name, emoji, color, tagline) in enumerate(users):
        with cols[i]:
            user_data = db.get_user(name)
            streak = db.get_login_streak(user_data["id"]) if user_data else 0
            total_days = db.get_total_login_days(user_data["id"]) if user_data else 0

            st.markdown(f"""
            <div class="user-card" style="border-color: {color}20; background: linear-gradient(135deg, {color}10, {color}25);">
                <span class="user-emoji">{emoji}</span>
                <div class="user-name">{name}</div>
                <div style="color: #6b7280; font-size: 0.85rem; margin: 0.3rem 0;">{tagline}</div>
                <div class="streak-badge">🔥 {streak} day streak</div>
                <div style="color: #9ca3af; font-size: 0.8rem; margin-top: 0.3rem;">{total_days} total days</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button(f"Start as {name}", key=f"btn_{name}", width="stretch", type="primary"):
                select_user(name)
                st.rerun()

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: #9ca3af; padding: 1rem;">
        <em>"The compound effect is the principle of reaping huge rewards from a series of small, smart choices."</em>
        <br>— Darren Hardy
    </div>
    """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# PAGE: User Dashboard
# ──────────────────────────────────────────────
def render_user_dashboard():
    name = st.session_state.selected_user
    user = db.get_user(name)
    if not user:
        st.error("User not found!")
        return

    streak = db.get_login_streak(user["id"])
    total_days = db.get_total_login_days(user["id"])
    today_scores = db.get_today_scores(user["id"])

    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Home", key="back_home"):
            go_home()
            st.rerun()

    st.markdown(f"""
    <div style="text-align: center; padding: 1rem 0;">
        <span style="font-size: 4rem;">{user['avatar_emoji']}</span>
        <h1 style="margin: 0.5rem 0 0.2rem 0;">{name}'s Dashboard</h1>
        <p style="color: #6b7280;">Keep going, you're doing amazing! 🎉</p>
    </div>
    """, unsafe_allow_html=True)

    today_time = db.get_today_time_spent(user["id"])
    today_min, today_sec = divmod(today_time, 60)
    today_time_str = f"{today_min}m {today_sec}s" if today_min > 0 else f"{today_sec}s"
    if today_time == 0:
        today_time_str = "—"

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(f'<div class="score-card"><div class="score-number">🔥 {streak}</div><div class="score-label">Day Streak</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="score-card"><div class="score-number">📅 {total_days}</div><div class="score-label">Total Days</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="score-card"><div class="score-number">✅ {len(today_scores)}</div><div class="score-label">Activities Today</div></div>', unsafe_allow_html=True)
    with col4:
        avg_display = f"{sum(s['score'] for s in today_scores) / len(today_scores):.0f}%" if today_scores else "—"
        st.markdown(f'<div class="score-card"><div class="score-number">⭐ {avg_display}</div><div class="score-label">Avg Score Today</div></div>', unsafe_allow_html=True)
    with col5:
        st.markdown(f'<div class="score-card"><div class="score-number">⏱️ {today_time_str}</div><div class="score-label">Time Today</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    if name == "Krish":
        st.markdown("### 📚 Choose Your Activity")
        st.markdown("")

        act_col1, act_col2, act_col3, act_col4 = st.columns(4, gap="large")
        with act_col1:
            st.markdown("""
            <div class="score-card" style="border-top: 5px solid #10b981;">
                <div style="font-size: 3rem;">📖</div>
                <h3 style="margin: 0.5rem 0;">Reading</h3>
                <p style="color: #6b7280;">Picture books & fun questions</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button("📖 Start Reading", key="btn_reading", width="stretch", type="primary"):
                select_activity("Reading")
                st.rerun()

        with act_col2:
            st.markdown("""
            <div class="score-card" style="border-top: 5px solid #667eea;">
                <div style="font-size: 3rem;">🧮</div>
                <h3 style="margin: 0.5rem 0;">Math</h3>
                <p style="color: #6b7280;">Math puzzles & practice</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button("🧮 Start Math", key="btn_math", width="stretch", type="primary"):
                select_activity("Math")
                st.rerun()

        with act_col3:
            st.markdown("""
            <div class="score-card" style="border-top: 5px solid #f59e0b;">
                <div style="font-size: 3rem;">👁️</div>
                <h3 style="margin: 0.5rem 0;">Sight Words</h3>
                <p style="color: #6b7280;">Learn to read common words</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button("👁️ Sight Words", key="btn_sight_words", width="stretch", type="primary"):
                select_activity("SightWords")
                st.rerun()

        with act_col4:
            st.markdown("""
            <div class="score-card" style="border-top: 5px solid #ef4444;">
                <div style="font-size: 3rem;">🧊</div>
                <h3 style="margin: 0.5rem 0;">Cube Addition</h3>
                <p style="color: #6b7280;">Learn adding with cubes!</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button("🧊 Cube Addition", key="btn_cube_add", width="stretch", type="primary"):
                select_activity("CubeAddition")
                st.rerun()
    elif name == "Arjun":
        st.markdown("### 📚 Choose Your Activity")
        st.markdown("")

        act_row1_c1, act_row1_c2 = st.columns(2, gap="large")
        with act_row1_c1:
            st.markdown("""
            <div class="score-card" style="border-top: 5px solid #f59e0b;">
                <div style="font-size: 3rem;">🧠</div>
                <h3 style="margin: 0.5rem 0;">General Knowledge</h3>
                <p style="color: #6b7280;">Daily quiz on fun topics</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button("🧠 Start GK", key="btn_gk", width="stretch", type="primary"):
                select_activity("GK")
                st.rerun()

        with act_row1_c2:
            st.markdown("""
            <div class="score-card" style="border-top: 5px solid #6366f1;">
                <div style="font-size: 3rem;">📖</div>
                <h3 style="margin: 0.5rem 0;">Factual Stories</h3>
                <p style="color: #6b7280;">Real events, real learning!</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button("📖 Start Stories", key="btn_arjun_stories", width="stretch", type="primary"):
                select_activity("ArjunStories")
                st.rerun()

        st.markdown("")
        act_row2_c1, act_row2_c2 = st.columns(2, gap="large")
        with act_row2_c1:
            st.markdown("""
            <div class="score-card" style="border-top: 5px solid #3b82f6;">
                <div style="font-size: 3rem;">🗺️</div>
                <h3 style="margin: 0.5rem 0;">Map Explorer</h3>
                <p style="color: #6b7280;">Explore the world!</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button("🗺️ Map Explorer", key="btn_map_explorer", width="stretch", type="primary"):
                select_activity("MapExplorer")
                st.rerun()

        with act_row2_c2:
            st.markdown("""
            <div class="score-card" style="border-top: 5px solid #10b981;">
                <div style="font-size: 3rem;">🧩</div>
                <h3 style="margin: 0.5rem 0;">Problem Solver</h3>
                <p style="color: #6b7280;">Break down real-world problems!</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button("🧩 Problem Solver", key="btn_problem_solver", width="stretch", type="primary"):
                select_activity("ProblemSolver")
                st.rerun()

        st.markdown("")
        act_row3_c1, act_row3_c2 = st.columns(2, gap="large")
        with act_row3_c1:
            st.markdown("""
            <div class="score-card" style="border-top: 5px solid #ef4444;">
                <div style="font-size: 3rem;">⚡</div>
                <h3 style="margin: 0.5rem 0;">Mental Math Sprint</h3>
                <p style="color: #6b7280;">Speed + accuracy challenge!</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button("⚡ Mental Math", key="btn_mental_math", width="stretch", type="primary"):
                select_activity("MentalMath")
                st.rerun()

        with act_row3_c2:
            st.markdown("""
            <div class="score-card" style="border-top: 5px solid #06b6d4;">
                <div style="font-size: 3rem;">🔬</div>
                <h3 style="margin: 0.5rem 0;">Science Corner</h3>
                <p style="color: #6b7280;">Grade 6 Inspire Science!</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button("🔬 Science Corner", key="btn_science", width="stretch", type="primary"):
                select_activity("Science")
                st.rerun()

        st.markdown("")
        act_row4_c1, act_row4_c2 = st.columns(2, gap="large")
        with act_row4_c1:
            st.markdown("""
            <div class="score-card" style="border-top: 5px solid #f59e0b;">
                <div style="font-size: 3rem;">🏷️</div>
                <h3 style="margin: 0.5rem 0;">Logo Identifier</h3>
                <p style="color: #6b7280;">Guess the brand from its logo!</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button("🏷️ Logo Identifier", key="btn_logo_id", width="stretch", type="primary"):
                select_activity("LogoID")
                st.rerun()

    elif name == "Sangeetha":
        st.markdown("### 🌸 Choose Your Activity")
        st.markdown("")

        act_col1, act_col2 = st.columns(2, gap="large")
        with act_col1:
            st.markdown("""
            <div class="score-card" style="border-top: 5px solid #f093fb;">
                <div style="font-size: 3rem;">🧠</div>
                <h3 style="margin: 0.5rem 0;">General Knowledge</h3>
                <p style="color: #6b7280;">Daily quiz — learn a little every day</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button("🧠 Start GK", key="btn_gk_s", width="stretch", type="primary"):
                select_activity("GK")
                st.rerun()

        with act_col2:
            st.markdown("""
            <div class="score-card" style="border-top: 5px solid #9ca3af;">
                <div style="font-size: 3rem;">🔮</div>
                <h3 style="margin: 0.5rem 0;">More Coming Soon</h3>
                <p style="color: #6b7280;">Stay tuned for new activities!</p>
            </div>
            """, unsafe_allow_html=True)

    elif name == "Rakesh":
        st.markdown("### ⚡ Choose Your Activity")
        st.markdown("")

        act_col1, act_col2 = st.columns(2, gap="large")
        with act_col1:
            st.markdown("""
            <div class="score-card" style="border-top: 5px solid #3b82f6;">
                <div style="font-size: 3rem;">🧠</div>
                <h3 style="margin: 0.5rem 0;">General Knowledge</h3>
                <p style="color: #6b7280;">Explore the United States daily</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button("🧠 Start GK", key="btn_gk_r", width="stretch", type="primary"):
                select_activity("GK")
                st.rerun()

        with act_col2:
            st.markdown("""
            <div class="score-card" style="border-top: 5px solid #dc2626;">
                <div style="font-size: 3rem;">🏛️</div>
                <h3 style="margin: 0.5rem 0;">US Civics Test</h3>
                <p style="color: #6b7280;">Practice for the citizenship exam</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button("🏛️ Start Civics", key="btn_civics_r", width="stretch", type="primary"):
                select_activity("Civics")
                st.rerun()

    else:
        st.markdown(f"### 🚧 {name}'s activities are coming soon!")
        st.info(f"We're building personalized activities for {name}. Check back soon!")

    # Progress charts — calendar-filled series so every day appears; scores aggregated per day
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📊 Progress Over Time")

    _chart_days = 30
    _cumulative_chart_days = 60  # longer window for running-total line only
    score_calendar = daily_score_calendar_for_dashboard(user["id"], days=_chart_days)
    time_calendar = daily_time_calendar_for_dashboard(user["id"], days=_chart_days)
    time_calendar_cumulative = daily_time_calendar_for_dashboard(
        user["id"], days=_cumulative_chart_days
    )
    # Recent window (charts): any logged scores or time in the last N days
    has_recent_window = any(s["activity_count"] > 0 for s in score_calendar) or any(
        t["total_seconds"] > 0 for t in time_calendar
    )
    # Lifetime: catches older activity outside the window (and helps after Cloud DB resets / new deploys)
    has_lifetime_activity = (
        db.get_total_time_spent(user["id"]) > 0
        or len(db.get_scores_history(user["id"], days=365)) > 0
        or len(db.get_reading_history(user["id"], days=365)) > 0
    )

    # Always show charts so the section is never blank on Streamlit Cloud; empty days render as gaps/zeros
    if not has_recent_window and not has_lifetime_activity:
        st.info(
            "📊 **No activity logged yet.** Complete a quiz, reading, or practice session — "
            "your charts will fill in automatically. "
            "(On a fresh app, everyone starts here.)"
        )
    elif not has_recent_window and has_lifetime_activity:
        st.caption(
            "No sessions in the last 30 days — charts below may look quiet; older data may fall outside this window."
        )

    tab_scores, tab_time = st.tabs(["📈 Scores", "⏱️ Time Spent"])

    with tab_scores:
        dates_s = [s["log_date"] for s in score_calendar]
        y_avg = [s["avg_score"] if s["activity_count"] else None for s in score_calendar]
        n_act = [s["activity_count"] for s in score_calendar]
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dates_s,
            y=y_avg,
            mode="lines+markers",
            connectgaps=False,
            marker=dict(size=8, color="#667eea"),
            line=dict(color="#667eea", width=3),
            customdata=n_act,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Avg score: %{y:.1f}%<br>"
                "Activities: %{customdata}<extra></extra>"
            ),
        ))
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Average score that day (%)",
            yaxis=dict(range=[0, 105]),
            template="plotly_white",
            height=350,
            margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig, width="stretch")
        st.caption(
            "Each point is the **average** of all quiz scores that day. "
            "Days with no activity show a gap."
        )

    with tab_time:
        dates_t = [t["log_date"] for t in time_calendar]
        daily_mins = [round(t["total_seconds"] / 60, 2) for t in time_calendar]
        counts_t = [t["activity_count"] for t in time_calendar]
        bar_colors = ["#10b981" if m > 0 else "#e5e7eb" for m in daily_mins]

        fig_time = go.Figure()
        fig_time.add_trace(go.Bar(
            x=dates_t,
            y=daily_mins,
            marker_color=bar_colors,
            customdata=counts_t,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Minutes: %{y:.1f}<br>"
                "Sessions: %{customdata}<extra></extra>"
            ),
        ))
        fig_time.update_layout(
            xaxis_title="Date",
            yaxis_title="Minutes that day",
            template="plotly_white",
            height=350,
            margin=dict(l=20, r=20, t=20, b=20),
            bargap=0.25,
        )
        st.plotly_chart(fig_time, width="stretch")
        st.caption(
            "Shows **every calendar day** in the last 30 days. "
            "Gray bars are days with no logged activity; green is time spent on quizzes."
        )

        # Running total over last 60 days (bars above stay at 30 days)
        daily_mins_cum = [
            round(t["total_seconds"] / 60, 2) for t in time_calendar_cumulative
        ]
        dates_cum = [t["log_date"] for t in time_calendar_cumulative]
        cum_mins = []
        run = 0.0
        for m in daily_mins_cum:
            run += m
            cum_mins.append(round(run, 1))
        fig_cum = go.Figure()
        fig_cum.add_trace(go.Scatter(
            x=dates_cum,
            y=cum_mins,
            mode="lines+markers",
            fill="tozeroy",
            marker=dict(size=6, color="#059669"),
            line=dict(color="#059669", width=2),
            hovertemplate=f"<b>%{{x}}</b><br>Cumulative ({_cumulative_chart_days}d): %{{y:.1f}} min<extra></extra>",
        ))
        fig_cum.update_layout(
            title=f"Cumulative minutes (last {_cumulative_chart_days} days)",
            xaxis_title="Date",
            yaxis_title="Total minutes (running)",
            template="plotly_white",
            height=280,
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_cum, width="stretch")

        total_all_time = db.get_total_time_spent(user["id"])
        total_hrs, total_rem = divmod(total_all_time, 3600)
        total_mins = total_rem // 60
        st.markdown(f"""
        <div style="text-align:center;padding:0.8rem;background:#ecfdf5;border-radius:12px;
             border:2px solid #10b981;margin-top:0.5rem;">
            <span style="font-size:1.5rem;">⏱️</span>
            <span style="font-size:1.1rem;color:#065f46;">
                <strong>Total time on app (all time):</strong>
                {f'{total_hrs}h {total_mins}m' if total_hrs > 0 else f'{total_mins}m'}
            </span>
        </div>
        """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# PAGE: Reading Home — Bookshelf
# ──────────────────────────────────────────────
def render_reading_home():
    name = st.session_state.selected_user
    user = db.get_user(name)

    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Back", key="back_to_dash"):
            st.session_state.current_page = "user_dashboard"
            st.session_state.selected_activity = None
            st.rerun()

    st.markdown(f"""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <h1 style="font-size: 2.5rem;">📖 {name}'s Bookshelf</h1>
        <p style="color: #6b7280; font-size: 1.1rem;">Pick a book and start reading!</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    reading_history = []
    completed_ids = set()
    today_completed = set()
    if user:
        reading_history = db.get_reading_history(user["id"])
        completed_ids = {h["story_id"] for h in reading_history}
        today = datetime.now().strftime("%Y-%m-%d")
        today_completed = {h["story_id"] for h in reading_history if h["log_date"] == today}

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="score-card"><div class="score-number">📚 {len(completed_ids)}</div><div class="score-label">Stories Read</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="score-card"><div class="score-number">📅 {len(today_completed)}</div><div class="score-label">Read Today</div></div>', unsafe_allow_html=True)
    with col3:
        if reading_history:
            avg_pct = sum(h["questions_correct"] / max(h["questions_total"], 1) * 100 for h in reading_history) / len(reading_history)
            avg_display = f"{avg_pct:.0f}%"
        else:
            avg_display = "—"
        st.markdown(f'<div class="score-card"><div class="score-number">🎯 {avg_display}</div><div class="score-label">Avg Score</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # Book covers grid (newest first) — exclude Arjun's stories from Krish's bookshelf
    stories = [s for s in rc.get_all_stories() if not s["id"].startswith("gen_arjun_")][::-1]
    cols = st.columns(3, gap="medium")

    for j, story in enumerate(stories):
        with cols[j % 3]:
            done_today = story["id"] in today_completed
            is_done = story["id"] in completed_ids
            badge = "✅ Done today!" if done_today else ("⭐ Read before" if is_done else "✨ New!")
            color = story.get("color", "#667eea")

            st.markdown(f"""
            <div class="book-cover" style="background: linear-gradient(135deg, {color}, {color}cc);">
                <div class="book-emoji">{story['cover_emoji']}</div>
                <div class="book-title">{story['title']}</div>
                <div class="book-pages">{len(story['pages'])} pages · {len(story['questions'])} questions</div>
                <div style="margin-top:0.4rem;font-size:0.8rem;color:rgba(255,255,255,0.9);">{badge}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button(f"📖 Read: {story['title']}", key=f"story_{story['id']}", width="stretch", type="primary"):
                start_story(story["id"])
                st.rerun()
            st.markdown("")

    # "Create New Story" card (only shown when HF_TOKEN is available)
    if _CAN_GENERATE:
        next_col = len(stories) % 3
        with cols[next_col]:
            st.markdown("""
            <div class="book-cover" style="background: linear-gradient(135deg, #9ca3af, #6b7280); border: 2px dashed rgba(255,255,255,0.5);">
                <div class="book-emoji">✨</div>
                <div class="book-title">Create New Story</div>
                <div class="book-pages">AI-generated picture book</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button("✨ Create New Story", key="btn_generate", width="stretch", type="secondary"):
                go_to_generate()
                st.rerun()
            st.markdown("")


# ──────────────────────────────────────────────
# PAGE: Reading a Picture Book + Quiz
# ──────────────────────────────────────────────
def render_reading_story():
    name = st.session_state.selected_user
    user = db.get_user(name)
    story_id = st.session_state.reading_state
    story = rc.get_story(story_id)

    if not story:
        st.error("Story not found!")
        return

    pages = story["pages"]
    total_pages = len(pages)
    page_idx = st.session_state.story_page_idx
    color = story.get("color", "#667eea")
    in_quiz = page_idx >= total_pages

    is_arjun_story = story_id and story_id.startswith("gen_arjun_")

    # Navigation bar
    col_nav1, col_nav_mid, col_nav2 = st.columns([1, 4, 1])
    with col_nav1:
        if st.button("← Books", key="back_stories"):
            if is_arjun_story:
                back_to_arjun_stories()
            else:
                back_to_reading_home()
            st.rerun()
    with col_nav_mid:
        if not in_quiz:
            st.markdown(f"""
            <div style="text-align:center; color:#6b7280; font-size:0.9rem; padding-top:0.5rem;">
                Page {page_idx + 1} of {total_pages}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="text-align:center; color:#6b7280; font-size:0.9rem; padding-top:0.5rem;">
                📝 Quiz Time!
            </div>
            """, unsafe_allow_html=True)

    # Book title
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 0.5rem;">
        <h1 style="color: {color}; margin: 0.3rem 0; font-size: 2.2rem;">{story['cover_emoji']} {story['title']}</h1>
    </div>
    """, unsafe_allow_html=True)

    # Progress bar
    if not in_quiz:
        progress = (page_idx + 1) / total_pages
    else:
        progress = 1.0
    st.markdown(f"""
    <div style="background:#e5e7eb;border-radius:10px;height:10px;overflow:hidden;margin:0 0 1.5rem 0;">
        <div style="width:{progress*100:.0f}%;height:100%;background:linear-gradient(90deg,{color},{color}bb);border-radius:10px;transition:width 0.4s ease;"></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Show story pages ──
    if not in_quiz:
        pg = pages[page_idx]
        img_path = rc.get_image_path(story_id, page_idx + 1)

        st.markdown('<div class="story-page" style="display:flex;flex-direction:column;align-items:center;">', unsafe_allow_html=True)

        if os.path.exists(img_path):
            import base64 as _b64
            with open(img_path, "rb") as _imgf:
                _img_b64 = _b64.b64encode(_imgf.read()).decode()
            _ext = os.path.splitext(img_path)[1].lstrip(".") or "png"
            st.markdown(
                f'<img src="data:image/{_ext};base64,{_img_b64}" '
                f'style="max-width:512px;width:100%;border-radius:16px;margin:0 auto;display:block;" />',
                unsafe_allow_html=True,
            )
        else:
            fallback = pg.get("fallback_emoji", "📖")
            st.markdown(f'<div style="font-size:5rem;text-align:center;">{fallback}</div>', unsafe_allow_html=True)

        is_long_text = len(pg['text']) > 120
        if is_long_text:
            text_style = (
                "font-size:1.1rem;font-weight:400;color:#1f2937;line-height:1.8;"
                "font-family:'Georgia','Times New Roman',serif;text-align:left;"
                "max-width:560px;margin:0.8rem auto;padding:0 0.5rem;"
            )
        else:
            text_style = (
                "font-size:1.6rem;font-weight:600;color:#1f2937;line-height:1.5;"
                "font-family:'Georgia','Times New Roman',serif;text-align:center;"
            )

        st.markdown(f"""
            <div style="{text_style}">{pg['text']}</div>
            <div class="story-page-number" style="text-align:center;">— page {page_idx + 1} —</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")

        # Page navigation buttons
        col_prev, col_mid, col_next = st.columns([1, 2, 1])
        with col_prev:
            if page_idx > 0:
                if st.button("⬅️ Back", key="prev_page", width="stretch"):
                    st.session_state.story_page_idx -= 1
                    st.rerun()
        with col_next:
            if page_idx < total_pages - 1:
                if st.button("Next ➡️", key="next_page", width="stretch", type="primary"):
                    st.session_state.story_page_idx += 1
                    st.rerun()
            else:
                if st.button("📝 Take Quiz!", key="go_quiz", width="stretch", type="primary"):
                    st.session_state.story_page_idx = total_pages
                    st.rerun()

    # ── Quiz section ──
    else:
        questions = story["questions"]
        quiz_submitted = st.session_state.quiz_submitted

        st.markdown("""
        <div style="text-align:center; margin-bottom:1rem;">
            <span style="font-size:3rem;">🤔</span>
            <h3 style="margin:0.3rem 0;">Let's see what you remember!</h3>
        </div>
        """, unsafe_allow_html=True)

        for idx, q in enumerate(questions):
            key = f"q_{story_id}_{idx}"

            if quiz_submitted:
                user_ans = st.session_state.quiz_answers.get(key)
                correct_ans = q["answer"]
                is_correct = user_ans == correct_ans

                if is_correct:
                    st.markdown(f"""
                    <div class="correct-answer">
                        <strong style="font-size:1.2rem;">Q{idx+1}: {q['q']}</strong><br><br>
                        ✅ <strong>{q['options'][user_ans]}</strong> — Great job!
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    user_answer_text = q["options"][user_ans] if user_ans is not None else "No answer"
                    st.markdown(f"""
                    <div class="wrong-answer">
                        <strong style="font-size:1.2rem;">Q{idx+1}: {q['q']}</strong><br><br>
                        ❌ You said: <strong>{user_answer_text}</strong><br>
                        ✅ Answer: <strong>{q['options'][correct_ans]}</strong>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="quiz-question">Q{idx+1}: {q["q"]}</div>', unsafe_allow_html=True)
                answer = st.radio(
                    "Pick one:",
                    options=range(len(q["options"])),
                    format_func=lambda x, opts=q["options"]: opts[x],
                    key=key,
                    label_visibility="collapsed",
                )
                st.session_state.quiz_answers[key] = answer
                st.markdown("")

        st.markdown("")

        if not quiz_submitted:
            col_back, col_submit, _ = st.columns([1, 2, 1])
            with col_back:
                if st.button("⬅️ Re-read Story", key="back_to_pages", width="stretch"):
                    st.session_state.story_page_idx = 0
                    st.rerun()
            with col_submit:
                if st.button("✅ Submit Answers!", key="submit_quiz", width="stretch", type="primary"):
                    st.session_state.quiz_submitted = True

                    correct = sum(
                        1 for i, q in enumerate(questions)
                        if st.session_state.quiz_answers.get(f"q_{story_id}_{i}") == q["answer"]
                    )
                    total = len(questions)
                    score_pct = int((correct / total) * 100) if total > 0 else 0
                    time_spent = int(time.time() - st.session_state.reading_start_time) if st.session_state.reading_start_time else 0

                    if user:
                        db.save_reading_progress(user["id"], story_id, story["title"], total, correct, time_spent)
                        db.save_activity_score(user["id"], "Reading", story["title"], score_pct, 100, f"{correct}/{total} correct", time_spent)

                    st.rerun()
        else:
            # Results summary
            correct = sum(
                1 for i, q in enumerate(questions)
                if st.session_state.quiz_answers.get(f"q_{story_id}_{i}") == q["answer"]
            )
            total = len(questions)
            score_pct = int((correct / total) * 100) if total > 0 else 0
            time_spent = int(time.time() - st.session_state.reading_start_time) if st.session_state.reading_start_time else 0
            minutes, seconds = divmod(time_spent, 60)

            if score_pct == 100:
                res_emoji, message, res_color = "🏆", "Perfect! You are a superstar reader!", "#10b981"
            elif score_pct >= 75:
                res_emoji, message, res_color = "🌟", "Great job! Almost perfect!", "#3b82f6"
            elif score_pct >= 50:
                res_emoji, message, res_color = "👍", "Good try! Keep reading!", "#f59e0b"
            else:
                res_emoji, message, res_color = "💪", "Let's read it again! You can do it!", "#ef4444"

            st.markdown(f"""
            <div style="text-align:center;padding:2rem;background:{res_color}10;border-radius:20px;border:3px solid {res_color};margin-top:1rem;">
                <div style="font-size:5rem;">{res_emoji}</div>
                <h2 style="color:{res_color};margin:0.5rem 0;font-size:2rem;">{correct} out of {total} correct!</h2>
                <p style="font-size:1.2rem;color:#4b5563;">{message}</p>
                <p style="color:#9ca3af;">⏱️ Time: {minutes}m {seconds}s</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("")
            col_r1, col_r2, col_r3 = st.columns(3)
            with col_r1:
                if st.button("📖 Read Again", key="read_again", width="stretch"):
                    start_story(story_id)
                    st.rerun()
            with col_r2:
                if st.button("📚 More Books", key="more_stories", width="stretch", type="primary"):
                    if is_arjun_story:
                        back_to_arjun_stories()
                    else:
                        back_to_reading_home()
                    st.rerun()
            with col_r3:
                if st.button("🏠 Dashboard", key="go_dashboard", width="stretch"):
                    st.session_state.current_page = "user_dashboard"
                    st.session_state.reading_state = None
                    st.session_state.quiz_answers = {}
                    st.session_state.quiz_submitted = False
                    st.session_state.story_page_idx = 0
                    st.rerun()


# ──────────────────────────────────────────────
# PAGE: Math Home — Level Selection
# ──────────────────────────────────────────────
def render_math_home():
    name = st.session_state.selected_user
    user = db.get_user(name)

    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Back", key="math_back_to_dash"):
            st.session_state.current_page = "user_dashboard"
            st.session_state.selected_activity = None
            st.rerun()

    st.markdown(f"""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <h1 style="font-size: 2.5rem;">🧮 {name}'s Math Practice</h1>
        <p style="color: #6b7280; font-size: 1.1rem;">Pick a level and start practicing!</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats
    today_math = []
    if user:
        today_math = db.get_today_scores(user["id"], activity_type="Math")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="score-card"><div class="score-number">🧮 {len(today_math)}</div><div class="score-label">Rounds Today</div></div>', unsafe_allow_html=True)
    with col2:
        if today_math:
            avg_pct = sum(s["score"] for s in today_math) / len(today_math)
            avg_display = f"{avg_pct:.0f}%"
        else:
            avg_display = "—"
        st.markdown(f'<div class="score-card"><div class="score-number">🎯 {avg_display}</div><div class="score-label">Avg Score Today</div></div>', unsafe_allow_html=True)
    with col3:
        total_math = db.get_scores_history(user["id"], activity_type="Math", days=365) if user else []
        st.markdown(f'<div class="score-card"><div class="score-number">⭐ {len(total_math)}</div><div class="score-label">Total Rounds</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # Level cards
    levels = mc.get_all_levels()
    cols = st.columns(3, gap="large")

    for i, level in enumerate(levels):
        with cols[i]:
            color = level["color"]
            st.markdown(f"""
            <div class="math-level-card" style="background: linear-gradient(135deg, {color}, {color}cc);">
                <div style="font-size: 2.8rem;">{level['emoji']}</div>
                <div style="font-size: 1.15rem; font-weight: 700; color: white; margin-top: 0.4rem; text-shadow: 1px 1px 3px rgba(0,0,0,0.3);">
                    {level['title']}
                </div>
                <div style="font-size: 0.85rem; color: rgba(255,255,255,0.9); margin-top: 0.2rem;">
                    {level['description']}
                </div>
                <div style="font-size: 0.75rem; color: rgba(255,255,255,0.75); margin-top: 0.2rem;">
                    5 questions per round
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button(f"▶️ Play {level['title']}", key=f"math_{level['id']}", width="stretch", type="primary"):
                start_math_level(level["id"])
                st.rerun()
            st.markdown("")


# ──────────────────────────────────────────────
# PAGE: Math Practice — Solve Problems
# ──────────────────────────────────────────────
def render_math_practice():
    name = st.session_state.selected_user
    user = db.get_user(name)
    level_id = st.session_state.math_level
    level = mc.get_level(level_id)
    problems = st.session_state.math_problems
    current = st.session_state.math_current
    total = len(problems)
    color = level["color"] if level else "#667eea"
    is_done = current >= total

    # Nav bar
    col_nav1, col_nav_mid, _ = st.columns([1, 4, 1])
    with col_nav1:
        if st.button("← Levels", key="math_back_levels"):
            back_to_math_home()
            st.rerun()
    with col_nav_mid:
        if not is_done:
            st.markdown(f"""
            <div style="text-align:center; color:#6b7280; font-size:0.9rem; padding-top:0.5rem;">
                Question {current + 1} of {total}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center; color:#6b7280; font-size:0.9rem; padding-top:0.5rem;">
                🎉 Round Complete!
            </div>
            """, unsafe_allow_html=True)

    # Title
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 0.5rem;">
        <h1 style="color: {color}; margin: 0.3rem 0; font-size: 2.2rem;">{level['emoji']} {level['title']}</h1>
    </div>
    """, unsafe_allow_html=True)

    # Progress bar
    progress = (current / total) if total > 0 else 0
    st.markdown(f"""
    <div style="background:#e5e7eb;border-radius:10px;height:10px;overflow:hidden;margin:0 0 1.5rem 0;">
        <div style="width:{progress*100:.0f}%;height:100%;background:linear-gradient(90deg,{color},{color}bb);border-radius:10px;transition:width 0.4s ease;"></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Active problem ──
    if not is_done:
        problem = problems[current]

        # Show the visual emoji display
        st.markdown(f"""
        <div class="math-problem-box">
            {problem['display_html']}
        </div>
        """, unsafe_allow_html=True)

        # Question text
        st.markdown(f'<div class="math-question-text" style="text-align:center;margin:1rem 0;">{problem["question"]}</div>', unsafe_allow_html=True)

        # Check if this question was just answered (for feedback)
        last_feedback = st.session_state.get("math_last_feedback")

        if last_feedback and last_feedback["idx"] == current:
            if last_feedback["correct"]:
                st.markdown("""
                <style>
                @keyframes float-up {
                    0%   { transform: translateY(0) scale(1) rotate(0deg); opacity: 1; }
                    70%  { transform: translateY(-350px) scale(1.1) rotate(10deg); opacity: 1; }
                    85%  { transform: translateY(-420px) scale(2.2) rotate(-5deg); opacity: 1; }
                    100% { transform: translateY(-440px) scale(3.0) rotate(0deg); opacity: 0; }
                }
                .celebration-container {
                    position: fixed;
                    bottom: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    pointer-events: none;
                    z-index: 9999;
                    overflow: hidden;
                }
                .celebration-item {
                    position: absolute;
                    bottom: -80px;
                    font-size: 3.5rem;
                    animation: float-up 4s ease-out forwards;
                }
                </style>
                <div class="celebration-container">
                    <span class="celebration-item" style="left:5%;  animation-delay:0s;">🎈</span>
                    <span class="celebration-item" style="left:15%; animation-delay:0.3s;">🎉</span>
                    <span class="celebration-item" style="left:25%; animation-delay:0.1s;">🎊</span>
                    <span class="celebration-item" style="left:35%; animation-delay:0.5s;">🎈</span>
                    <span class="celebration-item" style="left:45%; animation-delay:0.2s;">🥳</span>
                    <span class="celebration-item" style="left:55%; animation-delay:0.6s;">🎉</span>
                    <span class="celebration-item" style="left:65%; animation-delay:0.15s;">🎈</span>
                    <span class="celebration-item" style="left:75%; animation-delay:0.4s;">🎊</span>
                    <span class="celebration-item" style="left:85%; animation-delay:0.35s;">🎈</span>
                    <span class="celebration-item" style="left:95%; animation-delay:0.55s;">🎉</span>
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div class="correct-answer" style="text-align:center;">
                    ✅ <strong>Correct!</strong> The answer is <strong>{last_feedback['correct_val']}</strong>  🎉
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="wrong-answer" style="text-align:center;">
                    Not quite! You picked <strong>{last_feedback['picked']}</strong>.
                    The answer is <strong>{last_feedback['correct_val']}</strong> 💪
                </div>
                """, unsafe_allow_html=True)

            st.markdown("")
            _, col_next, _ = st.columns([1, 2, 1])
            with col_next:
                if current < total - 1:
                    if st.button("Next Question ➡️", key="math_next", width="stretch", type="primary"):
                        st.session_state.math_current += 1
                        st.session_state.math_last_feedback = None
                        st.rerun()
                else:
                    if st.button("🎉 See Results!", key="math_results", width="stretch", type="primary"):
                        st.session_state.math_current = total
                        st.session_state.math_last_feedback = None
                        st.rerun()
        else:
            # Show answer buttons
            answer_cols = st.columns(3, gap="medium")
            for i, opt in enumerate(problem["options"]):
                with answer_cols[i]:
                    if st.button(str(opt), key=f"math_opt_{current}_{i}", width="stretch", type="primary"):
                        is_correct = (i == problem["answer"])
                        st.session_state.math_answers.append({
                            "picked": opt,
                            "correct_val": problem["options"][problem["answer"]],
                            "correct": is_correct,
                        })
                        st.session_state.math_last_feedback = {
                            "idx": current,
                            "picked": opt,
                            "correct_val": problem["options"][problem["answer"]],
                            "correct": is_correct,
                        }
                        st.rerun()

    # ── Score summary ──
    else:
        answers = st.session_state.math_answers
        correct = sum(1 for a in answers if a["correct"])
        score_pct = int((correct / total) * 100) if total > 0 else 0
        time_spent = int(time.time() - st.session_state.math_start_time) if st.session_state.math_start_time else 0
        minutes, seconds = divmod(time_spent, 60)

        # Save score
        if user and level:
            db.save_activity_score(user["id"], "Math", level["title"], score_pct, 100, f"{correct}/{total} correct", time_spent)

        if score_pct == 100:
            res_emoji, message, res_color = "🏆", "Perfect! You are a math superstar!", "#10b981"
        elif score_pct >= 80:
            res_emoji, message, res_color = "🌟", "Great job! Almost perfect!", "#3b82f6"
        elif score_pct >= 60:
            res_emoji, message, res_color = "👍", "Good try! Keep practicing!", "#f59e0b"
        else:
            res_emoji, message, res_color = "💪", "Let's try again! You can do it!", "#ef4444"

        st.markdown(f"""
        <div style="text-align:center;padding:2rem;background:{res_color}10;border-radius:20px;border:3px solid {res_color};margin-top:1rem;">
            <div style="font-size:5rem;">{res_emoji}</div>
            <h2 style="color:{res_color};margin:0.5rem 0;font-size:2rem;">{correct} out of {total} correct!</h2>
            <p style="font-size:1.2rem;color:#4b5563;">{message}</p>
            <p style="color:#9ca3af;">⏱️ Time: {minutes}m {seconds}s</p>
        </div>
        """, unsafe_allow_html=True)

        # Review answers
        st.markdown("")
        st.markdown("### Review")
        for idx, (prob, ans) in enumerate(zip(problems, answers)):
            if ans["correct"]:
                st.markdown(f"""
                <div class="correct-answer">
                    <strong>Q{idx+1}:</strong> {prob['question']}<br>
                    ✅ <strong>{ans['correct_val']}</strong> — Great job!
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="wrong-answer">
                    <strong>Q{idx+1}:</strong> {prob['question']}<br>
                    ❌ You said: <strong>{ans['picked']}</strong> &nbsp; ✅ Answer: <strong>{ans['correct_val']}</strong>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("")
        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            if st.button(f"🔄 Play {level['title']} Again", key="math_again", width="stretch"):
                start_math_level(level_id)
                st.rerun()
        with col_r2:
            if st.button("🧮 More Levels", key="math_more", width="stretch", type="primary"):
                back_to_math_home()
                st.rerun()
        with col_r3:
            if st.button("🏠 Dashboard", key="math_dashboard", width="stretch"):
                st.session_state.current_page = "user_dashboard"
                st.session_state.math_level = None
                st.session_state.math_problems = []
                st.session_state.math_current = 0
                st.session_state.math_answers = []
                st.rerun()


# ──────────────────────────────────────────────
# PAGE: Generate a New Story with AI
# ──────────────────────────────────────────────
def render_generate_story():
    name = st.session_state.selected_user

    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Books", key="back_to_books_gen"):
            back_to_reading_home()
            st.rerun()

    st.markdown("""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <h1 style="font-size: 2.5rem;">✨ Create a New Story</h1>
        <p style="color: #6b7280; font-size: 1.1rem;">Tell us a topic and AI will write a picture book for you!</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    topic = st.text_input(
        "What should the story be about?",
        placeholder="e.g. a bunny learns to share, a kitten goes to school, a dinosaur makes friends",
        key="gen_topic",
    )

    col1, col2, _ = st.columns([2, 2, 3])
    with col1:
        generate_clicked = st.button(
            "✨ Generate Story",
            key="btn_do_generate",
            width="stretch",
            type="primary",
            disabled=(not topic),
        )
    with col2:
        if st.button("← Cancel", key="btn_cancel_gen", width="stretch"):
            back_to_reading_home()
            st.rerun()

    if generate_clicked and topic:
        import story_context
        import generate_images as gen_img

        with st.status("Creating your story...", expanded=True) as status:
            # Step 1: Generate story text via LLM
            st.write("📝 Writing the story...")
            try:
                story = story_context.generate_story_from_topic(topic, _HF_TOKEN)
            except Exception as exc:
                status.update(label="Story generation failed", state="error")
                st.error(f"Could not generate story: {exc}")
                return

            st.write(f"📖 **{story['title']}** — {len(story['pages'])} pages, {len(story['questions'])} questions")

            # Step 2: Save story JSON
            st.write("💾 Saving story...")
            rc.save_generated_story(story)

            # Step 3: Generate illustrations
            st.write("🎨 Drawing illustrations...")
            progress_bar = st.progress(0)

            def _update_progress(page_num, total, msg):
                progress_bar.progress(page_num / total, text=msg)

            gen, skip, fail = gen_img.generate_images_for_story(
                story, _HF_TOKEN, progress_callback=_update_progress
            )

            progress_bar.progress(1.0, text="All illustrations done!")

            st.write(f"✅ Created {gen} illustrations" + (f" ({fail} failed)" if fail else ""))
            status.update(label="Story created!", state="complete")

        st.markdown("")
        st.success(f"**{story['title']}** is ready to read!")

        col_r1, col_r2, _ = st.columns([2, 2, 3])
        with col_r1:
            if st.button(f"📖 Read: {story['title']}", key="read_new_story", width="stretch", type="primary"):
                start_story(story["id"])
                st.rerun()
        with col_r2:
            if st.button("📚 Back to Books", key="back_books_after_gen", width="stretch"):
                back_to_reading_home()
                st.rerun()

    # Show some example topics for inspiration
    if not generate_clicked:
        st.markdown("")
        st.markdown("### 💡 Need ideas? Try one of these:")
        idea_cols = st.columns(3, gap="medium")
        ideas = [
            ("🐰", "A bunny learns to share"),
            ("🦕", "A friendly dinosaur"),
            ("🚀", "A trip to the moon"),
            ("🐱", "A kitten's first day at school"),
            ("🌻", "A seed that grows into a flower"),
            ("🐢", "A slow turtle wins a race"),
        ]
        for idx, (emoji, idea) in enumerate(ideas):
            with idea_cols[idx % 3]:
                st.markdown(f"""
                <div style="background:#f8f9ff;border-radius:12px;padding:1rem;text-align:center;margin-bottom:0.5rem;">
                    <div style="font-size:2rem;">{emoji}</div>
                    <div style="color:#4b5563;font-size:0.9rem;">{idea}</div>
                </div>
                """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# PAGE: Arjun's Factual Stories Home
# ──────────────────────────────────────────────
def render_arjun_stories_home():
    import arjun_story_context as asc
    import reading_content as rc

    name = st.session_state.selected_user
    user = db.get_user(name)

    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Back", key="arjun_stories_back"):
            st.session_state.current_page = "user_dashboard"
            st.session_state.selected_activity = None
            st.rerun()

    st.markdown("""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <h1 style="font-size: 2.5rem;">📖 Factual Stories</h1>
        <p style="color: #6b7280; font-size: 1.1rem;">Real events, real learning — pick a topic and dive in!</p>
    </div>
    """, unsafe_allow_html=True)

    if not _CAN_GK:
        st.warning("Story generation requires an XAI_API_KEY. Please set it in `.streamlit/secrets.toml` or as an environment variable.")
        return

    # ── Previously read stories ──
    generated = rc._load_generated_stories()
    arjun_stories = {k: v for k, v in generated.items() if k.startswith("gen_arjun_")}

    if arjun_stories:
        st.markdown("### 📚 Your Stories")
        story_cols = st.columns(min(len(arjun_stories), 4), gap="medium")
        for idx, (sid, story) in enumerate(sorted(arjun_stories.items(), reverse=True)):
            with story_cols[idx % min(len(arjun_stories), 4)]:
                cat = story.get("topic_category", "General")
                cat_emoji = asc.TOPIC_EMOJIS.get(cat, "📖")
                color = story.get("color", "#6366f1")
                st.markdown(f"""
                <div class="score-card" style="border-top: 4px solid {color};text-align:center;padding:1rem;">
                    <div style="font-size:2.5rem;">{story.get('cover_emoji', '📖')}</div>
                    <h4 style="margin:0.3rem 0;font-size:0.95rem;">{story['title']}</h4>
                    <p style="color:#9ca3af;font-size:0.75rem;margin:0;">{cat_emoji} {cat}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"📖 Read", key=f"read_{sid}", width="stretch"):
                    start_story(sid)
                    st.rerun()
        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # ── Topic picker ──
    st.markdown("### ✨ Generate a New Story")
    st.markdown('<p style="color:#6b7280;">Topics are fetched live from the web — always fresh and trending!</p>', unsafe_allow_html=True)

    # Top action row
    col_random, col_custom = st.columns(2, gap="medium")
    with col_random:
        if st.button("🎲 Surprise Me — Random Topic!", key="arjun_random_topic", width="stretch", type="primary"):
            cat, topic = asc.get_random_topic()
            _generate_and_launch_arjun_story(topic, user)
            return

    st.markdown("")

    # ── Write your own topic ──
    with st.expander("✏️ Write Your Own Topic", expanded=False):
        custom_topic = st.text_input(
            "What real-world topic should the story be about?",
            placeholder="e.g. Winter Olympics 2026, Mars Rover, The Panama Canal",
            key="arjun_custom_topic",
        )
        col_gen_custom, _ = st.columns([2, 3])
        with col_gen_custom:
            if st.button("✨ Generate Story", key="arjun_gen_custom", width="stretch", type="primary", disabled=(not custom_topic)):
                _generate_and_launch_arjun_story(custom_topic, user)
                return

    st.markdown("")

    # ── Trending topics (fetched from the web) ──
    if "arjun_trending_topics" not in st.session_state:
        st.session_state.arjun_trending_topics = None
    if "arjun_topics_fetched_at" not in st.session_state:
        st.session_state.arjun_topics_fetched_at = None

    _cat_colors = {
        "Science": "#6366f1",
        "Social Science": "#8b5cf6",
        "Places": "#0ea5e9",
        "Sports": "#10b981",
        "Events": "#f59e0b",
        "Current Events": "#ef4444",
    }

    if st.session_state.arjun_trending_topics is None:
        if st.button("🌐 Load Trending Story Ideas from the Web", key="load_trending_topics", width="stretch", type="primary"):
            with st.spinner("Searching the web for trending, kid-friendly story ideas..."):
                try:
                    topics = asc.fetch_trending_topics(_XAI_API_KEY)
                    st.session_state.arjun_trending_topics = topics
                    st.session_state.arjun_topics_fetched_at = datetime.now().strftime("%I:%M %p")
                except Exception as e:
                    st.error(f"Could not fetch trending topics: {e}")
                    st.session_state.arjun_trending_topics = asc.get_all_topics()
                    st.session_state.arjun_topics_fetched_at = "fallback"
                st.rerun()
        st.markdown("""
        <div style="text-align:center;padding:2rem;color:#9ca3af;">
            <div style="font-size:3rem;">🌐</div>
            <p>Click the button above to search the web for today's trending story topics!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        all_topics = st.session_state.arjun_trending_topics

        col_refresh, col_info = st.columns([2, 5])
        with col_refresh:
            if st.button("🔄 Refresh Topics", key="refresh_trending"):
                st.session_state.arjun_trending_topics = None
                st.session_state.arjun_topics_fetched_at = None
                st.rerun()
        with col_info:
            fetched_at = st.session_state.arjun_topics_fetched_at or ""
            if fetched_at and fetched_at != "fallback":
                st.caption(f"Fetched at {fetched_at} — live from the web")

        tab_labels = [f"{asc.TOPIC_EMOJIS.get(cat, '📖')} {cat}" for cat in all_topics]
        tabs = st.tabs(tab_labels)

        for tab, (category, topics) in zip(tabs, all_topics.items()):
            with tab:
                cat_color = _cat_colors.get(category, "#6366f1")
                topic_cols = st.columns(2, gap="medium")
                for idx, topic in enumerate(topics):
                    with topic_cols[idx % 2]:
                        short_title = topic.split("—")[0].strip() if "—" in topic else topic
                        subtitle = topic.split("—")[1].strip() if "—" in topic else ""
                        st.markdown(f"""
                        <div style="background:#f8f9ff;border-radius:12px;padding:0.8rem 1rem;
                                    margin-bottom:0.5rem;border-left:4px solid {cat_color};">
                            <div style="font-weight:600;font-size:0.95rem;color:#1f2937;">{short_title}</div>
                            {"<div style='color:#6b7280;font-size:0.8rem;'>" + subtitle + "</div>" if subtitle else ""}
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button("📝 Generate", key=f"gen_{category}_{idx}", width="stretch"):
                            _generate_and_launch_arjun_story(topic, user)
                            return


def _generate_and_launch_arjun_story(topic: str, user):
    """Generate a story for Arjun, save it, and navigate to reading it."""
    import arjun_story_context as asc
    import reading_content as rc

    with st.status("Creating your story...", expanded=True) as status:
        st.write(f"📝 Writing a story about: **{topic}**")
        try:
            story = asc.generate_arjun_story(_XAI_API_KEY, topic=topic)
        except Exception as exc:
            status.update(label="Story generation failed", state="error")
            st.error(f"Could not generate story: {exc}")
            return

        st.write(f"📖 **{story['title']}** — {len(story['pages'])} pages, {len(story['questions'])} questions")

        st.write("💾 Saving story...")
        rc.save_generated_story(story)

        # Generate illustrations if HF token available
        if _CAN_GENERATE:
            import generate_images as gen_img
            st.write("🎨 Drawing illustrations...")
            progress_bar = st.progress(0)

            def _update_progress(page_num, total, msg):
                progress_bar.progress(page_num / total, text=msg)

            gen, skip, fail = gen_img.generate_images_for_story(
                story, _HF_TOKEN, progress_callback=_update_progress
            )
            progress_bar.progress(1.0, text="All illustrations done!")
            st.write(f"✅ Created {gen} illustrations" + (f" ({fail} failed)" if fail else ""))
        else:
            st.write("🖼️ Illustrations will use emoji fallbacks (set HF_TOKEN for AI images)")

        status.update(label="Story created!", state="complete")

    # Save the generated story ID so it survives reruns
    st.session_state.arjun_last_story_id = story["id"]
    st.session_state.arjun_last_story_title = story["title"]

    # Navigate directly to the story
    start_story(story["id"])
    st.rerun()


# ──────────────────────────────────────────────
# PAGE: GK Home — Today's Progress
# ──────────────────────────────────────────────
def render_gk_home():
    import json as _json
    import gk_content as gk

    name = st.session_state.selected_user
    user = db.get_user(name)
    profile = gk.get_profile(name)

    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Back", key="gk_back_to_dash"):
            st.session_state.current_page = "user_dashboard"
            st.session_state.selected_activity = None
            st.rerun()

    st.markdown(f"""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <h1 style="font-size: 2.5rem;">🧠 {name}'s General Knowledge</h1>
        <p style="color: #6b7280; font-size: 1.1rem;">{profile['subtitle']}</p>
    </div>
    """, unsafe_allow_html=True)

    today = datetime.now().strftime("%Y-%m-%d")
    today_gk = db.get_today_scores(user["id"], activity_type="GK") if user else []
    total_gk = db.get_scores_history(user["id"], activity_type="GK", days=365) if user else []

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="score-card"><div class="score-number">📅 {today}</div><div class="score-label">Today\'s Date</div></div>', unsafe_allow_html=True)
    with col2:
        if today_gk:
            best = max(s["score"] for s in today_gk)
            st.markdown(f'<div class="score-card"><div class="score-number">🎯 {best}%</div><div class="score-label">Today\'s Best Score</div></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="score-card"><div class="score-number">🎯 —</div><div class="score-label">Today\'s Score</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="score-card"><div class="score-number">⭐ {len(total_gk)}</div><div class="score-label">Total Quizzes</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    if not _CAN_GK:
        st.warning("GK quiz requires an XAI_API_KEY. Please set it in `.streamlit/secrets.toml` or as an environment variable.")
        return

    # Check for cached questions (last set generated today)
    cached_json = db.get_daily_questions(user["id"], today) if user else None

    if today_gk:
        best = max(s["score"] for s in today_gk)
        st.markdown(f"""
        <div style="text-align:center; padding:1rem; background:#d1fae5; border-radius:16px; border:2px solid #10b981; margin-bottom:1rem;">
            <span style="font-size:2rem;">🎉</span>
            <p style="margin:0.3rem 0; font-size:1.1rem; color:#065f46;">
                <strong>{len(today_gk)} quiz{'zes' if len(today_gk) > 1 else ''} completed today!</strong>
                &nbsp; Best score: <strong>{best}%</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

    gk_heading = "Ready for another round?" if today_gk else "Ready for today's quiz?"
    st.markdown(f"""
    <div style="text-align:center; padding:1.5rem;">
        <div style="font-size: 4rem;">🧠</div>
        <h3 style="margin: 0.5rem 0;">{gk_heading}</h3>
        <p style="color: #6b7280;">{profile['quiz_description']}</p>
    </div>
    """, unsafe_allow_html=True)

    new_quiz = False
    if today_gk and cached_json:
        col_new, col_review = st.columns(2, gap="medium")
        with col_new:
            new_quiz = st.button("🚀 New Quiz", key="gk_new", width="stretch", type="primary")
        with col_review:
            if st.button("📝 Review Last Quiz", key="gk_review", width="stretch"):
                questions = _json.loads(cached_json)
                start_gk_quiz(questions)
                st.rerun()
    else:
        _, col_btn, _ = st.columns([1, 2, 1])
        with col_btn:
            btn_label = "🚀 New Quiz" if today_gk else "🚀 Start Today's Quiz"
            new_quiz = st.button(btn_label, key="gk_start", width="stretch", type="primary")

    if new_quiz:
        with st.spinner("Generating fresh questions..."):
            try:
                past_qs = db.get_recent_gk_questions(user["id"], limit=100) if user else []
                questions = gk.generate_daily_questions(
                    _XAI_API_KEY, user_name=name, past_questions=past_qs,
                )
                db.save_daily_questions(user["id"], today, _json.dumps(questions))
            except Exception as exc:
                st.error(f"Could not generate questions: {exc}")
                return
        start_gk_quiz(questions)
        st.rerun()


# ──────────────────────────────────────────────
# PAGE: GK Practice — Question by Question
# ──────────────────────────────────────────────
def render_gk_practice():
    import gk_content as gk

    name = st.session_state.selected_user
    user = db.get_user(name)
    profile = gk.get_profile(name)
    gk_color = profile["color"]
    questions = st.session_state.gk_questions
    current = st.session_state.gk_current
    total = len(questions)
    is_done = current >= total

    # Nav bar
    col_nav1, col_nav_mid, _ = st.columns([1, 4, 1])
    with col_nav1:
        if st.button("← GK Home", key="gk_back_home"):
            back_to_gk_home()
            st.rerun()
    with col_nav_mid:
        if not is_done:
            st.markdown(f"""
            <div style="text-align:center; color:#6b7280; font-size:0.9rem; padding-top:0.5rem;">
                Question {current + 1} of {total}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center; color:#6b7280; font-size:0.9rem; padding-top:0.5rem;">
                🎉 Quiz Complete!
            </div>
            """, unsafe_allow_html=True)

    # Title
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 0.5rem;">
        <h1 style="color: {gk_color}; margin: 0.3rem 0; font-size: 2.2rem;">🧠 General Knowledge Quiz</h1>
    </div>
    """, unsafe_allow_html=True)

    # Progress bar
    progress = (current / total) if total > 0 else 0
    st.markdown(f"""
    <div style="background:#e5e7eb;border-radius:10px;height:10px;overflow:hidden;margin:0 0 1.5rem 0;">
        <div style="width:{progress*100:.0f}%;height:100%;background:linear-gradient(90deg,{gk_color},{gk_color}bb);border-radius:10px;transition:width 0.4s ease;"></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Active question ──
    if not is_done:
        q = questions[current]
        topic_emoji_map = profile.get("topic_emojis", {})
        topic_emoji = topic_emoji_map.get(q.get("topic", ""), "📚")

        st.markdown(f"""
        <div class="gk-question-box">
            <span class="gk-topic-badge">{topic_emoji} {q.get('topic', 'General')}</span>
            <div class="gk-question-text" style="margin-top:0.8rem;">{q['question']}</div>
        </div>
        """, unsafe_allow_html=True)

        # Check if this question was just answered
        last_feedback = st.session_state.get("gk_last_feedback")

        if last_feedback and last_feedback["idx"] == current:
            if last_feedback["correct"]:
                st.markdown(f"""
                <div class="correct-answer" style="text-align:center;">
                    ✅ <strong>Correct!</strong> 🎉
                    <br><br><em>{q.get('explanation', '')}</em>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="wrong-answer" style="text-align:center;">
                    Not quite! You picked <strong>{last_feedback['picked']}</strong>.
                    <br>The answer is <strong>{last_feedback['correct_val']}</strong> 💪
                    <br><br><em>{q.get('explanation', '')}</em>
                </div>
                """, unsafe_allow_html=True)

            # Show map with location marker (for profiles with has_map)
            # Supports India maps (Sangeetha) and US maps (Rakesh)
            if profile.get("has_map") and q.get("location"):
                map_country = profile.get("map_country", "india")

                if map_country == "us":
                    import us_map_data as country_map
                    import us_state_map_data as country_smap
                    country_flag = "🇺🇸"
                    country_label = "United States"
                else:
                    import india_map_data as country_map
                    import state_map_data as country_smap
                    country_flag = "🇮🇳"
                    country_label = "India"

                overview_html = country_map.render_map_with_marker(q["location"])

                state_name = country_smap.infer_state(q)
                state_html = country_smap.render_state_map_with_marker(
                    state_name, q["location"]
                ) if state_name else None

                if overview_html and state_html:
                    col_country, col_state = st.columns(2)
                    with col_country:
                        st.markdown(
                            f'<p style="text-align:center;font-weight:600;color:#6b7280;'
                            f'margin-bottom:0.3rem;font-size:0.85rem;">{country_flag} {country_label}</p>',
                            unsafe_allow_html=True,
                        )
                        st.markdown(overview_html, unsafe_allow_html=True)
                    with col_state:
                        st.markdown(
                            f'<p style="text-align:center;font-weight:600;color:#6b7280;'
                            f'margin-bottom:0.3rem;font-size:0.85rem;">🔍 {state_name}</p>',
                            unsafe_allow_html=True,
                        )
                        st.markdown(state_html, unsafe_allow_html=True)
                elif overview_html:
                    st.markdown('<div style="text-align:center;margin:1rem 0;">', unsafe_allow_html=True)
                    st.markdown(overview_html, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("")
            _, col_next, _ = st.columns([1, 2, 1])
            with col_next:
                if current < total - 1:
                    if st.button("Next Question ➡️", key="gk_next", width="stretch", type="primary"):
                        st.session_state.gk_current += 1
                        st.session_state.gk_last_feedback = None
                        st.rerun()
                else:
                    if st.button("🎉 See Results!", key="gk_results", width="stretch", type="primary"):
                        st.session_state.gk_current = total
                        st.session_state.gk_last_feedback = None
                        st.rerun()
        else:
            # Answer buttons (2x2 grid)
            ans_col1, ans_col2 = st.columns(2, gap="medium")
            for i, opt in enumerate(q["options"]):
                col = ans_col1 if i % 2 == 0 else ans_col2
                with col:
                    label = f"{chr(65 + i)}. {opt}"
                    if st.button(label, key=f"gk_opt_{current}_{i}", width="stretch", type="primary"):
                        is_correct = (i == q["answer"])
                        st.session_state.gk_answers.append({
                            "picked": opt,
                            "correct_val": q["options"][q["answer"]],
                            "correct": is_correct,
                        })
                        st.session_state.gk_last_feedback = {
                            "idx": current,
                            "picked": opt,
                            "correct_val": q["options"][q["answer"]],
                            "correct": is_correct,
                        }
                        st.rerun()

            # ── Chat tutor section ──
            if _CAN_GK:
                st.markdown("")
                with st.expander("💬 Need a hint? Ask me!", expanded=False):
                    chat_key = f"chat_{current}"
                    if chat_key not in st.session_state.gk_chat_histories:
                        st.session_state.gk_chat_histories[chat_key] = []

                    chat_history = st.session_state.gk_chat_histories[chat_key]

                    for msg in chat_history:
                        if msg["role"] == "user":
                            st.chat_message("user").write(msg["content"])
                        else:
                            st.chat_message("assistant").write(msg["content"])

                    user_input = st.chat_input("Ask for a hint...", key=f"gk_chat_input_{current}")
                    if user_input:
                        chat_history.append({"role": "user", "content": user_input})
                        st.chat_message("user").write(user_input)

                        with st.spinner("Thinking..."):
                            try:
                                reply = gk.chat_with_tutor(q, user_input, chat_history[:-1], _XAI_API_KEY, user_name=name)
                            except Exception as exc:
                                reply = f"Oops, I had trouble thinking! Try again. ({exc})"

                        chat_history.append({"role": "assistant", "content": reply})
                        st.chat_message("assistant").write(reply)
                        st.session_state.gk_chat_histories[chat_key] = chat_history

    # ── Score summary ──
    else:
        answers = st.session_state.gk_answers
        correct = sum(1 for a in answers if a["correct"])
        score_pct = int((correct / total) * 100) if total > 0 else 0
        time_spent = int(time.time() - st.session_state.gk_start_time) if st.session_state.gk_start_time else 0
        minutes, seconds = divmod(time_spent, 60)

        if user:
            db.save_activity_score(user["id"], "GK", "Daily Quiz", score_pct, 100, f"{correct}/{total} correct", time_spent)

        if score_pct == 100:
            res_emoji, message, res_color = "🏆", "Perfect! You're a GK superstar!", "#10b981"
        elif score_pct >= 70:
            res_emoji, message, res_color = "🌟", "Great job! You know a lot!", "#3b82f6"
        elif score_pct >= 50:
            res_emoji, message, res_color = "👍", "Good try! You're learning every day!", "#f59e0b"
        else:
            res_emoji, message, res_color = "💪", "Keep going! Every day you learn more!", "#ef4444"

        st.markdown(f"""
        <div style="text-align:center;padding:2rem;background:{res_color}10;border-radius:20px;border:3px solid {res_color};margin-top:1rem;">
            <div style="font-size:5rem;">{res_emoji}</div>
            <h2 style="color:{res_color};margin:0.5rem 0;font-size:2rem;">{correct} out of {total} correct!</h2>
            <p style="font-size:1.2rem;color:#4b5563;">{message}</p>
            <p style="color:#9ca3af;">⏱️ Time: {minutes}m {seconds}s</p>
        </div>
        """, unsafe_allow_html=True)

        # Review answers
        st.markdown("")
        st.markdown("### Review")
        for idx, (q, ans) in enumerate(zip(questions, answers)):
            topic_label = q.get("topic", "")
            if ans["correct"]:
                st.markdown(f"""
                <div class="correct-answer">
                    <span class="gk-topic-badge">{topic_label}</span><br>
                    <strong>Q{idx+1}:</strong> {q['question']}<br>
                    ✅ <strong>{ans['correct_val']}</strong> — Great job!
                    <br><em style="color:#6b7280;">{q.get('explanation', '')}</em>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="wrong-answer">
                    <span class="gk-topic-badge">{topic_label}</span><br>
                    <strong>Q{idx+1}:</strong> {q['question']}<br>
                    ❌ You said: <strong>{ans['picked']}</strong> &nbsp; ✅ Answer: <strong>{ans['correct_val']}</strong>
                    <br><em style="color:#6b7280;">{q.get('explanation', '')}</em>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("")
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            if st.button("🧠 GK Home", key="gk_home_btn", width="stretch", type="primary"):
                back_to_gk_home()
                st.rerun()
        with col_r2:
            if st.button("🏠 Dashboard", key="gk_dashboard", width="stretch"):
                st.session_state.current_page = "user_dashboard"
                st.session_state.gk_questions = []
                st.session_state.gk_current = 0
                st.session_state.gk_answers = []
                st.session_state.gk_chat_histories = {}
                st.rerun()


# ──────────────────────────────────────────────
# PAGE: Sight Words Home — Pick a Level
# ──────────────────────────────────────────────
def render_sight_words_home():
    import sight_words_content as sw

    name = st.session_state.selected_user
    user = db.get_user(name)

    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Back", key="sw_back_to_dash"):
            st.session_state.current_page = "user_dashboard"
            st.session_state.selected_activity = None
            st.rerun()

    st.markdown(f"""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <h1 style="font-size: 2.5rem;">👁️ {name}'s Sight Words</h1>
        <p style="color: #6b7280; font-size: 1.1rem;">Learn to read words by sight — pick a level!</p>
    </div>
    """, unsafe_allow_html=True)

    today_sw = db.get_today_scores(user["id"], activity_type="SightWords") if user else []
    total_sw = db.get_scores_history(user["id"], activity_type="SightWords", days=365) if user else []

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div class="score-card"><div class="score-number">📅 {len(today_sw)}</div>'
            f'<div class="score-label">Rounds Today</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        if today_sw:
            avg_pct = sum(s["score"] for s in today_sw) / len(today_sw)
            st.markdown(
                f'<div class="score-card"><div class="score-number">🎯 {avg_pct:.0f}%</div>'
                f'<div class="score-label">Avg Score Today</div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="score-card"><div class="score-number">🎯 —</div>'
                '<div class="score-label">Avg Score Today</div></div>',
                unsafe_allow_html=True,
            )
    with col3:
        st.markdown(
            f'<div class="score-card"><div class="score-number">⭐ {len(total_sw)}</div>'
            f'<div class="score-label">Total Rounds</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    num_levels = len(sw.LEVELS)
    cols = st.columns(min(num_levels, 4), gap="large")
    for i, lvl in enumerate(sw.LEVELS):
        word_count = len(sw.WORD_BANK.get(lvl["id"], []))
        with cols[i % len(cols)]:
            st.markdown(f"""
            <div class="math-level-card" style="background: linear-gradient(135deg, {lvl['color']}, {lvl['color']}cc);">
                <div style="font-size: 2.8rem;">{lvl['emoji']}</div>
                <div style="font-size: 1.15rem; font-weight: 700; color: white; margin-top: 0.4rem;
                     text-shadow: 1px 1px 3px rgba(0,0,0,0.3);">
                    {lvl['title']}
                </div>
                <div style="font-size: 0.85rem; color: rgba(255,255,255,0.9); margin-top: 0.2rem;">
                    {lvl['subtitle']}
                </div>
                <div style="font-size: 0.75rem; color: rgba(255,255,255,0.75); margin-top: 0.2rem;">
                    {word_count} words · {lvl['words_per_round']} per round
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("")
            if st.button(
                f"▶️ Play {lvl['title']}", key=f"sw_{lvl['id']}",
                width="stretch", type="primary",
            ):
                start_sight_words(lvl["id"])
                st.rerun()
            st.markdown("")


# ──────────────────────────────────────────────
# PAGE: Sight Words Practice — Find the Word
# ──────────────────────────────────────────────
def render_sight_words_practice():
    import sight_words_content as sw

    name = st.session_state.selected_user
    user = db.get_user(name)
    level_id = st.session_state.sw_level
    level = sw.get_level(level_id)
    questions = st.session_state.sw_questions
    current = st.session_state.sw_current
    total = len(questions)
    color = level["color"] if level else "#f59e0b"
    is_done = current >= total

    col_nav1, col_nav_mid, _ = st.columns([1, 4, 1])
    with col_nav1:
        if st.button("← Levels", key="sw_back_levels"):
            back_to_sight_words_home()
            st.rerun()
    with col_nav_mid:
        if not is_done:
            st.markdown(f"""
            <div style="text-align:center; color:#6b7280; font-size:0.9rem; padding-top:0.5rem;">
                Word {current + 1} of {total}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center; color:#6b7280; font-size:0.9rem; padding-top:0.5rem;">
                🎉 All Done!
            </div>
            """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 0.5rem;">
        <h1 style="color: {color}; margin: 0.3rem 0; font-size: 2.2rem;">
            {level['emoji']} {level['title']} Sight Words
        </h1>
    </div>
    """, unsafe_allow_html=True)

    progress = (current / total) if total > 0 else 0
    st.markdown(f"""
    <div style="background:#e5e7eb;border-radius:10px;height:10px;overflow:hidden;margin:0 0 1.5rem 0;">
        <div style="width:{progress*100:.0f}%;height:100%;background:linear-gradient(90deg,{color},{color}bb);
             border-radius:10px;transition:width 0.4s ease;"></div>
    </div>
    """, unsafe_allow_html=True)

    if not is_done:
        q = questions[current]
        word_color = q["color"]

        st.markdown(f"""
        <div style="text-align:center; padding:2.5rem 1rem; background:linear-gradient(135deg, {word_color}15, {word_color}08);
             border-radius:28px; border:3px solid {word_color}40; margin-bottom:1.5rem;">
            <div style="font-size:3rem; margin-bottom:0.5rem;">{q['emoji']}</div>
            <div style="font-size:1.1rem; color:#6b7280; margin-bottom:0.5rem; font-weight:600;">
                Read this word:
            </div>
            <div style="font-size:5.5rem; font-weight:900; color:{word_color}; font-family:'Comic Sans MS','Chalkboard SE',
                 'Segoe Print',cursive; letter-spacing:0.15em; text-shadow:3px 3px 6px {word_color}30;
                 line-height:1.1; padding:0.5rem 0;">
                {q['word']}
            </div>
            <div style="font-size:1.15rem; color:#6b7280; margin-top:1rem; font-style:italic;">
                "{q['sentence']}"
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        _, col_next, _ = st.columns([1, 2, 1])
        with col_next:
            if current < total - 1:
                if st.button("Next Word ➡️", key="sw_next", width="stretch", type="primary"):
                    st.session_state.sw_current += 1
                    st.rerun()
            else:
                if st.button("🎉 All Done!", key="sw_done", width="stretch", type="primary"):
                    st.session_state.sw_current = total
                    st.rerun()

    else:
        time_spent = int(time.time() - st.session_state.sw_start_time) if st.session_state.sw_start_time else 0
        minutes, seconds = divmod(time_spent, 60)

        if user:
            lvl_title = level["title"] if level else "Sight Words"
            db.save_activity_score(
                user["id"], "SightWords", lvl_title,
                100, 100, f"{total} words practiced", time_spent,
            )

        _fn_css = (
            "<style>"
            "@keyframes fn-launch{"
            "0%{transform:translateY(0) scale(.6) rotate(0deg);opacity:0}"
            "10%{opacity:1}"
            "50%{transform:translateY(-55vh) scale(1.3) rotate(180deg);opacity:1}"
            "75%{transform:translateY(-70vh) scale(1.6) rotate(270deg);opacity:.9}"
            "90%{transform:translateY(-80vh) scale(2.2) rotate(340deg);opacity:.5}"
            "100%{transform:translateY(-90vh) scale(2.5) rotate(360deg);opacity:0}}"
            "@keyframes fn-rain{"
            "0%{transform:translateY(-100px) rotate(0deg);opacity:1}"
            "100%{transform:translateY(110vh) rotate(720deg);opacity:.3}}"
            ".fn-arena{position:fixed;top:0;left:0;width:100%;height:100%;"
            "pointer-events:none;z-index:9999;overflow:hidden}"
            ".fn-item{position:absolute;bottom:-60px;font-size:3.2rem;"
            "animation:fn-launch 3.5s ease-out forwards}"
            ".fn-drop{position:absolute;top:-80px;font-size:2.6rem;"
            "animation:fn-rain 4s linear forwards}"
            "</style>"
        )
        st.markdown(_fn_css, unsafe_allow_html=True)

        _fn_items = [
            ("fn-item", "3%",  "0s",     "3.5rem", "\U0001f349"),
            ("fn-item", "10%", "0.15s",  "2.8rem", "\U0001f388"),
            ("fn-item", "17%", "0.3s",   "3rem",   "\U0001f34e"),
            ("fn-item", "24%", "0.1s",   "3.5rem", "\U0001f34c"),
            ("fn-item", "31%", "0.45s",  "2.8rem", "\U0001f388"),
            ("fn-item", "38%", "0.2s",   "3.2rem", "\U0001f353"),
            ("fn-item", "45%", "0.5s",   "3.5rem", "\U0001f95d"),
            ("fn-item", "52%", "0.05s",  "3rem",   "\U0001f34a"),
            ("fn-item", "59%", "0.35s",  "2.8rem", "\U0001f388"),
            ("fn-item", "66%", "0.25s",  "3.5rem", "\U0001f347"),
            ("fn-item", "73%", "0.55s",  "3rem",   "\U0001f351"),
            ("fn-item", "80%", "0.4s",   "2.8rem", "\U0001f388"),
            ("fn-item", "87%", "0.12s",  "3.2rem", "\U0001fad0"),
            ("fn-item", "94%", "0.6s",   "3.5rem", "\U0001f352"),
            ("fn-drop", "5%",  "1.5s",   "2.5rem", "\U0001f349"),
            ("fn-drop", "15%", "1.8s",   "2rem",   "\U0001f388"),
            ("fn-drop", "25%", "2.0s",   "2.5rem", "\U0001f34e"),
            ("fn-drop", "35%", "1.6s",   "2.2rem", "\U0001f34c"),
            ("fn-drop", "45%", "2.2s",   "2.5rem", "\U0001f353"),
            ("fn-drop", "55%", "1.7s",   "2rem",   "\U0001f388"),
            ("fn-drop", "65%", "2.4s",   "2.5rem", "\U0001f95d"),
            ("fn-drop", "75%", "1.9s",   "2.2rem", "\U0001f34a"),
            ("fn-drop", "85%", "2.1s",   "2.5rem", "\U0001f347"),
            ("fn-drop", "95%", "2.3s",   "2rem",   "\U0001f388"),
        ]
        _fn_spans = "".join(
            f'<span class="{cls}" style="left:{l};animation-delay:{d};font-size:{s};">{e}</span>'
            for cls, l, d, s, e in _fn_items
        )
        st.markdown(f'<div class="fn-arena">{_fn_spans}</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div style="text-align:center; padding:2rem; background:#10b98110;
             border-radius:20px; border:3px solid #10b981; margin-top:1rem;">
            <div style="font-size:5rem;">🌟</div>
            <h2 style="color:#10b981; margin:0.5rem 0; font-size:2rem;">
                Great job, {name}!
            </h2>
            <p style="font-size:1.2rem; color:#4b5563;">
                You practiced <strong>{total} words</strong> today!
            </p>
            <p style="color:#9ca3af;">⏱️ Time: {minutes}m {seconds}s</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        st.markdown("### 📝 Words You Practiced")

        review_cols = st.columns(2, gap="medium")
        for idx, q in enumerate(questions):
            with review_cols[idx % 2]:
                st.markdown(f"""
                <div style="padding:0.8rem; border-radius:12px; background:#f0fdf4;
                     border-left:4px solid {q['color']}; margin-bottom:0.6rem;">
                    <span style="font-size:1.5rem;">{q['emoji']}</span>
                    <strong style="font-size:1.3rem; color:#065f46; margin-left:0.3rem;">{q['word']}</strong>
                    <span style="float:right; color:#6b7280; font-size:0.85rem; font-style:italic;">
                        {q['sentence']}
                    </span>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("")
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            if st.button("👁️ Sight Words Home", key="sw_home_btn", width="stretch", type="primary"):
                back_to_sight_words_home()
                st.rerun()
        with col_r2:
            if st.button("🏠 Dashboard", key="sw_dashboard", width="stretch"):
                st.session_state.current_page = "user_dashboard"
                st.session_state.sw_questions = []
                st.session_state.sw_current = 0
                st.session_state.sw_answers = []
                st.rerun()


# ──────────────────────────────────────────────
# PAGE: Map Explorer Home
# ──────────────────────────────────────────────
def render_map_explorer_home():
    import map_explorer_content as me

    name = st.session_state.selected_user
    user = db.get_user(name)

    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Back", key="me_back_to_dash"):
            st.session_state.current_page = "user_dashboard"
            st.session_state.selected_activity = None
            st.rerun()

    st.markdown(f"""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <h1 style="font-size: 2.5rem;">🗺️ {name}'s Map Explorer</h1>
        <p style="color: #6b7280; font-size: 1.1rem;">
            Explore the world — countries, landmarks, rivers, and more!
        </p>
    </div>
    """, unsafe_allow_html=True)

    today_me = db.get_today_scores(user["id"], activity_type="MapExplorer") if user else []
    total_me = db.get_scores_history(user["id"], activity_type="MapExplorer", days=365) if user else []

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div class="score-card"><div class="score-number">📅 {len(today_me)}</div>'
            f'<div class="score-label">Quizzes Today</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        if today_me:
            best = max(s["score"] for s in today_me)
            st.markdown(
                f'<div class="score-card"><div class="score-number">🎯 {best}%</div>'
                f'<div class="score-label">Today\'s Best</div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="score-card"><div class="score-number">🎯 —</div>'
                '<div class="score-label">Today\'s Best</div></div>',
                unsafe_allow_html=True,
            )
    with col3:
        st.markdown(
            f'<div class="score-card"><div class="score-number">⭐ {len(total_me)}</div>'
            f'<div class="score-label">Total Quizzes</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    if today_me:
        best = max(s["score"] for s in today_me)
        st.markdown(f"""
        <div style="text-align:center; padding:1rem; background:#dbeafe; border-radius:16px;
             border:2px solid #3b82f6; margin-bottom:1rem;">
            <span style="font-size:2rem;">🎉</span>
            <p style="margin:0.3rem 0; font-size:1.1rem; color:#1e40af;">
                <strong>{len(today_me)} quiz{'zes' if len(today_me) > 1 else ''} completed today!</strong>
                &nbsp; Best score: <strong>{best}%</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center; padding:1.5rem;">
        <div style="font-size: 4rem;">🌍</div>
        <h3 style="margin: 0.5rem 0;">{"Ready for another adventure?" if today_me else "Ready to explore the world?"}</h3>
        <p style="color: #6b7280;">
            10 questions about countries, landmarks, rivers, mountains, and more!
        </p>
    </div>
    """, unsafe_allow_html=True)

    category_choice = st.selectbox(
        "Focus on a category (optional)",
        ["All Categories"] + [
            f"{me.CATEGORIES[k]['emoji']} {me.CATEGORIES[k]['name']}"
            for k in me.CATEGORIES
        ],
        key="me_category_filter",
    )

    selected_cat = None
    if category_choice != "All Categories":
        for k, v in me.CATEGORIES.items():
            if v["name"] in category_choice:
                selected_cat = k
                break

    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        btn_label = "🗺️ New Adventure" if today_me else "🗺️ Start Exploring"
        if st.button(btn_label, key="me_start", width="stretch", type="primary"):
            questions = me.generate_quiz(num_questions=10, category=selected_cat)
            start_map_explorer(questions)
            st.rerun()

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📖 Categories")

    counts = me.get_category_counts()
    cat_cols = st.columns(3, gap="medium")
    for idx, (cat_id, cat_info) in enumerate(me.CATEGORIES.items()):
        cat_count = counts.get(cat_id, 0)
        cat_color = cat_info["color"]
        with cat_cols[idx % 3]:
            st.markdown(f"""
            <div style="padding:0.8rem;border-radius:12px;border-left:4px solid {cat_color};
                 background:{cat_color}10;margin-bottom:0.8rem;">
                <span style="font-size:1.3rem;">{cat_info['emoji']}</span>
                <strong style="color:{cat_color};"> {cat_info['name']}</strong>
                <br><span style="color:#6b7280;font-size:0.85rem;">{cat_count} questions</span>
            </div>
            """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# PAGE: Map Explorer Practice — Question by Question
# ──────────────────────────────────────────────
def render_map_explorer_practice():
    import map_explorer_content as me
    import world_map_data as wmap

    name = st.session_state.selected_user
    user = db.get_user(name)
    questions = st.session_state.me_questions
    current = st.session_state.me_current
    total = len(questions)
    is_done = current >= total

    col_nav1, col_nav_mid, _ = st.columns([1, 4, 1])
    with col_nav1:
        if st.button("← Map Home", key="me_back_home"):
            back_to_map_explorer_home()
            st.rerun()
    with col_nav_mid:
        if not is_done:
            st.markdown(f"""
            <div style="text-align:center; color:#6b7280; font-size:0.9rem; padding-top:0.5rem;">
                Question {current + 1} of {total}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center; color:#6b7280; font-size:0.9rem; padding-top:0.5rem;">
                🎉 Adventure Complete!
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; margin-bottom: 0.5rem;">
        <h1 style="color: #3b82f6; margin: 0.3rem 0; font-size: 2.2rem;">🗺️ Map Explorer</h1>
    </div>
    """, unsafe_allow_html=True)

    progress = (current / total) if total > 0 else 0
    st.markdown(f"""
    <div style="background:#e5e7eb;border-radius:10px;height:10px;overflow:hidden;margin:0 0 1.5rem 0;">
        <div style="width:{progress*100:.0f}%;height:100%;background:linear-gradient(90deg,#3b82f6,#60a5fa);
             border-radius:10px;transition:width 0.4s ease;"></div>
    </div>
    """, unsafe_allow_html=True)

    if not is_done:
        q = questions[current]
        cat_info = me.CATEGORIES.get(q["category"], {})
        cat_color = cat_info.get("color", "#3b82f6")
        cat_emoji = cat_info.get("emoji", "🌍")
        cat_name = cat_info.get("name", "Geography")

        st.markdown(f"""
        <div class="gk-question-box">
            <span class="gk-topic-badge" style="background:{cat_color}20;color:{cat_color};">
                {cat_emoji} {cat_name}
            </span>
            <div class="gk-question-text" style="margin-top:0.8rem;">{q['question']}</div>
        </div>
        """, unsafe_allow_html=True)

        last_feedback = st.session_state.get("me_last_feedback")

        if last_feedback and last_feedback["idx"] == current:
            if last_feedback["correct"]:
                st.markdown(f"""
                <div class="correct-answer" style="text-align:center;">
                    ✅ <strong>Correct!</strong> 🎉
                    <br><br><em>{q.get('explanation', '')}</em>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="wrong-answer" style="text-align:center;">
                    Not quite! You picked <strong>{last_feedback['picked']}</strong>.
                    <br>The answer is <strong>{last_feedback['correct_val']}</strong> 💪
                    <br><br><em>{q.get('explanation', '')}</em>
                </div>
                """, unsafe_allow_html=True)

            # Show flag image when the answer is a country
            correct_answer = q["options"][q["answer"]]
            flag_url = me.get_flag_url(correct_answer)
            if not flag_url and q.get("country"):
                flag_url = me.get_flag_url(q["country"])
                correct_answer = q["country"]
            if flag_url:
                st.markdown(f"""
                <div style="text-align:center;margin:1rem 0;">
                    <img src="{flag_url}" alt="Flag of {correct_answer}"
                         style="width:200px;border-radius:8px;box-shadow:0 2px 8px rgba(0,0,0,0.15);"/>
                    <p style="color:#6b7280;font-size:0.9rem;margin-top:0.3rem;">
                        🏳️ Flag of {correct_answer}
                    </p>
                </div>
                """, unsafe_allow_html=True)

            if q.get("lat") is not None and q.get("lon") is not None:
                map_label = q.get("country") or q["options"][q["answer"]]
                map_html = wmap.render_map_with_marker(q["lat"], q["lon"], label=map_label)
                if map_html:
                    st.markdown(
                        '<div style="text-align:center;margin:1rem 0;">',
                        unsafe_allow_html=True,
                    )
                    st.markdown(map_html, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("")
            _, col_next, _ = st.columns([1, 2, 1])
            with col_next:
                if current < total - 1:
                    if st.button("Next Question ➡️", key="me_next", width="stretch", type="primary"):
                        st.session_state.me_current += 1
                        st.session_state.me_last_feedback = None
                        st.rerun()
                else:
                    if st.button("🎉 See Results!", key="me_results", width="stretch", type="primary"):
                        st.session_state.me_current = total
                        st.session_state.me_last_feedback = None
                        st.rerun()
        else:
            ans_col1, ans_col2 = st.columns(2, gap="medium")
            for i, opt in enumerate(q["options"]):
                col = ans_col1 if i % 2 == 0 else ans_col2
                with col:
                    label = f"{chr(65 + i)}. {opt}"
                    if st.button(label, key=f"me_opt_{current}_{i}", width="stretch", type="primary"):
                        is_correct = (i == q["answer"])
                        st.session_state.me_answers.append({
                            "picked": opt,
                            "correct_val": q["options"][q["answer"]],
                            "correct": is_correct,
                        })
                        st.session_state.me_last_feedback = {
                            "idx": current,
                            "picked": opt,
                            "correct_val": q["options"][q["answer"]],
                            "correct": is_correct,
                        }
                        st.rerun()

    else:
        answers = st.session_state.me_answers
        correct_count = sum(1 for a in answers if a["correct"])
        score_pct = int((correct_count / total) * 100) if total > 0 else 0
        time_spent = int(time.time() - st.session_state.me_start_time) if st.session_state.me_start_time else 0
        minutes, seconds = divmod(time_spent, 60)

        if user:
            db.save_activity_score(
                user["id"], "MapExplorer", "World Quiz",
                score_pct, 100, f"{correct_count}/{total} correct", time_spent,
            )

        if score_pct == 100:
            res_emoji, message, res_color = "🏆", "Perfect! You're a world explorer!", "#10b981"
        elif score_pct >= 70:
            res_emoji, message, res_color = "🌟", "Great job! You know a lot about the world!", "#3b82f6"
        elif score_pct >= 50:
            res_emoji, message, res_color = "👍", "Good try! Keep exploring!", "#f59e0b"
        else:
            res_emoji, message, res_color = "💪", "Keep going! Every quiz teaches you something new!", "#ef4444"

        st.markdown(f"""
        <div style="text-align:center;padding:2rem;background:{res_color}10;border-radius:20px;
             border:3px solid {res_color};margin-top:1rem;">
            <div style="font-size:5rem;">{res_emoji}</div>
            <h2 style="color:{res_color};margin:0.5rem 0;font-size:2rem;">
                {correct_count} out of {total} correct!
            </h2>
            <p style="font-size:1.2rem;color:#4b5563;">{message}</p>
            <p style="color:#9ca3af;">⏱️ Time: {minutes}m {seconds}s</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        st.markdown("### 📋 Review Answers")
        for idx, (q, ans) in enumerate(zip(questions, answers)):
            cat_info = me.CATEGORIES.get(q["category"], {})
            cat_emoji = cat_info.get("emoji", "🌍")
            cat_name = cat_info.get("name", "Geography")

            flag_html = ""
            correct_country = q["options"][q["answer"]]
            flag_url = me.get_flag_url(correct_country)
            if not flag_url and q.get("country"):
                flag_url = me.get_flag_url(q["country"])
                correct_country = q["country"]
            if flag_url:
                flag_html = (
                    f'<div style="margin-top:0.5rem;">'
                    f'<img src="{flag_url}" alt="Flag of {correct_country}" '
                    f'style="width:120px;border-radius:6px;box-shadow:0 1px 4px rgba(0,0,0,0.12);"/>'
                    f'<span style="color:#6b7280;font-size:0.8rem;margin-left:0.5rem;">'
                    f'🏳️ {correct_country}</span></div>'
                )

            if ans["correct"]:
                st.markdown(f"""
                <div class="correct-answer">
                    <span class="gk-topic-badge">{cat_emoji} {cat_name}</span><br>
                    <strong>Q{idx+1}:</strong> {q['question']}<br>
                    ✅ <strong>{ans['correct_val']}</strong>
                    <br><em style="color:#6b7280;">{q.get('explanation', '')}</em>
                    {flag_html}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="wrong-answer">
                    <span class="gk-topic-badge">{cat_emoji} {cat_name}</span><br>
                    <strong>Q{idx+1}:</strong> {q['question']}<br>
                    ❌ You said: <strong>{ans['picked']}</strong>
                    &nbsp; ✅ Answer: <strong>{ans['correct_val']}</strong>
                    <br><em style="color:#6b7280;">{q.get('explanation', '')}</em>
                    {flag_html}
                </div>
                """, unsafe_allow_html=True)

        st.markdown("")
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            if st.button("🗺️ Map Explorer Home", key="me_home_btn", width="stretch", type="primary"):
                back_to_map_explorer_home()
                st.rerun()
        with col_r2:
            if st.button("🏠 Dashboard", key="me_dashboard", width="stretch"):
                st.session_state.current_page = "user_dashboard"
                st.session_state.me_questions = []
                st.session_state.me_current = 0
                st.session_state.me_answers = []
                st.rerun()


# ──────────────────────────────────────────────
# PAGE: Mental Math Home
# ──────────────────────────────────────────────
def render_mental_math_home():
    import mental_math_content as mm

    name = st.session_state.selected_user
    user = db.get_user(name)

    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Back", key="mm_back_to_dash"):
            st.session_state.current_page = "user_dashboard"
            st.session_state.selected_activity = None
            st.rerun()

    st.markdown(f"""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <h1 style="font-size: 2.5rem;">⚡ {name}'s Mental Math Sprint</h1>
        <p style="color: #6b7280; font-size: 1.1rem;">
            10 questions — think fast, be accurate!
        </p>
    </div>
    """, unsafe_allow_html=True)

    today_mm = db.get_today_scores(user["id"], activity_type="MentalMath") if user else []
    total_mm = db.get_scores_history(user["id"], activity_type="MentalMath", days=365) if user else []

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div class="score-card"><div class="score-number">📅 {len(today_mm)}</div>'
            f'<div class="score-label">Sprints Today</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        if today_mm:
            best = max(s["score"] for s in today_mm)
            st.markdown(
                f'<div class="score-card"><div class="score-number">🎯 {best}%</div>'
                f'<div class="score-label">Today\'s Best</div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="score-card"><div class="score-number">🎯 —</div>'
                '<div class="score-label">Today\'s Best</div></div>',
                unsafe_allow_html=True,
            )
    with col3:
        st.markdown(
            f'<div class="score-card"><div class="score-number">⭐ {len(total_mm)}</div>'
            f'<div class="score-label">Total Sprints</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    if today_mm:
        best = max(s["score"] for s in today_mm)
        st.markdown(f"""
        <div style="text-align:center; padding:1rem; background:#fef3c7; border-radius:16px;
             border:2px solid #f59e0b; margin-bottom:1rem;">
            <span style="font-size:2rem;">🔥</span>
            <p style="margin:0.3rem 0; font-size:1.1rem; color:#92400e;">
                <strong>{len(today_mm)} sprint{'s' if len(today_mm) > 1 else ''} today!</strong>
                &nbsp; Best score: <strong>{best}%</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center; padding:1.5rem;">
        <div style="font-size: 4rem;">⚡</div>
        <h3 style="margin: 0.5rem 0;">{"Ready for another sprint?" if today_mm else "Ready to sprint?"}</h3>
        <p style="color: #6b7280;">
            10 questions — arithmetic, percentages, fractions, estimation & word problems!
        </p>
    </div>
    """, unsafe_allow_html=True)

    category_choice = st.selectbox(
        "Focus on a category (optional)",
        ["All Categories (Mixed)"] + [
            f"{mm.CATEGORIES[k]['emoji']} {mm.CATEGORIES[k]['name']}"
            for k in mm.CATEGORIES
        ],
        key="mm_category_filter",
    )

    selected_cat = None
    if category_choice != "All Categories (Mixed)":
        for k, v in mm.CATEGORIES.items():
            if v["name"] in category_choice:
                selected_cat = k
                break

    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        btn_label = "⚡ New Sprint" if today_mm else "⚡ Start Sprint"
        if st.button(btn_label, key="mm_start", width="stretch", type="primary"):
            questions = mm.generate_sprint(num_questions=10, category=selected_cat)
            start_mental_math(questions)
            st.rerun()

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📖 Categories")

    cat_cols = st.columns(3, gap="medium")
    for idx, (cat_id, cat_info) in enumerate(mm.CATEGORIES.items()):
        with cat_cols[idx % 3]:
            st.markdown(f"""
            <div style="padding:0.8rem;border-radius:12px;border-left:4px solid {cat_info['color']};
                 background:{cat_info['color']}10;margin-bottom:0.8rem;">
                <span style="font-size:1.3rem;">{cat_info['emoji']}</span>
                <strong style="color:{cat_info['color']};"> {cat_info['name']}</strong>
            </div>
            """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# PAGE: Mental Math Practice
# ──────────────────────────────────────────────
def render_mental_math_practice():
    import mental_math_content as mm

    name = st.session_state.selected_user
    user = db.get_user(name)
    questions = st.session_state.mm_questions
    current = st.session_state.mm_current
    total = len(questions)
    is_done = current >= total

    col_nav1, col_nav_mid, _ = st.columns([1, 4, 1])
    with col_nav1:
        if st.button("← Math Home", key="mm_back_home"):
            back_to_mental_math_home()
            st.rerun()
    with col_nav_mid:
        if not is_done:
            elapsed = int(time.time() - st.session_state.mm_start_time) if st.session_state.mm_start_time else 0
            st.markdown(f"""
            <div style="text-align:center; color:#6b7280; font-size:0.9rem; padding-top:0.5rem;">
                Question {current + 1} of {total} &nbsp;|&nbsp; ⏱️ {elapsed}s
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; margin-bottom: 0.5rem;">
        <h1 style="color: #ef4444; margin: 0.3rem 0; font-size: 2.2rem;">⚡ Mental Math Sprint</h1>
    </div>
    """, unsafe_allow_html=True)

    progress = (current / total) if total > 0 else 0
    st.markdown(f"""
    <div style="background:#e5e7eb;border-radius:10px;height:10px;overflow:hidden;margin:0 0 1.5rem 0;">
        <div style="width:{progress*100:.0f}%;height:100%;background:linear-gradient(90deg,#ef4444,#f59e0b);
             border-radius:10px;transition:width 0.4s ease;"></div>
    </div>
    """, unsafe_allow_html=True)

    if not is_done:
        q = questions[current]
        cat_info = mm.CATEGORIES.get(q["category"], {})
        cat_color = cat_info.get("color", "#ef4444")
        cat_emoji = cat_info.get("emoji", "⚡")
        cat_name = cat_info.get("name", "Math")

        st.markdown(f"""
        <div class="gk-question-box">
            <span class="gk-topic-badge" style="background:{cat_color}20;color:{cat_color};">
                {cat_emoji} {cat_name}
            </span>
            <div class="gk-question-text" style="margin-top:0.8rem;font-size:1.4rem;">{q['question']}</div>
        </div>
        """, unsafe_allow_html=True)

        last_feedback = st.session_state.get("mm_last_feedback")

        if last_feedback and last_feedback.get("idx") == current:
            if last_feedback["correct"]:
                st.markdown("""
                <div class="correct-answer" style="text-align:center;">
                    ✅ <strong>Correct!</strong> 🎉
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="wrong-answer" style="text-align:center;">
                    Not quite! The answer is <strong>{last_feedback['correct_val']}</strong>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("")
            _, col_next, _ = st.columns([1, 2, 1])
            with col_next:
                if current < total - 1:
                    if st.button("Next ➡️", key="mm_next", width="stretch", type="primary"):
                        st.session_state.mm_current += 1
                        st.session_state.mm_last_feedback = None
                        st.rerun()
                else:
                    if st.button("🎉 See Results!", key="mm_results", width="stretch", type="primary"):
                        st.session_state.mm_current = total
                        st.session_state.mm_last_feedback = None
                        st.rerun()
        else:
            ans_col1, ans_col2 = st.columns(2, gap="medium")
            for i, opt in enumerate(q["options"]):
                col = ans_col1 if i % 2 == 0 else ans_col2
                with col:
                    label = str(opt)
                    if st.button(label, key=f"mm_opt_{current}_{i}", width="stretch", type="primary"):
                        is_correct = (i == q["answer"])
                        st.session_state.mm_answers.append({
                            "picked": opt,
                            "correct_val": q["options"][q["answer"]],
                            "correct": is_correct,
                        })
                        st.session_state.mm_last_feedback = {
                            "idx": current,
                            "picked": opt,
                            "correct_val": q["options"][q["answer"]],
                            "correct": is_correct,
                        }
                        st.rerun()

    else:
        answers = st.session_state.mm_answers
        correct_count = sum(1 for a in answers if a["correct"])
        score_pct = int((correct_count / total) * 100) if total > 0 else 0
        time_spent = int(time.time() - st.session_state.mm_start_time) if st.session_state.mm_start_time else 0
        minutes, seconds = divmod(time_spent, 60)

        if user:
            db.save_activity_score(
                user["id"], "MentalMath", "Sprint",
                score_pct, 100, f"{correct_count}/{total} in {time_spent}s", time_spent,
            )

        if score_pct == 100:
            res_emoji, message, res_color = "🏆", "Perfect score! Lightning fast!", "#10b981"
        elif score_pct >= 80:
            res_emoji, message, res_color = "🔥", "On fire! Great speed and accuracy!", "#3b82f6"
        elif score_pct >= 60:
            res_emoji, message, res_color = "⚡", "Nice sprint! Keep practicing!", "#f59e0b"
        else:
            res_emoji, message, res_color = "💪", "Good effort! Speed comes with practice!", "#ef4444"

        st.markdown(f"""
        <div style="text-align:center;padding:2rem;background:{res_color}10;border-radius:20px;
             border:3px solid {res_color};margin-top:1rem;">
            <div style="font-size:5rem;">{res_emoji}</div>
            <h2 style="color:{res_color};margin:0.5rem 0;font-size:2rem;">
                {correct_count} out of {total} correct!
            </h2>
            <p style="font-size:1.2rem;color:#4b5563;">{message}</p>
            <p style="color:#9ca3af;">⏱️ Time: {minutes}m {seconds}s &nbsp;|&nbsp;
               Avg: {time_spent / total:.1f}s per question</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        st.markdown("### 📋 Review")
        for idx, (q, ans) in enumerate(zip(questions, answers)):
            if ans["correct"]:
                st.markdown(f"""
                <div class="correct-answer">
                    <strong>Q{idx+1}:</strong> {q['question']}
                    &nbsp; ✅ <strong>{ans['correct_val']}</strong>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="wrong-answer">
                    <strong>Q{idx+1}:</strong> {q['question']}
                    &nbsp; ❌ You said: <strong>{ans['picked']}</strong>
                    &nbsp; ✅ Answer: <strong>{ans['correct_val']}</strong>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("")
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            if st.button("⚡ Sprint Again", key="mm_home_btn", width="stretch", type="primary"):
                back_to_mental_math_home()
                st.rerun()
        with col_r2:
            if st.button("🏠 Dashboard", key="mm_dashboard", width="stretch"):
                st.session_state.current_page = "user_dashboard"
                st.session_state.mm_questions = []
                st.session_state.mm_current = 0
                st.session_state.mm_answers = []
                st.rerun()


# ──────────────────────────────────────────────
# PAGE: Science Corner Home
# ──────────────────────────────────────────────
def render_science_home():
    import science_content as sc

    name = st.session_state.selected_user
    user = db.get_user(name)

    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Back", key="sci_back_to_dash"):
            st.session_state.current_page = "user_dashboard"
            st.session_state.selected_activity = None
            st.rerun()

    st.markdown(f"""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <h1 style="font-size: 2.5rem;">🔬 {name}'s Science Corner</h1>
        <p style="color: #6b7280; font-size: 1.1rem;">
            Grade 6 Inspire Science — 10 questions per quiz!
        </p>
    </div>
    """, unsafe_allow_html=True)

    today_sci = db.get_today_scores(user["id"], activity_type="Science") if user else []
    total_sci = db.get_scores_history(user["id"], activity_type="Science", days=365) if user else []

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div class="score-card"><div class="score-number">📅 {len(today_sci)}</div>'
            f'<div class="score-label">Quizzes Today</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        if today_sci:
            best = max(s["score"] for s in today_sci)
            st.markdown(
                f'<div class="score-card"><div class="score-number">🎯 {best}%</div>'
                f'<div class="score-label">Today\'s Best</div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="score-card"><div class="score-number">🎯 —</div>'
                '<div class="score-label">Today\'s Best</div></div>',
                unsafe_allow_html=True,
            )
    with col3:
        st.markdown(
            f'<div class="score-card"><div class="score-number">⭐ {len(total_sci)}</div>'
            f'<div class="score-label">Total Quizzes</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    if today_sci:
        best = max(s["score"] for s in today_sci)
        st.markdown(f"""
        <div style="text-align:center; padding:1rem; background:#ecfdf5; border-radius:16px;
             border:2px solid #10b981; margin-bottom:1rem;">
            <span style="font-size:2rem;">🔬</span>
            <p style="margin:0.3rem 0; font-size:1.1rem; color:#065f46;">
                <strong>{len(today_sci)} quiz{'zes' if len(today_sci) > 1 else ''} today!</strong>
                &nbsp; Best score: <strong>{best}%</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center; padding:1.5rem;">
        <div style="font-size: 4rem;">🔬</div>
        <h3 style="margin: 0.5rem 0;">{"Ready for another quiz?" if today_sci else "Ready to explore science?"}</h3>
        <p style="color: #6b7280;">
            Life Science, Genetics, Ecosystems & Physical Science!
        </p>
    </div>
    """, unsafe_allow_html=True)

    category_choice = st.selectbox(
        "Focus on a topic (optional)",
        ["All Topics (Mixed)"] + [
            f"{sc.CATEGORIES[k]['emoji']} {sc.CATEGORIES[k]['name']}"
            for k in sc.CATEGORIES
        ],
        key="sci_category_filter",
    )

    selected_cat = None
    if category_choice != "All Topics (Mixed)":
        for k, v in sc.CATEGORIES.items():
            if v["name"] in category_choice:
                selected_cat = k
                break

    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        btn_label = "🔬 New Quiz" if today_sci else "🔬 Start Quiz"
        if st.button(btn_label, key="sci_start", width="stretch", type="primary"):
            questions = sc.generate_quiz(num_questions=10, category=selected_cat)
            start_science_quiz(questions)
            st.rerun()

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📖 Topics")

    counts = sc.get_category_counts()
    cat_cols = st.columns(2, gap="medium")
    for idx, (cat_id, cat_info) in enumerate(sc.CATEGORIES.items()):
        with cat_cols[idx % 2]:
            st.markdown(f"""
            <div style="padding:1rem;border-radius:12px;border-left:4px solid {cat_info['color']};
                 background:{cat_info['color']}10;margin-bottom:0.8rem;">
                <span style="font-size:1.3rem;">{cat_info['emoji']}</span>
                <strong style="color:{cat_info['color']};"> {cat_info['name']}</strong>
                <span style="color:#9ca3af;font-size:0.85rem;"> — {counts[cat_id]} questions</span>
                <p style="color:#6b7280;font-size:0.85rem;margin:0.3rem 0 0 0;">
                    {cat_info['description']}
                </p>
            </div>
            """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# PAGE: Science Corner Practice
# ──────────────────────────────────────────────
def render_science_practice():
    import science_content as sc

    name = st.session_state.selected_user
    user = db.get_user(name)
    questions = st.session_state.sci_questions
    current = st.session_state.sci_current
    total = len(questions)
    is_done = current >= total

    col_nav1, col_nav_mid, _ = st.columns([1, 4, 1])
    with col_nav1:
        if st.button("← Science Home", key="sci_back_home"):
            back_to_science_home()
            st.rerun()
    with col_nav_mid:
        if not is_done:
            elapsed = int(time.time() - st.session_state.sci_start_time) if st.session_state.sci_start_time else 0
            st.markdown(f"""
            <div style="text-align:center; color:#6b7280; font-size:0.9rem; padding-top:0.5rem;">
                Question {current + 1} of {total} &nbsp;|&nbsp; ⏱️ {elapsed}s
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; margin-bottom: 0.5rem;">
        <h1 style="color: #06b6d4; margin: 0.3rem 0; font-size: 2.2rem;">🔬 Science Corner</h1>
    </div>
    """, unsafe_allow_html=True)

    progress = (current / total) if total > 0 else 0
    st.markdown(f"""
    <div style="background:#e5e7eb;border-radius:10px;height:10px;overflow:hidden;margin:0 0 1.5rem 0;">
        <div style="width:{progress*100:.0f}%;height:100%;background:linear-gradient(90deg,#06b6d4,#10b981);
             border-radius:10px;transition:width 0.4s ease;"></div>
    </div>
    """, unsafe_allow_html=True)

    if not is_done:
        q = questions[current]
        cat_info = sc.CATEGORIES.get(q["category"], {})
        cat_color = cat_info.get("color", "#06b6d4")
        cat_emoji = cat_info.get("emoji", "🔬")
        cat_name = cat_info.get("name", "Science")

        sci_img_name = q.get("image")
        sci_img_path = os.path.join("science_images", f"{sci_img_name}.png") if sci_img_name else None
        has_sci_img = sci_img_path and os.path.exists(sci_img_path)

        if has_sci_img:
            q_col, img_col = st.columns([3, 2], gap="medium")
            with q_col:
                st.markdown(f"""
                <div class="gk-question-box">
                    <span class="gk-topic-badge" style="background:{cat_color}20;color:{cat_color};">
                        {cat_emoji} {cat_name}
                    </span>
                    <div class="gk-question-text" style="margin-top:0.8rem;font-size:1.4rem;">{q['question']}</div>
                </div>
                """, unsafe_allow_html=True)
            with img_col:
                st.image(sci_img_path, width="stretch")
        else:
            st.markdown(f"""
            <div class="gk-question-box">
                <span class="gk-topic-badge" style="background:{cat_color}20;color:{cat_color};">
                    {cat_emoji} {cat_name}
                </span>
                <div class="gk-question-text" style="margin-top:0.8rem;font-size:1.4rem;">{q['question']}</div>
            </div>
            """, unsafe_allow_html=True)

        last_feedback = st.session_state.get("sci_last_feedback")

        if last_feedback and last_feedback.get("idx") == current:
            if last_feedback["correct"]:
                st.markdown(f"""
                <div class="correct-answer" style="text-align:center;">
                    ✅ <strong>Correct!</strong> 🎉
                    <p style="color:#065f46;font-size:0.9rem;margin-top:0.3rem;">
                        {q.get('explanation', '')}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="wrong-answer" style="text-align:center;">
                    Not quite! The answer is <strong>{last_feedback['correct_val']}</strong>
                    <p style="color:#991b1b;font-size:0.9rem;margin-top:0.3rem;">
                        {q.get('explanation', '')}
                    </p>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("")
            _, col_next, _ = st.columns([1, 2, 1])
            with col_next:
                if current < total - 1:
                    if st.button("Next ➡️", key="sci_next", width="stretch", type="primary"):
                        st.session_state.sci_current += 1
                        st.session_state.sci_last_feedback = None
                        st.rerun()
                else:
                    if st.button("🎉 See Results!", key="sci_results", width="stretch", type="primary"):
                        st.session_state.sci_current = total
                        st.session_state.sci_last_feedback = None
                        st.rerun()
        else:
            ans_col1, ans_col2 = st.columns(2, gap="medium")
            for i, opt in enumerate(q["options"]):
                col = ans_col1 if i % 2 == 0 else ans_col2
                with col:
                    label = str(opt)
                    if st.button(label, key=f"sci_opt_{current}_{i}", width="stretch", type="primary"):
                        is_correct = (i == q["answer"])
                        st.session_state.sci_answers.append({
                            "picked": opt,
                            "correct_val": q["options"][q["answer"]],
                            "correct": is_correct,
                            "explanation": q.get("explanation", ""),
                        })
                        st.session_state.sci_last_feedback = {
                            "idx": current,
                            "picked": opt,
                            "correct_val": q["options"][q["answer"]],
                            "correct": is_correct,
                        }
                        st.rerun()

    else:
        answers = st.session_state.sci_answers
        correct_count = sum(1 for a in answers if a["correct"])
        score_pct = int((correct_count / total) * 100) if total > 0 else 0
        time_spent = int(time.time() - st.session_state.sci_start_time) if st.session_state.sci_start_time else 0
        minutes, seconds = divmod(time_spent, 60)

        if user:
            db.save_activity_score(
                user["id"], "Science", "Quiz",
                score_pct, 100, f"{correct_count}/{total} correct", time_spent,
            )

        if score_pct == 100:
            res_emoji, message, res_color = "🏆", "Perfect score! You're a science superstar!", "#10b981"
        elif score_pct >= 80:
            res_emoji, message, res_color = "🔥", "Excellent! You really know your science!", "#3b82f6"
        elif score_pct >= 60:
            res_emoji, message, res_color = "🔬", "Good job! Keep exploring and learning!", "#f59e0b"
        else:
            res_emoji, message, res_color = "💪", "Keep it up! Science gets easier with practice!", "#ef4444"

        st.markdown(f"""
        <div style="text-align:center;padding:2rem;background:{res_color}10;border-radius:20px;
             border:3px solid {res_color};margin-top:1rem;">
            <div style="font-size:5rem;">{res_emoji}</div>
            <h2 style="color:{res_color};margin:0.5rem 0;font-size:2rem;">
                {correct_count} out of {total} correct!
            </h2>
            <p style="font-size:1.2rem;color:#4b5563;">{message}</p>
            <p style="color:#9ca3af;">⏱️ Time: {minutes}m {seconds}s</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        st.markdown("### 📋 Review")
        for idx, (q, ans) in enumerate(zip(questions, answers)):
            rev_img_name = q.get("image")
            rev_img_path = os.path.join("science_images", f"{rev_img_name}.png") if rev_img_name else None
            has_rev_img = rev_img_path and os.path.exists(rev_img_path)

            if ans["correct"]:
                st.markdown(f"""
                <div class="correct-answer">
                    <strong>Q{idx+1}:</strong> {q['question']}
                    &nbsp; ✅ <strong>{ans['correct_val']}</strong>
                    <p style="color:#065f46;font-size:0.85rem;margin:0.3rem 0 0 0;">
                        {q.get('explanation', '')}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="wrong-answer">
                    <strong>Q{idx+1}:</strong> {q['question']}
                    &nbsp; ❌ You said: <strong>{ans['picked']}</strong>
                    &nbsp; ✅ Answer: <strong>{ans['correct_val']}</strong>
                    <p style="color:#991b1b;font-size:0.85rem;margin:0.3rem 0 0 0;">
                        {q.get('explanation', '')}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            if has_rev_img:
                st.image(rev_img_path, width=280)

        st.markdown("")
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            if st.button("🔬 Quiz Again", key="sci_again_btn", width="stretch", type="primary"):
                back_to_science_home()
                st.rerun()
        with col_r2:
            if st.button("🏠 Dashboard", key="sci_dashboard", width="stretch"):
                st.session_state.current_page = "user_dashboard"
                st.session_state.sci_questions = []
                st.session_state.sci_current = 0
                st.session_state.sci_answers = []
                st.rerun()


# ──────────────────────────────────────────────
# PAGE: Logo Identifier Home
# ──────────────────────────────────────────────
def render_logo_id_home():
    import logo_identifier_content as li

    name = st.session_state.selected_user
    user = db.get_user(name)

    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Back", key="logo_back_to_dash"):
            st.session_state.current_page = "user_dashboard"
            st.session_state.selected_activity = None
            st.rerun()

    st.markdown(f"""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <h1 style="font-size: 2.5rem;">🏷️ {name}'s Logo Identifier</h1>
        <p style="color: #6b7280; font-size: 1.1rem;">
            Can you name the brand from its logo? 10 questions per quiz!
        </p>
    </div>
    """, unsafe_allow_html=True)

    today_logo = db.get_today_scores(user["id"], activity_type="LogoID") if user else []
    total_logo = db.get_scores_history(user["id"], activity_type="LogoID", days=365) if user else []

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div class="score-card"><div class="score-number">📅 {len(today_logo)}</div>'
            f'<div class="score-label">Quizzes Today</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        if today_logo:
            best = max(s["score"] for s in today_logo)
            st.markdown(
                f'<div class="score-card"><div class="score-number">🎯 {best}%</div>'
                f'<div class="score-label">Today\'s Best</div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="score-card"><div class="score-number">🎯 —</div>'
                '<div class="score-label">Today\'s Best</div></div>',
                unsafe_allow_html=True,
            )
    with col3:
        st.markdown(
            f'<div class="score-card"><div class="score-number">⭐ {len(total_logo)}</div>'
            f'<div class="score-label">Total Quizzes</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    if today_logo:
        best = max(s["score"] for s in today_logo)
        st.markdown(f"""
        <div style="text-align:center; padding:1rem; background:#fffbeb; border-radius:16px;
             border:2px solid #f59e0b; margin-bottom:1rem;">
            <span style="font-size:2rem;">🏷️</span>
            <p style="margin:0.3rem 0; font-size:1.1rem; color:#92400e;">
                <strong>{len(today_logo)} quiz{'zes' if len(today_logo) > 1 else ''} today!</strong>
                &nbsp; Best score: <strong>{best}%</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center; padding:1.5rem;">
        <div style="font-size: 4rem;">🏷️</div>
        <h3 style="margin: 0.5rem 0;">{"Ready for another round?" if today_logo else "Think you know your logos?"}</h3>
        <p style="color: #6b7280;">
            Tech, Food, Sports, Cars, Entertainment & Fashion!
        </p>
    </div>
    """, unsafe_allow_html=True)

    category_choice = st.selectbox(
        "Focus on a category (optional)",
        ["All Categories (Mixed)"] + [
            f"{li.CATEGORIES[k]['emoji']} {li.CATEGORIES[k]['name']}"
            for k in li.CATEGORIES
        ],
        key="logo_category_filter",
    )

    selected_cat = None
    if category_choice != "All Categories (Mixed)":
        for k, v in li.CATEGORIES.items():
            if v["name"] in category_choice:
                selected_cat = k
                break

    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        btn_label = "🏷️ New Quiz" if today_logo else "🏷️ Start Quiz"
        if st.button(btn_label, key="logo_start", width="stretch", type="primary"):
            questions = li.generate_quiz(10, category=selected_cat)
            start_logo_quiz(questions)
            st.rerun()

    counts = li.get_category_counts()
    st.markdown("---")
    st.markdown("#### 📚 Brand Collection")
    cols = st.columns(len(li.CATEGORIES))
    for i, (cat_id, cat_info) in enumerate(li.CATEGORIES.items()):
        with cols[i]:
            st.markdown(
                f'<div style="text-align:center;padding:0.8rem;background:{cat_info["color"]}15;'
                f'border-radius:12px;border:1px solid {cat_info["color"]}40;">'
                f'<div style="font-size:1.5rem;">{cat_info["emoji"]}</div>'
                f'<div style="font-weight:600;font-size:0.85rem;">{cat_info["name"]}</div>'
                f'<div style="color:#6b7280;font-size:0.8rem;">{counts.get(cat_id, 0)} brands</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ──────────────────────────────────────────────
# PAGE: Logo Identifier Practice
# ──────────────────────────────────────────────
def render_logo_id_practice():
    import logo_identifier_content as li

    name = st.session_state.selected_user
    user = db.get_user(name)
    questions = st.session_state.logo_questions
    current = st.session_state.logo_current

    if not questions:
        back_to_logo_home()
        st.rerun()
        return

    total = len(questions)

    st.markdown("""
    <div style="text-align: center; margin-bottom: 0.5rem;">
        <h1 style="color: #f59e0b; margin: 0.3rem 0; font-size: 2.2rem;">🏷️ Logo Identifier</h1>
    </div>
    """, unsafe_allow_html=True)

    progress = (current / total) if total > 0 else 0
    st.markdown(f"""
    <div style="background:#e5e7eb;border-radius:10px;height:10px;overflow:hidden;margin:0 0 1.5rem 0;">
        <div style="width:{progress*100:.0f}%;height:100%;background:linear-gradient(90deg,#f59e0b,#ef4444);
             border-radius:10px;transition:width 0.4s ease;"></div>
    </div>
    <div style="text-align:center;color:#6b7280;margin-top:-0.8rem;margin-bottom:1rem;font-size:0.9rem;">
        Question {min(current + 1, total)} of {total}
    </div>
    """, unsafe_allow_html=True)

    if current < total:
        q = questions[current]
        cat_info = li.CATEGORIES.get(q["category"], {})
        options = q["_shuffled_options"]
        answer_idx = q["_answer_idx"]

        logo_img_name = q.get("_image") or q.get("image")
        logo_img_path = os.path.join("brand_logos", f"{logo_img_name}.png") if logo_img_name else None
        has_local_logo = logo_img_path and os.path.exists(logo_img_path)

        logo_col, q_col = st.columns([1, 2], gap="medium")
        with logo_col:
            if has_local_logo:
                st.markdown(f"""
                <div style="text-align:center;padding:1rem;background:white;border-radius:16px;
                     box-shadow:0 4px 20px rgba(0,0,0,0.08);border:2px solid #e5e7eb;">
                """, unsafe_allow_html=True)
                st.image(logo_img_path, width=220)
                st.markdown(f"""
                    <p style="margin:0.3rem 0 0 0;color:#9ca3af;font-size:0.85rem;text-align:center;">
                        {cat_info.get('emoji','')} {cat_info.get('name','')}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                logo_url = q["_logo_url"]
                st.markdown(f"""
                <div style="text-align:center;padding:1.5rem;background:white;border-radius:16px;
                     box-shadow:0 4px 20px rgba(0,0,0,0.08);border:2px solid #e5e7eb;">
                    <img src="{logo_url}" alt="Logo"
                         style="width:180px;height:180px;object-fit:contain;image-rendering:auto;"
                         onerror="this.style.display='none';this.parentElement.innerHTML+='<div style=\\'font-size:4rem;\\'>❓</div><p style=\\'color:#9ca3af;\\'>Logo unavailable</p>';">
                    <p style="margin:0.8rem 0 0 0;color:#9ca3af;font-size:0.85rem;">
                        {cat_info.get('emoji','')} {cat_info.get('name','')}
                    </p>
                </div>
                """, unsafe_allow_html=True)

        with q_col:
            st.markdown(f"""
            <div style="padding:1rem 0;">
                <h3 style="margin:0 0 0.5rem 0;font-size:1.4rem;color:#1f2937;">
                    Which company uses this logo?
                </h3>
            </div>
            """, unsafe_allow_html=True)

            hint_text = q.get("hint", "")
            if hint_text:
                with st.expander("💡 Need a hint?"):
                    st.markdown(f"*{hint_text}*")

            feedback = st.session_state.logo_last_feedback

            if feedback and feedback.get("question_id") == q["id"]:
                for i, opt in enumerate(options):
                    if i == answer_idx:
                        st.markdown(
                            f'<div style="padding:0.8rem 1.2rem;border-radius:12px;margin:0.4rem 0;'
                            f'background:#dcfce7;border:2px solid #22c55e;font-weight:600;">'
                            f'✅ {opt}</div>',
                            unsafe_allow_html=True,
                        )
                    elif i == feedback.get("selected") and not feedback.get("correct"):
                        st.markdown(
                            f'<div style="padding:0.8rem 1.2rem;border-radius:12px;margin:0.4rem 0;'
                            f'background:#fee2e2;border:2px solid #ef4444;text-decoration:line-through;">'
                            f'❌ {opt}</div>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.markdown(
                            f'<div style="padding:0.8rem 1.2rem;border-radius:12px;margin:0.4rem 0;'
                            f'background:#f9fafb;border:1px solid #e5e7eb;color:#9ca3af;">'
                            f'{opt}</div>',
                            unsafe_allow_html=True,
                        )

                if feedback.get("correct"):
                    st.success(f"🎉 Correct! {q.get('fun_fact', '')}")
                else:
                    st.error(f"Not quite! {q.get('fun_fact', '')}")

                st.markdown("")
                next_label = "Next Logo ➡️" if current + 1 < total else "See Results 🏆"
                if st.button(next_label, key=f"logo_next_{current}", width="stretch", type="primary"):
                    st.session_state.logo_current += 1
                    st.session_state.logo_last_feedback = None
                    st.rerun()
            else:
                opt_cols = st.columns(2)
                for i, opt in enumerate(options):
                    with opt_cols[i % 2]:
                        if st.button(opt, key=f"logo_opt_{current}_{i}", width="stretch"):
                            is_correct = i == answer_idx
                            st.session_state.logo_answers.append({
                                "company": q["company"],
                                "domain": q["domain"],
                                "selected": i,
                                "selected_text": opt,
                                "correct": is_correct,
                                "fun_fact": q.get("fun_fact", ""),
                                "category": q.get("category", ""),
                                "logo_url": q["_logo_url"],
                                "image": q.get("_image") or q.get("image"),
                            })
                            st.session_state.logo_last_feedback = {
                                "question_id": q["id"],
                                "selected": i,
                                "correct": is_correct,
                            }
                            st.rerun()

    else:
        answers = st.session_state.logo_answers
        correct_count = sum(1 for a in answers if a["correct"])
        score_pct = int((correct_count / total) * 100) if total > 0 else 0
        time_spent = int(time.time() - st.session_state.logo_start_time) if st.session_state.logo_start_time else 0
        minutes, seconds = divmod(time_spent, 60)

        if user:
            db.save_activity_score(
                user["id"], "LogoID", "Quiz",
                score_pct, 100, f"{correct_count}/{total} correct", time_spent,
            )

        if score_pct >= 80:
            emoji, msg = "🏆", "Amazing! You're a brand genius!"
        elif score_pct >= 60:
            emoji, msg = "⭐", "Great eye! You know your logos!"
        elif score_pct >= 40:
            emoji, msg = "🏷️", "Good start! Keep looking around — logos are everywhere!"
        else:
            emoji, msg = "👀", "Time to pay more attention to those logos around you!"

        st.markdown(f"""
        <div style="text-align:center;padding:2rem;background:linear-gradient(135deg,#fffbeb,#fef2f2);
             border-radius:20px;margin:1rem 0;">
            <div style="font-size:4rem;">{emoji}</div>
            <h2 style="margin:0.5rem 0;">{score_pct}%</h2>
            <p style="font-size:1.2rem;color:#374151;">{msg}</p>
            <p style="color:#6b7280;">{correct_count} of {total} correct &nbsp;|&nbsp; ⏱️ {minutes}m {seconds}s</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        _, c1, c2, _ = st.columns([1, 2, 2, 1])
        with c1:
            if st.button("🏷️ New Quiz", key="logo_new_quiz", width="stretch", type="primary"):
                back_to_logo_home()
                st.rerun()
        with c2:
            if st.button("← Dashboard", key="logo_to_dash", width="stretch"):
                st.session_state.current_page = "user_dashboard"
                st.session_state.selected_activity = None
                st.rerun()

        st.markdown("---")
        st.markdown("### 📋 Review Answers")

        for i, a in enumerate(answers):
            icon = "✅" if a["correct"] else "❌"
            with st.expander(f"{icon} Q{i+1}: {a['company']}"):
                rev_cols = st.columns([1, 3])
                with rev_cols[0]:
                    rev_img_name = a.get("image")
                    rev_img_path = os.path.join("brand_logos", f"{rev_img_name}.png") if rev_img_name else None
                    if rev_img_path and os.path.exists(rev_img_path):
                        st.image(rev_img_path, width=80)
                    else:
                        st.markdown(
                            f'<img src="{a["logo_url"]}" style="width:80px;height:80px;object-fit:contain;">',
                            unsafe_allow_html=True,
                        )
                with rev_cols[1]:
                    if a["correct"]:
                        st.markdown(f"**Your answer:** {a['selected_text']} ✅")
                    else:
                        st.markdown(f"**Your answer:** {a['selected_text']} ❌")
                        st.markdown(f"**Correct answer:** {a['company']} ✅")
                    if a.get("fun_fact"):
                        st.info(f"💡 {a['fun_fact']}")


# ──────────────────────────────────────────────
# PAGE: Movie Buff Home
# ──────────────────────────────────────────────
def render_movie_buff_home():
    import movie_buff_content as mb

    name = st.session_state.selected_user
    user = db.get_user(name)

    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Back", key="movie_back_to_dash"):
            st.session_state.current_page = "user_dashboard"
            st.session_state.selected_activity = None
            st.rerun()

    st.markdown(f"""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <h1 style="font-size: 2.5rem;">🎬 {name}'s Movie Buff</h1>
        <p style="color: #6b7280; font-size: 1.1rem;">
            Kid-friendly movie trivia — 10 questions per quiz!
        </p>
    </div>
    """, unsafe_allow_html=True)

    today_movie = db.get_today_scores(user["id"], activity_type="MovieBuff") if user else []
    total_movie = db.get_scores_history(user["id"], activity_type="MovieBuff", days=365) if user else []

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div class="score-card"><div class="score-number">📅 {len(today_movie)}</div>'
            f'<div class="score-label">Quizzes Today</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        if today_movie:
            best = max(s["score"] for s in today_movie)
            st.markdown(
                f'<div class="score-card"><div class="score-number">🎯 {best}%</div>'
                f'<div class="score-label">Today\'s Best</div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="score-card"><div class="score-number">🎯 —</div>'
                '<div class="score-label">Today\'s Best</div></div>',
                unsafe_allow_html=True,
            )
    with col3:
        st.markdown(
            f'<div class="score-card"><div class="score-number">⭐ {len(total_movie)}</div>'
            f'<div class="score-label">Total Quizzes</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    if today_movie:
        best = max(s["score"] for s in today_movie)
        st.markdown(f"""
        <div style="text-align:center; padding:1rem; background:#fff1f2; border-radius:16px;
             border:2px solid #e11d48; margin-bottom:1rem;">
            <span style="font-size:2rem;">🎬</span>
            <p style="margin:0.3rem 0; font-size:1.1rem; color:#9f1239;">
                <strong>{len(today_movie)} quiz{'zes' if len(today_movie) > 1 else ''} today!</strong>
                &nbsp; Best score: <strong>{best}%</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center; padding:1.5rem;">
        <div style="font-size: 4rem;">🍿</div>
        <h3 style="margin: 0.5rem 0;">{"Ready for another round?" if today_movie else "Ready for movie trivia?"}</h3>
        <p style="color: #6b7280;">
            Animated, Adventure, Superheroes, Comedy & Fantasy!
        </p>
    </div>
    """, unsafe_allow_html=True)

    category_choice = st.selectbox(
        "Focus on a genre (optional)",
        ["All Genres (Mixed)"] + [
            f"{mb.CATEGORIES[k]['emoji']} {mb.CATEGORIES[k]['name']}"
            for k in mb.CATEGORIES
        ],
        key="movie_category_filter",
    )

    selected_cat = None
    if category_choice != "All Genres (Mixed)":
        for k, v in mb.CATEGORIES.items():
            if v["name"] in category_choice:
                selected_cat = k
                break

    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        btn_label = "🎬 New Quiz" if today_movie else "🎬 Start Quiz"
        if st.button(btn_label, key="movie_start", width="stretch", type="primary"):
            questions = mb.generate_quiz(10, category=selected_cat)
            start_movie_quiz(questions)
            st.rerun()

    counts = mb.get_category_counts()
    st.markdown("---")
    st.markdown("#### 📚 Question Bank")
    cols = st.columns(len(mb.CATEGORIES))
    for i, (cat_id, cat_info) in enumerate(mb.CATEGORIES.items()):
        with cols[i]:
            st.markdown(
                f'<div style="text-align:center;padding:0.8rem;background:{cat_info["color"]}15;'
                f'border-radius:12px;border:1px solid {cat_info["color"]}40;">'
                f'<div style="font-size:1.5rem;">{cat_info["emoji"]}</div>'
                f'<div style="font-weight:600;font-size:0.85rem;">{cat_info["name"]}</div>'
                f'<div style="color:#6b7280;font-size:0.8rem;">{counts.get(cat_id, 0)} questions</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ──────────────────────────────────────────────
# PAGE: Movie Buff Practice
# ──────────────────────────────────────────────
def render_movie_buff_practice():
    import movie_buff_content as mb

    name = st.session_state.selected_user
    user = db.get_user(name)
    questions = st.session_state.movie_questions
    current = st.session_state.movie_current

    if not questions:
        back_to_movie_home()
        st.rerun()
        return

    total = len(questions)

    st.markdown("""
    <div style="text-align: center; margin-bottom: 0.5rem;">
        <h1 style="color: #e11d48; margin: 0.3rem 0; font-size: 2.2rem;">🎬 Movie Buff</h1>
    </div>
    """, unsafe_allow_html=True)

    progress = (current / total) if total > 0 else 0
    st.markdown(f"""
    <div style="background:#e5e7eb;border-radius:10px;height:10px;overflow:hidden;margin:0 0 1.5rem 0;">
        <div style="width:{progress*100:.0f}%;height:100%;background:linear-gradient(90deg,#e11d48,#f59e0b);
             border-radius:10px;transition:width 0.4s ease;"></div>
    </div>
    <div style="text-align:center;color:#6b7280;margin-top:-0.8rem;margin-bottom:1rem;font-size:0.9rem;">
        Question {min(current + 1, total)} of {total}
    </div>
    """, unsafe_allow_html=True)

    if current < total:
        q = questions[current]
        cat_info = mb.CATEGORIES.get(q["category"], {})
        cat_emoji = cat_info.get("emoji", "🎬")
        cat_name = cat_info.get("name", "Movies")

        st.markdown(f"""
        <div style="background:white;border-radius:16px;padding:1.5rem 2rem;
             box-shadow:0 2px 12px rgba(0,0,0,0.06);border-left:5px solid {cat_info.get('color','#e11d48')};">
            <div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.8rem;">
                <span style="font-size:1.3rem;">{cat_emoji}</span>
                <span style="font-size:0.85rem;color:#6b7280;font-weight:600;">{cat_name}</span>
            </div>
            <h3 style="margin:0;font-size:1.3rem;color:#1f2937;">{q['question']}</h3>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")

        feedback = st.session_state.movie_last_feedback

        if feedback and feedback.get("question_id") == q["id"]:
            for i, opt in enumerate(q["options"]):
                if i == q["answer"]:
                    st.markdown(
                        f'<div style="padding:0.8rem 1.2rem;border-radius:12px;margin:0.4rem 0;'
                        f'background:#dcfce7;border:2px solid #22c55e;font-weight:600;">'
                        f'✅ {opt}</div>',
                        unsafe_allow_html=True,
                    )
                elif i == feedback.get("selected") and not feedback.get("correct"):
                    st.markdown(
                        f'<div style="padding:0.8rem 1.2rem;border-radius:12px;margin:0.4rem 0;'
                        f'background:#fee2e2;border:2px solid #ef4444;text-decoration:line-through;">'
                        f'❌ {opt}</div>',
                        unsafe_allow_html=True,
                    )
                else:
                    st.markdown(
                        f'<div style="padding:0.8rem 1.2rem;border-radius:12px;margin:0.4rem 0;'
                        f'background:#f9fafb;border:1px solid #e5e7eb;color:#9ca3af;">'
                        f'{opt}</div>',
                        unsafe_allow_html=True,
                    )

            if feedback.get("correct"):
                st.success(f"🎉 Correct! {q.get('explanation', '')}")
            else:
                st.error(f"Not quite! {q.get('explanation', '')}")

            st.markdown("")
            _, btn_col, _ = st.columns([1, 2, 1])
            with btn_col:
                next_label = "Next Question ➡️" if current + 1 < total else "See Results 🏆"
                if st.button(next_label, key=f"movie_next_{current}", width="stretch", type="primary"):
                    st.session_state.movie_current += 1
                    st.session_state.movie_last_feedback = None
                    st.rerun()
        else:
            opt_cols = st.columns(2)
            for i, opt in enumerate(q["options"]):
                with opt_cols[i % 2]:
                    if st.button(opt, key=f"movie_opt_{current}_{i}", width="stretch"):
                        is_correct = i == q["answer"]
                        st.session_state.movie_answers.append({
                            "question": q["question"],
                            "selected": i,
                            "selected_text": opt,
                            "correct_answer": q["options"][q["answer"]],
                            "correct": is_correct,
                            "explanation": q.get("explanation", ""),
                            "category": q.get("category", ""),
                        })
                        st.session_state.movie_last_feedback = {
                            "question_id": q["id"],
                            "selected": i,
                            "correct": is_correct,
                        }
                        st.rerun()

    else:
        answers = st.session_state.movie_answers
        correct_count = sum(1 for a in answers if a["correct"])
        score_pct = int((correct_count / total) * 100) if total > 0 else 0
        time_spent = int(time.time() - st.session_state.movie_start_time) if st.session_state.movie_start_time else 0
        minutes, seconds = divmod(time_spent, 60)

        if user:
            db.save_activity_score(
                user["id"], "MovieBuff", "Quiz",
                score_pct, 100, f"{correct_count}/{total} correct", time_spent,
            )

        if score_pct >= 80:
            emoji, msg = "🏆", "Amazing! You're a true Movie Buff!"
        elif score_pct >= 60:
            emoji, msg = "⭐", "Great job! Keep watching and learning!"
        elif score_pct >= 40:
            emoji, msg = "🎬", "Good effort! Time to watch more movies!"
        else:
            emoji, msg = "🍿", "Keep going! Every movie buff starts somewhere!"

        st.markdown(f"""
        <div style="text-align:center;padding:2rem;background:linear-gradient(135deg,#fff1f2,#fef3c7);
             border-radius:20px;margin:1rem 0;">
            <div style="font-size:4rem;">{emoji}</div>
            <h2 style="margin:0.5rem 0;">{score_pct}%</h2>
            <p style="font-size:1.2rem;color:#374151;">{msg}</p>
            <p style="color:#6b7280;">{correct_count} of {total} correct &nbsp;|&nbsp; ⏱️ {minutes}m {seconds}s</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        _, c1, c2, _ = st.columns([1, 2, 2, 1])
        with c1:
            if st.button("🎬 New Quiz", key="movie_new_quiz", width="stretch", type="primary"):
                back_to_movie_home()
                st.rerun()
        with c2:
            if st.button("← Dashboard", key="movie_to_dash", width="stretch"):
                st.session_state.current_page = "user_dashboard"
                st.session_state.selected_activity = None
                st.rerun()

        st.markdown("---")
        st.markdown("### 📋 Review Answers")

        for i, a in enumerate(answers):
            cat_info = mb.CATEGORIES.get(a["category"], {})
            icon = "✅" if a["correct"] else "❌"
            bg = "#f0fdf4" if a["correct"] else "#fef2f2"
            border = "#22c55e" if a["correct"] else "#ef4444"

            with st.expander(f"{icon} Q{i+1}: {a['question']}"):
                if a["correct"]:
                    st.markdown(f"**Your answer:** {a['selected_text']} ✅")
                else:
                    st.markdown(f"**Your answer:** {a['selected_text']} ❌")
                    st.markdown(f"**Correct answer:** {a['correct_answer']} ✅")
                if a.get("explanation"):
                    st.info(f"💡 {a['explanation']}")


# ──────────────────────────────────────────────
# PAGE: Problem Solver Home
# ──────────────────────────────────────────────
def render_problem_solver_home():
    import problem_solver_content as ps

    name = st.session_state.selected_user
    user = db.get_user(name)

    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Back", key="ps_back_to_dash"):
            st.session_state.current_page = "user_dashboard"
            st.session_state.selected_activity = None
            st.rerun()

    st.markdown(f"""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <h1 style="font-size: 2.5rem;">🧩 {name}'s Problem Solver</h1>
        <p style="color: #6b7280; font-size: 1.1rem;">
            Learn to break down real-world problems step by step!
        </p>
    </div>
    """, unsafe_allow_html=True)

    today_ps = db.get_today_scores(user["id"], activity_type="ProblemSolver") if user else []
    total_ps = db.get_scores_history(user["id"], activity_type="ProblemSolver", days=365) if user else []

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div class="score-card"><div class="score-number">📅 {len(today_ps)}</div>'
            f'<div class="score-label">Solved Today</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        if today_ps:
            best = max(s["score"] for s in today_ps)
            st.markdown(
                f'<div class="score-card"><div class="score-number">🎯 {best}%</div>'
                f'<div class="score-label">Today\'s Best</div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="score-card"><div class="score-number">🎯 —</div>'
                '<div class="score-label">Today\'s Best</div></div>',
                unsafe_allow_html=True,
            )
    with col3:
        st.markdown(
            f'<div class="score-card"><div class="score-number">⭐ {len(total_ps)}</div>'
            f'<div class="score-label">Total Solved</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center; padding:1rem; background:#f0fdf4; border-radius:16px;
         border:2px solid #10b981; margin-bottom:1.5rem;">
        <p style="margin:0; font-size:1rem; color:#065f46;">
            <strong>How it works:</strong> You'll get a real-world scenario and 6 thinking steps.
            Each step is a question that teaches you how to break problems into smaller pieces!
        </p>
    </div>
    """, unsafe_allow_html=True)

    category_choice = st.selectbox(
        "Pick a category (optional)",
        ["Any Category"] + [
            f"{ps.CATEGORIES[k]['emoji']} {ps.CATEGORIES[k]['name']}"
            for k in ps.CATEGORIES
        ],
        key="ps_category_filter",
    )

    selected_cat = None
    if category_choice != "Any Category":
        for k, v in ps.CATEGORIES.items():
            if v["name"] in category_choice:
                selected_cat = k
                break

    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        btn_label = "🧩 New Challenge" if today_ps else "🧩 Start Solving"
        if st.button(btn_label, key="ps_start", width="stretch", type="primary"):
            if not _XAI_API_KEY:
                st.error("xAI API key not found. Please set XAI_API_KEY as an environment variable.")
            else:
                with st.status("Creating your scenario...", expanded=True) as status:
                    st.write("Thinking up a fun problem for you...")
                    try:
                        scenario = ps.generate_scenario(_XAI_API_KEY, category=selected_cat)
                        status.update(label="Ready!", state="complete")
                        start_problem_solver(scenario)
                        st.rerun()
                    except Exception as e:
                        status.update(label="Error", state="error")
                        st.error(f"Could not generate scenario: {e}")

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📂 Scenario Categories")

    cat_cols = st.columns(3, gap="medium")
    for idx, (cat_id, cat_info) in enumerate(ps.CATEGORIES.items()):
        with cat_cols[idx % 3]:
            st.markdown(f"""
            <div style="padding:0.8rem;border-radius:12px;border-left:4px solid {cat_info['color']};
                 background:{cat_info['color']}10;margin-bottom:0.8rem;">
                <span style="font-size:1.3rem;">{cat_info['emoji']}</span>
                <strong style="color:{cat_info['color']};"> {cat_info['name']}</strong>
                <br><span style="color:#6b7280;font-size:0.85rem;">e.g. {cat_info['examples']}</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown("### 🧠 The 6 Thinking Steps")
    for i, step in enumerate(ps.STEP_FRAMEWORK):
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:0.8rem;padding:0.5rem 0;">
            <div style="min-width:2.5rem;height:2.5rem;border-radius:50%;background:#10b981;
                 color:white;display:flex;align-items:center;justify-content:center;
                 font-weight:700;font-size:1rem;">{i + 1}</div>
            <div>
                <strong>{step['icon']} {step['name']}</strong>
                <span style="color:#6b7280;"> — {step['description']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ──────────────────────────────────────────────
# PAGE: Problem Solver Practice — Step by Step
# ──────────────────────────────────────────────
def render_problem_solver_practice():
    import problem_solver_content as ps

    name = st.session_state.selected_user
    user = db.get_user(name)
    scenario = st.session_state.ps_scenario
    if not scenario:
        back_to_problem_solver_home()
        st.rerun()
        return

    steps = scenario["steps"]
    total = len(steps)
    current = st.session_state.ps_current_step
    is_done = current >= total

    col_nav1, col_nav_mid, _ = st.columns([1, 4, 1])
    with col_nav1:
        if st.button("← Home", key="ps_back_home"):
            back_to_problem_solver_home()
            st.rerun()
    with col_nav_mid:
        if not is_done:
            st.markdown(f"""
            <div style="text-align:center; color:#6b7280; font-size:0.9rem; padding-top:0.5rem;">
                Step {current + 1} of {total}
            </div>
            """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center;padding:0.5rem 0 0.3rem 0;">
        <h1 style="color:#10b981;margin:0;font-size:1.8rem;">🧩 Problem Solver</h1>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="background:linear-gradient(135deg, #f0fdf4, #ecfdf5);padding:1.2rem;
         border-radius:16px;border:2px solid #10b981;margin-bottom:1rem;">
        <h3 style="margin:0 0 0.5rem 0;color:#065f46;">📝 {scenario['title']}</h3>
        <p style="margin:0;color:#374151;line-height:1.6;">{scenario['description']}</p>
    </div>
    """, unsafe_allow_html=True)

    step_indicators = ""
    for i in range(total):
        if i < current:
            ans = st.session_state.ps_answers[i] if i < len(st.session_state.ps_answers) else None
            if ans and ans.get("correct"):
                step_indicators += (
                    f'<div style="width:2rem;height:2rem;border-radius:50%;background:#10b981;'
                    f'color:white;display:flex;align-items:center;justify-content:center;'
                    f'font-size:0.8rem;font-weight:700;">✓</div>'
                )
            else:
                step_indicators += (
                    f'<div style="width:2rem;height:2rem;border-radius:50%;background:#ef4444;'
                    f'color:white;display:flex;align-items:center;justify-content:center;'
                    f'font-size:0.8rem;font-weight:700;">✗</div>'
                )
        elif i == current and not is_done:
            step_indicators += (
                f'<div style="width:2rem;height:2rem;border-radius:50%;background:#3b82f6;'
                f'color:white;display:flex;align-items:center;justify-content:center;'
                f'font-size:0.8rem;font-weight:700;">{i + 1}</div>'
            )
        else:
            step_indicators += (
                f'<div style="width:2rem;height:2rem;border-radius:50%;background:#e5e7eb;'
                f'color:#9ca3af;display:flex;align-items:center;justify-content:center;'
                f'font-size:0.8rem;font-weight:700;">{i + 1}</div>'
            )

    st.markdown(f"""
    <div style="display:flex;justify-content:center;gap:0.5rem;margin-bottom:1.5rem;">
        {step_indicators}
    </div>
    """, unsafe_allow_html=True)

    if not is_done:
        step = steps[current]
        step_name = step.get("step_name", ps.STEP_FRAMEWORK[current]["name"])
        step_icon = step.get("step_icon", ps.STEP_FRAMEWORK[current]["icon"])
        step_desc = ps.STEP_FRAMEWORK[current]["description"] if current < len(ps.STEP_FRAMEWORK) else ""

        st.markdown(f"""
        <div style="background:#eff6ff;padding:1rem;border-radius:12px;border-left:4px solid #3b82f6;
             margin-bottom:1rem;">
            <strong style="font-size:1.1rem;color:#1e40af;">
                {step_icon} Step {current + 1}: {step_name}
            </strong>
            <br><span style="color:#6b7280;font-size:0.9rem;">{step_desc}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="gk-question-box">
            <div class="gk-question-text">{step['question']}</div>
        </div>
        """, unsafe_allow_html=True)

        last_feedback = st.session_state.get("ps_last_feedback")

        if last_feedback and last_feedback.get("step_idx") == current:
            if last_feedback["correct"]:
                st.markdown(f"""
                <div class="correct-answer" style="text-align:center;">
                    ✅ <strong>Great thinking!</strong> 🎉
                    <br><br><em>{step.get('explanation', '')}</em>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="wrong-answer" style="text-align:center;">
                    Not quite! You picked <strong>{last_feedback['picked']}</strong>.
                    <br>The best approach: <strong>{last_feedback['correct_val']}</strong>
                    <br><br><em>{step.get('explanation', '')}</em>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("")
            _, col_next, _ = st.columns([1, 2, 1])
            with col_next:
                if current < total - 1:
                    if st.button("Next Step ➡️", key="ps_next", width="stretch", type="primary"):
                        st.session_state.ps_current_step += 1
                        st.session_state.ps_last_feedback = None
                        st.rerun()
                else:
                    if st.button("🎉 See Results!", key="ps_results", width="stretch", type="primary"):
                        st.session_state.ps_current_step = total
                        st.session_state.ps_last_feedback = None
                        st.rerun()
        else:
            ans_col1, ans_col2 = st.columns(2, gap="medium")
            for i, opt in enumerate(step["options"]):
                col = ans_col1 if i % 2 == 0 else ans_col2
                with col:
                    label = f"{chr(65 + i)}. {opt}"
                    if st.button(label, key=f"ps_opt_{current}_{i}", width="stretch", type="primary"):
                        is_correct = (i == step["answer"])
                        st.session_state.ps_answers.append({
                            "picked": opt,
                            "correct_val": step["options"][step["answer"]],
                            "correct": is_correct,
                        })
                        st.session_state.ps_last_feedback = {
                            "step_idx": current,
                            "picked": opt,
                            "correct_val": step["options"][step["answer"]],
                            "correct": is_correct,
                        }
                        st.rerun()

    else:
        answers = st.session_state.ps_answers
        correct_count = sum(1 for a in answers if a["correct"])
        score_pct = int((correct_count / total) * 100) if total > 0 else 0
        time_spent = int(time.time() - st.session_state.ps_start_time) if st.session_state.ps_start_time else 0
        minutes, seconds = divmod(time_spent, 60)

        if user:
            db.save_activity_score(
                user["id"], "ProblemSolver", scenario.get("title", "Scenario"),
                score_pct, 100, f"{correct_count}/{total} steps correct", time_spent,
            )

        if score_pct == 100:
            res_emoji, message, res_color = "🏆", "Perfect! You're a master problem solver!", "#10b981"
        elif score_pct >= 70:
            res_emoji, message, res_color = "🌟", "Great thinking! You're learning to break things down!", "#3b82f6"
        elif score_pct >= 50:
            res_emoji, message, res_color = "👍", "Good effort! Practice makes you a better thinker!", "#f59e0b"
        else:
            res_emoji, message, res_color = "💪", "Keep going! Every challenge teaches you something new!", "#ef4444"

        st.markdown(f"""
        <div style="text-align:center;padding:2rem;background:{res_color}10;border-radius:20px;
             border:3px solid {res_color};margin-top:1rem;">
            <div style="font-size:5rem;">{res_emoji}</div>
            <h2 style="color:{res_color};margin:0.5rem 0;font-size:2rem;">
                {correct_count} out of {total} steps correct!
            </h2>
            <p style="font-size:1.2rem;color:#4b5563;">{message}</p>
            <p style="color:#9ca3af;">⏱️ Time: {minutes}m {seconds}s</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        st.markdown("### 🗺️ Your Problem Breakdown")
        st.markdown(f"""
        <div style="background:#f9fafb;padding:1rem;border-radius:12px;border:1px solid #e5e7eb;
             margin-bottom:1rem;">
            <strong>📝 {scenario['title']}</strong>
            <br><span style="color:#6b7280;">{scenario['description'][:150]}...</span>
        </div>
        """, unsafe_allow_html=True)

        for idx, (step, ans) in enumerate(zip(steps, answers)):
            step_name = step.get("step_name", ps.STEP_FRAMEWORK[idx]["name"] if idx < len(ps.STEP_FRAMEWORK) else f"Step {idx+1}")
            step_icon = step.get("step_icon", ps.STEP_FRAMEWORK[idx]["icon"] if idx < len(ps.STEP_FRAMEWORK) else "📌")

            if ans["correct"]:
                st.markdown(f"""
                <div class="correct-answer">
                    <strong>{step_icon} Step {idx+1}: {step_name}</strong><br>
                    {step['question']}<br>
                    ✅ <strong>{ans['correct_val']}</strong>
                    <br><em style="color:#6b7280;">{step.get('explanation', '')}</em>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="wrong-answer">
                    <strong>{step_icon} Step {idx+1}: {step_name}</strong><br>
                    {step['question']}<br>
                    ❌ You said: <strong>{ans['picked']}</strong>
                    &nbsp; ✅ Best approach: <strong>{ans['correct_val']}</strong>
                    <br><em style="color:#6b7280;">{step.get('explanation', '')}</em>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("")
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            if st.button("🧩 Solve Another", key="ps_home_btn", width="stretch", type="primary"):
                back_to_problem_solver_home()
                st.rerun()
        with col_r2:
            if st.button("🏠 Dashboard", key="ps_dashboard", width="stretch"):
                st.session_state.current_page = "user_dashboard"
                st.session_state.ps_scenario = None
                st.session_state.ps_current_step = 0
                st.session_state.ps_answers = []
                st.rerun()


# ──────────────────────────────────────────────
# PAGE: Civics Test Home
# ──────────────────────────────────────────────
def render_civics_home():
    import civics_content as civics

    name = st.session_state.selected_user
    user = db.get_user(name)

    col_nav1, _ = st.columns([1, 6])
    with col_nav1:
        if st.button("← Back", key="civics_back_to_dash"):
            st.session_state.current_page = "user_dashboard"
            st.session_state.selected_activity = None
            st.rerun()

    st.markdown(f"""
    <div style="text-align: center; padding: 0.5rem 0 1rem 0;">
        <h1 style="font-size: 2.5rem;">🏛️ {name}'s US Civics Test</h1>
        <p style="color: #6b7280; font-size: 1.1rem;">Practice the official USCIS 100 Civics Questions</p>
    </div>
    """, unsafe_allow_html=True)

    today = datetime.now().strftime("%Y-%m-%d")
    today_civics = db.get_today_scores(user["id"], activity_type="Civics") if user else []
    total_civics = db.get_scores_history(user["id"], activity_type="Civics", days=365) if user else []

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div class="score-card"><div class="score-number">📅 {today}</div>'
            f'<div class="score-label">Today\'s Date</div></div>',
            unsafe_allow_html=True,
        )
    with col2:
        if today_civics:
            best = max(s["score"] for s in today_civics)
            st.markdown(
                f'<div class="score-card"><div class="score-number">🎯 {best}%</div>'
                f'<div class="score-label">Today\'s Best Score</div></div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="score-card"><div class="score-number">🎯 —</div>'
                '<div class="score-label">Today\'s Score</div></div>',
                unsafe_allow_html=True,
            )
    with col3:
        st.markdown(
            f'<div class="score-card"><div class="score-number">⭐ {len(total_civics)}</div>'
            f'<div class="score-label">Total Tests</div></div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    if today_civics:
        best = max(s["score"] for s in today_civics)
        st.markdown(f"""
        <div style="text-align:center; padding:1rem; background:#dbeafe; border-radius:16px;
             border:2px solid #3b82f6; margin-bottom:1rem;">
            <span style="font-size:2rem;">🎉</span>
            <p style="margin:0.3rem 0; font-size:1.1rem; color:#1e40af;">
                <strong>{len(today_civics)} test{'s' if len(today_civics) > 1 else ''} completed today!</strong>
                &nbsp; Best score: <strong>{best}%</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center; padding:1.5rem;">
        <div style="font-size: 4rem;">🇺🇸</div>
        <h3 style="margin: 0.5rem 0;">{"Ready for another practice test?" if today_civics else "Ready to practice?"}</h3>
        <p style="color: #6b7280;">
            10 questions from the official USCIS question bank.<br>
            You need <strong>6 out of 10</strong> correct to pass — just like the real test!
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Category filter
    st.markdown("")
    category_choice = st.selectbox(
        "Focus on a category (optional)",
        ["All Categories"] + [
            f"{civics.CATEGORIES[k]['emoji']} {civics.CATEGORIES[k]['name']}"
            for k in civics.CATEGORIES
        ],
        key="civics_category_filter",
    )

    selected_cat = None
    if category_choice != "All Categories":
        for k, v in civics.CATEGORIES.items():
            if v["name"] in category_choice:
                selected_cat = k
                break

    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        btn_label = "🚀 New Practice Test" if today_civics else "🚀 Start Practice Test"
        if st.button(btn_label, key="civics_start", width="stretch", type="primary"):
            questions = civics.generate_quiz(num_questions=10, category=selected_cat)
            start_civics_quiz(questions)
            st.rerun()

    # Show category breakdown
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📖 Question Bank Overview")
    st.markdown(
        '<p style="color:#6b7280;margin-bottom:1rem;">'
        "The official USCIS Civics Test covers 100 questions across 9 categories.</p>",
        unsafe_allow_html=True,
    )

    cat_cols = st.columns(3, gap="medium")
    for idx, (cat_id, cat_info) in enumerate(civics.CATEGORIES.items()):
        cat_count = len([q for q in civics.QUESTION_BANK if q["category"] == cat_id])
        cat_color = civics.CATEGORY_COLORS.get(cat_id, "#6b7280")
        with cat_cols[idx % 3]:
            st.markdown(f"""
            <div style="padding:0.8rem;border-radius:12px;border-left:4px solid {cat_color};
                 background:{cat_color}10;margin-bottom:0.8rem;">
                <span style="font-size:1.3rem;">{cat_info['emoji']}</span>
                <strong style="color:{cat_color};"> {cat_info['name']}</strong>
                <br><span style="color:#6b7280;font-size:0.85rem;">{cat_count} questions (Q{cat_info['questions']})</span>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("")
    st.markdown(
        '<p style="text-align:center;color:#9ca3af;font-size:0.85rem;">'
        "⭐ 20 of the 100 questions are designated for the 65/20 special consideration rule.</p>",
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────────────
# PAGE: Civics Practice — Question by Question
# ──────────────────────────────────────────────
def render_civics_practice():
    import civics_content as civics

    name = st.session_state.selected_user
    user = db.get_user(name)
    questions = st.session_state.civics_questions
    current = st.session_state.civics_current
    total = len(questions)
    is_done = current >= total
    passing = civics.get_passing_score(total)

    col_nav1, col_nav_mid, _ = st.columns([1, 4, 1])
    with col_nav1:
        if st.button("← Civics Home", key="civics_back_home"):
            back_to_civics_home()
            st.rerun()
    with col_nav_mid:
        if not is_done:
            st.markdown(f"""
            <div style="text-align:center; color:#6b7280; font-size:0.9rem; padding-top:0.5rem;">
                Question {current + 1} of {total}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align:center; color:#6b7280; font-size:0.9rem; padding-top:0.5rem;">
                🎉 Test Complete!
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align: center; margin-bottom: 0.5rem;">
        <h1 style="color: #dc2626; margin: 0.3rem 0; font-size: 2.2rem;">🏛️ US Civics Practice Test</h1>
    </div>
    """, unsafe_allow_html=True)

    progress = (current / total) if total > 0 else 0
    st.markdown(f"""
    <div style="background:#e5e7eb;border-radius:10px;height:10px;overflow:hidden;margin:0 0 1.5rem 0;">
        <div style="width:{progress*100:.0f}%;height:100%;background:linear-gradient(90deg,#dc2626,#ef4444);border-radius:10px;transition:width 0.4s ease;"></div>
    </div>
    """, unsafe_allow_html=True)

    if not is_done:
        q = questions[current]
        cat_info = civics.CATEGORIES.get(q["category"], {})
        cat_color = civics.CATEGORY_COLORS.get(q["category"], "#6b7280")
        cat_emoji = cat_info.get("emoji", "📚")
        cat_name = cat_info.get("name", "General")

        st.markdown(f"""
        <div class="gk-question-box">
            <span class="gk-topic-badge" style="background:{cat_color}20;color:{cat_color};">{cat_emoji} {cat_name}</span>
            <div class="gk-question-text" style="margin-top:0.8rem;">Q{q['id']}. {q['question']}</div>
        </div>
        """, unsafe_allow_html=True)

        last_feedback = st.session_state.get("civics_last_feedback")

        if last_feedback and last_feedback["idx"] == current:
            if last_feedback["correct"]:
                st.markdown(f"""
                <div class="correct-answer" style="text-align:center;">
                    ✅ <strong>Correct!</strong> 🎉
                </div>
                """, unsafe_allow_html=True)
            else:
                all_valid = last_feedback.get("all_correct", [])
                also_accepted = ""
                if len(all_valid) > 1:
                    also_accepted = (
                        "<br><span style='color:#6b7280;font-size:0.85rem;'>"
                        f"Also accepted: {', '.join(all_valid)}</span>"
                    )
                st.markdown(f"""
                <div class="wrong-answer" style="text-align:center;">
                    Not quite! You picked <strong>{last_feedback['picked']}</strong>.
                    <br>The answer is <strong>{last_feedback['correct_val']}</strong> 💪
                    {also_accepted}
                </div>
                """, unsafe_allow_html=True)

            st.markdown("")
            _, col_next, _ = st.columns([1, 2, 1])
            with col_next:
                if current < total - 1:
                    if st.button("Next Question ➡️", key="civics_next", width="stretch", type="primary"):
                        st.session_state.civics_current += 1
                        st.session_state.civics_last_feedback = None
                        st.rerun()
                else:
                    if st.button("🎉 See Results!", key="civics_results", width="stretch", type="primary"):
                        st.session_state.civics_current = total
                        st.session_state.civics_last_feedback = None
                        st.rerun()
        else:
            ans_col1, ans_col2 = st.columns(2, gap="medium")
            for i, opt in enumerate(q["options"]):
                col = ans_col1 if i % 2 == 0 else ans_col2
                with col:
                    label = f"{chr(65 + i)}. {opt}"
                    if st.button(label, key=f"civics_opt_{current}_{i}", width="stretch", type="primary"):
                        is_correct = (i == q["answer"])
                        st.session_state.civics_answers.append({
                            "picked": opt,
                            "correct_val": q["options"][q["answer"]],
                            "correct": is_correct,
                        })
                        st.session_state.civics_last_feedback = {
                            "idx": current,
                            "picked": opt,
                            "correct_val": q["options"][q["answer"]],
                            "correct": is_correct,
                            "all_correct": q.get("all_correct", []),
                        }
                        st.rerun()

    else:
        answers = st.session_state.civics_answers
        correct_count = sum(1 for a in answers if a["correct"])
        score_pct = int((correct_count / total) * 100) if total > 0 else 0
        time_spent = int(time.time() - st.session_state.civics_start_time) if st.session_state.civics_start_time else 0
        minutes, seconds = divmod(time_spent, 60)
        passed = correct_count >= passing

        if user:
            db.save_activity_score(
                user["id"], "Civics", "Practice Test",
                score_pct, 100, f"{correct_count}/{total} correct", time_spent,
            )

        if passed:
            if score_pct == 100:
                res_emoji, message, res_color = "🏆", "Perfect score! You're ready for the real test!", "#10b981"
            elif score_pct >= 80:
                res_emoji, message, res_color = "🌟", "Excellent! You passed with flying colors!", "#3b82f6"
            else:
                res_emoji, message, res_color = "✅", f"You passed! {correct_count}/{total} correct (need {passing}).", "#10b981"
        else:
            res_emoji, message, res_color = "💪", f"You need {passing} correct to pass. Keep practicing!", "#ef4444"

        pass_text = "PASSED ✅" if passed else "NOT YET ❌"

        st.markdown(f"""
        <div style="text-align:center;padding:2rem;background:{res_color}10;border-radius:20px;border:3px solid {res_color};margin-top:1rem;">
            <div style="font-size:5rem;">{res_emoji}</div>
            <h2 style="color:{res_color};margin:0.5rem 0;font-size:2rem;">{correct_count} out of {total} correct!</h2>
            <p style="font-size:1.3rem;font-weight:700;color:{res_color};">{pass_text}</p>
            <p style="font-size:1.1rem;color:#4b5563;">{message}</p>
            <p style="color:#9ca3af;">⏱️ Time: {minutes}m {seconds}s &nbsp;|&nbsp; Passing: {passing}/{total}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        st.markdown("### 📋 Review Answers")
        for idx, (q, ans) in enumerate(zip(questions, answers)):
            cat_info = civics.CATEGORIES.get(q["category"], {})
            cat_emoji = cat_info.get("emoji", "📚")
            cat_name = cat_info.get("name", "General")
            all_valid = q.get("all_correct", [])
            also_line = ""
            if len(all_valid) > 1 and not ans["correct"]:
                also_line = f"<br><span style='color:#6b7280;font-size:0.85rem;'>Also accepted: {', '.join(all_valid)}</span>"

            if ans["correct"]:
                st.markdown(f"""
                <div class="correct-answer">
                    <span class="gk-topic-badge">{cat_emoji} {cat_name}</span><br>
                    <strong>Q{q['id']}:</strong> {q['question']}<br>
                    ✅ <strong>{ans['correct_val']}</strong>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="wrong-answer">
                    <span class="gk-topic-badge">{cat_emoji} {cat_name}</span><br>
                    <strong>Q{q['id']}:</strong> {q['question']}<br>
                    ❌ You said: <strong>{ans['picked']}</strong> &nbsp; ✅ Answer: <strong>{ans['correct_val']}</strong>
                    {also_line}
                </div>
                """, unsafe_allow_html=True)

        st.markdown("")
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            if st.button("🏛️ Civics Home", key="civics_home_btn", width="stretch", type="primary"):
                back_to_civics_home()
                st.rerun()
        with col_r2:
            if st.button("🏠 Dashboard", key="civics_dashboard", width="stretch"):
                st.session_state.current_page = "user_dashboard"
                st.session_state.civics_questions = []
                st.session_state.civics_current = 0
                st.session_state.civics_answers = []
                st.rerun()


# ──────────────────────────────────────────────
# PAGE: Cube Addition — Learn Adding with Shapes
# ──────────────────────────────────────────────
def render_cube_addition():
    import random as _rnd

    name = st.session_state.selected_user

    # shape_id → (css_class_extra, border_radius, inner_html_fn, singular, plural, emoji)
    SHAPE_TYPES = [
        {
            "id": "cube", "singular": "cube", "plural": "cubes",
            "radius": "16px", "emoji": "🧊",
            "inner": '<div class="shape-shine" style="border-radius:8px;"></div>',
            "anim_left": "shapeBounceLeft", "anim_right": "shapeBounceRight",
        },
        {
            "id": "star", "singular": "star", "plural": "stars",
            "radius": "0", "emoji": "⭐",
            "clip": "polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%)",
            "inner": '<div class="shape-shine" style="border-radius:0; top:25%; left:35%; width:20px; height:20px;"></div>',
            "anim_left": "shapeSpinLeft", "anim_right": "shapeSpinRight",
        },
        {
            "id": "heart", "singular": "heart", "plural": "hearts",
            "radius": "0", "emoji": "❤️",
            "clip": "path('M 40 70 Q 0 40 10 20 A 15 15 0 0 1 40 25 A 15 15 0 0 1 70 20 Q 80 40 40 70 Z')",
            "inner": '<div class="shape-shine" style="border-radius:50%; top:18px; left:18px; width:14px; height:14px;"></div>',
            "anim_left": "shapePulseLeft", "anim_right": "shapePulseRight",
        },
        {
            "id": "balloon", "singular": "balloon", "plural": "balloons",
            "radius": "50% 50% 50% 50% / 40% 40% 60% 60%", "emoji": "🎈",
            "inner": '<div class="shape-shine" style="border-radius:50%; top:12px; left:12px;"></div><div class="balloon-string"></div>',
            "anim_left": "shapeFloatLeft", "anim_right": "shapeFloatRight",
        },
        {
            "id": "flower", "singular": "flower", "plural": "flowers",
            "radius": "50%", "emoji": "🌸",
            "inner": '<div class="flower-center"></div>',
            "anim_left": "shapeBloomLeft", "anim_right": "shapeBloomRight",
            "shadow_extra": ", 16px 0 0 -4px currentColor, -16px 0 0 -4px currentColor, 0 16px 0 -4px currentColor, 0 -16px 0 -4px currentColor",
        },
        {
            "id": "diamond", "singular": "diamond", "plural": "diamonds",
            "radius": "4px", "emoji": "💎",
            "rotate_base": "rotate(45deg)",
            "inner": '<div class="shape-shine" style="border-radius:4px; top:10px; left:10px; width:16px; height:16px;"></div>',
            "anim_left": "shapeTumbleLeft", "anim_right": "shapeTumbleRight",
        },
        {
            "id": "circle", "singular": "ball", "plural": "balls",
            "radius": "50%", "emoji": "🔵",
            "inner": '<div class="shape-shine" style="border-radius:50%;"></div>',
            "anim_left": "shapeRollLeft", "anim_right": "shapeRollRight",
        },
    ]

    COLORS = [
        ("#3b82f6", "Blue"),   ("#ef4444", "Red"),    ("#f59e0b", "Yellow"),
        ("#10b981", "Green"),  ("#8b5cf6", "Purple"), ("#f97316", "Orange"),
        ("#ec4899", "Pink"),   ("#14b8a6", "Teal"),
    ]

    def new_problem():
        total = _rnd.randint(2, 5)
        a = _rnd.randint(1, total - 1)
        b = total - a
        c1, c2 = _rnd.sample(COLORS, 2)
        shape = _rnd.choice(SHAPE_TYPES)
        wrong_opts = [x for x in range(0, 6) if x != total]
        distractors = _rnd.sample(wrong_opts, min(3, len(wrong_opts)))
        jumbled = [total] + distractors
        _rnd.shuffle(jumbled)
        st.session_state.cube_problem = {
            "a": a, "b": b, "total": total,
            "color_a": c1, "color_b": c2,
            "shape": shape,
            "options": jumbled,
        }
        st.session_state.cube_phase = "show"

    col_nav, _ = st.columns([1, 6])
    with col_nav:
        if st.button("← Back", key="cube_back"):
            st.session_state.current_page = "user_dashboard"
            st.session_state.selected_activity = None
            st.rerun()

    st.markdown(f"""
    <div style="text-align:center; padding:0.5rem 0 0.5rem 0;">
        <h1 style="font-size:2.5rem;">🧊 {name}'s Fun Addition</h1>
        <p style="color:#6b7280; font-size:1.1rem;">Watch the shapes appear and count them up!</p>
    </div>
    """, unsafe_allow_html=True)

    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        st.markdown(
            f'<div class="score-card"><div class="score-number">⭐ {st.session_state.cube_score}/{st.session_state.cube_total}</div>'
            f'<div class="score-label">Score</div></div>', unsafe_allow_html=True)
    with sc2:
        pct = int(st.session_state.cube_score / st.session_state.cube_total * 100) if st.session_state.cube_total else 0
        st.markdown(
            f'<div class="score-card"><div class="score-number">🎯 {pct}%</div>'
            f'<div class="score-label">Accuracy</div></div>', unsafe_allow_html=True)
    with sc3:
        st.markdown(
            f'<div class="score-card"><div class="score-number">🔥 {st.session_state.cube_streak}</div>'
            f'<div class="score-label">Streak</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    # ── Intro phase ──
    if st.session_state.cube_phase == "intro":
        st.markdown("""
        <div style="text-align:center; padding:2rem 0;">
            <div style="font-size:4rem;">🧊 ⭐ ❤️ 🎈 🌸 💎 🔵</div>
            <h2 style="margin:1rem 0;">Ready to add fun shapes?</h2>
            <p style="color:#6b7280; font-size:1.15rem;">
                Cubes, stars, hearts, balloons, flowers, diamonds &amp; balls!<br>
                All totals are <b>5 or less</b> — you've got this!
            </p>
        </div>
        """, unsafe_allow_html=True)
        _, bc, _ = st.columns([2, 1, 2])
        with bc:
            if st.button("🚀 Let's Go!", key="cube_start", width="stretch", type="primary"):
                new_problem()
                st.rerun()
        return

    # ── Problem is active ──
    p = st.session_state.cube_problem
    if not p:
        new_problem()
        st.rerun()
        return

    a, b, total = p["a"], p["b"], p["total"]
    hex_a, name_a = p["color_a"]
    hex_b, name_b = p["color_b"]
    shape = p["shape"]
    options = p["options"]

    s_name = shape["singular"]
    p_name = shape["plural"]
    s_emoji = shape["emoji"]
    s_radius = shape["radius"]
    s_clip = shape.get("clip", "")
    s_rotate = shape.get("rotate_base", "")
    s_inner = shape["inner"]
    anim_l = shape["anim_left"]
    anim_r = shape["anim_right"]
    flower_shadow = shape.get("shadow_extra", "")

    sz = 80 if shape["id"] != "diamond" else 60
    gap = 14

    phase = st.session_state.cube_phase

    clip_css = f"clip-path: {s_clip};" if s_clip else ""
    rotate_css = f"transform: {s_rotate};" if s_rotate else ""

    st.markdown(f"""
    <style>
        .cube-arena {{
            display: flex; align-items: center; justify-content: center;
            gap: 24px; padding: 2rem 1rem; min-height: 200px; flex-wrap: wrap;
        }}
        .cube-group {{
            display: flex; gap: {gap}px; align-items: center;
            flex-wrap: wrap; justify-content: center;
        }}
        .shape-block {{
            width: {sz}px; height: {sz}px;
            position: relative; opacity: 0;
            border-radius: {s_radius};
            {clip_css}
            box-shadow: 0 6px 20px rgba(0,0,0,0.15), inset 0 -4px 8px rgba(0,0,0,0.1) {flower_shadow};
        }}
        .shape-shine {{
            position: absolute; top: 8px; left: 8px;
            width: 22px; height: 22px;
            background: rgba(255,255,255,0.45);
        }}
        .balloon-string {{
            position: absolute; bottom: -18px; left: 50%;
            width: 2px; height: 18px;
            background: rgba(0,0,0,0.3); transform: translateX(-50%);
        }}
        .flower-center {{
            position: absolute; top: 50%; left: 50%;
            width: 22px; height: 22px;
            background: #fbbf24; border-radius: 50%;
            transform: translate(-50%, -50%);
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}

        /* ── bounce (cubes) ── */
        @keyframes shapeBounceLeft {{
            0% {{ opacity:0; transform: scale(0) translateX(-80px) {s_rotate}; }}
            60% {{ opacity:1; transform: scale(1.2) translateX(0) {s_rotate}; }}
            80% {{ transform: scale(0.9) {s_rotate}; }}
            100% {{ opacity:1; transform: scale(1) {s_rotate}; }}
        }}
        @keyframes shapeBounceRight {{
            0% {{ opacity:0; transform: scale(0) translateX(80px) {s_rotate}; }}
            60% {{ opacity:1; transform: scale(1.2) translateX(0) {s_rotate}; }}
            80% {{ transform: scale(0.9) {s_rotate}; }}
            100% {{ opacity:1; transform: scale(1) {s_rotate}; }}
        }}
        /* ── spin (stars) ── */
        @keyframes shapeSpinLeft {{
            0% {{ opacity:0; transform: scale(0) rotate(-360deg); }}
            70% {{ opacity:1; transform: scale(1.15) rotate(15deg); }}
            100% {{ opacity:1; transform: scale(1) rotate(0deg); }}
        }}
        @keyframes shapeSpinRight {{
            0% {{ opacity:0; transform: scale(0) rotate(360deg); }}
            70% {{ opacity:1; transform: scale(1.15) rotate(-15deg); }}
            100% {{ opacity:1; transform: scale(1) rotate(0deg); }}
        }}
        /* ── pulse (hearts) ── */
        @keyframes shapePulseLeft {{
            0% {{ opacity:0; transform: scale(0); }}
            50% {{ opacity:1; transform: scale(1.35); }}
            70% {{ transform: scale(0.85); }}
            85% {{ transform: scale(1.1); }}
            100% {{ opacity:1; transform: scale(1); }}
        }}
        @keyframes shapePulseRight {{
            0% {{ opacity:0; transform: scale(0); }}
            50% {{ opacity:1; transform: scale(1.35); }}
            70% {{ transform: scale(0.85); }}
            85% {{ transform: scale(1.1); }}
            100% {{ opacity:1; transform: scale(1); }}
        }}
        /* ── float (balloons) ── */
        @keyframes shapeFloatLeft {{
            0% {{ opacity:0; transform: translateY(120px) scale(0.5); }}
            60% {{ opacity:1; transform: translateY(-15px) scale(1.1); }}
            80% {{ transform: translateY(5px) scale(0.95); }}
            100% {{ opacity:1; transform: translateY(0) scale(1); }}
        }}
        @keyframes shapeFloatRight {{
            0% {{ opacity:0; transform: translateY(120px) scale(0.5); }}
            60% {{ opacity:1; transform: translateY(-15px) scale(1.1); }}
            80% {{ transform: translateY(5px) scale(0.95); }}
            100% {{ opacity:1; transform: translateY(0) scale(1); }}
        }}
        /* ── bloom (flowers) ── */
        @keyframes shapeBloomLeft {{
            0% {{ opacity:0; transform: scale(0) rotate(-90deg); }}
            60% {{ opacity:1; transform: scale(1.2) rotate(10deg); }}
            100% {{ opacity:1; transform: scale(1) rotate(0deg); }}
        }}
        @keyframes shapeBloomRight {{
            0% {{ opacity:0; transform: scale(0) rotate(90deg); }}
            60% {{ opacity:1; transform: scale(1.2) rotate(-10deg); }}
            100% {{ opacity:1; transform: scale(1) rotate(0deg); }}
        }}
        /* ── tumble (diamonds) ── */
        @keyframes shapeTumbleLeft {{
            0% {{ opacity:0; transform: rotate(45deg) scale(0) translateX(-60px); }}
            60% {{ opacity:1; transform: rotate(45deg) scale(1.15) translateX(0); }}
            100% {{ opacity:1; transform: rotate(45deg) scale(1) translateX(0); }}
        }}
        @keyframes shapeTumbleRight {{
            0% {{ opacity:0; transform: rotate(45deg) scale(0) translateX(60px); }}
            60% {{ opacity:1; transform: rotate(45deg) scale(1.15) translateX(0); }}
            100% {{ opacity:1; transform: rotate(45deg) scale(1) translateX(0); }}
        }}
        /* ── roll (balls) ── */
        @keyframes shapeRollLeft {{
            0% {{ opacity:0; transform: translateX(-100px) rotate(-360deg) scale(0.5); }}
            70% {{ opacity:1; transform: translateX(8px) rotate(10deg) scale(1.05); }}
            100% {{ opacity:1; transform: translateX(0) rotate(0deg) scale(1); }}
        }}
        @keyframes shapeRollRight {{
            0% {{ opacity:0; transform: translateX(100px) rotate(360deg) scale(0.5); }}
            70% {{ opacity:1; transform: translateX(-8px) rotate(-10deg) scale(1.05); }}
            100% {{ opacity:1; transform: translateX(0) rotate(0deg) scale(1); }}
        }}

        .shape-anim-left {{
            animation: {anim_l} 0.7s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
        }}
        .shape-anim-right {{
            animation: {anim_r} 0.7s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
        }}

        .operator-sign {{
            font-size: 3.5rem; font-weight: 900; opacity: 0;
            animation: fadeInBounce 0.5s ease forwards;
            animation-delay: {a * 0.3 + 0.2:.2f}s;
        }}
        .equals-sign {{
            font-size: 3.5rem; font-weight: 900; opacity: 0;
            animation: fadeInBounce 0.5s ease forwards;
            animation-delay: {(a + b) * 0.3 + 0.5:.2f}s;
        }}
        @keyframes fadeInBounce {{
            0% {{ opacity:0; transform: scale(0.3); }}
            70% {{ opacity:1; transform: scale(1.2); }}
            100% {{ opacity:1; transform: scale(1); }}
        }}
        .question-mark-box {{
            width: {sz + 10}px; height: {sz + 10}px;
            border-radius: 18px; border: 4px dashed #9ca3af;
            display: flex; align-items: center; justify-content: center;
            font-size: 3rem; font-weight: 900; color: #9ca3af;
            opacity: 0; animation: fadeInBounce 0.6s ease forwards;
            animation-delay: {(a + b) * 0.3 + 0.7:.2f}s;
        }}
        .answer-reveal {{
            width: {sz + 10}px; height: {sz + 10}px; border-radius: 18px;
            display: flex; align-items: center; justify-content: center;
            font-size: 3rem; font-weight: 900;
            animation: answerPop 0.7s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
        }}
        @keyframes answerPop {{
            0% {{ transform: scale(0) rotate(-10deg); }}
            50% {{ transform: scale(1.3) rotate(5deg); }}
            100% {{ transform: scale(1) rotate(0deg); }}
        }}
        .cube-label {{
            text-align: center; font-size: 1.1rem; font-weight: 700;
            margin-top: 0.5rem; opacity: 0; animation: fadeInBounce 0.5s ease forwards;
        }}
        .cube-label-a {{ animation-delay: {a * 0.3 + 0.1:.2f}s; color: {hex_a}; }}
        .cube-label-b {{ animation-delay: {(a + b) * 0.3 + 0.1:.2f}s; color: {hex_b}; }}
        .equation-text {{
            text-align: center; font-size: 2rem; font-weight: 800; margin: 1rem 0;
            opacity: 0; animation: fadeInBounce 0.6s ease forwards;
            animation-delay: {(a + b) * 0.3 + 0.9:.2f}s;
        }}
        .celebrate-text {{
            text-align: center; font-size: 2.5rem; font-weight: 900;
            animation: celebrateWave 1s ease forwards;
        }}
        @keyframes celebrateWave {{
            0% {{ transform: scale(0); opacity:0; }}
            50% {{ transform: scale(1.3); opacity:1; }}
            70% {{ transform: scale(0.9); }}
            100% {{ transform: scale(1); opacity:1; }}
        }}
        @keyframes sparkle {{
            0%,100% {{ opacity:0; transform:scale(0) rotate(0deg); }}
            50% {{ opacity:1; transform:scale(1) rotate(180deg); }}
        }}
        .sparkle {{
            position: fixed; font-size: 2rem;
            animation: sparkle 1.5s ease-in-out infinite;
            pointer-events: none; z-index: 9999;
        }}
        .wrong-shake {{ animation: shakeIt 0.5s ease; }}
        @keyframes shakeIt {{
            0%,100% {{ transform: translateX(0); }}
            20% {{ transform: translateX(-15px); }}
            40% {{ transform: translateX(15px); }}
            60% {{ transform: translateX(-10px); }}
            80% {{ transform: translateX(10px); }}
        }}
        .ans-btn {{
            font-size: 1.8rem !important; font-weight: 800 !important;
            padding: 0.8rem !important; border-radius: 16px !important;
        }}
        /* idle wobble for balloons & flowers */
        @keyframes gentleFloat {{
            0%,100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-6px); }}
        }}
    </style>
    """, unsafe_allow_html=True)

    def shape_html(color_hex, count, anim_cls, delay_start=0):
        html = ""
        for i in range(count):
            d = delay_start + i * 0.3
            html += f"""
            <div class="shape-block {anim_cls}" style="
                background: linear-gradient(135deg, {color_hex}, {color_hex}cc);
                animation-delay: {d:.2f}s; color: {color_hex};
            ">{s_inner}</div>"""
        return html

    shapes_a = shape_html(hex_a, a, "shape-anim-left", delay_start=0.1)
    shapes_b = shape_html(hex_b, b, "shape-anim-right", delay_start=a * 0.3 + 0.5)

    if phase in ("show", "answer"):
        qmark = '<div class="question-mark-box">?</div>'
    elif phase == "correct":
        qmark = f'<div class="answer-reveal" style="background:linear-gradient(135deg,#10b981,#059669);color:white;">{total}</div>'
    elif phase == "wrong":
        qmark = f'<div class="answer-reveal wrong-shake" style="background:linear-gradient(135deg,#ef4444,#dc2626);color:white;">{total}</div>'
    else:
        qmark = '<div class="question-mark-box">?</div>'

    label_a = f"{a} {name_a} {s_name if a == 1 else p_name}"
    label_b = f"{b} {name_b} {s_name if b == 1 else p_name}"

    st.markdown(f"""
    <div class="cube-arena">
        <div>
            <div class="cube-group">{shapes_a}</div>
            <div class="cube-label cube-label-a">{label_a}</div>
        </div>
        <div class="operator-sign" style="color:#374151;">+</div>
        <div>
            <div class="cube-group">{shapes_b}</div>
            <div class="cube-label cube-label-b">{label_b}</div>
        </div>
        <div class="equals-sign" style="color:#374151;">=</div>
        <div>{qmark}</div>
    </div>
    """, unsafe_allow_html=True)

    if phase in ("show", "answer"):
        st.markdown(f"""
        <div class="equation-text" style="color:#374151;">
            {s_emoji} {a} + {b} = ❓
        </div>
        """, unsafe_allow_html=True)

    # ── Show → ready ──
    if phase == "show":
        _, cc, _ = st.columns([2, 1, 2])
        with cc:
            if st.button("🤔 I'm Ready to Answer!", key="cube_ready", width="stretch", type="primary"):
                st.session_state.cube_phase = "answer"
                st.rerun()

    # ── Answer → pick ──
    elif phase == "answer":
        st.markdown(f"""
        <div style="text-align:center; margin:1rem 0;">
            <h3 style="color:#374151;">How many {p_name} are there in total?</h3>
        </div>
        """, unsafe_allow_html=True)

        n_opts = len(options)
        btn_cols = st.columns(n_opts)
        for i, opt in enumerate(options):
            with btn_cols[i]:
                if st.button(f"{s_emoji} {opt}", key=f"cube_ans_{i}_{opt}", width="stretch"):
                    st.session_state.cube_total += 1
                    if opt == total:
                        st.session_state.cube_score += 1
                        st.session_state.cube_streak += 1
                        st.session_state.cube_phase = "correct"
                    else:
                        st.session_state.cube_streak = 0
                        st.session_state.cube_phase = "wrong"
                    st.rerun()

    # ── Correct ──
    elif phase == "correct":
        sparkles = ""
        celebration_emojis = ["⭐", "🌟", "✨", "🎉", "🎊", "💫", s_emoji]
        for i in range(15):
            x = _rnd.randint(5, 95)
            y = _rnd.randint(5, 85)
            delay = _rnd.uniform(0, 1.5)
            sparkles += f'<div class="sparkle" style="left:{x}%;top:{y}%;animation-delay:{delay:.1f}s;">{_rnd.choice(celebration_emojis)}</div>'

        st.markdown(f"""
        {sparkles}
        <div class="celebrate-text" style="color:#10b981;">
            🎉 Amazing! {a} + {b} = {total}! 🎉
        </div>
        <div style="text-align:center; margin-top:0.5rem;">
            <p style="font-size:1.3rem; color:#374151;">
                {" ".join([s_emoji] * a)} <b>+</b> {" ".join([s_emoji] * b)} <b>=</b> {" ".join([s_emoji] * total)}
            </p>
            <p style="font-size:1.2rem; color:#6b7280; margin-top:0.3rem;">
                {label_a} and {label_b} make <b>{total}</b> {p_name}!
            </p>
        </div>
        """, unsafe_allow_html=True)

        _, nc, _ = st.columns([2, 1, 2])
        with nc:
            if st.button("▶️ Next Problem!", key="cube_next_ok", width="stretch", type="primary"):
                new_problem()
                st.rerun()

    # ── Wrong ──
    elif phase == "wrong":
        st.markdown(f"""
        <div class="celebrate-text" style="color:#ef4444;">
            Oops! Let's count again! 🤗
        </div>
        <div style="text-align:center; margin-top:0.5rem;">
            <p style="font-size:1.4rem; color:#374151;">
                Count them: {" ".join([s_emoji] * a)} <b>+</b> {" ".join([s_emoji] * b)}
            </p>
            <p style="font-size:1.6rem; font-weight:800; color:#10b981; margin-top:0.5rem;">
                {a} + {b} = {total} ✅
            </p>
            <p style="font-size:1.1rem; color:#6b7280;">
                {label_a} and {label_b} make <b>{total}</b> {p_name}!
            </p>
        </div>
        """, unsafe_allow_html=True)

        _, nc, _ = st.columns([2, 1, 2])
        with nc:
            if st.button("▶️ Try Another!", key="cube_next_wrong", width="stretch", type="primary"):
                new_problem()
                st.rerun()


# ──────────────────────────────────────────────
# Main Router
# ──────────────────────────────────────────────
page = st.session_state.current_page

if page == "home":
    render_home()
elif page == "user_dashboard":
    render_user_dashboard()
elif page == "reading_home":
    render_reading_home()
elif page == "reading_story":
    render_reading_story()
elif page == "generate_story":
    render_generate_story()
elif page == "math_home":
    render_math_home()
elif page == "math_practice":
    render_math_practice()
elif page == "arjun_stories_home":
    render_arjun_stories_home()
elif page == "gk_home":
    render_gk_home()
elif page == "gk_practice":
    render_gk_practice()
elif page == "sight_words_home":
    render_sight_words_home()
elif page == "sight_words_practice":
    render_sight_words_practice()
elif page == "map_explorer_home":
    render_map_explorer_home()
elif page == "map_explorer_practice":
    render_map_explorer_practice()
elif page == "mental_math_home":
    render_mental_math_home()
elif page == "mental_math_practice":
    render_mental_math_practice()
elif page == "science_home":
    render_science_home()
elif page == "science_practice":
    render_science_practice()
elif page == "logo_id_home":
    render_logo_id_home()
elif page == "logo_id_practice":
    render_logo_id_practice()
elif page == "movie_buff_home":
    render_movie_buff_home()
elif page == "movie_buff_practice":
    render_movie_buff_practice()
elif page == "problem_solver_home":
    render_problem_solver_home()
elif page == "problem_solver_practice":
    render_problem_solver_practice()
elif page == "civics_home":
    render_civics_home()
elif page == "civics_practice":
    render_civics_practice()
elif page == "cube_addition":
    render_cube_addition()
else:
    render_home()
