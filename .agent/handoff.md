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
- FN-rollspel v43: imported Docforge SharePoint-HTML export into the repo:
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

## Decisions

- Keep week pages as stable, linkable SPA routes (backend already provides history fallback).
- Default production hostname remains `projektveckor.hule.education` via nginx-proxy env vars.
- Portalen använder doc-as-code som normativt arbetssätt (backlog/ADR/PRD/ref + kontraktvalidering).
- Repo-root PDM-scripts kapslar frontend-kommandon (Skriptoteket-stil): `pdm run frontend:*`.

## Next steps

- Expand FN-rollspel v43 content with the real “dag-för-dag” + roles once the source doc is ready to copy into portal text.
- Add next weeks/pages using same routing pattern.
- Decide if v43 should stay as embedded static HTML export (current) or be converted to native Vue content.
- Kör lokalt:
  - `pdm install -G dev` (uppdaterar venv efter nya dev-deps/scriptytor)
  - `pdm run validate-docs` + `pdm run validate-backlog`
  - installera Node/pnpm om det saknas och kör `pdm run frontend:install`
  - `pdm run check:md` (kräver Node/npx)

## Links / references

- Frontend routes: `frontend/src/router.ts`
- Deploy pattern: `compose.prod.yaml` (nginx-proxy `VIRTUAL_HOST` + `LETSENCRYPT_HOST`)
- Docforge export source (local path on dev machine): `docforge/local_exports/..._html_portal/`
- Docs entrypoint: `docs/index.md`
- Docs structure spec: `docs/docs-structure-spec.md`
