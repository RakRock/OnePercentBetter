"""
Database module for the 1% Better Every Day app.
Uses SQLite for persistent storage of user activity, streaks, and scores.
"""

import json
import sqlite3
import os
from datetime import datetime, timedelta
from contextlib import contextmanager

DB_PATH = os.environ.get("ONEPERCENT_DB", "onepercent.db")


@contextmanager
def get_connection():
    """Context manager for database connections."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    """Initialize database tables if they don't exist."""
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                avatar_emoji TEXT DEFAULT '🧒',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS daily_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                log_date DATE NOT NULL,
                logged_in_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(user_id, log_date)
            );

            CREATE TABLE IF NOT EXISTS activity_scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                activity_type TEXT NOT NULL,
                activity_name TEXT NOT NULL,
                score INTEGER DEFAULT 0,
                max_score INTEGER DEFAULT 100,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                log_date DATE NOT NULL,
                details TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS reading_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                story_id TEXT NOT NULL,
                story_title TEXT NOT NULL,
                questions_total INTEGER DEFAULT 0,
                questions_correct INTEGER DEFAULT 0,
                time_spent_seconds INTEGER DEFAULT 0,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                log_date DATE NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS gk_daily_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                quiz_date DATE NOT NULL,
                questions_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(user_id, quiz_date)
            );

            CREATE TABLE IF NOT EXISTS arjun_vocab_progress (
                user_id INTEGER PRIMARY KEY,
                next_word_index INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS ec3_practice_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                unit_id INTEGER NOT NULL,
                question_ids TEXT NOT NULL,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS ec3_practice_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL UNIQUE,
                user_id INTEGER NOT NULL,
                session_kind TEXT NOT NULL,
                unit_id INTEGER,
                unit_label TEXT NOT NULL,
                score_pct INTEGER NOT NULL,
                correct_count INTEGER NOT NULL,
                total_count INTEGER NOT NULL,
                time_spent_seconds INTEGER DEFAULT 0,
                report_json TEXT NOT NULL,
                failed_json TEXT NOT NULL DEFAULT '[]',
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                log_date DATE NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE INDEX IF NOT EXISTS idx_ec3_results_user_date
                ON ec3_practice_results(user_id, log_date DESC);

            CREATE TABLE IF NOT EXISTS linear_eq_week_config (
                id INTEGER PRIMARY KEY CHECK (id = 1),
                week_label TEXT NOT NULL DEFAULT '',
                config_json TEXT NOT NULL DEFAULT '{}',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS cvc_review_words (
                user_id INTEGER NOT NULL,
                level_id TEXT NOT NULL,
                word TEXT NOT NULL,
                phonics_tip TEXT DEFAULT '',
                wrong_count INTEGER DEFAULT 1,
                last_wrong_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, level_id, word),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS daily_summaries (
                user_id INTEGER NOT NULL,
                log_date TEXT NOT NULL,
                activities_count INTEGER DEFAULT 0,
                avg_score_pct INTEGER DEFAULT 0,
                time_spent_seconds INTEGER DEFAULT 0,
                updated_at TEXT,
                PRIMARY KEY (user_id, log_date),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS harshit_math_progress (
                user_id INTEGER NOT NULL,
                phase_id TEXT NOT NULL DEFAULT 'phase1',
                day_id INTEGER NOT NULL,
                problem_id TEXT NOT NULL,
                current_node TEXT NOT NULL DEFAULT 'start',
                step_index INTEGER NOT NULL DEFAULT 0,
                visual_complete INTEGER NOT NULL DEFAULT 0,
                state_json TEXT NOT NULL DEFAULT '{}',
                completed_at TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, phase_id, day_id, problem_id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS harshit_math_day_status (
                user_id INTEGER NOT NULL,
                phase_id TEXT NOT NULL DEFAULT 'phase1',
                day_id INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'not_started',
                problems_completed INTEGER NOT NULL DEFAULT 0,
                problems_total INTEGER NOT NULL DEFAULT 0,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, phase_id, day_id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS harshit_prereq_chapter_status (
                user_id INTEGER NOT NULL,
                prereq_id INTEGER NOT NULL,
                chapter_num INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'not_started',
                notes TEXT DEFAULT '',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, prereq_id, chapter_num),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS harshit_prereq_week_config (
                prereq_id INTEGER PRIMARY KEY,
                week_label TEXT NOT NULL DEFAULT '',
                config_json TEXT NOT NULL DEFAULT '{}',
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS harshit_practice_sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                prereq_id INTEGER NOT NULL,
                question_ids TEXT NOT NULL,
                question_texts TEXT NOT NULL,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE INDEX IF NOT EXISTS idx_harshit_practice_user_prereq
                ON harshit_practice_sessions(user_id, prereq_id, completed_at DESC);
        """)
        # Migration: add time_spent_seconds if missing (added after initial schema)
        try:
            conn.execute("ALTER TABLE activity_scores ADD COLUMN time_spent_seconds INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            pass
        for stmt in (
            "ALTER TABLE activity_scores ADD COLUMN sync_id TEXT",
            "ALTER TABLE reading_progress ADD COLUMN sync_id TEXT",
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_activity_scores_sync_id ON activity_scores(sync_id)",
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_reading_progress_sync_id ON reading_progress(sync_id)",
        ):
            try:
                conn.execute(stmt)
            except sqlite3.OperationalError:
                pass

        # Seed default users
        default_users = [
            ("Arjun", "🦁"),
            ("Krish", "🚀"),
            ("Sangeetha", "🌸"),
            ("Rakesh", "⚡"),
            ("Harshit Sai", "📐"),
        ]
        for name, emoji in default_users:
            conn.execute(
                "INSERT OR IGNORE INTO users (name, avatar_emoji) VALUES (?, ?)",
                (name, emoji),
            )


def get_user(name: str) -> dict | None:
    """Get a user by name."""
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE name = ?", (name,)).fetchone()
        return dict(row) if row else None


def get_all_users() -> list[dict]:
    """All users ordered by id."""
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM users ORDER BY id").fetchall()
    return [dict(r) for r in rows]


def get_user_log_dates(user_id: int) -> list[str]:
    """Distinct login dates for a user (YYYY-MM-DD)."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT DISTINCT log_date FROM daily_logs WHERE user_id = ? ORDER BY log_date",
            (user_id,),
        ).fetchall()
    return [str(r["log_date"]) for r in rows]


def get_user_by_id(user_id: int) -> dict | None:
    """Get a user by id."""
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        return dict(row) if row else None


def _sharepoint_push(method_name: str, **kwargs) -> None:
    """Best-effort SharePoint sync; never raises."""
    try:
        import google_sheets_sync as gss

        if gss.skip_cloud_sync():
            return
        import sharepoint_sync as sps

        if sps.is_configured():
            getattr(sps, method_name)(**kwargs)
    except Exception:
        pass


def record_daily_login(user_id: int):
    """Record a daily login for the user (once per day)."""
    today = datetime.now().strftime("%Y-%m-%d")
    with get_connection() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO daily_logs (user_id, log_date) VALUES (?, ?)",
            (user_id, today),
        )
    user = get_user_by_id(user_id)
    if user:
        _sharepoint_push(
            "persist_daily_login",
            user_name=user["name"],
            user_id=user_id,
            log_date=today,
        )


def get_login_streak(user_id: int) -> int:
    """Calculate the current consecutive login streak for a user.

    The streak counts backwards from the most recent login.  It stays
    alive as long as the most recent login is today or yesterday (so a
    user doesn't lose their streak before they've had a chance to open
    the app today).
    """
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT DISTINCT log_date FROM daily_logs WHERE user_id = ? ORDER BY log_date DESC",
            (user_id,),
        ).fetchall()

    if not rows:
        return 0

    today = datetime.now().date()
    dates = [datetime.strptime(r["log_date"], "%Y-%m-%d").date() for r in rows]

    # The streak is only valid if the most recent login is today or yesterday
    if (today - dates[0]).days > 1:
        return 0

    streak = 1
    for i in range(1, len(dates)):
        if (dates[i - 1] - dates[i]).days == 1:
            streak += 1
        else:
            break

    return streak


def get_total_login_days(user_id: int) -> int:
    """Get total number of days the user has logged in."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT COUNT(DISTINCT log_date) as total FROM daily_logs WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        return row["total"] if row else 0


def save_activity_score(
    user_id: int,
    activity_type: str,
    activity_name: str,
    score: int,
    max_score: int,
    details: str = "",
    time_spent_seconds: int = 0,
    *,
    flush_sheets: bool = True,
):
    """Save a score for an activity."""
    today = datetime.now().strftime("%Y-%m-%d")
    completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        import sharepoint_sync as sps

        sync_id = sps.new_sync_id(f"activity-{user_id}")
    except Exception:
        sync_id = f"activity-{user_id}-{datetime.now().timestamp()}"

    with get_connection() as conn:
        conn.execute(
            """INSERT INTO activity_scores 
               (user_id, activity_type, activity_name, score, max_score, log_date, details,
                time_spent_seconds, sync_id, completed_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                user_id,
                activity_type,
                activity_name,
                score,
                max_score,
                today,
                details,
                time_spent_seconds,
                sync_id,
                completed_at,
            ),
        )

    user = get_user_by_id(user_id)
    if user:
        _sharepoint_push(
            "persist_activity_score",
            sync_id=sync_id,
            user_name=user["name"],
            user_id=user_id,
            activity_type=activity_type,
            activity_name=activity_name,
            score=score,
            max_score=max_score,
            log_date=today,
            details=details,
            time_spent_seconds=time_spent_seconds,
            completed_at=completed_at,
        )
        if flush_sheets:
            _google_sheets_flush_user_session(user_id, today)


def _google_sheets_flush_user_session(user_id: int, log_date: str) -> None:
    """Best-effort Google Sheets sync once after a session completes."""
    try:
        import google_sheets_sync as gss

        if gss.cloud_sync_enabled():
            gss.flush_user_session_to_sheets(user_id, log_date)
    except Exception:
        pass


def save_ec3_practice_session(user_id: int, unit_id: int, question_ids: list[str]) -> None:
    """Record question IDs from a completed Edgenuity practice set (for de-duplication)."""
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO ec3_practice_sessions (user_id, unit_id, question_ids) VALUES (?, ?, ?)",
            (user_id, unit_id, json.dumps(question_ids)),
        )
        stale = conn.execute(
            """SELECT id FROM ec3_practice_sessions
               WHERE user_id = ? AND unit_id = ?
               ORDER BY completed_at DESC
               LIMIT -1 OFFSET 20""",
            (user_id, unit_id),
        ).fetchall()
        if stale:
            placeholders = ",".join("?" * len(stale))
            conn.execute(
                f"DELETE FROM ec3_practice_sessions WHERE id IN ({placeholders})",
                [row["id"] for row in stale],
            )


def get_recent_ec3_question_ids(user_id: int, unit_id: int, sessions: int = 2) -> set[str]:
    """Question IDs from the most recent N practice sessions (avoid repeats)."""
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT question_ids FROM ec3_practice_sessions
               WHERE user_id = ? AND unit_id = ?
               ORDER BY completed_at DESC
               LIMIT ?""",
            (user_id, unit_id, max(sessions, 0)),
        ).fetchall()
    seen: set[str] = set()
    for row in rows:
        try:
            seen.update(json.loads(row["question_ids"]))
        except (json.JSONDecodeError, TypeError):
            continue
    return seen


def save_harshit_practice_session(
    user_id: int,
    prereq_id: int,
    question_ids: list[str],
    question_texts: list[str],
) -> None:
    """Remember recent Harshit PreReq questions so the next session avoids repeats."""
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO harshit_practice_sessions
               (user_id, prereq_id, question_ids, question_texts)
               VALUES (?, ?, ?, ?)""",
            (user_id, prereq_id, json.dumps(question_ids), json.dumps(question_texts)),
        )
        stale = conn.execute(
            """SELECT id FROM harshit_practice_sessions
               WHERE user_id = ? AND prereq_id = ?
               ORDER BY completed_at DESC
               LIMIT -1 OFFSET 24""",
            (user_id, prereq_id),
        ).fetchall()
        if stale:
            placeholders = ",".join("?" * len(stale))
            conn.execute(
                f"DELETE FROM harshit_practice_sessions WHERE id IN ({placeholders})",
                [row["id"] for row in stale],
            )


