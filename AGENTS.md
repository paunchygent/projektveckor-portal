# AGENTS.md — Projektveckor Portal

Det här repot följer en **doc-as-code**-modell (inspirerad av HuleEdu och Skriptoteket): rules-first, stabil agent-dokumentation och repeterbara dev/deploy-kommandon.

## Läsordning (obligatorisk)

1. `docs/index.md`
2. `.agents/readme-first.md`
3. `.agents/rules/000-rule-index.md`
4. `.agents/handoff.md`

## Icke förhandlingsbart

- Lägg aldrig in hemligheter (tokens/lösenord) i git.
- Håll strukturen stabil i `.agents/readme-first.md` och `.agents/handoff.md` (endast innehåll uppdateras).
- Föredra att uppdatera regler framför ad hoc-undantag.

## Arkitekturprinciper (MÅSTE)

- **DDD + Clean Architecture**: domän är “pure”, web/API är tunn, infrastruktur implementerar protokoll.
- **DIP/DI**: bero på abstraktioner (t.ex. `typing.Protocol`), injicera implementationer.
- **Strict SRP**: dela moduler innan de blir stora eller otydliga.
- **Filer < ~500 LoC** som riktlinje (refaktorera tidigt).

## Kommandon (repo-root)

- Backend: `pdm run dev`
- Frontend (från repo-root): `pdm run frontend:install`, `pdm run frontend:dev`, `pdm run frontend:build`
- Docs: `pdm run validate-docs`, `pdm run validate-backlog`, `pdm run check:md`

## Hemma Storage Model

- `/srv/scratch` = snabb SSD-arbetsyta för Docker root/BuildKit-cache, modell-
  och HF-cache samt aktiva genererade artefakter.
- `/srv/storage` = stor HDD-datayta för rådata/korpusar och kall långtidslagring.
- `/` får inte vara långsiktig plats för Docker persistent state eller stora
  ML-/byggartefakter.
