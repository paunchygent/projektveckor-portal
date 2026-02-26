---
id: "epic-self-hosted-doc-library-and-conversion"
title: "Självhostat dokumentbibliotek + preview/redigering + konvertering"
type: "epic"
status: "proposed"
priority: "high"
created: "2026-02-26"
last_updated: "2026-02-26"
related:
  - "docs/backlog/programmes/programme-projektveckor-portal-v0-1.md"
  - "docs/prd/prd-projektveckor-portal-v0.1.md"
  - "docs/decisions/0002-self-hosted-documents-and-conversion.md"
labels:
  - "docs"
  - "conversion"
---

Major capability increment managed through linked stories.

## Goal

Alla dokument och resurser som portalen använder ska kunna:

- hostas på hemmaservern,
- förhandsvisas i webben (som HTML),
- redigeras i lärarytan,
- exporteras till PDF/DOCX via Sir Convert a Lot.

## In Scope

- Dokumentbibliotek (URL-schema + lagring + metadata).
- Preview-komponenter (Markdown→HTML som primär, samt ev. PDF för exporter).
- Admin-redigering för källor (Markdown först).
- Adapter/integration mot Sir Convert a Lot.
- Åtkomstkontroll: öppet för alla som standard; lärarinstruktioner kräver inloggning.

## Out of Scope

- Avancerad versionshantering (Git-lik) för dokument (senare).
- Full WYSIWYG för alla format (starta med Markdown/HTML).

## Stories

1. `docs/backlog/stories/story-doc-library-preview-edit-convert.md`

## Acceptance Criteria

- [ ] Minst ett dokument kan redigeras i lärarytan och exporteras till PDF/DOCX.
- [ ] Elevytan kan förhandsvisa samma dokument utan att lämna portalen.

## Checklist

- [ ] Stories linked
- [ ] Acceptance criteria defined
- [ ] Execution gate defined
