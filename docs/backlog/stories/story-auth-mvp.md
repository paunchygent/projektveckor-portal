---
id: "story-auth-mvp"
title: "Auth MVP: teacher-only admin via HuleEdu/Skriptoteket (ingen hardcoded auth)"
type: "story"
status: "proposed"
priority: "high"
created: "2026-02-26"
last_updated: "2026-02-26"
related:
  - "docs/backlog/epics/epic-auth-integration.md"
  - "docs/decisions/0003-auth-integration-huleedu-skriptoteket.md"
labels:
  - "auth"
---

Implementation slice with acceptance-driven scope.

## Objective

Få en första fungerande inloggning/auktorisering för lärarytan som använder samma auth-mekanism som HuleEdu/Skriptoteket.

## Scope

- Välj integrationsmodell (JWT/OIDC verifiering, gateway headers eller introspektion).
- Backend: auth dependency/middleware + roll-check.
- Frontend: enkel “Logga in”/“Logga ut”/redirect enligt vald modell.

## Acceptance Criteria

- [ ] Admin-endpoints returnerar `401/403` utan giltig auth.
- [ ] Teacher-roll krävs för update/export.
- [ ] Inget “hardcoded admin-key”-system finns i portalen.

## Test Requirements

- [ ] Enhetstester för auth dependency (mockad provider).
- [ ] Manuell test: public route utan login, admin route med login.

## Done Definition

- ADR-0003 är uppdaterad till `accepted` med exakt modell beskriven.

## Checklist

- [ ] Implementation complete
- [ ] Tests and validations complete
- [ ] Docs synchronized
