```powershell
$PSVersionTable # check version; # alias: $PSVersionTable → $PSVersionTable.PSVersion (ps defined)
Get-Help Get-Content #tell me what Get-Content does
Get-Help Get-Content -Examples

Get-Command Join-Path | Format-List *
```

Show only the syntax

````powershell

Get-Command Join-Path -Syntax

````

Get built-in help (short / full / examples)

````powershell

Get-Help Join-Path              # short summary + syntax
Get-Help Join-Path -Full        # full help text (parameters, details)
Get-Help Join-Path -Examples    # focused examples
Get-Help Join-Path -Online      # opens Microsoft docs in your browser (if available)

````

View parameter details

````powershell
Get-Help Join-Path -Parameter Path
````

If help is missing, update local help (requires admin & internet)

````powershell
Update-Help
````

Inspect runtime behavior / output type

````powershell

# see the .NET type returned by Join-Path
'base','sub' | ForEach-Object { Join-Path 'C:\base' $_ } | Get-Member
````

If Join-Path were a function or script you could see its body:

````powershell
(Get-Command Join-Path -ErrorAction SilentlyContinue).Definition
````

Quick example usage

````powershell

Join-Path 'C:\folder' 'sub\file.txt'    # -> C:\folder\sub\file.txt
Join-Path 'C:\folder' '..\other'        # -> resolves .. in path string (no filesystem lookup)

````