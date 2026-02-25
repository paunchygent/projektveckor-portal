---
id: "080-home-server-deployment"
type: "standards"
created: "2026-02-25"
scope: "ops"
---

# Home-server deployment (hule.education)

Goal: deploy the portal on the home server, fronted by the existing reverse-proxy stack (same approach as Skriptoteket/HuleEdu).

## Strategy (baseline)

- Run `compose.prod.yaml` on the server.
- Attach to the shared external network `hule-network`.
- Configure host routing via `VIRTUAL_HOST` + `LETSENCRYPT_HOST` environment variables (nginx-proxy pattern).

