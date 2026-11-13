---
id: "task-12-admin-doc-editor"
title: "Frontend: admin-redigerare för dokument (MVP)"
type: "task"
status: "proposed"
priority: "medium"
created: "2026-02-26"
last_updated: "2026-02-26"
related:
  - "docs/backlog/stories/story-doc-library-preview-edit-convert.md"
labels:
  - "frontend"
  - "admin"
---

PR-sized execution unit; may be linked to a story or standalone.

## Objective

Låta lärare redigera dokument direkt i portalen och trigga export till PDF/DOCX.

## PR Scope

- Enkel editor (text) för Markdown/HTML-källor.
- “Spara” + “Exportera”-knappar som anropar backend.
- Grundläggande status/feedback (sparat, export pågår, export klar).
- Kräver inloggning (AuthN/AuthZ via HuleEdu/Skriptoteket).

## Deliverables

- [ ] Admin-route + editor.

## Acceptance Criteria

- [ ] Läraren kan uppdatera och exportera ett dokument utan att använda server-shell.

## Checklist

- [ ] Implementation complete
- [ ] Validation complete
- [ ] Docs updated
