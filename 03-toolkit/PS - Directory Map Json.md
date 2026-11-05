
```powershell
<#
.SYNOPSIS
    Maps directory structure with metadata for project documentation.

.DESCRIPTION
    Recursively scans directories and creates a JSON mapping file with custom
    sort orders, descriptions, and audit information. Maintains metadata across runs.

.PARAMETER Path
    Root directory to map. Defaults to current directory.

.PARAMETER Force
    Skip confirmation prompts and overwrite existing files.

.PARAMETER SkipBackup
    Skip the backup phase (use during development/testing).

.EXAMPLE
    .\Map-Directory.ps1
    Maps the current directory with interactive prompts and creates backup.

.EXAMPLE
    .\Map-Directory.ps1 -Path "C:\Projects\MyApp" -Force
    Maps specified directory without prompts.

.EXAMPLE
    .\Map-Directory.ps1 -SkipBackup
    Maps current directory without creating backup (dev mode).
#>

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$Path = (Get-Location).Path,
    
    [Parameter()]
    [switch]$Force,
    
    [Parameter()]
    [switch]$SkipBackup
)

# Configuration
$script:Config = @{
    DocumentationFolder = "documentation"
    DatabaseScriptsFolder = "database_scripts"
    BackupFolder = "backup"
    MappingFileName = "directory-map.json"
    RenamingLogFileName = "renaming-log.txt"
    MaxDescriptionLength = 200
    LoadSource = "dir_mapper"
    MaxBackupSizeMB = 100  # Maximum size before warning
    LargeFolderThresholdMB = 10  # Folders larger than this will be flagged
    ExcludedFolders = @('.git', 'node_modules', '.vs', 'bin', 'obj', '__pycache__', 'documentation', 'database_scripts', 'backup', '.venv', 'venv', '__pypackages__')
    ExcludedFiles = @('.DS_Store', 'Thumbs.db', 'desktop.ini')
}

$script:RenamingLog = @()

# Helper Functions
function Get-DirectorySize {
    param(
        [string]$Path,
        [string[]]$ExcludeFolders = @()
    )
    
    $totalSize = 0
    $folderSizes = @{}
    
    try {
        $items = Get-ChildItem -Path $Path -Recurse -Force -ErrorAction SilentlyContinue
        
        foreach ($item in $items) {
            # Check if item is in excluded folder
            $excluded = $false
            foreach ($folder in $ExcludeFolders) {
                if ($item.FullName -match "\\$folder(\\|$)") {
                    $excluded = $true
                    break
                }
            }
            
            if (-not $excluded -and -not $item.PSIsContainer) {
                $totalSize += $item.Length
                
                # Track folder sizes
                $parentFolder = $item.DirectoryName
                if (-not $folderSizes.ContainsKey($parentFolder)) {
                    $folderSizes[$parentFolder] = 0
                }
                $folderSizes[$parentFolder] += $item.Length
            }
        }
    } catch {
        Write-Warning "Error calculating size: $_"
    }
    
    return @{
        TotalBytes = $totalSize
        TotalMB = [math]::Round($totalSize / 1MB, 2)
        FolderSizes = $folderSizes
    }
}

function Test-BackupSize {
    param(
        [string]$Path
    )
    
    Write-Host "\nCalculating directory size..." -ForegroundColor Gray
    
    $sizeInfo = Get-DirectorySize -Path $Path -ExcludeFolders $script:Config.ExcludedFolders
    $sizeMB = $sizeInfo.TotalMB
    
    Write-Host "Total size (excluding .venv, node_modules, etc.): $sizeMB MB" -ForegroundColor Cyan
    
    # Check for large folders
    $largeFolders = @()
    foreach ($folder in $sizeInfo.FolderSizes.Keys) {
        $folderSizeMB = [math]::Round($sizeInfo.FolderSizes[$folder] / 1MB, 2)
        if ($folderSizeMB -gt $script:Config.LargeFolderThresholdMB) {
            $relativePath = $folder.Replace($Path, '').TrimStart('\\')
            if (-not $relativePath) { $relativePath = '(root)' }
            $largeFolders += @{
                Path = $relativePath
                SizeMB = $folderSizeMB
            }
        }
    }
    
    # Show large folders
    if ($largeFolders.Count -gt 0) {
        Write-Host "\nLarge folders detected:" -ForegroundColor Yellow
        foreach ($folder in ($largeFolders | Sort-Object -Property SizeMB -Descending | Select-Object -First 5)) {
            Write-Host "  $($folder.Path): $($folder.SizeMB) MB" -ForegroundColor Yellow
        }
    }
    
    # Warn if too large
    if ($sizeMB -gt $script:Config.MaxBackupSizeMB) {
        Write-Host "\n⚠ WARNING: Directory is large ($sizeMB MB)" -ForegroundColor Yellow
        $estimatedSeconds = [math]::Ceiling($sizeMB / 10)  # Rough estimate: 10 MB/sec
        Write-Host "Estimated backup time: ~$estimatedSeconds seconds" -ForegroundColor Yellow
        
        Write-Host "\nOptions:" -ForegroundColor Cyan
        Write-Host "  1. Proceed with backup" -ForegroundColor White
        Write-Host "  2. Skip backup (use -SkipBackup flag next time)" -ForegroundColor White
        Write-Host "  3. Cancel" -ForegroundColor White
        
        $choice = Read-Host "\nEnter choice (1-3)"
        
        switch ($choice) {
            "1" { return $true }
            "2" { return $false }
            default { 
                Write-Host "Cancelled." -ForegroundColor Red
                exit 0
            }
        }
    }
    
    return $true
}

function Backup-Directory {
    param(
        [string]$SourcePath
    )
    
    $backupPath = Join-Path -Path $SourcePath -ChildPath $script:Config.BackupFolder
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupDestination = Join-Path -Path $backupPath -ChildPath $timestamp
    
    # Create backup folder
    if (-not (Test-Path -Path $backupPath)) {
        New-Item -Path $backupPath -ItemType Directory -Force | Out-Null
    }
    
    Write-Host "\nCreating backup..." -ForegroundColor Gray
    New-Item -Path $backupDestination -ItemType Directory -Force | Out-Null
    
    # Copy all items except excluded folders and the backup folder itself
    $items = Get-ChildItem -Path $SourcePath -Force -ErrorAction SilentlyContinue |
        Where-Object { 
            $_.Name -notin $script:Config.ExcludedFolders -and
            $_.Name -ne $script:Config.BackupFolder
        }
    
    $copiedCount = 0
    foreach ($item in $items) {
        try {
            Copy-Item -Path $item.FullName -Destination $backupDestination -Recurse -Force -ErrorAction Stop
            $copiedCount++
        } catch {
            Write-Warning "Could not backup: $($item.Name) - $_"
        }
    }
    
    Write-Host "✓ Backed up $copiedCount items to: $backupDestination" -ForegroundColor Green
    return $backupDestination
}

function ConvertTo-SnakeCase {
    param(
        [string]$FileName
    )
    
    # Split into name and extension
    $extension = [System.IO.Path]::GetExtension($FileName)
    $nameWithoutExt = [System.IO.Path]::GetFileNameWithoutExtension($FileName)
    
    # Remove numeric prefixes (e.g., 00_, 01_, 123_)
    $nameWithoutExt = $nameWithoutExt -replace '^\d+_', ''
    
    # Replace hyphens with underscores
    $nameWithoutExt = $nameWithoutExt -replace '-', '_'
    
    # Convert camelCase and PascalCase to snake_case
    # Insert underscore before uppercase letters that follow lowercase letters
    $nameWithoutExt = $nameWithoutExt -creplace '([a-z])([A-Z])', '$1_$2'
    # Insert underscore before uppercase letters followed by lowercase (for sequences like "XMLParser")
    $nameWithoutExt = $nameWithoutExt -creplace '([A-Z]+)([A-Z][a-z])', '$1_$2'
    
    # Convert to lowercase
    $nameWithoutExt = $nameWithoutExt.ToLower()
    
    # Replace multiple underscores with single underscore
    $nameWithoutExt = $nameWithoutExt -replace '_+', '_'
    
    # Remove leading/trailing underscores
    $nameWithoutExt = $nameWithoutExt.Trim('_')
    
    return $nameWithoutExt + $extension
}

function Get-RelativePath {
    param(
        [string]$FullPath,
        [string]$BasePath
    )
    
    $FullPath = $FullPath.TrimEnd('\')
    $BasePath = $BasePath.TrimEnd('\')
    
    if ($FullPath -eq $BasePath) {
        return "."
    }
    
    if ($FullPath.StartsWith($BasePath)) {
        return $FullPath.Substring($BasePath.Length).TrimStart('\', '/')
    }
    
    return $FullPath
}

function New-FileEntry {
    param(
        [System.IO.FileSystemInfo]$Item,
        [string]$BasePath,
        [hashtable]$ExistingEntry = $null
    )
    
    $relativePath = Get-RelativePath -FullPath $Item.FullName -BasePath $BasePath
    $modified = $Item.LastWriteTime.ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    $now = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
    
    $entry = [ordered]@{
        name = $Item.Name
        type = if ($Item.PSIsContainer) { "folder" } else { "file" }
        path = $relativePath
        sort_order = if ($ExistingEntry -and $ExistingEntry.sort_order) { 
            $ExistingEntry.sort_order 
        } else { 
            999 
        }
        description = if ($ExistingEntry -and $ExistingEntry.description) { 
            $ExistingEntry.description 
        } else { 
            "" 
        }
        load_datetime = $now
        load_source = $script:Config.LoadSource
        loaded_by = $env:USERNAME
        modified_datetime = $modified
    }
    
    if (-not $Item.PSIsContainer) {
        $entry.size_bytes = $Item.Length
    }
    
    $entry.children = @()
    
    return $entry
}

function Move-SqlFiles {
    param(
        [string]$RootPath
    )
    
    $dbScriptsPath = Join-Path -Path $RootPath -ChildPath $script:Config.DatabaseScriptsFolder
    
    # Find all SQL files NOT already in database_scripts folder
    $sqlFiles = Get-ChildItem -Path $RootPath -Recurse -Filter "*.sql" -File -ErrorAction SilentlyContinue |
        Where-Object { 
            $_.DirectoryName -ne $dbScriptsPath -and
            $_.DirectoryName -notmatch '\\documentation$' -and
            $_.DirectoryName -notmatch '\\backup$'
        }
    
    if ($sqlFiles.Count -eq 0) {
        return
    }
    
    # Create database_scripts folder if needed
    if (-not (Test-Path -Path $dbScriptsPath)) {
        New-Item -Path $dbScriptsPath -ItemType Directory -Force | Out-Null
        Write-Host "✓ Created database_scripts folder" -ForegroundColor Green
    }
    
    foreach ($file in $sqlFiles) {
        $newName = ConvertTo-SnakeCase -FileName $file.Name
        $newPath = Join-Path -Path $dbScriptsPath -ChildPath $newName
        
        # Skip if file already exists at destination (don't create duplicates)
        if (Test-Path -Path $newPath) {
            Write-Host "  Skipped: $($file.Name) (already exists in database_scripts)" -ForegroundColor Yellow
            continue
        }
        
        Move-Item -Path $file.FullName -Destination $newPath -Force
        $script:RenamingLog += "Moved: $($file.FullName) -> $newPath"
        Write-Host "  Moved: $($file.Name) -> $(Split-Path -Leaf $newPath)" -ForegroundColor Cyan
    }
}

function Rename-FilesToSnakeCase {
    param(
        [string]$RootPath
    )
    
    # Get all files except in excluded folders
    $files = Get-ChildItem -Path $RootPath -Recurse -File -ErrorAction SilentlyContinue |
        Where-Object {
            $exclude = $false
            foreach ($folder in $script:Config.ExcludedFolders) {
                if ($_.FullName -match "\\$folder\\") {
                    $exclude = $true
                    break
                }
            }
            -not $exclude -and $_.Extension -ne '.sql'
        }
    
    foreach ($file in $files) {
        $newName = ConvertTo-SnakeCase -FileName $file.Name
        
        if ($newName -ne $file.Name) {
            $newPath = Join-Path -Path $file.DirectoryName -ChildPath $newName
            
            # Skip if target already exists
            if (Test-Path -Path $newPath) {
                Write-Host "  Skipped: $($file.Name) (target exists)" -ForegroundColor Yellow
                continue
            }
            
            Rename-Item -Path $file.FullName -NewName $newName -Force
            $script:RenamingLog += "Renamed: $($file.FullName) -> $newName"
            Write-Host "  Renamed: $($file.Name) -> $newName" -ForegroundColor Cyan
        }
    }
}

function Get-DirectoryTree {
    param(
        [string]$RootPath,
        [hashtable]$ExistingMap = @{}
    )
    
    $items = Get-ChildItem -Path $RootPath -Force -ErrorAction SilentlyContinue |
        Where-Object { 
            $_.Name -notin $script:Config.ExcludedFiles -and
            $_.Name -notin $script:Config.ExcludedFolders
        } |
        Sort-Object -Property LastWriteTime -Descending
    
    $entries = @()
    
    foreach ($item in $items) {
        $relativePath = Get-RelativePath -FullPath $item.FullName -BasePath $RootPath
        $existingEntry = $ExistingMap[$relativePath]
        
        $entry = New-FileEntry -Item $item -BasePath $RootPath -ExistingEntry $existingEntry
        
        if ($item.PSIsContainer) {
            $entry.children = @(Get-DirectoryTree -RootPath $item.FullName -ExistingMap $ExistingMap)
        }
        
        $entries += $entry
    }
    
    # Sort by custom sort_order first, then by modified date
    $entries = $entries | Sort-Object -Property @{
        Expression = { if ($_.sort_order -ne 999) { $_.sort_order } else { 9999 } }
    }, @{
        Expression = { $_.modified_datetime }
        Descending = $true
    }
    
    return $entries
}

function ConvertTo-FlatMap {
    param(
        [array]$Tree,
        [hashtable]$Map = @{}
    )
    
    foreach ($entry in $Tree) {
        $Map[$entry.path] = $entry
        
        if ($entry.children -and $entry.children.Count -gt 0) {
            ConvertTo-FlatMap -Tree $entry.children -Map $Map
        }
    }
    
    return $Map
}

function Compare-Mappings {
    param(
        [hashtable]$OldMap,
        [hashtable]$NewMap
    )
    
    $changes = @{
        Added = @()
        Removed = @()
        Modified = @()
    }
    
    # Find added and modified
    foreach ($path in $NewMap.Keys) {
        if (-not $OldMap.ContainsKey($path)) {
            $changes.Added += $path
        } elseif ($NewMap[$path].modified_datetime -ne $OldMap[$path].modified_datetime) {
            $changes.Modified += $path
        }
    }
    
    # Find removed
    foreach ($path in $OldMap.Keys) {
        if (-not $NewMap.ContainsKey($path)) {
            $changes.Removed += $path
        }
    }
    
    return $changes
}

function Show-Changes {
    param(
        [hashtable]$Changes
    )
    
    $hasChanges = $false
    
    if ($Changes.Added.Count -gt 0) {
        $hasChanges = $true
        Write-Host "`n✓ Added ($($Changes.Added.Count)):" -ForegroundColor Green
        foreach ($path in $Changes.Added | Select-Object -First 10) {
            Write-Host "  + $path" -ForegroundColor Green
        }
        if ($Changes.Added.Count -gt 10) {
            Write-Host "  ... and $($Changes.Added.Count - 10) more" -ForegroundColor Gray
        }
    }
    
    if ($Changes.Removed.Count -gt 0) {
        $hasChanges = $true
        Write-Host "`n✗ Removed ($($Changes.Removed.Count)):" -ForegroundColor Red
        foreach ($path in $Changes.Removed | Select-Object -First 10) {
            Write-Host "  - $path" -ForegroundColor Red
        }
        if ($Changes.Removed.Count -gt 10) {
            Write-Host "  ... and $($Changes.Removed.Count - 10) more" -ForegroundColor Gray
        }
    }
    
    if ($Changes.Modified.Count -gt 0) {
        $hasChanges = $true
        Write-Host "`n⟳ Modified ($($Changes.Modified.Count)):" -ForegroundColor Yellow
        foreach ($path in $Changes.Modified | Select-Object -First 10) {
            Write-Host "  ~ $path" -ForegroundColor Yellow
        }
        if ($Changes.Modified.Count -gt 10) {
            Write-Host "  ... and $($Changes.Modified.Count - 10) more" -ForegroundColor Gray
        }
    }
    
    if (-not $hasChanges) {
        Write-Host "`n✓ No changes detected" -ForegroundColor Green
    }
    
    return $hasChanges
}

