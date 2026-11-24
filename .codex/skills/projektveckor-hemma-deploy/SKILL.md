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
- `.env.example.prod` is the template for the server `.env`.
  `compose.prod.yaml` has no `env_file`: `web.environment` names each
  non-secret `PVP_*` setting as a value-less entry, which Compose fills from
  the project `.env`, so no other `.env` entry reaches the container. `.env`
  holds configuration; the app reads the Sir key only from the process
  environment, never from `.env`. The key line leaves the production `.env`
  only at the approved live switch (TASK-SKILL-18-03-02). Real secrets never
  enter Git.
- `pdm run dev` and `dev:lan` set `PVP_SETTINGS_FILE=.env.dev` and never read
  `.env`; `.env.example.dev` is the template.

## Minimal deploy steps

1. On server, create `.env` from `.env.example.prod` (configuration).
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
