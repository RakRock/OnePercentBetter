"""Harshit Physics/Chemistry DB helpers for older or stale ``database`` modules.

Streamlit Cloud can keep a cached ``database`` import across redeploys. If the
UI expects ``get_harshit_physics_viewed_concepts`` but the loaded module predates
that helper, patch the missing API here (same idea as calendar fallbacks in app.py).
"""

from __future__ import annotations

import json
import types

_PHYSICS_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS harshit_physics_concept_status (
    user_id INTEGER NOT NULL,
    unit_id INTEGER NOT NULL,
    concept_id TEXT NOT NULL,
    viewed INTEGER NOT NULL DEFAULT 0,
    marked_review INTEGER NOT NULL DEFAULT 0,
    simpler_requests INTEGER NOT NULL DEFAULT 0,
    example_requests INTEGER NOT NULL DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, unit_id, concept_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS harshit_physics_day_status (
    user_id INTEGER NOT NULL,
    unit_id INTEGER NOT NULL,
    day_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'not_started',
    concepts_viewed INTEGER NOT NULL DEFAULT 0,
    concepts_total INTEGER NOT NULL DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, unit_id, day_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS harshit_physics_mcq_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    unit_id INTEGER NOT NULL,
    day_id INTEGER NOT NULL,
    question_id TEXT NOT NULL,
    selected TEXT,
    correct INTEGER NOT NULL DEFAULT 0,
    misconception TEXT DEFAULT '',
    concept_reviewed TEXT DEFAULT '',
    retry_correct INTEGER,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS harshit_physics_misconceptions (
    user_id INTEGER NOT NULL,
    unit_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    count INTEGER NOT NULL DEFAULT 0,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, unit_id, category),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS harshit_physics_week_config (
    unit_id INTEGER PRIMARY KEY,
    week_label TEXT NOT NULL DEFAULT '',
    config_json TEXT NOT NULL DEFAULT '{}',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

_CHEMISTRY_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS harshit_chemistry_concept_status (
    user_id INTEGER NOT NULL,
    unit_id INTEGER NOT NULL,
    concept_id TEXT NOT NULL,
    viewed INTEGER NOT NULL DEFAULT 0,
    marked_review INTEGER NOT NULL DEFAULT 0,
    simpler_requests INTEGER NOT NULL DEFAULT 0,
    example_requests INTEGER NOT NULL DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, unit_id, concept_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS harshit_chemistry_day_status (
    user_id INTEGER NOT NULL,
    unit_id INTEGER NOT NULL,
    day_id INTEGER NOT NULL,
    status TEXT NOT NULL DEFAULT 'not_started',
    concepts_viewed INTEGER NOT NULL DEFAULT 0,
    concepts_total INTEGER NOT NULL DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, unit_id, day_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS harshit_chemistry_mcq_attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    unit_id INTEGER NOT NULL,
    day_id INTEGER NOT NULL,
    question_id TEXT NOT NULL,
    selected TEXT,
    correct INTEGER NOT NULL DEFAULT 0,
    misconception TEXT DEFAULT '',
    concept_reviewed TEXT DEFAULT '',
    retry_correct INTEGER,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS harshit_chemistry_misconceptions (
    user_id INTEGER NOT NULL,
    unit_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    count INTEGER NOT NULL DEFAULT 0,
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, unit_id, category),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
CREATE TABLE IF NOT EXISTS harshit_chemistry_week_config (
    unit_id INTEGER PRIMARY KEY,
    week_label TEXT NOT NULL DEFAULT '',
    config_json TEXT NOT NULL DEFAULT '{}',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


def _ensure_tables(db_module: types.ModuleType, sql: str) -> None:
    with db_module.get_connection() as conn:
        conn.executescript(sql)


def _default_week_config(unit_id: int, *, use_chapter_llm: bool) -> dict:
    return {
        "week_label": "",
        "topics": [],
        "practice_difficulty": 3,
        "use_chapter_llm": use_chapter_llm,
        "grok_fresh_only": False,
        "unit_id": unit_id,
    }


def _parse_week_config(row, unit_id: int, *, use_chapter_llm: bool) -> dict:
    if not row:
        return _default_week_config(unit_id, use_chapter_llm=use_chapter_llm)
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
        practice_difficulty = max(1, min(5, int(data.get("practice_difficulty", 3))))
    except (TypeError, ValueError):
        practice_difficulty = 3
    return {
        "week_label": row["week_label"] or data.get("week_label", ""),
        "topics": topics,
        "practice_difficulty": practice_difficulty,
        "use_chapter_llm": bool(data.get("use_chapter_llm", use_chapter_llm)),
        "grok_fresh_only": bool(data.get("grok_fresh_only", False)),
        "unit_id": unit_id,
    }


def _patch_subject(
    db_module: types.ModuleType,
    *,
    prefix: str,
    tables_sql: str,
    use_chapter_llm_default: bool,
) -> None:
    concept_table = f"harshit_{prefix}_concept_status"
    day_table = f"harshit_{prefix}_day_status"
    mcq_table = f"harshit_{prefix}_mcq_attempts"
    misc_table = f"harshit_{prefix}_misconceptions"
    week_table = f"harshit_{prefix}_week_config"

    get_viewed_name = f"get_harshit_{prefix}_viewed_concepts"
    if not hasattr(db_module, get_viewed_name):
        _ensure_tables(db_module, tables_sql)

        def get_viewed_concepts(user_id: int, *, unit_id: int) -> list[str]:
            with db_module.get_connection() as conn:
                rows = conn.execute(
                    f"""SELECT concept_id FROM {concept_table}
                        WHERE user_id = ? AND unit_id = ? AND viewed = 1""",
                    (user_id, unit_id),
                ).fetchall()
            return [r["concept_id"] for r in rows]

        setattr(db_module, get_viewed_name, get_viewed_concepts)

    get_review_name = f"get_harshit_{prefix}_review_concepts"
    if not hasattr(db_module, get_review_name):

        def get_review_concepts(user_id: int, *, unit_id: int) -> list[str]:
            with db_module.get_connection() as conn:
                rows = conn.execute(
                    f"""SELECT concept_id FROM {concept_table}
                        WHERE user_id = ? AND unit_id = ? AND marked_review = 1""",
                    (user_id, unit_id),
                ).fetchall()
            return [r["concept_id"] for r in rows]

        setattr(db_module, get_review_name, get_review_concepts)

    save_concept_name = f"save_harshit_{prefix}_concept_status"
    if not hasattr(db_module, save_concept_name):

        def save_concept_status(
            user_id: int,
            *,
            unit_id: int,
            concept_id: str,
            viewed: bool = False,
            marked_review: bool = False,
            simpler_request: bool = False,
            example_request: bool = False,
        ) -> None:
            with db_module.get_connection() as conn:
                row = conn.execute(
                    f"""SELECT simpler_requests, example_requests, viewed, marked_review
                        FROM {concept_table}
                        WHERE user_id = ? AND unit_id = ? AND concept_id = ?""",
                    (user_id, unit_id, concept_id),
                ).fetchone()
                simpler = int(row["simpler_requests"]) if row else 0
                examples = int(row["example_requests"]) if row else 0
                if simpler_request:
                    simpler += 1
                if example_request:
                    examples += 1
                viewed_val = 1 if viewed or (row and row["viewed"]) else 0
                review_val = 1 if marked_review else (int(row["marked_review"]) if row else 0)
                conn.execute(
                    f"""INSERT INTO {concept_table}
                        (user_id, unit_id, concept_id, viewed, marked_review, simpler_requests,
                         example_requests, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                        ON CONFLICT(user_id, unit_id, concept_id) DO UPDATE SET
                          viewed = MAX({concept_table}.viewed, excluded.viewed),
                          marked_review = excluded.marked_review,
                          simpler_requests = excluded.simpler_requests,
                          example_requests = excluded.example_requests,
                          updated_at = CURRENT_TIMESTAMP""",
                    (user_id, unit_id, concept_id, viewed_val, review_val, simpler, examples),
                )

        setattr(db_module, save_concept_name, save_concept_status)

    update_day_name = f"update_harshit_{prefix}_day_status"
    if not hasattr(db_module, update_day_name):

        def update_day_status(
            user_id: int,
            *,
            unit_id: int,
            day_id: int,
            status: str,
            concepts_viewed: int,
            concepts_total: int,
        ) -> None:
            with db_module.get_connection() as conn:
                conn.execute(
                    f"""INSERT INTO {day_table}
                        (user_id, unit_id, day_id, status, concepts_viewed, concepts_total, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
                        ON CONFLICT(user_id, unit_id, day_id) DO UPDATE SET
                          status = excluded.status,
                          concepts_viewed = excluded.concepts_viewed,
                          concepts_total = excluded.concepts_total,
                          updated_at = CURRENT_TIMESTAMP""",
                    (user_id, unit_id, day_id, status, concepts_viewed, concepts_total),
                )

        setattr(db_module, update_day_name, update_day_status)

    get_week_name = f"get_harshit_{prefix}_week_config"
    if not hasattr(db_module, get_week_name):

        def get_week_config(unit_id: int) -> dict:
            with db_module.get_connection() as conn:
                row = conn.execute(
                    f"SELECT week_label, config_json FROM {week_table} WHERE unit_id = ?",
                    (unit_id,),
                ).fetchone()
            return _parse_week_config(row, unit_id, use_chapter_llm=use_chapter_llm_default)

        setattr(db_module, get_week_name, get_week_config)

    save_week_name = f"save_harshit_{prefix}_week_config"
    if not hasattr(db_module, save_week_name):

        def save_week_config(
            unit_id: int,
            week_label: str,
            topics: list[dict],
            *,
            practice_difficulty: int = 3,
            use_chapter_llm: bool = use_chapter_llm_default,
            grok_fresh_only: bool = False,
        ) -> None:
            payload = {
                "week_label": week_label,
                "topics": topics,
                "practice_difficulty": max(1, min(5, int(practice_difficulty))),
                "use_chapter_llm": use_chapter_llm,
                "grok_fresh_only": grok_fresh_only,
                "unit_id": unit_id,
            }
            with db_module.get_connection() as conn:
                conn.execute(
                    f"""INSERT INTO {week_table} (unit_id, week_label, config_json, updated_at)
                        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                        ON CONFLICT(unit_id) DO UPDATE SET
                          week_label = excluded.week_label,
                          config_json = excluded.config_json,
                          updated_at = CURRENT_TIMESTAMP""",
                    (unit_id, week_label, json.dumps(payload)),
                )

        setattr(db_module, save_week_name, save_week_config)

    save_mcq_name = f"save_harshit_{prefix}_mcq_attempt"
    if not hasattr(db_module, save_mcq_name):

        def save_mcq_attempt(
            user_id: int,
            *,
            unit_id: int,
            day_id: int,
            question_id: str,
            selected: str,
            correct: bool,
            misconception: str = "",
            concept_reviewed: str = "",
            retry_correct: bool | None = None,
        ) -> None:
            with db_module.get_connection() as conn:
                conn.execute(
                    f"""INSERT INTO {mcq_table}
                        (user_id, unit_id, day_id, question_id, selected, correct,
                         misconception, concept_reviewed, retry_correct)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        user_id,
                        unit_id,
                        day_id,
                        question_id,
                        selected,
                        1 if correct else 0,
                        misconception,
                        concept_reviewed,
                        None if retry_correct is None else (1 if retry_correct else 0),
                    ),
                )
                if misconception and not correct:
                    conn.execute(
                        f"""INSERT INTO {misc_table} (user_id, unit_id, category, count, last_seen)
                            VALUES (?, ?, ?, 1, CURRENT_TIMESTAMP)
                            ON CONFLICT(user_id, unit_id, category) DO UPDATE SET
                              count = count + 1,
                              last_seen = CURRENT_TIMESTAMP""",
                        (user_id, unit_id, misconception),
                    )

        setattr(db_module, save_mcq_name, save_mcq_attempt)


def patch_harshit_db_api(db_module: types.ModuleType) -> None:
    """Attach missing Harshit Physics/Chemistry helpers to ``database``."""
    _patch_subject(
        db_module,
        prefix="physics",
        tables_sql=_PHYSICS_TABLES_SQL,
        use_chapter_llm_default=False,
    )
    _patch_subject(
        db_module,
        prefix="chemistry",
        tables_sql=_CHEMISTRY_TABLES_SQL,
        use_chapter_llm_default=False,
    )


def ensure_harshit_db_api(db_module: types.ModuleType) -> types.ModuleType:
    """Reload stale ``database`` modules, then patch any still-missing Harshit API."""
    if hasattr(db_module, "get_harshit_physics_viewed_concepts"):
        return db_module

    import importlib
    import database

    db_module = importlib.reload(database)
    db_module.init_db()
    if not hasattr(db_module, "get_harshit_physics_viewed_concepts"):
        patch_harshit_db_api(db_module)
    return db_module
