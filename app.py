"""
1% Better Every Day - Main Application
A daily improvement tracker for kids and adults.
"""

import os
import streamlit as st
import database as db
from datetime import datetime
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

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="score-card"><div class="score-number">🔥 {streak}</div><div class="score-label">Day Streak</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="score-card"><div class="score-number">📅 {total_days}</div><div class="score-label">Total Days</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="score-card"><div class="score-number">✅ {len(today_scores)}</div><div class="score-label">Activities Today</div></div>', unsafe_allow_html=True)
    with col4:
        avg_display = f"{sum(s['score'] for s in today_scores) / len(today_scores):.0f}%" if today_scores else "—"
        st.markdown(f'<div class="score-card"><div class="score-number">⭐ {avg_display}</div><div class="score-label">Avg Score Today</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)

    if name == "Krish":
        st.markdown("### 📚 Choose Your Activity")
        st.markdown("")

        act_col1, act_col2, act_col3 = st.columns(3, gap="large")
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
    elif name == "Arjun":
        st.markdown("### 📚 Choose Your Activity")
        st.markdown("")

        act_col1, act_col2, act_col3 = st.columns(3, gap="large")
        with act_col1:
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

        with act_col2:
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

        with act_col3:
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

    # Progress chart
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown("### 📊 Progress Over Time")

    history = db.get_scores_history(user["id"], days=30)
    if history:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[h["log_date"] for h in history],
            y=[h["score"] for h in history],
            mode="lines+markers",
            marker=dict(size=10, color="#667eea"),
            line=dict(color="#667eea", width=3),
            text=[h["activity_name"] for h in history],
            hovertemplate="<b>%{text}</b><br>Score: %{y}%<br>Date: %{x}<extra></extra>",
        ))
        fig.update_layout(
            xaxis_title="Date", yaxis_title="Score (%)",
            yaxis=dict(range=[0, 105]), template="plotly_white",
            height=350, margin=dict(l=20, r=20, t=20, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown('<div style="text-align:center;padding:2rem;color:#9ca3af;"><div style="font-size:3rem;">📈</div><p>Complete activities to see your progress chart!</p></div>', unsafe_allow_html=True)


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
                        db.save_activity_score(user["id"], "Reading", story["title"], score_pct, 100, f"{correct}/{total} correct")

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
            db.save_activity_score(user["id"], "Math", level["title"], score_pct, 100, f"{correct}/{total} correct")

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
    st.markdown('<p style="color:#6b7280;">Choose a category, pick a topic, write your own — or let us surprise you!</p>', unsafe_allow_html=True)

    all_topics = asc.get_all_topics()

    # Top action row: Random + Write Your Own
    col_random, col_custom = st.columns(2, gap="medium")
    with col_random:
        if st.button("🎲 Surprise Me — Random Topic!", key="arjun_random_topic", width="stretch", type="primary"):
            cat, topic = asc.get_random_topic()
            _generate_and_launch_arjun_story(topic, user)
            return
    with col_custom:
        pass

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

    # Build tab list: static categories + Current Events
    tab_labels = [f"{asc.TOPIC_EMOJIS.get(cat, '📖')} {cat}" for cat in all_topics]
    tab_labels.append(f"{asc.TOPIC_EMOJIS.get('Current Events', '📰')} Current Events")

    tabs = st.tabs(tab_labels)

    # Static category tabs
    for tab, (category, topics) in zip(tabs[:-1], all_topics.items()):
        with tab:
            topic_cols = st.columns(2, gap="medium")
            for idx, topic in enumerate(topics):
                with topic_cols[idx % 2]:
                    short_title = topic.split("—")[0].strip() if "—" in topic else topic
                    subtitle = topic.split("—")[1].strip() if "—" in topic else ""
                    st.markdown(f"""
                    <div style="background:#f8f9ff;border-radius:12px;padding:0.8rem 1rem;
                                margin-bottom:0.5rem;border-left:4px solid #6366f1;">
                        <div style="font-weight:600;font-size:0.95rem;color:#1f2937;">{short_title}</div>
                        {"<div style='color:#6b7280;font-size:0.8rem;'>" + subtitle + "</div>" if subtitle else ""}
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button("📝 Generate", key=f"gen_{category}_{idx}", width="stretch"):
                        _generate_and_launch_arjun_story(topic, user)
                        return

    # Current Events tab (fetched from Grok)
    with tabs[-1]:
        if "arjun_current_events" not in st.session_state:
            st.session_state.arjun_current_events = None

        if st.session_state.arjun_current_events is None:
            if st.button("🔄 Load Current Events", key="load_current_events", width="stretch", type="primary"):
                with st.spinner("Asking AI for kid-friendly current events..."):
                    events = asc.fetch_current_events(_XAI_API_KEY)
                    st.session_state.arjun_current_events = events if events else []
                    st.rerun()
            st.markdown("""
            <div style="text-align:center;padding:2rem;color:#9ca3af;">
                <div style="font-size:3rem;">📰</div>
                <p>Click above to load fresh, kid-appropriate current event topics!</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            events = st.session_state.arjun_current_events
            if events:
                col_refresh, _ = st.columns([2, 5])
                with col_refresh:
                    if st.button("🔄 Refresh", key="refresh_current_events"):
                        st.session_state.arjun_current_events = None
                        st.rerun()
                st.markdown("")
                topic_cols = st.columns(2, gap="medium")
                for idx, topic in enumerate(events):
                    with topic_cols[idx % 2]:
                        short_title = topic.split("—")[0].strip() if "—" in topic else topic
                        subtitle = topic.split("—")[1].strip() if "—" in topic else ""
                        st.markdown(f"""
                        <div style="background:#fffbeb;border-radius:12px;padding:0.8rem 1rem;
                                    margin-bottom:0.5rem;border-left:4px solid #f59e0b;">
                            <div style="font-weight:600;font-size:0.95rem;color:#1f2937;">{short_title}</div>
                            {"<div style='color:#6b7280;font-size:0.8rem;'>" + subtitle + "</div>" if subtitle else ""}
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button("📝 Generate", key=f"gen_current_{idx}", width="stretch"):
                            _generate_and_launch_arjun_story(topic, user)
                            return
            else:
                st.info("No current events found. Try refreshing!")
                if st.button("🔄 Try Again", key="retry_current_events"):
                    st.session_state.arjun_current_events = None
                    st.rerun()


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
                questions = gk.generate_daily_questions(_XAI_API_KEY, user_name=name)
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
            db.save_activity_score(user["id"], "GK", "Daily Quiz", score_pct, 100, f"{correct}/{total} correct")

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

    cols = st.columns(3, gap="large")
    for i, lvl in enumerate(sw.LEVELS):
        word_count = len(sw.WORD_BANK.get(lvl["id"], []))
        with cols[i]:
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
                100, 100, f"{total} words practiced",
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
                score_pct, 100, f"{correct_count}/{total} correct",
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

            if ans["correct"]:
                st.markdown(f"""
                <div class="correct-answer">
                    <span class="gk-topic-badge">{cat_emoji} {cat_name}</span><br>
                    <strong>Q{idx+1}:</strong> {q['question']}<br>
                    ✅ <strong>{ans['correct_val']}</strong>
                    <br><em style="color:#6b7280;">{q.get('explanation', '')}</em>
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
                score_pct, 100, f"{correct_count}/{total} correct",
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
elif page == "civics_home":
    render_civics_home()
elif page == "civics_practice":
    render_civics_practice()
else:
    render_home()
