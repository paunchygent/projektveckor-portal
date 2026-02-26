---
id: "epic-doc-as-code-governance"
title: "Doc-as-code governance (backlog/ADR/PRD/ref) + validering"
type: "epic"
status: "in_progress"
priority: "high"
created: "2026-02-26"
last_updated: "2026-02-26"
related:
  - "docs/backlog/programmes/programme-projektveckor-portal-v0-1.md"
  - "docs/prd/prd-projektveckor-portal-v0.1.md"
labels:
  - "docs-as-code"
  - "governance"
---

Major capability increment managed through linked stories.

## Goal

Införa ett robust, kontraktsdrivet doc-as-code system som stödjer:

- backlog och planning artifacts,
- decisions/ADR,
- PRD,
- references/runbooks/templates,
  med validering och repeterbara root-kommandon.

## In Scope

- Docs-kontrakt + validator.
- Backlog-kontrakt (programme/epic/story/task/fix/review/task-log/reference) + validator.
- Markdown quality: formatter + lint + check.
- Root-kommandon (`pdm run ...`) som kapslar frontend och docs.

## Out of Scope

- Full CI-pipeline (kan komma senare).
- Full “skills library” i Codex (skapas iterativt).

## Stories

1. `docs/backlog/stories/story-doc-as-code-mvp.md`

## Acceptance Criteria

- [ ] `pdm run validate-docs` passerar.
- [ ] `pdm run validate-backlog` passerar.
- [ ] `pdm run check:md` kan köras (förutsätter Node/npx).

## Checklist

- [ ] Stories linked
- [ ] Acceptance criteria defined
- [ ] Execution gate defined
