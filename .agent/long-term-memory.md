# Long-term memory (append-only)

Rules:

- Append-only. Do not rewrite history.
- Put new items at the top with an ISO date.
- Only store durable decisions, conventions, and “why”.

---

2026-02-25

- Week content can be shipped as static HTML exports under `frontend/public/...` and embedded in SPA routes (iframe) to avoid SharePoint preview navigation constraints.

2026-02-25

- Portal is hosted and navigated as a SPA with stable routes (Vue Router); backend serves history fallback.
- Production default host is `projektveckor.hule.education` via nginx-proxy env vars (`VIRTUAL_HOST`, `LETSENCRYPT_HOST`).
