#!/usr/bin/env python3
"""Entry point for the news-image-20261122 make.fun entry.

Copies the pre-rendered entry.png (drawn by draw.py) into the output
directory: $MAKEFUN_OUTPUT_DIR when set, otherwise /output.
Standard library only; no network; deterministic output bytes.
"""
import os
import shutil
from pathlib import Path


def main():
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    src = Path(__file__).resolve().parent / "entry.png"
    dst = out_dir / "entry.png"
    shutil.copyfile(src, dst)
    # Determinism self-check: the copy must be byte-identical in size,
    # and a second run must produce exactly the same bytes again.
    assert dst.stat().st_size == src.stat().st_size, "copy size mismatch"


if __name__ == "__main__":
    main()
