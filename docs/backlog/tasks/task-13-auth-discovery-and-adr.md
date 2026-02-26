---
id: 'task-13-auth-discovery-and-adr'
title: 'Inventera auth i HuleEdu/Skriptoteket och acceptera ADR-0003'
type: 'task'
status: 'proposed'
priority: 'high'
created: '2026-02-26'
last_updated: '2026-02-26'
related:
  - 'docs/backlog/stories/story-auth-mvp.md'
  - 'docs/decisions/0003-auth-integration-huleedu-skriptoteket.md'
labels:
  - 'auth'
  - 'discovery'
---

PR-sized execution unit; may be linked to a story or standalone.

## Objective

Ta fram exakt hur auth görs i HuleEdu/Skriptoteket och dokumentera valet så att portalen kan integrera utan duplicerad boilerplate.

## PR Scope

- Kartlägg: token-typ, headers/cookies, endpoint för login/introspektion, roll-claims.
- Uppdatera ADR-0003 från `proposed` till `accepted` med exakta detaljer.

## Deliverables

- [ ] Uppdaterad ADR-0003 (accepted) + ref med “hur man kör lokalt”.

## Acceptance Criteria

- [ ] Det finns en tydlig, implementerbar integration (ingen “TBD auth” kvar).

## Checklist

- [ ] Implementation complete
- [ ] Validation complete
- [ ] Docs updated

