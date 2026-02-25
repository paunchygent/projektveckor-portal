# Skill: add a new project week entry

Use this skill when adding a new project week to the portal.

## Current implementation (v0.1)

Weeks are hardcoded in `frontend/src/App.vue`.

## Add a week

1. Add the SharePoint root folder URL (or direct PDF/DOCX URLs).
2. Prefer linking to:
   - “Börja här” PDF (teacher entrypoint)
   - Schema PDF
   - A folder link for “resources”
3. Keep names teacher-friendly (no “resursindex”/dev jargon).

## Next refactor (when needed)

Move week data to a JSON file (checked in) and render entries dynamically.

