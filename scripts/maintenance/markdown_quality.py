#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

MARKDOWNLINT_CLI2_PKG = "markdownlint-cli2@0.21.0"
PRETTIER_PKG = "prettier@3.8.1"


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _has_local_npx() -> bool:
    return shutil.which("npx") is not None


def _has_cmd_exe() -> bool:
    return shutil.which("cmd.exe") is not None


def _cmd_exe() -> str:
    return os.environ.get("COMSPEC") or "cmd.exe"


def _run_local(argv: list[str]) -> int:
    proc = subprocess.run(argv, cwd=_repo_root())
    return proc.returncode


def _run_windows_cmd(argv: list[str]) -> int:
    cmdline = subprocess.list2cmdline(argv)
    proc = subprocess.run([_cmd_exe(), "/c", cmdline], cwd=_repo_root())
    return proc.returncode


def _run_npx(args: list[str]) -> int:
    argv = ["npx", "--yes", *args]
    if sys.platform == "win32":
        return _run_windows_cmd(argv)
    if _has_local_npx():
        return _run_local(argv)
    if _has_cmd_exe():
        return _run_windows_cmd(argv)
    raise RuntimeError("Neither `npx` nor `cmd.exe` is available; install Node.js.")


def _run_markdownlint(*, fix: bool, paths: list[str]) -> int:
    argv = [MARKDOWNLINT_CLI2_PKG]
    if paths:
        argv.append("--no-globs")
        argv.extend(paths)
    if fix:
        argv.append("--fix")
    return _run_npx(argv)


def _run_prettier(*, write: bool, paths: list[str]) -> int:
    default_patterns = ["**/*.md", "**/*.mdc"]
    targets = paths or default_patterns

    argv = [
        PRETTIER_PKG,
        "--ignore-path",
        ".prettierignore",
        "--config",
        ".prettierrc.json",
        "--log-level",
        "warn",
        "--no-error-on-unmatched-pattern",
        "--write" if write else "--check",
        *targets,
    ]
    return _run_npx(argv)


def _run_frontmatter_fixer(*, apply: bool) -> int:
    argv = [
        sys.executable,
        "-m",
        "scripts.maintenance.fix_frontmatter_duplicate_h1",
        "--root",
        str(_repo_root()),
    ]
    if apply:
        argv.append("--apply")
    proc = subprocess.run(argv, cwd=_repo_root())
    return proc.returncode


def _run_emphasis_normalizer(*, apply: bool) -> int:
    argv = [
        sys.executable,
        "-m",
        "scripts.maintenance.normalize_emphasis_markers",
        "--root",
        str(_repo_root()),
    ]
    if apply:
        argv.append("--apply")
    proc = subprocess.run(argv, cwd=_repo_root())
    return proc.returncode


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Markdown quality wrapper (prettier + markdownlint-cli2)."
    )
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    p_lint = subparsers.add_parser("lint", help="Run markdownlint (no fixes).")
    p_lint.add_argument("paths", nargs="*", help="Optional file/glob paths to lint.")

    p_fix = subparsers.add_parser("fix", help="Run markdownlint with --fix.")
    p_fix.add_argument("paths", nargs="*", help="Optional file/glob paths to fix.")

    p_format = subparsers.add_parser("format", help="Run prettier --write on Markdown files.")
    p_format.add_argument("paths", nargs="*", help="Optional file/glob paths to format.")

    p_check = subparsers.add_parser(
        "check",
        help=(
            "Run prettier --check, frontmatter title/H1 check, emphasis marker check, "
            "and markdownlint."
        ),
    )
    p_check.add_argument("paths", nargs="*", help="Optional file/glob paths to check.")

    p_autofix = subparsers.add_parser(
        "autofix",
        help="Run fixers + markdownlint --fix + prettier --write.",
    )
    p_autofix.add_argument("paths", nargs="*", help="Optional file/glob paths to autofix.")

    args = parser.parse_args()
    paths: list[str] = list(getattr(args, "paths", []))

    if args.cmd == "lint":
        return _run_markdownlint(fix=False, paths=paths)
    if args.cmd == "fix":
        return _run_markdownlint(fix=True, paths=paths)
    if args.cmd == "format":
        return _run_prettier(write=True, paths=paths)
    if args.cmd == "check":
        rc = _run_prettier(write=False, paths=paths)
        if rc != 0:
            return rc
        rc = _run_frontmatter_fixer(apply=False)
        if rc != 0:
            return rc
        rc = _run_emphasis_normalizer(apply=False)
        if rc != 0:
            return rc
        return _run_markdownlint(fix=False, paths=paths)
    if args.cmd == "autofix":
        rc = _run_frontmatter_fixer(apply=True)
        if rc != 0:
            return rc
        rc = _run_emphasis_normalizer(apply=True)
        if rc != 0:
            return rc
        rc = _run_markdownlint(fix=True, paths=paths)
        if rc != 0:
            return rc
        rc = _run_prettier(write=True, paths=paths)
        if rc != 0:
            return rc
        return 0

    raise RuntimeError(f"Unknown command: {args.cmd}")


if __name__ == "__main__":
    raise SystemExit(main())
