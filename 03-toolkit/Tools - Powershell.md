---
aliases:
  - PS
  - Powershell
---
1. go to `dir` that has the .ps1 file (make sure it has that extension)
2. call with `.\ps-filename.ps1`

# How to Run
always write in snakecase, although Pascal Case is convention
5.1 project_template_guide.md = snake_case (documentation/data file convention)
5.2 New-ProjectTemplate.ps1 = PascalCase (PowerShell approved verb-noun cmdlet convention)

```
.\new_project_template.ps1 
```


Bash is a scripting language - Bash
[[Tools - Powershell|Powershell]] is an Object Oriented Language - built on .NET runtime, everything is an object, even a string. Piping data → not like "text" like in Linux. Passing live structured "string" object with properties and methods. [Bash] is not, it is a scripting languagge.


# Basic Commands
[[PS - Find folder and get all Parent Dirs that have it]]
[[PS - Instantialize New PS Admin Terminal]]
[[PS - Add Command to Path Environment Variable]]
[[PS - Get Running Apps]]
[[PS - Get Distinct Terminal Commands Passed]]
[[PS - Trigger PS Script]]
[[PS - Trigger PY Script]]
[[PS - Create New Subdir]]
[[PS - Find And Replace Rename Folders]]
[[PS - Get Help]]
[[PS - Clear Host]]
[[PS - Clear Variables, Set Variables]]
[[PS - Pipes]]
[[Tools - Comment Blocks]]
[[PS - Installation + Versions]]
[[PS - Run as Administrator]]
[[PS - Restart Powershell]]
[[PS - Activate Virtual Environment]]
# Command Tools
[[PS - Task Kill]]
[[PS - Start Tasks]]
# Basic Tools
[[PS - Get PnP for Sharepoint]]

# Basic Scripts
[PS - Diagnostics]
[[PS - Generate New GUID]]
[[PS - Get Paths or PathsAndFiles]]
[[PS - Navigate Folders]]
[[PS - Delete Item]]
[[PS - Delete all files that string_pattern]]
[[PS - Move all files into subdir that start_with]]
[PS - Get filenames in dir → output.txt]
[[PS - Get File Counts]]
[[PS - Copy Item for Backup]]
[[PS - Get Content - First 10 Lines]]
[[PS - Edit and Overwrite - Research]]

# Context
[[PS - Parameter - Force]]
# Advanced Tools
[[PS - SQL BCP Header Query]]

```
# 2 lines in 1
cd c:\vsWorkspace\jpascua313\site ; npm start

`                 # new line
;                 # separates as if new line
#                 # comment
<# #>             # multi-line comment
@()               # array
```


# Versions
- Blue is 5 (Native); Black is 7 (Current)
- Terminal > Tab > Settings > Default Open

# Output and Read
```shell
python sql_normalizer.py --input input.txt --output 20251231-1620-QRY2.md 2>&1 | Out-Null ; 
Select-String -Path 20251231-1620-QRY2.md -Pattern "^\| 9a " | Select-Object -First 5
```

```powershell






# copy / move / rename / delete
Copy-Item -Path .\src -Destination 'C:\dest' -Recurse -Force
Copy-Item -Path .\filename.py -Destination .\filename.py.bak  # create backup
Move-Item -Path .\file.txt -Destination 'C:\archive' -Force
Rename-Item -Path .\old.txt -NewName 'new.txt'


# Preview destructive actions
Remove-Item -Path .\temp -Recurse -WhatIf
Rename-Item -Path .\old.txt -NewName 'new.txt' -WhatIf

# use of backtick for readability
Move-Item `
    -Path C:\vsWorkspace\projects_sd\clean_sql_joins.py `
    -Destination C:\vsWorkspace\shared-utils\utils\clean_sql_joins.py

# bool for exists
Test-Path C:\vsWorkspace\shared-utils\utils\clean_sql_joins.py 

Get-Alias cat #define Get-Content

```

## Arrays

```powershell
$Source = 'C:\in'; $Archive = 'C:\archive'; $Error = 'C:\error'
$folders = @($Source, $Archive, $Error)
Write-Output "Count: $($folders.Count)"
Write-Output $folders        # prints each item

```
## Renames
```powershell
# Get all files in the current directory, exclude folders, rename w prefix
$files = Get-ChildItem -File
$prefix = "JONAS_"

foreach ($file in $files) {
    $newName = $prefix + $file.Name
    Rename-Item -Path $file.FullName -NewName $newName
}

Remove-Item *_1.sql    # delete items with "_1.sql" suffix
```


```powershell

# see modules from pip, select only those that have pandas in it
pip freeze | Select-String "pandas"



# backtick is new line


```



# Get Processes, Kill Processes

| command                                              | comment                                                                           |
| ---------------------------------------------------- | --------------------------------------------------------------------------------- |
| tasklist \| findstr /I "lg"<br>                      | list running processes                                                            |
| taskill /F /PID 31516 /PID 31436                     | delete multiple processes                                                         |
| wmic process where "processid='6248'" call terminate | elevated permissions using Windows Management Instrumentation Command-line (WMIC) |
| tasklist /?                                          | get help for tasklist                                                             |


# Create / ensure folder exists

```powershell

New-Item -Path 'C:\a\b\c' -ItemType Directory -Force

# safe pattern: create if missing

if (-not (Test-Path $d)) { New-Item -Path $d -ItemType Directory | Out-Null }

$sub = Join-Path $PWD 'SlideSMS'; if (-not (Test-Path $sub)) { New-Item $sub -ItemType Directory | Out-Null; "Created $sub" } else { "Already exists: $sub" }

```

