
```powershell

Get-ChildItem -Directory | ForEach-Object {
    $files = Get-ChildItem -LiteralPath $_.FullName -File
    $size  = ($files | Measure-Object -Property Length -Sum).Sum
    [PSCustomObject]@{

        Folder     = $_.FullName
        FileCount  = $files.Count
        TotalBytes = $size
    }

} | Format-Table -AutoSize
```

