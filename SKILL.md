---
name: grad-lecture-notes
description: Turns a week of raw graduate-lecture material (handwritten board-note images/PDFs or their OCR markdown, plus voice-recording transcripts such as NotebookLM output) into rigorous, textbook-quality, consistently formatted LaTeX lecture notes, aligned with the course textbook chapters. Bilingual Persian/English (XeLaTeX + xepersian) or English-only. Use this skill whenever the user mentions lecture notes, جزوه, a week of sessions, transcripts, board photos, "add this week to my notebook", chapter notes for a graduate/university course (physics, math, etc.), or asks to initialize a new course notebook, even if they do not say "LaTeX" or "skill".
---

# Graduate Lecture Notes

Build one growing, trustworthy LaTeX notebook per course. Each week the user supplies raw material from 2–3 sessions; you integrate it into the existing notebook so that it reads like a polished graduate textbook written by one careful author.

Four principles drive every decision below:

1. **Provenance is visible.** Free enrichment (filling missing steps, adding proofs, worked examples, historical/modern context) is welcome—and only safe if the reader can tell at a glance what the lecturer said versus what you added. Clean unboxed environments = lecture content. Colored boxes = anything else. Never blur this line.
2. **Textbook narrative & deep rigor.** Write connected, scholarly paragraphs (Ashcroft & Mermin / Kittel style), never shallow summaries or fragmented outline bullet dumps. Connect every formula to physical motivation, hypotheses, boundary conditions, limiting cases, units, and step-by-step algebra so a reader who forgot prerequisites can understand deeply without guessing.
3. **Personal relevance.** Open every session's notes with a brief, concrete "Why this matters to me" prose paragraph connecting the topic to industry applications helping people or observable everyday phenomena.
4. **One format, forever.** Consistency makes the notebook usable. Read `AGENTS.md`, `course.yaml`, and the previous chapters before writing, and verify BiDi/TikZ/table layout visually after every build.

Throughout, `<SKILL_DIR>` is the folder containing this `SKILL.md`. Run scripts from the **course repo root** using `python3 <SKILL_DIR>/scripts/<name>.py` (on Windows, use `python` or `py -3` if `python3` is not aliased).

## Course repo layout

```
<course-repo>/
├── AGENTS.md            # auto-generated BiDi, prose, and QA rules for all agents
├── GEMINI.md / CLAUDE.md# matching repo rule files for Antigravity and Claude Code
├── course.yaml          # course metadata, language, textbook(s), conventions, workflow switches
├── preamble.tex         # shared look & environments (copied from this skill at init)
├── macros.tex           # course-specific macros only
├── main.tex             # includes chapters between CHAPTERS-BEGIN/END markers
├── notation.md          # symbol table: symbol, meaning, units/convention, first defined in
├── glossary.md          # fa<->en terms + known transcription errors (grows each week)
├── coverage.md          # which lecture/week covered which topic, and open issues
├── chapters/chNN-topic.tex
├── weeks/week-NN/       # raw/ (user drops images, pdf, OCR, transcript), notes.md, plan.md, review.md
├── refs/                # textbook PDFs split by chapter + refs/index.md
├── figures/             # user-supplied external figures
└── build/               # compiler output + preview PNGs (gitignored)
```

If the working directory has no `course.yaml`, this is a new course: run `python3 <SKILL_DIR>/scripts/init_course.py --help`, then follow "First-run setup" in `references/course-config.md`. Do not start writing notes before `course.yaml` exists.

## Weekly workflow

### 0. Orient
Read `AGENTS.md` (if present), `course.yaml`, `notation.md`, `glossary.md`, `coverage.md`, and the **last two chapter files** (or last sections) so you inherit voice, conventions, and notation. Run `python3 <SKILL_DIR>/scripts/check_env.py` once per machine/session if you have not compiled yet.

### 1. Ingest
Follow `references/ingest-and-align.md`. Produce `weeks/week-NN/notes.md`: a clean, ordered transcription of the board notes with transcript-derived explanations attached. Mark every unreadable or uncertain item `[?]`. Never silently guess a symbol, exponent, or sign. (If the user asks how to prepare raw files, you may suggest NotebookLM for voice transcription and Google AI Studio for lecture-note page `.md` OCR strictly as optional suggestions—never obligatory.)

