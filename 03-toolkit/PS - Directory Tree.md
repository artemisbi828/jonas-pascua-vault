

```powershell
<#
.SYNOPSIS
    Generates a visual hierarchy tree of a directory structure.

.DESCRIPTION
    Recursively scans a directory and creates a hierarchical tree view
    in text format showing all folders and files with their sizes.

.PARAMETER Path
    Root directory to scan. Defaults to current directory.

.PARAMETER OutputFileName
    Name of the output hierarchy file. Defaults to "hierarchy.txt".

.PARAMETER ExcludeFolders
    Array of folder names to exclude from the scan. Defaults to common system/build folders.

.EXAMPLE
    .\create_hierarchy_tree.ps1
    Generates hierarchy.txt in the current directory.

.EXAMPLE
    .\create_hierarchy_tree.ps1 -Path "C:\Projects\MyApp"
    Generates hierarchy for a specific project directory.

.EXAMPLE
    .\create_hierarchy_tree.ps1 -OutputFileName "project-structure.txt"
    Generates hierarchy with a custom output filename.
#>

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$Path = (Get-Location).Path,
    
    [Parameter()]
    [string]$OutputFileName = "hierarchy.txt",
    
    [Parameter()]
    [string[]]$ExcludeFolders = @('.git', 'node_modules', '.vs', 'bin', 'obj', '__pycache__', '.venv', 'venv', '__pypackages__')
)

function Get-HierarchyText {
    param(
        [System.IO.DirectoryInfo]$Directory,
        [int]$Depth = 0,
        [string]$Prefix = "",
        [string[]]$ExcludeFolders
    )
    
    $output = @()
    
    # Get all items in current directory
    try {
        $items = Get-ChildItem -Path $Directory.FullName -Force -ErrorAction SilentlyContinue |
            Where-Object { 
                $_.Name -notin $ExcludeFolders -and
                $_.Name -ne $OutputFileName
            } |
            Sort-Object @{Expression = { $_.PSIsContainer }; Descending = $true }, Name
    } catch {
        return $output
    }
    
    for ($i = 0; $i -lt $items.Count; $i++) {
        $item = $items[$i]
        $isLastItem = ($i -eq ($items.Count - 1))
        
        if ($Depth -eq 0) {
            $line = $item.Name
        } else {
            $connector = if ($isLastItem) { "└── " } else { "├── " }
            $line = $Prefix + $connector + $item.Name
        }
        
        # Add file size for files
        if (-not $item.PSIsContainer) {
            $sizeKB = [math]::Round($item.Length / 1KB, 2)
            if ($sizeKB -lt 1) {
                $line += " [$($item.Length) bytes]"
            } elseif ($sizeKB -lt 1024) {
                $line += " [$sizeKB KB]"
            } else {
                $sizeMB = [math]::Round($item.Length / 1MB, 2)
                $line += " [$sizeMB MB]"
            }
        }
        
        $output += $line
        
        # Process subdirectories recursively
        if ($item.PSIsContainer) {
            $newPrefix = if ($Depth -eq 0) { "" } else {
                if ($isLastItem) { $Prefix + "    " } else { $Prefix + "│   " }
            }
            
            $childOutput = Get-HierarchyText -Directory $item -Depth ($Depth + 1) -Prefix $newPrefix -ExcludeFolders $ExcludeFolders
            $output += $childOutput
        }
    }
    
    return $output
}

# Main execution
try {
    Write-Host "`n=== Generate Directory Hierarchy ===" -ForegroundColor Cyan
    Write-Host "Target directory: $Path" -ForegroundColor Gray
    
    # Validate path exists
    if (-not (Test-Path -Path $Path)) {
        Write-Host "✗ Error: Path not found: $Path" -ForegroundColor Red
        exit 1
    }
    
    # Build output path
    $hierarchyPath = Join-Path -Path $Path -ChildPath $OutputFileName
    
    # Scan directory
    Write-Host "`nScanning directory structure..." -ForegroundColor Gray
    $directory = Get-Item -Path $Path
    
    # Generate hierarchy
    Write-Host "Generating hierarchy tree..." -ForegroundColor Gray
    $hierarchy = Get-HierarchyText -Directory $directory -ExcludeFolders $ExcludeFolders
    
    # Count items
    $allItems = Get-ChildItem -Path $Path -Recurse -Force -ErrorAction SilentlyContinue |
        Where-Object {
            $excluded = $false
            foreach ($folder in $ExcludeFolders) {
                if ($_.FullName -match "\\$folder(\\|$)") {
                    $excluded = $true
                    break
                }
            }
            -not $excluded
        }
    
    $totalFolders = ($allItems | Where-Object { $_.PSIsContainer }).Count
    $totalFiles = ($allItems | Where-Object { -not $_.PSIsContainer }).Count
    $totalItems = $allItems.Count
    
    Write-Host "Found: $totalFolders folders, $totalFiles files" -ForegroundColor Cyan
    
    # Add header
    $header = @(
        "# Directory Hierarchy",
        "# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
        "# Source: $Path",
        "# Total Items: $totalItems ($totalFolders folders, $totalFiles files)",
        "# Excluded: $($ExcludeFolders -join ', ')",
        "",
        $directory.Name
    )
    
    $output = $header + $hierarchy
    
    # Save hierarchy file
    $output | Set-Content -Path $hierarchyPath -Encoding UTF8
    Write-Host "✓ Saved: $hierarchyPath" -ForegroundColor Green
    
    # Summary
    Write-Host "`n=== Summary ===" -ForegroundColor Cyan
    Write-Host "Hierarchy file: $hierarchyPath" -ForegroundColor Gray
    Write-Host "Total items included: $totalItems" -ForegroundColor Gray
    Write-Host "  - Folders: $totalFolders" -ForegroundColor Gray
    Write-Host "  - Files: $totalFiles" -ForegroundColor Gray
    Write-Host "`nTo view hierarchy:" -ForegroundColor Gray
    Write-Host "  Get-Content '$hierarchyPath'" -ForegroundColor White
    Write-Host ""
    
} catch {
    Write-Host "`n✗ Error: $_" -ForegroundColor Red
    Write-Host $_.ScriptStackTrace -ForegroundColor Red
    exit 1
}

```