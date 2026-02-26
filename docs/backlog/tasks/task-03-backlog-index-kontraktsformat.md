---
id: 'task-03-backlog-index-kontraktsformat'
title: 'Indexera backlog i kontraktsformat (frontmatter + inga H1)'
type: 'task'
status: 'completed'
priority: 'medium'
created: '2026-02-26'
last_updated: '2026-02-26'
related:
  - 'docs/backlog/stories/story-doc-as-code-mvp.md'
labels:
  - 'docs-as-code'
  - 'backlog'
---

PR-sized execution unit; may be linked to a story or standalone.

## Objective

Göra `pdm run index-backlog` kompatibel med backlog-valideringen, så att index-filen själv är ett giltigt backlog-dokument.

## PR Scope

- Indexgenerator skriver frontmatter och använder H2 (inga H1).
- Output placeras som `docs/backlog/README-index.md` och undantas från att indexera sig själv.

## Deliverables

- [ ] Indexfil genereras utan att bryta `validate-backlog`.

## Acceptance Criteria

- [ ] `pdm run index-backlog` passerar och skapar/uppdaterar `docs/backlog/README-index.md`.

## Checklist

- [ ] Implementation complete
- [ ] Validation complete
- [ ] Docs updated

