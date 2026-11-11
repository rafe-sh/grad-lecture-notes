#!/usr/bin/env python3
"""Build the lecture notebook with XeLaTeX, verify the log, and optionally render pages to PNG.

Usage (run from the course repo root, or pass --dir):
  python3 build.py                              # full build (multi-pass until settled)
  python3 build.py --only chapters/ch03-x       # fast build of one chapter
  python3 build.py --render all                 # build and render all PDF pages to build/preview/
  python3 build.py --render 1 4 17-20           # build and render specific pages for visual QA
  python3 build.py --main other.tex             # build a different root file

Output goes to build/ (PDF: build/main.pdf). Exit code 0 = clean build.
Cross-platform, standard library only for compilation (pymupdf or pdftoppm needed only for --render).
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

from _texutil import find_tool

MAX_PASSES = 4
RERUN_PAT = re.compile(r"Rerun to get|Label\(s\) may have changed|Please \(re\)run")


def run_pass(xelatex: str, root: Path, outdir: str, jobname: str, source_arg: str) -> subprocess.CompletedProcess[str]:
    cmd = [
        xelatex,
        "-interaction=nonstopmode",
        "-halt-on-error",
        "-file-line-error",
        f"-output-directory={outdir}",
        f"-jobname={jobname}",
        source_arg,
    ]
    return subprocess.run(cmd, cwd=root, capture_output=True, text=True, errors="replace")


def parse_log(text: str, check_rerun: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    lines = text.splitlines()

    for i, ln in enumerate(lines):
        m = re.match(r"^(.*?):(\d+): (.*)$", ln)
        if m and not ln.startswith("LaTeX"):
            ctx = " | ".join(l.strip() for l in lines[i + 1 : i + 3] if l.strip())
            errors.append(f"{m.group(1)}:{m.group(2)}: {m.group(3)}" + (f"  [{ctx}]" if ctx else ""))
        elif ln.startswith("!"):
            ctx = " | ".join(l.strip() for l in lines[i + 1 : i + 3] if l.strip())
            errors.append(f"{ln}  [{ctx}]")
        elif ln.startswith("Missing character:"):
            errors.append(ln.strip())
        elif re.match(r"^Package (?:bidi|xepersian) Error:", ln):
            errors.append(ln.strip())
        elif "Undefined control sequence" in ln and not any("Undefined control sequence" in e for e in errors[-2:]):
            errors.append(ln.strip())

        mo = re.match(r"Overfull \\hbox \(([\d.]+)pt too wide\)(.*)", ln)
        if mo and float(mo.group(1)) > 10:
            warnings.append(f"Overfull box {mo.group(1)}pt{mo.group(2)}")
        if "Warning: Reference" in ln or "Warning: Citation" in ln:
            warnings.append(ln.strip())
        if re.search(r"font .* cannot be found|Font .* not found|not loadable", ln, re.I):
            warnings.append("FONT: " + ln.strip())
        if check_rerun and RERUN_PAT.search(ln):
            warnings.append("References did not settle: " + ln.strip())

    return errors, warnings


def hints(errors: list[str], text: str) -> list[str]:
    out: list[str] = []
    for m in set(re.findall(r"File `([^']+\.(?:sty|cls|def|tex))' not found", text)):
        out.append(
            f"Missing file {m}. TeX Live/TinyTeX: `tlmgr search --global --file {m}` then `tlmgr install <package>`. "
            "MiKTeX: install the package in MiKTeX Console or enable on-the-fly installation."
        )
    if re.search(r"Package fontspec Error: The font|cannot be found", text):
        out.append(
            "A configured font is missing. Run check_env.py; preamble.tex falls back automatically for known Persian "
            "fonts, while custom fonts must be installed."
        )
    if any(e.startswith("Missing character:") for e in errors):
        out.append(
            "Missing character detected (e.g. U+030A from bare \\text{\\AA} in a Persian font). "
            "Wrap Latin symbols, units, and runs in \\lr{...} (use \\text{\\lr{\\AA}} or \\angstrom)."
        )
    return out


def parse_page_spec(specs: list[str], total_pages: int) -> list[int]:
    """Parse 1-based page tokens ('all', '3', '12-15') into a deduplicated ordered list."""
    if any(s.lower() == "all" for s in specs):
        return list(range(1, total_pages + 1))

    pages: list[int] = []
    seen: set[int] = set()
    for spec in specs:
        for part in spec.split(","):
            token = part.strip()
            if not token:
                continue
            if "-" in token:
                lo_s, hi_s = token.split("-", 1)
                lo, hi = int(lo_s), int(hi_s)
                if lo < 1 or hi > total_pages or lo > hi:
                    raise ValueError(f"Page range '{token}' out of bounds (1..{total_pages}).")
                rng = range(lo, hi + 1)
            else:
                pg = int(token)
                if pg < 1 or pg > total_pages:
                    raise ValueError(f"Page {pg} out of bounds (1..{total_pages}).")
                rng = range(pg, pg + 1)
            for pg in rng:
                if pg not in seen:
                    seen.add(pg)
                    pages.append(pg)
    return pages


def render_pages(pdf_path: Path, specs: list[str], preview_dir: Path, dpi: int) -> list[Path]:
    """Render selected PDF pages to PNGs using PyMuPDF (preferred) or pdftoppm."""
    preview_dir.mkdir(parents=True, exist_ok=True)
    rendered: list[Path] = []

    try:
        import fitz  # type: ignore

        with fitz.open(pdf_path) as doc:
            pages = parse_page_spec(specs, len(doc))
            for pg in pages:
                pix = doc[pg - 1].get_pixmap(dpi=dpi)
                out_png = preview_dir / f"page-{pg:03d}.png"
                pix.save(out_png)
                rendered.append(out_png)
        return rendered
    except ImportError:
        pass

    pdftoppm = find_tool("pdftoppm")
    if not pdftoppm:
        sys.exit(
            "[build] --render requested, but neither PyMuPDF (`pip install pymupdf`) nor `pdftoppm` (poppler) was found."
        )

    # Determine page count via pypdf if installed, or pdfinfo
    total_pages: int | None = None
    try:
        from pypdf import PdfReader

        total_pages = len(PdfReader(str(pdf_path)).pages)
    except Exception:
        pdfinfo = find_tool("pdfinfo")
        if pdfinfo:
            res = subprocess.run([pdfinfo, str(pdf_path)], capture_output=True, text=True)
            m = re.search(r"^Pages:\s+(\d+)", res.stdout, re.M)
            if m:
                total_pages = int(m.group(1))

    if total_pages is None:
        sys.exit("[build] Cannot determine PDF page count for pdftoppm; install `pymupdf` or `pypdf`.")

    pages = parse_page_spec(specs, total_pages)
    for pg in pages:
        stem = preview_dir / f"page-{pg:03d}"
        res = subprocess.run(
            [pdftoppm, "-png", "-r", str(dpi), "-f", str(pg), "-l", str(pg), "-singlefile", str(pdf_path), str(stem)],
            capture_output=True,
            text=True,
        )
        if res.returncode != 0:
            sys.exit(f"[build] pdftoppm failed on page {pg}: {res.stderr.strip()}")
        rendered.append(Path(f"{stem}.png"))
    return rendered


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default=".", help="course repo root (default: cwd)")
    ap.add_argument("--main", default="main.tex", help="root TeX file (default: main.tex)")
    ap.add_argument("--only", nargs="+", help="chapter paths without .tex, e.g. chapters/ch03-bloch")
    ap.add_argument("--outdir", default="build", help="build output directory (default: build)")
    ap.add_argument("--render", nargs="+", metavar="PAGE", help="render PDF pages to PNGs (e.g. all or 1 4 17-20)")
    ap.add_argument("--dpi", type=int, default=180, help="PNG DPI when --render is used (default: 180)")
    ap.add_argument("--preview-dir", default=None, help="PNG preview output directory (default: <outdir>/preview)")
    a = ap.parse_args()

    root = Path(a.dir).resolve()
    main_tex = root / a.main
    if not main_tex.exists():
        sys.exit(f"{main_tex} not found. Run from the course repo root or pass --dir.")

    xelatex = find_tool("xelatex")
    if xelatex is None:
        sys.exit("xelatex not found on PATH or in /Library/TeX/texbin. Install MacTeX/TeX Live/TinyTeX/MiKTeX.")

    outdir = root / a.outdir
    outdir.mkdir(exist_ok=True)
    chapters_dir = root / "chapters"
    if chapters_dir.exists():
        for d in chapters_dir.glob("**/"):  # \include writes aux files into outdir/chapters
            (outdir / d.relative_to(root)).mkdir(parents=True, exist_ok=True)

    jobname = Path(a.main).stem
    if a.only:
        inc = ",".join(p.replace("\\", "/")[:-4] if p.endswith(".tex") else p.replace("\\", "/") for p in a.only)
        source = f"\\includeonly{{{inc}}}\\input{{{jobname}}}"
        print(f"[build] partial build: {inc}")
    else:
        source = Path(a.main).name

    text = ""
    settled = False
    for pass_num in range(1, MAX_PASSES + 1):
        res = run_pass(xelatex, root, a.outdir, jobname, source)
        logf = outdir / f"{jobname}.log"
        text = logf.read_text(errors="replace") if logf.exists() else res.stdout
        print(f"[build] pass {pass_num}: return code {res.returncode}")
        if res.returncode != 0:
            break
        if not RERUN_PAT.search(text):
            settled = True
            break

    errors, warnings = parse_log(text, check_rerun=not settled)
    pdf = outdir / f"{jobname}.pdf"
    pages_match = re.search(r"Output written on .*\((\d+) page", text)

    if errors:
        print("\n[build] ERRORS (fix these first, top one is usually the cause):")
        for e in errors[:20]:
            print("  -", e)
        for h in hints(errors, text):
            print("  hint:", h)
        sys.exit(1)

    if warnings:
        print("\n[build] warnings:")
        for w in sorted(set(warnings))[:25]:
            print("  -", w)

    print(f"\n[build] OK: {pdf}" + (f" ({pages_match.group(1)} pages)" if pages_match else ""))

    if a.render:
        if not pdf.exists():
            sys.exit(f"[build] Cannot render; PDF missing at {pdf}")
        preview_dir = Path(a.preview_dir) if a.preview_dir else (outdir / "preview")
        if not preview_dir.is_absolute():
            preview_dir = root / preview_dir
        try:
            rendered = render_pages(pdf, a.render, preview_dir, a.dpi)
        except ValueError as exc:
            sys.exit(f"[build] Invalid --render page spec: {exc}")
        print(f"[render] wrote {len(rendered)} PNG(s) in {preview_dir}:")
        for png in rendered:
            print("  -", png)


if __name__ == "__main__":
    main()
