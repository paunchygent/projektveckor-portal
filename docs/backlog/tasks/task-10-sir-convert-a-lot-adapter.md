---
id: 'task-10-sir-convert-a-lot-adapter'
title: 'Backend: adapter mot Sir Convert a Lot (export PDF/DOCX)'
type: 'task'
status: 'proposed'
priority: 'high'
created: '2026-02-26'
last_updated: '2026-02-26'
related:
  - 'docs/backlog/stories/story-doc-library-preview-edit-convert.md'
  - 'docs/decisions/0002-self-hosted-documents-and-conversion.md'
labels:
  - 'backend'
  - 'conversion'
---

PR-sized execution unit; may be linked to a story or standalone.

## Objective

Koppla portalen till Sir Convert a Lot så att ett dokument kan exporteras till PDF/DOCX på ett repeterbart sätt.

## PR Scope

- Definiera port (protocol) för konvertering + implementation (HTTP/CLI beroende på tjänsten).
- Spara exporter på servern och exponera dem som nedladdningslänkar.
- Hantera async job-status om Sir Convert a Lot jobbar asynkront.

## Deliverables

- [ ] Adapter + config + enkel job-status.

## Acceptance Criteria

- [ ] “Exportera” ger en PDF och en DOCX som går att ladda ner från portalen.

## Checklist

- [ ] Implementation complete
- [ ] Validation complete
- [ ] Docs updated

