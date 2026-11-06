```
let
    // 1. Split the string into a list: {"2025", "Sep"}
    Parts = Text.Split([YearMonth_Current], " "),
    Year = Parts{0},
    MonthName = Parts{1},

    // 2. Convert "Sep" to "09"
    // We create a dummy date to extract the month number
    MonthNum = Date.Month(Date.FromText(MonthName & " 1")),
    MonthPad = Text.PadStart(Text.From(MonthNum), 2, "0"),

    // 3. Combine back together
    Result = Year & " " & MonthPad
in
    Result
```