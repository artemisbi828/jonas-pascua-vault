---
aliases:
  - Refresh Box
---

Accounts for Svc UTC Time Refresh

```DAX
Refresh Check = 
VAR OffsetHours = -6
VAR RefreshUTC =
    CALCULATE ( MAX ( F_LastRefreshed[DataLoad_LastRefreshedDateTime] ) )
VAR RefreshLocalDate =
    DATEVALUE ( RefreshUTC + ( OffsetHours / 24 ) )
VAR LocalToday =
    DATEVALUE ( UTCNOW() + ( OffsetHours / 24 ) )
RETURN
IF ( RefreshLocalDate = LocalToday, "☑", "☒" )
```

