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
- 2026-02-26: Tooling: lade till PEP517-build backend (`pdm-backend`) och ignorerar `*.egg-info/` (rensade `src/projektveckor_portal.egg-info`).
- 2026-02-26: Frontend: installerade pnpm-deps och verifierade `frontend:typecheck` + `frontend:build`.
- 2026-02-26: Doclib: seedade exempel-dokument under `data/doclib/fn-rollspel/v43/borja-har/` och verifierade listning + preview.
- 2026-02-26: Markdown quality: fixade `check:md`-körning på Windows och exkluderade `.tools/` från markdownlint.

## Next Actions

1. Ta fram konkret integrationsbrief för Sir Convert a Lot (API/CLI, jobmodell, format) och skapa adapter-kontrakt i `docs/reference/`.
2. Implementera första slice för exportflödet (task-10 + API-route) och lagring under `PVP_EXPORTS_ROOT`.
3. Slutför auth discovery och acceptera ADR-0003 (exakt modell för JWT/OIDC/introspection + roller).