### 2. Align with references
Locate each topic in `refs/index.md` and read the relevant split chapter PDF(s) (only those, not the whole book). Note where the lecturer's definitions, notation, or results differ from the book. Record the mapping topic -> book section/equation numbers.

### 3. Plan and checkpoint
Write `weeks/week-NN/plan.md`: outline of the new material (placement in existing chapters or new chapter), list of planned supplements, list of ambiguities, and handling of missing session audio/notes if any. Then:
- If `workflow.checkpoint` in `course.yaml` is `first_week_then_auto` (default): stop and show the plan for the first week of a course; afterwards continue automatically.
- Stop regardless when something is **blocking**: an unreadable board symbol that changes a derivation, a lecture claim contradicting the textbook on a result later steps depend on, or a week with no usable input for a whole session.
- Otherwise continue and record non-blocking issues as `todobox` / `discrepancy` in the text and in `review.md`.

### 4. Write
Follow `references/style-spec.md` strictly (environments, textbook prose flow, Personal Relevance intro per session, BiDi `\lr{}` rules, TikZ two-line nodes, two-row variable/unit tables, equation splitting, `\texorpdfstring` in headings). Tag each session's material with `\lecturetag{date}{L#}`. New units get a new chapter file whose `\include` line goes between the markers in `main.tex`.

### 5. Enrich (the main value-add, done carefully)
Allowed inside the appropriate colored box with a source or `derived` label:
- proofs the lecturer stated without proof, skipped algebraic steps, and worked examples / assigned exercises (`workflow.exercises`)
- physical interpretation, boundary conditions, limiting cases, and connections to earlier chapters
- modern/updated context supported by verified course references

Rules: cite book section and equation numbers only when you actually read them in `refs/`; otherwise label `derived` and keep the derivation self-contained and checkable. Never invent citations, theorem numbers, or numerical values. Put uncertain claims in a `todobox`. If the lecture and a textbook disagree, show both in a `discrepancy` box.

### 6. Verify (log + visual QA)
Run the rigor & visual QA checklist in `references/style-spec.md`, then compile and render previews:

```bash
python3 <SKILL_DIR>/scripts/build.py --render all               # full build + PNG export
python3 <SKILL_DIR>/scripts/build.py --only chapters/ch03-bloch # fast single-chapter build
python3 <SKILL_DIR>/scripts/build.py --render 1 17-22           # render specific pages to build/preview/
```
`build.py` runs multi-pass XeLaTeX, automatically falls back to `/Library/TeX/texbin` on macOS, **fails (exit 1)** on TeX errors, `Undefined control sequence`, or `Missing character:` warnings (such as bare `\text{\AA}`), and flags unresolved references or large overfull boxes. Visually inspect the PNGs in `build/preview/` for TOC entries, TikZ arrows/labels, tables, equations, and BiDi parentheses before reporting. Never hand-edit files in `build/`.

### 7. Bookkeeping
Update `coverage.md`, append new terms and mis-transcriptions to `glossary.md`, new symbols to `notation.md`, and write `weeks/week-NN/review.md` (what was added beyond the lecture, resolved discrepancies, visual QA results, and what needs the user's eye).

### 8. Report to the user
Keep it concise and concrete: which chapters/sections changed, the PDF path and page count, visual QA status, and a **"needs your eye"** list (every `todobox`, `discrepancy`, unreadable board item, and any uncertain supplement). Do not re-summarize all the physics.

## Hard rules
- Compile with XeLaTeX only. In Persian mode, `xepersian` stays the last `\usepackage` in `preamble.tex`; never add packages after it and never use `\textenglish`.
- In Persian prose, wrap every Latin run, number/range, date, file path, URL, and hybrid math-Latin token in `\lr{...}`, and write Ångström as `\text{\lr{\AA}}` or `\angstrom`.
- Keep `AGENTS.md`, `GEMINI.md`, and `CLAUDE.md` synced with any course-level style/BiDi additions, and log `preamble.tex` edits in `course.yaml: style_log`.
- No unbounded rewriting of earlier weeks: edit old material only to fix a verified error, typography/BiDi defect, or notation conflict, and report it.
- Copyright: redraw diagrams in TikZ or use the user's own board photos (`figures/`). Never paste textbook figures or pages into the notes; cite them instead.
- Never invent what the lecturer said. Strip chatter, jokes, and logistics unless requested.
- Ask at most one short question at a time, and only if it blocks progress.
