---
type: reference
id: REF-doc-as-code-quickstart
title: Doc-as-code quickstart (Projektveckor Portal)
status: draft
created: "2026-02-26"
updated: "2026-02-26"
owners:
  - portal
tags:
  - docs-as-code
links:
  - docs/_meta/docs-contract.yaml
  - docs/backlog/README.md
---

## Syfte

Snabbguide för hur vi skapar och validerar dokument i repo:t.

## Skapa dokument

- Backlog-item: `pdm run new-task "<titel>"` (eller `new-epic`, `new-story`, `new-review`).
- Doc: `pdm run new-doc <relativ sökväg under docs/>`.
- Regel: `pdm run new-rule "<namn>"`.

## Validera

- `pdm run validate-docs`
- `pdm run validate-backlog`
- `pdm run check:md`