# Main Script Logic
Write-Host "`n=== Directory Mapper ===" -ForegroundColor Cyan
Write-Host "Scanning: $Path`n" -ForegroundColor Gray

# Validate path
if (-not (Test-Path -Path $Path -PathType Container)) {
    Write-Error "Path not found or is not a directory: $Path"
    exit 1
}

# Backup (unless skipped)
if (-not $SkipBackup) {
    Write-Host "\n=== Backup Phase ==" -ForegroundColor Cyan
    Write-Host "Checking if backup is needed..." -ForegroundColor Gray
    
    $shouldBackup = Test-BackupSize -Path $Path
    
    if ($shouldBackup) {
        Backup-Directory -SourcePath $Path
    } else {
        Write-Host "Skipping backup." -ForegroundColor Yellow
    }
} else {
    Write-Host "\n⚠ Backup skipped (dev mode)" -ForegroundColor Yellow
}

# Process files: rename and organize
Write-Host "Processing files..." -ForegroundColor Gray
Write-Host "Moving SQL files to database_scripts..." -ForegroundColor Gray
Move-SqlFiles -RootPath $Path
Write-Host "Renaming files to snake_case..." -ForegroundColor Gray
Rename-FilesToSnakeCase -RootPath $Path

if ($script:RenamingLog.Count -gt 0) {
    Write-Host "✓ Processed $($script:RenamingLog.Count) files" -ForegroundColor Green
}

