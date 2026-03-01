"""Validate `.agents/skills/*/SKILL.md` frontmatter requirements.

Purpose:
    Enforce a minimal metadata contract for repo-local Codex skills so skill
    discovery remains stable and predictable.

Relationships:
    - Canonical skill surface: `.agents/skills/`
    - Exposed via `pdm run validate-skills`
    - Wired to pre-commit for commit-time enforcement
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

from scripts.docs_as_code.common import ROOT

DEFAULT_SKILLS_ROOT = ROOT / ".agents" / "skills"
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
REQUIRED_FIELDS: tuple[str, ...] = ("name", "description")


def _display_path(path: Path) -> str:
    """Return a stable repo-relative display path."""
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def parse_frontmatter(text: str) -> tuple[dict[str, object] | None, str | None]:
    """Parse YAML frontmatter from markdown text.

    Args:
        text: Full markdown file contents.

    Returns:
        Parsed frontmatter mapping and parse error string.
    """
    if not text.startswith("---"):
        return None, "missing YAML frontmatter block at top of file"

    match = FRONTMATTER_RE.match(text)
    if match is None:
        return None, "frontmatter not closed (missing second '---')"

    try:
        raw = yaml.safe_load(match.group(1)) or {}
    except Exception as exc:  # pragma: no cover
        return None, f"invalid YAML frontmatter: {exc}"

    if not isinstance(raw, dict):
        return None, "frontmatter must be a YAML mapping/object"

    return {str(key): value for key, value in raw.items()}, None


def validate_skill_frontmatter(skills_root: Path) -> list[str]:
    """Return validation errors for all skill files under `skills_root`.

    Args:
        skills_root: Path to `.agents/skills`.

    Returns:
        Human-readable validation errors.
    """
    errors: list[str] = []
    if not skills_root.exists():
        return [f"skills root not found: {skills_root}"]
    if not skills_root.is_dir():
        return [f"skills root is not a directory: {skills_root}"]

    skill_files = sorted(skills_root.glob("*/SKILL.md"))
    if not skill_files:
        return [f"no SKILL.md files found under: {skills_root}"]

    for skill_file in skill_files:
        text = skill_file.read_text(encoding="utf-8")
        frontmatter, parse_error = parse_frontmatter(text)
        display = _display_path(skill_file)
        if parse_error is not None:
            errors.append(f"{display}: {parse_error}")
            continue

        assert frontmatter is not None
        for field_name in REQUIRED_FIELDS:
            value = frontmatter.get(field_name)
            if not isinstance(value, str) or not value.strip():
                errors.append(f"{display}: missing required frontmatter field '{field_name}'")

    return errors


def main() -> None:
    """CLI entrypoint."""
    parser = argparse.ArgumentParser(
        description="Validate required frontmatter fields for repo-local skill files."
    )
    parser.add_argument(
        "--skills-root",
        default=str(DEFAULT_SKILLS_ROOT),
        help="Path to skills root directory (default: .agents/skills).",
    )
    args = parser.parse_args()

    skills_root = Path(args.skills_root).resolve(strict=False)
    errors = validate_skill_frontmatter(skills_root)
    if errors:
        print("[ERROR] Skill frontmatter validation failed:")
        for error in errors:
            print(f"  - {error}")
        raise SystemExit(1)

    print(f"Validation passed. Checked {skills_root}")


if __name__ == "__main__":
    main()
