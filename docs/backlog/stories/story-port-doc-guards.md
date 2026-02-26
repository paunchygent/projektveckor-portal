---
id: 'story-port-doc-guards'
title: 'Porta HuleEdu guards + pre-commit gate (docs/backlog)'
type: 'story'
status: 'proposed'
priority: 'medium'
created: '2026-02-26'
last_updated: '2026-02-26'
related:
  - 'docs/backlog/epics/epic-doc-guards-and-precommit.md'
labels:
  - 'docs-as-code'
  - 'quality'
---

Implementation slice with acceptance-driven scope.

## Objective

Införa extra validering (“guards”) och ett lokalt kvalitetsstopp så att doc-as-code inte degraderas över tid.

## Scope

- Ny validator eller utökning av befintlig `validate_docs.py` för:
  - länk-integritet,
  - allowlist,
  - legacy-token guard.
- Pre-commit som kör de nya validatorerna.

## Acceptance Criteria

- [ ] `pre-commit run --all-files` stoppar kontraktbrott.
- [ ] Broken links i `docs/` ger tydliga felmeddelanden.

## Test Requirements

- [ ] Kör `pdm run validate-docs`
- [ ] Kör `pdm run validate-backlog`
- [ ] Kör `pre-commit run --all-files`

## Done Definition

- Guards är dokumenterade i `docs/reference/` eller `.agent/rules/`.

## Checklist

- [ ] Implementation complete
- [ ] Tests and validations complete
- [ ] Docs synchronized

