---
id: "090-documentation-standards"
type: "standards"
created: "2026-02-25"
scope: "all"
---

# Documentation standards (doc-as-code)

## Canonical docs

- `docs/index.md` is the documentation entrypoint.
- `.agent/readme-first.md` is the agent entrypoint.
- `.agent/handoff.md` holds cross-session context (current only).
- `.agent/long-term-memory.md` is append-only durable memory.

## MUST

- Keep `.agent/readme-first.md` and `.agent/handoff.md` structure stable.
- Prefer links over duplication.
- Avoid drift: when a workflow changes, update the rule that defines it.

