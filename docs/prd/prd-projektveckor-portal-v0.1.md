---
type: prd
id: PRD-projektveckor-portal-v0.1
title: Projektveckor Portal v0.1
status: draft
created: "2026-02-26"
updated: "2026-02-26"
owners:
  - portal
tags:
  - prd
links:
  - docs/index.md
---

## Bakgrund

Hulebäcksgymnasiet genomför återkommande projektveckor. För att minska friktion och öka kvalitet behöver elever och delegationer en samlad ingång till material, regler och arbetsstöd.

## Mål

- En stabil webbadress per projektvecka.
- En tydlig ingång till FN-rollspelsveckan (förberedelse + spel).
- Lärarverktyg för bulletin/nyheter och resurshantering (inloggat).

## I scope (v0.1)

- Hostad portal på `hule.education`.
- FN-rollspel v.43 (HT25) som första “week page”.
- Dokument och resurser hostas på hemmaservern och kan förhandsvisas i portalen.
- Konvertering till nedladdningsbara filer (PDF/DOCX) via Sir Convert a Lot.
- Autentisering/auktorisering för lärarytan återanvänds från HuleEdu/Skriptoteket (ADR-0003).

## Out of scope (v0.1)

- Fullständig roll-/resolution-generator (kan bli v0.2+).
- Support för fler projektveckor (läggs efter FN-rollspel v.43 är stabil).

## Krav (hög nivå)

- Navigering och preview ska fungera i vanliga webbläsare (utan externa “preview”-sandboxes).
- Backend ska vara tunn och följa DDD/Clean Architecture (DIP, DI, SRP).
