---
id: "task-17-inf-r-tunn-agents-md-router-till-skills"
title: "Inför tunn AGENTS.md-router till skills"
type: "task"
status: "proposed"
priority: "high"
created: "2026-04-18"
last_updated: "2026-04-18"
related: []
labels:
  - agents
  - docs-as-code
  - skills
  - governance
---

PR-sized execution unit; may be linked to a story or standalone.

## Objective

Inför HuleEdu-liknande tunn `AGENTS.md`: rootfilen ska vara en kort router för
repoidentitet, hårda regler, skill-routing, docs-auktoritet och validering,
inte bära lång procedurtext.

## PR Scope

- Klassificera nuvarande `AGENTS.md`, `.agents/readme-first.md`,
  `.agents/rules/`, `.agents/skills/`, `docs/reference/` och backlogytor som
  keep, route-to-skill, route-to-reference, route-to-runbook,
  route-to-backlog eller remove.
- Skapa en kompakt skill-router efter HuleEdu-modellen.
- Bestäm om Projektveckor Portal ska få en egen repo-reference i
  `agent-docs-governance`, eller om rootfilen tills vidare ska peka till
  repo-lokala docs-as-code-regler.
- Flytta lång procedur till `.agents/rules/`, `.agents/skills/`,
  `docs/reference/`, `docs/runbooks/` eller backlog.
- Uppdatera `.agents/readme-first.md` och `.agents/handoff.md` bara där de
  pekar på gammalt rootbeteende.

## Deliverables

- [ ] `AGENTS.md` är tunn och routerformad.
- [ ] Docs/backlog governance har en tydlig startpunkt: antingen
      `agent-docs-governance` plus repo-reference eller en uttrycklig lokal
      fallback.
- [ ] Skill-, regel- och docs-ytor har en tydlig ägarordning utan duplicerad
      procedur i root.

## Acceptance Criteria

- [ ] `AGENTS.md` behåller repoidentitet, icke-förhandlingsbara regler,
      skill-router, docs-auktoritet och valideringskommandon.
- [ ] Detaljerad procedur för docs, frontend/backend, auth, Sir Convert-a-Lot,
      handoff och markdown-kvalitet ligger i skills, regler, references,
      runbooks eller backlog.
- [ ] Om `agent-docs-governance` används ska skill-repository få en matchande
      Projektveckor Portal-reference innan rootfilen pekar dit.
- [ ] Validering inkluderar `pdm run validate-docs`,
      `pdm run validate-backlog`, `pdm run validate-skills`,
      `pdm run check:md` och `git diff --check`.

## Checklist

- [ ] Implementation complete
- [ ] Validation complete
- [ ] Docs updated
