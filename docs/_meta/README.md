---
type: meta
id: META-docs-contract
title: Docs contract (översikt)
status: active
created: "2026-02-26"
updated: "2026-02-26"
owners:
  - portal
tags:
  - docs-as-code
links:
  - docs/_meta/docs-contract.yaml
  - scripts/docs_as_code/validate_docs.py
---

## Vad det här är

`docs/_meta/docs-contract.yaml` är repo:ts kontrakt för dokumentation och regler.

Det används av valideraren för att säkerställa att:

- dokument har YAML-frontmatter,
- filnamn och placering följer taxonomin,
- obligatoriska metadatafält finns per dokumenttyp.

## Varför

Det gör att repo:t kan växa (fler projektveckor, fler resurser, fler team) utan att dokumentationen blir ett “mystery meat”-lager.
