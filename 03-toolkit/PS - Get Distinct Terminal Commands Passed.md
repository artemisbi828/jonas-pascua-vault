
```bash
Get-History |
  Select-Object -ExpandProperty CommandLine |
  Where-Object { $_ -and $_.Trim() } |
  Sort-Object -Unique |
  Set-Content -Encoding UTF8 .\distinct-commands.session.txt
```

---
Yes — **as long as your session history exists** (either via PowerShell’s built-in history or PSReadLine), you can export **distinct commands** pretty easily.

Below are the reliable ways, with “copy/paste-ready” commands.

***

## 1) From the current session: `Get-History` (works everywhere, but limited)

This pulls the in-memory history for the current PowerShell session (and sometimes only what *PowerShell* recorded, not necessarily every interactive line depending on host/config).

### Export distinct command *lines* from this session

```powershell
Get-History |
  Select-Object -ExpandProperty CommandLine |
  Where-Object { $_ -and $_.Trim() } |
  Sort-Object -Unique |
  Set-Content -Encoding UTF8 .\distinct-commands.session.txt
```

### If you want just the command “verb-noun” (first token) distinct

Useful when you want a list like `git`, `kubectl`, `Get-Item`, etc.

```powershell
Get-History |
  Select-Object -ExpandProperty CommandLine |
  ForEach-Object { ($_ -split '\s+')[0] } |
  Where-Object { $_ -and $_.Trim() } |
  Sort-Object -Unique |
  Set-Content -Encoding UTF8 .\distinct-first-token.session.txt
```

> **Note:** `Get-History` can miss some lines in some hosts, and it won’t include commands from previous sessions unless you explicitly load them.

***

## 2) Best for interactive terminals: PSReadLine history (usually complete)

If you’re using PowerShell 7+ interactively, **PSReadLine** typically records what you type and persists it to a history file.

### Export distinct commands from your PSReadLine history file

```powershell
$path = (Get-PSReadLineOption).HistorySavePath

Get-Content $path |
  Where-Object { $_ -and $_.Trim() } |
  Sort-Object -Unique |
  Set-Content -Encoding UTF8 .\distinct-commands.psreadline.txt
```

### Restrict to “commands used in this session only”

PSReadLine history is usually **across sessions**, so if you only want “this session”, do this:

```powershell
# Capture the starting length at session start (run once at beginning)
$script:HistoryStart = (Get-Content (Get-PSReadLineOption).HistorySavePath).Count
```

Then later, export only the new lines:

```powershell
$path = (Get-PSReadLineOption).HistorySavePath
$all  = Get-Content $path
$sessionOnly = $all[$script:HistoryStart..($all.Count-1)]

$sessionOnly |
  Where-Object { $_ -and $_.Trim() } |
  Sort-Object -Unique |
  Set-Content -Encoding UTF8 .\distinct-commands.this-session.txt
```

> If you didn’t capture `$HistoryStart` at the beginning, you can’t perfectly reconstruct “this session only” from the PSReadLine file after the fact — because it’s append-only and spans sessions.

***

## 3) Include **native commands** (git, az, terraform, etc.) too?

Both methods above include whatever was typed as a command line.  
But if your aim is “distinct executables invoked” (e.g., just `git`, `az`, `terraform`), use:

```powershell
$path = (Get-PSReadLineOption).HistorySavePath

Get-Content $path |
  ForEach-Object { ($_ -split '\s+')[0] } |
  Where-Object { $_ -and $_.Trim() } |
  Sort-Object -Unique |
  Set-Content -Encoding UTF8 .\distinct-tools.txt
```

***

## 4) Export as CSV (handy for analysis)

### CSV of distinct commands + count (frequency)

```powershell
Get-History |
  Group-Object -Property CommandLine |
  Sort-Object Count -Descending |
  Select-Object @{n='Count';e={$_.Count}}, @{n='CommandLine';e={$_.Name}} |
  Export-Csv .\commands.frequency.session.csv -NoTypeInformation -Encoding UTF8
```

For PSReadLine (usually better coverage):

```powershell
$path = (Get-PSReadLineOption).HistorySavePath

Get-Content $path |
  Group-Object |
  Sort-Object Count -Descending |
  Select-Object @{n='Count';e={$_.Count}}, @{n='CommandLine';e={$_.Name}} |
  Export-Csv .\commands.frequency.psreadline.csv -NoTypeInformation -Encoding UTF8
```

***

## Gotchas / “why is my list incomplete?”

*   **PSReadLine might be disabled** in some non-interactive hosts, remoting, or constrained environments.
*   **History saving settings** can limit what is persisted.
*   Some commands executed via scripts won’t appear as “typed commands” unless you typed them.

If you want, I can give you a 10‑second diagnostic to tell which history source is authoritative in your setup:

```powershell
$PSVersionTable.PSVersion
Get-Module PSReadLine
(Get-PSReadLineOption).HistorySavePath
(Get-History | Measure-Object).Count
```

***

### Quick question (so I give you the exact best one-liner)

Do you mean **distinct full command lines** (including args), or **distinct command names/tools** (first token like `git`, `uv`, `Get-ChildItem`)?
