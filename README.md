# Graduate Lecture Notes (`grad-lecture-notes`)

Turn weekly raw lecture inputs—handwritten board photos/PDFs, OCR markdown drafts, and lecture audio transcripts (e.g., NotebookLM exports)—into a unified, graduate-textbook-quality LaTeX notebook aligned with your course textbooks. Supports **bilingual Persian/English (`xepersian` + XeLaTeX)** and **English-only** courses.

---

## 1. Where to Put This Skill (Installation Folders)

Clone this repository or unzip `grad-lecture-notes.zip` so the `grad-lecture-notes/` directory (containing `SKILL.md`, `README.md`, `references/`, `assets/`, `scripts/`) sits in your AI agent's skill directory:

| Agent / Tool | Global Install (all projects) | Project-Local Install (one repo) | Notes |
|---|---|---|---|
| **Antigravity** | `~/.gemini/config/skills/grad-lecture-notes/` | `<course-repo>/.agents/skills/grad-lecture-notes/` | Discovered automatically via `SKILL.md` |
| **Claude Code** | `~/.claude/skills/grad-lecture-notes/` | `<course-repo>/.claude/skills/grad-lecture-notes/` | Restart session after copying |
| **Claude Desktop / Web** | *Settings → Capabilities → Skills → Upload* | — | Upload `grad-lecture-notes.zip` directly |
| **OpenCode** | `~/.config/opencode/skills/grad-lecture-notes/` | `<course-repo>/.opencode/skills/grad-lecture-notes/` | Compatible with `SKILL.md` |
| **OpenAI Codex CLI** | `~/.codex/skills/grad-lecture-notes/` | `<course-repo>/.agents/skills/grad-lecture-notes/` | Discovered automatically |

**Quick `git clone` examples:**
```bash
# Antigravity (global)
git clone https://github.com/rafe-sh/grad-lecture-notes.git ~/.gemini/config/skills/grad-lecture-notes

# Claude Code (global)
git clone https://github.com/rafe-sh/grad-lecture-notes.git ~/.claude/skills/grad-lecture-notes
```

> **Tip:** Make sure the directory inside `skills/` is `grad-lecture-notes/SKILL.md` (not nested twice like `grad-lecture-notes/grad-lecture-notes/SKILL.md`). If you download GitHub's auto-generated branch zip, rename `grad-lecture-notes-main/` to `grad-lecture-notes/`.

---

## 2. Prerequisites & Environment Check

1. **Python 3.8+** (`python3` on macOS/Linux; `python` or `py -3` on Windows)
2. **XeLaTeX distribution**: MacTeX (macOS), TeX Live (Linux/Windows), TinyTeX, or MiKTeX with `xepersian`, `bidi`, `tcolorbox`, `tikz`, `mathtools`, `amsthm`, `titlesec`, `fancyhdr`, `geometry`, `hyperref`, `booktabs`, `xcolor`.
3. **Optional Python / PDF tools**:
   - `pip install pypdf` — required only for splitting full textbook PDFs by chapter (`split_pdf.py`).
   - `pip install pymupdf` (or `poppler` for `pdftoppm`) — used by `build.py --render` to export PNG previews for visual BiDi & TikZ inspection.

Verify your machine in one command (macOS automatically checks `/Library/TeX/texbin` if not on `PATH`):

```bash
python3 <SKILL_DIR>/scripts/check_env.py
```

---

## 3. Course Folder Map: Where to Put Your Files

Inside your course folder (created by `init_course.py` or when you ask your agent to start a new course), **only three folders hold files you drop in manually**:

```text
<my-course-repo>/
├── refs/                         <-- [YOU PUT] Full textbook PDFs here (plus split chapter PDFs)
│   └── index.md                      (agent maintains chapter-to-PDF mapping)
├── weeks/
│   ├── week-01/
│   │   ├── raw/                  <-- [YOU PUT] Week 1 board photos, board PDFs, OCR .md, voice transcripts
│   │   ├── notes.md                  (agent-cleaned lecture log)
│   │   ├── plan.md                   (agent integration plan)
│   │   └── review.md                 (agent summary & items needing your eye)
│   └── week-02/
│       └── raw/                  <-- [YOU PUT] Week 2 files here, etc.
├── figures/                      <-- [YOU PUT] Optional external figures/board snapshots to embed
│
├── chapters/                     <-- (agent writes/updates ch01-..., ch02-...)
├── main.tex                      <-- (master LaTeX file; agent adds \include lines)
├── preamble.tex                  <-- (shared LaTeX styles & BiDi-safe macros)
├── macros.tex                    <-- (course-specific LaTeX shortcuts)
├── course.yaml                   <-- (course settings, conventions, workflow flags)
├── notation.md                   <-- (running symbol table)
├── glossary.md                   <-- (fa <-> en terminology + voice mis-transcription log)
├── coverage.md                   <-- (week-by-week topic map)
├── AGENTS.md / GEMINI.md / CLAUDE.md  (auto-generated rules so every AI agent respects BiDi & style)
└── build/                        <-- (compiled main.pdf & preview/ PNGs -- gitignored, never hand-edit)
```

### Quick Checklist: What Goes Where
- **Full textbook PDFs** (e.g., *Ashcroft & Mermin*, *Kittel*) → drop into `refs/` and ask the agent to split them by chapter (or run `split_pdf.py`).
- **Weekly board images / PDFs / OCR `.md` / audio transcripts** → drop into `weeks/week-NN/raw/` (e.g., `weeks/week-01/raw/notes-oct-28.md`, `voice-oct-28.md`, `board-1.jpg`).
- **Anything you want embedded directly as an image** → put in `figures/`.
- **Never manually edit files inside `build/`** — `build/main.pdf` and `build/preview/` are regenerated on every build.

