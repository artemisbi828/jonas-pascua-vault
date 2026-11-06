```shell
# Delete files containing "_history" in the current directory
Get-ChildItem -Path . -File | Where-Object { $_.Name -like "*_history*" } | Remove-Item -Force

Write-Host "Deleted all files containing '_history' in the current directory" -ForegroundColor Green
```

