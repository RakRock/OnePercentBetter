#!/usr/bin/env python3
"""Standalone email worker — never import Streamlit."""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: send_practice_email.py <payload.json>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    payload = json.loads(path.read_text(encoding="utf-8"))

    from practice_email.settings import load_settings
    from practice_email.transport import deliver_now

    settings = load_settings()
    deliver_now(
        settings,
        payload["subject"],
        payload["plain"],
        payload["html"],
        recipient=payload.get("recipient") or None,
    )
    path.unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1) from exc
