#!/usr/bin/env python3
"""Shared executable discovery helpers for grad-lecture-notes scripts."""
from __future__ import annotations

from pathlib import Path
import shutil
import sys

EXTRA_BIN_DIRS = [
    "/Library/TeX/texbin",
    "/usr/texbin",
    "/opt/homebrew/bin",
    "/usr/local/bin",
]


def find_tool(name: str) -> str | None:
    """Locate an executable on PATH or in standard MacTeX/TeX Live locations."""
    found = shutil.which(name)
    if found:
        return found

    candidates = [Path(d) / name for d in EXTRA_BIN_DIRS]
    if sys.platform == "darwin":
        tl_root = Path("/usr/local/texlive")
        if tl_root.exists():
            candidates.extend(sorted(tl_root.glob(f"*/bin/*/{name}"), reverse=True))
    elif sys.platform.startswith("win"):
        for base in (Path("C:/texlive"), Path("C:/Program Files/MiKTeX/miktex/bin/x64")):
            if base.exists():
                candidates.extend(base.glob(f"**/bin/**/{name}.exe"))
                candidates.append(base / f"{name}.exe")

    for path in candidates:
        if path.is_file():
            return str(path)
    return None
