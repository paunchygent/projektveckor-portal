---
name: projektveckor-ssh-hemma-windows-wsl
description: Hjälp för att få `ssh hemma` att fungera mot hemmaservern från Windows (PowerShell/Windows OpenSSH) och från WSL (Linux OpenSSH), inklusive var nycklar/config/known_hosts ligger, hur man verifierar vilken nyckel som används, hur man lägger till pubkey via Taildrop, och felsökning av hostkey/permission denied/wrong key/SSH-agent.
---

# Skill: SSH hemma (Windows + WSL)

Använd den här skillen när en användare vill ansluta till hemmaservern med `ssh hemma` och fastnar i skillnader mellan Windows och WSL (nyckelplatser, `~/.ssh/config`, agent, filrättigheter, host keys).

## Canonical runbook

- `docs/runbooks/runbook-ssh-hemma-windows-wsl.md`

## Installera globalt (valfritt)

Om du vill att skillen ska vara global (inte bara repo-lokal), kopiera mappen till din Codex-home:

- Windows: `%USERPROFILE%\.codex\skills\projektveckor-ssh-hemma-windows-wsl\`
- WSL/Linux: `~/.codex/skills/projektveckor-ssh-hemma-windows-wsl/`

## Först: samla minsta nödvändiga fakta (ställ frågor)

Fråga alltid innan du föreslår fixar:

1. Kör användaren `ssh` i **Windows** (PowerShell/Terminal) eller i **WSL**?
2. Vilket felmeddelande får de (exakt rad)?
3. Har de redan en `Host hemma` i SSH config (och i vilken fil)?
4. Är anslutningen via Tailscale (Tailnet) och vad är `HostName` tänkt att vara (hostname eller Tailscale-IP)?

Be om output (klistra in) från rätt miljö:

- `ssh -vvv hemma`
- `ssh -G hemma` (för att se effektiv `User/HostName/IdentityFile`)

## Snabb påminnelse: skillnader Windows vs WSL

- Windows OpenSSH använder normalt:
  - `%USERPROFILE%\\.ssh\\config`
  - `%USERPROFILE%\\.ssh\\known_hosts`
  - `%USERPROFILE%\\.ssh\\<nycklar>`
- WSL OpenSSH använder normalt:
  - `~/.ssh/config`
  - `~/.ssh/known_hosts`
  - `~/.ssh/<nycklar>`
- Windows och WSL har i praktiken **olika SSH-agenter** och olika “nyckel-listor”.

## Säkerhet

- Be aldrig om privatnyckelns innehåll.
- Be max om publik nyckel (`*.pub`) och kommandoutskrifter.
- Om någon råkar klistra in privatnyckel: be dem rotera nyckeln direkt.

## Få `ssh hemma` att fungera (procedur)

### 1) Säkerställ att rätt config-fil används

- Om de kör i Windows: redigera `%USERPROFILE%\\.ssh\\config`
- Om de kör i WSL: redigera `~/.ssh/config`

Be dem lägga till (eller verifiera) ett host-block med:

- `HostName <hemma-hostname-eller-tailscale-ip>`
- `User <user>`
- `IdentityFile <path-till-privatnyckel>`
- `IdentitiesOnly yes` (för att undvika “fel nyckel” från agenten)

### 2) Verifiera “vilken nyckel” som faktiskt används

Leta i `ssh -vvv` efter:

- `identity file ...` (vilka filer den försöker läsa)
- `Offering public key: ...` (vilken pubkey som erbjuds)
- `Authentication succeeded (publickey)` (vilken som accepteras)

Om fel nyckel erbjuds:

- Sätt/behåll `IdentitiesOnly yes`
- Sätt explicit `IdentityFile ...`
- Be dem köra `ssh-add -D` (i samma miljö som `ssh` körs) och testa igen

### 3) Om pubkey inte finns på servern: lägg till via Taildrop

Mål: få in klientens `*.pub` i serverns `~/.ssh/authorized_keys`.

Be användaren:

1. Skapa ny nyckel i rätt miljö (Windows eller WSL).
2. Skicka **endast** `.pub` via Taildrop till servern.
3. På servern: appenda pubkey till `~/.ssh/authorized_keys` och säkra permissions:
   - `mkdir -p ~/.ssh && chmod 700 ~/.ssh`
   - `cat /path/till/pubkey.pub >> ~/.ssh/authorized_keys`
   - `chmod 600 ~/.ssh/authorized_keys`

### 4) Om det fortfarande blir “Permission denied (publickey)”

Triagera i den här ordningen:

1. Fel `User` i config (nyckeln ligger på annan användare).
2. Fel `HostName` (du når fel maskin).
3. Fel nyckel (verifiera med `ssh -vvv`).
4. Permissions på servern (`~/.ssh` och `authorized_keys`).

## Vanliga fel och åtgärder (kort)

- `REMOTE HOST IDENTIFICATION HAS CHANGED!`:
  - Verifiera att host key verkligen ändrats (out-of-band), kör `ssh-keygen -R hemma`, testa igen.
- `WARNING: UNPROTECTED PRIVATE KEY FILE!` (ofta WSL):
  - Kör `chmod 600 ~/.ssh/<nyckel>` och `chmod 700 ~/.ssh`, undvik nycklar via `/mnt/c/...`.
- “Wrong key” / många keys erbjuds:
  - `IdentitiesOnly yes`, explicit `IdentityFile`, töm agenten med `ssh-add -D`.
- Agent-förvirring:
  - Kör `ssh-add -l` i samma miljö som `ssh`.
  - I WSL: kontrollera `echo $SSH_AUTH_SOCK` (ska inte vara tom).

## När du ska uppdatera runbooken

Om du hittar ett återkommande fel (ny Tailscale/Taildrop-variant, ny standardplats för mottagna filer, eller ny typ av hostkey-problem), uppdatera:

- `docs/runbooks/runbook-ssh-hemma-windows-wsl.md`
