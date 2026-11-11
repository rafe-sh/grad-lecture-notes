#!/usr/bin/env python3
"""Split a textbook PDF into per-chapter PDFs so the agent loads only what a week needs.
  python3 split_pdf.py book.pdf --outline
  python3 split_pdf.py book.pdf --out refs --auto [--key kittel]
  python3 split_pdf.py book.pdf --out refs --key kittel --chapters "08:bloch-theorem:141-168" ...
Page numbers are 1-based PDF page indices (not the printed numbers). Requires: pip install pypdf
"""
import argparse, re, sys
from pathlib import Path

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    sys.exit("pypdf missing: pip install pypdf  (or use: qpdf in.pdf --pages . 141-168 -- out.pdf)")

def slug(s):
    s = re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-").lower()
    return s[:50] or "chapter"

def flatten(reader, items, level=0, acc=None):
    acc = [] if acc is None else acc
    for it in items:
        if isinstance(it, list):
            flatten(reader, it, level + 1, acc)
        else:
            try:
                acc.append((level, it.title, reader.get_destination_page_number(it) + 1))
            except Exception:
                pass
    return acc

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf")
    ap.add_argument("--outline", action="store_true")
    ap.add_argument("--auto", action="store_true", help="split at top-level bookmarks")
    ap.add_argument("--chapters", nargs="+", help='"NN:slug:first-last"')
    ap.add_argument("--out", default="refs")
    ap.add_argument("--key", default=None, help="file prefix, default = pdf name")
    a = ap.parse_args()

    reader = PdfReader(a.pdf)
    n = len(reader.pages)
    key = a.key or slug(Path(a.pdf).stem)
    marks = flatten(reader, reader.outline)

    if a.outline:
        print(f"{a.pdf}: {n} pages, {len(marks)} bookmarks")
        for lvl, t, p in marks:
            if lvl <= 1:
                print(f"{'  ' * lvl}{p:>5}  {t}")
        return

    jobs = []
    if a.chapters:
        for c in a.chapters:
            num, name, rng = c.split(":")
            lo, hi = (int(x) for x in rng.split("-"))
            jobs.append((num, name, lo, hi))
    elif a.auto:
        tops = [(t, p) for lvl, t, p in marks if lvl == 0]
        for i, (t, p) in enumerate(tops):
            hi = (tops[i + 1][1] - 1) if i + 1 < len(tops) else n
            jobs.append((f"{i + 1:02d}", slug(t), p, max(p, hi)))
    else:
        sys.exit("Choose --outline, --auto or --chapters.")

    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    for num, name, lo, hi in jobs:
        w = PdfWriter()
        for pg in range(lo - 1, min(hi, n)):
            w.add_page(reader.pages[pg])
        f = out / f"{key}-ch{num}-{name}.pdf"
        with open(f, "wb") as fh:
            w.write(fh)
        print(f"wrote {f}  (pages {lo}-{hi})")
    print("\nNext: record these in refs/index.md and check each chapter's first page.")

if __name__ == "__main__":
    main()
