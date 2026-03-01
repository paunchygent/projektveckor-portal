---
name: hooks
description: >-
  Projektveckor Portal pre-commit and docs-as-code hook workflow (skill frontmatter
  validation and commit-time guardrails).
---

# Hooks Skill

This repo uses pre-commit to enforce deterministic docs-as-code gates.

Canonical entrypoints:

- `pdm run validate-skills`
- `pdm run validate-docs`
- `pdm run validate-backlog`
