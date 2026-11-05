
# Find "GIT"
```powershell
$root = (Get-Location).Path
$pending = [System.Collections.Generic.Stack[string]]::new()
$pending.Push($root)

while ($pending.Count -gt 0) {
    $dir = $pending.Pop()

    if (Test-Path -LiteralPath (Join-Path $dir '.git')) {
        $dir
    }

    Get-ChildItem -LiteralPath $dir -Directory -Force -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -ne '.git' } |
        ForEach-Object { $pending.Push($_.FullName) }
}
```