def get_recent_harshit_practice_exclusions(
    user_id: int,
    prereq_id: int,
    *,
    sessions: int = 8,
) -> tuple[set[str], set[str]]:
    """Question ids and exact question text from recent sessions (avoid repeats)."""
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT question_ids, question_texts FROM harshit_practice_sessions
               WHERE user_id = ? AND prereq_id = ?
               ORDER BY completed_at DESC
               LIMIT ?""",
            (user_id, prereq_id, max(sessions, 0)),
        ).fetchall()
    ids: set[str] = set()
    texts: set[str] = set()
    for row in rows:
        try:
            ids.update(json.loads(row["question_ids"]))
        except (json.JSONDecodeError, TypeError):
            pass
        try:
            texts.update(json.loads(row["question_texts"]))
        except (json.JSONDecodeError, TypeError):
            pass
    return ids, texts


def get_today_scores(user_id: int, activity_type: str = None) -> list:
    """Get all scores for today, optionally filtered by activity type."""
    today = datetime.now().strftime("%Y-%m-%d")
    with get_connection() as conn:
        if activity_type:
            rows = conn.execute(
                """SELECT * FROM activity_scores 
                   WHERE user_id = ? AND log_date = ? AND activity_type = ?
                   ORDER BY completed_at DESC""",
                (user_id, today, activity_type),
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT * FROM activity_scores 
                   WHERE user_id = ? AND log_date = ?
                   ORDER BY completed_at DESC""",
                (user_id, today),
            ).fetchall()
        return [dict(r) for r in rows]


