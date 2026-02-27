---
type: reference
id: REF-dishka-migration-plan
title: "Plan: Dishka-migrering av DI (Projektveckor Portal)"
status: active
created: "2026-02-26"
updated: "2026-02-26"
owners:
  - portal
tags:
  - di
  - dishka
  - architecture
links:
  - docs/decisions/0003-auth-integration-huleedu-skriptoteket.md
---

## Syfte

Portalen ska kunna växa utan att låsa oss vid FastAPI:s `Depends(...)` som primär DI-mekanism.
Vi vill ha en tydlig **composition root**, testbar wiring och stabila abstraktioner (ports/adapters).

## Nuläge

- Vi använder redan en enkel composition root i `src/projektveckor_portal/app.py` via `app.state`.
- Web-lagret använder `Depends(...)` främst för:
  - auth-guards (teacher/admin),
  - CSRF-guard.

## Målbild

- Dishka används för att:
  - skapa och livscykelhantera beroenden (clients/repos/services),
  - injicera i routes utan manuell `app.state`-plockning,
  - göra test-wiring trivial (byta providers i test).

## Stegvis migrering (PR-slices)

1. **Avgränsa “service registry”**
   - Alla externa beroenden (Identity client, Convert client, repos) exponeras som tydliga typer/ports.
   - `app.state` behålls som interim-lösning men samlas i en enda “registry”.

2. **Inför Dishka i backend (utan att ändra beteende)**
   - Lägg till Dishka som dependency och skapa en `container` i `create_app()`.
   - Koppla Dishka-integrationen för FastAPI.
   - Låt routes gradvis byta från `request.app.state` till `FromDishka[...]`.

3. **Flytta guards till Dishka**
   - Authenticator + Identity client injiceras via Dishka.
   - Guards för teacher/admin/CSRF blir tunna och testbara.

4. **Rensa ut `app.state`**
   - När alla routes använder Dishka: ta bort registry-koden och behåll bara composition root.

## Designprinciper

- Ports i `interfaces/` ska vara stabila.
- Web/API ska vara tunn (SRP).
- Infra implementerar protokoll och kan bytas i test.
