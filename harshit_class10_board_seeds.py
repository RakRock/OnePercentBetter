"""Load board-exam question seeds derived from previous-year CBSE papers."""

from __future__ import annotations

import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SEEDS_DIR = ROOT / "HarshitMath" / "class10" / "board_paper_seeds"

_CACHE: dict[int, dict] = {}


def _seed_path(unit_id: int) -> Path:
    return SEEDS_DIR / f"unit_{unit_id:02d}.json"


def load_unit_seeds(unit_id: int) -> dict:
    if unit_id in _CACHE:
        return _CACHE[unit_id]
    path = _seed_path(unit_id)
    if not path.is_file():
        return {"meta": {"unit_id": unit_id}, "mcq": [], "assertion_reason": [], "vsa": [], "sa": [], "la": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    for key in ("mcq", "assertion_reason", "vsa", "sa", "la"):
        data.setdefault(key, [])
    _CACHE[unit_id] = data
    return data


def seeds_available(unit_id: int) -> bool:
    data = load_unit_seeds(unit_id)
    return any(len(data.get(k, [])) > 0 for k in ("mcq", "assertion_reason", "vsa", "sa", "la"))


def seed_sources(unit_id: int) -> list[str]:
    return list(load_unit_seeds(unit_id).get("meta", {}).get("sources", []))


def pick_seed(unit_id: int, bucket: str, *, exclude_ids: set[str] | None = None) -> dict | None:
    exclude_ids = exclude_ids or set()
    pool = [q for q in load_unit_seeds(unit_id).get(bucket, []) if q.get("id") not in exclude_ids]
    if not pool:
        return None
    return random.choice(pool)


def pick_mcq_seed(unit_id: int, *, exclude_ids: set[str]) -> dict | None:
    return pick_seed(unit_id, "mcq", exclude_ids=exclude_ids)


def pick_ar_seed(unit_id: int, *, exclude_ids: set[str]) -> dict | None:
    return pick_seed(unit_id, "assertion_reason", exclude_ids=exclude_ids)


def pick_written_seed(unit_id: int, bucket: str, *, exclude_ids: set[str]) -> dict | None:
    return pick_seed(unit_id, bucket, exclude_ids=exclude_ids)