def get_scores_history(user_id: int, activity_type: str = None, days: int = 30) -> list:
    """Get score history for the past N days."""
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    with get_connection() as conn:
        if activity_type:
            rows = conn.execute(
                """SELECT log_date, activity_name, score, max_score,
                          COALESCE(time_spent_seconds, 0) as time_spent_seconds
                   FROM activity_scores 
                   WHERE user_id = ? AND log_date >= ? AND activity_type = ?
                   ORDER BY log_date ASC""",
                (user_id, start_date, activity_type),
            ).fetchall()
        else:
            rows = conn.execute(
                """SELECT log_date, activity_type, activity_name, score, max_score,
                          COALESCE(time_spent_seconds, 0) as time_spent_seconds
                   FROM activity_scores 
                   WHERE user_id = ? AND log_date >= ?
                   ORDER BY log_date ASC""",
                (user_id, start_date),
            ).fetchall()
        return [dict(r) for r in rows]


def get_daily_time_spent(user_id: int, days: int = 30) -> list[dict]:
    """Get total time spent per day across all activities.

    Returns a list of dicts with 'log_date', 'total_seconds', and
    'activity_count'.
    """
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT log_date,
                      SUM(COALESCE(time_spent_seconds, 0)) as total_seconds,
                      COUNT(*) as activity_count
               FROM activity_scores
               WHERE user_id = ? AND log_date >= ?
               GROUP BY log_date
               ORDER BY log_date ASC""",
            (user_id, start_date),
        ).fetchall()
        return [dict(r) for r in rows]


def get_daily_time_spent_calendar(user_id: int, days: int = 30) -> list[dict]:
    """Every calendar day in the last `days` days (including today) with time totals.

    Days with no recorded activity have total_seconds=0 and activity_count=0.
    This fills gaps so charts can show a continuous timeline.
    """
    end = datetime.now().date()
    start = end - timedelta(days=days - 1)
    start_str = start.strftime("%Y-%m-%d")
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT log_date,
                      SUM(COALESCE(time_spent_seconds, 0)) as total_seconds,
                      COUNT(*) as activity_count
               FROM activity_scores
               WHERE user_id = ? AND log_date >= ?
               GROUP BY log_date""",
            (user_id, start_str),
        ).fetchall()
    by_date = {
        r["log_date"]: {
            "total_seconds": r["total_seconds"] or 0,
            "activity_count": r["activity_count"] or 0,
        }
        for r in rows
    }
    out = []
    d = start
    while d <= end:
        ds = d.strftime("%Y-%m-%d")
        rec = by_date.get(ds, {"total_seconds": 0, "activity_count": 0})
        out.append({"log_date": ds, **rec})
        d += timedelta(days=1)
    return out


