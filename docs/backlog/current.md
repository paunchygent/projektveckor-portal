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
- 2026-02-26: Auth: bytte till cookie+CSRF (Skriptoteket-stil) med `/api/v1/auth/*` och `/login`-vy i frontend. ADR-0003 satt till accepted.
- 2026-02-26: Exports: implementerade första slice för `task-10` (teacher-only export-API via Sir Convert a Lot v2 + lagring under `data/exports`).
- 2026-02-26: DI: lade referens för Dishka-migrering (plan utan runtime-ändring).

## Next Actions

1. Koppla portalen mot riktiga tjänster i dev/prod:
   - sätt `PVP_IDENTITY_BASE_URL` + `PVP_IDENTITY_INTROSPECT_URL`
   - sätt `PVP_SIR_CONVERT_A_LOT_*` och verifiera PDF/DOCX-export end-to-end.
2. Implementera `task-12` i frontend: doc-editor + export-knappar + statuspolling (baserat på `/api/admin/exports/...`).
3. Förbättra roll-gränser: teacher-only för redigering/export, admin-only för framtida no-code/konfiguration.
4. Starta Dishka-migrering steg 1 (container + wiring i composition root) utan att ändra externt beteende.
