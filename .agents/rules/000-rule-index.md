---
trigger: model_decision
rule_id: RULE-000
title: Projektveckor Portal — Regelindex
status: active
created: "2026-02-25"
updated: "2026-02-26"
owners:
  - portal
tags:
  - rules
scope: all
---

## Syfte

Reglerna i `.agents/rules/` är normativt “source of truth” för hur vi bygger och underhåller Projektveckor Portal.

## Regler

- `010-foundational-principles.md`: grundprinciper (stabilitet, enkelhet, lärarfokus).
- `050-python-standards.md`: backend-standard (PDM, ruff, typing, SRP).
- `090-documentation-standards.md`: doc-as-code (backlog/ADR/PRD/ref + validering).
- `200-frontend-vue-vite.md`: frontend-standard (Vue/Vite, stabila rutter, iframe-strategi för HTML-exporter).
- `060-docker-and-compose.md`: docker/compose standard.
- `080-home-server-deployment.md`: hemma/hule.education deploy.