def get_daily_score_calendar(user_id: int, days: int = 30) -> list[dict]:
    """One row per calendar day with aggregated scores (multiple sessions averaged).

    Days with no activity have avg_score=None and activity_count=0.
    """
    end = datetime.now().date()
    start = end - timedelta(days=days - 1)
    start_str = start.strftime("%Y-%m-%d")
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT log_date,
                      AVG(score) as avg_score,
                      MAX(score) as best_score,
                      COUNT(*) as activity_count
               FROM activity_scores
               WHERE user_id = ? AND log_date >= ?
               GROUP BY log_date""",
            (user_id, start_str),
        ).fetchall()
    by_date = {r["log_date"]: dict(r) for r in rows}
    out = []
    d = start
    while d <= end:
        ds = d.strftime("%Y-%m-%d")
        if ds in by_date:
            r = by_date[ds]
            out.append(
                {
                    "log_date": ds,
                    "avg_score": round(r["avg_score"], 1) if r["avg_score"] is not None else None,
                    "best_score": int(r["best_score"]) if r["best_score"] is not None else None,
                    "activity_count": int(r["activity_count"] or 0),
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


def get_total_time_spent(user_id: int) -> int:
    """Get the all-time total seconds spent across all activities."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT SUM(COALESCE(time_spent_seconds, 0)) as total FROM activity_scores WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        return row["total"] if row and row["total"] else 0


def get_today_time_spent(user_id: int) -> int:
    """Get total seconds spent on activities today."""
    today = datetime.now().strftime("%Y-%m-%d")
    with get_connection() as conn:
        row = conn.execute(
            "SELECT SUM(COALESCE(time_spent_seconds, 0)) as total FROM activity_scores "
            "WHERE user_id = ? AND log_date = ?",
            (user_id, today),
        ).fetchone()
        return row["total"] if row and row["total"] else 0


def compute_user_daily_summary(user_id: int, log_date: str | None = None) -> dict:
    """Activities count, average score %, and time spent for one user on one day."""
    log_date = log_date or datetime.now().strftime("%Y-%m-%d")
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT score, COALESCE(time_spent_seconds, 0) AS time_spent_seconds
               FROM activity_scores WHERE user_id = ? AND log_date = ?""",
            (user_id, log_date),
        ).fetchall()
    activities_count = len(rows)
    if activities_count:
        avg_score_pct = round(sum(r["score"] for r in rows) / activities_count)
        time_spent_seconds = sum(int(r["time_spent_seconds"] or 0) for r in rows)
    else:
        avg_score_pct = 0
        time_spent_seconds = 0
    return {
        "activities_count": activities_count,
        "avg_score_pct": avg_score_pct,
        "time_spent_seconds": time_spent_seconds,
    }


def import_daily_summary(
    user_id: int,
    log_date: str,
    *,
    activities_count: int,
    avg_score_pct: int,
    time_spent_seconds: int,
    updated_at: str = "",
) -> None:
    """Upsert a daily summary row imported from Google Sheets."""
    when = updated_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO daily_summaries
               (user_id, log_date, activities_count, avg_score_pct, time_spent_seconds, updated_at)
               VALUES (?, ?, ?, ?, ?, ?)
               ON CONFLICT(user_id, log_date) DO UPDATE SET
                 activities_count = excluded.activities_count,
                 avg_score_pct = excluded.avg_score_pct,
                 time_spent_seconds = excluded.time_spent_seconds,
                 updated_at = excluded.updated_at""",
            (
                user_id,
                log_date,
                int(activities_count),
                int(avg_score_pct),
                int(time_spent_seconds),
                when,
            ),
        )


def get_user_daily_stats(user_id: int, log_date: str | None = None) -> dict:
    """Dashboard stats for one day — live activity_scores, else sheet cache."""
    log_date = log_date or datetime.now().strftime("%Y-%m-%d")
    computed = compute_user_daily_summary(user_id, log_date)
    if computed["activities_count"] > 0:
        return computed

    with get_connection() as conn:
        row = conn.execute(
            """SELECT activities_count, avg_score_pct, time_spent_seconds
               FROM daily_summaries WHERE user_id = ? AND log_date = ?""",
            (user_id, log_date),
        ).fetchone()
    if row:
        return {
            "activities_count": int(row["activities_count"]),
            "avg_score_pct": int(row["avg_score_pct"]),
            "time_spent_seconds": int(row["time_spent_seconds"]),
        }
    return computed


