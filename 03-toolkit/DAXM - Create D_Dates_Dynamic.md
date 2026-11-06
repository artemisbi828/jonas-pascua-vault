```
let
    // --- CONSOLIDATED UNIFIED SCRIPT WITH SORTING ---
    
    // 1. Monthly Part
    Part1 = Table.SelectRows(D_Dates, each [IsTrailingMonthly] = 1),
    MonthlyPart = Table.SelectColumns(Table.AddColumn(Part1, "Transform", each [
        DateKey = [DateKey], 
        SlicerType = "Monthly", 
        SlicerRank = 1,
        Axis2 = [YearMonth], // Or use [YYYYMM_Sort] if preferred
        IsCurrent = [IsTrailingMonthly]
    ]), "Transform"),
    
    // 2. Weekly Part
    Part2 = Table.SelectRows(D_Dates, each [IsTrailingWeekly] = 1),
    WeeklyPart = Table.SelectColumns(Table.AddColumn(Part2, "Transform", each 
        let d = [DateKey] in [
        DateKey = d, 
        SlicerType = "Weekly", 
        SlicerRank = 2,
        Axis2 = Text.From(Date.Year(d)) & " W" & Text.PadStart(Text.From(Date.WeekOfYear(d)), 2, "0"),
        IsCurrent = [IsTrailingWeekly]
    ]), "Transform"),

    // 3. Daily Part
    Part3 = Table.SelectRows(D_Dates, each [IsTrailingDaily] = 1),
    DailyPart = Table.SelectColumns(Table.AddColumn(Part3, "Transform", each 
        let d = [DateKey] in [
        DateKey = d, 
        SlicerType = "Daily", 
        SlicerRank = 3,
        Axis2 = "'" & Text.End(Text.From(Date.Year(d)), 2) & " " & Text.From(Date.Month(d)) & "-" & Text.PadStart(Text.From(Date.Day(d)), 2, "0"),
        IsCurrent = [IsTrailingDaily]
    ]), "Transform"),

    // Combine all 3 (The UNION)
    Combined = Table.FromRecords(MonthlyPart[Transform] & WeeklyPart[Transform] & DailyPart[Transform]),
    
    // Final Type Casting
    Typed = Table.TransformColumnTypes(Combined, {
        {"DateKey", type date}, 
        {"SlicerType", type text},
        {"SlicerRank", Int64.Type}, 
        {"IsCurrent", Int64.Type}
    })
in
    Typed
```
