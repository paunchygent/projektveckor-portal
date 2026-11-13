---
id: "task-15-frontend-login-flow"
title: "Frontend: login/logout och admin-nav (integrerat auth-flöde)"
type: "task"
status: "proposed"
priority: "medium"
created: "2026-02-26"
last_updated: "2026-02-26"
related:
  - "docs/backlog/stories/story-auth-mvp.md"
labels:
  - "frontend"
  - "auth"
---

PR-sized execution unit; may be linked to a story or standalone.

## Objective

Göra auth-flödet användbart i UI: lärare kan logga in och nå admin-sidor, elever ser bara public innehåll.

## PR Scope

- UI-komponent(er) för inloggningsstatus.
- Redirect/route guard för admin-rutter.
- Minimal felhantering (401/403 → “du behöver logga in”).

## Deliverables

- [ ] Login/logout syns i UI och admin-sidor går inte att nå utan auth.

## Acceptance Criteria

- [ ] En lärare kan nå redigerings- och exportfunktioner efter login.

## Checklist

- [ ] Implementation complete
- [ ] Validation complete
- [ ] Docs updated
