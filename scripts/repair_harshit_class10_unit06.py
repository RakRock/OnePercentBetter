#!/usr/bin/env python3
"""Repair Class 10 Unit 6 (Triangles) math and template defects."""

from __future__ import annotations

import hashlib
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import harshit_class10_topics as h10t
from harshit_class10_topics import _bpt_ratios_equal

UNIT06_DIR = ROOT / "HarshitMath" / "class10" / "question_banks" / "unit_06"

_RATIO_D = re.compile(
    r"sides in ratio (\d+):(\d+).*smaller side is (\d+)\s*cm",
    re.I,
)
_BPT_SEG = re.compile(
    r"AD\s*=\s*(\d+).*DB\s*=\s*(\d+).*AE\s*=\s*(\d+).*EC\s*=\s*(\d+)",
    re.I,
)
_BPT_SEG2 = re.compile(
    r"AD\s*=\s*(\d+).*DB\s*=\s*(\d+).*AE\s*=\s*(\d+)",
    re.I,
)
_PARALLEL = re.compile(
    r"PE\s*=\s*(\d+)\s*cm.*EQ\s*=\s*(\d+)\s*cm.*PF\s*=\s*(\d+)\s*cm.*FR\s*=\s*(\d+)\s*cm",
    re.I,
)
_SHADOW = re.compile(
    r"(\d+(?:\.\d+)?)\s*m tree casts a (\d+(?:\.\d+)?)\s*m shadow.*?pole casts (\d+(?:\.\d+)?)\s*m shadow",
    re.I,
)


def _det_seed(qid: str) -> int:
    return int(hashlib.md5(qid.encode()).hexdigest()[:8], 16)


def _set_answer_for_text(q: dict, correct: str) -> None:
    opts = [str(o) for o in q.get("options", [])]
    for i, opt in enumerate(opts):
        if opt.strip() == correct.strip():
            q["answer"] = i
            return
    for i, opt in enumerate(opts):
        if correct.strip() in opt:
            q["answer"] = i
            return


def _fix_bare_cm_options(q: dict) -> bool:
    if " cm" not in str(q.get("question", "")):
        return False
    changed = False
    opts = []
    for o in q.get("options", []):
        s = str(o).strip()
        if re.fullmatch(r"-?\d+$", s):
            opts.append(f"{s} cm")
            changed = True
        elif s in ("None of these", "Cannot tell"):
            opts.append(s)
        else:
            opts.append(str(o))
    if changed:
        q["options"] = opts
    return changed


def _fix_u6_t1_d(q: dict) -> bool:
    m = _RATIO_D.search(str(q.get("question", "")))
    if not m:
        return False
    a, b, base = int(m.group(1)), int(m.group(2)), int(m.group(3))
    sm, lg = min(a, b), max(a, b)
    if sm == 0:
        return False
    larger = base * lg // sm
    correct = f"{larger} cm"
    wrong = [f"{base} cm", f"{larger + lg} cm", f"{max(base + 1, larger - sm)} cm"]
    opts, ans = h10t._shuffle_options(correct, wrong)
    q["options"] = opts
    q["answer"] = ans
    q["explanation"] = f"Larger side = {base} × ({lg}/{sm}) = {larger} cm."
    if "smaller : larger" not in q["question"]:
        q["question"] = (
            f"Two similar triangles have sides in ratio {sm}:{lg} (smaller : larger). "
            f"If the smaller side is {base} cm, the corresponding larger side is:"
        )
    return True


def _fix_u6_t2_c(q: dict) -> bool:
    text = str(q.get("question", ""))
    if "Which ratio is correct" not in text:
        return False
    m = _BPT_SEG.search(text.replace("cm", ""))
    if not m:
        return False
    ad, db, ae, ec = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
    if ad * ec != ae * db:
        ec = ae * db // ad
    q["question"] = (
        f"In ΔABC, DE ∥ BC. AD = {ad} cm, DB = {db} cm, AE = {ae} cm. Find EC."
    )
    correct = f"{ec} cm"
    opts, ans = h10t._shuffle_options(
        correct, [f"{ec + db} cm", f"{max(1, ec - 1)} cm", f"{ae + 1} cm"]
    )
    q["options"] = opts
    q["answer"] = ans
    q["explanation"] = f"AD/DB = AE/EC ⇒ EC = {ae}×{db}/{ad} = {ec} cm."
    return True


