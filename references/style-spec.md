# Style Specification

The format contract for every chapter. Contents: 1 Environments · 2 Topic anatomy & prose style · 3 Language & BiDi rules · 4 Math, derivations & tables · 5 Figures · 6 Labels and references · 7 Rigor & visual QA checklist

## 1. Environments

The rule that matters: **plain = lecturer, colored box = not the lecturer.**

### Lecture content (plain amsthm-style, no box)
| Env | Use |
|---|---|
| `definition` | A defined term or object. Introduce the term with `\term{fa}{en}` the first time. |
| `theorem`, `proposition`, `lemma`, `corollary` | Precise statements with all hypotheses. Optional title in brackets: `\begin{theorem}[Bloch]`. |
| `proof` | Only when the lecturer gave the proof (or a proof directly following the lecture's own argument). |
| `example` | Examples or assigned exercises worked in lecture (solutions beyond class go in `supplement`). |
| `remark` | Lecturer's comments, caveats, or physical intuition stated in class. |

All share one counter per chapter (Theorem 3.4 follows Definition 3.3).

### Added by you (colored boxes)
| Env | Color | Use |
|---|---|---|
| `\begin{supplement}[Source]` | teal | Anything beyond the lecture that is *sourced*: `[Ashcroft--Mermin, Ch.~8, Eq.~(8.4)]`. Omit the argument for material you derived yourself (the title then prints "derived"). Supplementary proofs, intermediate derivation steps, worked examples, historical/modern context. |
| `\begin{discrepancy}` | red | Lecture and a source disagree (result, sign, factor, convention). State both versions, name the source, and say which one the rest of the notes follow and why. |
| `\begin{todobox}` | amber | Needs the user: unreadable board item, unverified claim, missing session. One clear sentence on what to check. |
| `\begin{summarybox}` | gray | End-of-topic / end-of-chapter summary of key results. The only box that restates lecture content. |

Never nest boxes. Never put an unverified claim in plain text.

### Helper macros (defined in `preamble.tex`)
- `\lecturetag{2026-10-28}{L5}`: thin rule marking where material from a session starts. Put one at the start of each session's material, even when sessions interleave topics.
- `\srcref{Kittel, Ch.~7, Sec.~3}`: gray reference line placed right after a section heading, listing where the textbook covers it.
- `\term{fa}{en}`: Persian term with English in parentheses (`اصطلاح فارسی~(\lr{English term})`, or `\emph{English term}` in English-only mode). **Argument order is strictly `(Persian, English)`**, and `\term` already adds the parentheses—never swap arguments and never wrap `\term` inside outer `(...)`.
- `\fa{...}`: Persian text inside math: `$E_{\fa{فرمی}}$`, `$u=\fa{ثابت}$`.
- `\en{...}` or `\lr{...}`: force left-to-right Latin text inside Persian prose.
- `\angstrom`: safe Ångström symbol (`\text{\lr{\AA}}`) that never triggers missing Persian font glyph errors.
- Physics macros: `\ket`, `\bra`, `\braket`, `\expval`, `\abs`, `\norm`, `\dd`, `\ii`, `\ee`, `\vb`, `\Tr`, `\hc`, and `\pdv[order]{f}{x}` (takes **two mandatory arguments** `{f}{x}` and an optional `[order]`, e.g., `\pdv{\psi}{x}`, `\pdv[2]{\psi}{x}`, `\pdv[2]{}{x}`). Course-specific macros go in `macros.tex`.
- **Never use `\textenglish`** under `xepersian`; use `\lr{...}` inline and `\begin{latin}` for blocks.

## 2. Topic anatomy & textbook prose style

Every chapter must read like a self-contained graduate textbook (e.g., Ashcroft & Mermin or Kittel) written so a reader who has forgotten prerequisite details can follow every step without guessing.

### Session & topic flow
1. **Personal Relevance ("Why this matters to me")**: At the beginning of each session's notes (right after `\lecturetag` or the session's opening section intro), include one brief, concrete, connected paragraph explaining why the main topic matters—connecting the physics to industry applications that help people or to a familiar phenomenon observable in everyday life. Integrate this naturally into prose (never as a bullet list).
2. **Motivation**: What physical question is being answered, what is already known, and why earlier assumptions fail.
3. **Setup and definitions**: Every object, symbol, hypothesis, and convention stated explicitly.
4. **Statement**: Theorem, proposition, or physical law with all conditions stated.
5. **Proof or derivation**: From the lecture (plain `proof` or connected derivation prose), with skipped algebraic steps, physical justifications, and textbook derivations filled in cleanly inside `supplement` boxes rather than leaving the reader to infer gaps.
6. **Meaning & limiting cases**: Physical interpretation, dimensions/units, orders of magnitude, and sanity-check limits (free-electron limit, $T \to 0$, weak/strong coupling).
7. **Example / Exercise**: Worked in class (`example`); extra worked examples or assigned exercise solutions (`workflow.exercises`) in `supplement` boxes or a dedicated end-of-chapter Exercises section.
8. **Summary**: End-of-chapter or major-section `summarybox` with comparative balance sheets or key takeaways.

