Related to: [[DAX - Add WDE and Holiday Columns]]

```
let
    // 1. Setup Date Range
    StartDate = #date(2023, 1, 1),
    EndDate = #date(2026, 12, 31),
    NumberOfDays = Duration.Days(EndDate - StartDate) + 1,
    Dates = List.Dates(StartDate, NumberOfDays, #duration(1, 0, 0, 0)),
    #"Converted to Table" = Table.FromList(Dates, Splitter.SplitByNothing(), {"Date"}),
    #"Changed Type" = Table.TransformColumnTypes(#"Converted to Table",{{"Date", type date}}),

    // 2. Add Calendar Helpers
    #"Added Year" = Table.AddColumn(#"Changed Type", "Year", each Date.Year([Date]), Int64.Type),
    #"Added Month" = Table.AddColumn(#"Added Year", "Month", each Date.Month([Date]), Int64.Type),
    #"Added DayOfWeek" = Table.AddColumn(#"Added Month", "DayOfWeek", each Date.DayOfWeek([Date], Day.Monday), Int64.Type), // 0 = Mon
    #"Added DayOfMonth" = Table.AddColumn(#"Added DayOfWeek", "DayOfMonth", each Date.Day([Date]), Int64.Type),

    // 3. Logic for Floating Holidays
    // Logic: Identify which Monday of the month it is (1st, 2nd, 3rd, etc)
    #"Added Occurrence" = Table.AddColumn(#"Added DayOfMonth", "WeekdayOccurrence", each 
        Number.IntegerDivide([DayOfMonth] - 1, 7) + 1),

    // 4. Identify Holidays (Static and Floating)
    #"Added IsHoliday" = Table.AddColumn(#"Added Occurrence", "IsHoliday", each 
        let 
            m = [Month], d = [DayOfMonth], dow = [DayOfWeek], occ = [WeekdayOccurrence]
        in
            if (m = 1 and d = 1) then true                    // New Year
            else if (m = 1 and dow = 0 and occ = 3) then true // MLK Day (3rd Mon)
            else if (m = 7 and d = 4) then true               // July 4th
            else if (m = 10 and dow = 0 and occ = 2) then true // Indigenous Peoples (2nd Mon)
            else if (m = 11 and d = 11) then true             // Veterans Day
            else if (m = 12 and d = 25) then true             // Christmas
            else false
    ),

    // 5. Apply Custom Weights
    // Mon-Thu (0-3) = 1.0 | Fri-Sun (4-6) = 0.33 | Holiday = 0
    #"Added DayWeight" = Table.AddColumn(#"Added IsHoliday", "DayWeight", each 
        if [IsHoliday] then 0 
        else if [DayOfWeek] <= 3 then 1.0 
        else 0.33, 
        type number
    )
in
    #"Added DayWeight"
```