# Create documentation folder
$docPath = Join-Path -Path $Path -ChildPath $script:Config.DocumentationFolder
if (-not (Test-Path -Path $docPath)) {
    New-Item -Path $docPath -ItemType Directory -Force | Out-Null
    Write-Host "✓ Created documentation folder" -ForegroundColor Green
}

# Check for existing mapping
$mappingPath = Join-Path -Path $docPath -ChildPath $script:Config.MappingFileName
$isFirstRun = -not (Test-Path -Path $mappingPath)
$existingMap = @{}

if (-not $isFirstRun) {
    Write-Host "Loading existing mapping..." -ForegroundColor Gray
    try {
        $existingJson = Get-Content -Path $mappingPath -Raw | ConvertFrom-Json
        $existingMap = ConvertTo-FlatMap -Tree @($existingJson)
        Write-Host "✓ Loaded $($existingMap.Keys.Count) existing entries" -ForegroundColor Green
    } catch {
        Write-Warning "Could not load existing mapping: $_"
        $isFirstRun = $true
    }
}

# Scan directory
Write-Host "`nScanning directory structure..." -ForegroundColor Gray
$tree = @(Get-DirectoryTree -RootPath $Path -ExistingMap $existingMap)
$newMap = ConvertTo-FlatMap -Tree $tree

