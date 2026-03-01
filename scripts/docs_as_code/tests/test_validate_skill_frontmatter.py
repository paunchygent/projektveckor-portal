"""Tests for `.agents/skills` frontmatter validation.

Purpose:
    Ensure repo-local skill files require `name` and `description` frontmatter
    fields.
"""

from __future__ import annotations

from pathlib import Path

from scripts.docs_as_code.validate_skill_frontmatter import validate_skill_frontmatter


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_validate_skill_frontmatter_accepts_required_fields(tmp_path: Path) -> None:
    """Accept frontmatter when required fields are present."""
    skills_root = tmp_path / ".agents" / "skills"
    _write(
        skills_root / "example-skill" / "SKILL.md",
        "---\nname: Example skill\ndescription: Example skill\n---\n\n# Example Skill\n",
    )

    errors = validate_skill_frontmatter(skills_root)
    assert errors == []


def test_validate_skill_frontmatter_rejects_missing_name(tmp_path: Path) -> None:
    """Reject frontmatter when `name` is missing."""
    skills_root = tmp_path / ".agents" / "skills"
    _write(
        skills_root / "example-skill" / "SKILL.md",
        "---\ndescription: Example skill\n---\n\n# Example Skill\n",
    )

    errors = validate_skill_frontmatter(skills_root)
    assert any("missing required frontmatter field 'name'" in error for error in errors)


def test_validate_skill_frontmatter_rejects_missing_description(tmp_path: Path) -> None:
    """Reject frontmatter when `description` is missing."""
    skills_root = tmp_path / ".agents" / "skills"
    _write(
        skills_root / "example-skill" / "SKILL.md",
        "---\nname: Example skill\n---\n\n# Example Skill\n",
    )

    errors = validate_skill_frontmatter(skills_root)
    assert any("missing required frontmatter field 'description'" in error for error in errors)
