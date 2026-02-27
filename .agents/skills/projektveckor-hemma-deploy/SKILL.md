---
name: projektveckor-hemma-deploy
description: Use when deploying Projektveckor Portal to the home server with Docker Compose, environment setup, and health verification.
---

# Skill: hemma deploy (hule.education)

Use this skill when deploying the portal to the home server.

## Canonical deploy file

- `compose.prod.yaml`

## Minimal deploy steps

1. On server, create `.env` from `.env.example.prod`.
2. Build + run:
   - `docker compose -f compose.prod.yaml build`
   - `docker compose -f compose.prod.yaml up -d`
3. Verify:
   - `GET /healthz` returns 200

## Notes

- Uses shared external network `hule-network`.
- Host routing uses nginx-proxy environment variables: `VIRTUAL_HOST`, `LETSENCRYPT_HOST`.
