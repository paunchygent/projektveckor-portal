# AGENTS.md — Projektveckor Portal

This repository follows the same **doc-as-code** operating model as HuleEdu and Skriptoteket:
rules-first, stable agent docs, and repeatable dev/deploy commands.

## Read order (mandatory)

1. `.agents/readme-first.md`
2. `.agents/rules/000-rule-index.md`
3. `.agents/handoff.md` (current session context)

## Non-negotiables

- Do not add secrets (tokens/passwords) anywhere in git.
- Keep `.agents/readme-first.md` and `.agents/handoff.md` **structure stable** (only update content).
- Prefer updating rules over ad-hoc exceptions.
