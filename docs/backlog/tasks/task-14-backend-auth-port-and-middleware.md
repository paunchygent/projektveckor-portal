---
id: "task-14-backend-auth-port-and-middleware"
title: "Backend: auth-port + middleware/dependency (HuleEdu/Skriptoteket)"
type: "task"
status: "proposed"
priority: "high"
created: "2026-02-26"
last_updated: "2026-02-26"
related:
  - "docs/backlog/stories/story-auth-mvp.md"
labels:
  - "backend"
  - "auth"
---

PR-sized execution unit; may be linked to a story or standalone.

## Objective

Implementera auth som DIP-kompatibel port/adaptrar så att web-lagret kan kräva roller utan att känna till implementationen.

## PR Scope

- `CurrentUser`-modell (id, roller, display name).
- Dependency för FastAPI som ger `CurrentUser` eller 401.
- Decorator/guard för `teacher`-krav.

## Deliverables

- [ ] Backend kan skydda admin endpoints med teacher-roll.

## Acceptance Criteria

- [ ] Public endpoints är öppna; admin endpoints kräver giltig auth.

## Checklist

- [ ] Implementation complete
- [ ] Validation complete
- [ ] Docs updated
