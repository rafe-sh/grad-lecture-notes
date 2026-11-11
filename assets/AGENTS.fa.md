# Project Rules & Guidelines for Persian XeLaTeX Lecture Notes

This repository compiles lecture notes using **XeLaTeX** with **`xepersian`** and **`bidi`**. All AI models and contributors MUST strictly obey these rules to keep provenance unambiguous, typography readable, and rendered PDFs free of BiDi corruption.

---

## 1. BiDi & LTR / RTL Environment Rules

### A. Latin Runs, Numbers, Paths & Mixed Math-Latin in Persian Flow
- **Wrap every Latin run, number/range, date, file path, URL, or hybrid math-Latin term inside `\lr{...}`** (alias `\en{...}`), with attached punctuation placed inside `\lr{...}`:
  - Bad: `\item \textbf{الکترون‌های مستقل} ($e^-$--$e^-$): ...`
  - Good: `\textbf{الکترون‌های مستقل} (\lr{$e^-$--$e^-$}) ...`
  - Bad: `در بازهٔ 141--168 کتاب Ashcroft & Mermin`
  - Good: `در بازهٔ \lr{141--168} کتاب \lr{Ashcroft \& Mermin}`
- **Avoid bare inline parenthetical equations** in Persian prose (e.g., `($n(T)=n(0)$)` or `($g(\mathcal{E}<0)=0$)`), which XePersian frequently flips or pairs with double parentheses. Either integrate them naturally into Persian prose («یعنی $n(T)=n(0)$») or wrap the whole parenthetical run in `\lr{($n(T)=n(0)$)}`.

### B. Latin Units & Non-Persian Symbols (`\AA`, etc.)
- Always wrap `\AA` and Latin unit expressions in `\lr{...}` (or use `\angstrom` from `preamble.tex`):
  - Bad: `\text{\AA}` (inherits the Persian font context and causes `Missing character: There is no ̊ (U+030A) in font IRNazanin`)
  - Good: `\text{\lr{\AA}}` or `\angstrom`

### C. Section Headings, TOC & `hyperref` Bookmarks
- When placing math or parenthetical Latin expressions inside `\section{...}` or `\subsection{...}`, wrap them with `\texorpdfstring` so both the Table of Contents and PDF bookmarks render cleanly without unmatched outer parentheses:
  - Good: `\section{چگالی حالت‌ها \texorpdfstring{\lr{($g(\mathcal{E})$)}}{(g(E))}}`

### D. Titlepage Fields (`main.tex`)
- Wrap pure Latin/ASCII title fields (e.g., `\coursecode` = `\lr{PHYS-501}`, ASCII `\semester` = `\lr{1405-1}`) in `\lr{...}`.
- Keep Persian fields that contain parentheses (e.g., `نیم‌سال ۱۴۰۵-۱ (پاییز ۲۰۲۶)`) **unwrapped** so RTL parentheses are not scrambled.

### E. Helper Commands & Macros
- `\term{اصطلاح فارسی}{English term}` takes `(Persian, English)` and already outputs `اصطلاح فارسی~(\lr{English term})`. Never swap arguments and never wrap `\term` inside outer `(...)`.
- `\srcref{...}`, `\lecturetag{...}{...}`, and `\begin{supplement}[Reference]` already wrap their Latin arguments in `\lr{...}`.
- Use `\fa{...}` for Persian words inside math mode (`$E_{\fa{فرمی}}$`, `$u=\fa{ثابت}$`).
- `\pdv[order]{f}{x}` takes **two mandatory arguments** `{f}{x}` and an optional `[order]` (e.g., `\pdv{\psi}{x}`, `\pdv[2]{\psi}{x}`, `\pdv[2]{}{x}`).
- **Never use `\textenglish`** under `xepersian` (use `\lr{...}` inline and `\begin{latin}` for blocks).

---

## 2. TikZ, Tables & Equations

- **TikZ BiDi Labels**: Never put mixed Persian + math/Latin on one line inside a TikZ node (`\rl{دایرهٔ فرمی ($2\text{D}$)}` inverts parentheses). Use two-line centered nodes (`\node[align=center] ... {\rl{دایرهٔ فرمی} \\ \lr{($2\text{D}$)}};`), add `fill=white, inner sep=1.5pt` on labels near lines or dashed curves, and verify every vector arrow's physical sign and direction (e.g., diffusion vs. induced $\mathbf{E}$ field).
- **Tables**: In multi-column physics/data tables, place variable symbols in Header Row 1 and units in a dedicated Header Row 2 below them; keep cell phrasing concise to avoid stretched inter-word gaps.
- **Long Equations**: Split wide display formulas across lines using `align` so equation numbers never overlap text or terms.

---

## 3. Provenance, Prose Architecture & Textbook Standard

- **Visible Provenance**: Plain unboxed text and theorem environments represent lecture content; colored boxes (`supplement`, `discrepancy`, `todobox`, `summarybox`) contain everything added, derived, or verified beyond the lecture. Never invent lecture claims or unverified citations.
- **Textbook Narrative Flow**: Write in connected, scholarly academic Persian paragraphs (with proper ZWNJ half-spaces, like Ashcroft & Mermin or Kittel), not shallow outlines.
- **Strict Bullet Policy**: Do NOT break core physical explanations into fragmented bullet lists. Reserve bullet points strictly for concise comparative summaries (e.g., inside `summarybox` or tables).
- **Deep Self-Contained Explanations**: Connect every formula to physical motivation, hypotheses, boundary conditions, limiting cases, units/dimensions, and step-by-step derivations with no skipped algebra.
- **Personal Relevance ("Why this matters to me")**: At the beginning of each session's notes (right after `\lecturetag` or section intro), include a brief, concrete connected prose paragraph explaining why the session's main topic matters—linking it to industry applications helping people or familiar everyday phenomena (no bullet list).

---

## 4. Compilation & Visual Verification Standard

After editing any `.tex` file:
1. Build with the skill's multi-pass build script (or `xelatex` twice):
   ```bash
   python3 <SKILL_DIR>/scripts/build.py --render all
   ```
   (Or on specific pages: `--render 1 4-6`.)
2. Verify `build/main.log` has **0 errors**, **0 `Missing character:` warnings**, **0 `Undefined control sequence` errors**, and **0 undefined references**.
3. Visually inspect the rendered PNG previews (`build/preview/`) for every modified/new page, TOC entry, TikZ diagram, table, and equation block before reporting completion.
