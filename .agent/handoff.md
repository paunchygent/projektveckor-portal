# Handoff (keep structure stable)

## Snapshot

- Repo: `projektveckor-portal`
- Target: `hule.education` (home server)
- Stack: FastAPI (Python/PDM) + Vue/Vite (pnpm)

## What changed in this session

- Frontend: added Vue Router and real portal pages:
  - `/` home page with internal navigation
  - `/fn-rollspel/v43` FN-rollspel v43 page (tabs + embedded HTML portal)
  - `/fn-rollspel/v43/schema` embedded schema
  - `/fn-rollspel/v43/bokningsinfo` embedded booking info
  - `404` not found page
- Frontend: svenskare UI-copy:
  - `healthz`-länk bytt till “Driftstatus”
  - små språkjusteringar (“Portalen”, “portalsida”, etc.)
- FN-rollspel v43: imported Docforge HTML export into the repo:
  - Static HTML: `frontend/public/fn-rollspel/v43/portal/`
  - Embedded via iframe in the SPA routes above
- Docs-as-code: införde styrande dokumentstruktur + validering:
  - Docs-kontrakt: `docs/_meta/docs-contract.yaml`
  - Backlog-yta: `docs/backlog/` (+ `current.md`)
  - PRD/ADR/Reference: `docs/prd/`, `docs/decisions/`, `docs/reference/`
  - Mallar: `docs/templates/`
  - Valideringsscript + scaffolding: `scripts/docs_as_code/`
  - Markdown quality (prettier + markdownlint): `scripts/maintenance/` + repo-root configs
- Agent/rules: uppdaterade `.agent/rules/*.md` till kontraktsformat (frontmatter + inga H1-rubriker).
- PDM/TOML: fixade `pyproject.toml` så PDM kan läsa scripts med `:` (citerade nycklar) och tog bort dublett-nyckel som gav `TOMLDecodeError`.
- Frontend/TS: aktiverade `forceConsistentCasingInFileNames` i `frontend/tsconfig.json`.
- Backlog: skapade programme→epic→story→task-kedja och backlog-index (`docs/backlog/README-index.md` via `pdm run index-backlog`).
- Reference: lagt synkplan för hur Skriptoteket + HuleEdu + Docforge används för skills och doc-as-code: `docs/reference/ref-synkplan-skriptoteket-huleedu-docforge.md`.
- Arkitektur: vände dokumentantagandet till självhostat dokumentbibliotek med preview/redigering i portalen och exports via Sir Convert a Lot (ADR-0002).
- Backend: införde första doclib-MVP (Markdown→HTML preview + admin write) med självhostad lagring under `PVP_DOCS_ROOT`:
  - Public preview: `/d/<doc_path>` (HTML)
  - API: `/api/documents` (list/get), `/api/admin/documents/<doc_path>` (put; teacher-only)
- Auth: påbörjad integration via HuleEdu Identity introspection (`PVP_IDENTITY_INTROSPECT_URL`) för teacher-only admin (ADR-0003).
- Tooling: fixade PEP517-build backend (`pdm-backend`) och ignorerar `*.egg-info/` (rensade `src/projektveckor_portal.egg-info`).
- Frontend deps: installerade via pnpm och verifierade `frontend:typecheck` + `frontend:build` från repo-root.
- Doclib smoke test: seedade exempel-dokument under `data/doclib/fn-rollspel/v43/borja-har/` och verifierade:
  - listning: `GET /api/documents?prefix=fn-rollspel/v43`
  - preview: `GET /d/fn-rollspel/v43/borja-har` (Markdown → HTML)
- Auth (cookie+CSRF, Skriptoteket-stil): införde portalens tunna BFF-yta mot HuleEdu Identity:
  - `POST /api/v1/auth/login` (sätter httpOnly cookies + CSRF-cookie)
  - `GET /api/v1/auth/me` (introspection + refresh vid behov)
  - `GET /api/v1/auth/csrf` (säkerställer CSRF-cookie)
  - `POST /api/v1/auth/logout` (kräver `X-CSRF-Token`)
