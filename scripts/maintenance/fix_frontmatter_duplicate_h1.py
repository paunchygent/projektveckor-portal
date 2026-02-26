#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
TITLE_RE = re.compile(r'^title:\s*["\']?(.+?)["\']?\s*$', re.MULTILINE)
FIRST_H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)

DEFAULT_IGNORED_DIRS = {
    ".git",
    ".venv",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    "node_modules",
    "build",
    "output",
    "frontend",
}


def _iter_markdown_files(root: Path) -> list[Path]:
    candidates = list(root.rglob("*.md")) + list(root.rglob("*.mdc"))
    return [p for p in candidates if not any(part in DEFAULT_IGNORED_DIRS for part in p.parts)]


def _split_frontmatter(text: str) -> tuple[str | None, str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None, "", text

    frontmatter_body = match.group(1)
    title_match = TITLE_RE.search(frontmatter_body)
    title = title_match.group(1).strip() if title_match else None
    return title, match.group(0), text[match.end() :]


def _remove_duplicate_h1(text: str) -> tuple[str, bool]:
    title, frontmatter_block, after = _split_frontmatter(text)
    if not title:
        return text, False

    h1_match = FIRST_H1_RE.search(after)
    if not h1_match:
        return text, False

    h1_text = h1_match.group(1).strip()
    if title.strip().lower() != h1_text.lower():
        return text, False

    start = h1_match.start()
    end = h1_match.end()
    while end < len(after) and after[end] == "\n":
        end += 1

    new_after = (after[:start] + after[end:]).lstrip("\n")
    return frontmatter_block + new_after, True


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Remove duplicate leading H1 when YAML frontmatter contains the same title."
    )
    parser.add_argument("--root", type=Path, default=Path("."), help="Repo root to scan (default: .)")
    parser.add_argument("--apply", action="store_true", help="Write changes (default: dry-run).")
    args = parser.parse_args()

    root: Path = args.root
    md_files = _iter_markdown_files(root)

    modified: list[Path] = []
    for path in md_files:
        original = path.read_text(encoding="utf-8")
        updated, changed = _remove_duplicate_h1(original)
        if not changed:
            continue
        modified.append(path)
        if args.apply:
            path.write_text(updated, encoding="utf-8")

    if not args.apply:
        for path in modified:
            print(f"[DRY RUN] Would modify: {path.as_posix()}")
    else:
        for path in modified:
            print(f"✓ Modified: {path.as_posix()}")

    if modified:
        return 0 if args.apply else 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
