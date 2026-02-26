---
type: reference
id: REF-synkplan-skriptoteket-huleedu-docforge
title: "Synkplan: Skriptoteket + HuleEdu + Docforge → skills och doc-as-code"
status: draft
created: "2026-02-26"
updated: "2026-02-26"
owners:
  - portal
tags:
  - docs-as-code
  - skills
  - synkplan
links:
  - docs/prd/prd-projektveckor-portal-v0.1.md
  - docs/_meta/docs-contract.yaml
---

## Syfte

Använd Skriptoteket, HuleEdu (inkl. Sir-Convert-a-Lot) och Docforge som “källrepos” för att:

1. etablera ett robust doc-as-code arbetssätt i `projektveckor-portal`, och
2. skapa återanvändbara Codex-skills som gör arbetsflödena repeterbara (content-import, validering, backlog, release).

## Input från Skriptoteket (mönster att adoptera)

- **Docs-kontrakt + validator som gate:** `docs/_meta/docs-contract.yaml` + `scripts/validate_docs.py`.
- **Backlog-nivåer:** epic/story/sprint/pr/review (PR-slices som egna artefakter).
- **Process-referenser:** sprint planning + review workflow under `docs/reference/`.
- **Pre-commit som kvalitetsport:** `.pre-commit-config.yaml` kör docs-validate + övriga checks.

Konsekvens för portalen:

- Inför en “one command”-gate (t.ex. `pdm run lint`) som kör `validate-docs` + `validate-backlog` (+ ev. `check:md`) utöver ruff.
- Lägg process-dokument i `docs/reference/` så planering och reviews blir konsekventa.

## Input från HuleEdu (guards som höjer robusthet)

Högst värde att cherry-picka in ovanpå nuvarande Sir-Convert-a-Lot-lika setup:

- **Top-level allowlist** för docs (stoppar oavsiktliga mappar/filer).
- **Länk-integritet** (inkl. tomma länkar) i docs/backlog.
- **Legacy-token guard** (stoppar gamla paths/kommandon som “lever kvar”).
- **Rule-surface authority guard** (reglerna är normativ yta; ingen “shadow policy”).

Praktiska källor i HuleEdu:

- `scripts/docs_mgmt/contracts/docs_contract_v2.yaml`
- `scripts/docs_mgmt/validators/*`
- `scripts/backlog_mgmt/*` (om vi vill ha striktare backlog-index/arkiv)

## Input från Docforge (varför HTML finns och när det används)

I repo `docforge` finns tasks som beskriver syftet med HTML-portalen och den historiska SharePoint-preview-constrainten:

- `TASKS/content/fn_rollspel/fn-rollspel-v43-ht25-sharepoint-html-portal.md`
  - HTML som “startpunkt” i SharePoint (experiment), men navigation mellan HTML-sidor fallerade i SharePoint-preview → hostad portal på `hule.education` är robust.
- `TASKS/content/fn_rollspel/fn-rollspel-v43-ht25-overlamning.md`
  - HTML-templates under `handout_templates/` är källor för att kunna regenerera PDF/DOCX enhetligt och fungera i överlämningspaket.
- `TASKS/001-html-to-pdf-setup.md`
  - Repo-målbild: förvalta HTML-templates + CSS-pipeline och automatisera konvertering (WeasyPrint/Pandoc) till PDF/DOCX.

Konsekvens för portalen:

- Håll “HTML-export som portal” som separat leveransartefakt under `frontend/public/...` (publicering), och håll “HTML som källa för PDF/DOCX” i Docforge/Sir-Convert-a-Lot (produktion).

## Förslag: skill-katalog (vad vi vill automatisera)

Skapa (minst) följande skills i Codex, med repo-root som canonical CWD:

1. **`docs:validate`** — kör `validate-docs` + `validate-backlog` och sammanfattar fel.
2. **`docs:new`** — scaffold: PRD/ADR/ref/runbook/backlog item via befintliga `new-*` scripts.
3. **`backlog:slice`** — skapa story + tasks (PR-slices) och länka dem korrekt (related/links).
4. **`content:import-html-portal`** — importera Docforge-export (HTML/CSS/assets) till `frontend/public/<week>/portal/` + uppdatera rutter/meny.
5. **`release:week-page`** — skapa ny projektsida (Vue route + svensk copy + embed-strategi) med stabil URL.

## Steg-för-steg (implementation i portalen)

1. Dokumentera vilka guards som ska portas (HuleEdu) och skapa backlog-tasks för dem.
2. Inför “one command” quality gate och ev. pre-commit-konfiguration (Skriptoteket-mönster).
3. Skapa första setet Codex-skills och verifiera på FN-rollspel v43.
4. Uppdatera runbook för deploy när pipeline/guards är på plats.
