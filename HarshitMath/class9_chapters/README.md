# NCERT Class 9 chapter files

Place one folder per chapter: `chapter_01/`, `chapter_02/`, … each containing a PDF or notes.

## Extract from the combined textbook

If you have `ncert-books-for-class-9-maths.pdf`, extract missing chapters with:

```bash
python3 scripts/extract_ncert_chapters_from_book.py \
  --source ~/Downloads/Harshit-Math/ncert-books-for-class-9-maths.pdf \
  --chapters 13 14 15
```

| Chapter | Book pages | Content |
|---------|------------|---------|
| 13 | 208–237 | Surface Areas and Volumes |
| 14 | 238–270 | Statistics |
| 15 | 271–285 | Probability |

Then build question banks:

```bash
python3 scripts/build_harshit_chapter_questions.py --prereq 5 --per-level 8
python3 scripts/build_harshit_chapter_questions.py --prereq 6 --per-level 8
```
