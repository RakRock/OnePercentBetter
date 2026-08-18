# NCERT Class 9 Chapter Files

Drop chapter materials into folders here (e.g. `chapter_01/notes.md`).

Optional external folder — set only if you need it:

```bash
export HARSHIT_CLASS9_CHAPTERS="/path/to/your/chapters"
```

The app uses **only** this repo folder by default (safe for Streamlit Cloud).
Do not rely on `~/Downloads` unless you explicitly set the env var.

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
