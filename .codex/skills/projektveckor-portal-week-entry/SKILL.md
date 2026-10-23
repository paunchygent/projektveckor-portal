---
name: projektveckor-portal-week-entry
description: Use when adding or updating project week entries in Projektveckor Portal, including teacher-facing links and week content structure.
---

# Skill: add a new project week entry

Use this skill when adding a new project week to the portal.

## Current implementation

- The frontend is Vue 3, Vite and TypeScript. Week pages are Vue Router
  routes in `frontend/src/router.ts`, for example `/fn-rollspel/v43`, with
  pages under `frontend/src/pages/`.
- Week content can ship as a static HTML export under
  `frontend/public/<week>/...`, embedded in the SPA route through an `iframe`.
  This avoids SharePoint preview navigation limits
  (`frontend/public/fn-rollspel/v43/portal/` embedded by
  `FnRollspelV43Page.vue`).

## Add a week

1. Add a stable route `/<week>/<edition>`; a published URL must keep working
   for years.
2. Prefer linking to:
   - “Börja här” PDF (teacher entrypoint)
   - Schema PDF
   - A folder link for “resources”
3. Keep names teacher-friendly (no “resursindex”/dev jargon).
4. Teacher and export HTML that will be reused takes its styles from external
   CSS, never inline styles.
