
```powershell

# Define the name of the new folder
$DestinationFolder = "markdown_files"

# Get the path to the current directory where the script is being executed
$CurrentDirectory = Get-Location

# 1. Create the destination folder if it doesn't already exist
$DestinationPath = Join-Path -Path $CurrentDirectory -ChildPath $DestinationFolder

if (-not (Test-Path -Path $DestinationPath)) {
    Write-Host "Creating destination folder: $DestinationFolder"
    New-Item -Path $DestinationPath -ItemType Directory | Out-Null
}

# 2. Find all files with the .md extension in the current directory and subdirectories
# -Recurse makes it look in subfolders
# -File filters out directories, only listing files
$MarkdownFiles = Get-ChildItem -Path $CurrentDirectory -Recurse -File -Filter "*.md"

# 3. Loop through the found files and move them
if ($MarkdownFiles.Count -gt 0) {
    Write-Host "Found $($MarkdownFiles.Count) markdown files. Moving..."
    
    foreach ($File in $MarkdownFiles) {
        # Construct the full path for the new file location
        $NewFilePath = Join-Path -Path $DestinationPath -ChildPath $File.Name
        
        # Use Move-Item to move the file to the new folder
        # -Force overwrites any existing file with the same name in the destination
        Move-Item -Path $File.FullName -Destination $NewFilePath -Force
        Write-Host "Moved: $($File.Name)" -ForegroundColor Green
    }
    Write-Host "--- Done! All markdown files have been moved to $DestinationFolder ---"
} else {
    Write-Host "No markdown files (.md) found in this directory or subdirectories." -ForegroundColor Yellow
}
```
