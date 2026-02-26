---
id: 'task-05-doc-guard-link-integrity'
title: 'Docs guard: länk-integritet och tomma länkar'
type: 'task'
status: 'proposed'
priority: 'medium'
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

Fånga trasiga länkar och tomma markdown-länkar i `docs/` och `docs/backlog/` innan de sprids.

## PR Scope

- Port/adapta HuleEdu validator (link integrity + empty-link guard).
- Körs via `pdm run validate-docs` (eller ny sub-command).

## Deliverables

- [ ] Ny/utökad validator med tydliga felutskrifter.

## Acceptance Criteria

- [ ] Avsiktligt trasig länk ger ett deterministiskt fel med fil + rad.

## Checklist

- [ ] Implementation complete
- [ ] Validation complete
- [ ] Docs updated

