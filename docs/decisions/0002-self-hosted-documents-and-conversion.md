---
type: decision
id: ADR-0002
title: "Självhostade dokument med preview/redigering + exports via Sir Convert a Lot"
status: accepted
created: "2026-02-26"
updated: "2026-02-26"
owners:
  - portal
tags:
  - architecture
  - docs
  - conversion
links:
  - docs/prd/prd-projektveckor-portal-v0.1.md
---

## Kontext

Tidigare har upplägget utgått från att portalen “länkar vidare” till dokument i SharePoint/Teams. Det skapar beroenden på externa preview-miljöer, inloggningar och constraints som vi inte styr.

Projektets målbild kräver att elever/delegationer hittar _allt_ via portalen och att lärare kan uppdatera materialet direkt i portalen under projektveckan.

## Beslut

- **Alla dokument som portalen länkar till ska hostas på hemmaservern** (samma domän som portalen).
- Portalen ska erbjuda:
  - **förhandsvisning** av material (minst HTML/PDF/Markdown),
  - **redigering** (i första hand Markdown/HTML-baserade källor) i lärarytan, och
  - **konvertering** till nedladdningsbara format (PDF/DOCX) via **Sir Convert a Lot**.
- Sir Convert a Lot integreras via en **tunn adapter** (port + adapter enligt Clean Architecture/DIP), så att portalen inte blir beroende av en specifik transport eller implementation.

## Konsekvenser

- Vi behöver ett tydligt **dokumentbibliotek** (URL-schema, lagring, metadata, rättigheter).
- Frontend behöver komponenter för preview (iframe/pdf viewer/markdown renderer).
- Backend behöver API:er för listning/hämtning/uppdatering samt start av konverteringsjobb.
- “SharePoint som primär leveransyta” tas bort som antagande i copy och styrdokument.

## Alternativ som övervägdes

- Fortsätta med SharePoint/Teams som primär yta: för hög friktion och begränsad kontroll (preview/sandbox/inloggning).
- “Bara hosta statisk HTML”: fungerar för vissa fall, men saknar redigering + exports och blir svårt att förvalta långsiktigt.
