---
id: "story-doc-as-code-mvp"
title: "Doc-as-code MVP: kontrakt, backlogkedja och root-kommandon"
type: "story"
status: "in_progress"
priority: "high"
created: "2026-02-26"
last_updated: "2026-02-26"
related:
  - "docs/backlog/epics/epic-doc-as-code-governance.md"
  - "docs/prd/prd-projektveckor-portal-v0.1.md"
labels:
  - "docs-as-code"
---

Implementation slice with acceptance-driven scope.

## Objective

Göra doc-as-code-systemet i `projektveckor-portal` användbart i vardagen: tydlig backloghierarki, validering och root-kommandon som fungerar i en ny checkout.

## Scope

- Backlog: programme→epic→story→task med tydliga länkar.
- PDM-scripts: docs + frontend wrappers från repo-root.
- Indexering av backlog på kontraktskompatibelt sätt.
- Markdown quality tooling (formatter/lint) kopplat till root-kommandon.

## Acceptance Criteria

- [ ] `pdm lock` och `pdm install` fungerar (pyproject är giltig TOML).
- [ ] `pdm run validate-docs` och `pdm run validate-backlog` passerar.
- [ ] Backloggen innehåller minst 1 programme, 1 epic, 1 story och flera PR-slice tasks.

## Test Requirements

- [ ] Kör `pdm run validate-docs`
- [ ] Kör `pdm run validate-backlog`
- [ ] Kör `pdm run index-backlog`

## Done Definition

- Storyn är uppdelad i PR-slice tasks och varje task är “done” eller tydligt planerad.
- AGENTS/rules beskriver hur man jobbar (rules-first, doc-as-code, root-kommandon).

## Checklist

- [ ] Implementation complete
- [ ] Tests and validations complete
- [ ] Docs synchronized
