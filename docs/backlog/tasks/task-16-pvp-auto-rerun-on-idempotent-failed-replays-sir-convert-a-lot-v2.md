---
id: "task-16-pvp-auto-rerun-on-idempotent-failed-replays-sir-convert-a-lot-v2"
title: "PVP auto-rerun on idempotent failed replays (Sir Convert-a-Lot v2)"
type: "task"
status: "completed"
priority: "high"
created: "2026-03-01"
last_updated: "2026-03-01"
related:
  - src/projektveckor_portal/infrastructure/conversion/sir_convert_a_lot_v2_client.py
  - src/projektveckor_portal/application/exports_service.py
  - docs/reference/ref-sir-convert-a-lot-integration.md
labels:
  - conversion
  - sir-convert-a-lot
  - ux
---

PR-sized execution unit; may be linked to a story or standalone.

## Objective

Make “retry export after a fix” behave as users expect:

- If an export previously failed, clicking export again should start a new conversion job.
- Preserve Sir Convert-a-Lot v2 service idempotency semantics (no server changes).
- Keep portal logic deterministic and easy to reason about.

## PR Scope

- Fix v2 create-job payload parsing in the portal client:
  - v2 returns nested payload `{"job": {"job_id": "...", "status": "..."}}` (not flat keys).
- Fix v2 get-job payload parsing in the portal client:
  - `GET /v2/convert/jobs/{job_id}` returns the same nested `{"job": ...}` envelope (status is not a
    top-level key).
- Implement bounded auto-rerun in the portal v2 client:
  - if `POST /v2/convert/jobs` returns `X-Idempotent-Replay: true` and job status is terminal
    `failed`/`canceled`, submit a new job once with a fresh idempotency key.
- Update export workflow to allow reruns:
  - if an existing export record is terminal `failed`, create a new job and overwrite the stored
    `job_id` for the same `export_id`.
- Add regression tests for:
  - v2 client parsing (`POST` + `GET`) and bounded auto-rerun behavior.
  - export retry semantics: a terminal failed export does not block creating a new job.
- Remove new typing shortcuts in touched code paths (no new `Any`, casts, or ignores).
- Add tests that lock the behavior (auto-rerun + export retry).
- Update integration docs to describe retry behavior.

## Deliverables

- [x] Failed exports can be retried without changing source content or filenames.
- [x] Portal v2 client correctly parses and returns `job_id` + `status` from the v2 envelope.
- [x] Auto-rerun triggers only for idempotent replay + terminal fail/cancel and is bounded to one rerun.
- [x] Tests cover the retry behavior.

## Acceptance Criteria

- [x] When an export record exists with `status="failed"`, calling export again creates a new job and
      stores a new `job_id`.
- [x] Client behavior:
  - no rerun when a non-replayed job fails,
  - rerun occurs when replayed terminal failure is detected.
- [x] `GET /v2/convert/jobs/{job_id}` parsing yields correct status (no empty/unknown status mapping).
- [x] Quality gates:
  - `pdm run lint` passes.
  - `pdm run typecheck` passes.
  - `pdm run test` passes.
  - `pdm run validate-docs`, `pdm run validate-backlog`, `pdm run validate-skills` pass.

## Checklist

- [x] Implementation complete
- [x] Validation complete
- [x] Docs updated

## Validation Evidence

- `pdm run format`
- `pdm run lint`
- `pdm run typecheck`
- `pdm run test`
- `pdm run validate-docs`
- `pdm run validate-backlog`
- `pdm run validate-skills`