Write-Host "✓ Found $($newMap.Keys.Count) items" -ForegroundColor Green

# Compare if not first run
if (-not $isFirstRun) {
    Write-Host "`nComparing with previous mapping..." -ForegroundColor Gray
    $changes = Compare-Mappings -OldMap $existingMap -NewMap $newMap
    $hasChanges = Show-Changes -Changes $changes
    
    if ($hasChanges -and -not $Force) {
        Write-Host ""
        $response = Read-Host "Do you want to update the mapping? (Y/n)"
        if ($response -match '^n') {
            Write-Host "Aborted." -ForegroundColor Yellow
            exit 0
        }
    }
}

# Save mapping
Write-Host "`nSaving mapping file..." -ForegroundColor Gray
$tree | ConvertTo-Json -Depth 100 | Set-Content -Path $mappingPath -Encoding UTF8
Write-Host "✓ Saved: $mappingPath" -ForegroundColor Green

# Save renaming log if there were changes
if ($script:RenamingLog.Count -gt 0) {
    $renamingLogPath = Join-Path -Path $docPath -ChildPath $script:Config.RenamingLogFileName
    $logHeader = "# File Renaming Log - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')", ""
    ($logHeader + $script:RenamingLog) | Set-Content -Path $renamingLogPath -Encoding UTF8
    Write-Host "✓ Saved renaming log: $renamingLogPath" -ForegroundColor Green
}

