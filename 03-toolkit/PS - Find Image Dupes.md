Scan through F: drives and find dupe files (metadata not just filenames)

```powershell
# 1. Define the path to your external drive and the extensions to look for
$searchPath = "F:\" 
$extensions = @("*.jpg", "*.jpeg", "*.png", "*.mp4", "*.mov", "*.avi", "*.heic")

Write-Host "Scanning $searchPath for duplicates... This may take a while depending on drive speed." -ForegroundColor Cyan

# 2. Get all files with the specified extensions recursively
$files = Get-ChildItem -Path $searchPath -Include $extensions -Recurse -File -ErrorAction SilentlyContinue

# 3. Group files by length (Size) first to speed up the process 
# (Files of different sizes cannot be duplicates, so we only hash files that share the same size)
$potentialDupes = $files | Group-Object Length | Where-Object { $_.Count -gt 1 } | Select-Object -ExpandProperty Group

# 4. Calculate hashes for potential duplicates and group them
$duplicates = $potentialDupes | Get-FileHash -Algorithm MD5 | Group-Object Hash | Where-Object { $_.Count -gt 1 }

# 5. Output the results
if ($duplicates) {
    Write-Host "`nDuplicate Files Found:" -ForegroundColor Yellow
    foreach ($group in $duplicates) {
        Write-Host "--- Group: $($group.Name) ---" -ForegroundColor Green
        $group.Group | Select-Object Path | ForEach-Object { Write-Host $_.Path }
    }
} else {
    Write-Host "No duplicates found." -ForegroundColor Gray
}
```