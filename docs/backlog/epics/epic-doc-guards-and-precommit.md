---
id: "epic-doc-guards-and-precommit"
title: "Doc-as-code: guards + pre-commit quality gate"
type: "epic"
status: "proposed"
priority: "medium"
created: "2026-02-26"
last_updated: "2026-02-26"
related:
  - "docs/backlog/programmes/programme-projektveckor-portal-v0-1.md"
  - "docs/backlog/epics/epic-doc-as-code-governance.md"
  - "docs/prd/prd-projektveckor-portal-v0.1.md"
labels:
  - "docs-as-code"
  - "quality"
---

Major capability increment managed through linked stories.

## Goal

Höja robustheten i doc-as-code-flödet genom att porta in beprövade “guards” (HuleEdu) och lägga ett enkelt kvalitetsstopp (Skriptoteket/pre-commit) så att fel fångas tidigt.

## In Scope

- Länk-integritet (inkl. tomma länkar) i docs/backlog.
- Top-level allowlist för docs-strukturen.
- Legacy-token guard (stoppar gamla paths/kommandon).
- Pre-commit som kör `validate-docs` + `validate-backlog` (+ ev. markdown checks).

## Out of Scope

- CI/CD-pipeline (senare).

## Stories

1. `docs/backlog/stories/story-port-doc-guards.md`

## Acceptance Criteria

- [ ] Pre-commit kan köras lokalt och stoppar kontraktbrott.
- [ ] Docs/backlog-länkar valideras (broken links/tomma länkar fångas).

## Checklist

- [ ] Stories linked
- [ ] Acceptance criteria defined
- [ ] Execution gate defined
