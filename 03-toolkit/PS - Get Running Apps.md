
User-visible apps
```powershell
Get-Process |
Where-Object { $_.MainWindowHandle -ne 0 } |
Select-Object ProcessName, Id, MainWindowTitle |
Sort-Object ProcessName

# current user
Get-Process -IncludeUserName |
Where-Object {
    $_.UserName -eq "$env:USERDOMAIN\$env:USERNAME" -and
    $_.MainWindowHandle -ne 0
} |
Select-Object ProcessName, Id, UserName, MainWindowTitle
```

See all
```powershell
Get-Process | Sort-Object ProcessName
```