---
type: reference
id: REF-synk-port-plan-docs-skills
title: "Synk/port-plan: Skriptoteket + HuleEdu + Docforge (skills + doc-as-code)"
status: draft
created: "2026-02-26"
updated: "2026-02-26"
owners:
  - portal
tags:
  - docs-as-code
  - docforge
  - huleedu
  - skills
  - skriptoteket
links:
  - docs/index.md
  - docs/_meta/docs-contract.yaml
  - docs/reference/ref-doc-as-code-quickstart.md
  - scripts/docs_as_code/validate_docs.py
  - scripts/docs_as_code/validate_tasks.py
  - docforge/TASKS/content/fn_rollspel/fn-rollspel-v43-ht25-sharepoint-html-portal.md
  - docforge/TASKS/content/fn_rollspel/fn-rollspel-v43-ht25-overlamning.md
---

## Syfte

- Beskriva hur vi synkar/portar arbetssätt mellan **Skriptoteket**, **HuleEdu** och **Docforge** in i `projektveckor-portal`.
- Vara “karta” för var logik bor (skills vs repo-scripts vs docs) och hur den blir stabil över tid.

## Sammanfattning

- **Docforge** producerar innehållsunderlag (TASKS) och ibland HTML-exporter som kan hostas i portalen.
- **Projektveckor Portal** hostar stabila veck-sidor (SPA-rutter) och kan bädda in statiska HTML-exporter via `iframe`.
- **Skriptoteket-stilen** i detta repo: repeterbara `pdm run ...`-kommandon som kapslar både Python- och frontend-flöden.
- **HuleEdu-stilen** i detta repo: rules-first + doc-as-code-kontrakt som valideras i CI/innan merge.

## Principer (source of truth)

- Doc-as-code **kontrakt**: `docs/_meta/docs-contract.yaml` (styr frontmatter, filnamn, status-ordlista).
- Doc-as-code **validering**: `pdm run validate-docs` och `pdm run validate-backlog`.
- Publicerad portal-UX (stabila rutter + iframe-strategi): frontend-koden är “source of truth” för hur innehåll faktiskt visas.
- Docforge TASKS är “source of truth” för **varför** HTML-portalen finns (historiska SharePoint-constraints) och vad som levereras.

## Port/synk: ansvar och riktning

- **Upstream (idéer/mönster)**: Skriptoteket/HuleEdu/Docforge.
- **Downstream (implementerad stabilitet)**: `scripts/` + `docs/` + `frontend/` i detta repo.
- Porta hellre som små, tydliga moduler än “mega-script” (SRP; håll filer korta).
- Dokumentera portade beteenden som:
  - ref (hur det funkar) i `docs/reference/`
  - ADR i `docs/decisions/` när vi gör ett irreversibelt/konsekvent val

## Flöde: Docforge → HTML-portal → Projektveckor Portal

- Skapa/uppdatera Docforge TASKS som beskriver innehållet och constraints.
- När HTML behövs: exportera statiskt (Docforge) och “vendra” in i repo:t:
  - Källfiler i repo: `frontend/public/fn-rollspel/v43/portal/`
- Exponera som stabil sida/rutt i SPA:
  - Inbäddning (iframe): `frontend/src/pages/FnRollspelV43Page.vue`
- Dokument och resurser ska hostas på hemmaservern och kunna previewas i portalen.

## Flöde: Skills → Skriptoteket → PDM-scripts

- Använd “skills” för att snabbt prova ett arbetsflöde (t.ex. ny doc-typ, ny validator, ny scaffolding).
- När flödet är stabilt: porta det till repo som script + PDM entrypoint:
  - Doc-as-code-logik: `scripts/docs_as_code/` (körs via `pdm run new-doc`, `pdm run validate-docs`, osv.).
  - Markdown quality (Docforge-stil): `scripts/maintenance/markdown_quality.py` (körs via `pdm run check:md`, osv.).
  - Frontend-kommandon (Skriptoteket-stil): `pdm run frontend:*` (kör från repo-root, kapslar `pnpm -C frontend ...`).
- Dokumentera “hur man använder det” i `docs/reference/` så att skillen kan vara tunn (eller försvinna helt).

## Docforge TASKS (HTML-portalen)

- `docforge/TASKS/content/fn_rollspel/fn-rollspel-v43-ht25-sharepoint-html-portal.md`
  - Syfte: motivera varför vi hostar en separat HTML-portal (SharePoint-förhandsvisning/sandbox bröt intern HTML-navigation i experiment).
- `docforge/TASKS/content/fn_rollspel/fn-rollspel-v43-ht25-overlamning.md`
  - Syfte: definiera överlämningspaketet/strukturen (oavsett leveransyta).

## Kontrakt och gates

- Frontmatter + filnamn måste följa kontraktet: `pdm run validate-docs`.
- Backlog måste följa backlog-regler och indexeras: `pdm run validate-backlog` (+ ev. `pdm run index-backlog`).
- Markdown quality hålls “Docforge-ren”: `pdm run check:md` (format + lint + extra checks).

## Checklista (när vi portar något)

- Skriv först: “vad är source of truth?” (doc/task vs kod vs extern leveransyta).
- Få det repeterbart: ett `pdm run ...`-kommando med tydlig output.
- Lägg till docs-stöd: ref (och ev. ADR) + länka från relevant docs-ingång.
- Kör gates lokalt: `pdm run validate-docs`, `pdm run validate-backlog`, `pdm run check:md`.

## Rekommendationer / nästa steg

- Lägg en ADR om vi ska ha en standard för “vendrade” Docforge-exporter (naming, mapstruktur, uppdateringsprocess).
- Lägg en ref som beskriver “portal-content lifecycle” per projektvecka (Docforge → hule.education → exports via Sir Convert a Lot).
