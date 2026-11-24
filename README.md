# Projektveckor Portal

Portal för projektveckor (t.ex. FN-rollspel v.43) som hostas på `hule.education` och **hostar dokumenten själv** (förhandsvisning i webben + konvertering till PDF/DOCX via Sir Convert a Lot).

## Snabbstart (dev)

- Backend: `pdm install -G dev`, kopiera `.env.example.dev` till `.env.dev` och kör `pdm run dev` (LAN: `pdm run dev:lan`). Dev-kommandona sätter `PVP_SETTINGS_FILE=.env.dev` och läser aldrig `.env`.
- Frontend: `pdm run frontend:install` och sedan `pdm run frontend:dev` (LAN: `pdm run frontend:dev:lan`)

## Auth (dev)

- Logga in via `http://127.0.0.1:5173/login` (tunn proxy mot HuleEdu Identity).
- Kräver att du satt `PVP_IDENTITY_BASE_URL` (och ev. `PVP_IDENTITY_INTROSPECT_URL`) i `.env.dev`. `.env.dev` håller bara konfiguration; Sir-nyckeln `SIR_CONVERT_A_LOT_V2_API_KEY` kommer från agent-secrets (`pdm run serve`), aldrig från filen.

## Docs

Se `docs/index.md`.
