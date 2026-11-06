# Main w Merge
M Script in Advanced Editor for PowerQRY
```
let

    // 0. Declare Global Variables, Today := Yesterday due to Dashboards being Historical
    Today = Date.AddDays(Date.From(DateTime.LocalNow()),-1),
    ThisYear = Date.Year(Today),
    ThisMonth = Date.Month(Today),
    // ** important for shifts and full period capture **
    StartOfCurrentMonth = Date.StartOfMonth(Today),
    StartOfCurrentWeek = Date.StartOfWeek(Today, Day.Monday), 

    // 1. Get the Max Date from the FACT table (The Anchor)
    FactSource = Sql.Database("ARTEMIS", "NVS", [Query="SELECT MAX(DateKey) as MaxDate FROM sdrs.vw_F_OfficeDayStats"]),
    // Drill down to get the scalar date value
    FactMaxDate = Date.From(FactSource{0}[MaxDate]),

    // 2. Calculate the "Yesterday" Target and the Shift
    Yesterday = Date.From(DateTime.LocalNow()) - #duration(1, 0, 0, 0),
    RawGap = Duration.Days(Yesterday - FactMaxDate),
    // Multiples of 7 to keep Weekdays (Mon-Thu) consistent for your normalization
    WeekAlignedShift = Number.RoundDown(RawGap / 7) * 7,

    // 3. Load the CALENDAR Table
    CalendarSource = Sql.Database("ARTEMIS", "NVS", [Query="SELECT DateKey, YearMonth FROM sdrs.vw_D_Dates"]),

    // 3b. Rename the original DateKey so we can join data to it
    RenameRaw = Table.RenameColumns(CalendarSource, {{"DateKey", "DateKeyRaw"}}),

    InsertShiftedDate = Table.AddColumn(RenameRaw, "DateKey", each
        Date.AddDays([DateKeyRaw], WeekAlignedShift), 
        type date
        ),

    // 4. Convert 2026 JAN → Current
    AddDynamicLabel = Table.AddColumn(InsertShiftedDate, "YearMonth_Current", each
        let
        // 2. Compare to the shifted DateKey in the Current Row
        RowDate = [DateKey],
        IsCurrent = (Date.Year(RowDate) = ThisYear and Date.Month(RowDate) = ThisMonth)
        in 
            if IsCurrent then "Current Month" else [YearMonth],
        type text  
    ),

    // 5. Create the Sort Column and align "Current Month" to 2999 12
    AddYYYYMM_Sort = Table.AddColumn(AddDynamicLabel, "YYYYMM_Sort", each 
        if [YearMonth_Current] = "Current Month" then "2999 12" 
        else 
            let
                // Use the raw [YearMonth] from step 3 for the sort string logic
                // assuming [YearMonth] looks like "2025 Sep"
                Parts = Text.Split([YearMonth], " "),
                Year = Parts{0},
                MonthName = Parts{1},
                MonthNum = Date.Month(Date.FromText(MonthName & " 1")),
                MonthPad = Text.PadStart(Text.From(MonthNum), 2, "0")
            in 
                Year & " " & MonthPad,
        type text
    ),

    // 7. Add Dynamic Flags
    PrepForTrailing = Table.TransformColumnTypes(AddYYYYMM_Sort, {{"DateKey", type date}}),

    // Int64 for bit instead of "True vs False"
    AddT12 = Table.AddColumn(PrepForTrailing, "IsTrailing12Months", each 
        let 
            T12Start = Date.AddMonths(StartOfCurrentMonth, -12)
        in 
            if [DateKey] >= T12Start and [DateKey] <= Today then 1 else 0, Int64.Type),

    // 3. Add IsTrailingDaily (Last 9 Days including today)
    AddTDaily = Table.AddColumn(AddT12, "IsTrailingDaily", each 
        if [DateKey] >= Date.AddDays(Today, -9) and [DateKey] <= Today then 1 else 0, Int64.Type),

    // 4. Add IsTrailingWeekly (Last 9 Weeks including current week)
    AddTWeekly = Table.AddColumn(AddTDaily, "IsTrailingWeekly", each 
        if [DateKey] >= Date.AddWeeks(StartOfCurrentWeek, -9) and [DateKey] <= Date.EndOfWeek(Today, Day.Monday) then 1 else 0, Int64.Type),

    // 5. Add IsTrailingMonthly (Last 9 Months including current month)
    AddTMonthly = Table.AddColumn(AddTWeekly, "IsTrailingMonthly", each 
        if [DateKey] >= Date.AddMonths(StartOfCurrentMonth, -9) and [DateKey] <= Today then 1 else 0, Int64.Type),

    // 7. hard code change the data types
    #"Changed Type" = Table.TransformColumnTypes(AddTMonthly,{{"DateKey", type date}, {"DateKeyRaw", type date}}),
    #"Reordered Columns" = Table.ReorderColumns(#"Changed Type",{"DateKey", "DateKeyRaw"}),
    #"Removed Columns" = Table.RemoveColumns(#"Reordered Columns",{"YearMonth"}),
    #"Merged Queries" = Table.NestedJoin(#"Removed Columns", {"DateKey"}, D_Dates_RAW, {"DateKey"}, "D_Dates", JoinKind.LeftOuter),
    #"Expanded D_Dates" = Table.ExpandTableColumn(#"Merged Queries", "D_Dates", {"DayOfMonth", "DayOfWeek", "WeekOfYear", "MonthKey", "TotalWDE_byMonth", "MonthNameAbbrev", "YYYY", "MonthForSort", "YearMonth", "MonthYear", "Quarter", "EndOfMonth", "HolidayName", "RollingWDE", "WDE Button"}, {"DayOfMonth", "DayOfWeek", "WeekOfYear", "MonthKey", "TotalWDE_byMonth", "MonthNameAbbrev", "YYYY", "MonthForSort", "YearMonth", "MonthYear", "Quarter", "EndOfMonth", "HolidayName", "RollingWDE", "WDE Button"}),
    #"Filtered Rows" = Table.SelectRows(#"Expanded D_Dates", each [DateKey] < Today)
in
    #"Filtered Rows"
```