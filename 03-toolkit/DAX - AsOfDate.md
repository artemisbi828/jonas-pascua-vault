
```shell
AsOfLabel = "As of: " & MIN(D_Dates[MonthKey]) & " - " & EOMONTH(MAX(D_Dates[MonthKey]),0)
```