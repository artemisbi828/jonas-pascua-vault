PS Azure Authentication
#status/deferred/quick-paste-merge-later 

Install-Module -Name Az.Accounts -Scope CurrentUser -Force -AllowClobber

This is happening because **you switched to a "clean" terminal**.

Remember how we opened a separate PowerShell window to fix the SQL DLL conflict?

- **The Bad News:** That clean window is _so_ clean it doesn't even have the Azure commands installed.
    
- **The Good News:** You just need to install the Azure helper module once in this new window.
    


```
Install-Module -Name Az.Accounts -Scope CurrentUser -Force -AllowClobber
```


```
# 1. Load the module we just installed
Import-Module Az.Accounts

# 2. Login
Connect-AzAccount -Force

# 3. Test the token command
$Token = Get-AzAccessToken -ResourceUrl "https://database.windows.net"
Write-Host "Success! Token found." -ForegroundColor Green
```

### Option 1: The "Integrated" Bypass (Try This First)

If your work laptop is signed into the domain/Azure AD, BCP can often use your **Windows Identity** to pass through silently, just like SSMS does.

**The Fix:** Keep `-G`, but **remove** the `-U $User` parameter entirely from the BCP arguments.

- **Change this line:** `"-G", "-U", $User`
    
- **To this:** `"-G"`
    

**Why it works:** When you provide `-G` without a username, BCP attempts "Azure Active Directory Integrated" authentication (Single Sign-On). If your machine allows it, the popups stop immediately.

## BCP HEADER QUERY

```
# --- CONFIG ---
$ServerName = "az-p-sqlmi-fg-01.69bd49c6ce6d.database.windows.net"
$Database = "CentralC9" 
$ExportFolder = "C:\vsWorkspace\db_metadata"
$User = "jonas-adam.pascua@smiledoctors.com"

# YOUR QUERIES
$QueryList = @(
    "select top 200 * from CentralC9.dbo.EasyRxLogin",
    "select top 200 * from CentralC9.dbo.InvisalignLogin"
)

# --- EXECUTION ---

if (!(Test-Path -Path $ExportFolder)) { New-Item -ItemType Directory -Path $ExportFolder | Out-Null }

foreach ($Query in $QueryList) {
    
    # 1. Naming Logic & Temp Paths
    if ($Query -match "FROM\s+([\[\]\w\.]+)") {
        $RawTableName = $Matches[1]
        $CleanName = $RawTableName -replace '\[|\]', '' -replace '\.', '_' 
        $FileName = "$CleanName.csv"
    }
    else {
        $FileName = "Export_$(Get-Date -Format 'yyyyMMdd_HHmmss').csv"
        $RawTableName = $null
    }

    $FinalPath = Join-Path -Path $ExportFolder -ChildPath $FileName
    $TempHeaderPath = Join-Path -Path $ExportFolder -ChildPath "temp_header_$CleanName.csv"
    $TempDataPath   = Join-Path -Path $ExportFolder -ChildPath "temp_data_$CleanName.csv"
    
    Write-Host "Exporting: $CleanName (with Headers)..." -ForegroundColor Cyan

    # --- STEP 2: GET HEADERS (The "Cheat") ---
    # We query sys.columns to get a comma-separated list of column names for this specific table
    if ($RawTableName) {
        # Note: We rely on the Database context in BCP (-d) to find the object ID
        $HeaderQuery = "SELECT STRING_AGG(name, ',') WITHIN GROUP (ORDER BY column_id) FROM sys.columns WHERE object_id = OBJECT_ID('$RawTableName')"
        
        $BcpHeaderArgs = @(
            "`"$HeaderQuery`"", "queryout", "`"$TempHeaderPath`"", "-c", "-t,", "-S", $ServerName, "-d", $Database, "-G", "-U", $User
        )
        Start-Process -FilePath "bcp" -ArgumentList $BcpHeaderArgs -Wait -NoNewWindow
    }

    # --- STEP 3: GET DATA (Your original BCP) ---
    try {
        $BcpDataArgs = @(
            "`"$Query`"", "queryout", "`"$TempDataPath`"", "-c", "-t,", "-S", $ServerName, "-d", $Database, "-G", "-U", $User
        )

        $Process = Start-Process -FilePath "bcp" -ArgumentList $BcpDataArgs -Wait -NoNewWindow -PassThru
        
        if ($Process.ExitCode -eq 0) {
            
            # --- STEP 4: MERGE THEM ---
            # If we successfully grabbed headers, put them on top. Otherwise just output data.
            if (Test-Path $TempHeaderPath) {
                # Combine Header + Data -> Final File
                Get-Content $TempHeaderPath, $TempDataPath | Set-Content $FinalPath
                Write-Host "  -> Headers + Data merged to $FinalPath" -ForegroundColor Green
            }
            else {
                # Fallback if header generation failed
                Move-Item -Path $TempDataPath -Destination $FinalPath -Force
                Write-Host "  -> Data Only (No Headers Found) saved to $FinalPath" -ForegroundColor Yellow
            }

            # Cleanup Temps
            Remove-Item $TempHeaderPath -ErrorAction SilentlyContinue
            Remove-Item $TempDataPath -ErrorAction SilentlyContinue

        } else {
            Write-Host "  -> BCP FAILED. Exit Code: $($Process.ExitCode)" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "  -> ERROR: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "All done!" -ForegroundColor Yellow
```