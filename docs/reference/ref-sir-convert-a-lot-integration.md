---
type: reference
id: REF-sir-convert-a-lot-integration
title: "Integration: Sir Convert a Lot (API v2) från Projektveckor Portal"
status: draft
created: "2026-02-26"
updated: "2026-02-26"
owners:
  - portal
tags:
  - conversion
  - integration
links:
  - docs/decisions/0002-self-hosted-documents-and-conversion.md
  - docs/backlog/tasks/task-10-sir-convert-a-lot-adapter.md
---

## Syfte

Definiera hur `projektveckor-portal` integrerar med Sir Convert a Lot för att skapa exportfiler (PDF/DOCX) från hostade källor (Markdown/HTML/PDF).

I portalen är **Markdown canonical source** för instruktioner (Markdown→HTML för preview i webben).

## Contract-källor (upstream)

Normativa dokument i `sir-convert-a-lot`:

- API v2: `docs/converters/multi_format_conversion_service_api_v2.md`
- Adapterprinciper: `docs/converters/internal_adapter_contract_v1.md`

## Översikt (API v2)

- Base path: `/v2`
- Autentisering: header `X-API-Key`
- Idempotency vid job-skapande: header `Idempotency-Key`
- Konverteringar (v2):
  - `html -> pdf`
  - `html -> docx`
  - `md -> pdf`
  - `md -> docx`
  - `pdf -> docx`

## Endpoints (API v2)

1. `POST /v2/convert/jobs` (multipart)
   - `file`: PDF/MD/HTML
   - `job_spec`: JSON-sträng (v2 JobSpec)
   - `resources`: valfri zip (CSS/bilder/fonts)
   - `reference_docx`: valfri docx för styling
   - query: `wait_seconds=0..20` (valfritt)

2. `GET /v2/convert/jobs/{job_id}`
   - status + länkar

3. `GET /v2/convert/jobs/{job_id}/result`
   - metadata när `succeeded`

4. `GET /v2/convert/jobs/{job_id}/artifact`
   - binär output (PDF/DOCX) när `succeeded`

5. `POST /v2/convert/jobs/{job_id}/cancel`

## JobSpec (v2) — minsta fält vi behöver

`job_spec` skickas som JSON-sträng i `POST /v2/convert/jobs`.

Minsta praktiska mappning för portalen:

- `api_version: "v2"`
- `source.kind: "upload"`
- `source.filename`: originalfilnamn (för spårbarhet)
- `source.format: "md" | "html" | "pdf"`
- `conversion.output_format: "pdf" | "docx"`

## Portalens adapter-krav (DIP/DI)

Portalen ska ha en port (abstraktion) som inte är bunden till HTTP/CLI.

Mål:

- En enda canonical mapping från “portal-dokument” → `JobSpec`.
- Deterministiska headers (correlation + idempotency) enligt upstream-kontrakt.

## Lagring av exporter

Rekommenderat i portalen:

- Spara exporter server-side (t.ex. under `data/exports/...`).
- Exponera nedladdningslänk i portalen (inte inline base64).
- Visa job-status i admin-UI (queued/running/succeeded/failed).
