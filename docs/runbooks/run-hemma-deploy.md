---
type: runbook
id: RUN-hemma-deploy
title: Deploy på hemma (hule.education)
status: active
created: "2026-02-26"
updated: "2026-02-27"
owners:
  - portal
system: hemma
tags:
  - deploy
links:
  - docs/runbooks/run-ssh-hemma-windows-wsl.md
---

Den här runbooken följer samma operativa stil som Skriptoteket/HuleEdu.

## Förutsättningar

- SSH-access till Hemma (se `docs/runbooks/run-ssh-hemma-windows-wsl.md`).
- Docker installerat på servern
- Externt nätverk finns: `hule-network`
- Reverse-proxy stack kör (nginx-proxy + LetsEncrypt companion)

## Lagringsmodell på Hemma

- `/srv/scratch` = snabb SSD-arbetsyta för Docker root/BuildKit-cache och
  aktiva genererade artefakter.
- `/srv/storage` = stor HDD-datayta för rådata och kall långtidslagring.
- `/` ska inte vara långsiktig plats för Docker persistent state eller stora
  artefaktträd.

## Bygg och starta

På servern:

1. Skapa `.env` från `.env.example.prod` (det här är **prod**-värden och ska ligga på servern). `.env` håller konfiguration; Sir-nyckeln `SIR_CONVERT_A_LOT_V2_API_KEY` läses aldrig från `.env` utan kommer från `agent-secrets` (set `projektveckor-portal-prod`). Raden med nyckeln lämnar produktions-`.env` först vid det godkända live-bytet (TASK-SKILL-18-03-02); ändra inte produktionsfilen före det.
2. Bygg (utan hemligheter):
   - `docker compose -f compose.prod.yaml build`
3. Starta eller återskapa via wrappern, som sätter `SIR_CONVERT_A_LOT_V2_API_KEY` i processmiljön:
   - `pdm run prod-compose up -d`

Operativa compose-kommandon som inte behöver hemligheter (`ps`, `logs`,
`stop`, `config`, `exec`) körs mot basfilen direkt, utan wrappern:

- `docker compose -f compose.prod.yaml ps` (osv.)

Lokalt (dev):

- Skapa din lokala `.env` från `.env.example.dev` (dev-värden) och kör `pdm run dev`. `.env` innehåller bara konfiguration; en Sir-nyckel levereras av `agent-secrets` (`pdm run serve`), inte av filen.

## Verifiera

- `GET /healthz` returnerar 200
- Startsidan laddar på konfigurerad host
