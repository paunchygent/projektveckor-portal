# Skill: docs-as-code (Projektveckor Portal)

Use this skill when you need to create/update documentation, rules, or agent handoffs in this repo.

## Rules-first workflow

1. Read `.agents/rules/000-rule-index.md`.
2. Update the _rule_ that governs the workflow before adding exceptions.
3. Update `.agents/handoff.md` at the end of the session with what changed + next steps.

## Canonical files

- Entry docs: `docs/index.md`
- Agent entry: `.agents/readme-first.md`
- Cross-session: `.agents/handoff.md` (current only; keep structure stable)
- Memory: `.agents/long-term-memory.md` (append-only; keep durable decisions)
