# NCERT Class 9 Chapter Files

Drop chapter materials into folders here (e.g. `chapter_01/notes.md`).

Optional external folder — set only if you need it:

```bash
export HARSHIT_CLASS9_CHAPTERS="/path/to/your/chapters"
```

The app uses **only** this repo folder by default (safe for Streamlit Cloud).
Do not rely on `~/Downloads` unless you explicitly set the env var.

## Question banks (from chapter PDFs)

After adding PDFs, build cached MCQs derived from the book:

```bash
export XAI_API_KEY=your_key
python3 scripts/import_harshit_class9_chapters.py
python3 scripts/build_harshit_chapter_questions.py --prereq 1 --per-level 4
python3 scripts/build_harshit_chapter_questions.py --all --per-level 3
```

Banks are saved under `HarshitMath/question_banks/`. Practice prefers these over generic templates.

With `XAI_API_KEY` set, the app can also generate live from PDF excerpts when the bank is empty (Week Setup → *Generate from chapter PDFs*).

## Supported formats

- Markdown / text: `.md`, `.markdown`, `.txt`
- PDF: `.pdf`

## Naming (any of these work)

```
chapter_01/
  notes.md
  chapter.pdf

Chapter 1/
  Number-Systems.md

chapter-02-polynomials.pdf
```

## Chapters used by PreReq buckets

| PreReq | Chapters |
|--------|----------|
| 1 — Number Systems & Foundations | 1 |
| 2 — Algebraic Operations & Equations | 2, 4 |
| 3 — Coordinate Graphing | 3 |
| 4 — Core Euclidean Geometry | 5, 6, 7, 8, 10 |
| 5 — Mensuration | 12, 13 |
| 6 — Data & Probability | 14, 15 |

Override the external path with env var `HARSHIT_CLASS9_CHAPTERS`.
