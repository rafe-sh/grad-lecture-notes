# Course Configuration and First-Run Setup

Contents: 1 course.yaml · 2 First-run setup · 3 Updating conventions

## 1. course.yaml

```yaml
course:
  title: "فیزیک حالت جامد پیشرفته"     # shown in headers
  title_en: "Advanced Solid State Physics"
  code: ""
  semester: "نیم‌سال ۱۴۰۵-۱ (پاییز ۲۰۲۶)"
  instructor: ""
  author: ""

language:
  mode: fa                 # fa = Persian prose + English terms (xepersian) | en = English only
  terms: parenthetical     # first use per chapter: Persian (English)

organization: topic        # topic: chapters follow lecturer's units, each carries \srcref to book sections
                           # (alternative: book = mirror textbook chapters exactly)

references:
  primary: kittel
  books:
    kittel:  {title: "Introduction to Solid State Physics", author: "Kittel", edition: "", dir: refs}
    am:      {title: "Solid State Physics", author: "Ashcroft & Mermin", edition: "", dir: refs}

conventions:
  units: SI                # or gaussian / natural (ħ=c=1)
  fourier: "f(k)=∫ f(r) e^{-ik·r} d^3r"
  time_dependence: "e^{-iωt}"
  ltr: 'STANDING RULE: wrap every Latin run, number, date, range, file path, URL, or hybrid math-Latin token inside Persian prose in \lr{...} (alias \en{...}), with attached punctuation inside \lr{...}. Use \text{\lr{\AA}} or \angstrom (never bare \text{\AA}). Inspect build/main.log and rendered pages after every build.'
  notes: ""

workflow:
  checkpoint: first_week_then_auto   # always | first_week_then_auto | never
  enrichment: free                   # free | sourced_only | none
  prose_style: textbook              # textbook (connected narrative paragraphs) | concise
  personal_relevance: true           # brief "Why this matters to me" prose paragraph per session
  exercises: if_assigned             # include assigned problems with solutions in supplement boxes
  citations: only_verified           # never cite what you have not read in refs/

latex:
  engine: xelatex
  fonts_text: IRNazanin              # preamble falls back automatically if missing
  fonts_title: IRLotus
  fonts_latin: "Times New Roman"

style_log: []                        # one line per deviation/addition to preamble.tex, with date
```

Agents: read `course.yaml` and `AGENTS.md` (or `GEMINI.md` / `CLAUDE.md`) at the start of every session; never infer these values from habit.

## 2. First-run setup (new course)

1. Ask only what you cannot infer, in one short message: course title and field; Persian+English or English-only; the main textbook(s) and whether PDFs are available; the lecturer's units/syllabus if any; convention preferences (units, Fourier convention). Offer sensible defaults and let the user answer "defaults".
2. Run:
   ```bash
   python3 <SKILL_DIR>/scripts/init_course.py --dir . --lang fa|en --title "..."
   ```
   (On Windows if `python3` is not aliased, use `python` or `py -3`.) This creates the repo tree, writes `main.tex` (with smart `\lr{...}` wrapping for ASCII titlepage fields in `fa` mode), copies `preamble.tex` and starter metadata files, generates `AGENTS.md`, `GEMINI.md`, and `CLAUDE.md`, and adds a starter chapter to verify the toolchain.
3. Run `python3 <SKILL_DIR>/scripts/check_env.py` to check `xelatex`, TeX packages, fonts, `pypdf`, and visual-QA renderers (`pymupdf` / `pdftoppm`). Resolve any missing requirements before continuing.
4. Run `python3 <SKILL_DIR>/scripts/build.py --render all`: the starter chapter must compile with `0` errors and `0 Missing character:` warnings. Visually check the rendered starter page(s) in `build/preview/`, then delete `chapters/ch00-starter.tex` and its `\include` line in `main.tex`.
5. If textbook PDFs exist in `refs/`: split them per chapter (see `ingest-and-align.md` section 6) and write `refs/index.md`.
6. Seed `notation.md` and `glossary.md` from the syllabus/first chapter of the book with standard symbols and terms for the field.
7. Show the user the resulting tree and starter-check outcome, then proceed to Week 1 (checkpoint applies).

## 3. Updating conventions

If the lecturer switches convention mid-course (e.g. Fourier sign, units), do not rewrite old chapters silently: record the change in `course.yaml: conventions.notes`, add a `remark` at the switch, and ask the user whether earlier chapters should be converted.
