---
type: runbook
id: RUN-ssh-hemma-windows-wsl
title: SSH hemma från Windows + WSL
status: active
created: "2026-02-27"
updated: "2026-02-27"
owners:
  - portal
system: hemma
tags:
  - ssh
  - windows
  - wsl
  - tailscale
links: []
---

Den här runbooken beskriver hur du får `ssh hemma` att fungera från **Windows** (PowerShell/Windows OpenSSH) och från **WSL** (Linux OpenSSH), hur du verifierar **vilken nyckel** som faktiskt används, hur du lägger till din **pubkey** via **Taildrop**, samt vanlig felsökning.

## Viktigt: `tailscale ssh` vs vanlig SSH över Tailnet

I den här miljön utgår vi från **vanlig `ssh`** mot Hemma via Tailnet (dvs `ssh.exe` i Windows eller `ssh` i WSL). `tailscale ssh ...` kan vara avstängt/otillgängligt även om Tailnet fungerar.

## Snabbval: Windows eller WSL?

Välj medvetet _var_ du kör `ssh` — det styr vilka filer/agents som används.

- **Windows (PowerShell/Terminal)**:
  - SSH körs som Windows OpenSSH.
  - Nycklar/config/known_hosts ligger under `%USERPROFILE%\.ssh\`.
- **WSL (Ubuntu/Debian/etc.)**:
  - SSH körs som Linux OpenSSH.
  - Nycklar/config/known_hosts ligger under `~/.ssh/`.
  - Striktare filrättigheter (chmod) gäller.

## Förutsättningar

- Du kan nå hemmaservern via Tailscale (Tailnet uppkopplad).
- På servern finns en användare att logga in som (t.ex. `ubuntu`, `deploy`, eller ditt konto).
- På servern kör `sshd` (SSH-server).

## Var ligger nycklar och config?

### Windows (PowerShell)

- Privatnycklar: `C:\Users\<du>\.ssh\*` (dvs `%USERPROFILE%\.ssh\`)
- SSH-config: `C:\Users\<du>\.ssh\config`
- Known hosts: `C:\Users\<du>\.ssh\known_hosts`

Praktiska kommandon:

- Visa var SSH tittar: `ssh -G hemma`
- Lista filer: `dir $env:USERPROFILE\\.ssh`

### WSL (Linux)

- Privatnycklar: `/home/<du>/.ssh/*` (dvs `~/.ssh/`)
- SSH-config: `~/.ssh/config`
- Known hosts: `~/.ssh/known_hosts`

Praktiska kommandon:

- Lista filer: `ls -la ~/.ssh`
- Se effektiv config: `ssh -G hemma | sed -n '1,200p'`

### Viktigt om “Windows-nycklar i WSL”

Du _kan_ peka WSL-SSH på nycklar under `/mnt/c/Users/<du>/.ssh/`, men det orsakar ofta problem:

- Fel filrättigheter (”bad permissions”).
- Agent-/nyckelförvirring (du tror du använder WSL-nyckeln, men det är Windows-nyckeln).

Rekommendation: ha **en separat nyckel per miljö** (en för Windows och/eller en för WSL), eller kopiera nyckeln till `~/.ssh/` och säkra permissions i WSL.

## Skapa en ny SSH-nyckel (rekommenderat: ed25519)

Skapa nyckeln i den miljö där du faktiskt ska köra `ssh`.

### Windows

Kör i PowerShell:

- `ssh-keygen -t ed25519 -f $env:USERPROFILE\\.ssh\\hemma_ed25519 -C \"hemma (windows)\"`

Resultat:

- Privat: `%USERPROFILE%\\.ssh\\hemma_ed25519`
- Publik: `%USERPROFILE%\\.ssh\\hemma_ed25519.pub`

### WSL

Kör i WSL:

- `ssh-keygen -t ed25519 -f ~/.ssh/hemma_ed25519 -C \"hemma (wsl)\"`
- Säkra permissions:
  - `chmod 700 ~/.ssh`
  - `chmod 600 ~/.ssh/hemma_ed25519`
  - `chmod 644 ~/.ssh/hemma_ed25519.pub`

## Konfigurera `ssh hemma` via SSH config

Skapa/uppdatera din SSH config och lägg in en host-alias `hemma`.

### Windows: `%USERPROFILE%\.ssh\config`

Exempel (justera `User` och `HostName`):

```sshconfig
Host hemma
  HostName <hemma-hostname-eller-tailscale-ip>
  User <ditt-usernamn-på-servern>
  IdentityFile C:/Users/<du>/.ssh/hemma_ed25519
  IdentitiesOnly yes
```

### WSL: `~/.ssh/config`

```sshconfig
Host hemma
  HostName <hemma-hostname-eller-tailscale-ip>
  User <ditt-usernamn-på-servern>
  IdentityFile ~/.ssh/hemma_ed25519
  IdentitiesOnly yes
```

Testa sedan:

- `ssh hemma`

## Verifiera vilken nyckel som används

### 1) Kör med verbose-logg

- Windows: `ssh -vvv hemma`
- WSL: `ssh -vvv hemma`

Leta efter rader som indikerar:

- vilken “identity file” som laddas
- vilken pubkey som “Offering public key: …”
- vilken nyckel som accepteras (“Authentication succeeded (publickey)”)

### 2) Kontrollera vad host-alias faktiskt expanderar till

- Windows: `ssh -G hemma | findstr /i \"hostname user identityfile\"`
- WSL: `ssh -G hemma | egrep -i \"^(hostname|user|identityfile)\"`

### 3) Kontrollera SSH-agent (om du använder agent)

Agent påverkar vilka nycklar som erbjuds automatiskt.

- Lista nycklar i agent:
  - Windows: `ssh-add -l`
  - WSL: `ssh-add -l`
- Töm agent om fel nycklar ligger där:
  - Windows/WSL: `ssh-add -D`

Notera: Windows och WSL har normalt **olika** agent-processer och olika nyckellistor.

## Lägg till pubkey på servern via Taildrop (Tailscale)

Mål: få in din `.pub` i `~/.ssh/authorized_keys` på servern.

### Klient (Windows eller WSL)

1. Leta upp din **publika** nyckel-fil:
   - Windows: `%USERPROFILE%\\.ssh\\hemma_ed25519.pub`
   - WSL: `~/.ssh/hemma_ed25519.pub`
1. Skicka `.pub` till servern med Taildrop (via Tailscale UI eller CLI).

Viktigt:

- Skicka **aldrig** privatnyckeln (utan `.pub`).

### Server (hemma)

1. Hämta Taildrop-filen (plats/kommando kan variera beroende på OS/Tailscale-installation).
1. Lägg till nyckeln:

- `mkdir -p ~/.ssh`
- `chmod 700 ~/.ssh`
- `cat /path/till/mottagen_pubkey.pub >> ~/.ssh/authorized_keys`
- `chmod 600 ~/.ssh/authorized_keys`

1. Verifiera med klienten:

- `ssh -vvv hemma`

## Felsökning

### “REMOTE HOST IDENTIFICATION HAS CHANGED!”

Orsak: host key i `known_hosts` matchar inte längre (ny server, ominstallation, eller MITM-risk).

Åtgärd:

- Verifiera out-of-band att det _ska_ vara ny host key.
- Ta bort gammal hostkey:
  - Windows/WSL: `ssh-keygen -R hemma`
  - eller mot specifikt hostname/IP: `ssh-keygen -R <host>`
- Försök igen: `ssh hemma`

### “Permission denied (publickey).”

Vanliga orsaker:

- Pubkey saknas i `~/.ssh/authorized_keys` på servern.
- Du loggar in med fel `User` (nyckeln ligger på annan användare).
- Du erbjuder fel nyckel (agent eller fel `IdentityFile`).
- Servern tillåter inte den auth-metod du försöker använda.

Snabb isolering:

- Tvinga en specifik nyckel:
  - Windows: `ssh -i $env:USERPROFILE\\.ssh\\hemma_ed25519 -o IdentitiesOnly=yes hemma`
  - WSL: `ssh -i ~/.ssh/hemma_ed25519 -o IdentitiesOnly=yes hemma`
- Kontrollera serverns permissions:
  - `chmod 700 ~/.ssh`
  - `chmod 600 ~/.ssh/authorized_keys`

### “WARNING: UNPROTECTED PRIVATE KEY FILE!”

Vanligt i WSL när permissions är för öppna.

Åtgärd i WSL:

- `chmod 600 ~/.ssh/hemma_ed25519`
- `chmod 700 ~/.ssh`

Om du pekar på en nyckel under `/mnt/c/...`, flytta/kopiera den till `~/.ssh/` och säkra permissions där.

### Fel nyckel används (“wrong key” / erbjuder många keys)

Symptom: `ssh -vvv` visar att den erbjuder andra nycklar än du tänkt.

Åtgärder:

- Sätt `IdentitiesOnly yes` i host-blocket.
- Sätt explicit `IdentityFile ...` i host-blocket.
- Töm agenten: `ssh-add -D`
- Kontrollera att du editerar rätt config-fil (Windows vs WSL).

### Agent-strul (Windows vs WSL)

Symptom: du har lagt till nyckeln med `ssh-add`, men `ssh` hittar den ändå inte (eller tvärtom).

Checklista:

- Kör du `ssh` i Windows eller WSL?
- Kör `ssh-add -l` i _samma_ miljö som du kör `ssh`.
- I WSL: kontrollera `echo $SSH_AUTH_SOCK` (ska peka på en socket).
