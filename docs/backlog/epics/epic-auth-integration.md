---
id: 'epic-auth-integration'
title: 'Auth-integration: återanvänd HuleEdu/Skriptoteket för lärarytan'
type: 'epic'
status: 'proposed'
priority: 'high'
created: '2026-02-26'
last_updated: '2026-02-26'
related:
  - 'docs/backlog/programmes/programme-projektveckor-portal-v0-1.md'
  - 'docs/decisions/0003-auth-integration-huleedu-skriptoteket.md'
labels:
  - 'auth'
---
Major capability increment managed through linked stories.

## Goal

Införa autentisering/auktorisering för lärarytan utan att duplicera hardcoded auth-logik i portalen, genom att återanvända HuleEdu/Skriptoteket.

## In Scope

- Inventera befintlig auth i HuleEdu/Skriptoteket.
- Välja integrationsmodell och acceptera ADR-0003.
- Implementera minimal auth-gate för admin-rutter (teacher-only).

## Out of Scope

- Fullständig användaradmin i portalen.
- Finkorniga behörigheter (starta med roller).

## Stories

1. `docs/backlog/stories/story-auth-mvp.md`

## Acceptance Criteria

- [ ] Admin-rutter kräver inloggning och teacher-roll.
- [ ] Publika rutter är fortsatt öppna.

## Checklist

- [ ] Stories linked
- [ ] Acceptance criteria defined
- [ ] Execution gate defined
