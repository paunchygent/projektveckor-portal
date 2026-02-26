---
id: 'programme-projektveckor-portal-v0-1'
title: 'Projektveckor Portal v0.1'
type: 'programme'
status: 'in_progress'
priority: 'critical'
created: '2026-02-26'
last_updated: '2026-02-26'
related:
  - 'docs/prd/prd-projektveckor-portal-v0.1.md'
labels:
  - 'programme'
  - 'portal'
---

Cross-cutting programme scope and governance are defined here.

## Objective

Etablera en stabil portal för Hulebäcksgymnasiets projektveckor (start: FN-rollspel v.43) med en doc-as-code arbetsmodell som gör att både innehåll och utveckling kan växa utan att tappa styrning.

## Scope

- Publicera “överlämningsinformation” (HTML-struktur med navigation) som webb.
- Göra FN-rollspelsveckan tillgänglig som en interaktiv resursyta (elev + delegation).
- Förbereda för läraryta (inlogg) för bulletin/nyheter och resurshantering.
- Skapa en backlogstruktur (programme→epic→story→task) kopplad till PRD.

## Delivery Model

- PR-slice: varje `task` är PR-stor (helst 1–3 dagar).
- Doc-as-code först: PRD/ADR/backlog/ref/runbooks är normativt.
- DDD/Clean: backend är tunn och beroende på abstraktioner (DIP/DI).

## Active Epics

1. `docs/backlog/epics/epic-doc-as-code-governance.md`
2. `docs/backlog/epics/epic-fn-rollspel-v43-portal-mvp.md`

## Acceptance Criteria

- [ ] Portalen har stabila URL:er per projektvecka.
- [ ] Backlogkedjan (programme→epic→story→task) är etablerad och valideras.
- [ ] FN-rollspel v.43 är publicerad med fungerande navigation.

## Checklist

- [ ] Programme scaffold created
- [ ] Linked epics and stories
- [ ] Governance checkpoints defined
