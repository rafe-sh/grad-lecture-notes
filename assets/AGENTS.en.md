# Project Rules & Guidelines for XeLaTeX Lecture Notes

This repository compiles graduate lecture notes using **XeLaTeX**. All AI models and contributors MUST strictly follow these rules to keep provenance unambiguous, explanations deep, and rendered PDFs clean.

---

## 1. Provenance & Prose Architecture

- **Visible Provenance**: Plain unboxed prose and theorem environments represent material from the lecturer. Colored boxes (`supplement`, `discrepancy`, `todobox`, `summarybox`) represent everything added, derived, or verified beyond the lecture. Never blur this boundary, never invent lecture claims, and never cite a section or equation number you did not verify in `refs/`.
- **Textbook Narrative Flow**: Write in connected, scholarly graduate-textbook prose (Ashcroft & Mermin / Kittel style) rather than shallow outlines or fragmented bullet dumps. Reserve bullet lists strictly for concise comparative summaries (e.g., inside `summarybox` or tables).
- **Deep Self-Contained Explanations**: Connect every formula to its physical motivation, hypotheses, boundary conditions, limiting cases, dimensional checks, and complete step-by-step derivations so the reader does not have to guess missing steps.
- **Personal Relevance ("Why this matters to me")**: At the beginning of each session's notes (right after `\lecturetag` or section intro), include a brief, concrete connected paragraph tying the topic to industry applications helping people or familiar observable phenomena (integrated as prose, not a bullet list).

---

## 2. LaTeX, Macros, TikZ & Tables

- **Macro Signatures**:
  - `\pdv[order]{f}{x}` takes **two mandatory arguments** `{f}{x}` and an optional `[order]` (e.g., `\pdv{\psi}{x}`, `\pdv[2]{\psi}{x}`, `\pdv[2]{}{x}`).
  - `\term{fa}{en}` prints the English term in `\emph{...}` when `\notesfafalse`.
  - `\srcref{...}` and `\lecturetag{date}{L#}` mark textbook alignment and session boundaries.
- **Section Headings & TOC (`hyperref`)**: Use `\texorpdfstring{...}{...}` when section headings contain math so PDF bookmarks compile cleanly without warnings.
- **TikZ Figures**: Add white background pads (`fill=white, inner sep=1.5pt`) on labels near curves or dashed guides, and perform a physics sanity check on every vector arrow's sign and direction.
- **Tables & Equations**: Separate variable symbols (Header Row 1) and physical units (Header Row 2) in scientific tables; split wide display formulas across lines using `align` so equation numbers never collide with text.

---

## 3. Compilation & Visual Verification Standard

After editing any `.tex` file:
1. Build with the skill's multi-pass build script:
   ```bash
   python3 <SKILL_DIR>/scripts/build.py --render all
   ```
   (Or pass `--only chapters/chNN-topic` and specific pages to `--render`.)
2. Verify `build/main.log` has **0 errors**, **0 `Missing character:` warnings**, **0 `Undefined control sequence` errors**, and **0 undefined references**.
3. Visually inspect rendered PNG previews (`build/preview/`) for every modified/new page, TOC entry, TikZ diagram, table, and equation block before reporting completion.
