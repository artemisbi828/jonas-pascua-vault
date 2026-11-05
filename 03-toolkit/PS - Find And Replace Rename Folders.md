# Simple
1. delete `-WhatIf` once ready to go
2. 
```powershell
$root = (Get-Location).Path
$find = "--"
$replace = "-"

Get-ChildItem -LiteralPath $root -Directory |
Where-Object { $_.Name -like "*$find*" } |
ForEach-Object {
    $newName = $_.Name -replace [regex]::Escape($find), $replace
    Rename-Item -LiteralPath $_.FullName -NewName $newName -WhatIf
}
```

# Complex
```powershell
function Rename-FoldersFindReplace {
    [CmdletBinding(SupportsShouldProcess=$true)]
    param(
        # Root folder (defaults to current directory)
        [Parameter()]
        [string]$Root = (Get-Location).Path,

        # Find string or regex pattern
        [Parameter(Mandatory)]
        [string]$Find,

        # Replacement string
        [Parameter(Mandatory)]
        [string]$Replace,

        # Recurse into subfolders
        [switch]$Recurse,

        # Treat $Find as regex pattern instead of literal string
        [switch]$Regex,

        # Skip if the destination folder name already exists
        [switch]$SkipCollisions
    )

    $gciParams = @{
        LiteralPath = $Root
        Directory   = $true
    }
    if ($Recurse) { $gciParams.Recurse = $true }

    $items = Get-ChildItem @gciParams

    # If not regex, escape the find string so special regex chars are treated literally
    $pattern = if ($Regex) { $Find } else { [regex]::Escape($Find) }

    $items |
    Where-Object { $_.Name -match $pattern } |
    Sort-Object { $_.FullName.Length } -Descending |
    ForEach-Object {
        $newName = $_.Name -replace $pattern, $Replace

        # no-op guard
        if ($newName -eq $_.Name) { return }

        $targetPath = Join-Path -Path $_.Parent.FullName -ChildPath $newName

        if ($SkipCollisions -and (Test-Path -LiteralPath $targetPath)) {
            Write-Warning "SKIP (collision): '$($_.FullName)' -> '$targetPath'"
            return
        }

        if ($PSCmdlet.ShouldProcess($_.FullName, "Rename folder to '$newName'")) {
            Rename-Item -LiteralPath $_.FullName -NewName $newName
        }
    }
}

```

# Learning
2026-03-11 03:20 PM

```powershell
 cd "C:\Users\jonas-adam.pascua\OneDrive - Smile Doctors, LLC\Documents\SQL Server Management Studio\WORKBENCH"
$root = Get-Location

Get-ChildItem -LiteralPath $root -Directory |
Where-Object { $_.Name -like "*--*" } |
ForEach-Object {
    $newName = $_.Name -replace "--", "-"
    Rename-Item -LiteralPath $_.FullName -NewName $newName}  
```

```
$root = Get-Location $find = "_--_" $replace = ""

Get-ChildItem -LiteralPath $root -Directory | Where-Object { $_.Name -like $find } | ForEach-Object { $newName = $_.Name -replace $find, $replace Rename-Item -LiteralPath $_.FullName -NewName $newName}
```

What’s wrong with your script?
1) You’re mixing wildcard matching with regex replacement

-like uses wildcards (*), so $find="*--*" is fine for filtering names that contain --.
But -replace uses regex, not wildcards.
So $_ .Name -replace $find, $replace treats *--* as a regex pattern, where * means “repeat previous token,” and this will either error or behave unexpectedly.

2) Your $replace = "" would remove the whole match (and could blank names)
If your -replace pattern matched the entire string, you’d end up with an empty folder name, which isn’t valid. For -- → -, your replacement should be "-", not "".