# First run: Create additional files
if ($isFirstRun) {
    Write-Host "`nFirst run detected - creating additional files..." -ForegroundColor Cyan
    
    # Create requirements.txt if it doesn't exist
    $reqPath = Join-Path -Path $Path -ChildPath "requirements.txt"
    if (-not (Test-Path -Path $reqPath)) {
        @"
# Project Dependencies
# Add your project dependencies here
# Example:
# PowerShell 5.1+
# VS Code + JSON Tools extension (recommended)
"@ | Set-Content -Path $reqPath -Encoding UTF8
        Write-Host "✓ Created: requirements.txt" -ForegroundColor Green
    }
    
    # Create .env.local if it doesn't exist
    $envPath = Join-Path -Path $Path -ChildPath ".env.local"
    if (-not (Test-Path -Path $envPath)) {
        @"
# Local Environment Configuration
# Add your API keys and configuration here
# This file should be added to .gitignore

# Example:
# API_KEY=your_api_key_here
# DATABASE_URL=your_database_url_here
"@ | Set-Content -Path $envPath -Encoding UTF8
        Write-Host "✓ Created: .env.local" -ForegroundColor Green
    }
}

# Summary
Write-Host "`n=== Summary ===" -ForegroundColor Cyan
Write-Host "Mapping file: $mappingPath" -ForegroundColor Gray
Write-Host "`nTo generate hierarchy view:" -ForegroundColor Gray
Write-Host "  .\generate_hierarchy.ps1" -ForegroundColor White
Write-Host "`nTo edit descriptions and sort orders:" -ForegroundColor Gray
Write-Host "  Open '$mappingPath' in VS Code" -ForegroundColor White
Write-Host ""
```