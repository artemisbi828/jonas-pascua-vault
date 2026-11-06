related-to: [[Git - Discard Changes]]
# Basics
```powershell

# get folders
dir 

# alias: dir → Get-ChildItem
dir | Select-String "imm"

cd filename   # alias: cd → Get-Item (ps defined)
cd ..         # one folder up

Get-ChildItem -Path C:\path -File     # files only
Get-ChildItem -Path . -Directory      # folders only
Get-Item C:\path\file.txt             # specific item
(Get-ChildItem -Path . -File).Count   # count files
```


# Advanced
```powershell

#filter to find only the files we need
Get-ChildItem -Recurse -File -Filter "*SD*" # -- can alias Get-ChildItem → dir

# goes through every thing inside, then passes through to select-object to just give the path
Get-ChildItem -Recurse -File -Filter "*tree*" | Select-Object -Unique FullName
Get-ChildItem -Recurse -File | Select-String -Pattern "tree" | Select-Object -Unique Path

# case insensitive 
Get-ChildItem -Recurse -File |
    Where-Object { $_.Name -like "*tree*" } |
    Select-Object -Unique FullName

# case sensitive
Get-ChildItem -Recurse -File |
    Where-Object { $_.Name -clike "*tree*" } |
    Select-Object -Unique FullName
    
# move object
Copy-Item "c:\vsWorkspace_SD\sql_scans\input.txt" "c:\vsWorkspace_SD\sql_scans\sql-scraper-v2\input.txt"

```