- Frontend auth: lade till Pinia + `/login`-vy som använder cookie+CSRF mot API (`frontend/src/stores/auth.ts` + `frontend/src/api/client.ts`).
- Export (task-10 slice): teacher-only export-API via Sir Convert a Lot v2:
  - `POST /api/admin/documents/{doc_path}/exports` (kräver inloggning + CSRF)
  - `GET /api/admin/exports/{export_id}`
  - `GET /api/admin/exports/{export_id}/artifact`
- DI: migrerade runtime-DI till Dishka (bort från `request.app.state`/service locator) och kopplade routes via `DishkaRoute` + `FromDishka`: `src/projektveckor_portal/di/container.py` (migrationsplanen finns kvar i `docs/reference/ref-dishka-migration-plan.md`).
- Ops: lade till SSH-runbook + repo-local skill för `ssh hemma` i Windows/WSL: `docs/runbooks/runbook-ssh-hemma-windows-wsl.md` + `.agent/.codex/skills/projektveckor-ssh-hemma-windows-wsl/`.

## Decisions

- Keep week pages as stable, linkable SPA routes (backend already provides history fallback).
- Default production hostname remains `projektveckor.hule.education` via nginx-proxy env vars.
- Portalen använder doc-as-code som normativt arbetssätt (backlog/ADR/PRD/ref + kontraktvalidering).
- Repo-root PDM-scripts kapslar frontend-kommandon (Skriptoteket-stil): `pdm run frontend:*`.
- ADR-0002: dokument hostas på hemmaservern och preview/redigering sker i portalen; exports skapas via Sir Convert a Lot.
- ADR-0003 (accepted): AuthN/AuthZ återanvänds från HuleEdu/Skriptoteket; kort sikt via portalens tunna BFF (/login + cookies + CSRF), lång sikt via gemensam login och redan satta cookies.
- Docforge (historik): SharePoint-preview begränsade HTML→HTML-navigation; hostad portal var robust fallback (se Docforge task `TASKS/content/fn_rollspel/fn-rollspel-v43-ht25-sharepoint-html-portal.md`).

## Next steps

- Expand FN-rollspel v43 content with the real “dag-för-dag” + roles once the source doc is ready to copy into portal text.
- Add next weeks/pages using same routing pattern.
- Decide if v43 should stay as embedded static HTML export (current) or be converted to native Vue content.
- Implementera dokumentbibliotek-MVP enligt epic/story i `docs/backlog/` (preview/redigering/export).
- Slutför auth discovery (HuleEdu/Skriptoteket) och acceptera ADR-0003 med exakt modell (JWT/OIDC/gateway).
- Implementera exportflöde (Sir Convert a Lot v2) + lagring under `PVP_EXPORTS_ROOT`.
- Om `node`/`pnpm` inte hittas i PATH på devmaskinen: lägg till `C:\Program Files\nodejs\` och `%APPDATA%\npm\` i PATH (krävs för `pdm run frontend:*`).
- Dra upp första admin-sidan i frontend (doc-editor + exportknappar) kopplad till export-endpoints.
- Påbörja Dishka-migrering steg 1–2 enligt referensen (container + FastAPI-integration, men bibehåll beteende).
- Kör lokalt (prioriterad ordning):
  - `pdm lock` + `pdm install`
  - `pdm run validate-docs` + `pdm run validate-backlog`
  - installera Node + pnpm om det saknas och kör `pdm run frontend:install`
  - `pdm run frontend:typecheck`
  - `pdm run check:md` (kräver Node/npx)
- Skapa nya PR-slice tasks för:
  - port av HuleEdu “guards” (länk-integritet, allowlist, legacy-token guard, rule-surface authority),
  - ev. pre-commit gate (Skriptoteket-mönster),
  - skapande av Codex-skills enligt synkplanen.

## Links / references

- Frontend routes: `frontend/src/router.ts`
- Deploy pattern: `compose.prod.yaml` (nginx-proxy `VIRTUAL_HOST` + `LETSENCRYPT_HOST`)
- Docforge export source (local path on dev machine): `docforge/local_exports/..._html_portal/`
- Docs entrypoint: `docs/index.md`
- Docs structure spec: `docs/docs-structure-spec.md`
- Synkplan (skills + guards): `docs/reference/ref-synkplan-skriptoteket-huleedu-docforge.md`
