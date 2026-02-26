---
type: decision
id: ADR-0001
title: Doc-as-code som styrande governance för Projektveckor Portal
status: proposed
created: "2026-02-26"
updated: "2026-02-26"
owners:
  - portal
tags:
  - docs-as-code
links:
  - docs/docs-structure-spec.md
  - docs/_meta/docs-contract.yaml
---

## Kontext

Projektveckor Portal kommer växa över tid (fler projektveckor, fler resurser, fler användarflöden). Utan en tydlig struktur riskerar dokumentation och beslut att drifta.

## Beslut

Vi inför doc-as-code som normativt arbetssätt:

- Backlog för planering och genomförande (`docs/backlog/`).
- ADR för beslut (`docs/decisions/`).
- Referensytor för rapporter/reviews (`docs/reference/`).
- PRD för produktkrav (`docs/prd/`).
- Maskinvalidering via kontrakt (`docs/_meta/docs-contract.yaml`).

## Konsekvenser

- Alla nya dokument ska ha YAML-frontmatter.
- Validering ska köras lokalt/CI innan merge.
