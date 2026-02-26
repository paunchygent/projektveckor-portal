"""Validate docs/backlog frontmatter and template structure."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

from scripts.docs_as_code.common import BACKLOG_DIR, ROOT
from scripts.docs_as_code.task_templates import TEMPLATES, invalid_title_prefixes, subdirectory_for

REQUIRED_KEYS = ("id", "title", "type", "status", "priority", "created", "last_updated")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
TASK_LOG_REQUIRED_SECTIONS: tuple[str, ...] = ("Context", "Worklog", "Next Actions")
TASK_LOG_MAX_LINES = 220
TASK_LOG_MAX_WORKLOG_ENTRIES = 12
WORKLOG_DATE_ENTRY_RE = re.compile(r"^- \d{4}-\d{2}-\d{2}\b")


def parse_frontmatter(text: str) -> tuple[dict[str, object] | None, str | None]:
    if not text.startswith("---"):
        return None, "missing frontmatter start"

    match = FRONTMATTER_RE.match(text)
    if match is None:
        return None, "missing frontmatter end"

    try:
        raw = yaml.safe_load(match.group(1)) or {}
    except Exception as exc:  # pragma: no cover
        return None, f"invalid YAML frontmatter: {exc}"

    if not isinstance(raw, dict):
        return None, "frontmatter must be a mapping"

    return {str(key): value for key, value in raw.items()}, None


def extract_h1(text: str) -> str | None:
    match = FRONTMATTER_RE.match(text)
    body = text[match.end() :] if match is not None else text
    match = re.search(r"^#\s+(.+)$", body, flags=re.MULTILINE)
    return match.group(1).strip() if match else None


def extract_section(text: str, section: str) -> str | None:
    pattern = re.compile(
        rf"^##\s+{re.escape(section)}\s*\n(.*?)(?=^##\s+|\Z)",
        flags=re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group(1).strip() if match else None


def is_placeholder_block(text: str | None) -> bool:
    if text is None:
        return True
    compact = text.strip()
    if compact == "":
        return True
    lowered = compact.lower()
    return lowered in {"tbd.", "tbd"} or lowered.startswith("tbd") or lowered.startswith("pending")


def repo_relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def validate_sections(path: Path, text: str, item_type: str) -> list[str]:
    errors: list[str] = []
    template = TEMPLATES.get(item_type)
    if template is None:
        return errors

    for section in template.sections:
        marker = f"## {section}"
        if marker not in text:
            errors.append(f"{repo_relative(path)}: missing required section '{marker}'")

    return errors


def validate_task_log_invariants(path: Path, text: str) -> list[str]:
    errors: list[str] = []
    line_count = len(text.splitlines())
    if line_count > TASK_LOG_MAX_LINES:
        errors.append(
            f"{repo_relative(path)}: exceeds {TASK_LOG_MAX_LINES} lines ({line_count}); compress."
        )

    headings = [
        match.group(1).strip() for match in re.finditer(r"^##\s+(.+)$", text, flags=re.MULTILINE)
    ]
    if tuple(headings) != TASK_LOG_REQUIRED_SECTIONS:
        expected = ", ".join(TASK_LOG_REQUIRED_SECTIONS)
        found = ", ".join(headings) if headings else "(none)"
        errors.append(
            f"{repo_relative(path)}: task-log must use exact H2 template/order ({expected}); "
            f"found ({found})."
        )
        return errors

    worklog_start = text.find("## Worklog")
    next_actions_start = text.find("## Next Actions")
    if worklog_start == -1 or next_actions_start == -1 or next_actions_start <= worklog_start:
        return errors

    worklog_block = text[worklog_start:next_actions_start]
    entry_count = sum(1 for line in worklog_block.splitlines() if WORKLOG_DATE_ENTRY_RE.match(line))
    if entry_count > TASK_LOG_MAX_WORKLOG_ENTRIES:
        errors.append(
            f"{repo_relative(path)}: Worklog has {entry_count} entries; "
            f"compress to <= {TASK_LOG_MAX_WORKLOG_ENTRIES}."
        )
    return errors


def validate_location(path: Path, item_type: str) -> list[str]:
    errors: list[str] = []
    rel = path.relative_to(BACKLOG_DIR)
    expected = subdirectory_for(item_type)

    if item_type in {"task-log", "reference"}:
        if expected and rel.parts[0] != expected:
            errors.append(f"{repo_relative(path)}: expected in docs/backlog/{expected}/")
        if item_type == "task-log" and rel.name != "current.md":
            errors.append(f"{repo_relative(path)}: task-log file must be named current.md")
        if item_type == "reference" and len(rel.parts) == 1:
            if rel.name != "README.md" and not rel.name.startswith("README-"):
                errors.append(
                    f"{repo_relative(path)}: root reference filename should be README.md or README-*.md"
                )
        return errors

    if expected and (not rel.parts or rel.parts[0] != expected):
        errors.append(
            f"{repo_relative(path)}: type '{item_type}' must live in docs/backlog/{expected}/"
        )
    return errors


def validate_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []

    frontmatter, parse_error = parse_frontmatter(text)
    if parse_error is not None:
        return [f"{repo_relative(path)}: {parse_error}"]
    assert frontmatter is not None

    for key in REQUIRED_KEYS:
        if key not in frontmatter:
            errors.append(f"{repo_relative(path)}: missing required key '{key}'")

    item_type = str(frontmatter.get("type", "")).strip()
    if item_type not in TEMPLATES:
        errors.append(f"{repo_relative(path)}: unsupported type '{item_type}'")
        return errors

    if item_type == "review":
        status_value = str(frontmatter.get("status", "")).strip()
        allowed = {"pending", "responded", "completed"}
        if status_value not in allowed:
            errors.append(
                f"{repo_relative(path)}: review status must be one of "
                f"({', '.join(sorted(allowed))}); found '{status_value}'"
            )

    title = str(frontmatter.get("title", "")).strip()
    if not title:
        errors.append(f"{repo_relative(path)}: title must be non-empty")
    else:
        lowered = title.lower()
        for prefix in invalid_title_prefixes():
            if lowered.startswith(prefix):
                errors.append(
                    f"{repo_relative(path)}: title should not start with "
                    f"'{prefix.strip()}' (type exists in frontmatter)"
                )
                break

    h1 = extract_h1(text)
    if h1 is not None:
        errors.append(
            f"{repo_relative(path)}: top-level markdown H1 headings are not allowed; "
            "frontmatter title is canonical"
        )

    errors.extend(validate_location(path, item_type))
    errors.extend(validate_sections(path, text, item_type))
    if item_type == "task-log":
        errors.extend(validate_task_log_invariants(path, text))

    if item_type == "review":
        status_value = str(frontmatter.get("status", "")).strip()
        related_obj = frontmatter.get("related")
        if not isinstance(related_obj, list) or not related_obj:
            errors.append(f"{repo_relative(path)}: review must include non-empty related list")

        rel = path.relative_to(BACKLOG_DIR)
        if rel.parts[0] != "reviews" or len(rel.parts) != 3 or rel.name != "README.md":
            errors.append(
                f"{repo_relative(path)}: review must be stored at "
                "docs/backlog/reviews/<review-id>/README.md"
            )

        if status_value in {"responded", "completed"}:
            response_body = extract_section(text, "Response")
            if is_placeholder_block(response_body):
                errors.append(
                    f"{repo_relative(path)}: review status '{status_value}' requires a filled "
                    "Response section"
                )

        if status_value == "completed":
            completion_body = extract_section(text, "Completion")
            if is_placeholder_block(completion_body):
                errors.append(
                    f"{repo_relative(path)}: review status 'completed' requires a filled "
                    "Completion section"
                )

    return errors


def main() -> None:
    if not BACKLOG_DIR.exists():
        raise SystemExit("docs/backlog is missing")

    backlog_files = sorted(BACKLOG_DIR.rglob("*.md"))
    all_errors: list[str] = []

    for backlog_file in backlog_files:
        all_errors.extend(validate_file(backlog_file))

    if all_errors:
        for error in all_errors:
            print(error)
        raise SystemExit(1)

    print(f"Validated {len(backlog_files)} backlog files")


if __name__ == "__main__":
    main()

