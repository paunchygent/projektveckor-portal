---
id: 'task-09-backend-doc-preview-api'
title: 'Backend: API för dokument-preview (read) + update (admin)'
type: 'task'
status: 'proposed'
priority: 'high'
created: '2026-02-26'
last_updated: '2026-02-26'
related:
  - 'docs/backlog/stories/story-doc-library-preview-edit-convert.md'
labels:
  - 'backend'
  - 'docs'
---

PR-sized execution unit; may be linked to a story or standalone.

## Objective

Göra dokument åtkomliga för preview och redigering via ett tunt API (Clean Architecture/DIP).

## PR Scope

- Read endpoints: list + get (source + preview-ready representation).
- Admin endpoint: update source (minst för Markdown/HTML).
- Auth: integrera AuthN/AuthZ via HuleEdu/Skriptoteket från dag ett (ingen hardcoded admin-key).

## Deliverables

- [ ] FastAPI routes + app/service-lager + storage implementation.

## Acceptance Criteria

- [ ] En admin kan uppdatera ett dokument och elevytan ser uppdateringen vid refresh.

## Checklist

- [ ] Implementation complete
- [ ] Validation complete
- [ ] Docs updated
