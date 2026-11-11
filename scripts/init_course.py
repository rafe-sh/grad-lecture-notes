#!/usr/bin/env python3
"""Scaffold a new course notebook repository.

Usage:
  python3 init_course.py --dir . --lang fa --title "فیزیک حالت جامد پیشرفته" --semester "نیم‌سال ۱۴۰۵-۱ (پاییز ۲۰۲۶)"
"""
from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"
PERSIAN_ARABIC_RE = re.compile(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]")

FA_LTR_CONVENTION = (
    "  ltr: 'STANDING RULE: wrap every Latin run, number, date, range, file path, URL, "
    "or hybrid math-Latin token inside Persian prose in \\\\lr{...} (alias \\\\en{...}), "
    "with attached punctuation inside \\\\lr{...}. Use \\\\text{\\\\lr{\\\\AA}} or \\\\angstrom "
    "(never bare \\\\text{\\\\AA}). Inspect build/main.log and rendered pages after every build.'\n"
)

YAML_TEMPLATE = """course:
  title: "{title}"
  code: "{code}"
  semester: "{semester}"
  author: "{author}"
language:
  mode: {lang}                 # fa = Persian prose + English terms | en = English only
  terms: parenthetical         # first use per chapter: Persian (English)
organization: topic            # topic | book
references:
  primary: ""                  # key of the main textbook below
  books: {{}}                  # e.g. kittel: {{title: "...", author: "...", edition: "", dir: refs}}
conventions:
  units: SI
  fourier: ""
  time_dependence: ""
{ltr_line}  notes: ""
workflow:
  checkpoint: first_week_then_auto
  enrichment: free
  prose_style: textbook        # textbook (connected prose paragraphs) | concise
  personal_relevance: true     # brief "Why this matters to me" prose intro per session
  exercises: if_assigned
  citations: only_verified
style_log: []
"""


def format_title_field(value: str, lang: str) -> str:
    """Wrap pure-Latin/ASCII titlepage metadata in \\lr{} in Persian mode.

    Strings containing Persian/Arabic letters remain unwrapped so RTL parentheses
    and mixed words render in natural order.
    """
    stripped = value.strip()
    if not stripped or lang != "fa":
        return stripped
    if PERSIAN_ARABIC_RE.search(stripped):
        return stripped
    if stripped.startswith(("\\lr{", "\\en{")):
        return stripped
    return f"\\lr{{{stripped}}}"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dir", default=".", help="target course directory (default: cwd)")
    ap.add_argument("--lang", choices=["fa", "en"], default="fa", help="notebook language mode")
    ap.add_argument("--title", default="Course Notes", help="course title")
    ap.add_argument("--code", default="", help="course code (e.g. PHYS-501)")
    ap.add_argument("--semester", default="", help="semester label")
    ap.add_argument("--author", default="", help="author / note-taker name")
    ap.add_argument("--force", action="store_true", help="overwrite existing files")
    a = ap.parse_args()

    root = Path(a.dir).resolve()
    root.mkdir(parents=True, exist_ok=True)

    def put(name: str, text: str | None = None, src: Path | None = None) -> None:
        dst = root / name
        if dst.exists() and not a.force:
            print(f"  skip (exists): {name}")
            return
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src is not None:
            shutil.copyfile(src, dst)
        else:
            assert text is not None
            dst.write_text(text, encoding="utf-8")
        print(f"  wrote: {name}")

    for d in ["chapters", "weeks", "refs", "figures"]:
        (root / d).mkdir(exist_ok=True)

    main_txt = (ASSETS / "main.tex").read_text(encoding="utf-8")
    replacements = {
        "__FA_FLAG__": "true" if a.lang == "fa" else "false",
        "__TITLE__": format_title_field(a.title, a.lang),
        "__CODE__": format_title_field(a.code, a.lang),
        "__SEMESTER__": format_title_field(a.semester, a.lang),
        "__AUTHOR__": format_title_field(a.author, a.lang),
    }
    for k, v in replacements.items():
        main_txt = main_txt.replace(k, v)
    main_txt = main_txt.replace(
        "% CHAPTERS-BEGIN\n",
        "% CHAPTERS-BEGIN\n\\include{chapters/ch00-starter}\n",
        1,
    )

    put("main.tex", main_txt)
    put("preamble.tex", src=ASSETS / "preamble.tex")
    put("macros.tex", src=ASSETS / "macros.tex")
    put("notation.md", src=ASSETS / "notation.md")
    put("glossary.md", src=ASSETS / "glossary.md")
    put("coverage.md", src=ASSETS / "coverage.md")
    put(
        "refs/index.md",
        "# Reference index\n\nOne section per book: chapter -> split PDF, pages, sections, key equations.\n",
    )
    put(
        "course.yaml",
        YAML_TEMPLATE.format(
            title=a.title.replace('"', '\\"'),
            code=a.code.replace('"', '\\"'),
            semester=a.semester.replace('"', '\\"'),
            author=a.author.replace('"', '\\"'),
            lang=a.lang,
            ltr_line=FA_LTR_CONVENTION if a.lang == "fa" else "",
        ),
    )
    put(".gitignore", src=ASSETS / "gitignore.txt")
    put("chapters/ch00-starter.tex", src=ASSETS / f"starter-chapter.{a.lang}.tex")

    rules_src = ASSETS / f"AGENTS.{a.lang}.md"
    for rule_name in ("AGENTS.md", "GEMINI.md", "CLAUDE.md"):
        put(rule_name, src=rules_src)

    skill_scripts = Path(__file__).resolve().parent
    print(
        "\nDone. Next:\n"
        f"  python3 \"{skill_scripts / 'check_env.py'}\"\n"
        f"  python3 \"{skill_scripts / 'build.py'}\" --dir \"{root}\" --render all\n"
        "Then verify the PDF/PNG previews and delete chapters/ch00-starter.tex (and its \\include line)."
    )


if __name__ == "__main__":
    main()
