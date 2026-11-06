## Install

```powershell
# install
winget search Microsoft.Powershell
winget install --id Microsoft.Powershell --source winget
```

### Backtick vs `>>`
- backtick = next line
- `>>` ps auto line continuation prompt (NOT something I type)

```powershell

Get-ChildItem `
	-Path C:\ `
	-Recurse
```

### Powershell Versions

```
Windows Powershell (native) 5.1.x
Powershell 7 (Core) → 7.x.x
```

