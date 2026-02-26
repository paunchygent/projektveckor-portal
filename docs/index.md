---
type: spec
id: SPEC-projektveckor-portal-docs
title: Projektveckor Portal — dokumentation
status: active
created: "2026-02-26"
updated: "2026-02-26"
owners:
  - portal
tags:
  - docs-as-code
links:
  - docs/docs-structure-spec.md
  - docs/backlog/README.md
  - docs/runbooks/runbook-hemma-deploy.md
---

Det här repot bygger **Projektveckor Portal**: en webbportal för **Hulebäcksgymnasiets projektveckor** som hostas på `hule.education`.

Huvudfokus är att göra **FN-rollspelsveckan** (förberedelsevecka + själva FN-rollspelet) tillgänglig som en samlad, interaktiv resurs för elever och delegationer — och samtidigt ge lärare en separat yta för publicering och administration.

## Målbild

- **En stabil startpunkt per projektvecka** (länkbar URL) som elever/lärare kan återkomma till.
- **Allt material på rätt ställe**: dokument och resurser **hostas på hemmaservern** och kan förhandsvisas direkt i portalen.
- **Interaktiv resurs** för FN-rollspelet: regler, roller, förhandlingsstöd, mallar (t.ex. resolutioner och policydokument).
- **Två delar i samma portal**:
  - **Elev-/delegationsdel**: navigation + resurser + “hjälp för att göra rätt”.
  - **Lärardel (inloggning)**: bulletin/nyhetsflöde under spelet samt möjlighet att lägga till/uppdatera nedladdningsbara resurser.
- På sikt: stöd för fler projektveckor (t.ex. “Stockholmsveckan”) med samma mönster.

## Arkitektur (nuvarande)

- **Backend (FastAPI)** serverar:
  - `/healthz` för driftscheck
  - byggd SPA från `frontend/dist` i produktion
- **Frontend (Vue/Vite)** är portalens UI med stabila rutter (t.ex. `/fn-rollspel/v43`).
- **Statisk HTML-portal (v43)** finns redan i repot och bäddas in via `iframe`:
  - Källfiler: `frontend/public/fn-rollspel/v43/portal/`
  - Inbäddning: `frontend/src/pages/FnRollspelV43Page.vue`

Det här upplägget gör att intern navigation (HTML→HTML) fungerar i webbläsaren även när externa “preview”-miljöer skulle begränsa navigation.

## Innehållspipeline (Docforge → Portal + konvertering)

Docforge är historiskt “source of truth” för **varför** HTML-portalen finns och vilka constraints som identifierades i SharePoint-preview.

- Syfte och constraint (SharePoint vs hostad portal):
  - `docforge/TASKS/content/fn_rollspel/fn-rollspel-v43-ht25-sharepoint-html-portal.md`
- Överlämningspaket och struktur (överlämningens innehåll/ordning):
  - `docforge/TASKS/content/fn_rollspel/fn-rollspel-v43-ht25-overlamning.md`

Praktiskt arbetsflöde:

1. Skapa/uppdatera innehåll i Docforge (task + export/HTML vid behov).
2. Kopiera in statiska HTML-exporter till `frontend/public/<projektvecka>/...` när de ska hostas här.
3. Exponera dem som stabila SPA-rutter (och/eller iframe-inbäddning) i frontend.
4. Hostade dokument ska:
   - gå att förhandsvisa i portalen, och
   - kunna konverteras till PDF/DOCX via Sir Convert a Lot (för nedladdning/utskrift).
   - se integrationsref: `docs/reference/ref-sir-convert-a-lot-integration.md`

## Deploy

Se `docs/runbooks/runbook-hemma-deploy.md`.

## Dev workflow

- Starta backend: `pdm install -G dev` och sedan `pdm run dev`
- Starta frontend: `pdm run frontend:install` och sedan `pdm run frontend:dev`
