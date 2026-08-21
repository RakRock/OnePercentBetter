# NCERT Class 10 — Harshit Math

Fifteen units aligned with NCERT Class 10 Mathematics.

## Unit 1 — Real Numbers

- PDF: `units/unit_01/jemh101.pdf` (NCERT Chapter 1)
- Topics: FTA & prime factorisation, HCF/LCM, irrational proofs, rationals + irrationals
- Practice: 15 MCQs per session, difficulty slider (Foundation A → Challenge E)

## Unit 2 — Polynomials

- PDF: `units/unit_02/jemh102.pdf` (NCERT Chapter 2)
- Topics: degree & types, geometrical zeroes, zeroes–coefficient relations, division algorithm
- Practice: same format as Unit 1 (Week Setup + Practice tabs, email & Google Sheets on completion)

## Unit 3 — Pair of Linear Equations in Two Variables

- PDF: `units/unit_03/jemh103.pdf` (NCERT Chapter 3)
- Topics: graphical/consistency, substitution, elimination, cross-multiplication & applications

## Unit 4 — Quadratic Equations

- PDF: `units/unit_04/jemh104.pdf` (NCERT Chapter 4)
- Topics: standard form, factorisation, quadratic formula, discriminant

## Question banks

`question_banks/unit_XX/topic_YY.json` — seeded from NCERT-aligned templates:

```bash
python scripts/seed_harshit_class10_banks.py --unit 1 --per-level 15
python scripts/seed_harshit_class10_banks.py --unit 2 --per-level 15
python scripts/seed_harshit_class10_banks.py --unit 3 --per-level 15
python scripts/seed_harshit_class10_banks.py --unit 4 --per-level 15
```

## External PDF folder (optional)

Set `HARSHIT_CLASS10_UNITS` to a directory with `unit_01/`, `unit_02/`, … subfolders.
