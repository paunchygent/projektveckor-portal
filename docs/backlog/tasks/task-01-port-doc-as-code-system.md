---
id: "task-01-port-doc-as-code-system"
title: "Porta doc-as-code (backlog/decisions/reference/prd) + validering"
type: "task"
status: "in_progress"
priority: "high"
created: "2026-02-26"
last_updated: "2026-02-26"
related:
  - "docs/docs-structure-spec.md"
  - "docs/_meta/docs-contract.yaml"
labels:
  - "docs-as-code"
---

## Objective

Införa ett tydligt doc-as-code-system i `projektveckor-portal` (struktur + mallar + validering + markdown quality).

## PR Scope

- Skapa docs-taxonomi: backlog, decisions (ADR), reference, prd, runbooks, _meta.
- Porta valideringsscript och koppla in PDM-kommandon.
- Porta markdown formatter/lint (prettier + markdownlint) från Docforge.
- Uppdatera `AGENTS.md` så att arkitekturprinciper och doc-as-code är normativt.

## Deliverables

- [ ] `docs/_meta/docs-contract.yaml` + validator
- [ ] `docs/backlog/` (minst `README.md` + `current.md`)
- [ ] `docs/prd/` (minst en PRD)
- [ ] `docs/decisions/` (minst en ADR)
- [ ] `docs/reference/` (minst en referens)
- [ ] PDM-scripts för `validate-docs`, `validate-backlog`, `check:md`, samt frontend-kommandon från repo-root

## Acceptance Criteria

- [ ] `pdm run validate-docs` passerar
- [ ] `pdm run validate-backlog` passerar
- [ ] `pdm run check:md` kör och rapporterar fel korrekt

## Checklist

- [ ] Implementation complete
- [ ] Validation complete
- [ ] Docs updated
