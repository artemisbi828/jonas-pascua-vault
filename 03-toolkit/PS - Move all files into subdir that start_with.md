```shell
# move_edw_files.ps1
# Moves all files starting with "EDW." to a subdirectory called "EDW"

# Create EDW subdirectory if it doesn't exist
$edwDir = ".\EDW"
if (-not (Test-Path $edwDir)) {
    New-Item -ItemType Directory -Path $edwDir | Out-Null
    Write-Host "Created directory: EDW" -ForegroundColor Green
}

# Get files starting with "EDW."
$filesToMove = Get-ChildItem -Path . -File | Where-Object { $_.Name -like "EDW.*" }

if ($filesToMove.Count -eq 0) {
    Write-Host "No files starting with 'EDW.' found in current directory" -ForegroundColor Yellow
    exit
}

Write-Host "Moving $($filesToMove.Count) file(s) to EDW directory..." -ForegroundColor Cyan

foreach ($file in $filesToMove) {
    Move-Item -Path $file.FullName -Destination $edwDir -Force
    Write-Host "  Moved: $($file.Name)" -ForegroundColor Gray
}

Write-Host "`nCompleted! Moved $($filesToMove.Count) file(s) to EDW\" -ForegroundColor Green
```