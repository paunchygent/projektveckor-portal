"""Create a new rule file with contract-compliant frontmatter."""

from __future__ import annotations

import argparse

from scripts.docs_as_code.common import (
    RULES_DIR,
    ensure_parent,
    next_numeric_prefix,
    slugify,
    today_iso,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a new rule file in .agents/rules/.")
    parser.add_argument("name", help="Rule name")
    parser.add_argument("--trigger", default="model_decision", help="Rule trigger value")
    parser.add_argument("--status", default="active", help="Rule status")
    parser.add_argument(
        "--owner",
        action="append",
        default=[],
        help="Owner value; repeat for multiple entries (default: portal)",
    )
    args = parser.parse_args()

    prefix = next_numeric_prefix(RULES_DIR)
    slug = slugify(args.name)
    target = RULES_DIR / f"{prefix}-{slug}.md"

    owners = args.owner if args.owner else ["portal"]
    owners_yaml = "\n".join(f"  - {owner}" for owner in owners)
    created = today_iso()

    ensure_parent(target)
    content = f"""---
trigger: {args.trigger}
rule_id: RULE-{prefix}
title: {args.name}
status: {args.status}
created: {created}
owners:
{owners_yaml}
tags: []
scope: repo
---
## Purpose

TBD.

## Rules

- TBD.
"""
    target.write_text(content, encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
