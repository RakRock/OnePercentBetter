#!/usr/bin/env python3
"""Run a practice validation audit and optionally email the full report.

Examples:
  python scripts/run_practice_validation.py --list-apps
  python scripts/run_practice_validation.py --app course3 --unit 1 --count 100 --email
  python scripts/run_practice_validation.py --app course3 --unit 1 --base-seed --email
  python scripts/run_practice_validation.py --app harshit_prereq --unit 4 --count 100 --email
  python scripts/run_practice_validation.py --app harshit_class10 --unit 4 --base-seed --email
  python scripts/run_practice_validation.py --app harshit_class10 --unit 1 --count 50 --dry-run
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _parse_args() -> argparse.Namespace:
    from practice_validation import PRACTICE_APPS

    parser = argparse.ArgumentParser(description="Generate practice questions and audit answer keys.")
    parser.add_argument(
        "--list-apps",
        action="store_true",
        help="List available apps and unit ranges, then exit",
    )
    parser.add_argument(
        "--student",
        default=None,
        help="Student name in email (default: app default, e.g. Arjun or Harshit)",
    )
    parser.add_argument(
        "--app",
        default="course3",
        choices=sorted(PRACTICE_APPS.keys()),
        help="Practice app/track",
    )
    parser.add_argument("--unit", type=int, default=1, help="Unit or PreReq number (default: 1)")
    parser.add_argument("--count", type=int, default=100, help="Questions to generate (default: 100)")
    parser.add_argument(
        "--base-seed",
        action="store_true",
        help="Audit full persisted seed bank (Course 3 static+builtin, Harshit JSON banks, etc.)",
    )
    parser.add_argument(
        "--use-llm",
        action="store_true",
        help="Enable Grok generation where configured (requires XAI_API_KEY)",
    )
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducible audits")
    parser.add_argument(
        "--email",
        action="store_true",
        help="Send the full audit report via configured practice email",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Generate and print summary only; do not send email",
    )
    parser.add_argument(
        "--write-report",
        metavar="DIR",
        default=None,
        help="Write audit plain-text and HTML reports to this directory",
    )
    parser.add_argument(
        "--email-to",
        default=None,
        help="Override validation email recipient(s), comma-separated",
    )
    return parser.parse_args()


def _format_validation_audit_email():
    """Load formatter without pulling practice_email.delivery (httpx)."""
    import importlib.util

    fmt_path = ROOT / "practice_email" / "format.py"
    spec = importlib.util.spec_from_file_location("_practice_email_format", fmt_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot load {fmt_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.format_validation_audit_email


def _write_audit_reports(payload: dict, out_dir: Path) -> tuple[Path, Path]:
    format_validation_audit_email = _format_validation_audit_email()

    out_dir.mkdir(parents=True, exist_ok=True)
    spec = payload["app"]
    subject, plain, html = format_validation_audit_email(
        student_name=payload["student_name"],
        program_name=spec.label,
        unit_title=payload["unit_title"],
        unit_subtitle=payload["unit_subtitle"],
        audit_rows=payload["audit_rows"],
        report=payload["report"],
        requested_count=payload["requested_count"],
        generated_count=payload["generated_count"],
    )
    uid = payload["unit_id"]
    txt_path = out_dir / f"unit_{uid:02d}_validation.txt"
    html_path = out_dir / f"unit_{uid:02d}_validation.html"
    txt_path.write_text(plain, encoding="utf-8")
    html_path.write_text(html, encoding="utf-8")
    return txt_path, html_path


def main() -> int:
    args = _parse_args()
    from practice_validation import list_apps, run_base_seed_validation_audit, run_validation_audit

    if args.list_apps:
        print("Available practice validation apps:\n")
        for spec in list_apps():
            print(f"  {spec.key}")
            print(f"    Label:   {spec.label}")
            print(f"    Student: {spec.student_name}")
            print(f"    Range:   {spec.unit_id_label} 1–{spec.unit_count}")
            print()
        return 0

    try:
        if args.base_seed:
            payload = run_base_seed_validation_audit(
                args.app,
                args.unit,
                seed=args.seed,
                student_name=args.student,
            )
        else:
            payload = run_validation_audit(
                args.app,
                args.unit,
                args.count,
                use_llm=args.use_llm,
                seed=args.seed,
                student_name=args.student,
            )
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    spec = payload["app"]
    report = payload["report"]
    generated = payload["generated_count"]
    requested = payload["requested_count"]
    wrong = int(report.get("total", 0)) - int(report.get("correct_count", 0))
    student = payload["student_name"]

    print(f"Student: {student}")
    print(f"App: {spec.label}")
    print(f"{spec.unit_id_label}: {payload['unit_id']} — {payload['unit_title']}")
    mode = "base seed bank" if payload.get("base_seed") else "sampled session"
    print(f"Mode: {mode}")
    print(f"Generated: {generated}/{requested} questions")
    print(f"Simulated random score: {report.get('correct_count')}/{report.get('total')} ({report.get('score_pct')}%)")
    print(f"Simulated misses (explanations included in email): {wrong}")

    structural = payload.get("structural_issues") or []
    if structural:
        print(f"Structural issues found: {len(structural)}")
        for issue in structural[:20]:
            print(f"  - {issue}")
        if len(structural) > 20:
            print(f"  ... and {len(structural) - 20} more")
    else:
        print("Structural validation: all questions passed")

    if generated < requested:
        print(f"Warning: only {generated} unique questions available; requested {requested}.")

    if args.write_report:
        txt_path, html_path = _write_audit_reports(payload, Path(args.write_report))
        print(f"Wrote {txt_path}")
        print(f"Wrote {html_path}")

    if args.dry_run or not args.email:
        if not args.dry_run and not args.email:
            print("Email not sent (pass --email to send).")
        return 0

    from practice_email.delivery import send_validation_audit_email
    from practice_email.settings import delivery_ready, load_settings, parse_email_recipients
    import edgenuity_practice_email as mail

    email_recipients = parse_email_recipients(args.email_to or "")
    settings = load_settings()
    if not settings.enabled:
        print(f"Email not configured: {mail.email_status_message()}", file=sys.stderr)
        return 1
    ready, _, config_err = delivery_ready(settings)
    if not ready:
        print(f"Email not configured: {config_err or mail.email_status_message()}", file=sys.stderr)
        return 1
    if not email_recipients and not settings.recipients:
        print("No recipients: set PRACTICE_REPORT_EMAIL_TO or pass --email-to", file=sys.stderr)
        return 1

    result = send_validation_audit_email(
        student_name=student,
        program_name=spec.label,
        unit_title=payload["unit_title"],
        unit_subtitle=payload["unit_subtitle"],
        audit_rows=payload["audit_rows"],
        report=report,
        requested_count=requested,
        generated_count=generated,
        recipients=email_recipients or None,
    )
    if result.ok:
        print(f"Audit emailed to {result.recipient}")
        if result.error:
            print(f"Note: {result.error}")
        return 0

    print(f"Email failed: {result.error or 'unknown error'}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