def save_reading_progress(
    user_id: int,
    story_id: str,
    story_title: str,
    questions_total: int,
    questions_correct: int,
    time_spent_seconds: int,
):
    """Save reading comprehension progress."""
    today = datetime.now().strftime("%Y-%m-%d")
    completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        import sharepoint_sync as sps

        sync_id = sps.new_sync_id(f"reading-{user_id}")
    except Exception:
        sync_id = f"reading-{user_id}-{datetime.now().timestamp()}"

    with get_connection() as conn:
        conn.execute(
            """INSERT INTO reading_progress 
               (user_id, story_id, story_title, questions_total, questions_correct, 
                time_spent_seconds, log_date, sync_id, completed_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                user_id,
                story_id,
                story_title,
                questions_total,
                questions_correct,
                time_spent_seconds,
                today,
                sync_id,
                completed_at,
            ),
        )

    user = get_user_by_id(user_id)
    if user:
        _sharepoint_push(
            "persist_reading_progress",
            sync_id=sync_id,
            user_name=user["name"],
            user_id=user_id,
            story_id=story_id,
            story_title=story_title,
            questions_total=questions_total,
            questions_correct=questions_correct,
            time_spent_seconds=time_spent_seconds,
            log_date=today,
            completed_at=completed_at,
        )


def get_reading_history(user_id: int, days: int = 30) -> list:
    """Get reading history for the past N days."""
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT * FROM reading_progress 
               WHERE user_id = ? AND log_date >= ?
               ORDER BY completed_at DESC""",
            (user_id, start_date),
        ).fetchall()
        return [dict(r) for r in rows]


# ── GK daily questions helpers ──

def get_daily_questions(user_id: int, date: str) -> str | None:
    """Return the most recent cached questions JSON for a user on a given date."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT questions_json FROM gk_daily_questions WHERE user_id = ? AND quiz_date = ? "
            "ORDER BY created_at DESC LIMIT 1",
            (user_id, date),
        ).fetchone()
        return row["questions_json"] if row else None


def save_daily_questions(user_id: int, date: str, questions_json: str):
    """Save generated questions JSON for a user+date (allows multiple per day)."""
    with get_connection() as conn:
        conn.execute(
            "INSERT OR REPLACE INTO gk_daily_questions (user_id, quiz_date, questions_json) VALUES (?, ?, ?)",
            (user_id, date, questions_json),
        )


def get_recent_gk_questions(user_id: int, limit: int = 100) -> list[str]:
    """Return question texts from the user's recent GK quizzes.

    Pulls up to `limit` unique question strings from the last 14 days so the
    generator can avoid repeating them.
    """
    import json as _json
    cutoff = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT questions_json FROM gk_daily_questions "
            "WHERE user_id = ? AND quiz_date >= ? ORDER BY created_at DESC",
            (user_id, cutoff),
        ).fetchall()
    seen: list[str] = []
    for row in rows:
        try:
            questions = _json.loads(row["questions_json"])
            for q in questions:
                text = q.get("question", "")
                if text and text not in seen:
                    seen.append(text)
                    if len(seen) >= limit:
                        return seen
        except (ValueError, TypeError):
            continue
    return seen


def get_arjun_vocab_index(user_id: int) -> int:
    """Next word position (0-based) in the ordered Arjun vocabulary list."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT next_word_index FROM arjun_vocab_progress WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        return int(row["next_word_index"]) if row else 0


def set_arjun_vocab_index(user_id: int, index: int) -> None:
    """Persist vocabulary quiz progress (wraps at list length by caller)."""
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO arjun_vocab_progress (user_id, next_word_index)
               VALUES (?, ?)
               ON CONFLICT(user_id) DO UPDATE SET next_word_index = excluded.next_word_index""",
            (user_id, index),
        )


def get_linear_eq_week_config() -> dict:
    """Active weekly strategy/level plan for linear equation practice."""
    with get_connection() as conn:
        row = conn.execute(
            "SELECT week_label, config_json FROM linear_eq_week_config WHERE id = 1"
        ).fetchone()
    if not row:
        return {
            "week_label": "",
            "strategies": [],
            "mental_math": [],
            "mental_math_count": 5,
            "use_llm": False,
        }
    try:
        data = json.loads(row["config_json"] or "{}")
    except json.JSONDecodeError:
        data = {}
    if not isinstance(data, dict):
        data = {}
    strategies = data.get("strategies")
    if not isinstance(strategies, list):
        strategies = []
    mental_math = data.get("mental_math")
    if not isinstance(mental_math, list):
        mental_math = []
    raw_mm_count = data.get("mental_math_count", 5)
    try:
        mental_math_count = max(0, min(15, int(raw_mm_count)))
    except (TypeError, ValueError):
        mental_math_count = 5
    return {
        "week_label": row["week_label"] or data.get("week_label", ""),
        "strategies": strategies,
        "mental_math": mental_math,
        "mental_math_count": mental_math_count,
        "use_llm": bool(data.get("use_llm", False)),
    }


def save_linear_eq_week_config(
    week_label: str,
    strategies: list[dict],
    *,
    mental_math: list[dict] | None = None,
    mental_math_count: int = 5,
    use_llm: bool = False,
) -> None:
    """Save weekly strategy/level selections (single active plan, id=1)."""
    payload = {
        "week_label": week_label,
        "strategies": strategies,
        "mental_math": mental_math or [],
        "mental_math_count": max(0, min(15, int(mental_math_count))),
        "use_llm": use_llm,
    }
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO linear_eq_week_config (id, week_label, config_json, updated_at)
               VALUES (1, ?, ?, CURRENT_TIMESTAMP)
               ON CONFLICT(id) DO UPDATE SET
                 week_label = excluded.week_label,
                 config_json = excluded.config_json,
                 updated_at = CURRENT_TIMESTAMP""",
            (week_label, json.dumps(payload)),
        )
    _google_sheets_push_week_plan(
        week_label,
        strategies,
        mental_math=mental_math or [],
        mental_math_count=mental_math_count,
        use_llm=use_llm,
    )


