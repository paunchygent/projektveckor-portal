---
trigger: model_decision
rule_id: RULE-080
title: Deploy på hemma (hule.education)
status: active
created: "2026-02-25"
updated: "2026-02-26"
owners:
  - portal
tags: []
scope: ops
---

## MUST

- Produktion hostas på `hule.education` (hemma).
- Verifiera alltid:
  - `GET /healthz` = 200
  - startsidan laddar på hosten

## Runbook

- Se `docs/runbooks/runbook-hemma-deploy.md`.
