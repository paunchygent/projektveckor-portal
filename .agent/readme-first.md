# Read Me First (Agents)

Use this file as the starting point when you begin a new session.

## Behavioral rules (must follow)

- **Rules-first:** read `.agent/rules/000-rule-index.md` before making structural decisions.
- **Stable agent docs:** keep headings and section order unchanged in `.agent/readme-first.md` and `.agent/handoff.md`.
- **No secrets:** never add API keys/tokens, passwords, or personal data to `.agent/`, `docs/`, or committed config.
- **Prefer canonical commands:** use `pdm run ...` for backend tasks and `pdm run frontend:...` for frontend tasks.

## What this repo is

Projektveckor Portal is a small teacher-first portal for publishing project-week “entrypoints” as a web page:
- hosted on `hule.education`,
- hosting project-week documents on the home server (preview in the web UI + exports to PDF/DOCX via Sir Convert a Lot),
- with a consistent look and easy navigation.

## Read order (mandatory)

1. `docs/index.md`
2. `.agent/rules/000-rule-index.md`
3. `AGENTS.md`
4. `.agent/handoff.md`

## Key commands

- Backend (dev): `pdm run dev`
- Frontend (dev): `pdm run frontend:dev`
- Frontend (build): `pdm run frontend:build`
- Lint: `pdm run lint`
- Tests: `pdm run test`

## Session handoff

Before ending a session, update `.agent/handoff.md` (what changed, decisions, next steps).
