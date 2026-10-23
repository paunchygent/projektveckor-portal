## Current

- Production smoke test is open: login, document preview and teacher export
  with CSRF against `https://projektveckor.hule.education`. Next: create an
  Identity test account with `email_verified=true` and the `teacher` role,
  then walk the flow. Owner: the next portal session.
- Open product choices: keep FN-rollspel v43 as embedded static HTML or port
  it to native Vue; add the next project weeks on the same route pattern; add
  the first admin page (document editor and export buttons).

## Recent

- 23Oct: adopted repository governance (TASK-SKILL-16-03-02): root
  `handoff.md`, `AGENTS.md` skeleton, `.codex/skills` with `.claude/skills`
  and `.agents/skills` links, shared governance commands in `pyproject.toml`.
- Feb-Mar 2026: deployed on Hemma on `hule-network` with Identity and Sir
  Convert-a-Lot; HTTPS and `/healthz` answer 200 after the DNS A record and
  certificate order.
- 1Mar 2026: export retry for Sir Convert-a-Lot v2 (bounded rerun after an
  idempotent failed replay); 27Feb 2026: Dishka DI, cookie and CSRF auth BFF
  against HuleEdu Identity, document library preview and admin write.

## Facts

- Server `.env` key names only, never values: `~/apps/projektveckor-portal/.env`
  holds `PVP_*`, `VIRTUAL_HOST` and `LETSENCRYPT_HOST`.
- Decisions: ADR-0002 (self-hosted documents, exports through Sir
  Convert-a-Lot) and ADR-0003 (auth reuses HuleEdu Identity) in
  `docs/decisions/`.
- Legacy backlog documents under `docs/backlog/` predate PROJV identity and
  are history; new contracts use `pdm run new-task`.
