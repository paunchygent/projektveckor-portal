"""Create a new documentation file with contract-compliant frontmatter."""

from __future__ import annotations

import argparse
from pathlib import Path

from scripts.docs_as_code.common import DOCS_DIR, ensure_parent, slugify, today_iso


def infer_doc_type(relative_path: Path) -> str:
    if not relative_path.parts:
        return "spec"

    top = relative_path.parts[0]
    if top == "decisions":
        return "decision"
    if top == "runbooks":
        return "runbook"
    if top == "reference":
        return "reference"
    if top == "prd":
        return "prd"
    if top == "_meta":
        return "meta"
    return "spec"


def default_id(doc_type: str, target: Path) -> str:
    stem_slug = slugify(target.stem)

    if doc_type == "decision":
        prefix = target.name.split("-", 1)[0]
        if prefix.isdigit() and len(prefix) == 4:
            return f"ADR-{prefix}"
        return f"ADR-{stem_slug}"

    if doc_type == "runbook":
        suffix = stem_slug.replace("runbook-", "")
        return f"RUN-{suffix}"

    if doc_type == "reference":
        suffix = stem_slug.replace("ref-", "")
        return f"REF-{suffix}"

    if doc_type == "prd":
        suffix = stem_slug.replace("prd-", "")
        return f"PRD-{suffix}"

    if doc_type == "meta":
        return f"META-{stem_slug}"

    return f"SPEC-{stem_slug}"


def default_status(doc_type: str) -> str:
    if doc_type == "decision":
        return "proposed"
    return "draft"


def default_title(relative_path: Path) -> str:
    return relative_path.stem.replace("_", " ").replace("-", " ").title()


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a docs markdown file under docs/.")
    parser.add_argument("path", help="Relative path under docs/, e.g. runbooks/runbook-example.md")
    parser.add_argument("--title", default="", help="Optional document title")
    parser.add_argument("--type", default="", help="Override inferred type")
    parser.add_argument("--status", default="", help="Override default status")
    parser.add_argument("--id", default="", help="Override generated ID")
    parser.add_argument(
        "--owner",
        action="append",
        default=[],
        help="Owner value; repeat for multiple entries (default: portal)",
    )
    parser.add_argument("--system", default="", help="System value (required for runbooks)")
    args = parser.parse_args()

    relative_path = Path(args.path)
    target = DOCS_DIR / relative_path
    if target.suffix == "":
        target = target.with_suffix(".md")

    if target.exists():
        raise SystemExit(f"Target already exists: {target}")

    doc_type = args.type if args.type else infer_doc_type(relative_path)
    title = args.title if args.title else default_title(relative_path)
    status = args.status if args.status else default_status(doc_type)
    doc_id = args.id if args.id else default_id(doc_type, target)
    owners = args.owner if args.owner else ["portal"]
    created = today_iso()

    owners_yaml = "\n".join(f"  - {owner}" for owner in owners)
    system_yaml = f"system: {args.system}\n" if args.system else ""

    content = (
        "---\n"
        f"type: {doc_type}\n"
        f"id: {doc_id}\n"
        f"title: {title}\n"
        f"status: {status}\n"
        f"created: {created}\n"
        f"updated: {created}\n"
        "owners:\n"
        f"{owners_yaml}\n"
        "tags: []\n"
        "links: []\n"
        f"{system_yaml}"
        "---\n"
        "## Purpose\n\n"
        "TBD.\n"
    )

    ensure_parent(target)
    target.write_text(content, encoding="utf-8")
    print(target)


if __name__ == "__main__":
    main()