def import_linear_eq_week_config(
    week_label: str,
    strategies: list[dict],
    *,
    mental_math: list[dict] | None = None,
    mental_math_count: int = 5,
    use_llm: bool = False,
) -> None:
    """Import weekly plan from cloud sync without re-pushing to Google Sheets."""
    payload = {
        "week_label": week_label,
        "strategies": strategies,
        "mental_math": mental_math or [],
        "mental_math_count": max(0, min(15, int(mental_math_count))),
        "use_llm": use_llm,
    }
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO linear_eq_week_config (id, week_label, config_json, updated_at)
               VALUES (1, ?, ?, CURRENT_TIMESTAMP)
               ON CONFLICT(id) DO UPDATE SET
                 week_label = excluded.week_label,
                 config_json = excluded.config_json,
                 updated_at = CURRENT_TIMESTAMP""",
            (week_label, json.dumps(payload)),
        )


def _google_sheets_push_week_plan(
    week_label: str,
    strategies: list[dict],
    *,
    mental_math: list[dict] | None = None,
    mental_math_count: int = 5,
    use_llm: bool = False,
) -> None:
    """Best-effort Google Sheets sync for weekly linear-equations plan."""
    try:
        import google_sheets_sync as gss

        if gss.cloud_sync_enabled():
            gss.persist_week_plan(
                week_label,
                strategies,
                mental_math=mental_math or [],
                mental_math_count=mental_math_count,
                use_llm=use_llm,
            )
    except Exception:
        pass


def get_cvc_review_words(user_id: int, level_id: str) -> list[dict]:
    """Words Krish missed — kept until read correctly in a later batch."""
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT word, phonics_tip, wrong_count, last_wrong_at
               FROM cvc_review_words
               WHERE user_id = ? AND level_id = ?
               ORDER BY last_wrong_at DESC""",
            (user_id, level_id),
        ).fetchall()
    return [dict(r) for r in rows]


def get_cvc_review_count(user_id: int, level_id: str) -> int:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT COUNT(*) AS n FROM cvc_review_words WHERE user_id = ? AND level_id = ?",
            (user_id, level_id),
        ).fetchone()
    return row["n"] if row else 0


