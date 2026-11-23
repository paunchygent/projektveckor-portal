---
name: projektveckor-hemma-deploy
description: Use when deploying Projektveckor Portal to the home server with Docker Compose, environment setup, and health verification.
---

# Skill: hemma deploy (hule.education)

Use this skill when deploying the portal to the home server. The full
procedure is `docs/runbooks/run-hemma-deploy.md`.

## Canonical deploy files

- `compose.prod.yaml` for production and `compose.dev.yaml` for local runs;
  keep both small.
- `compose.secrets.prod.yaml` holds the only secret interpolation and is
  passed only through `pdm run prod-compose`
  (`agent-secrets run --set projektveckor-portal-prod`), which injects
  `SIR_CONVERT_A_LOT_V2_API_KEY` into the process environment. `ps`, `logs`,
  `stop`, `config` and `exec` run against `compose.prod.yaml` alone.
- `.env.example.prod` is the template for the server `.env`; `.env` holds
  configuration only, and real secrets never enter Git.

## Minimal deploy steps

1. On server, create `.env` from `.env.example.prod` (configuration only).
2. Build + run with Compose v2 (`docker compose`, never `docker-compose`):
   - `docker compose -f compose.prod.yaml build`
   - `pdm run prod-compose up -d`
3. Verify both:
   - `GET /healthz` returns 200
   - the start page loads on `https://projektveckor.hule.education`

## Notes

- Production runs on Hemma (`hule.education`) and joins the shared external
  network `hule-network`.
- The production host defaults to `projektveckor.hule.education` through the
  nginx-proxy environment variables `VIRTUAL_HOST` and `LETSENCRYPT_HOST`.
- On Hemma, Docker persistent state belongs on `/srv/scratch`, while raw bulk
  data belongs on `/srv/storage`.