### Textbook Narrative Prose (Strict Bullet Policy)
- **Write connected, scholarly prose paragraphs**: Do NOT dump fragmented bullet lists or outline-style summaries in the main body. Connect ideas, derivations, and physical reasoning smoothly across complete paragraphs.
- **Bullets are restricted**: Reserve `itemize`/`enumerate` strictly for concise comparative summaries (e.g., inside `summarybox` or tables) or numbered axioms/steps when genuine enumeration adds clarity over prose.

## 3. Language & BiDi rules

- **Persian mode (`\notesfatrue`)**:
  - Prose in natural, formal academic Persian with accurate ZWNJ half-spaces (`می‌شود`، `نمی‌دانیم`، `شبکه‌های`، `مدل درود`). No slang, no exam-hook chatter, no conversational filler.
  - Introduce technical terms with `\term{اصطلاح فارسی}{English term}` at first occurrence in each chapter, then Persian only (using the form fixed in `glossary.md`).
  - **Mandatory `\lr{...}` rule**: Never leave bare English words, hybrid math-Latin terms, numbers, Jalali/Gregorian dates, numeric ranges, file paths, or URLs inside Persian RTL text without `\lr{...}`. Attached punctuation stays inside `\lr{...}`:
    - Good: `\textbf{تقریب الکترون‌های مستقل} (\lr{$e^-$--$e^-$})`, `\lr{$e^-$--ion}`, `\lr{141--168}`, `\lr{Ashcroft \& Mermin}`.
    - Bad: `($e^-$--ion)` or `($e^-$--$e^-$)` without `\lr{...}` (XePersian reverses sub-elements).
  - **Units & `\AA`**: Always write `\text{\lr{\AA}}` or `\angstrom`, never bare `\text{\AA}` (causes `Missing character: U+030A` because `\text` inherits the Persian font).
  - **Avoid bare inline parenthetical equations**: Expressions like `($n(T)=n(0)$)` or `($g(\mathcal{E}<0)=0$)` in Persian prose often flip parentheses or misplace periods. Either integrate them naturally in Persian prose (`یعنی $n(T)=n(0)$`) or wrap the entire parenthetical expression in `\lr{($n(T)=n(0)$)}`.
  - **Section headings & TOC (`hyperref`)**: Wrap parenthetical math/Latin formulas in `\section` or `\subsection` using `\texorpdfstring`, e.g. `\section{چگالی حالت‌ها \texorpdfstring{\lr{($g(\mathcal{E})$)}}{(g(E))}}`, so TOC entries and PDF bookmarks have matching parentheses.
  - **Titlepage fields (`main.tex`)**: Wrap pure ASCII/Latin fields (`\lr{PHYS-501}`, `\lr{1405-1}`) in `\lr{...}`, but leave Persian fields containing parentheses (e.g. `نیم‌سال ۱۴۰۵-۱ (پاییز ۲۰۲۶)`) unwrapped.
