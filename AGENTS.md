# Projektveckor Portal Agent Entrypoint

Projektveckor Portal follows a docs-as-code model inspired by HuleEdu and
Skriptoteket: rules first, stable agent documentation, and repeatable
dev/deploy commands.

## Read Order

1. `docs/index.md`
2. `.agents/readme-first.md`
3. `.agents/rules/000-rule-index.md`
4. `.agents/handoff.md`

## Repo Invariants

- Keep `.agents/readme-first.md` and `.agents/handoff.md` structure stable;
  update content only.
- Prefer updating rules over ad hoc exceptions.
- `.agents/skills/` contains legacy repo-local skills until a governed
  `.codex/` cutover.

## Command Policy

- Backend: `pdm run dev`
- Frontend from repo root: `pdm run frontend:install`,
  `pdm run frontend:dev`, `pdm run frontend:build`
- Docs: `pdm run validate-docs`, `pdm run validate-backlog`, `pdm run check:md`
