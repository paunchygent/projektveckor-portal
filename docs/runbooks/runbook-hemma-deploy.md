---
type: runbook
id: RUN-hemma-deploy
title: Deploy på hemma (hule.education)
status: active
created: "2026-02-26"
updated: "2026-02-26"
owners:
  - portal
system: hemma
tags:
  - deploy
links: []
---

Den här runbooken följer samma operativa stil som Skriptoteket/HuleEdu.

## Förutsättningar

- Docker installerat på servern
- Externt nätverk finns: `hule-network`
- Reverse-proxy stack kör (nginx-proxy + LetsEncrypt companion)

## Bygg och starta

På servern:

1. Skapa `.env` från `.env.example.prod`.
2. Bygg och starta:
   - `docker compose -f compose.prod.yaml build`
   - `docker compose -f compose.prod.yaml up -d`

## Verifiera

- `GET /healthz` returnerar 200
- Startsidan laddar på konfigurerad host
