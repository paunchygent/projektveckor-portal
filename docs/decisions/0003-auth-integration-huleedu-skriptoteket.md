---
type: decision
id: ADR-0003
title: "Autentisering/auktorisering återanvänds från HuleEdu/Skriptoteket"
status: proposed
created: "2026-02-26"
updated: "2026-02-26"
owners:
  - portal
tags:
  - auth
  - architecture
links:
  - docs/decisions/0002-self-hosted-documents-and-conversion.md
  - docs/backlog/epics/epic-self-hosted-doc-library-and-conversion.md
---

## Kontext

Portalen behöver en läraryta (redigering + export + bulletin). Vi vill inte implementera ett separat hardcoded auth-system i `projektveckor-portal` eftersom vi redan har etablerade lösningar i HuleEdu och Skriptoteket.

Samtidigt ska elev-/delegationsinnehåll vara öppet och navigerbart utan inloggning.

## Beslut (förslag)

- `projektveckor-portal` ska använda samma AuthN/AuthZ-mekanism som HuleEdu/Skriptoteket.
- Portalen ska modellera auth som en **port** (abstraktion) i application-lagret och en **adapter** i infrastructure-lagret.
- Publica rutter och dokument är öppna; lärarinstruktioner och admin-rutter kräver giltig auth + rätt roll.

## Öppna frågor

- Exakt integrationsform:
  - OIDC/JWT-verifiering lokalt i portalen, eller
  - “auth gateway”/introspektion mot HuleEdu, eller
  - reverse-proxy auth (t.ex. headers från gateway).
- Rollmodell: minsta roller vi behöver (t.ex. `teacher`, `admin`).

## Konsekvenser

- Vi behöver inventera hur auth görs i HuleEdu/Skriptoteket och återanvända kod/kontrakt.
- Vi behöver tydliga regler för “public vs teacher-only” på dokumentnivå.

