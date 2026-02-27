---
trigger: model_decision
rule_id: RULE-090
title: Dokumentationsstandard (doc-as-code)
status: active
created: "2026-02-25"
updated: "2026-02-26"
owners:
  - portal
tags:
  - docs-as-code
scope: all
---

## Canonical docs

- `docs/index.md` är dokumentationsingång.
- `docs/docs-structure-spec.md` beskriver taxonomin.
- `docs/_meta/docs-contract.yaml` är kontraktet som validerar docs och regler.

## MUST

- Alla nya dokument under `docs/` ska ha YAML-frontmatter enligt kontraktet.
- Backlog används för planering/leverans: `docs/backlog/`.
- Beslut dokumenteras som ADR: `docs/decisions/`.
- Referenser/rapporter/reviews dokumenteras i `docs/reference/`.
- Kör validering före merge:
  - `pdm run validate-docs`
  - `pdm run validate-backlog`
  - `pdm run check:md`

## Agent-dokument

- Håll strukturen stabil i `.agents/readme-first.md` och `.agents/handoff.md` (endast innehåll uppdateras).
