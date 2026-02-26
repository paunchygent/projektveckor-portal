---
type: decision
id: ADR-0003
title: "Autentisering/auktorisering återanvänds från HuleEdu/Skriptoteket"
status: accepted
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

`projektveckor-portal` återanvänder HuleEdu/Skriptoteket och implementerar inga “egna användare”.

### Kort sikt (MVP)

- Portalen har en egen `/login`-vy (frontend) som anropar portalens API.
- Portalen fungerar som en **tunn proxy** mot HuleEdu Identity:
  - `POST /api/v1/auth/login` → vidarebefordrar login till HuleEdu Identity och **sätter httpOnly-cookies** för sessionen.
  - `GET /api/v1/auth/me` → validerar session (via HuleEdu Identity introspection/refresh vid behov) och returnerar rollinformation.
- CSRF-skydd körs på **skrivande requests** (POST/PUT/PATCH/DELETE) via headern `X-CSRF-Token`.
- Roller normaliseras till den minsta mängd vi behöver i portalen:
  - `student` (ej admin-yta)
  - `teacher` (får redigera/exports/bulletin)
  - `admin` (framtida “no-code”/konfiguration som vi inte vill bygga in i teacher-rollen)
- Allt elev-/delegationsinnehåll är öppet; admin-yta och lärardokument kräver inloggning.

### Lång sikt

- Inloggning sker i en gemensam plats (HuleEdu/Skriptoteket) och portalen **konsumerar redan satta cookies**.
- Portalen ska kunna köras bakom en gateway som centraliserar auth och minskar behovet av introspection per request.

## Öppna frågor

- Exakt gateway-modell på sikt (header-baserad auth vs fortsatta cookies).
- Hur vi vill exponera “login entrypoint” när portal + HuleEdu körs på olika subdomäner.

## Konsekvenser

- Vi behöver inventera hur auth görs i HuleEdu/Skriptoteket och återanvända kod/kontrakt.
- Vi behöver tydliga regler för “public vs teacher-only” på dokumentnivå.
