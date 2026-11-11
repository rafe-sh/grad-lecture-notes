# Ingesting Raw Material and Aligning It

Contents: 1 Inputs · 2 Board notes · 3 Transcripts · 4 Merging · 5 Textbook alignment · 6 Splitting PDFs

## 1. Inputs per week

Put everything in `weeks/week-NN/raw/` (images, PDFs, `.md` OCR output, transcript text). Expect any mix of:
- handwritten board notes as images or PDF (primary source for *what* was written)
- the same lecture-note pages as markdown produced by an OCR/vision tool (e.g., **Google AI Studio** as an optional suggestion—not obligatory): treat as a draft transcription, not as ground truth
- voice-recording transcripts (e.g., **NotebookLM** voice transcription as an optional suggestion—not obligatory): primary source for *why* and for how steps connect
- the user's occasional typed remarks

If a user asks how to prepare raw `.md` inputs from audio or handwritten pages, you may suggest **NotebookLM** for voice transcription and **Google AI Studio** for page-to-markdown OCR strictly as optional conveniences—never require them. If one of the sessions has no board notes or no voice transcript (for example, an absent session with board photos/OCR only), continue with the available material, note the gap explicitly in `plan.md` and `review.md`, and reconstruct missing steps rigorously from the verified textbook sections in `refs/` while marking textbook-sourced proofs and derivations in `supplement` boxes (never inventing spoken remarks). If assigned homework/exercise problems appear in raw notes or transcripts, follow `workflow.exercises` in `course.yaml` (e.g. placing worked solutions in `example` + `supplement` boxes or a dedicated end-of-chapter Exercises section).

## 2. Board notes

- Read images/PDF pages yourself when you can view them; if OCR markdown also exists, compare the two and trust the image on conflicts.
- Transcribe in the order written, keeping the lecturer's structure. Keep equations in LaTeX.
- Mark uncertain items inline with `[?]` and a short guess in brackets, e.g. `E_k = ħ²k²/2m [? factor 2 or 2m]`. Typical trouble: k vs κ, ν vs v, ħ vs h, ± signs, primes, subscripts, crossed-out lines (record as "struck out").
- Never silently complete an unreadable expression. If a derivation is only consistent with one reading, say that in `[? ... consistent with ...]`.

## 3. Transcripts

Voice-to-text on physics lectures has predictable failure modes. Check for:
- mangled names and terms (Bloch -> "block", Brillouin -> "breeloon", Wannier, Fermi, Kohn-Sham, Bravais)
- symbols read aloud and mis-heard (k vs "kay" vs "K", "h-bar", "omega" vs "w")
- numbers and orders of magnitude
- Persian/English code-switching: English terms rendered in Persian script, or Persian words rendered phonetically in Latin letters

Maintain the second half of `glossary.md` ("Known mis-transcriptions": heard form -> intended term). Consult it before every ingest and extend it after.
Remove chatter, logistics, repeated starts, off-topic stories, and exam/assignment announcements (list the latter separately in `review.md` if useful to the user, but not in the notes).

## 4. Merging into notes.md

Procedure:
1. Build a skeleton from the board notes (headings, definitions, equations, figures in order).
2. Walk the transcript in parallel and attach, under each board item, the explanation that connects it to the previous one: *why this step, what is being assumed, what the lecturer emphasised*.
3. Anything said but not written (intuition, caveats, corrections) goes under the nearest board item, labelled `said:`.
4. Anything written but never explained goes as is, labelled `board only:`; this often marks a place for a `supplement`.
5. Corrections the lecturer made verbally ("I wrote the wrong sign") are applied and noted: `corrected in lecture: ...`.
6. Record session boundaries (date, L#) so `\lecturetag` can be placed correctly.

`notes.md` is an intermediate artifact for the user to inspect. It is not part of the final notebook.

## 5. Textbook alignment

- `refs/index.md` maps every book chapter to its split PDF and lists section titles, page ranges, and key equation numbers. Create it when you split the book (section 6); extend it when you read a chapter in detail.
- For each topic of the week, open only the relevant chapter PDF. Extract text with the PDF-reading tools you have (page images for formula-heavy pages; plain text extraction often garbles equations).
- Compare: definitions, notation, assumptions, final formulas, factors of 2π and signs. Record equation numbers you actually saw.
- If several books are listed in `course.yaml`, prefer the primary textbook for citations, and use the others for supplements and discrepancy checks.
- If the course has no usable PDF, say so in the report; cite nothing you cannot see, and lean on `derived` supplements plus `todobox` for unverified facts.

## 6. Splitting the textbook

Whole-book PDFs waste context and invite drift. Split once per book:

```
python3 <SKILL_DIR>/scripts/split_pdf.py book.pdf --outline                       # show bookmarks and page numbers
python3 <SKILL_DIR>/scripts/split_pdf.py book.pdf --out refs --auto               # one file per top-level chapter
python3 <SKILL_DIR>/scripts/split_pdf.py book.pdf --out refs --chapters "08:bloch-theorem:141-168" "09:semiclassical:169-210"
```
Naming: `refs/<bookkey>-ch08-bloch-theorem.pdf`. Page numbers are PDF page indices, not printed numbers; check one chapter's first page before trusting a range. Then write `refs/index.md`:

```
## Kittel (kittel) -- Introduction to Solid State Physics
| ch | title | file | pdf pages | sections | key equations |
```
Fill sections and key equations lazily: when you first read a chapter, record what you learned so the next week does not reread it.
Needs `pypdf` (`pip install pypdf`); if unavailable, use `qpdf in.pdf --pages . 141-168 -- out.pdf` or ask the user to cut chapters manually.
