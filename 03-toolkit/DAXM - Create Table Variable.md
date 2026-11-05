```
if [YearMonth_Current] = "Current" then "2999 01" else let Parts = Text.Split([YearMonth_Current], " "), MonthMap = [Jan="01", Feb="02", Mar="03", Apr="04", May="05", Jun="06", Jul="07", Aug="08", Sep="09", Oct="10", Nov="11", Dec="12"] in Parts{0} & " " & Record.Field(MonthMap, Parts{1})
```

```
let
    MonthMap = [Jan="01", Feb="02", Mar="03", Apr="04", May="05", Jun="06", 
                Jul="07", Aug="08", Sep="09", Oct="10", Nov="11", Dec="12"],
    Parts = Text.Split([YearMonth_Current], " "),
    Year = Parts{0},
    MonthKey = Parts{1},
    MonthVal = Record.Field(MonthMap, MonthKey)
in
    Year & " " & MonthVal
```