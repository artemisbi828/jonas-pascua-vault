
SQLPS

Assuming "it" refers to the **SQL Server PowerShell module** (required for the script I gave you in the previous step), here is how to check.

### 1. Check for the Module (The Script Dependency)

Run this command in PowerShell. If it returns data, you have it. If it returns nothing, you don't.

PowerShell

```
Get-Module -ListAvailable -Name SqlServer
```

**What to look for:**

- **Version:** If you see version `21.x` or higher, you are golden.
    
- **Version 1.0 (SQLPS):** If you only see `SQLPS`, that is the old, deprecated version. You should install the new one (`Install-Module -Name SqlServer`).
    

---

### 2. Check for the Application (SSMS)

If "it" meant the actual **SSMS application** (to see if SSMS 21/20 is on the box), PowerShell can check the installation path or registry.1

The "Quick & Dirty" Path Check:

SSMS is a 32-bit app (even on 64-bit Windows), so it usually lives in Program Files (x86).

PowerShell

```
Test-Path "C:\Program Files (x86)\Microsoft SQL Server Management Studio 21\Common7\IDE\Ssms.exe"
```

_(Note: As of late 2025, SSMS 21 is the bleeding edge. If that returns `False`, try changing `21` to `20` or `19` in the path)._

The "Registry" Way (More Accurate):

This checks the uninstall list to see exactly what is registered.

PowerShell

```
Get-ItemProperty HKLM:\Software\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\* | 
Select-Object DisplayName, DisplayVersion | 
Where-Object { $_.DisplayName -like "*SQL Server Management Studio*" }
```