def mark_cvc_word_wrong(user_id: int, level_id: str, word: str, phonics_tip: str = "") -> None:
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO cvc_review_words (user_id, level_id, word, phonics_tip, wrong_count, last_wrong_at)
               VALUES (?, ?, ?, ?, 1, CURRENT_TIMESTAMP)
               ON CONFLICT(user_id, level_id, word) DO UPDATE SET
                 phonics_tip = CASE WHEN excluded.phonics_tip != '' THEN excluded.phonics_tip ELSE phonics_tip END,
                 wrong_count = wrong_count + 1,
                 last_wrong_at = CURRENT_TIMESTAMP""",
            (user_id, level_id, word, phonics_tip),
        )


def mark_cvc_word_mastered(user_id: int, level_id: str, word: str) -> None:
    with get_connection() as conn:
        conn.execute(
            "DELETE FROM cvc_review_words WHERE user_id = ? AND level_id = ? AND word = ?",
            (user_id, level_id, word),
        )


def import_daily_login(user_id: int, log_date: str) -> bool:
    """Import one login row from SharePoint. Returns True if inserted."""
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT OR IGNORE INTO daily_logs (user_id, log_date) VALUES (?, ?)",
            (user_id, log_date),
        )
        return cur.rowcount > 0


def _sync_id_exists(table: str, sync_id: str) -> bool:
    with get_connection() as conn:
        row = conn.execute(
            f"SELECT 1 FROM {table} WHERE sync_id = ? LIMIT 1",
            (sync_id,),
        ).fetchone()
    return row is not None


def import_activity_score_row(
    *,
    sync_id: str,
    user_id: int,
    activity_type: str,
    activity_name: str,
    score: int,
    max_score: int,
    log_date: str,
    details: str,
    time_spent_seconds: int,
    completed_at: str,
) -> bool:
    """Import one activity score from SharePoint. Returns True if inserted."""
    if _sync_id_exists("activity_scores", sync_id):
        return False
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO activity_scores
               (user_id, activity_type, activity_name, score, max_score, log_date, details,
                time_spent_seconds, sync_id, completed_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                user_id,
                activity_type,
                activity_name,
                score,
                max_score,
                log_date,
                details,
                time_spent_seconds,
                sync_id,
                completed_at,
            ),
        )
    return True


def import_reading_progress_row(
    *,
    sync_id: str,
    user_id: int,
    story_id: str,
    story_title: str,
    questions_total: int,
    questions_correct: int,
    time_spent_seconds: int,
    log_date: str,
    completed_at: str,
) -> bool:
    """Import one reading progress row from SharePoint. Returns True if inserted."""
    if _sync_id_exists("reading_progress", sync_id):
        return False
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO reading_progress
               (user_id, story_id, story_title, questions_total, questions_correct,
                time_spent_seconds, log_date, sync_id, completed_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                user_id,
                story_id,
                story_title,
                questions_total,
                questions_correct,
                time_spent_seconds,
                log_date,
                sync_id,
                completed_at,
            ),
        )
    return True


def ec3_practice_result_exists(session_id: str) -> bool:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM ec3_practice_results WHERE session_id = ? LIMIT 1",
            (session_id,),
        ).fetchone()
    return row is not None


def save_ec3_practice_result(
    user_id: int,
    *,
    session_id: str,
    session_kind: str,
    unit_id: int | None,
    unit_label: str,
    report: dict,
    failed_questions: list[dict],
    time_spent_seconds: int = 0,
    completed_at: str | None = None,
    log_date: str | None = None,
) -> None:
    """Persist one completed Edgenuity practice session (idempotent on session_id)."""
    if ec3_practice_result_exists(session_id):
        return
    when = completed_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    day = log_date or datetime.now().strftime("%Y-%m-%d")
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO ec3_practice_results
               (session_id, user_id, session_kind, unit_id, unit_label,
                score_pct, correct_count, total_count, time_spent_seconds,
                report_json, failed_json, completed_at, log_date)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                session_id,
                user_id,
                session_kind,
                unit_id,
                unit_label,
                int(report.get("score_pct", 0)),
                int(report.get("correct_count", 0)),
                int(report.get("total", 0)),
                time_spent_seconds,
                json.dumps(report),
                json.dumps(failed_questions),
                when,
                day,
            ),
        )


def import_ec3_practice_result_row(
    *,
    session_id: str,
    user_id: int,
    session_kind: str,
    unit_id: int | None,
    unit_label: str,
    score_pct: int,
    correct_count: int,
    total_count: int,
    time_spent_seconds: int,
    report_json: str,
    failed_json: str,
    completed_at: str,
    log_date: str,
) -> bool:
    """Import one row from Google Sheets. Returns True if inserted."""
    if ec3_practice_result_exists(session_id):
        return False
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO ec3_practice_results
               (session_id, user_id, session_kind, unit_id, unit_label,
                score_pct, correct_count, total_count, time_spent_seconds,
                report_json, failed_json, completed_at, log_date)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                session_id,
                user_id,
                session_kind,
                unit_id,
                unit_label,
                score_pct,
                correct_count,
                total_count,
                time_spent_seconds,
                report_json,
                failed_json,
                completed_at,
                log_date,
            ),
        )
    return True


def get_ec3_practice_results(user_id: int, days: int = 90) -> list[dict]:
    """Recent Edgenuity practice sessions for analytics."""
    since = (datetime.now() - timedelta(days=max(days, 1))).strftime("%Y-%m-%d")
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT session_id, session_kind, unit_id, unit_label,
                      score_pct, correct_count, total_count, time_spent_seconds,
                      report_json, failed_json, completed_at, log_date
               FROM ec3_practice_results
               WHERE user_id = ? AND log_date >= ?
               ORDER BY completed_at DESC""",
            (user_id, since),
        ).fetchall()
    out = []
    for row in rows:
        item = dict(row)
        try:
            item["report"] = json.loads(item.pop("report_json") or "{}")
        except json.JSONDecodeError:
            item["report"] = {}
        try:
            item["failed"] = json.loads(item.pop("failed_json") or "[]")
        except json.JSONDecodeError:
            item["failed"] = []
        out.append(item)
    return out


# ── Harshit Math intervention progress ──


def get_harshit_problem_progress(
    user_id: int,
    day_id: int,
    problem_id: str,
    phase_id: str = "phase1",
) -> dict | None:
    with get_connection() as conn:
        row = conn.execute(
            """SELECT current_node, step_index, visual_complete, state_json, completed_at
               FROM harshit_math_progress
               WHERE user_id = ? AND phase_id = ? AND day_id = ? AND problem_id = ?""",
            (user_id, phase_id, day_id, problem_id),
        ).fetchone()
    if not row:
        return None
    out = dict(row)
    try:
        out["state"] = json.loads(out.pop("state_json") or "{}")
    except json.JSONDecodeError:
        out["state"] = {}
    return out