- **English mode (`\notesfafalse`)**: Same textbook narrative structure, deep derivations, Personal Relevance opener, and provenance rules in ordinary academic English.

## 4. Math, derivations & tables

- Number only equations that are referenced or are key results (`equation`/`align`; starred `*` when unreferenced).
- Derivations are step-by-step with the physical or mathematical *reason* attached:
```latex
\begin{align}
  H\psi &= E\psi && \fa{معادلهٔ شرودینگر} \\
  \psi_{\vb{k}}(\vb{r}) &= \ee^{\ii\vb{k}\cdot\vb{r}}\, u_{\vb{k}}(\vb{r}) && \fa{شکل بلوخ}
\end{align}
```
- **Split wide equations**: Break long display equations into multi-line `align` blocks so equation numbers `(N.M)` never collide with formulas or prose.
- **Tables**: In multi-column quantitative tables, put variable names/symbols in Header Row 1 and units in a dedicated Header Row 2 below them rather than cramming symbols and units into narrow cells. Keep cell wording concise so narrow columns do not stretch awkwardly.
- Fix conventions once (`course.yaml`: units, Fourier convention, time dependence) and apply everywhere; map differing textbook conventions explicitly inside a `supplement`.
- State dimensions/units for every new physical formula at first appearance.

## 5. Figures & TikZ BiDi safety

- Redraw board diagrams cleanly in TikZ (`blue!85!black`, `red!80!black`, `teal`, lines `1.1--1.6pt`, dashed gray guides).
- **TikZ BiDi labels**: Never place mixed Persian + math/Latin text on a single line inside a TikZ node (`\rl{دایرهٔ فرمی ($2\text{D}$)}` scrambles word and parenthesis order). Split into a two-line centered node:
  ```latex
  \node[align=center] at (-1.8,-1.8) {\rl{دایرهٔ فرمی} \\ \lr{($2\text{D}$)}};
  ```
- **Overlap prevention**: Add `fill=white, inner sep=1.5pt` to annotations sitting near curves or dashed guides, and leave clear vertical/horizontal margin around axes.
- **Physics arrow sanity check**: Double-check every vector arrow's direction and sign against the text and equations (e.g., thermal diffusion velocity vs. induced electric field $\mathbf{E}$ in Seebeck/Hall schematics).
- Every figure carries a caption stating what it shows and the key takeaway, labelled `fig:chNN-name`. Board photos may be included from `figures/` with `\includegraphics` (credited in the caption). Never copy textbook figures; cite them instead.

## 6. Labels and references

- Labels: `def:chNN-name`, `thm:chNN-name`, `eq:chNN-name`, `fig:chNN-name`, `tab:chNN-name`, `sec:chNN-name`. Lowercase ASCII with hyphens.
- Refer exclusively via `\ref`/`\eqref`; never hardcode numbers. Cross-chapter references are encouraged.

## 7. Rigor & visual QA checklist (run before reporting)

1. Every symbol defined at or before first use and recorded in `notation.md`.
2. Every theorem states hypotheses and has a proof, `supplement` proof, or explicit `\srcref`.
3. Every added statement sits inside a colored box with a source or `derived` label. No unboxed additions.
4. Dimensions/units checked for every new formula; at least one limiting case or sanity check per major result.
5. Conventions consistent with `course.yaml`; differences from references documented in `discrepancy` or mapped in `supplement`.
6. No unresolved `[?]` from `notes.md`: every uncertainty is either resolved or flagged in a `todobox`.
7. Personal Relevance prose opener present for each session; main text uses connected textbook prose (bullets only in summaries/tables).
8. Build cleanly with `python3 <SKILL_DIR>/scripts/build.py --render <pages>`:
   - `0` errors, **`0 Missing character:` warnings**, `0 Undefined control sequence`, `0` undefined references/labels.
   - Visually inspect rendered PNGs (`build/preview/`) for TOC headings, TikZ labels/arrows, tables, parenthetical inline math, and equation tags.
9. `glossary.md`, `notation.md`, `coverage.md`, and `weeks/week-NN/review.md` updated.
