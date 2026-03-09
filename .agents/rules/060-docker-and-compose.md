---
trigger: model_decision
rule_id: RULE-060
title: Docker och Compose
status: active
created: "2026-02-25"
updated: "2026-02-26"
owners:
  - portal
tags: []
scope: ops
---

## MUST

- Använd `docker compose` (v2), inte `docker-compose`.
- Håll compose-filer små och tydliga (dev vs prod).
- Använd `.env.example.prod` som mall; lägg aldrig riktiga secrets i git.
- På Hemma ska Docker persistent state ligga på `/srv/scratch`, inte på `/`.
- På Hemma ska rådata och kall bulk-lagring ligga på `/srv/storage`.
