---
trigger: model_decision
rule_id: RULE-050
title: Python-standard (backend)
status: active
created: "2026-02-25"
updated: "2026-02-26"
owners:
  - portal
tags: []
scope: backend
---

## MUST

- Använd `src/`-layout (`src/projektveckor_portal/...`).
- Använd PDM (`pyproject.toml`) och `pdm run ...`-scripts.
- Ruff-format + lint, line length ≤ 100.
- Håll moduler små (riktlinje: < ~500 LoC). Refaktorera tidigt.

## Arkitektur (backend)

- Följ Clean Architecture/DDD:
  - domän/affärslogik ska vara frikopplad från web/IO,
  - web-lager ska vara tunt (FastAPI routers + mapping),
  - infrastruktur implementerar abstraktioner/protokoll,
  - använd DI för att koppla ihop implementationer.
