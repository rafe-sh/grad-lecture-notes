#!/usr/bin/env python3
"""Check the LaTeX and helper toolchain for grad-lecture-notes.

Usage:
  python3 check_env.py
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

from _texutil import find_tool

PACKAGES = [
    "fontspec.sty",
    "xepersian.sty",
    "bidi.sty",
    "tcolorbox.sty",
    "tikz.sty",
    "pgf.sty",
    "mathtools.sty",
    "amsthm.sty",
    "titlesec.sty",
    "fancyhdr.sty",
    "geometry.sty",
    "hyperref.sty",
    "booktabs.sty",
    "xcolor.sty",
]
FONTS = [
    "IRNazanin",
    "IRLotus",
    "IRTitr",
    "Vazirmatn",
    "Times New Roman",
    "TeX Gyre Termes",
    "Latin Modern Roman",
]


def run_cmd(cmd: list[str]) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, errors="replace", timeout=180)
    except Exception:
        return None


def main() -> None:
    ok = True
    xelatex = find_tool("xelatex")
    print("xelatex:", xelatex or "NOT FOUND")
    if not xelatex:
        sys.exit("Install a TeX distribution (MacTeX, TeX Live, TinyTeX, or MiKTeX) and ensure xelatex is available.")

    ver = run_cmd([xelatex, "--version"])
    first = ver.stdout.splitlines()[0] if ver and ver.stdout else "?"
    print("version:", first)
    dist = "MiKTeX" if ver and "MiKTeX" in ver.stdout else "TeX Live-family"
    print("distribution:", dist)

    kpsewhich = find_tool("kpsewhich")
    if kpsewhich:
        print("\nPackages:")
        for pkg in PACKAGES:
            res = run_cmd([kpsewhich, pkg])
            found = bool(res and res.stdout.strip())
            print(f"  {'ok     ' if found else 'MISSING'} {pkg}")
            ok &= found or dist == "MiKTeX"
        if dist == "MiKTeX":
            print("  (MiKTeX can install missing packages on first use if 'install on-the-fly' is enabled.)")
        else:
            print("  Fix missing ones with: tlmgr install <package>   (tlmgr search --global --file <name>.sty)")
    else:
        print("\nkpsewhich not found; skipping package check (a build will reveal missing packages).")

    with tempfile.TemporaryDirectory() as tmp:
        probe = Path(tmp) / "font_probe.tex"
        checks = "".join(f"\\chk{{{font}}}" for font in FONTS)
        probe.write_text(
            "\\documentclass{article}\\usepackage{fontspec}\n"
            "\\newcommand\\chk[1]{\\IfFontExistsTF{#1}{\\typeout{FONT-OK: #1}}{\\typeout{FONT-MISSING: #1}}}\n"
            f"{checks}\n\\begin{{document}}x\\end{{document}}\n",
            encoding="utf-8",
        )
        res = run_cmd([xelatex, "-interaction=nonstopmode", f"-output-directory={tmp}", str(probe)])
        print("\nFonts (as XeLaTeX sees them):")
        if res:
            out = res.stdout
            for font in FONTS:
                status = "ok     " if f"FONT-OK: {font}" in out else "MISSING"
                print(f"  {status} {font}")
            print(
                "  Fallback order in preamble.tex: IRNazanin -> Vazirmatn -> DejaVu Serif (body), "
                "IRLotus -> Vazirmatn -> DejaVu Sans (titles)."
            )
        else:
            print("  could not run font probe")
            ok = False

    print("\nOptional PDF / visual-QA helpers:")
    try:
        import pypdf  # noqa: F401
        print("  ok      pypdf (needed for split_pdf.py)")
    except ImportError:
        print("  missing pypdf (pip install pypdf) -- needed only for splitting textbook PDFs")

    has_fitz = False
    try:
        import fitz  # noqa: F401
        has_fitz = True
        print("  ok      pymupdf/fitz (used by build.py --render)")
    except ImportError:
        print("  missing pymupdf/fitz (pip install pymupdf) -- optional for build.py --render")

    pdftoppm = find_tool("pdftoppm")
    print(f"  {'ok     ' if pdftoppm else 'missing'} pdftoppm ({pdftoppm or 'install poppler'}) -- fallback for build.py --render")
    if not has_fitz and not pdftoppm:
        print("  Note: install either pymupdf or poppler (pdftoppm) to use build.py --render for visual QA.")

    print("\nResult:", "ready" if ok else "fix the MISSING items above, then run build.py")
    if not ok:
        sys.exit(1)


if __name__ == "__main__":
    main()