### Optional Suggestions for Preparing Raw Files (Not Obligatory)
- **Voice transcripts (`voice-*.md` / `.txt`):** For recorded lecture audio, you can optionally use **NotebookLM** voice transcription (or any transcription tool you prefer) and drop the output into `weeks/week-NN/raw/`.
- **Handwritten lecture-note pages (`notes-*.md`):** For handwritten board photos or scanned note pages, you can optionally use **Google AI Studio** to generate a draft `.md` file in `weeks/week-NN/raw/`—or simply drop the raw photos/PDFs directly into `weeks/week-NN/raw/` (providing both lets the agent cross-check the OCR draft against the images). Neither tool is required.

---

## 4. How to Use (Prompts & Standalone CLI)

### Option A: Using Your AI Agent (Recommended)

1. **Initialize a new course** (from an empty course directory):
   > "Initialize a new graduate lecture notebook here for *Advanced Solid State Physics* in Persian (`fa`), using Kittel and Ashcroft & Mermin in `refs/`."
2. **Split textbook PDFs** (optional, saves huge context/tokens):
   > "Split the textbook PDFs in `refs/` into per-chapter PDFs and create `refs/index.md`."
3. **Add each week's notes** (after putting raw files into `weeks/week-NN/raw/`):
   > "Add `weeks/week-01/raw/` to my lecture notebook, align with `refs/`, compile, and visually check the rendered pages."

### Option B: Running the Scripts Directly (Standalone Verification)

Replace `<SKILL_DIR>` with the folder where you unzipped `grad-lecture-notes`:

```bash
# 1. Check XeLaTeX, packages, fonts, and PDF helpers
python3 <SKILL_DIR>/scripts/check_env.py

# 2. Initialize a new course folder (creates main.tex, preamble.tex, course.yaml, AGENTS.md/GEMINI.md/CLAUDE.md, starter chapter)
python3 <SKILL_DIR>/scripts/init_course.py \
  --dir ./MyCourse \
  --lang fa \
  --title "فیزیک حالت جامد پیشرفته" \
  --code "PHYS-501" \
  --semester "نیم‌سال ۱۴۰۵-۱ (پاییز ۲۰۲۶)"

# 3. Compile the starter notebook and render PNGs for visual inspection
python3 <SKILL_DIR>/scripts/build.py --dir ./MyCourse --render all

# 4. Split a textbook PDF by chapter into refs/
cd ./MyCourse
python3 <SKILL_DIR>/scripts/split_pdf.py refs/textbook.pdf --outline
python3 <SKILL_DIR>/scripts/split_pdf.py refs/textbook.pdf --out refs --auto --key kittel

# 5. Fast single-chapter rebuild during writing
python3 <SKILL_DIR>/scripts/build.py --only chapters/ch01-drude --render 1-5
```

---

## 5. Built-In Quality, Provenance & BiDi Protections

This package incorporates battle-tested fixes for graduate physics/math notes and Persian `xepersian` typesetting:

- **Visible Provenance**: Lecture definitions/theorems stay unboxed; supplementary proofs, missing steps, and worked exercises live in teal `supplement` boxes; lecture-vs-textbook differences live in red `discrepancy` boxes; unresolved board ambiguities live in amber `todobox`es.
- **Textbook Prose & Personal Relevance**: Notes follow a connected graduate-textbook narrative (no shallow outline bullet dumps) with full step-by-step algebra and a concise **"Why this matters to me"** paragraph opening each session.
- **Strict BiDi & XeLaTeX Safety**:
  - `build.py` **fails immediately (exit code 1)** on any `Missing character:` warning (catching glyphs dropped by Persian fonts like bare `\text{\AA}`) as well as `Undefined control sequence` and BiDi errors.
  - `preamble.tex` provides `\angstrom` (`\text{\lr{\AA}}`) and supports optional derivative order `\pdv[2]{f}{x}` alongside `\pdv{f}{x}`.
  - `init_course.py` auto-wraps pure-ASCII titlepage metadata (`--code`, ASCII `--semester`) in `\lr{...}` while leaving Persian text with parentheses unwrapped, and generates `AGENTS.md`, `GEMINI.md`, and `CLAUDE.md` in every new course repo.
  - `build.py --render` exports PNG pages to `build/preview/` so TikZ arrows/labels, TOC parentheses, tables, and equation numbers can be visually verified.

---

## 6. Troubleshooting

- **`xelatex not found`**: On macOS, MacTeX installs to `/Library/TeX/texbin/xelatex`. `check_env.py` and `build.py` check `/Library/TeX/texbin` automatically; if using a custom TeX Live path, add it to `PATH`.
- **`python: command not found` on macOS/Linux**: Use `python3` (the documentation and scripts all use `python3`).
- **`Missing character:` build failure**: Usually caused by bare `\text{\AA}` or Latin symbols inside Persian math/text context. Replace with `\text{\lr{\AA}}` or `\angstrom`, and wrap Latin/number/date runs in `\lr{...}`.
- **`pypdf` or `pymupdf` missing**: Compilation works with standard library Python only; install `pip install pypdf pymupdf` (or `brew install poppler` for `pdftoppm`) if you want PDF chapter splitting and `--render` PNG previews.
