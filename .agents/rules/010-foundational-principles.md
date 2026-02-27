---
trigger: model_decision
rule_id: RULE-010
title: Grundprinciper
status: active
created: "2026-02-25"
updated: "2026-02-26"
owners:
  - portal
tags: []
scope: all
---

## MUST

- Portalen ska vara lärar- och elevnära: tydlighet > cleverness.
- Föredra stabila URL:er. Innehåll ska kunna länkas i flera år.
- Håll deployment repeterbar: Compose + miljövariabler.
- Lägg inte in hemligheter i git.

## SHOULD

- Minimera rörliga delar: statisk SPA + tunn backend (healthz + static hosting).
- Skriv dokumentation som “source of truth” för arbetsflöden.
