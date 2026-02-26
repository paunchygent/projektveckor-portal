---
id: "task-07-pre-commit-quality-gate"
title: "Inför pre-commit: docs-kontrakt + backlog-kontrakt (lokal gate)"
type: "task"
status: "proposed"
priority: "medium"
created: "2026-02-26"
last_updated: "2026-02-26"
related:
  - "docs/backlog/stories/story-port-doc-guards.md"
labels:
  - "quality"
  - "pre-commit"
---

PR-sized execution unit; may be linked to a story or standalone.

## Objective

Göra det lätt att “göra rätt” genom att kvalitetssäkra docs/backlog automatiskt vid commit.

## PR Scope

- Lägg till `.pre-commit-config.yaml` med hooks för:
  - `pdm run validate-docs`
  - `pdm run validate-backlog`
  - (valfritt) `pdm run check:md` om Node finns

## Deliverables

- [ ] Pre-commit-konfig som kan installeras och köras lokalt.

## Acceptance Criteria

- [ ] `pre-commit run --all-files` stoppar kontraktbrott.

## Checklist

- [ ] Implementation complete
- [ ] Validation complete
- [ ] Docs updated
