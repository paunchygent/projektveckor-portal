# Runbook — Deploy on hemma (hule.education)

This runbook mirrors the same operational style used for Skriptoteket/HuleEdu.

## Prerequisites

- Docker installed on server
- External network exists: `hule-network`
- Reverse-proxy stack is running (nginx-proxy + LetsEncrypt companion)

## Build and start

On server:

1. Create `.env` from `.env.example.prod`
2. Build + run:
   - `docker compose -f compose.prod.yaml build`
   - `docker compose -f compose.prod.yaml up -d`

## Verify

- `GET /healthz` returns 200
- Front page loads at the configured host

