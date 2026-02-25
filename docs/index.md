# Projektveckor Portal — docs

This repo hosts a small portal for project weeks (e.g. FN-rollspel v.43) on `hule.education`.

## Goals

- One stable “start page” per project week.
- Link into SharePoint resources (PDF/DOCX/folders) using correct URLs.
- Keep styling consistent across weeks.
- Keep week pages as stable SPA routes (e.g. `/fn-rollspel/v43`).

## Architecture (initial)

- FastAPI backend serves:
  - `/healthz` for ops checks
  - built SPA from `frontend/dist` in production
- Vue/Vite frontend is the portal UI.
- Some week content may be included as static HTML exports under `frontend/public/...` (copied into `dist/` at build time)
  and embedded in SPA pages (iframe) to preserve navigation even when SharePoint preview blocks HTML→HTML links.

## Deploy

See `docs/runbooks/runbook-hemma-deploy.md`.

## Dev workflow

- Start backend: `pdm install -G dev` then `pdm run dev`
- Start frontend: `pnpm -C frontend install` then `pnpm -C frontend dev`
