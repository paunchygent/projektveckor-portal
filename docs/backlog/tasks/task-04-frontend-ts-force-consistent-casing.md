---
id: 'task-04-frontend-ts-force-consistent-casing'
title: 'Aktivera forceConsistentCasingInFileNames i frontend'
type: 'task'
status: 'completed'
priority: 'low'
created: '2026-02-26'
last_updated: '2026-02-26'
related:
  - 'docs/backlog/stories/story-doc-as-code-mvp.md'
labels:
  - 'frontend'
  - 'typescript'
---

PR-sized execution unit; may be linked to a story or standalone.

## Objective

Minska “funkar på min maskin”-problem mellan Windows/macOS/Linux genom att tvinga konsekvent filnamnscasing i TS.

## PR Scope

- Sätt `compilerOptions.forceConsistentCasingInFileNames=true`.

## Deliverables

- [ ] `frontend/tsconfig.json` uppdaterad.

## Acceptance Criteria

- [ ] Typecheck varnar inte om casing-mismatch upptäcks.

## Checklist

- [ ] Implementation complete
- [ ] Validation complete
- [ ] Docs updated

