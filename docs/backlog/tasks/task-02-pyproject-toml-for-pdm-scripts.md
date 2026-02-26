---
id: "task-02-pyproject-toml-for-pdm-scripts"
title: "Gör pyproject.toml giltig för PDM scripts (kolon-nycklar)"
type: "task"
status: "completed"
priority: "high"
created: "2026-02-26"
last_updated: "2026-02-26"
related:
  - "docs/backlog/stories/story-doc-as-code-mvp.md"
labels:
  - "pdm"
  - "docs-as-code"
---

PR-sized execution unit; may be linked to a story or standalone.

## Objective

Säkerställa att `pyproject.toml` är giltig TOML för PDM och att scripts med `:` fungerar via citerade nycklar.

## PR Scope

- Citerade keys i `[tool.pdm.scripts]` för `lint:md`, `check:md`, `frontend:dev`, etc.

## Deliverables

- [ ] `pyproject.toml` parse:ar med TOML-parser.
- [ ] `pdm lock` + `pdm install` fungerar.

## Acceptance Criteria

- [ ] PDM kan läsa `pyproject.toml` utan `TOMLDecodeError`.

## Checklist

- [ ] Implementation complete
- [ ] Validation complete
- [ ] Docs updated
