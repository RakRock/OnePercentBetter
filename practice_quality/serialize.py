"""JSON-safe report payloads for DB / Google Sheets storage."""


def sanitize_report_for_storage(report: dict) -> dict:
    """Strip non-serializable / bulky nested question objects from learning reports."""
    out = dict(report)
    err = out.get("error_analysis")
    if isinstance(err, dict):
        err = dict(err)
        weak = []
        for row in err.get("weak_skills") or []:
            if not isinstance(row, dict):
                continue
            clean = {k: v for k, v in row.items() if k != "items"}
            items = []
            for item in row.get("items") or []:
                if not isinstance(item, dict):
                    continue
                items.append(
                    {
                        "index": item.get("index"),
                        "picked": item.get("picked"),
                        "correct": item.get("correct"),
                        "pattern": item.get("pattern"),
                        "question": str(
                            item.get("question", {}).get("question")
                            if isinstance(item.get("question"), dict)
                            else item.get("question", "")
                        )[:500],
                    }
                )
            clean["items"] = items
            weak.append(clean)
        err["weak_skills"] = weak
        out["error_analysis"] = err
    return out