def save_harshit_problem_progress(
    user_id: int,
    day_id: int,
    problem_id: str,
    *,
    current_node: str,
    step_index: int,
    visual_complete: bool,
    state: dict | None = None,
    completed: bool = False,
    phase_id: str = "phase1",
) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    completed_at = now if completed else None
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO harshit_math_progress
               (user_id, phase_id, day_id, problem_id, current_node, step_index,
                visual_complete, state_json, completed_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(user_id, phase_id, day_id, problem_id) DO UPDATE SET
                 current_node = excluded.current_node,
                 step_index = excluded.step_index,
                 visual_complete = excluded.visual_complete,
                 state_json = excluded.state_json,
                 completed_at = COALESCE(excluded.completed_at, harshit_math_progress.completed_at),
                 updated_at = excluded.updated_at""",
            (
                user_id,
                phase_id,
                day_id,
                problem_id,
                current_node,
                step_index,
                1 if visual_complete else 0,
                json.dumps(state or {}),
                completed_at,
                now,
            ),
        )


def update_harshit_day_status(
    user_id: int,
    day_id: int,
    *,
    status: str,
    problems_completed: int,
    problems_total: int,
    phase_id: str = "phase1",
) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO harshit_math_day_status
               (user_id, phase_id, day_id, status, problems_completed, problems_total, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(user_id, phase_id, day_id) DO UPDATE SET
                 status = excluded.status,
                 problems_completed = excluded.problems_completed,
                 problems_total = excluded.problems_total,
                 updated_at = excluded.updated_at""",
            (user_id, phase_id, day_id, status, problems_completed, problems_total, now),
        )


def get_harshit_day_status(user_id: int, phase_id: str = "phase1") -> dict[int, dict]:
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT day_id, status, problems_completed, problems_total
               FROM harshit_math_day_status
               WHERE user_id = ? AND phase_id = ?""",
            (user_id, phase_id),
        ).fetchall()
    return {int(r["day_id"]): dict(r) for r in rows}


def get_harshit_prereq_chapter_status(user_id: int, prereq_id: int) -> dict[int, dict]:
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT chapter_num, status, notes, updated_at
               FROM harshit_prereq_chapter_status
               WHERE user_id = ? AND prereq_id = ?""",
            (user_id, prereq_id),
        ).fetchall()
    return {int(r["chapter_num"]): dict(r) for r in rows}


def save_harshit_prereq_chapter_status(
    user_id: int,
    prereq_id: int,
    chapter_num: int,
    *,
    status: str,
    notes: str = "",
) -> None:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO harshit_prereq_chapter_status
               (user_id, prereq_id, chapter_num, status, notes, updated_at)
               VALUES (?, ?, ?, ?, ?, ?)
               ON CONFLICT(user_id, prereq_id, chapter_num) DO UPDATE SET
                 status = excluded.status,
                 notes = excluded.notes,
                 updated_at = excluded.updated_at""",
            (user_id, prereq_id, chapter_num, status, notes, now),
        )


def get_harshit_prereq_summary(user_id: int) -> dict[int, dict]:
    """Per-bucket counts of chapter completion."""
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT prereq_id, chapter_num, status
               FROM harshit_prereq_chapter_status
               WHERE user_id = ?""",
            (user_id,),
        ).fetchall()
    out: dict[int, dict] = {}
    for r in rows:
        pid = int(r["prereq_id"])
        bucket = out.setdefault(pid, {"complete": 0, "in_progress": 0, "total_marked": 0})
        bucket["total_marked"] += 1
        if r["status"] == "complete":
            bucket["complete"] += 1
        elif r["status"] == "in_progress":
            bucket["in_progress"] += 1
    return out


def get_harshit_prereq_week_config(prereq_id: int) -> dict:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT week_label, config_json FROM harshit_prereq_week_config WHERE prereq_id = ?",
            (prereq_id,),
        ).fetchone()
    if not row:
        return {"week_label": "", "topics": [], "warmup_count": 0, "use_llm": False, "use_chapter_llm": True, "grok_fresh_only": False}
    try:
        data = json.loads(row["config_json"] or "{}")
    except json.JSONDecodeError:
        data = {}
    if not isinstance(data, dict):
        data = {}
    topics = data.get("topics")
    if not isinstance(topics, list):
        topics = []
    try:
        warmup_count = max(0, min(5, int(data.get("warmup_count", 2))))
    except (TypeError, ValueError):
        warmup_count = 2
    return {
        "week_label": row["week_label"] or data.get("week_label", ""),
        "topics": topics,
        "warmup_count": warmup_count,
        "use_llm": bool(data.get("use_llm", False)),
        "use_chapter_llm": bool(data.get("use_chapter_llm", True)),
        "grok_fresh_only": bool(data.get("grok_fresh_only", False)),
        "prereq_id": prereq_id,
    }


def save_harshit_prereq_week_config(
    prereq_id: int,
    week_label: str,
    topics: list[dict],
    *,
    warmup_count: int = 2,
    use_llm: bool = False,
    use_chapter_llm: bool = True,
    grok_fresh_only: bool = False,
) -> None:
    payload = {
        "week_label": week_label,
        "topics": topics,
        "warmup_count": max(0, min(5, int(warmup_count))),
        "use_llm": use_llm,
        "use_chapter_llm": use_chapter_llm,
        "grok_fresh_only": grok_fresh_only,
        "prereq_id": prereq_id,
    }
    with get_connection() as conn:
        conn.execute(
            """INSERT INTO harshit_prereq_week_config (prereq_id, week_label, config_json, updated_at)
               VALUES (?, ?, ?, CURRENT_TIMESTAMP)
               ON CONFLICT(prereq_id) DO UPDATE SET
                 week_label = excluded.week_label,
                 config_json = excluded.config_json,
                 updated_at = CURRENT_TIMESTAMP""",
            (prereq_id, week_label, json.dumps(payload)),
        )
    try:
        import google_sheets_sync as gss

        if gss.cloud_sync_enabled():
            gss.save_harshit_prereq_week_plan(prereq_id, week_label, payload)
    except Exception:
        pass

