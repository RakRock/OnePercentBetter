"""Practice setup defaults and persistence for Arjun Spanish."""

from __future__ import annotations

import database as db
from arjun_spanish import content as es


def default_config() -> dict:
    return {
        "week_label": "",
        "topics": es.school_topic_ids(),
        "use_llm": True,
        "grok_fresh_only": False,
        "question_count": es.DEFAULT_SESSION_COUNT,
    }


def ensure_config() -> dict:
    saved = db.get_arjun_spanish_config()
    base = default_config()
    if not saved:
        return base
    topics = [t for t in saved.get("topics", []) if t in {x["id"] for x in es.TOPICS}]
    if not topics:
        topics = base["topics"]
    return {
        "week_label": str(saved.get("week_label", "")),
        "topics": topics,
        "use_llm": bool(saved.get("use_llm", True)),
        "grok_fresh_only": bool(saved.get("grok_fresh_only", False)),
        "question_count": int(saved.get("question_count", es.DEFAULT_SESSION_COUNT)),
    }


def save_config(config: dict) -> None:
    db.save_arjun_spanish_config(
        str(config.get("week_label", "")),
        list(config.get("topics", [])),
        use_llm=bool(config.get("use_llm", True)),
        grok_fresh_only=bool(config.get("grok_fresh_only", False)),
        question_count=int(config.get("question_count", es.DEFAULT_SESSION_COUNT)),
    )
