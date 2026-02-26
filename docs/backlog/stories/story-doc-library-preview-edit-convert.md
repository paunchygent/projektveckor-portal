---
id: 'story-doc-library-preview-edit-convert'
title: 'Dokumentbibliotek MVP: preview + redigering + export (Sir Convert a Lot)'
type: 'story'
status: 'proposed'
priority: 'high'
created: '2026-02-26'
last_updated: '2026-02-26'
related:
  - 'docs/backlog/epics/epic-self-hosted-doc-library-and-conversion.md'
labels:
  - 'docs'
  - 'conversion'
---

Implementation slice with acceptance-driven scope.

## Objective

Leverera en första fungerande kedja för “dokument i portalen”:
1) lagras på servern, 2) previewas i elevytan, 3) kan redigeras av lärare, 4) exporteras till PDF/DOCX via Sir Convert a Lot.

## Scope

- Definiera dokumentmodell och URL-schema.
- Backend-API för CRUD (minst read/update) + export-trigger.
- Frontend-preview som visar allt innehåll som HTML (Markdown-rendering som primär).
- Minimal admin-UI för redigering.
- AuthN/AuthZ integreras från dag ett via HuleEdu/Skriptoteket (ingen hardcoded auth i portalen).

## Acceptance Criteria

- [ ] Ett dokument kan skapas/uppdateras via admin och previewas i elevytan.
- [ ] Export-knapp skapar PDF och DOCX (eller en tydlig job-status om async).
- [ ] Dokument som inte är lärarinstruktioner är åtkomliga utan inloggning.
- [ ] Lärarinstruktioner kräver inloggning via HuleEdu/Skriptoteket.

## Test Requirements

- [ ] API-test eller manuell check: list/get/update fungerar.
- [ ] Manuell check: preview laddar och export skapar filer.

## Done Definition

- Dokumentmodellen och integrationen är dokumenterade (ref + ADR-länk).

## Checklist

- [ ] Implementation complete
- [ ] Tests and validations complete
- [ ] Docs synchronized
