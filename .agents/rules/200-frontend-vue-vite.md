---
trigger: model_decision
rule_id: RULE-200
title: Frontend-standard (Vue/Vite)
status: active
created: "2026-02-25"
updated: "2026-02-26"
owners:
  - portal
tags: []
scope: frontend
---

## MUST

- Vue 3 + Vite + TypeScript.
- Stabila rutter för projektveckor (t.ex. `/fn-rollspel/v43`).
- Portalen ska fungera utan SharePoints preview-begränsningar:
  - statisk HTML-export i `frontend/public/...` kan bäddas in via `iframe`.
- Inga inline-stilar i lärar-/export-HTML som vi vill återanvända (använd extern CSS).
