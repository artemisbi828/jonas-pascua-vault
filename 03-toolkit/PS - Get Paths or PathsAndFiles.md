RunAs: 

`.\list-all-paths-recursive.ps1 -Root "F:\00 RAWS\20100101 Panache Legacy\01 Operations\01 music library\02 PVG Piano-Harp-Guitar" -Mode PathsAndFiles -Suffix pdf`

`.\list-all-paths-recursive.ps1 -Root "F:\00 RAWS\20100101 Panache Legacy\01 Operations\01 music library\03 Piano" -Mode PathsOnly -Prefix VCP`

# Script To Save
SaveAs: list-all-paths-recursive.ps1

```
param(
    [Parameter(Mandatory = $true)]
    [string]$Root,

    [ValidateSet("PathsOnly", "PathsAndFiles")]
    [string]$Mode = "PathsOnly",

    [string]$Suffix,
    [string]$Prefix,
    [string]$Contains
)

$resolvedRoot = (Resolve-Path -Path $Root).Path
$hasFilter = [bool]($Suffix -or $Prefix -or $Contains)

Write-Output "Root: $resolvedRoot"

if (-not ($Mode -eq "PathsAndFiles" -and $hasFilter)) {
    Write-Output ""
    Write-Output "Folders:"
    $folderItems = Get-ChildItem -Path $resolvedRoot -Recurse -Directory -Force

    if ($Prefix) {
        $folderItems = $folderItems | Where-Object { $_.Name -like "$Prefix*" }
    }

    if ($Contains) {
        $folderItems = $folderItems | Where-Object { $_.Name -like "*$Contains*" }
    }

    if ($Suffix) {
        $folderItems = $folderItems | Where-Object { $_.Name -like "*$Suffix" }
    }

    $folderItems |
        Sort-Object FullName |
        ForEach-Object { $_.FullName }
}

if ($Mode -eq "PathsAndFiles") {
    Write-Output ""
    Write-Output "Files:"

    $fileItems = Get-ChildItem -Path $resolvedRoot -Recurse -File -Force

    if ($Prefix) {
        $fileItems = $fileItems | Where-Object { $_.Name -like "$Prefix*" }
    }

    if ($Contains) {
        $fileItems = $fileItems | Where-Object { $_.Name -like "*$Contains*" }
    }

    if ($Suffix) {
        $normalizedSuffix = $Suffix.TrimStart('.')
        $fileItems = $fileItems | Where-Object { $_.Extension.TrimStart('.') -eq $normalizedSuffix }
    }

    $fileItems |
        Sort-Object FullName |
        ForEach-Object { $_.FullName }
}
```