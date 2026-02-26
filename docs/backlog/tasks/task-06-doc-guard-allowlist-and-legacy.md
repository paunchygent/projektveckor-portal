---
id: 'task-06-doc-guard-allowlist-and-legacy'
title: 'Docs guard: top-level allowlist + legacy-token guard'
type: 'task'
status: 'proposed'
priority: 'low'
created: '2026-02-26'
last_updated: '2026-02-26'
related:
  - 'docs/backlog/stories/story-port-doc-guards.md'
labels:
  - 'docs-as-code'
  - 'validation'
---

PR-sized execution unit; may be linked to a story or standalone.

## Objective

Stoppa “drift” i dokumentstrukturen och gamla paths/kommandon som annars blir kvar i text över tid.

## PR Scope

- Top-level allowlist för `docs/` och relevanta undermappar.
- Legacy-token guard för kända “felstavade/utgångna” paths (t.ex. `.agents/` vs `.agent/`).

## Deliverables

- [ ] Validatorregler (konfigurerade och dokumenterade).

## Acceptance Criteria

- [ ] Oönskade mappar/filer i docs-surface ger fel.
- [ ] Legacy-token i docs ger fel med tydlig rekommendation.

## Checklist

- [ ] Implementation complete
- [ ] Validation complete
- [ ] Docs updated

