#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

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

FENCE_START_RE = re.compile(r"^\s*(`{3,}|~{3,})")

# Avoid converting escaped placeholders like "\__\_\_\__" used for fill-in lines.
STRONG_UNDERSCORE_RE = re.compile(r"(?<![\\\w])__(?=\S)(.+?)(?<=\S)(?<!\\)__(?!\w)")


@dataclass(frozen=True)
class NormalizeResult:
    updated: str
    changed: bool


def _iter_markdown_files(root: Path) -> list[Path]:
    candidates = list(root.rglob("*.md")) + list(root.rglob("*.mdc"))
    return [p for p in candidates if not any(part in DEFAULT_IGNORED_DIRS for part in p.parts)]


def _split_by_inline_code(line: str) -> list[tuple[str, bool]]:
    parts: list[tuple[str, bool]] = []
    i = 0
    while i < len(line):
        if line[i] != "`":
            j = line.find("`", i)
            if j == -1:
                parts.append((line[i:], False))
                break
            parts.append((line[i:j], False))
            i = j
            continue

        tick_len = 1
        while i + tick_len < len(line) and line[i + tick_len] == "`":
            tick_len += 1

        closing = "`" * tick_len
        end = line.find(closing, i + tick_len)
        if end == -1:
            parts.append((line[i:], False))
            break

        parts.append((line[i : end + tick_len], True))
        i = end + tick_len

    return parts


def _normalize_inline(segment: str) -> str:
    return STRONG_UNDERSCORE_RE.sub(r"**\1**", segment)


def normalize_text(text: str) -> NormalizeResult:
    in_fence = False
    fence_token: str | None = None

    out_lines: list[str] = []
    changed = False

    for raw_line in text.splitlines(keepends=True):
        match = FENCE_START_RE.match(raw_line)
        if match:
            token = match.group(1)
            if not in_fence:
                in_fence = True
                fence_token = token
            else:
                if (
                    fence_token
                    and token.startswith(fence_token[0])
                    and len(token) >= len(fence_token)
                ):
                    in_fence = False
                    fence_token = None
            out_lines.append(raw_line)
            continue

        if in_fence:
            out_lines.append(raw_line)
            continue

        segments = _split_by_inline_code(raw_line)
        new_line_parts: list[str] = []
        for seg, is_code in segments:
            if is_code:
                new_line_parts.append(seg)
                continue

            normalized = _normalize_inline(seg)
            if normalized != seg:
                changed = True
            new_line_parts.append(normalized)

        out_lines.append("".join(new_line_parts))

    updated = "".join(out_lines)
    return NormalizeResult(updated=updated, changed=changed)


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize emphasis markers to asterisk style.")
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("."),
        help="Repo root to scan (default: .)",
    )
    parser.add_argument("--apply", action="store_true", help="Write changes (default: dry-run).")
    args = parser.parse_args()

    paths = _iter_markdown_files(args.root)
    modified: list[Path] = []

    for path in paths:
        original = path.read_text(encoding="utf-8")
        result = normalize_text(original)
        if not result.changed:
            continue
        modified.append(path)
        if args.apply:
            path.write_text(result.updated, encoding="utf-8")

    if not args.apply:
        for path in modified:
            print(f"[DRY RUN] Would modify: {path.as_posix()}")
        return 2 if modified else 0

    for path in modified:
        print(f"✓ Modified: {path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
