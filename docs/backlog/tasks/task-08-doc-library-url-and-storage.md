---
id: 'task-08-doc-library-url-and-storage'
title: 'Definiera dokumentbibliotek: URL-schema, lagring och metadata'
type: 'task'
status: 'proposed'
priority: 'high'
created: '2026-02-26'
last_updated: '2026-02-26'
related:
  - 'docs/backlog/stories/story-doc-library-preview-edit-convert.md'
  - 'docs/decisions/0002-self-hosted-documents-and-conversion.md'
labels:
  - 'docs'
---

PR-sized execution unit; may be linked to a story or standalone.

## Objective

Sätta en stabil grund för dokument i portalen: hur de adresseras (URL), var de lagras, och hur de beskrivs (metadata).

## PR Scope

- Beskriv och implementera ett första URL-schema (t.ex. `/dokument/<projektvecka>/<slug>`).
- Beskriv och implementera lagring på servern (t.ex. `data/docs/...`) samt metadata (YAML/JSON).

## Deliverables

- [ ] Dokumenterad modell (ref) + kodstöd i backend.

## Acceptance Criteria

- [ ] Det går att lista dokument och hämta ett dokument via backend.

## Checklist

- [ ] Implementation complete
- [ ] Validation complete
- [ ] Docs updated

