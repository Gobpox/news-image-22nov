#!/usr/bin/env python3
"""Deliver the finished page for the 22 November 2026 news entry.

The artwork itself is rendered ahead of time by draw.py and committed
beside this file as entry.png. Running this program publishes those
exact bytes as the entry image: the destination folder comes from the
MAKEFUN_OUTPUT_DIR environment variable when the harness sets one,
and falls back to /output otherwise. Nothing here touches the
network, and repeated runs always emit identical bytes.
"""
import os
from pathlib import Path


def deliver_page():
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    page_bytes = (Path(__file__).resolve().parent / "entry.png").read_bytes()
    target_file = target_dir / "entry.png"
    target_file.write_bytes(page_bytes)
    # Guard against a truncated write: what landed must be the page.
    if target_file.stat().st_size != len(page_bytes):
        raise SystemExit("delivered page size mismatch")


if __name__ == "__main__":
    deliver_page()
