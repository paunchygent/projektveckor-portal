# Repo-lokala skills (Projektveckor Portal)

Den här mappen innehåller **repo-lokala skills** som kan overridea/komplettera globala Codex-skills.

## Rules

- Repo-lokala skills ligger under `.agents/.codex/skills/` och committas.
- Globala skills ligger under `$CODEX_HOME/skills/`:
  - Windows: `%USERPROFILE%\.codex\skills\`
  - WSL/Linux: `~/.codex/skills/`
- Namnge lokala varianter med prefixet `projektveckor-` för att undvika krockar med globala skill-namn.

## Current local skills

- `projektveckor-docs-as-code/`
- `projektveckor-hemma-deploy/`
- `projektveckor-portal-week-entry/`
- `projektveckor-ssh-hemma-windows-wsl/`
