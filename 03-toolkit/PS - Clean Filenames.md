

```powershell

<#
.SYNOPSIS
    Rename files to follow naming conventions (lowercase, underscores instead of spaces)

.DESCRIPTION
    Recursively scans directories and renames files to:
    - Convert all characters to lowercase
    - Replace spaces with underscores
    - Preview changes before applying them

.USAGE
    # Preview changes only (dry run)
    .\rename_to_conventions.ps1 -DryRun
    
    # Apply changes
    .\rename_to_conventions.ps1
    
    # Scan specific directory
    .\rename_to_conventions.ps1 -Path "C:\MyProject"
#>

param(
    [string]$Path = "C:\vsWorkspace",
    [switch]$DryRun
)

$startTime = Get-Date
Write-Host "`n[1/3] Scanning directory: $Path" -ForegroundColor Cyan
Write-Host "      Mode: $(if ($DryRun) { 'DRY RUN (preview only)' } else { 'APPLY CHANGES' })`n" -ForegroundColor $(if ($DryRun) { 'Yellow' } else { 'Green' })

# Get all files recursively
$files = Get-ChildItem -Path $Path -File -Recurse -ErrorAction SilentlyContinue

Write-Host "[2/3] Analyzing files..." -ForegroundColor Cyan
Write-Host "      Found $($files.Count) files total`n"

$filesToRename = @()
$skippedFiles = @()

foreach ($file in $files) {
    $currentName = $file.Name
    $newName = $currentName.ToLower() -replace ' ', '_'
    
    if ($currentName -ne $newName) {
        $filesToRename += [PSCustomObject]@{
            CurrentPath = $file.FullName
            CurrentName = $currentName
            NewName = $newName
            Directory = $file.DirectoryName
        }
    }
}

Write-Host "[3/3] Processing results..." -ForegroundColor Cyan
Write-Host "      Files needing rename: $($filesToRename.Count)" -ForegroundColor Yellow
Write-Host "      Files already compliant: $($files.Count - $filesToRename.Count)" -ForegroundColor Green
Write-Host ""

if ($filesToRename.Count -eq 0) {
    Write-Host "✓ All files already follow naming conventions!" -ForegroundColor Green
    $duration = (Get-Date) - $startTime
    Write-Host "`nCompleted in $([math]::Round($duration.TotalSeconds, 2)) seconds`n"
    exit 0
}

# Display files that will be renamed
Write-Host "FILES TO RENAME:" -ForegroundColor Yellow
Write-Host ("=" * 80) -ForegroundColor DarkGray

$counter = 0
foreach ($item in $filesToRename) {
    $counter++
    Write-Host "`n[$counter/$($filesToRename.Count)]" -ForegroundColor Cyan
    Write-Host "  File:      $($item.CurrentPath)" -ForegroundColor White
    Write-Host "  Current:   $($item.CurrentName)" -ForegroundColor Red
    Write-Host "  New:       $($item.NewName)" -ForegroundColor Green
}

Write-Host "`n" ("=" * 80) -ForegroundColor DarkGray

if ($DryRun) {
    Write-Host "`n[DRY RUN MODE - No files were modified]" -ForegroundColor Yellow
    Write-Host "Run without -DryRun parameter to apply changes`n" -ForegroundColor Yellow
} else {
    Write-Host "`nApplying changes..." -ForegroundColor Yellow
    
    $renamed = 0
    $errors = 0
    
    foreach ($item in $filesToRename) {
        $newPath = Join-Path $item.Directory $item.NewName
        
        try {
            # Check if target file already exists
            if (Test-Path $newPath) {
                Write-Host "  ⚠ SKIP: Target already exists - $($item.CurrentName)" -ForegroundColor Red
                $errors++
            } else {
                Rename-Item -Path $item.CurrentPath -NewName $item.NewName -ErrorAction Stop
                $renamed++
            }
        } catch {
            Write-Host "  ✗ ERROR: Failed to rename $($item.CurrentName)" -ForegroundColor Red
            Write-Host "    $($_.Exception.Message)" -ForegroundColor Red
            $errors++
        }
    }
    
    Write-Host "`n✓ Successfully renamed: $renamed files" -ForegroundColor Green
    if ($errors -gt 0) {
        Write-Host "✗ Errors/Skipped: $errors files" -ForegroundColor Red
    }
}

$duration = (Get-Date) - $startTime
Write-Host "`nCompleted in $([math]::Round($duration.TotalSeconds, 2)) seconds`n"
```