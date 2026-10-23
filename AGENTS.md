# Projektveckor Portal

## Identity

Teacher-first portal for Hulebäcksgymnasiet's project weeks, served at
`projektveckor.hule.education` from Hemma: FastAPI backend, Vue/Vite frontend.
Registered as `projektveckor-portal` / `PROJV`.

## Commands

Run from the repository root.

- Setup and worktrees: `pdm run setup`, `pdm run new-worktree <authority-id>`.
- Docs: `pdm run new-task`, `pdm run new-doc`, `pdm run docs-validate`.
- Validation: `pdm run handoff-validate`, `pdm run skills-validate`,
  `pdm run check`.
- Product: `pdm run dev`, `pdm run frontend:install`, `pdm run frontend:dev`,
  `pdm run frontend:build`.

## Product Facts

- Every project week has a stable, linkable SPA route (`/fn-rollspel/v43`);
  the backend serves the history fallback and `/healthz`.
- Backend: `src/projektveckor_portal/`, Clean Architecture with Dishka DI;
  domain logic stays out of FastAPI routers and IO adapters.
- Hosted documents live under `PVP_DOCS_ROOT` on Hemma; PDF and DOCX exports
  go through Sir Convert-a-Lot v2. Auth reuses HuleEdu Identity.
- Secrets and personal data never enter Git; `.env.example.*` hold key names.

## Local Routes

- Active state: `handoff.md`; durable docs: `docs/index.md`.
- Repo-local skills: `.codex/skills/` (deploy, week entry, docs, hooks, SSH).
- Docs-as-code and backlog: `agent-docs-governance`, reference
  `projektveckor-portal.md`; planning: `agent-planning`.
- Local commands: `local-devops`; Hemma operations: `hemma-devops`.
