---
type: spec
id: SPEC-docs-structure
title: Dokumentationsstruktur (doc-as-code)
status: active
created: "2026-02-26"
updated: "2026-02-26"
owners:
  - portal
tags:
  - docs-as-code
links:
  - docs/_meta/docs-contract.yaml
  - scripts/docs_as_code/validate_docs.py
  - scripts/docs_as_code/validate_tasks.py
---

## Syfte

Göra repo:t lätt att vidareutveckla över tid genom att ha en **spårbar** och **validerbar** struktur för planering, beslut och referenser.

## Taxonomi

- `docs/index.md`: dokumentationsingång (mänsklig).
- `docs/runbooks/`: drift- och deployinstruktioner.
- `docs/prd/`: PRD:er (produktkrav och leveranser).
- `docs/decisions/`: ADR/beslut (varför vi gjorde ett val).
- `docs/reference/`: referenser, rapporter, reviews och “hur det funkar”.
- `docs/backlog/`: planering och genomförande (programme → epic → story → task/fix + reviews).
- `docs/templates/`: mallar för ADR/PRD/runbook/referens/review.
- `docs/_meta/`: docs-contract (maskinvalidering).

## Validering (gates)

- `pdm run validate-docs`: validerar att dokument följer docs-kontraktet.
- `pdm run validate-backlog`: validerar att backlog-dokument följer mall/struktur.
- `pdm run check:md`: markdown quality (prettier + markdownlint + extra checks).

## Invariant

- Inga förändringar av produktionsexponerat beteende utan en styrande backlogpunkt och, vid behov, ett beslut (ADR).
