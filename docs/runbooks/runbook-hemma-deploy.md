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
  - docs/runbooks/runbook-ssh-hemma-windows-wsl.md
---

Den här runbooken följer samma operativa stil som Skriptoteket/HuleEdu.

## Förutsättningar

- SSH-access till Hemma (se `docs/runbooks/runbook-ssh-hemma-windows-wsl.md`).
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

1. Skapa `.env` från `.env.example.prod` (det här är **prod**-värden och ska ligga på servern).
2. Bygg och starta:
   - `docker compose -f compose.prod.yaml build`
   - `docker compose -f compose.prod.yaml up -d`

Lokalt (dev):

- Skapa din lokala `.env` från `.env.example.dev` (dev-värden) och kör `pdm run dev`.

## Verifiera

- `GET /healthz` returnerar 200
- Startsidan laddar på konfigurerad host
