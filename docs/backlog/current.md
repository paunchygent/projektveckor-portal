---
id: "current-task-log"
title: "Aktuellt arbetslogg"
type: "task-log"
status: "active"
priority: "medium"
created: "2026-02-26"
last_updated: "2026-02-26"
related: []
labels: []
---

## Context

- Doc-as-code-port pågår.

## Worklog

- 2026-02-26: Initierade docs/backlog + docs-contract.
- 2026-02-26: Fixade `pyproject.toml` (PDM/TOML: citerade `:`-scriptkeys och tog bort dublettnyckel).
- 2026-02-26: Aktiverade `forceConsistentCasingInFileNames` i `frontend/tsconfig.json`.
- 2026-02-26: Skapade backlogkedja programme→epic→story→tasks och autogenererat backlog-index (`pdm run index-backlog`).
- 2026-02-26: Lagt synkplan/ref för Skriptoteket + HuleEdu + Docforge (skills + guards).
- 2026-02-26: Vände hosting-modellen: dokument ska hostas på hemmaservern med preview/redigering i portalen + export via Sir Convert a Lot (ADR-0002). Sanerade SharePoint-copy i frontend och styrdokument.
- 2026-02-26: Implementerat första doclib-MVP i backend: självhostad lagring + Markdown→HTML preview (`/d/...`) och admin write via API med Identity introspection (Auth).

## Next Actions

1. Ta fram konkret integrationsbrief för Sir Convert a Lot (API/CLI, jobmodell, format) och skapa adapter-kontrakt i `docs/reference/`.
2. Implementera första slice för dokumentbiblioteket (task-08/09/10) med minimal preview + export.
3. Kör `pdm run check:md` efter att Node/npx är installerat.
