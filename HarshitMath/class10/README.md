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

## Unit 5 — Arithmetic Progressions

- PDF: `units/unit_05/jemh105.pdf` (NCERT Chapter 5)
- Topics: AP definition, nth term, sum of n terms, word problems
- Unit Guide, Practice, Unit Test, and Week Setup (same as Units 2–4)

## Unit 6 — Triangles

- PDF: `units/unit_06/jemh106.pdf` (NCERT Chapter 6)
- Topics: similar figures & scale factor, BPT, similarity criteria (AAA/SSS/SAS), Pythagoras & applications
- Unit Guide, Practice, Unit Test, and Week Setup (same as Units 2–5)

## Question banks

`question_banks/unit_XX/topic_YY.json` — seeded from NCERT-aligned templates:

```bash
python scripts/seed_harshit_class10_banks.py --unit 1 --per-level 15
python scripts/seed_harshit_class10_banks.py --unit 2 --per-level 15
python scripts/seed_harshit_class10_banks.py --unit 3 --per-level 15
python scripts/seed_harshit_class10_banks.py --unit 4 --per-level 15
python scripts/seed_harshit_class10_banks.py --unit 5 --per-level 15
python scripts/seed_harshit_class10_banks.py --unit 6 --per-level 15
```

## External PDF folder (optional)

Set `HARSHIT_CLASS10_UNITS` to a directory with `unit_01/`, `unit_02/`, … subfolders.