def _fix_u6_t2_d(q: dict) -> bool:
    m = _PARALLEL.search(str(q.get("question", "")))
    if not m:
        return False
    pe, eq, pf, fr = int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))
    parallel = _bpt_ratios_equal(pe, eq, pf, fr)
    ans_text = "Yes, EF ∥ QR" if parallel else "No"
    opts, ans = h10t._shuffle_options(
        ans_text,
        ["No" if parallel else "Yes, EF ∥ QR", "Only if PQ = PR", "Cannot tell"],
    )
    q["options"] = opts
    q["answer"] = ans
    q["explanation"] = (
        f"PE/EQ = {pe}/{eq}, PF/FR = {pf}/{fr} "
        + ("(equal ⇒ parallel)." if parallel else "(not equal ⇒ not parallel).")
    )
    return True


def _fix_u6_t4_c(q: dict) -> bool:
    m = _SHADOW.search(str(q.get("question", "")))
    if not m:
        return False
    h_m, s_m, pole_s_m = float(m.group(1)), float(m.group(2)), float(m.group(3))
    h_cm, sh_cm, pole_sh_cm = int(h_m * 100), int(s_m * 100), int(pole_s_m * 100)
    h_pole = int(round(h_cm * pole_sh_cm / sh_cm))
    correct = f"{h_pole} cm"
    opts, ans = h10t._shuffle_options(
        correct,
        [f"{pole_sh_cm} cm", f"{h_cm} cm", f"{h_pole + max(10, pole_sh_cm // 2)} cm"],
    )
    q["options"] = opts
    q["answer"] = ans
    q["explanation"] = (
        f"height/shadow is constant: {h_cm}/{sh_cm} = h/{pole_sh_cm} ⇒ h ≈ {h_pole} cm."
    )
    return True


def _regen_from_template(q: dict) -> bool:
    uid, tid, lvl = int(q.get("unit_id", 6)), int(q.get("topic", 0)), str(q.get("level", ""))
    if not tid or not lvl:
        return False
    random.seed(_det_seed(str(q.get("id", ""))))
    fresh = h10t.generate_question(6, tid, lvl, templates_only=True)
    if not fresh:
        return False
    qid = q.get("id")
    fresh["id"] = qid
    fresh["source"] = q.get("source", "template")
    q.clear()
    q.update(fresh)
    return True


def repair_question(q: dict) -> list[str]:
    fixes: list[str] = []
    cat = str(q.get("category", ""))
    if _fix_bare_cm_options(q):
        fixes.append("bare_cm")
    if cat.startswith("u6_t1_D") or (
        q.get("level") == "D" and q.get("topic") == 1 and "smaller side" in str(q.get("question", ""))
    ):
        if _fix_u6_t1_d(q):
            fixes.append("scale_factor")
    if cat.startswith("u6_t2_C") or "Which ratio is correct" in str(q.get("question", "")):
        if _fix_u6_t2_c(q):
            fixes.append("bpt_c")
    if cat.startswith("u6_t2_D") or "Is EF ∥ QR" in str(q.get("question", "")):
        if _fix_u6_t2_d(q):
            fixes.append("bpt_d")
    if cat.startswith("u6_t4_C") or "pole casts" in str(q.get("question", "")).lower():
        if _fix_u6_t4_c(q):
            fixes.append("shadow")
    # If larger side still below smaller, regenerate
    if q.get("topic") == 1 and q.get("level") == "D":
        m = _RATIO_D.search(str(q.get("question", "")))
        if m:
            base = int(m.group(3))
            ans_i = int(q.get("answer", 0))
            try:
                ans_val = int(str(q["options"][ans_i]).split()[0])
            except (ValueError, IndexError, KeyError):
                ans_val = 0
            if ans_val < base and _regen_from_template(q):
                fixes.append("regen_t1_d")
    return fixes


def repair_file(path: Path) -> dict[str, int]:
    data = json.loads(path.read_text(encoding="utf-8"))
    stats: dict[str, int] = {}
    for bucket in data.get("questions", {}).values():
        if not isinstance(bucket, list):
            continue
        for q in bucket:
            if not isinstance(q, dict):
                continue
            for tag in repair_question(q):
                stats[tag] = stats.get(tag, 0) + 1
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return stats


def main() -> int:
    if not UNIT06_DIR.is_dir():
        print(f"Missing {UNIT06_DIR}", file=sys.stderr)
        return 1
    totals: dict[str, int] = {}
    for path in sorted(UNIT06_DIR.glob("topic_*.json")):
        stats = repair_file(path)
        if stats:
            print(f"{path.name}: {stats}")
        for k, v in stats.items():
            totals[k] = totals.get(k, 0) + v
    print("Totals:", totals)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
