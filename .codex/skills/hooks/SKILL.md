---
name: hooks
description: >-
  Projektveckor Portal pre-commit hooks: the shared docs, skills and handoff
  validators that run at commit time, and how to install them.
---

# Hooks Skill

`.pre-commit-config.yaml` runs the shared repository-governance
validators at commit time:

- `pdm run docs-validate` when files under `docs/` change.
- `pdm run skills-validate` when files under `.codex/skills/` change.
- `pdm run handoff-validate` when `handoff.md` changes.

Install the Git hook once per checkout with `pdm run precommit-install`.
Never bypass the hooks; fix the reported failure instead.
